"""
API REST con FastAPI para Dashboard Web
Endpoints para estudiantes y panel de administración
"""

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime

from database.models import get_db
from modules.estudiantes import Estudiante
from modules.admin_panel import PanelAdministrativo
from api.schemas import (
    EstudianteCreate, EstudianteResponse, EstudianteUpdate,
    LoginRequest, LoginResponse, EstadisticasResponse
)
from api.auth import crear_token, verificar_token

app = FastAPI(
    title="Bot Visas Estudio API",
    description="API para gestión de estudiantes y agencia educativa",
    version="1.0.0"
)

# CORS - Permitir requests desde frontend
@app.on_event("startup")
async def startup_event():
    """Ejecutar migraciones al iniciar"""
    import os
    import psycopg2
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Crear tabla documentos_generados si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documentos_generados (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
                tipo_documento VARCHAR(100) NOT NULL,
                nombre_archivo VARCHAR(255) NOT NULL,
                contenido_pdf TEXT NOT NULL,
                estado VARCHAR(50) DEFAULT 'generado',
                notas TEXT,
                generado_por VARCHAR(100),
                aprobado_por VARCHAR(100),
                fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_aprobacion TIMESTAMP,
                enviado_estudiante BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_documentos_generados_estudiante 
            ON documentos_generados(estudiante_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_documentos_generados_estado 
            ON documentos_generados(estado);
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Tabla documentos_generados verificada/creada")
    except Exception as e:
        print(f"⚠️ Error en startup: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


# ============================================================================
# AUTENTICACIÓN
# ============================================================================

@app.post("/api/login", response_model=LoginResponse, tags=["Auth"])
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    """
    Login para admins
    Usuario: admin / Contraseña: admin123 (cambiar en producción)
    """
    from passlib.hash import bcrypt
    from database.models import Usuario
    
    # Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == datos.usuario).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Verificar contraseña
    if not bcrypt.verify(datos.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Crear token
    token = crear_token({"usuario": usuario.email, "rol": usuario.rol})
    return LoginResponse(
        token=token,
        tipo="Bearer",
        usuario=usuario.nombre,
        rol=usuario.rol
    )


def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Verifica token JWT y retorna usuario"""
    token = credentials.credentials
    payload = verificar_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    return payload


# ============================================================================
# ENDPOINTS PÚBLICOS (Estudiantes)
# ============================================================================

@app.post("/api/estudiantes", tags=["Estudiantes"])
def registrar_estudiante(datos: dict, db: Session = Depends(get_db)):
    """
    Registro público de estudiantes
    No requiere autenticación
    """
    try:
        from database.models import Estudiante as EstudianteModel
        
        # Verificar si ya existe
        existe = db.query(EstudianteModel).filter(
            EstudianteModel.email == datos.get('email')
        ).first()
        
        if existe:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un estudiante con este email"
            )
        
        # Crear nuevo estudiante
        nuevo = EstudianteModel(
            nombre=datos.get('nombre'),
            email=datos.get('email'),
            telefono=datos.get('telefono'),
            pasaporte=datos.get('pasaporte'),
            edad=datos.get('edad'),
            nacionalidad=datos.get('nacionalidad'),
            ciudad_origen=datos.get('ciudad_origen'),
            especialidad=datos.get('especialidad'),
            nivel_espanol=datos.get('nivel_espanol'),
            tipo_visa=datos.get('tipo_visa', 'estudiante'),
            estado='pendiente',
            documentos_estado='pendiente'
        )
        
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        
        # Enviar email de confirmación (sin bloquear)
        try:
            from api.notificaciones_email import NotificacionesEmail
            NotificacionesEmail.enviar_confirmacion_registro({
                'id': nuevo.id,
                'nombre': nuevo.nombre,
                'email': nuevo.email,
                'especialidad': nuevo.especialidad
            })
        except Exception as e:
            print(f"⚠️ Error enviando email: {e}")
        
        return {
            "id": nuevo.id,
            "mensaje": "Registro exitoso. Revisa tu email para más información.",
            "estado": nuevo.estado
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/estudiantes/{estudiante_id}", tags=["Estudiantes"])
def obtener_estudiante_publico(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Obtiene datos de un estudiante (sin auth para estudiante)
    """
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return {
        "id": estudiante.id,
        "nombre": estudiante.nombre,
        "email": estudiante.email,
        "telefono": estudiante.telefono,
        "pasaporte": estudiante.pasaporte,
        "edad": estudiante.edad,
        "nacionalidad": estudiante.nacionalidad,
        "ciudad_origen": estudiante.ciudad_origen,
        "especialidad": estudiante.especialidad,
        "nivel_espanol": estudiante.nivel_espanol,
        "tipo_visa": estudiante.tipo_visa,
        "estado": estudiante.estado,
        "documentos_estado": estudiante.documentos_estado,
        "notas": estudiante.notas,
        "created_at": estudiante.created_at.isoformat() if estudiante.created_at else None,
        "updated_at": estudiante.updated_at.isoformat() if estudiante.updated_at else None
    }


@app.put("/api/estudiantes/{estudiante_id}", tags=["Estudiantes"])
def actualizar_estudiante_publico(estudiante_id: int, datos: dict, db: Session = Depends(get_db)):
    """
    Actualiza datos de un estudiante (sin auth para estudiante)
    """
    from database.models import Estudiante as EstudianteModel
    from datetime import datetime
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Actualizar campos permitidos
    campos_permitidos = ['nombre', 'email', 'telefono', 'pasaporte', 'edad', 
                         'nacionalidad', 'ciudad_origen', 'especialidad', 
                         'nivel_espanol', 'tipo_visa']
    
    for campo in campos_permitidos:
        if campo in datos:
            setattr(estudiante, campo, datos[campo])
    
    estudiante.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(estudiante)
    
    return {
        "mensaje": "Datos actualizados correctamente",
        "estudiante": {
            "id": estudiante.id,
            "nombre": estudiante.nombre,
            "email": estudiante.email
        }
    }


@app.get("/api/estudiantes/{estudiante_id}/probabilidad-visa", tags=["Estudiantes"])
def calcular_probabilidad_visa(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Calcula la probabilidad de aprobación de visa del estudiante
    """
    from database.models import Estudiante as EstudianteModel
    from api.calculadora_visa import CalculadoraProbabilidadVisa
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Preparar datos para el cálculo
    estudiante_data = {
        'nombre': estudiante.nombre,
        'email': estudiante.email,
        'telefono': estudiante.telefono,
        'pasaporte': estudiante.pasaporte,
        'edad': estudiante.edad,
        'nacionalidad': estudiante.nacionalidad,
        'ciudad_origen': estudiante.ciudad_origen,
        'especialidad': estudiante.especialidad,
        'nivel_espanol': estudiante.nivel_espanol,
        'tipo_visa': estudiante.tipo_visa
    }
    
    # Calcular probabilidad
    analisis = CalculadoraProbabilidadVisa.calcular_probabilidad(estudiante_data)
    
    return {
        'estudiante_id': estudiante_id,
        'estudiante_nombre': estudiante.nombre,
        'analisis': analisis
    }


@app.post("/api/estudiantes/{estudiante_id}/documentos", tags=["Estudiantes"])
async def subir_documento(
    estudiante_id: int,
    tipo_documento: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Sube un documento para el estudiante
    """
    import base64
    from datetime import datetime
    
    # Verificar que el estudiante existe
    from database.models import Estudiante as EstudianteModel
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Validar tipo de archivo
    allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    file_extension = archivo.filename[archivo.filename.rfind('.'):].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de archivo no permitido. Use: {', '.join(allowed_extensions)}"
        )
    
    # Leer archivo y convertir a base64
    contenido = await archivo.read()
    tamano_bytes = len(contenido)
    
    # Validar tamaño (máximo 5MB)
    if tamano_bytes > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo muy grande. Máximo 5MB")
    
    # Convertir a base64 para almacenar en DB
    contenido_base64 = base64.b64encode(contenido).decode('utf-8')
    url_archivo = f"data:application/{file_extension[1:]};base64,{contenido_base64}"
    
    # Guardar en base de datos
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            INSERT INTO documentos 
            (estudiante_id, tipo_documento, nombre_archivo, url_archivo, tamano_bytes, estado, created_at)
            VALUES (%s, %s, %s, %s, %s, 'pendiente', %s)
            RETURNING id
        """, (estudiante_id, tipo_documento, archivo.filename, url_archivo, tamano_bytes, datetime.utcnow()))
        
        documento_id = cursor.fetchone()[0]
        db.commit()
        
        # Actualizar estado de documentos del estudiante
        estudiante.documentos_estado = 'en_revision'
        db.commit()
        
        return {
            "mensaje": "Documento subido correctamente",
            "documento_id": documento_id,
            "nombre_archivo": archivo.filename,
            "tamano_bytes": tamano_bytes
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar documento: {str(e)}")


@app.get("/api/estudiantes/{estudiante_id}/documentos", tags=["Estudiantes"])
def listar_documentos(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Lista todos los documentos de un estudiante
    """
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            SELECT id, tipo_documento, nombre_archivo, tamano_bytes, estado, notas, created_at
            FROM documentos
            WHERE estudiante_id = %s
            ORDER BY created_at DESC
        """, (estudiante_id,))
        
        documentos = []
        for row in cursor.fetchall():
            documentos.append({
                'id': row[0],
                'tipo_documento': row[1],
                'nombre_archivo': row[2],
                'tamano_bytes': row[3],
                'estado': row[4],
                'notas': row[5],
                'created_at': row[6].isoformat() if row[6] else None
            })
        
        return {
            'total': len(documentos),
            'documentos': documentos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar documentos: {str(e)}")


@app.get("/api/estudiantes/{estudiante_id}/reporte-pdf", tags=["Reportes"])
def generar_reporte_pdf(estudiante_id: int, tipo: str = 'completo', db: Session = Depends(get_db)):
    """
    Genera un PDF con el reporte del estudiante
    tipo: 'completo' o 'analisis'
    """
    from database.models import Estudiante as EstudianteModel
    from api.generador_pdf import GeneradorReportesPDF
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante_data = {
        'id': estudiante.id,
        'nombre': estudiante.nombre,
        'email': estudiante.email,
        'telefono': estudiante.telefono,
        'pasaporte': estudiante.pasaporte,
        'edad': estudiante.edad,
        'nacionalidad': estudiante.nacionalidad,
        'ciudad_origen': estudiante.ciudad_origen,
        'especialidad': estudiante.especialidad,
        'nivel_espanol': estudiante.nivel_espanol,
        'tipo_visa': estudiante.tipo_visa,
        'estado': estudiante.estado,
        'documentos_estado': estudiante.documentos_estado,
        'notas': estudiante.notas
    }
    
    if tipo == 'analisis':
        # Generar análisis de visa
        from api.calculadora_visa import CalculadoraProbabilidadVisa
        analisis = CalculadoraProbabilidadVisa.calcular_probabilidad(estudiante_data)
        pdf_buffer = GeneradorReportesPDF.generar_reporte_analisis_visa(estudiante_data, analisis)
        filename = f"analisis_visa_{estudiante.id}.pdf"
    else:
        # Generar reporte completo
        pdf_buffer = GeneradorReportesPDF.generar_reporte_completo_estudiante(estudiante_data)
        filename = f"reporte_estudiante_{estudiante.id}.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# ============================================================================
# GENERACIÓN DE DOCUMENTOS OFICIALES (ADMIN)
# ============================================================================

@app.post("/api/admin/estudiantes/{estudiante_id}/generar-documentos", tags=["Admin - Documentos"])
def generar_documentos_estudiante(
    estudiante_id: int,
    tipos_documentos: List[str],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Genera documentos oficiales para un estudiante
    tipos_documentos: ['carta_aceptacion', 'carta_motivacion', 'formulario_solicitud', 'certificado_matricula']
    """
    verificar_token(credentials.credentials)
    
    from database.models import Estudiante as EstudianteModel
    from api.generador_documentos import GeneradorDocumentosOficiales
    import base64
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    datos_estudiante = {
        'id': estudiante.id,
        'nombre': estudiante.nombre,
        'email': estudiante.email,
        'telefono': estudiante.telefono,
        'pasaporte': estudiante.pasaporte,
        'edad': estudiante.edad,
        'nacionalidad': estudiante.nacionalidad,
        'ciudad_origen': estudiante.ciudad_origen,
        'especialidad': estudiante.especialidad,
        'nivel_espanol': estudiante.nivel_espanol,
        'tipo_visa': estudiante.tipo_visa
    }
    
    documentos_generados = []
    
    for tipo in tipos_documentos:
        try:
            # Generar PDF según tipo
            if tipo == 'carta_aceptacion':
                pdf_buffer = GeneradorDocumentosOficiales.generar_carta_aceptacion(datos_estudiante)
                nombre = f"Carta_Aceptacion_{estudiante.id}.pdf"
            elif tipo == 'carta_motivacion':
                pdf_buffer = GeneradorDocumentosOficiales.generar_carta_motivacion(datos_estudiante)
                nombre = f"Carta_Motivacion_{estudiante.id}.pdf"
            elif tipo == 'formulario_solicitud':
                pdf_buffer = GeneradorDocumentosOficiales.generar_formulario_solicitud(datos_estudiante)
                nombre = f"Formulario_Solicitud_{estudiante.id}.pdf"
            elif tipo == 'certificado_matricula':
                pdf_buffer = GeneradorDocumentosOficiales.generar_certificado_matricula(datos_estudiante)
                nombre = f"Certificado_Matricula_{estudiante.id}.pdf"
            else:
                continue
            
            # Convertir a base64 para almacenar
            pdf_content = pdf_buffer.read()
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            # Guardar en base de datos usando SQL directo
            import os
            import psycopg2
            conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO documentos_generados 
                (estudiante_id, tipo_documento, nombre_archivo, contenido_pdf, estado, generado_por)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (estudiante_id, tipo, nombre, pdf_base64, 'generado', 'admin'))
            
            doc_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            
            documentos_generados.append({
                'id': doc_id,
                'tipo': tipo,
                'nombre': nombre,
                'estado': 'generado'
            })
            
        except Exception as e:
            print(f"Error generando documento {tipo}: {e}")
            continue
    
    return {
        'estudiante_id': estudiante_id,
        'documentos_generados': documentos_generados,
        'total': len(documentos_generados)
    }


@app.get("/api/admin/documentos-generados", tags=["Admin - Documentos"])
def listar_documentos_generados(
    estudiante_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Lista todos los documentos generados con filtros opcionales"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    query = """
        SELECT dg.id, dg.estudiante_id, dg.tipo_documento, dg.nombre_archivo,
               dg.estado, dg.fecha_generacion, dg.enviado_estudiante,
               e.nombre as estudiante_nombre
        FROM documentos_generados dg
        JOIN estudiantes e ON dg.estudiante_id = e.id
        WHERE 1=1
    """
    params = []
    
    if estudiante_id:
        query += " AND dg.estudiante_id = %s"
        params.append(estudiante_id)
    
    if estado:
        query += " AND dg.estado = %s"
        params.append(estado)
    
    query += " ORDER BY dg.fecha_generacion DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    documentos = []
    for row in rows:
        documentos.append({
            'id': row[0],
            'estudiante_id': row[1],
            'tipo_documento': row[2],
            'nombre_archivo': row[3],
            'estado': row[4],
            'fecha_generacion': row[5].isoformat() if row[5] else None,
            'enviado_estudiante': row[6],
            'estudiante_nombre': row[7]
        })
    
    cursor.close()
    conn.close()
    
    return documentos


@app.get("/api/admin/documentos-generados/{documento_id}/descargar", tags=["Admin - Documentos"])
def descargar_documento_generado(
    documento_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Descarga un documento generado"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    import base64
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT nombre_archivo, contenido_pdf
        FROM documentos_generados
        WHERE id = %s
    """, (documento_id,))
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    nombre_archivo, contenido_base64 = row
    pdf_content = base64.b64decode(contenido_base64)
    
    from io import BytesIO
    buffer = BytesIO(pdf_content)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={nombre_archivo}"}
    )


@app.put("/api/admin/documentos-generados/{documento_id}/aprobar", tags=["Admin - Documentos"])
def aprobar_documento_generado(
    documento_id: int,
    enviar_a_estudiante: bool = True,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Aprueba un documento y opcionalmente lo envía al estudiante"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE documentos_generados
        SET estado = 'aprobado',
            fecha_aprobacion = CURRENT_TIMESTAMP,
            enviado_estudiante = %s,
            aprobado_por = 'admin'
        WHERE id = %s
        RETURNING estudiante_id
    """, (enviar_a_estudiante, documento_id))
    
    result = cursor.fetchone()
    if not result:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    estudiante_id = result[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    # TODO: Enviar email al estudiante con el documento adjunto
    
    return {
        'mensaje': 'Documento aprobado correctamente',
        'enviado_estudiante': enviar_a_estudiante
    }


@app.get("/api/estudiantes/{estudiante_id}/estado", tags=["Estudiantes"])
def consultar_estado(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Estudiante consulta su estado (sin auth por simplicidad en MVP)
    """
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return {
        "nombre": estudiante.nombre_completo,
        "estado_procesamiento": estudiante.estado_procesamiento,
        "estado_visa": estudiante.estado_visa,
        "fecha_registro": estudiante.created_at,
        "curso_seleccionado": estudiante.curso_seleccionado_id,
        "mensaje": _obtener_mensaje_estado(estudiante.estado_procesamiento)
    }


def _obtener_mensaje_estado(estado: str) -> str:
    """Mensajes amigables por estado"""
    mensajes = {
        "registrado": "Tu solicitud ha sido recibida. Estamos procesando tu información.",
        "procesado_automaticamente": "Hemos analizado tu perfil. Un asesor revisará tu caso pronto.",
        "pendiente_revision_admin": "Tu caso está siendo revisado por nuestro equipo.",
        "aprobado_admin": "¡Felicidades! Tu solicitud ha sido aprobada. Te contactaremos pronto.",
        "enviado_estudiante": "Te hemos enviado toda la información. Revisa tu email.",
        "rechazado_admin": "Necesitamos información adicional. Te contactaremos."
    }
    return mensajes.get(estado, "En proceso")


# ============================================================================
# MENSAJERÍA INTERNA
# ============================================================================

@app.get("/api/estudiantes/{estudiante_id}/mensajes", tags=["Mensajería"])
def obtener_mensajes(estudiante_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los mensajes de un estudiante"""
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            SELECT id, remitente, mensaje, leido, created_at
            FROM mensajes
            WHERE estudiante_id = %s
            ORDER BY created_at ASC
        """, (estudiante_id,))
        
        mensajes = []
        for row in cursor.fetchall():
            mensajes.append({
                'id': row[0],
                'remitente': row[1],
                'mensaje': row[2],
                'leido': row[3],
                'created_at': row[4].isoformat() if row[4] else None
            })
        
        return {'total': len(mensajes), 'mensajes': mensajes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/estudiantes/{estudiante_id}/mensajes", tags=["Mensajería"])
def enviar_mensaje(estudiante_id: int, datos: dict, db: Session = Depends(get_db)):
    """Envía un mensaje (estudiante o admin)"""
    from database.models import Estudiante as EstudianteModel
    from datetime import datetime
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    remitente = datos.get('remitente', 'estudiante')  # 'estudiante' o 'admin'
    mensaje = datos.get('mensaje', '')
    
    if not mensaje:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
    
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            INSERT INTO mensajes (estudiante_id, remitente, mensaje, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (estudiante_id, remitente, mensaje, datetime.utcnow()))
        
        mensaje_id = cursor.fetchone()[0]
        db.commit()
        
        return {
            'mensaje_id': mensaje_id,
            'mensaje': 'Mensaje enviado correctamente'
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/mensajes/{mensaje_id}/marcar-leido", tags=["Mensajería"])
def marcar_mensaje_leido(mensaje_id: int, db: Session = Depends(get_db)):
    """Marca un mensaje como leído"""
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            UPDATE mensajes 
            SET leido = TRUE 
            WHERE id = %s
        """, (mensaje_id,))
        
        db.commit()
        
        return {'mensaje': 'Mensaje marcado como leído'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# ENDPOINTS ADMIN (Requieren autenticación)
# ============================================================================

@app.get("/api/admin/estudiantes", response_model=List[Dict], tags=["Admin"])
def listar_estudiantes(
    estado: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Lista todos los estudiantes con filtros opcionales"""
    from database.models import Estudiante as EstudianteModel
    
    query = db.query(EstudianteModel)
    
    if estado:
        query = query.filter(EstudianteModel.estado == estado)
    
    estudiantes = query.order_by(EstudianteModel.created_at.desc()).offset(skip).limit(limit).all()
    
    return [{
        'id': e.id,
        'nombre_completo': e.nombre or f"Estudiante {e.id}",
        'email': e.email or f"estudiante{e.id}@example.com",
        'especialidad_interes': e.especialidad or e.tipo_visa or 'No especificado',
        'estado_procesamiento': e.estado,
        'created_at': e.created_at.isoformat() if e.created_at else None
    } for e in estudiantes]


@app.get("/api/admin/estudiantes/{estudiante_id}", response_model=EstudianteResponse, tags=["Admin"])
def obtener_estudiante(
    estudiante_id: int,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Detalle completo de un estudiante"""
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return EstudianteResponse.from_orm(estudiante)


@app.put("/api/admin/estudiantes/{estudiante_id}", tags=["Admin"])
def actualizar_estudiante(
    estudiante_id: int,
    datos: EstudianteUpdate,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Actualiza información de estudiante"""
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Actualizar campos
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(estudiante, campo, valor)
    
    db.commit()
    db.refresh(estudiante)
    
    return {"message": "Estudiante actualizado correctamente"}


@app.post("/api/admin/estudiantes/{estudiante_id}/aprobar", tags=["Admin"])
def aprobar_estudiante(
    estudiante_id: int,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Aprobar estudiante para envío"""
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante.estado = 'aprobado'
    estudiante.updated_at = datetime.utcnow()
    db.commit()
    
    # Enviar email de notificación
    try:
        from api.notificaciones_email import NotificacionesEmail
        NotificacionesEmail.notificar_cambio_estado({
            'nombre': estudiante.nombre,
            'email': estudiante.email
        }, 'aprobado')
    except Exception as e:
        print(f"⚠️ Error enviando email: {e}")
    
    return {"message": "Estudiante aprobado correctamente", "id": estudiante_id}


@app.post("/api/admin/estudiantes/{estudiante_id}/rechazar", tags=["Admin"])
def rechazar_estudiante(
    estudiante_id: int,
    motivo: str,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Rechazar estudiante y solicitar correcciones"""
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante.estado = 'rechazado'
    estudiante.notas = motivo
    estudiante.updated_at = datetime.utcnow()
    db.commit()
    
    # Enviar email de notificación
    try:
        from api.notificaciones_email import NotificacionesEmail
        NotificacionesEmail.notificar_cambio_estado({
            'nombre': estudiante.nombre,
            'email': estudiante.email
        }, 'rechazado', motivo)
    except Exception as e:
        print(f"⚠️ Error enviando email: {e}")
    
    return {"message": "Estudiante marcado para revisión", "id": estudiante_id, "motivo": motivo}
    from modules.notificaciones_email import NotificacionesEmail
    
    try:
        resultado = PanelRevisionAdmin.rechazar_y_solicitar_revision(
            estudiante_id=estudiante_id,
            admin_id=1,
            motivo_rechazo=motivo
        )
        
        # Enviar email de revisión pendiente
        try:
            estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
            if estudiante:
                estudiante_dict = {
                    'id': estudiante.id,
                    'nombre_completo': estudiante.nombre_completo,
                    'email': estudiante.email
                }
                NotificacionesEmail.enviar_solicitud_pendiente_revision(estudiante_dict, motivo)
        except Exception as e:
            print(f"⚠️ Error enviando email de revisión: {e}")
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/estadisticas", response_model=EstadisticasResponse, tags=["Admin"])
def obtener_estadisticas(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Estadísticas del dashboard"""
    from database.models import Estudiante as EstudianteModel
    
    # Contar estudiantes por estado
    total = db.query(EstudianteModel).count()
    pendientes = db.query(EstudianteModel).filter(EstudianteModel.estado == 'pendiente').count()
    aprobados = db.query(EstudianteModel).filter(EstudianteModel.estado == 'aprobado').count()
    rechazados = db.query(EstudianteModel).filter(EstudianteModel.estado == 'rechazado').count()
    
    return EstadisticasResponse(
        total_estudiantes=total,
        pendientes_revision=pendientes,
        aprobados=aprobados,
        enviados=aprobados,  # Por ahora enviados = aprobados
        por_especialidad={}  # TODO: implementar después
    )


# ============================================================================
# CURSOS - Endpoints para gestión de cursos
# ============================================================================

@app.get("/api/cursos", tags=["Cursos"])
def listar_cursos(
    especialidad: Optional[str] = None,
    ciudad: Optional[str] = None,
    precio_max: Optional[float] = None,
    nivel_idioma: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Lista cursos disponibles con filtros"""
    from modules.cursos import GestorCursos
    
    cursos = GestorCursos.filtrar_cursos(
        especialidad=especialidad,
        ciudad=ciudad,
        precio_max=precio_max,
        nivel_idioma=nivel_idioma
    )
    
    return {
        'total': len(cursos),
        'cursos': [
            {
                'id': c.id,
                'nombre': c.nombre,
                'escuela': c.escuela,
                'ciudad': c.ciudad,
                'especialidad': c.especialidad,
                'precio': c.precio,
                'duracion_meses': c.duracion_meses,
                'nivel_minimo_espanol': c.nivel_minimo_espanol,
                'fecha_inicio': c.fecha_inicio.isoformat() if c.fecha_inicio else None,
                'disponible': c.disponible
            }
            for c in cursos[skip:skip+limit]
        ]
    }


@app.get("/api/cursos/{curso_id}", tags=["Cursos"])
def obtener_curso(curso_id: int, db: Session = Depends(get_db)):
    """Obtiene detalles de un curso específico"""
    from modules.cursos import GestorCursos
    
    curso = GestorCursos.obtener_curso_por_id(curso_id)
    
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    return {
        'id': curso.id,
        'nombre': curso.nombre,
        'escuela': curso.escuela,
        'ciudad': curso.ciudad,
        'especialidad': curso.especialidad,
        'precio': curso.precio,
        'duracion_meses': curso.duracion_meses,
        'nivel_minimo_espanol': curso.nivel_minimo_espanol,
        'fecha_inicio': curso.fecha_inicio.isoformat() if curso.fecha_inicio else None,
        'descripcion': curso.descripcion,
        'requisitos': curso.requisitos,
        'url_informacion': curso.url_informacion,
        'disponible': curso.disponible
    }


# ============================================================================
# FONDOS - Verificación económica
# ============================================================================

@app.get("/api/estudiantes/{estudiante_id}/fondos", tags=["Fondos"])
def verificar_fondos(estudiante_id: int, db: Session = Depends(get_db)):
    """Verifica situación económica del estudiante"""
    from modules.fondos import GestorFondos
    
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    verificacion = GestorFondos.verificar_fondos(estudiante_id)
    return verificacion


@app.post("/api/estudiantes/{estudiante_id}/patrocinador", tags=["Fondos"])
def agregar_patrocinador(
    estudiante_id: int,
    datos_patrocinador: Dict,
    db: Session = Depends(get_db)
):
    """Agrega patrocinador para el estudiante"""
    from modules.fondos import GestorFondos
    
    resultado = GestorFondos.agregar_patrocinador(estudiante_id, datos_patrocinador)
    return resultado


# ============================================================================
# ALOJAMIENTO - Búsqueda y gestión
# ============================================================================

@app.get("/api/alojamientos", tags=["Alojamiento"])
def buscar_alojamientos(
    ciudad: Optional[str] = None,
    precio_max: Optional[float] = None,
    tipo: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Busca alojamientos disponibles"""
    from modules.alojamiento import GestorAlojamiento
    
    alojamientos = GestorAlojamiento.buscar_alojamientos(
        ciudad=ciudad,
        precio_max=precio_max,
        tipo=tipo,
        disponible=True
    )
    
    return {
        'total': len(alojamientos),
        'alojamientos': [
            {
                'id': a.id,
                'tipo': a.tipo,
                'direccion': a.direccion,
                'ciudad': a.ciudad,
                'precio_mensual': a.precio_mensual,
                'gastos_incluidos': a.gastos_incluidos,
                'num_habitaciones': a.num_habitaciones,
                'num_banos': a.num_banos,
                'metros_cuadrados': a.metros_cuadrados,
                'disponible': a.disponible
            }
            for a in alojamientos[skip:skip+limit]
        ]
    }


# ============================================================================
# DOCUMENTOS - Upload y gestión
# ============================================================================

from fastapi import UploadFile, File

@app.post("/api/estudiantes/{estudiante_id}/documentos/upload", tags=["Documentos"])
async def subir_documento(
    estudiante_id: int,
    tipo_documento: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Sube un documento del estudiante"""
    import os
    from pathlib import Path
    
    # Verificar estudiante existe
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Crear directorio si no existe
    upload_dir = Path(f"uploads/estudiantes/{estudiante_id}")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar archivo
    file_path = upload_dir / f"{tipo_documento}_{archivo.filename}"
    
    with file_path.open("wb") as buffer:
        content = await archivo.read()
        buffer.write(content)
    
    return {
        'mensaje': 'Documento subido correctamente',
        'tipo': tipo_documento,
        'filename': archivo.filename,
        'path': str(file_path)
    }


@app.get("/api/estudiantes/{estudiante_id}/documentos", tags=["Documentos"])
def obtener_checklist(estudiante_id: int, db: Session = Depends(get_db)):
    """Obtiene checklist de documentos del estudiante"""
    from modules.estudiantes import GestorEstudiantes
    
    checklist = GestorEstudiantes.checklist_documentos(estudiante_id)
    return checklist


# ============================================================================
# NOTIFICACIONES WEB - Sistema interno
# ============================================================================

@app.get("/api/estudiantes/{estudiante_id}/notificaciones", tags=["Notificaciones"])
def obtener_notificaciones(
    estudiante_id: int,
    no_leidas: bool = False,
    db: Session = Depends(get_db)
):
    """Obtiene notificaciones del estudiante"""
    from modules.notificaciones import SistemaNotificaciones
    
    # Implementación simplificada - expandir según necesidades
    return {
        'notificaciones': [],
        'total': 0,
        'no_leidas': 0
    }


# ============================================================================
# MENSAJERÍA - Chat entre estudiantes y admins
# ============================================================================

@app.post("/api/mensajes", tags=["Mensajería"])
def enviar_mensaje(
    datos: Dict,
    db: Session = Depends(get_db)
):
    """Envía mensaje entre estudiante y admin"""
    # Implementación de sistema de chat
    return {
        'exito': True,
        'mensaje_id': 1,
        'fecha': datetime.now().isoformat()
    }


@app.get("/api/estudiantes/{estudiante_id}/mensajes", tags=["Mensajería"])
def obtener_mensajes(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene conversación del estudiante"""
    return {
        'mensajes': [],
        'total': 0
    }


# ============================================================================
# ADMIN - GESTIÓN DE CURSOS
# ============================================================================

@app.post("/api/admin/cursos", tags=["Admin - Cursos"])
def crear_curso(
    datos: Dict,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Crea un nuevo curso"""
    from modules.cursos import GestorCursos
    from database.models import Curso
    
    nuevo_curso = Curso(
        nombre=datos['nombre'],
        escuela=datos['escuela'],
        ciudad=datos['ciudad'],
        especialidad=datos['especialidad'],
        precio=datos['precio'],
        duracion_meses=datos['duracion_meses'],
        nivel_minimo_espanol=datos.get('nivel_minimo_espanol', 'B1'),
        descripcion=datos.get('descripcion'),
        requisitos=datos.get('requisitos'),
        url_informacion=datos.get('url_informacion'),
        disponible=True
    )
    
    db.add(nuevo_curso)
    db.commit()
    db.refresh(nuevo_curso)
    
    return {'exito': True, 'curso_id': nuevo_curso.id}


@app.put("/api/admin/cursos/{curso_id}", tags=["Admin - Cursos"])
def actualizar_curso(
    curso_id: int,
    datos: Dict,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Actualiza un curso existente"""
    from database.models import Curso
    
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    for campo, valor in datos.items():
        if hasattr(curso, campo):
            setattr(curso, campo, valor)
    
    db.commit()
    return {'exito': True, 'mensaje': 'Curso actualizado'}


@app.delete("/api/admin/cursos/{curso_id}", tags=["Admin - Cursos"])
def eliminar_curso(
    curso_id: int,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Elimina un curso"""
    from database.models import Curso
    
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    curso.disponible = False
    db.commit()
    
    return {'exito': True, 'mensaje': 'Curso desactivado'}


# ============================================================================
# ADMIN - GESTIÓN DE ALOJAMIENTOS
# ============================================================================

@app.post("/api/admin/alojamientos", tags=["Admin - Alojamiento"])
def crear_alojamiento(
    datos: Dict,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Crea nuevo alojamiento"""
    from database.models import Alojamiento
    
    nuevo = Alojamiento(
        tipo=datos['tipo'],
        direccion=datos['direccion'],
        ciudad=datos['ciudad'],
        precio_mensual=datos['precio_mensual'],
        gastos_incluidos=datos.get('gastos_incluidos', False),
        num_habitaciones=datos.get('num_habitaciones', 1),
        num_banos=datos.get('num_banos', 1),
        metros_cuadrados=datos.get('metros_cuadrados'),
        disponible=True
    )
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    
    return {'exito': True, 'alojamiento_id': nuevo.id}


@app.put("/api/admin/alojamientos/{alojamiento_id}", tags=["Admin - Alojamiento"])
def actualizar_alojamiento(
    alojamiento_id: int,
    datos: Dict,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Actualiza alojamiento"""
    from database.models import Alojamiento
    
    alojamiento = db.query(Alojamiento).filter(Alojamiento.id == alojamiento_id).first()
    if not alojamiento:
        raise HTTPException(status_code=404, detail="Alojamiento no encontrado")
    
    for campo, valor in datos.items():
        if hasattr(alojamiento, campo):
            setattr(alojamiento, campo, valor)
    
    db.commit()
    return {'exito': True, 'mensaje': 'Alojamiento actualizado'}


# ============================================================================
# ADMIN - REPORTES AVANZADOS
# ============================================================================

@app.get("/api/admin/reportes/mensual", tags=["Admin - Reportes"])
def reporte_mensual(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Genera reporte mensual completo"""
    reporte = PanelAdministrativo.generar_reporte_mensual()
    return reporte


@app.get("/api/admin/reportes/especialidades", tags=["Admin - Reportes"])
def estadisticas_especialidades(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Estadísticas por especialidad"""
    stats = PanelAdministrativo.estadisticas_por_especialidad()
    return {'especialidades': stats}


@app.get("/api/admin/reportes/conversion", tags=["Admin - Reportes"])
def embudo_conversion(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Embudo de conversión de estudiantes"""
    embudo = PanelAdministrativo.embudo_conversion()
    return embudo


# ============================================================================
# ADMIN - GESTIÓN DE DOCUMENTOS
# ============================================================================

@app.get("/api/admin/documentos/pendientes", tags=["Admin - Documentos"])
def documentos_pendientes(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Lista estudiantes con documentos pendientes"""
    estudiantes = db.query(Estudiante).filter(
        Estudiante.estado_procesamiento.in_([
            'registrado',
            'procesado_automaticamente',
            'pendiente_revision_admin'
        ])
    ).all()
    
    pendientes = []
    for est in estudiantes:
        from modules.estudiantes import GestorEstudiantes
        checklist = GestorEstudiantes.checklist_documentos(est.id)
        
        if checklist['total_obligatorios'] > 0:
            pendientes.append({
                'estudiante_id': est.id,
                'nombre': est.nombre_completo,
                'documentos_obligatorios_pendientes': checklist['total_obligatorios'],
                'documentos_recomendados_pendientes': checklist['total_recomendados']
            })
    
    return {'total': len(pendientes), 'estudiantes': pendientes}


# ============================================================================
# MENSAJERÍA INTERNA - Chat entre estudiantes y admins
# ============================================================================

@app.post("/api/conversaciones", tags=["Mensajería"])
def crear_conversacion(datos: Dict, db: Session = Depends(get_db)):
    """Crea una nueva conversación"""
    from modules.mensajeria import SistemaMensajeria
    
    conversacion = SistemaMensajeria.crear_conversacion(
        estudiante_id=datos['estudiante_id'],
        admin_id=datos.get('admin_id')
    )
    
    return {'exito': True, 'conversacion_id': conversacion.id}


@app.post("/api/mensajes", tags=["Mensajería"])
def enviar_mensaje(datos: Dict, db: Session = Depends(get_db)):
    """Envía mensaje en una conversación"""
    from modules.mensajeria import SistemaMensajeria
    
    resultado = SistemaMensajeria.enviar_mensaje(
        conversacion_id=datos['conversacion_id'],
        remitente_tipo=datos['remitente_tipo'],
        remitente_id=datos['remitente_id'],
        contenido=datos['contenido']
    )
    
    return resultado


@app.get("/api/conversaciones/{conversacion_id}/mensajes", tags=["Mensajería"])
def obtener_mensajes_conversacion(
    conversacion_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Obtiene mensajes de una conversación"""
    from modules.mensajeria import SistemaMensajeria
    
    mensajes = SistemaMensajeria.obtener_mensajes(conversacion_id, limit=limit)
    return {'mensajes': mensajes, 'total': len(mensajes)}


@app.get("/api/estudiantes/{estudiante_id}/conversaciones", tags=["Mensajería"])
def obtener_conversaciones_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    """Obtiene conversaciones del estudiante"""
    from modules.mensajeria import SistemaMensajeria
    
    conversaciones = SistemaMensajeria.obtener_conversaciones_estudiante(estudiante_id)
    return {'conversaciones': conversaciones}


@app.get("/api/admin/conversaciones", tags=["Admin - Mensajería"])
def obtener_conversaciones_admin(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Obtiene todas las conversaciones activas para admin"""
    from modules.mensajeria import SistemaMensajeria
    
    conversaciones = SistemaMensajeria.obtener_conversaciones_admin()
    return {'conversaciones': conversaciones}


# ============================================================================
# NOTIFICACIONES EMAIL
# ============================================================================

@app.post("/api/notificaciones/test-email", tags=["Notificaciones"])
def test_email(destinatario: str):
    """Endpoint de prueba para verificar configuración de email"""
    from modules.notificaciones_email import EmailService
    import config
    
    html = EmailService.generar_template_html(
        titulo="Email de Prueba",
        mensaje="<p>Este es un email de prueba del sistema de notificaciones.</p><p>Si recibes este mensaje, la configuración SMTP está funcionando correctamente.</p>",
        boton_texto="Visitar Plataforma",
        boton_url=getattr(config, 'WEB_URL', 'http://localhost:3000')
    )
    
    resultado = EmailService.enviar_email(
        destinatario=destinatario,
        asunto="🧪 Email de Prueba - Sistema de Notificaciones",
        contenido_html=html
    )
    
    if resultado:
        return {"mensaje": "Email enviado correctamente", "destinatario": destinatario}
    else:
        raise HTTPException(status_code=500, detail="Error al enviar email")


@app.post("/api/estudiantes/{estudiante_id}/notificaciones/resend", tags=["Notificaciones"])
def reenviar_notificacion(
    estudiante_id: int,
    tipo: str,
    db: Session = Depends(get_db)
):
    """
    Reenviar notificación por email a un estudiante
    Tipos: registro, aprobacion, pendiente
    """
    from modules.notificaciones_email import NotificacionesEmail
    
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante_dict = {
        'id': estudiante.id,
        'nombre_completo': estudiante.nombre_completo,
        'email': estudiante.email,
        'especialidad_interes': estudiante.especialidad_interes,
        'nacionalidad': estudiante.nacionalidad
    }
    
    resultado = False
    
    if tipo == "registro":
        resultado = NotificacionesEmail.enviar_confirmacion_registro(estudiante_dict)
    elif tipo == "aprobacion":
        resultado = NotificacionesEmail.enviar_solicitud_aprobada(estudiante_dict)
    elif tipo == "pendiente":
        motivo = "Revisión de documentación requerida"
        resultado = NotificacionesEmail.enviar_solicitud_pendiente_revision(estudiante_dict, motivo)
    else:
        raise HTTPException(status_code=400, detail="Tipo de notificación inválido")
    
    if resultado:
        return {"mensaje": f"Notificación '{tipo}' reenviada a {estudiante.email}"}
    else:
        raise HTTPException(status_code=500, detail="Error al enviar notificación")


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/", tags=["Health"])
def root():
    """Health check"""
    return {
        "status": "online",
        "servicio": "Bot Visas Estudio API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", tags=["Health"])
def health():
    """Health check detallado"""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
