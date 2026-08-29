"""
API REST - Capital Trade Iberia
Simple y funcional
"""
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
import os
import uuid
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-muy-segura-aqui")
ALGORITHM = "HS256"
DATABASE_URL = os.getenv("DATABASE_URL")

# Pool de conexiones reutilizables (evita abrir/cerrar una conexion TCP+SSL nueva en cada request)
from psycopg2 import pool as _pg_pool
DB_POOL = None
_FALLBACK_CONN_IDS = set()  # conexiones directas (no del pool) pendientes de cerrar

def get_conn():
    global DB_POOL
    if DB_POOL is None:
        DB_POOL = _pg_pool.ThreadedConnectionPool(1, 30, DATABASE_URL, sslmode="require")
    try:
        return DB_POOL.getconn()
    except _pg_pool.PoolError:
        # Pool agotado momentaneamente: abrir una conexion directa de respaldo
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        _FALLBACK_CONN_IDS.add(id(conn))
        return conn

def release_conn(conn):
    try:
        if id(conn) in _FALLBACK_CONN_IDS:
            _FALLBACK_CONN_IDS.discard(id(conn))
            conn.close()
        elif DB_POOL is not None:
            DB_POOL.putconn(conn)
        else:
            conn.close()
    except Exception:
        pass

app = FastAPI(title="Capital Trade Iberia API")

# CORS - solo dominios reales del frontend, no comodín
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:3005",
        "https://bot-visas-web-marca-como-private.onrender.com",
        "https://bot-visas-web-marca-como-private-s785-g4twzsjhe.vercel.app",
        "https://majestic-souffle-c1d9f9.netlify.app",
        "https://fortunariocash.com",
        "https://www.fortunariocash.com",
        "https://capitaltradeiberia.com",
        "https://www.capitaltradeiberia.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

security = HTTPBearer()

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
# MODELOS
# ============================================================================
class InversorRegistroRequest(BaseModel):
    nombre: str
    email: str
    password: str
    telefono: str = ""
    pais: str = "España"
    codigo_patrocinio: str = ""

class InversorLoginRequest(BaseModel):
    email: str
    password: str

# --- ADMIN ENDPOINT: REPARTIR RENDIMIENTO DIARIO ---
class PayoutRequest(BaseModel):
    porcentaje: float

