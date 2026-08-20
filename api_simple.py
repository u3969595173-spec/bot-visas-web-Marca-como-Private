"""
API REST - Capital Trade Iberia
Simple y funcional
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-muy-segura-aqui")
ALGORITHM = "HS256"
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Capital Trade Iberia API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# ============================================================================
# MODELOS
# ============================================================================
class InversorRegistroRequest(BaseModel):
    nombre: str
    email: str
    password: str
    telefono: str = ""
    pais: str = "España"

class InversorLoginRequest(BaseModel):
    email: str
    password: str

class AportacionRequest(BaseModel):
    inversor_id: int
    nombre: str
    email: str
    importe: float
    moneda: str
    estado: str = "Pendiente de validación"

class RetiroRequest(BaseModel):
    inversor_id: int
    nombre: str
    email: str
    importe: float
    moneda: str
    estado: str = "Pendiente de validación"

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================
def crear_token(data: dict):
    """Crea JWT token"""
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(days=30)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(token: str):
    """Verifica JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obtiene usuario desde JWT token"""
    token = credentials.credentials
    payload = verificar_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    return payload

# ============================================================================
# ENDPOINTS - AUTENTICACIÓN
# ============================================================================

@app.post("/api/inversores/registro")
async def registro_inversor(datos: InversorRegistroRequest):
    """Registra un nuevo inversor"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        # Crear tabla si no existe
        cur.execute("""
            CREATE TABLE IF NOT EXISTS inversores (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(200) NOT NULL,
                email VARCHAR(200) UNIQUE NOT NULL,
                telefono VARCHAR(50),
                pais VARCHAR(100) DEFAULT 'España',
                password_hash VARCHAR(255) NOT NULL,
                estado VARCHAR(50) DEFAULT 'pendiente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        # Hashear password
        password_hash = bcrypt.hashpw(datos.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insertar inversor
        cur.execute("""
            INSERT INTO inversores (nombre, email, telefono, pais, password_hash)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (datos.nombre, datos.email, datos.telefono, datos.pais, password_hash))
        
        inversor_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        token = crear_token({"inversor_id": inversor_id, "email": datos.email, "rol": "inversor"})

        return {
            "token": token,
            "tipo": "Bearer",
            "inversor": {"id": inversor_id, "nombre": datos.nombre, "email": datos.email}
        }
    except psycopg2.IntegrityError:
        raise HTTPException(status_code=400, detail="Email ya existe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/inversores/login")
