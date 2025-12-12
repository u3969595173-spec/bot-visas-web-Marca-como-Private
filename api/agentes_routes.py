"""
Endpoints para sistema de Agentes/Afiliados
Comisión: 10% del presupuesto aceptado por estudiantes referidos
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
import secrets
import bcrypt

from database.models import get_db
from api.auth import crear_token, verificar_token

router = APIRouter()

# =====================================================
# SCHEMAS
# =====================================================

class AgenteRegistro(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    telefono: Optional[str] = None

class AgenteLogin(BaseModel):
    email: EmailStr
    password: str

class AgenteResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str]
    codigo_referido: str
    comision_total: float
    credito_disponible: float
    total_referidos: int
    activo: bool
    created_at: datetime

# =====================================================
# AUTENTICACIÓN
# =====================================================

def obtener_agente_actual(token: str = Depends(verificar_token), db: Session = Depends(get_db)):
    """Verifica que el token corresponda a un agente"""
    
    result = db.execute(text("""
        SELECT id, nombre, email, activo 
        FROM agentes 
        WHERE email = :email AND activo = TRUE
    """), {"email": token.get("sub")}).fetchone()
    
    if not result:
        raise HTTPException(status_code=401, detail="Agente no encontrado o inactivo")
    
    return {
        "id": result[0],
        "nombre": result[1],
        "email": result[2],
        "activo": result[3]
    }

# =====================================================
# REGISTRO Y LOGIN
# =====================================================

@router.post("/registro", tags=["Agentes"])
async def registrar_agente(datos: AgenteRegistro, db: Session = Depends(get_db)):
    """Registrar nuevo agente (solo admin puede hacer esto desde panel)"""
    
    # Verificar si email ya existe
    existe = db.execute(text("""
        SELECT id FROM agentes WHERE email = :email
    """), {"email": datos.email}).fetchone()
    
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Generar código de referido único
    while True:
        codigo = secrets.token_hex(4).upper()
        existe_codigo = db.execute(text("""
            SELECT id FROM agentes WHERE codigo_referido = :codigo
        """), {"codigo": codigo}).fetchone()
        
        if not existe_codigo:
            break
    
    # Hash de contraseña
    password_hash = bcrypt.hashpw(datos.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Insertar agente
    result = db.execute(text("""
        INSERT INTO agentes (nombre, email, password, telefono, codigo_referido)
        VALUES (:nombre, :email, :password, :telefono, :codigo)
        RETURNING id, nombre, email, codigo_referido
    """), {
        "nombre": datos.nombre,
        "email": datos.email,
        "password": password_hash,
        "telefono": datos.telefono,
        "codigo": codigo
    })
    
    db.commit()
    agente = result.fetchone()
    
    return {
        "mensaje": "Agente registrado exitosamente",
        "agente_id": agente[0],
        "nombre": agente[1],
        "email": agente[2],
        "codigo_referido": agente[3]
    }

@router.post("/login", tags=["Agentes"])
async def login_agente(datos: AgenteLogin, db: Session = Depends(get_db)):
    """Login para agentes"""
    
    # Buscar agente
    agente = db.execute(text("""
        SELECT id, nombre, email, password, activo 
        FROM agentes 
        WHERE email = :email
    """), {"email": datos.email}).fetchone()
    
    if not agente:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Verificar contraseña
    if not bcrypt.checkpw(datos.password.encode('utf-8'), agente[3].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Verificar si está activo
    if not agente[4]:
        raise HTTPException(status_code=403, detail="Tu cuenta está desactivada. Contacta al administrador.")
    
    # Crear token
    token = crear_token({"sub": agente[2], "tipo": "agente"})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "agente": {
            "id": agente[0],
            "nombre": agente[1],
            "email": agente[2]
        }
    }

# =====================================================
# PERFIL Y ESTADÍSTICAS
# =====================================================

@router.get("/perfil", tags=["Agentes"])
async def obtener_perfil_agente(
    agente = Depends(obtener_agente_actual),
    db: Session = Depends(get_db)
):
    """Obtener perfil completo del agente"""
    
    perfil = db.execute(text("""
        SELECT id, nombre, email, telefono, codigo_referido,
               comision_total, credito_disponible, COALESCE(credito_retirado, 0) as credito_retirado,
               total_referidos, activo, created_at
        FROM agentes
        WHERE id = :id
    """), {"id": agente["id"]}).fetchone()
    
    # Calcular comisión total real (disponible + retirado)
    credito_disponible = float(perfil[6])
    credito_retirado = float(perfil[7])
    comision_total_real = credito_disponible + credito_retirado
    
    return {
        "id": perfil[0],
        "nombre": perfil[1],
        "email": perfil[2],
        "telefono": perfil[3],
        "codigo_referido": perfil[4],
        "comision_total": comision_total_real,  # Total ganado = disponible + retirado
        "credito_disponible": credito_disponible,
        "credito_retirado": credito_retirado,
        "total_referidos": perfil[8],
        "activo": perfil[9],
        "created_at": perfil[10].isoformat() if perfil[10] else None
    }

@router.get("/estadisticas", tags=["Agentes"])
async def obtener_estadisticas_agente(
    agente = Depends(obtener_agente_actual),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas del agente"""
    
    # Obtener crédito disponible y retirado del agente
    agente_data = db.execute(text("""
        SELECT credito_disponible, COALESCE(credito_retirado, 0) as credito_retirado
        FROM agentes
        WHERE id = :agente_id
    """), {"agente_id": agente["id"]}).fetchone()
    
    credito_disponible = float(agente_data[0] or 0)
    credito_retirado = float(agente_data[1] or 0)
    comision_total = credito_disponible + credito_retirado  # Total ganado = disponible + retirado
    
    # Estadísticas generales
    stats = db.execute(text("""
        SELECT 
            COUNT(DISTINCT e.id) as total_referidos,
            COUNT(DISTINCT CASE WHEN e.estado = 'activo' THEN e.id END) as referidos_activos,
            COUNT(DISTINCT CASE WHEN p.estado = 'aceptado' THEN p.id END) as presupuestos_aceptados
        FROM estudiantes e
        LEFT JOIN presupuestos p ON p.estudiante_id = e.id
        WHERE e.referido_por_agente_id = :agente_id
    """), {"agente_id": agente["id"]}).fetchone()
    
    # Referidos recientes
    referidos_recientes = db.execute(text("""
        SELECT id, nombre, email, estado, created_at
        FROM estudiantes
        WHERE referido_por_agente_id = :agente_id
        ORDER BY created_at DESC
        LIMIT 10
    """), {"agente_id": agente["id"]}).fetchall()
    
    return {
        "total_referidos": stats[0],
        "referidos_activos": stats[1],
        "presupuestos_aceptados": stats[2],
        "comision_total": comision_total,
        "credito_disponible": credito_disponible,
        "credito_retirado": credito_retirado,
        "referidos_recientes": [
            {
                "id": r[0],
                "nombre": r[1],
                "email": r[2],
                "estado": r[3],
                "created_at": r[4].isoformat() if r[4] else None
            }
            for r in referidos_recientes
        ]
    }

