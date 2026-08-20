"""
API REST - Capital Trade Iberia
Simple y funcional
"""
from fastapi import FastAPI, Depends, HTTPException, Query, status
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
# ENDPOINTS - SOLICITUDES DE PARTICIPACIÓN (FORMULARIO PÚBLICO)
# ============================================================================
@app.post("/api/solicitudes-participacion")
async def crear_solicitud_participacion(datos: dict):
    """Guarda una solicitud de participación de un usuario no registrado"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes_participacion (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(200),
                email VARCHAR(200),
                telefono VARCHAR(100),
                pais VARCHAR(100),
                importe DECIMAL(12,2),
                moneda VARCHAR(10),
                estado VARCHAR(50) DEFAULT 'Pendiente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        cur.execute("""
            INSERT INTO solicitudes_participacion (nombre, email, telefono, pais, importe, moneda)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            datos.get('nombre', 'Desconocido'), 
            datos.get('email', ''), 
            datos.get('telefono', ''),
            datos.get('pais', ''),
            float(datos.get('importe', 0)),
            datos.get('moneda', 'EUR')
        ))
        
        solicitud_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {"id": solicitud_id, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# ENDPOINTS - JUSTIFICANTES
# ============================================================================

@app.post("/api/solicitudes-inversion/{solicitud_id}/justificante")
async def subir_justificante(solicitud_id: str, datos: dict, usuario=Depends(obtener_usuario_actual)):
    """Sube un justificante en base64 para una solicitud/aportación"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        
        # Guardamos en la base de datos el string base64 completo
        # Idealmente en producción se sube a S3, pero para mantener la simplicidad lo guardamos en BD
        cur.execute("""
            ALTER TABLE aportaciones 
            ADD COLUMN IF NOT EXISTS justificante TEXT
        """)
        conn.commit()

        # Intentamos actualizar asumiendo que solicitud_id es el id de la aportación o creamos una tabla de solicitudes separada
        # Para mantener compatibilidad con la estructura actual, lo guardamos en la tabla aportaciones
        cur.execute("UPDATE aportaciones SET justificante = %s, estado = 'Pendiente revisión' WHERE id = %s", 
                    (datos.get('justificante'), solicitud_id))

        if cur.rowcount == 0:
            # Si no es un id numérico de aportación o no se encontró,
            # lo intentamos guardar en texto crudo por si el frontend manda un string como 'ap-12345'
            cur.execute("""
            CREATE TABLE IF NOT EXISTS justificantes (
                id SERIAL PRIMARY KEY,
                origen_id VARCHAR(100),
                justificante_base64 TEXT,
                nombre_archivo VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            cur.execute("INSERT INTO justificantes (origen_id, justificante_base64, nombre_archivo) VALUES (%s, %s, %s)",
                       (solicitud_id, datos.get('justificante'), datos.get('nombreArchivo', 'documento')))
            
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# ENDPOINTS - OFERTAS PRIVADAS (LÍDERES)
# ============================================================================

class OfertaRequest(BaseModel):
    nombre: str
    descripcion: str
    condiciones: str = ""
    programa: str
    nivel: str = ""
    importeMaximo: float
    importe_maximo: float = 0
    inversorIdEspecial: str = ""

@app.post("/api/ofertas")
async def crear_oferta(datos: OfertaRequest, usuario=Depends(obtener_usuario_actual)):
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ofertas_privadas (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(200),
                descripcion TEXT,
                condiciones TEXT,
                programa VARCHAR(50),
                nivel VARCHAR(50),
                importe_maximo DECIMAL(12,2),
                inversor_id_especial VARCHAR(100),
                progreso_actual DECIMAL(12,2) DEFAULT 0,
                estado VARCHAR(50) DEFAULT 'Activa',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        importe_final = datos.importeMaximo if datos.importeMaximo > 0 else datos.importe_maximo

        cur.execute("""
            INSERT INTO ofertas_privadas (nombre, descripcion, condiciones, programa, nivel, importe_maximo, inversor_id_especial)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id, created_at
        """, (datos.nombre, datos.descripcion, datos.condiciones, datos.programa, datos.nivel, importe_final, datos.inversorIdEspecial))
        
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": row[0], "created_at": row[1].isoformat(), "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/ofertas")
async def obtener_ofertas(usuario=Depends(obtener_usuario_actual)):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        
        cur.execute("SELECT to_regclass('ofertas_privadas')")
        if not cur.fetchone()[0]:
            return {"ofertas": []}

        cur.execute("SELECT id, nombre, descripcion, condiciones, programa, nivel, importe_maximo, inversor_id_especial, progreso_actual, estado, created_at FROM ofertas_privadas ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        ofertas = []
        for row in rows:
            ofertas.append({
                "id": str(row[0]),
                "nombre": row[1],
                "descripcion": row[2],
                "condiciones": row[3],
                "programa": row[4],
                "nivel": row[5],
                "importeMaximo": float(row[6]),
                "inversorIdEspecial": row[7],
                "progresoActual": float(row[8]),
                "estado": row[9],
                "fechaCreacion": row[10].isoformat() if row[10] else None
            })
        return {"ofertas": ofertas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.put("/api/ofertas/{oferta_id}")
async def actualizar_oferta(oferta_id: str, datos: dict, usuario=Depends(obtener_usuario_actual)):
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("UPDATE ofertas_privadas SET estado = %s WHERE id = %s", (datos.get('estado'), oferta_id))
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


class AportacionOfertaRequest(BaseModel):
    ofertaId: str
    inversorNombre: str
    inversorId: str
    importe: float
    comprobante: str = ""

@app.post("/api/ofertas/aportaciones")
async def registrar_aportacion_oferta(datos: AportacionOfertaRequest, usuario=Depends(obtener_usuario_actual)):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ofertas_aportaciones (
                id SERIAL PRIMARY KEY,
                oferta_id VARCHAR(50),
                inversor_id VARCHAR(100),
                inversor_nombre VARCHAR(200),
                importe DECIMAL(12,2),
                comprobante TEXT,
                estado VARCHAR(50) DEFAULT 'Pendiente de validación',
                validador_id VARCHAR(100),
                fecha_validacion TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            INSERT INTO ofertas_aportaciones (oferta_id, inversor_id, inversor_nombre, importe, comprobante)
            VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at
        """, (datos.ofertaId, datos.inversorId, datos.inversorNombre, datos.importe, datos.comprobante))
        
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": str(row[0]), "fecha": row[1].isoformat(), "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/ofertas/aportaciones")
async def obtener_aportaciones_ofertas(usuario=Depends(obtener_usuario_actual)):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        
        cur.execute("SELECT to_regclass('ofertas_aportaciones')")
        if not cur.fetchone()[0]:
            return {"aportaciones": []}

        if usuario.get('rol') == 'admin':
            cur.execute("SELECT id, oferta_id, inversor_id, inversor_nombre, importe, comprobante, estado, validador_id, fecha_validacion, created_at FROM ofertas_aportaciones ORDER BY created_at DESC")
        else:
            inversor = str(usuario.get('inversor_id'))
            cur.execute("SELECT id, oferta_id, inversor_id, inversor_nombre, importe, comprobante, estado, validador_id, fecha_validacion, created_at FROM ofertas_aportaciones WHERE inversor_id = %s ORDER BY created_at DESC", (inversor,))
        
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        aports = []
        for r in rows:
            aports.append({
                "id": str(r[0]),
                "ofertaId": r[1],
                "inversorId": r[2],
                "inversorNombre": r[3],
                "importe": float(r[4]),
                "comprobante": r[5],
                "estado": r[6],
                "validador_id": r[7],
                "fechaValidacion": r[8].isoformat() if r[8] else None,
                "fecha": r[9].isoformat() if r[9] else None
            })
        return {"aportaciones": aports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.put("/api/ofertas/aportaciones/{aportacion_id}")
async def validar_aportacion_oferta(aportacion_id: str, datos: dict, usuario=Depends(obtener_usuario_actual)):
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    estado_final = datos.get('estado')
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("""
            UPDATE ofertas_aportaciones 
            SET estado = %s, validador_id = %s, fecha_validacion = CURRENT_TIMESTAMP 
            WHERE id = %s RETURNING oferta_id, importe
        """, (estado_final, usuario.get('email', 'admin'), aportacion_id))
        
        res = cur.fetchone()
        if not res:
            raise HTTPException(status_code=404, detail="Aportacion no encontrada")
        
        oferta_id, importe = res

        if estado_final == 'Validado':
            cur.execute("""
                UPDATE ofertas_privadas 
                SET progreso_actual = progreso_actual + %s 
                WHERE id = %s RETURNING progreso_actual, importe_maximo
            """, (importe, oferta_id))
            
            of_res = cur.fetchone()
            if of_res:
                progreso, maximo = of_res
                if float(progreso) >= float(maximo):
                    cur.execute("UPDATE ofertas_privadas SET estado = 'Completada' WHERE id = %s", (oferta_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/comunidad/mensajes")
async def obtener_mensajes(privado: bool = Query(False), usuario = Depends(obtener_usuario_actual)):
    """Obtiene mensajes públicos o la conversación privada con el admin."""
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
                destinatario VARCHAR(200),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("ALTER TABLE mensajes_comunidad ADD COLUMN IF NOT EXISTS destinatario VARCHAR(200)")
        conn.commit()

        if privado:
            if usuario.get('rol') == 'admin':
                cur.execute("SELECT id, autor_id, autor_nombre, autor_rol, mensaje, destinatario, created_at FROM mensajes_comunidad WHERE destinatario IS NOT NULL AND destinatario <> '' ORDER BY created_at DESC LIMIT 100")
            else:
                cur.execute("SELECT nombre FROM inversores WHERE id = %s OR email = %s LIMIT 1", (usuario.get('inversor_id'), usuario.get('email', '')))
                inversor = cur.fetchone()
                nombre_inversor = inversor[0] if inversor else ''
                cur.execute("SELECT id, autor_id, autor_nombre, autor_rol, mensaje, destinatario, created_at FROM mensajes_comunidad WHERE autor_id = %s OR destinatario IN ('admin', %s, %s, %s) ORDER BY created_at DESC LIMIT 100", (usuario.get('inversor_id'), usuario.get('email', ''), nombre_inversor, str(usuario.get('inversor_id', ''))))
        else:
            cur.execute("SELECT id, autor_id, autor_nombre, autor_rol, mensaje, destinatario, created_at FROM mensajes_comunidad WHERE destinatario IS NULL OR destinatario = '' ORDER BY created_at DESC LIMIT 100")
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
                "destinatario": row[5],
                "created_at": row[6].isoformat() if row[6] else None
            })

        return {"mensajes": mensajes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/comunidad/mensajes")
async def crear_mensaje(datos: dict, privado: bool = Query(False), usuario = Depends(obtener_usuario_actual)):
    """Crea un mensaje público o privado con el administrador."""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        autor_id = usuario.get('inversor_id') or 0
        autor_nombre = usuario.get('email', 'Usuario')
        autor_rol = usuario.get('rol', 'inversor')

        destinatario = datos.get('destinatario') if privado else None

        cur.execute("""
            INSERT INTO mensajes_comunidad (autor_id, autor_nombre, autor_rol, mensaje, destinatario)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (autor_id, autor_nombre, autor_rol, datos.get('mensaje'), destinatario))
        
        mensaje_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {"id": mensaje_id, "success": True, "private": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/chat-admin/mensajes")
async def obtener_mensajes_chat_admin(usuario = Depends(obtener_usuario_actual)):
    """Obtiene solo la conversación privada entre el inversor y el admin."""
    return await obtener_mensajes(privado=True, usuario=usuario)


@app.post("/api/chat-admin/mensajes")
async def crear_mensaje_chat_admin(datos: dict, usuario = Depends(obtener_usuario_actual)):
    """Guarda un mensaje privado entre el inversor y el admin."""
    return await crear_mensaje(datos, privado=True, usuario=usuario)

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