async def login_inversor(datos: InversorLoginRequest):
    """Login de inversor"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("SELECT id, nombre, email, password_hash FROM inversores WHERE email = %s", 
                   (datos.email.lower(),))
        result = cur.fetchone()
        
        if not result or not bcrypt.checkpw(datos.password.encode('utf-8'), result[3].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

        inversor_id, nombre, email, _ = result
        token = crear_token({"inversor_id": inversor_id, "email": email, "rol": "inversor"})
        
        cur.close()
        conn.close()

        return {
            "token": token,
            "tipo": "Bearer",
            "inversor": {"id": inversor_id, "nombre": nombre, "email": email}
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/inversores/perfil")
async def get_perfil(usuario=Depends(obtener_usuario_actual)):
    """Devuelve el perfil completo del inversor autenticado"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""
            ALTER TABLE inversores
            ADD COLUMN IF NOT EXISTS foto_perfil TEXT,
            ADD COLUMN IF NOT EXISTS foto_portada TEXT
        """)
        conn.commit()
        cur.execute(
            "SELECT id, nombre, email, telefono, pais, estado, foto_perfil, foto_portada FROM inversores WHERE id = %s",
            (usuario.get("inversor_id"),)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Inversor no encontrado")
        return {
            "id": row[0], "nombre": row[1], "email": row[2],
            "telefono": row[3], "pais": row[4], "estado": row[5],
            "foto_perfil": row[6], "foto_portada": row[7]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


class FotoRequest(BaseModel):
    foto: str  # base64 data URL


@app.put("/api/inversores/perfil/foto")
async def update_foto_perfil(datos: FotoRequest, usuario=Depends(obtener_usuario_actual)):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("UPDATE inversores SET foto_perfil = %s WHERE id = %s",
                    (datos.foto, usuario.get("inversor_id")))
        conn.commit()
        cur.close()
        conn.close()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/inversores/perfil/portada")
async def update_foto_portada(datos: FotoRequest, usuario=Depends(obtener_usuario_actual)):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("UPDATE inversores SET foto_portada = %s WHERE id = %s",
                    (datos.foto, usuario.get("inversor_id")))
        conn.commit()
        cur.close()
        conn.close()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/admin/login")
async def admin_login(datos: dict):
    """Login de admin"""
    usuario = datos.get("usuario", "")
    password = datos.get("password", "")
    ADMIN_USER = os.getenv("ADMIN_USUARIO", "admin")
    ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "")
    
    if usuario != ADMIN_USER or password != ADMIN_PASS:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = crear_token({"usuario": ADMIN_USER, "email": "admin@capitaltrade.com", "rol": "admin"})
    
    return {
        "token": token,
        "tipo": "Bearer",
        "usuario": "Administrador",
        "rol": "admin"
    }


# ============================================================================
# ENDPOINTS - CONFIGURACIÓN DE PAGOS (MLC / CUP / USDT BEP-20)
# ============================================================================

METODOS_DEFAULT = [
    {"moneda": "MLC",        "tipo": "tarjeta", "titular": "", "numero": "", "banco": "", "instrucciones": ""},
    {"moneda": "CUP",        "tipo": "tarjeta", "titular": "", "numero": "", "banco": "", "instrucciones": ""},
    {"moneda": "USDT BEP-20","tipo": "wallet",  "wallet":  "", "red": "BEP-20 (BSC)", "instrucciones": ""},
]

def _ensure_config_table(cur, conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS configuracion_pagos (
            id SERIAL PRIMARY KEY,
            clave VARCHAR(100) UNIQUE NOT NULL,
            valor TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


@app.get("/api/admin/config")
async def get_config(usuario=Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Solo admins")
    return {"minimos": {"MLC": 100, "CUP": 500, "USDT BEP-20": 50}}


@app.get("/api/admin/cuentas")
async def get_cuentas(usuario=Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Solo admins")
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        _ensure_config_table(cur, conn)
        cur.execute("SELECT valor FROM configuracion_pagos WHERE clave = 'metodos_pago'")
        row = cur.fetchone()
        cur.close(); conn.close()
        if row:
            import json
            return {"cuentas": json.loads(row[0])}
        return {"cuentas": METODOS_DEFAULT}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/admin/cuentas")
async def update_cuentas(datos: dict, usuario=Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Solo admins")
    try:
        import json
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        _ensure_config_table(cur, conn)
        valor = json.dumps(datos.get("cuentas", []))
        cur.execute("""
            INSERT INTO configuracion_pagos (clave, valor) VALUES ('metodos_pago', %s)
            ON CONFLICT (clave) DO UPDATE SET valor = %s, updated_at = NOW()
        """, (valor, valor))
        conn.commit()
        cur.close(); conn.close()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metodos-pago")
async def get_metodos_publico():
    """Para inversores: ver métodos de pago disponibles (sin auth)"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        _ensure_config_table(cur, conn)
        cur.execute("SELECT valor FROM configuracion_pagos WHERE clave = 'metodos_pago'")
        row = cur.fetchone()
        cur.close(); conn.close()
        if row:
            import json
            return {"metodos": json.loads(row[0])}
        return {"metodos": METODOS_DEFAULT}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS - APORTACIONES
# ============================================================================