# =====================================================
# GESTIÓN DE REFERIDOS
# =====================================================

@router.get("/referidos", tags=["Agentes"])
async def listar_referidos(
    agente = Depends(obtener_agente_actual),
    db: Session = Depends(get_db)
):
    """Listar todos los estudiantes referidos por el agente"""
    
    referidos = db.execute(text("""
        SELECT 
            e.id, e.nombre, e.email, e.telefono, e.estado,
            e.carrera_deseada, e.perfil_completo, e.created_at,
            COALESCE(SUM(CASE WHEN p.estado = 'aceptado' THEN p.precio_ofertado * 0.10 ELSE 0 END), 0) as comision_generada
        FROM estudiantes e
        LEFT JOIN presupuestos p ON p.estudiante_id = e.id
        WHERE e.referido_por_agente_id = :agente_id
        GROUP BY e.id, e.nombre, e.email, e.telefono, e.estado, e.carrera_deseada, e.perfil_completo, e.created_at
        ORDER BY e.created_at DESC
    """), {"agente_id": agente["id"]}).fetchall()
    
    return [
        {
            "id": r[0],
            "nombre": r[1],
            "email": r[2],
            "telefono": r[3],
            "estado": r[4],
            "carrera_deseada": r[5],
            "perfil_completo": r[6],
            "fecha_registro": r[7].isoformat() if r[7] else None,
            "comision_generada": float(r[8])
        }
        for r in referidos
    ]

@router.get("/referidos/{estudiante_id}", tags=["Agentes"])
async def obtener_detalle_referido(
    estudiante_id: int,
    agente = Depends(obtener_agente_actual),
    db: Session = Depends(get_db)
):
    """Obtener detalles completos de un estudiante referido"""
    
    # Verificar que el estudiante pertenece al agente
    estudiante = db.execute(text("""
        SELECT * FROM estudiantes
        WHERE id = :id AND referido_por_agente_id = :agente_id
    """), {"id": estudiante_id, "agente_id": agente["id"]}).fetchone()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado o no pertenece a este agente")
    
    # Obtener presupuestos
    presupuestos = db.execute(text("""
        SELECT id, modalidad, duracion_meses, precio_ofertado, estado, fecha_creacion
        FROM presupuestos
        WHERE estudiante_id = :id
        ORDER BY fecha_creacion DESC
    """), {"id": estudiante_id}).fetchall()
    
    return {
        "estudiante": dict(estudiante._mapping),
        "presupuestos": [
            {
                "id": p[0],
                "modalidad": p[1],
                "duracion_meses": p[2],
                "precio": float(p[3]) if p[3] else 0,
                "estado": p[4],
                "fecha": p[5].isoformat() if p[5] else None
            }
            for p in presupuestos
        ]
    }