@app.post("/api/admin/repartir_diario")
async def repartir_diario(datos: PayoutRequest, usuario = Depends(obtener_usuario_actual)):
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS pagos_rentabilidad (
                id SERIAL PRIMARY KEY,
                aportacion_id INT NOT NULL,
                inversor_id INT NOT NULL,
                nombre VARCHAR(200),
                moneda VARCHAR(30) NOT NULL,
                porcentaje DECIMAL(8,4) NOT NULL,
                importe DECIMAL(12,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Buscar todas las aportaciones activas cuyas 72 horas ya vencieron.
        cur.execute("""
                 SELECT id, inversor_id, nombre, importe, moneda, ganancia_rentabilidad,
                     (COALESCE(ganancia_acelerada, 0)) as accel
            FROM aportaciones
            WHERE (estado = 'Aprobada' OR estado = 'Activa') 
              AND fecha_aprobacion IS NOT NULL
              AND fecha_aprobacion + INTERVAL '72 hours' <= CURRENT_TIMESTAMP
        """)
        oportunidades = cur.fetchall()
        
        pagados = 0
        total_repartido = 0
        
        for apo in oportunidades:
            a_id = apo[0]
            inversor_id = apo[1]
            nombre = apo[2]
            importe = float(apo[3])
            moneda = apo[4]
            ganado = float(apo[5] if apo[5] is not None else 0)
            acelerada = float(apo[6])
            
            meta_limite = importe * 3.0
            saldo_pre_pago = ganado + acelerada
            
            if saldo_pre_pago < meta_limite:
                pago_de_hoy = importe * (float(datos.porcentaje) / 100.0)
                nuevo_ganado = ganado + pago_de_hoy
                
                estado = 'Activa'
                if (nuevo_ganado + acelerada) >= meta_limite:
                    # Limitar si se pasó del 300% y expirar
                    nuevo_ganado = meta_limite - acelerada
                    estado = 'Completada (300%)'
                
                cur.execute("""
                    UPDATE aportaciones
                    SET ganancia_rentabilidad = %s, ultima_fecha_pago = CURRENT_DATE, estado = %s
                    WHERE id = %s
                """, (nuevo_ganado, estado, a_id))
                importe_acreditado = nuevo_ganado - ganado
                cur.execute("""
                    INSERT INTO pagos_rentabilidad (aportacion_id, inversor_id, nombre, moneda, porcentaje, importe)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (a_id, inversor_id, nombre, moneda, datos.porcentaje, importe_acreditado))
                pagados += 1
                total_repartido += importe_acreditado

        conn.commit()
        return {"mensaje": f"Reparto completado. {pagados} contratos procesados.", "total_pagado": total_repartido}
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            cur.close()
            release_conn(conn)


@app.get("/api/pagos-rentabilidad")
async def obtener_pagos_rentabilidad(usuario = Depends(obtener_usuario_actual)):
    """Historial de pagos de rentabilidad; el inversor solo ve los propios."""
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pagos_rentabilidad (
                id SERIAL PRIMARY KEY,
                aportacion_id INT NOT NULL,
                inversor_id INT NOT NULL,
                nombre VARCHAR(200),
                moneda VARCHAR(30) NOT NULL,
                porcentaje DECIMAL(8,4) NOT NULL,
                importe DECIMAL(12,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        if usuario.get('rol') == 'admin':
            cur.execute("""
                SELECT id, aportacion_id, inversor_id, nombre, moneda, porcentaje, importe, created_at
                FROM pagos_rentabilidad ORDER BY created_at DESC, id DESC LIMIT 200
            """)
        else:
            cur.execute("""
                SELECT id, aportacion_id, inversor_id, nombre, moneda, porcentaje, importe, created_at
                FROM pagos_rentabilidad WHERE inversor_id = %s ORDER BY created_at DESC, id DESC LIMIT 200
            """, (usuario.get('inversor_id'),))
        pagos = [{
            "id": row[0], "aportacion_id": row[1], "inversor_id": row[2], "nombre": row[3],
            "moneda": row[4], "porcentaje": float(row[5]), "importe": float(row[6]),
            "fecha": row[7].isoformat() if row[7] else None
        } for row in cur.fetchall()]
        conn.commit()
        return {"pagos": pagos}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            cur.close()
            release_conn(conn)

class TransaccionBase(BaseModel):
    inversor_id: int
    nombre: str
    email: str
    importe: float
    moneda: str

class AportacionRequest(TransaccionBase):
    estado: str = "Pendiente de validación"

class RetiroRequest(TransaccionBase):
    estado: str = "Pendiente de validación"

class JustificanteRequest(BaseModel):
    justificante: str
    nombreArchivo: Optional[str] = None
    tipoArchivo: Optional[str] = None


# ============================================================================
# ENDPOINTS - AUTENTICACIÓN
# ============================================================================

@app.post("/api/inversores/registro")
async def registro_inversor(datos: InversorRegistroRequest):
    """Registra un nuevo inversor"""
    try:
        conn = get_conn()
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                referido_por VARCHAR(100),
                codigo_referido VARCHAR(50)
            )
        """)
        conn.commit()

        # Hashear password
        password_hash = bcrypt.hashpw(datos.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insertar inversor (cuenta activa de inmediato, sin validacion manual del admin)
        cur.execute("""
            INSERT INTO inversores (nombre, email, telefono, pais, password_hash, referido_por, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'validada')
            RETURNING id
        """, (datos.nombre, datos.email, datos.telefono, datos.pais, password_hash, datos.codigo_patrocinio))
        
        inversor_id = cur.fetchone()[0]
        
        # Generar su codigo propio tipo ALAN13 para invitar
        codigo_propio = f"{datos.nombre[:3].upper()}{inversor_id}{datos.telefono[-2:] if len(datos.telefono)>2 else '99'}"
        cur.execute("UPDATE inversores SET codigo_referido = %s WHERE id = %s", (codigo_propio, inversor_id))
        
        conn.commit()
        cur.close()
        release_conn(conn)

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
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT id, nombre, email, password_hash, estado FROM inversores WHERE email = %s", 
                   (datos.email.lower(),))
        result = cur.fetchone()
        
        if not result or not bcrypt.checkpw(datos.password.encode('utf-8'), result[3].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

        inversor_id, nombre, email, _, estado = result
        if estado == 'rechazada':
            raise HTTPException(status_code=403, detail="Tu cuenta ha sido rechazada. Contacta con soporte.")
        token = crear_token({"inversor_id": inversor_id, "email": email, "rol": "inversor"})
        
        cur.close()
        release_conn(conn)

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
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            ALTER TABLE inversores
            ADD COLUMN IF NOT EXISTS foto_perfil TEXT,
            ADD COLUMN IF NOT EXISTS foto_portada TEXT
        """)
        conn.commit()
        cur.execute(
            "SELECT id, nombre, email, telefono, pais, estado, foto_perfil, foto_portada, codigo_referido, referido_por FROM inversores WHERE id = %s",
            (usuario.get("inversor_id"),)
        )
        row = cur.fetchone()
        cur.close()
        release_conn(conn)
        if not row:
            raise HTTPException(status_code=404, detail="Inversor no encontrado")
        if row[5] == 'rechazada':
            raise HTTPException(status_code=403, detail="Cuenta rechazada")
        return {
            "id": row[0], "nombre": row[1], "email": row[2],
            "telefono": row[3], "pais": row[4], "estado": row[5],
            "foto_perfil": row[6],
            "foto_portada": row[7],
            "codigo_referido": row[8],
            "referido_por": row[9]
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
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE inversores SET foto_perfil = %s WHERE id = %s",
                    (datos.foto, usuario.get("inversor_id")))
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/inversores/perfil/portada")
async def update_foto_portada(datos: FotoRequest, usuario=Depends(obtener_usuario_actual)):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE inversores SET foto_portada = %s WHERE id = %s",
                    (datos.foto, usuario.get("inversor_id")))
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


class ActualizarPerfilRequest(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    pais: Optional[str] = None


@app.put("/api/inversores/perfil/actualizar")
async def actualizar_perfil_inversor(datos: ActualizarPerfilRequest, usuario=Depends(obtener_usuario_actual)):
    """Actualiza nombre, teléfono y país del inversor autenticado"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE inversores SET
                nombre = COALESCE(%s, nombre),
                telefono = COALESCE(%s, telefono),
                pais = COALESCE(%s, pais)
            WHERE id = %s
        """, (datos.nombre, datos.telefono, datos.pais, usuario.get("inversor_id")))
        conn.commit()
        cur.close()
        release_conn(conn)
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
    {"moneda": "EUR",         "tipo": "iban",   "titular": "", "iban": "", "concepto": "", "instrucciones": ""},
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
    return {"minimos": {"EUR": 500, "USDT BEP-20": 50}}


@app.get("/api/admin/cuentas")
async def get_cuentas(usuario=Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Solo admins")
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_config_table(cur, conn)
        cur.execute("SELECT valor FROM configuracion_pagos WHERE clave = 'metodos_pago'")
        row = cur.fetchone()
        cur.close(); release_conn(conn)
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
        conn = get_conn()
        cur = conn.cursor()
        _ensure_config_table(cur, conn)
        valor = json.dumps(datos.get("cuentas", []))
        cur.execute("""
            INSERT INTO configuracion_pagos (clave, valor) VALUES ('metodos_pago', %s)
            ON CONFLICT (clave) DO UPDATE SET valor = %s, updated_at = NOW()
        """, (valor, valor))
        conn.commit()
        cur.close(); release_conn(conn)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metodos-pago")
async def get_metodos_publico():
    """Para inversores: ver métodos de pago disponibles (sin auth)"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_config_table(cur, conn)
        cur.execute("SELECT valor FROM configuracion_pagos WHERE clave = 'metodos_pago'")
        row = cur.fetchone()
        cur.close(); release_conn(conn)
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
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS aportaciones (
                id SERIAL PRIMARY KEY,
                inversor_id INT,
                nombre VARCHAR(200),
                email VARCHAR(200),
                importe DECIMAL(12,2),
                moneda VARCHAR(30),
                estado VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_aprobacion TIMESTAMP,
                tasa_diaria DECIMAL(5,2),
                ganancia_acelerada DECIMAL(12,2) DEFAULT 0,
                ganancia_rentabilidad DECIMAL(12,2) DEFAULT 0,
                ultima_fecha_pago DATE,
                comprobante_base64 TEXT,
                comprobante_tipo VARCHAR(100)
            )
        """)
        conn.commit()

        cur.execute("""
            ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS comprobante_base64 TEXT;
            ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS comprobante_tipo VARCHAR(100);
        """)
        conn.commit()
        conn.commit()

        cur.execute("""
            INSERT INTO aportaciones (inversor_id, nombre, email, importe, moneda, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (datos.inversor_id, datos.nombre, datos.email, datos.importe, datos.moneda, datos.estado))
        
        aportacion_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        release_conn(conn)

        return {"id": aportacion_id, "importe": datos.importe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/aportaciones/{id}/justificante")
async def subir_justificante(id: int, datos: JustificanteRequest, usuario = Depends(obtener_usuario_actual)):
    """Sube un justificante Base64 a una aportación existente"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Verificar que la aportación exista y sea del usuario (o admin)
        if usuario.get('rol') != 'admin':
            cur.execute("SELECT inversor_id FROM aportaciones WHERE id = %s", (id,))
            resultado = cur.fetchone()
            if not resultado or resultado[0] != usuario.get('inversor_id'):
                raise HTTPException(status_code=403, detail="Aportación no encontrada o no autorizada")

        cur.execute("""
            ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS comprobante_base64 TEXT;
            ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS comprobante_tipo VARCHAR(100);
        """)
        conn.commit()

        cur.execute("""
            UPDATE aportaciones 
            SET comprobante_base64 = %s, comprobante_tipo = %s
            WHERE id = %s
        """, (datos.justificante, datos.tipoArchivo, id))
        
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"mensaje": "Justificante subido correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/aportaciones/{id}/justificante")
async def obtener_justificante(id: int, usuario = Depends(obtener_usuario_actual)):
    """Devuelve el Base64 del justificante para que no cargue la lista general"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Admin ve todo, Inversor solo suyo
        if usuario.get('rol') == 'admin':
             cur.execute("SELECT comprobante_base64, comprobante_tipo FROM aportaciones WHERE id = %s", (id,))
        else:
             cur.execute("SELECT comprobante_base64, comprobante_tipo FROM aportaciones WHERE id = %s AND inversor_id = %s", (id, usuario.get('inversor_id')))
             
        resultado = cur.fetchone()
        cur.close()
        release_conn(conn)
        
        if not resultado:
             raise HTTPException(status_code=404, detail="Justificante no encontrado o sin acceso")
             
        # Si resultado[0] es None, retornar algo vacío o 404
        if not resultado[0]:
             return {"justificante": None}
             
        return {
             "justificante": resultado[0],
             "tipoArchivo": resultado[1]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/aportaciones")
async def obtener_aportaciones(usuario = Depends(obtener_usuario_actual)):
    """Obtiene aportaciones (admin ve todas, inversor ve suyas)"""
    try:
        conn = get_conn()
        cur = conn.cursor()

        if usuario.get('rol') == 'admin':
            cur.execute("SELECT id, inversor_id, nombre, email, importe, moneda, estado, created_at, fecha_aprobacion, ganancia_acelerada, ganancia_rentabilidad, ultima_fecha_pago, comprobante_base64 FROM aportaciones ORDER BY created_at DESC")
        else:
            inversor_id = usuario.get('inversor_id')
            cur.execute("SELECT id, inversor_id, nombre, email, importe, moneda, estado, created_at, fecha_aprobacion, ganancia_acelerada, ganancia_rentabilidad, ultima_fecha_pago, comprobante_base64 FROM aportaciones WHERE inversor_id = %s ORDER BY created_at DESC", (inversor_id,))
        
        resultados = cur.fetchall()
        cur.close()
        release_conn(conn)
        
        aportaciones = []
        for row in resultados:
            aportacion_id = row[0]
            importe = float(row[4])
            estado = row[6]
            fecha = row[7]
            fecha_aprobacion = row[8]
            ganancia_acelerada = float(row[9] or 0)
            ganancia_rentabilidad = float(row[10] or 0)
            
            meta_ganancia = importe * 3.0
            ganancia_acumulada = ganancia_rentabilidad + ganancia_acelerada
            
            # Limitar al 300% exacto
            if ganancia_acumulada >= meta_ganancia:
                ganancia_acumulada = meta_ganancia

            ganancias_disponibles = max(meta_ganancia - ganancia_acumulada, 0)
            
            aportaciones.append({
                "id": aportacion_id,
                "inversor_id": row[1],
                "nombre": row[2],
                "email": row[3],
                "importe": importe,
                "moneda": row[5],
                "estado": estado,
                "fecha": fecha.isoformat() if fecha else None,
                "fecha_aprobacion": fecha_aprobacion.isoformat() if fecha_aprobacion else None,
                "ultima_fecha_pago": row[11].isoformat() if row[11] else None,
                "ganancia_total": ganancia_acumulada,
                "meta_ganancia": meta_ganancia,
                "gananciasDisponibles": ganancias_disponibles,
                "tiene_justificante": row[12] is not None
            })

        return {"aportaciones": aportaciones}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/aportaciones/{aportacion_id}")
async def actualizar_aportacion(aportacion_id: int, datos: dict, usuario = Depends(obtener_usuario_actual)):
    """Actualiza estado de aportación (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        conn = get_conn()
        cur = conn.cursor()

        estado = datos.get('estado')
        tasa_diaria = datos.get('tasa_diaria', 0.5)

        if estado == 'Aprobada' or estado == 'Activa':
            cur.execute("""
                UPDATE aportaciones 
                SET estado = %s, fecha_aprobacion = CURRENT_TIMESTAMP, tasa_diaria = %s 
                WHERE id = %s
                RETURNING inversor_id, importe
            """, (estado, tasa_diaria, aportacion_id))
            
            inversion_data = cur.fetchone()
            if inversion_data:
                # Disparar acelerador para el patrocinador (10% de importe)
                inversor_id, importe = inversion_data
                monto_acelerador = float(importe) * 0.10

                # Buscar si el inversor fue referido por alguien (aún falta la tabla, previendo logica)
                cur.execute("SELECT referido_por FROM inversores WHERE id = %s", (inversor_id,))
                ref_row = cur.fetchone()
                if ref_row and ref_row[0]:
                    patrocinador_codigo = ref_row[0]
                    # Encontrar al patrocinador
                    cur.execute("SELECT id FROM inversores WHERE codigo_referido = %s", (patrocinador_codigo,))
                    patr_row = cur.fetchone()
                    if patr_row:
                        patrocinador_id = patr_row[0]
                        # Repartir acelerador en sus inversiones activas en cascada (FIFO)
                        cur.execute("""
                            SELECT id, importe, COALESCE(ganancia_acelerada, 0) as ganac, COALESCE(ganancia_rentabilidad, 0) as rent, fecha_aprobacion
                            FROM aportaciones 
                            WHERE inversor_id = %s AND (estado = 'Aprobada' OR estado = 'Activa')
                            ORDER BY fecha_aprobacion ASC NULLS LAST, id ASC
                        """, (patrocinador_id,))
                        invs_activas = cur.fetchall()
                        
                        monto_restante = monto_acelerador
                        
                        for inv in invs_activas:
                            if monto_restante <= 0:
                                break
                            
                            inv_id = inv[0]
                            inv_importe = float(inv[1])
                            inv_ganac = float(inv[2])
                            inv_rent = float(inv[3])
                            
                            meta = inv_importe * 3.0
                            
                            # Validar espacio libre teniendo en cuenta TODO lo ganado hasta el momento
                            espacio_libre = meta - (inv_rent + inv_ganac)
                            
                            if espacio_libre > 0:
                                abs_ganado = min(monto_restante, espacio_libre)
                                
                                estado = 'Activa'
                                # Si este pago llena la meta al 300%, completamos el contrato.
                                if (inv_rent + inv_ganac + abs_ganado) >= meta:
                                    estado = 'Completada (300%)'

                                cur.execute("UPDATE aportaciones SET ganancia_acelerada = ganancia_acelerada + %s, estado = %s WHERE id = %s", (abs_ganado, estado, inv_id))
                                monto_restante -= abs_ganado
        else:
            cur.execute("UPDATE aportaciones SET estado = %s WHERE id = %s", (estado, aportacion_id))

        conn.commit()
        cur.close()
        release_conn(conn)

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.delete("/api/aportaciones/{aportacion_id}")
async def eliminar_aportacion(aportacion_id: int, usuario = Depends(obtener_usuario_actual)):
    """Elimina una aportación (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM aportaciones WHERE id = %s RETURNING id", (aportacion_id,))
        row = cur.fetchone()
        conn.commit()
        cur.close()
        release_conn(conn)
        if not row:
            raise HTTPException(status_code=404, detail="Aportación no encontrada")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - RETIROS
# ============================================================================

@app.post("/api/retiros")
async def crear_retiro(datos: RetiroRequest, usuario = Depends(obtener_usuario_actual)):
    """Crea un retiro"""
    if usuario.get('rol') != 'inversor':
        raise HTTPException(status_code=403, detail="Solo los inversores pueden solicitar retiros")
    try:
        conn = get_conn()
        cur = conn.cursor()

        inversor_id = usuario.get('inversor_id')
        moneda = datos.moneda.strip()
        cur.execute("""
            SELECT 1 FROM aportaciones
            WHERE inversor_id = %s AND moneda = %s AND (estado = 'Aprobada' OR estado = 'Activa' OR estado = 'Validada')
            LIMIT 1
        """, (inversor_id, moneda))
        if not cur.fetchone():
            raise HTTPException(status_code=400, detail="El retiro debe usar una moneda con inversión activa")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS retiros (
                id SERIAL PRIMARY KEY,
                inversor_id INT,
                nombre VARCHAR(200),
                email VARCHAR(200),
                importe DECIMAL(12,2),
                moneda VARCHAR(30),
                estado VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        cur.execute("""
            INSERT INTO retiros (inversor_id, nombre, email, importe, moneda, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (inversor_id, datos.nombre, datos.email, datos.importe, moneda, datos.estado))
        
        retiro_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        release_conn(conn)

        return {"id": retiro_id, "importe": datos.importe}
    except HTTPException:
        if 'conn' in locals() and conn:
            conn.rollback()
            release_conn(conn)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/retiros")
async def obtener_retiros(usuario = Depends(obtener_usuario_actual)):
    """Obtiene retiros (admin ve todas, inversor ve suyas)"""
    try:
        conn = get_conn()
        cur = conn.cursor()


        if usuario.get('rol') == 'admin':
            cur.execute("SELECT id, inversor_id, nombre, email, importe, moneda, estado, created_at FROM retiros ORDER BY created_at DESC")
        else:
            inversor_id = usuario.get('inversor_id')
            cur.execute("SELECT id, inversor_id, nombre, email, importe, moneda, estado, created_at FROM retiros WHERE inversor_id = %s ORDER BY created_at DESC", (inversor_id,))
        
        resultados = cur.fetchall()
        cur.close()
        release_conn(conn)

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
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("UPDATE retiros SET estado = %s WHERE id = %s", (datos.get('estado'), retiro_id))
        conn.commit()
        cur.close()
        release_conn(conn)

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
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT id, nombre, email, estado, telefono, pais, created_at FROM inversores WHERE estado = 'pendiente' ORDER BY id DESC")
        resultados = cur.fetchall()
        cur.close()
        release_conn(conn)

        inversores = []
        for row in resultados:
            inversores.append({
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "estado": row[3],
                "telefono": row[4],
                "pais": row[5],
                "created_at": row[6].isoformat() if row[6] else None
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
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT id, nombre, email, estado, telefono, pais, created_at, codigo_referido, referido_por FROM inversores WHERE estado = 'validada' ORDER BY id DESC")
        resultados = cur.fetchall()
        cur.close()
        release_conn(conn)

        inversores = []
        for row in resultados:
            inversores.append({
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "estado": row[3],
                "telefono": row[4],
                "pais": row[5],
                "created_at": row[6].isoformat() if row[6] else None,
                "codigo_referido": row[7],
                "referido_por": row[8]
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
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("UPDATE inversores SET estado = %s WHERE id = %s", (datos.get('estado'), inversor_id))
        conn.commit()
        cur.close()
        release_conn(conn)

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/inversores/{inversor_id}/referido-por")
async def corregir_referido_por(inversor_id: int, datos: dict, usuario = Depends(obtener_usuario_actual)):
    """Corrige manualmente quien invito a un inversor (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE inversores SET referido_por = %s WHERE id = %s RETURNING id, nombre, codigo_referido",
            (datos.get('referido_por'), inversor_id)
        )
        row = cur.fetchone()
        conn.commit()
        cur.close()
        release_conn(conn)
        if not row:
            raise HTTPException(status_code=404, detail="Inversor no encontrado")
        return {"success": True, "id": row[0], "nombre": row[1], "codigo_referido": row[2]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - SOLICITUDES DE PARTICIPACIÓN (FORMULARIO PÚBLICO)
# ============================================================================
@app.post("/api/solicitudes-participacion")
async def crear_solicitud_participacion(datos: dict):
    """Guarda una solicitud de participación de un usuario no registrado"""
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes_participacion (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(200),
                email VARCHAR(200),
                telefono VARCHAR(100),
                pais VARCHAR(100),
                importe DECIMAL(12,2),
                moneda VARCHAR(30),
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
        release_conn(conn)

        return {"id": solicitud_id, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/solicitudes-participacion")
async def listar_solicitudes_participacion(usuario=Depends(obtener_usuario_actual)):
    """Lista las solicitudes de participación recibidas del formulario público (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT to_regclass('solicitudes_participacion')")
        if not cur.fetchone()[0]:
            cur.close()
            release_conn(conn)
            return {"solicitudes": []}

        cur.execute("""
            SELECT id, nombre, email, telefono, pais, importe, moneda, estado, created_at
            FROM solicitudes_participacion ORDER BY created_at DESC
        """)
        filas = cur.fetchall()
        cur.close()
        release_conn(conn)
        return {"solicitudes": [{
            "id": f[0], "nombre": f[1], "email": f[2], "telefono": f[3], "pais": f[4],
            "importe": float(f[5] or 0), "moneda": f[6], "estado": f[7],
            "fecha": f[8].isoformat() if f[8] else None
        } for f in filas]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/solicitudes-participacion/{solicitud_id}")
async def actualizar_solicitud_participacion(solicitud_id: int, datos: dict, usuario=Depends(obtener_usuario_actual)):
    """Actualiza el estado de una solicitud de participación (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE solicitudes_participacion SET estado = %s WHERE id = %s", (datos.get('estado'), solicitud_id))
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# ENDPOINTS - JUSTIFICANTES
# ============================================================================

@app.post("/api/solicitudes-inversion/{solicitud_id}/justificante")
async def subir_justificante(solicitud_id: str, datos: dict, usuario=Depends(obtener_usuario_actual)):
    """Sube un justificante en base64 para una solicitud/aportación"""
    try:
        conn = get_conn()
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
        release_conn(conn)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# ENDPOINTS - REFERIDOS
# ============================================================================

class ReferidoRequest(BaseModel):
    id: str
    codigo: str
    nombreInversor: str
    usuarioId: str = ""
    referidoPor: Optional[str] = None
    inversionTotal: float = 0
    pagado: bool = False
    esAdmin: bool = False


def _ensure_referidos_table(cur, conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS referidos (
            id VARCHAR(100) PRIMARY KEY,
            codigo VARCHAR(50) UNIQUE NOT NULL,
            nombre_inversor VARCHAR(200),
            usuario_id VARCHAR(100),
            referido_por VARCHAR(50),
            inversion_total DECIMAL(12,2) DEFAULT 0,
            pagado BOOLEAN DEFAULT FALSE,
            es_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


@app.get("/api/referidos")
async def obtener_referidos(usuario = Depends(obtener_usuario_actual)):
    """Obtiene todos los referidos (usados por el programa de líderes)"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_referidos_table(cur, conn)

        cur.execute("""
            SELECT id, codigo, nombre_inversor, usuario_id, referido_por, inversion_total, pagado, es_admin
            FROM referidos ORDER BY created_at ASC
        """)
        filas = cur.fetchall()
        cur.close()
        release_conn(conn)

        referidos = [{
            "id": fila[0],
            "codigo": fila[1],
            "nombreInversor": fila[2],
            "usuarioId": fila[3],
            "referidoPor": fila[4],
            "inversionTotal": float(fila[5] or 0),
            "pagado": fila[6],
            "esAdmin": fila[7]
        } for fila in filas]

        return {"referidos": referidos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/referidos")
async def crear_o_actualizar_referido(datos: ReferidoRequest, usuario = Depends(obtener_usuario_actual)):
    """Crea o actualiza un registro de referido (código propio o comisión pagada)"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_referidos_table(cur, conn)

        cur.execute("""
            INSERT INTO referidos (id, codigo, nombre_inversor, usuario_id, referido_por, inversion_total, pagado, es_admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                nombre_inversor = EXCLUDED.nombre_inversor,
                referido_por = EXCLUDED.referido_por,
                inversion_total = EXCLUDED.inversion_total,
                pagado = EXCLUDED.pagado,
                es_admin = EXCLUDED.es_admin
        """, (
            datos.id, datos.codigo, datos.nombreInversor, datos.usuarioId,
            datos.referidoPor, datos.inversionTotal, datos.pagado, datos.esAdmin
        ))
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# ENDPOINTS - APORTACIONES A OPERACIONES PÚBLICAS (catálogo de operaciones)
# ============================================================================

class OperacionAportacionRequest(BaseModel):
    id: str
    operacionId: str
    operacionNombre: str
    usuarioId: str
    usuarioNombre: str
    importe: float
    moneda: str = "EUR"
    metodoPago: str = "transferencia"
    cuentaDestino: str = ""
    comentario: Optional[str] = ""
    estado: str = "Pendiente de validación"
    justificante: Optional[str] = ""


def _ensure_operaciones_aportaciones_table(cur, conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS operaciones_aportaciones (
            id VARCHAR(100) PRIMARY KEY,
            operacion_id VARCHAR(100) NOT NULL,
            operacion_nombre VARCHAR(255) NOT NULL,
            usuario_id VARCHAR(100),
            usuario_nombre VARCHAR(255),
            importe DECIMAL(15, 2) NOT NULL,
            moneda VARCHAR(30) DEFAULT 'EUR',
            metodo_pago VARCHAR(50),
            cuenta_destino VARCHAR(100),
            comentario TEXT,
            estado VARCHAR(50) DEFAULT 'Pendiente de validación',
            justificante TEXT,
            ganancias_disponibles DECIMAL(15, 2),
            fecha_validacion TIMESTAMP,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


@app.post("/api/operaciones/aportaciones")
async def crear_aportacion_operacion(datos: OperacionAportacionRequest, usuario=Depends(obtener_usuario_actual)):
    """Registra una aportación a una operación del catálogo público"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_aportaciones_table(cur, conn)

        cur.execute("""
            INSERT INTO operaciones_aportaciones
            (id, operacion_id, operacion_nombre, usuario_id, usuario_nombre, importe, moneda, metodo_pago, cuenta_destino, comentario, estado, justificante)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            datos.id, datos.operacionId, datos.operacionNombre, str(datos.usuarioId), datos.usuarioNombre,
            datos.importe, datos.moneda, datos.metodoPago, datos.cuentaDestino, datos.comentario,
            datos.estado, datos.justificante
        ))
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"success": True, "message": "Aportación registrada."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/operaciones/aportaciones")
async def obtener_aportaciones_operaciones(usuario=Depends(obtener_usuario_actual)):
    """Lista las aportaciones registradas a operaciones del catálogo público"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_aportaciones_table(cur, conn)

        cur.execute("""
            SELECT id, operacion_id, operacion_nombre, usuario_id, usuario_nombre, importe, moneda,
                   metodo_pago, cuenta_destino, comentario, estado, justificante, ganancias_disponibles,
                   fecha_validacion, fecha_creacion
            FROM operaciones_aportaciones
        """)
        filas = cur.fetchall()
        cur.close()
        release_conn(conn)

        aportaciones = [{
            "id": f[0], "operacionId": f[1], "operacionNombre": f[2],
            "usuarioId": f[3], "usuarioNombre": f[4], "importe": float(f[5]),
            "moneda": f[6], "metodoPago": f[7], "cuentaDestino": f[8],
            "comentario": f[9], "estado": f[10], "justificante": f[11],
            "gananciasDisponibles": float(f[12]) if f[12] else 0,
            "fechaValidacion": f[13].isoformat() if f[13] else None,
            "fechaCreacion": f[14].isoformat() if f[14] else None
        } for f in filas]

        return {"aportaciones": aportaciones}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ValidarOperacionAportacionRequest(BaseModel):
    estado: Optional[str] = None
    gananciasDisponibles: Optional[float] = None
    fechaUltimoPago: Optional[str] = None


@app.put("/api/operaciones/aportaciones/{aportacion_id}")
async def validar_aportacion_operacion(aportacion_id: str, datos: ValidarOperacionAportacionRequest, usuario=Depends(obtener_usuario_actual)):
    """Valida o actualiza el saldo disponible de una aportación a operación (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Sin permisos")
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_aportaciones_table(cur, conn)

        cur.execute("SELECT id FROM operaciones_aportaciones WHERE id = %s", (aportacion_id,))
        if not cur.fetchone():
            cur.close()
            release_conn(conn)
            raise HTTPException(status_code=404, detail="No encontrada")

        if datos.estado is not None:
            cur.execute(
                "UPDATE operaciones_aportaciones SET estado = %s, fecha_validacion = CURRENT_TIMESTAMP WHERE id = %s",
                (datos.estado, aportacion_id)
            )
        if datos.gananciasDisponibles is not None:
            cur.execute(
                "UPDATE operaciones_aportaciones SET ganancias_disponibles = %s WHERE id = %s",
                (datos.gananciasDisponibles, aportacion_id)
            )
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"success": True, "message": f"Aportación a operación procesada como {datos.estado}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS - CATÁLOGO DE OPERACIONES
# ============================================================================

OPERACIONES_SEED = [
    ("🌾", "Exportaciones de alimentos", "Agricultura y exportación", "Agricultura y exportación", "€120.000", "Participación en la exportación de alimentos hacia mercados internacionales."),
    ("🏗️", "Compra y venta de cemento en Cuba", "Materiales de construcción", "Materiales de construcción", "€95.000", "Compra y distribución de cemento con estructura de participación por tramo."),
    ("💸", "Remesas desde el exterior", "Servicios financieros", "Servicios financieros", "€85.000", "Gestión de remesas desde el exterior con condiciones y plazos definidos."),
    ("📊", "Financiación a MYPIMEs y TCP", "Financiamiento", "Financiamiento", "€150.000", "Financiación a pequeñas y medianas empresas y trabajadores por cuenta propia."),
    ("📈", "Inversiones en MYPIMEs y TCP propias", "Participación accionaria", "Participación accionaria", "€110.000", "Participación accionaria directa en negocios propios en desarrollo."),
    ("🌍", "Inversiones en el extranjero", "Mercados internacionales", "Mercados internacionales", "€200.000", "Participación en operaciones comerciales en mercados internacionales."),
]

CONDICIONES_DEFAULT = [
    "Participación por tramos según capital aportado.",
    "No se ofrece rentabilidad garantizada.",
    "Los plazos y condiciones se especifican en el anexo legal antes de formalizar la aportación."
]


def _ensure_operaciones_table(cur, conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS operaciones (
            id SERIAL PRIMARY KEY,
            icono VARCHAR(10) DEFAULT '',
            nombre VARCHAR(255) NOT NULL,
            tipo VARCHAR(150),
            categoria VARCHAR(150),
            estado VARCHAR(50) DEFAULT 'Activa',
            capital VARCHAR(50),
            comprometido VARCHAR(50) DEFAULT '€0',
            disponible VARCHAR(50),
            plazo VARCHAR(100),
            riesgo VARCHAR(100) DEFAULT 'Medio',
            rendimiento TEXT,
            descripcion TEXT,
            condiciones TEXT,
            fecha_inicio VARCHAR(50),
            fecha_fin_estimada VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM operaciones")
    if cur.fetchone()[0] == 0:
        import json
        for icono, nombre, tipo, categoria, capital, descripcion in OPERACIONES_SEED:
            cur.execute("""
                INSERT INTO operaciones (icono, nombre, tipo, categoria, capital, disponible, plazo, rendimiento, descripcion, condiciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                icono, nombre, tipo, categoria, capital, capital,
                "Por definir", "Variable según cierre comercial", descripcion,
                json.dumps(CONDICIONES_DEFAULT)
            ))
        conn.commit()


def _ensure_avisos_operaciones_table(cur, conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS avisos_operaciones (
            id VARCHAR(100) PRIMARY KEY,
            operacion_id INTEGER NOT NULL REFERENCES operaciones(id) ON DELETE CASCADE,
            titulo VARCHAR(180) NOT NULL,
            contenido TEXT NOT NULL,
            imagenes TEXT[] NOT NULL DEFAULT '{}',
            publicado_por VARCHAR(255) DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def _fila_a_operacion(fila):
    import json
    try:
        condiciones = json.loads(fila[13]) if fila[13] else CONDICIONES_DEFAULT
    except Exception:
        condiciones = CONDICIONES_DEFAULT
    return {
        "id": fila[0], "icono": fila[1], "nombre": fila[2], "tipo": fila[3],
        "categoria": fila[4], "estado": fila[5], "capital": fila[6],
        "comprometido": fila[7], "disponible": fila[8], "plazo": fila[9],
        "riesgo": fila[10], "rendimiento": fila[11], "descripcion": fila[12],
        "condiciones": condiciones, "fechaInicio": fila[14], "fechaFinEstimada": fila[15]
    }


@app.get("/api/operaciones")
async def listar_operaciones():
    """Catálogo público de operaciones (sin autenticación)"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_table(cur, conn)

        cur.execute("""
            SELECT id, icono, nombre, tipo, categoria, estado, capital, comprometido,
                   disponible, plazo, riesgo, rendimiento, descripcion, condiciones,
                   fecha_inicio, fecha_fin_estimada
            FROM operaciones ORDER BY id ASC
        """)
        filas = cur.fetchall()
        cur.close()
        release_conn(conn)
        return {"operaciones": [_fila_a_operacion(f) for f in filas]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class OperacionCatalogoRequest(BaseModel):
    icono: str = ""
    nombre: str
    tipo: str = ""
    categoria: str = ""
    estado: str = "Activa"
    capital: str = ""
    comprometido: str = "€0"
    disponible: str = ""
    plazo: str = ""
    riesgo: str = "Medio"
    rendimiento: str = ""
    descripcion: str = ""
    condiciones: list[str] = []
    fechaInicio: Optional[str] = None
    fechaFinEstimada: Optional[str] = None


@app.post("/api/operaciones")
async def crear_operacion(datos: OperacionCatalogoRequest, usuario=Depends(obtener_usuario_actual)):
    """Crea una operación del catálogo (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    try:
        import json
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_table(cur, conn)

        cur.execute("""
            INSERT INTO operaciones (icono, nombre, tipo, categoria, estado, capital, comprometido,
                disponible, plazo, riesgo, rendimiento, descripcion, condiciones, fecha_inicio, fecha_fin_estimada)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            datos.icono, datos.nombre, datos.tipo, datos.categoria, datos.estado, datos.capital,
            datos.comprometido, datos.disponible, datos.plazo, datos.riesgo, datos.rendimiento,
            datos.descripcion, json.dumps(datos.condiciones or CONDICIONES_DEFAULT),
            datos.fechaInicio, datos.fechaFinEstimada
        ))
        operacion_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"id": operacion_id, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/operaciones/{operacion_id}")
async def actualizar_operacion(operacion_id: int, datos: dict, usuario=Depends(obtener_usuario_actual)):
    """Actualiza una operación del catálogo (solo admin)"""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    try:
        import json
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_table(cur, conn)

        campos = {
            "icono": "icono", "nombre": "nombre", "tipo": "tipo", "categoria": "categoria",
            "estado": "estado", "capital": "capital", "comprometido": "comprometido",
            "disponible": "disponible", "plazo": "plazo", "riesgo": "riesgo",
            "rendimiento": "rendimiento", "descripcion": "descripcion",
            "fechaInicio": "fecha_inicio", "fechaFinEstimada": "fecha_fin_estimada"
        }
        sets, valores = [], []
        for clave_frontend, columna in campos.items():
            if clave_frontend in datos:
                sets.append(f"{columna} = %s")
                valores.append(datos[clave_frontend])
        if "condiciones" in datos:
            sets.append("condiciones = %s")
            valores.append(json.dumps(datos["condiciones"]))

        if not sets:
            cur.close()
            release_conn(conn)
            return {"success": True, "message": "Nada que actualizar"}

        sets.append("updated_at = CURRENT_TIMESTAMP")
        valores.append(operacion_id)
        cur.execute(f"UPDATE operaciones SET {', '.join(sets)} WHERE id = %s", valores)
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AvisoOperacionRequest(BaseModel):
    operacionId: int
    titulo: str
    contenido: str
    imagenes: list[str] = []


def _validar_imagenes_aviso(imagenes: list[str]):
    if len(imagenes) > 3:
        raise HTTPException(status_code=400, detail="Cada aviso admite un máximo de 3 fotos")
    for imagen in imagenes:
        if not imagen.startswith("data:image/"):
            raise HTTPException(status_code=400, detail="Las fotos deben ser imágenes válidas")
        if len(imagen) > 2_800_000:
            raise HTTPException(status_code=400, detail="Cada foto puede pesar como máximo 2 MB")


def _fila_a_aviso_operacion(fila):
    return {
        "id": fila[0], "operacionId": fila[1], "operacionNombre": fila[2],
        "operacionIcono": fila[3], "titulo": fila[4], "contenido": fila[5],
        "imagenes": fila[6] or [], "publicadoPor": fila[7] or "Administración",
        "createdAt": fila[8], "updatedAt": fila[9]
    }


@app.get("/api/avisos-operaciones")
async def listar_avisos_operaciones(usuario=Depends(obtener_usuario_actual)):
    """Publicaciones operativas visibles para inversores autenticados."""
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_table(cur, conn)
        _ensure_avisos_operaciones_table(cur, conn)
        cur.execute("""
            SELECT a.id, a.operacion_id, o.nombre, o.icono, a.titulo, a.contenido,
                   a.imagenes, a.publicado_por, a.created_at, a.updated_at
            FROM avisos_operaciones a
            JOIN operaciones o ON o.id = a.operacion_id
            ORDER BY a.created_at DESC
        """)
        avisos = [_fila_a_aviso_operacion(fila) for fila in cur.fetchall()]
        cur.close()
        release_conn(conn)
        return {"avisos": avisos}
    except Exception as e:
        if conn:
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/avisos-operaciones")
async def crear_aviso_operacion(datos: AvisoOperacionRequest, usuario=Depends(obtener_usuario_actual)):
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    if not datos.titulo.strip() or not datos.contenido.strip():
        raise HTTPException(status_code=400, detail="El titular y el contenido son obligatorios")
    _validar_imagenes_aviso(datos.imagenes)
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_table(cur, conn)
        _ensure_avisos_operaciones_table(cur, conn)
        cur.execute("SELECT id FROM operaciones WHERE id = %s", (datos.operacionId,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="La operación indicada no existe")
        aviso_id = f"aviso-operacion-{uuid.uuid4().hex}"
        cur.execute("""
            INSERT INTO avisos_operaciones (id, operacion_id, titulo, contenido, imagenes, publicado_por)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (aviso_id, datos.operacionId, datos.titulo.strip(), datos.contenido.strip(), datos.imagenes, usuario.get('email', 'Administración')))
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"id": aviso_id, "success": True}
    except HTTPException:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise
    except Exception as e:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/avisos-operaciones/{aviso_id}")
async def actualizar_aviso_operacion(aviso_id: str, datos: AvisoOperacionRequest, usuario=Depends(obtener_usuario_actual)):
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    if not datos.titulo.strip() or not datos.contenido.strip():
        raise HTTPException(status_code=400, detail="El titular y el contenido son obligatorios")
    _validar_imagenes_aviso(datos.imagenes)
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_table(cur, conn)
        _ensure_avisos_operaciones_table(cur, conn)
        cur.execute("SELECT id FROM operaciones WHERE id = %s", (datos.operacionId,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="La operación indicada no existe")
        cur.execute("""
            UPDATE avisos_operaciones
            SET operacion_id = %s, titulo = %s, contenido = %s, imagenes = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (datos.operacionId, datos.titulo.strip(), datos.contenido.strip(), datos.imagenes, aviso_id))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="El aviso no existe")
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"success": True}
    except HTTPException:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise
    except Exception as e:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/avisos-operaciones/{aviso_id}")
async def eliminar_aviso_operacion(aviso_id: str, usuario=Depends(obtener_usuario_actual)):
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_operaciones_table(cur, conn)
        _ensure_avisos_operaciones_table(cur, conn)
        cur.execute("DELETE FROM avisos_operaciones WHERE id = %s", (aviso_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="El aviso no existe")
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"success": True}
    except HTTPException:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise
    except Exception as e:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


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
        conn = get_conn()
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
        oferta_id = f"oferta-{uuid.uuid4().hex}"
        inversor_especial = datos.inversorIdEspecial.strip().lower()

        cur.execute("""
            INSERT INTO ofertas_privadas (id, nombre, descripcion, condiciones, programa, nivel, importe_maximo, inversor_id_especial)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, created_at
        """, (oferta_id, datos.nombre, datos.descripcion, datos.condiciones, datos.programa, datos.nivel, importe_final, inversor_especial))
        
        row = cur.fetchone()
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"id": row[0], "created_at": row[1].isoformat(), "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/ofertas")
async def obtener_ofertas(usuario=Depends(obtener_usuario_actual)):
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT to_regclass('ofertas_privadas')")
        if not cur.fetchone()[0]:
            return {"ofertas": []}

        cur.execute("""
            ALTER TABLE ofertas_privadas ADD COLUMN IF NOT EXISTS inversor_id_especial VARCHAR(100);
            ALTER TABLE ofertas_privadas ADD COLUMN IF NOT EXISTS progreso_actual DECIMAL(12,2) DEFAULT 0;
            ALTER TABLE ofertas_privadas ADD COLUMN IF NOT EXISTS estado VARCHAR(50) DEFAULT 'Activa';
            ALTER TABLE ofertas_privadas ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        """)
        conn.commit()

        cur.execute("SELECT id, nombre, descripcion, condiciones, programa, nivel, importe_maximo, inversor_id_especial, progreso_actual, estado, created_at FROM ofertas_privadas ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        release_conn(conn)
        
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
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE ofertas_privadas SET estado = %s WHERE id = %s", (datos.get('estado'), oferta_id))
        conn.commit()
        cur.close()
        release_conn(conn)
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
        conn = get_conn()
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
        aportacion_id = f"oferta-aportacion-{uuid.uuid4().hex}"
        
        cur.execute("""
            INSERT INTO ofertas_aportaciones (id, oferta_id, inversor_id, inversor_nombre, importe, comprobante)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, created_at
        """, (aportacion_id, datos.ofertaId, datos.inversorId, datos.inversorNombre, datos.importe, datos.comprobante))
        
        row = cur.fetchone()
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"id": str(row[0]), "fecha": row[1].isoformat(), "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/ofertas/aportaciones")
async def obtener_aportaciones_ofertas(usuario=Depends(obtener_usuario_actual)):
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT to_regclass('ofertas_aportaciones')")
        if not cur.fetchone()[0]:
            return {"aportaciones": []}

        cur.execute("""
            ALTER TABLE ofertas_aportaciones ADD COLUMN IF NOT EXISTS validador_id VARCHAR(100);
            ALTER TABLE ofertas_aportaciones ADD COLUMN IF NOT EXISTS fecha_validacion TIMESTAMP;
            ALTER TABLE ofertas_aportaciones ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        """)
        conn.commit()

        if usuario.get('rol') == 'admin':
            cur.execute("SELECT id, oferta_id, inversor_id, inversor_nombre, importe, comprobante, estado, validador_id, fecha_validacion, created_at FROM ofertas_aportaciones ORDER BY created_at DESC")
        else:
            inversor = str(usuario.get('inversor_id'))
            cur.execute("SELECT id, oferta_id, inversor_id, inversor_nombre, importe, comprobante, estado, validador_id, fecha_validacion, created_at FROM ofertas_aportaciones WHERE inversor_id = %s ORDER BY created_at DESC", (inversor,))
        
        rows = cur.fetchall()
        cur.close()
        release_conn(conn)
        
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
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            ALTER TABLE ofertas_aportaciones ADD COLUMN IF NOT EXISTS validador_id VARCHAR(100);
            ALTER TABLE ofertas_aportaciones ADD COLUMN IF NOT EXISTS fecha_validacion TIMESTAMP;
        """)
        conn.commit()

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
        release_conn(conn)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/comunidad/mensajes")
async def obtener_mensajes(privado: bool = Query(False), usuario = Depends(obtener_usuario_actual)):
    """Obtiene mensajes públicos o la conversación privada con el admin."""
    try:
        conn = get_conn()
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
                cur.execute("""
                    SELECT id, autor_id, autor_nombre, autor_rol, mensaje, destinatario, created_at 
                    FROM mensajes_comunidad 
                    WHERE (autor_id::text = %s AND destinatario = 'admin') 
                       OR (autor_rol = 'admin' AND destinatario IN (%s, %s, %s)) 
                    ORDER BY created_at DESC LIMIT 100
                """, (str(usuario.get('inversor_id', '')), usuario.get('email', ''), nombre_inversor, str(usuario.get('inversor_id', ''))))
        else:
            cur.execute("SELECT id, autor_id, autor_nombre, autor_rol, mensaje, destinatario, created_at FROM mensajes_comunidad WHERE destinatario IS NULL OR destinatario = '' ORDER BY created_at DESC LIMIT 100")
        resultados = cur.fetchall()
        cur.close()
        release_conn(conn)

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
        conn = get_conn()
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
        release_conn(conn)

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
# FONDO SOLIDARIO - registros separados de inversiones y retiros
# ============================================================================
def _ensure_fondo_solidario_tables(cur, conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fondo_solidario_config (
            id INTEGER PRIMARY KEY,
            porcentaje_fee DECIMAL(5,2) NOT NULL DEFAULT 2,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        INSERT INTO fondo_solidario_config (id, porcentaje_fee)
        VALUES (1, 2)
        ON CONFLICT (id) DO NOTHING
    """)
    cur.execute("""
        UPDATE fondo_solidario_config
        SET porcentaje_fee = 2, updated_at = NOW()
        WHERE id = 1 AND porcentaje_fee <> 2
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fondo_solidario_movimientos (
            id SERIAL PRIMARY KEY,
            tipo VARCHAR(30) NOT NULL,
            importe DECIMAL(12,2) NOT NULL CHECK (importe > 0),
            moneda VARCHAR(20) NOT NULL DEFAULT 'USDT',
            descripcion TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fondo_solidario_casos (
            id SERIAL PRIMARY KEY,
            alias_familia VARCHAR(150) NOT NULL,
            categoria VARCHAR(100) NOT NULL,
            descripcion TEXT NOT NULL,
            fuente VARCHAR(30) NOT NULL DEFAULT 'comunidad',
            estado VARCHAR(30) NOT NULL DEFAULT 'recibido',
            visible BOOLEAN NOT NULL DEFAULT FALSE,
            importe_solicitado DECIMAL(12,2),
            importe_entregado DECIMAL(12,2),
            responsable_entrega VARCHAR(200),
            resumen_entrega TEXT,
            evidencia TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def _obtener_resumen_fondo_solidario(cur, admin=False):
    cur.execute("SELECT porcentaje_fee, updated_at FROM fondo_solidario_config WHERE id = 1")
    config = cur.fetchone() or (0, None)
    cur.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN tipo = 'aporte_fee' THEN importe ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN tipo = 'aporte_empresa' THEN importe ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN tipo = 'entrega' THEN importe ELSE 0 END), 0)
        FROM fondo_solidario_movimientos
    """)
    aportado_fees, aportado_empresa, entregado = cur.fetchone()
    aportado = float(aportado_fees or 0) + float(aportado_empresa or 0)
    filtro_casos = "" if admin else "WHERE visible = TRUE AND estado IN ('verificado', 'seleccionado', 'entregado')"
    cur.execute(f"""
        SELECT id, alias_familia, categoria, descripcion, fuente, estado, visible,
               importe_solicitado, importe_entregado, responsable_entrega,
               resumen_entrega, evidencia, created_at, updated_at
        FROM fondo_solidario_casos
        {filtro_casos}
        ORDER BY created_at DESC
    """)
    casos = []
    for row in cur.fetchall():
        casos.append({
            "id": row[0], "alias_familia": row[1], "categoria": row[2],
            "descripcion": row[3], "fuente": row[4], "estado": row[5],
            "visible": row[6], "importe_solicitado": float(row[7]) if row[7] is not None else None,
            "importe_entregado": float(row[8]) if row[8] is not None else None,
            "responsable_entrega": row[9], "resumen_entrega": row[10],
            "evidencia": row[11], "created_at": row[12].isoformat() if row[12] else None,
            "updated_at": row[13].isoformat() if row[13] else None,
        })
    resultado = {
        "porcentaje_fee": float(config[0] or 0),
        "actualizado_at": config[1].isoformat() if config[1] else None,
        "aportado": aportado,
        "aportado_fees": float(aportado_fees or 0),
        "aportado_empresa": float(aportado_empresa or 0),
        "entregado": float(entregado or 0),
        "saldo": aportado - float(entregado or 0),
        "casos": casos,
    }
    if admin:
        cur.execute("""
            SELECT id, tipo, importe, moneda, descripcion, created_at
            FROM fondo_solidario_movimientos ORDER BY created_at DESC LIMIT 100
        """)
        resultado["movimientos"] = [{
            "id": row[0], "tipo": row[1], "importe": float(row[2]),
            "moneda": row[3], "descripcion": row[4],
            "created_at": row[5].isoformat() if row[5] else None,
        } for row in cur.fetchall()]
    return resultado


@app.get("/api/fondo-solidario")
async def obtener_fondo_solidario(usuario=Depends(obtener_usuario_actual)):
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_fondo_solidario_tables(cur, conn)
        resumen = _obtener_resumen_fondo_solidario(cur, admin=usuario.get("rol") == "admin")
        cur.close()
        release_conn(conn)
        return resumen
    except Exception as e:
        if conn:
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/admin/fondo-solidario/config")
async def actualizar_config_fondo_solidario(datos: dict, usuario=Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Solo admins")
    porcentaje = 2
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_fondo_solidario_tables(cur, conn)
        cur.execute("""
            UPDATE fondo_solidario_config
            SET porcentaje_fee = %s, updated_at = NOW()
            WHERE id = 1
        """, (porcentaje,))
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"ok": True, "porcentaje_fee": porcentaje}
    except Exception as e:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/fondo-solidario/movimientos")
async def registrar_movimiento_fondo_solidario(datos: dict, usuario=Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Solo admins")
    tipo = datos.get("tipo")
    if tipo not in ("aporte_fee", "aporte_empresa"):
        raise HTTPException(status_code=400, detail="Tipo de aporte no valido")
    importe = float(datos.get("importe", 0))
    descripcion = str(datos.get("descripcion", "")).strip()
    if importe <= 0 or not descripcion:
        raise HTTPException(status_code=400, detail="Indica un importe y una descripcion")
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_fondo_solidario_tables(cur, conn)
        cur.execute("""
            INSERT INTO fondo_solidario_movimientos (tipo, importe, moneda, descripcion)
            VALUES (%s, %s, %s, %s)
        """, (tipo, importe, str(datos.get("moneda", "USDT")), descripcion))
        conn.commit()
        resumen = _obtener_resumen_fondo_solidario(cur, admin=True)
        cur.close()
        release_conn(conn)
        return resumen
    except Exception as e:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/fondo-solidario/casos")
async def crear_caso_fondo_solidario(datos: dict, usuario=Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Solo admins")
    alias = str(datos.get("alias_familia", "")).strip()
    categoria = str(datos.get("categoria", "")).strip()
    descripcion = str(datos.get("descripcion", "")).strip()
    if not alias or not categoria or not descripcion:
        raise HTTPException(status_code=400, detail="Completa alias, categoria y descripcion")
    importe_solicitado = datos.get("importe_solicitado")
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_fondo_solidario_tables(cur, conn)
        cur.execute("""
            INSERT INTO fondo_solidario_casos
            (alias_familia, categoria, descripcion, fuente, importe_solicitado)
            VALUES (%s, %s, %s, %s, %s)
        """, (alias, categoria, descripcion, str(datos.get("fuente", "comunidad")), importe_solicitado or None))
        conn.commit()
        resumen = _obtener_resumen_fondo_solidario(cur, admin=True)
        cur.close()
        release_conn(conn)
        return resumen
    except Exception as e:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/admin/fondo-solidario/casos/{caso_id}")
async def actualizar_caso_fondo_solidario(caso_id: int, datos: dict, usuario=Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Solo admins")
    estado = datos.get("estado")
    if estado not in ("recibido", "verificado", "seleccionado", "entregado", "descartado"):
        raise HTTPException(status_code=400, detail="Estado no valido")
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_fondo_solidario_tables(cur, conn)
        cur.execute("""
            UPDATE fondo_solidario_casos
            SET estado = %s, visible = %s, updated_at = NOW()
            WHERE id = %s
        """, (estado, bool(datos.get("visible", False)), caso_id))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Caso no encontrado")
        conn.commit()
        resumen = _obtener_resumen_fondo_solidario(cur, admin=True)
        cur.close()
        release_conn(conn)
        return resumen
    except HTTPException:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise
    except Exception as e:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/fondo-solidario/casos/{caso_id}/entrega")
async def registrar_entrega_fondo_solidario(caso_id: int, datos: dict, usuario=Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Solo admins")
    importe = float(datos.get("importe", 0))
    responsable = str(datos.get("responsable_entrega", "")).strip()
    resumen = str(datos.get("resumen_entrega", "")).strip()
    if importe <= 0 or not responsable or not resumen:
        raise HTTPException(status_code=400, detail="Completa importe, responsable y resumen de entrega")
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        _ensure_fondo_solidario_tables(cur, conn)
        cur.execute("SELECT alias_familia FROM fondo_solidario_casos WHERE id = %s", (caso_id,))
        caso = cur.fetchone()
        if not caso:
            raise HTTPException(status_code=404, detail="Caso no encontrado")
        cur.execute("""
            INSERT INTO fondo_solidario_movimientos (tipo, importe, moneda, descripcion)
            VALUES ('entrega', %s, %s, %s)
        """, (importe, str(datos.get("moneda", "USDT")), f"Entrega a {caso[0]}: {resumen}"))
        cur.execute("""
            UPDATE fondo_solidario_casos
            SET estado = 'entregado', visible = TRUE, importe_entregado = %s,
                responsable_entrega = %s, resumen_entrega = %s, evidencia = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (importe, responsable, resumen, datos.get("evidencia") or None, caso_id))
        conn.commit()
        resumen_fondo = _obtener_resumen_fondo_solidario(cur, admin=True)
        cur.close()
        release_conn(conn)
        return resumen_fondo
    except HTTPException:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise
    except Exception as e:
        if conn:
            conn.rollback()
            release_conn(conn)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# RESET DE DATOS DE PRUEBA (solo admin) - borra usuarios y todo lo generado por ellos
# ============================================================================

TABLAS_RESET_USUARIOS = [
    "ofertas_aportaciones", "operaciones_aportaciones", "mensajes_comunidad",
    "justificantes", "solicitudes_inversion", "solicitudes_participacion",
    "retiros", "aportaciones", "referidos", "referidos_inversores", "inversores"
]


@app.post("/api/admin/reset-demo")
async def resetear_datos_demo(usuario=Depends(obtener_usuario_actual)):
    """Borra inversores y todos los datos que dependen de ellos. No toca el catálogo de operaciones ni la configuración."""
    if usuario.get('rol') != 'admin':
        raise HTTPException(status_code=403, detail="Acceso denegado")
    try:
        conn = get_conn()
        cur = conn.cursor()
        borradas = []
        for tabla in TABLAS_RESET_USUARIOS:
            cur.execute("SELECT to_regclass(%s)", (tabla,))
            if cur.fetchone()[0]:
                cur.execute(f"TRUNCATE TABLE {tabla} RESTART IDENTITY CASCADE")
                borradas.append(tabla)
        conn.commit()
        cur.close()
        release_conn(conn)
        return {"success": True, "tablas_vaciadas": borradas}
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