@app.post("/api/aportaciones")
async def crear_aportacion(datos: AportacionRequest, usuario = Depends(obtener_usuario_actual)):
    """Crea una aportación"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS aportaciones (
                id SERIAL PRIMARY KEY,
                inversor_id INT,
                nombre VARCHAR(200),
                email VARCHAR(200),
                importe DECIMAL(12,2),
                moneda VARCHAR(10),
                estado VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        cur.execute("""
            INSERT INTO aportaciones (inversor_id, nombre, email, importe, moneda, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (datos.inversor_id, datos.nombre, datos.email, datos.importe, datos.moneda, datos.estado))
        
        aportacion_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {"id": aportacion_id, "importe": datos.importe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/aportaciones")
async def obtener_aportaciones(usuario = Depends(obtener_usuario_actual)):
    """Obtiene aportaciones (admin ve todas, inversor ve suyas)"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        if usuario.get('rol') == 'admin':
            cur.execute("SELECT id, inversor_id, nombre, email, importe, moneda, estado, created_at FROM aportaciones ORDER BY created_at DESC")
        else:
            inversor_id = usuario.get('inversor_id')
            cur.execute("SELECT id, inversor_id, nombre, email, importe, moneda, estado, created_at FROM aportaciones WHERE inversor_id = %s ORDER BY created_at DESC", (inversor_id,))
        
        resultados = cur.fetchall()
        cur.close()
        conn.close()

        aportaciones = []
        for row in resultados:
            aportaciones.append({
                "id": row[0],
                "inversor_id": row[1],
                "nombre": row[2],
                "email": row[3],
                "importe": float(row[4]),
                "moneda": row[5],
                "estado": row[6],
                "fecha": row[7].isoformat() if row[7] else None
            })

        return {"aportaciones": aportaciones}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/aportaciones/{aportacion_id}")
async def actualizar_aportacion(aportacion_id: int, datos: dict, usuario = Depends(obtener_usuario_actual)):
    """Actualiza estado de aportación (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("UPDATE aportaciones SET estado = %s WHERE id = %s", (datos.get('estado'), aportacion_id))
        conn.commit()
        cur.close()
        conn.close()

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - RETIROS
# ============================================================================

@app.post("/api/retiros")
async def crear_retiro(datos: RetiroRequest, usuario = Depends(obtener_usuario_actual)):
    """Crea un retiro"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS retiros (
                id SERIAL PRIMARY KEY,
                inversor_id INT,
                nombre VARCHAR(200),
                email VARCHAR(200),
                importe DECIMAL(12,2),
                moneda VARCHAR(10),
                estado VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        cur.execute("""
            INSERT INTO retiros (inversor_id, nombre, email, importe, moneda, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (datos.inversor_id, datos.nombre, datos.email, datos.importe, datos.moneda, datos.estado))
        
        retiro_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {"id": retiro_id, "importe": datos.importe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/retiros")
async def obtener_retiros(usuario = Depends(obtener_usuario_actual)):
    """Obtiene retiros (admin ve todas, inversor ve suyas)"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        if usuario.get('rol') == 'admin':
            cur.execute("SELECT id, inversor_id, nombre, email, importe, moneda, estado, created_at FROM retiros ORDER BY created_at DESC")
        else:
            inversor_id = usuario.get('inversor_id')
            cur.execute("SELECT id, inversor_id, nombre, email, importe, moneda, estado, created_at FROM retiros WHERE inversor_id = %s ORDER BY created_at DESC", (inversor_id,))
        
        resultados = cur.fetchall()
        cur.close()
        conn.close()

        retiros = []
        for row in resultados:
            retiros.append({
                "id": row[0],
                "inversor_id": row[1],
                "nombre": row[2],
                "email": row[3],
                "importe": float(row[4]),
                "moneda": row[5],
                "estado": row[6],
                "fecha": row[7].isoformat() if row[7] else None
            })

        return {"retiros": retiros}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/retiros/{retiro_id}")
async def actualizar_retiro(retiro_id: int, datos: dict, usuario = Depends(obtener_usuario_actual)):
    """Actualiza estado de retiro (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("UPDATE retiros SET estado = %s WHERE id = %s", (datos.get('estado'), retiro_id))
        conn.commit()
        cur.close()
        conn.close()

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - INVERSORES
# ============================================================================

@app.get("/api/inversores/pendientes")
async def obtener_inversores_pendientes(usuario = Depends(obtener_usuario_actual)):
    """Obtiene inversores pendientes (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("SELECT id, nombre, email, estado FROM inversores WHERE estado = 'pendiente' ORDER BY id DESC")
        resultados = cur.fetchall()
        cur.close()
        conn.close()

        inversores = []
        for row in resultados:
            inversores.append({
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "estado": row[3]
            })

        return {"inversores": inversores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/inversores/validados")
async def obtener_inversores_validados(usuario = Depends(obtener_usuario_actual)):
    """Obtiene inversores validados (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("SELECT id, nombre, email, estado FROM inversores WHERE estado = 'validada' ORDER BY id DESC")
        resultados = cur.fetchall()
        cur.close()
        conn.close()

        inversores = []
        for row in resultados:
            inversores.append({
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "estado": row[3]
            })

        return {"inversores": inversores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/inversores/{inversor_id}/estado")
async def actualizar_estado_inversor(inversor_id: int, datos: dict, usuario = Depends(obtener_usuario_actual)):
    """Actualiza estado de inversor (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("UPDATE inversores SET estado = %s WHERE id = %s", (datos.get('estado'), inversor_id))
        conn.commit()
        cur.close()
        conn.close()

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - CHAT COMUNIDAD
# ============================================================================

@app.get("/api/comunidad/mensajes")
async def obtener_mensajes(usuario = Depends(obtener_usuario_actual)):
    """Obtiene mensajes del chat comunidad"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS mensajes_comunidad (
                id SERIAL PRIMARY KEY,
                autor_id INT,
                autor_nombre VARCHAR(200),
                autor_rol VARCHAR(50),
                mensaje TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        cur.execute("SELECT id, autor_id, autor_nombre, autor_rol, mensaje, created_at FROM mensajes_comunidad ORDER BY created_at DESC LIMIT 100")
        resultados = cur.fetchall()
        cur.close()
        conn.close()

        mensajes = []
        for row in reversed(resultados):
            mensajes.append({
                "id": row[0],
                "autor_id": row[1],
                "autor_nombre": row[2],
                "autor_rol": row[3],
                "mensaje": row[4],
                "created_at": row[5].isoformat() if row[5] else None
            })

        return {"mensajes": mensajes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/comunidad/mensajes")
async def crear_mensaje(datos: dict, usuario = Depends(obtener_usuario_actual)):
    """Crea un mensaje en el chat comunidad"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        autor_id = usuario.get('inversor_id') or 'admin'
        autor_nombre = usuario.get('email', 'Usuario')
        autor_rol = usuario.get('rol', 'inversor')

        cur.execute("""
            INSERT INTO mensajes_comunidad (autor_id, autor_nombre, autor_rol, mensaje)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (autor_id, autor_nombre, autor_rol, datos.get('mensaje')))
        
        mensaje_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {"id": mensaje_id, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINT - HEALTH CHECK
# ============================================================================

@app.get("/api/health")
async def health_check():
    """Verifica que la API está disponible"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