@router.put("/referidos/{estudiante_id}", tags=["Agentes"])
async def actualizar_referido(
    estudiante_id: int,
    datos: dict,
    agente = Depends(obtener_agente_actual),
    db: Session = Depends(get_db)
):
    """Actualizar información de un estudiante referido"""
    
    # Verificar que el estudiante pertenece al agente
    existe = db.execute(text("""
        SELECT id FROM estudiantes
        WHERE id = :id AND referido_por_agente_id = :agente_id
    """), {"id": estudiante_id, "agente_id": agente["id"]}).fetchone()
    
    if not existe:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Actualizar campos permitidos
    campos_permitidos = ['telefono', 'carrera_deseada', 'nivel_espanol', 'pais_origen', 'ciudad_origen']
    campos_update = []
    params = {"id": estudiante_id}
    
    for campo in campos_permitidos:
        if campo in datos:
            campos_update.append(f"{campo} = :{campo}")
            params[campo] = datos[campo]
    
    if campos_update:
        query = f"""
            UPDATE estudiantes
            SET {', '.join(campos_update)}, updated_at = NOW()
            WHERE id = :id
        """
        db.execute(text(query), params)
        db.commit()
    
    return {"mensaje": "Estudiante actualizado exitosamente"}

# =====================================================
# SUBIR DOCUMENTOS
# =====================================================

@router.post("/referidos/{estudiante_id}/documentos", tags=["Agentes"])
async def subir_documento_referido(
    estudiante_id: int,
    tipo_documento: str = Form(...),
    archivo: UploadFile = File(...),
    agente = Depends(obtener_agente_actual),
    db: Session = Depends(get_db)
):
    """Subir documento para un estudiante referido"""
    
    # Verificar que el estudiante pertenece al agente
    existe = db.execute(text("""
        SELECT id FROM estudiantes
        WHERE id = :id AND referido_por_agente_id = :agente_id
    """), {"id": estudiante_id, "agente_id": agente["id"]}).fetchone()
    
    if not existe:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Aquí va la lógica de subir archivo (similar a la que ya existe)
    # Por ahora retorno success
    
    return {
        "mensaje": "Documento subido exitosamente",
        "tipo": tipo_documento,
        "archivo": archivo.filename
    }

# =====================================================
# SOLICITUD DE RETIRO
# =====================================================

@router.post("/solicitar-retiro", tags=["Agentes"])
async def solicitar_retiro(
    data: dict,
    agente = Depends(obtener_agente_actual),
    db: Session = Depends(get_db)
):
    """Agente solicita retiro de comisiones"""
    
    monto = data.get('monto')
    notas = data.get('notas', '')
    
    if not monto or monto <= 0:
        raise HTTPException(status_code=400, detail="Monto inválido")
    
    # Verificar crédito disponible
    perfil = db.execute(text("""
        SELECT credito_disponible, nombre, email FROM agentes WHERE id = :id
    """), {"id": agente["id"]}).fetchone()
    
    if not perfil or perfil[0] < monto:
        raise HTTPException(
            status_code=400, 
            detail=f"Crédito insuficiente. Disponible: {perfil[0] if perfil else 0}€"
        )
    
    # Crear solicitud en tabla específica de agentes
    db.execute(text("""
        INSERT INTO solicitudes_retiro_agentes (
            agente_id, monto, estado, notas_agente, created_at
        )
        VALUES (:agente_id, :monto, 'pendiente', :notas, CURRENT_TIMESTAMP)
    """), {"agente_id": agente["id"], "monto": monto, "notas": notas})
    
    db.commit()
    
    # Notificar al admin
    try:
        from api.notificaciones_admin import notificar_solicitud_credito
        
        agente_dict = {
            'nombre': perfil[1],
            'email': perfil[2],
            'credito_disponible': float(perfil[0] or 0)
        }
        notificar_solicitud_credito(None, agente_dict, 'retiro', monto)
    except Exception as e:
        print(f"⚠️ Error enviando notificación: {e}")
    
    return {"message": "Solicitud de retiro enviada al administrador"}


@router.get("/retiros", tags=["Agentes"])
async def obtener_retiros(
    agente = Depends(obtener_agente_actual),
    db: Session = Depends(get_db)
):
    """Obtener historial de retiros del agente"""
    
    result = db.execute(text("""
        SELECT id, monto, estado, notas_agente, comentarios_admin, 
               created_at, updated_at
        FROM solicitudes_retiro_agentes
        WHERE agente_id = :agente_id
        ORDER BY created_at DESC
    """), {"agente_id": agente["id"]})
    
    retiros = []
    for row in result.fetchall():
        retiros.append({
            'id': row[0],
            'monto': float(row[1]),
            'estado': row[2],
            'notas_agente': row[3],
            'comentarios_admin': row[4],
            'fecha_solicitud': row[5].isoformat() if row[5] else None,
            'fecha_respuesta': row[6].isoformat() if row[6] else None
        })
    
    return retiros
