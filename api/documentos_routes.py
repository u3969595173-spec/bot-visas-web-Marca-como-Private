from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database.models import get_db, Estudiante, Notificacion
from api.auth import verificar_token
from datetime import datetime
import os
import psycopg2
import base64
import io
import zipfile

router = APIRouter()

CATEGORIAS_PERMITIDAS = ['pasaporte', 'visa', 'academicos', 'financieros', 'otros']
TIPOS_ARCHIVO_PERMITIDOS = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/documentos/{estudiante_id}/subir")
async def subir_documentos(
    estudiante_id: int,
    archivos: list[UploadFile] = File(...),
    categorias: str = Form(...),
    db: Session = Depends(get_db)
):
    """Subir múltiples documentos de un estudiante"""
    try:
        # Parsear categorías (vienen como string separado por comas)
        categorias_list = [c.strip() for c in categorias.split(',')]
        
        if len(archivos) != len(categorias_list):
            raise HTTPException(status_code=400, detail="Número de archivos y categorías no coincide")
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        documentos_subidos = []
        
        for i, archivo in enumerate(archivos):
            categoria = categorias_list[i]
            
            # Validar categoría
            if categoria not in CATEGORIAS_PERMITIDAS:
                continue
            
            # Validar tipo de archivo
            if archivo.content_type not in TIPOS_ARCHIVO_PERMITIDOS:
                continue
            
            # Leer contenido
            contenido = await archivo.read()
            
            # Validar tamaño
            if len(contenido) > MAX_FILE_SIZE:
                continue
            
            # Convertir a base64 para almacenar en DB
            contenido_base64 = base64.b64encode(contenido).decode('utf-8')
            
            # Insertar en BD
            cursor.execute("""
                INSERT INTO documentos (
                    estudiante_id, tipo_documento, nombre_archivo, url_archivo,
                    categoria, contenido_base64, mime_type, tamano_archivo,
                    estado_revision, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                estudiante_id,
                categoria,  # tipo_documento = categoria
                archivo.filename,
                f'base64://{archivo.filename}',  # url_archivo placeholder para base64
                categoria,
                contenido_base64,
                archivo.content_type,
                len(contenido),
                'pendiente',
                datetime.now()
            ))
            
            doc_id = cursor.fetchone()[0]
            
            documentos_subidos.append({
                'id': doc_id,
                'nombre': archivo.filename,
                'categoria': categoria,
                'tamano': len(contenido)
            })
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'message': f'{len(documentos_subidos)} documentos subidos',
            'documentos': documentos_subidos
        }
    except Exception as e:
        print(f"❌ Error subiendo documentos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documentos/{estudiante_id}/listar")
def listar_documentos(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """Listar todos los documentos de un estudiante"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nombre_archivo, categoria, mime_type, 
                   tamano_archivo, estado_revision, comentario_admin, 
                   created_at, updated_at
            FROM documentos
            WHERE estudiante_id = %s
            ORDER BY created_at DESC
        """, (estudiante_id,))
        
        documentos = []
        for row in cursor.fetchall():
            documentos.append({
                'id': row[0],
                'nombre': row[1],
                'categoria': row[2],
                'mime_type': row[3],
                'tamano': row[4],
                'estado_revision': row[5],
                'comentario_admin': row[6],
                'created_at': row[7].isoformat() if row[7] else None,
                'updated_at': row[8].isoformat() if row[8] else None
            })
        
        # Calcular progreso
        total_categorias = len(CATEGORIAS_PERMITIDAS)
        categorias_completadas = len(set([doc['categoria'] for doc in documentos if doc['estado_revision'] != 'rechazado']))
        progreso = round((categorias_completadas / total_categorias) * 100, 2)
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'documentos': documentos,
            'progreso': progreso,
            'total_documentos': len(documentos)
        }
    except Exception as e:
        print(f"❌ Error listando documentos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documentos/{doc_id}/descargar")
def descargar_documento(
    doc_id: int,
    db: Session = Depends(get_db)
):
    """Descargar un documento específico"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nombre_archivo, contenido_base64, mime_type
            FROM documentos
            WHERE id = %s
        """, (doc_id,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        nombre, contenido_b64, mime_type = row
        contenido = base64.b64decode(contenido_b64)
        
        cursor.close()
        conn.close()
        
        return StreamingResponse(
            io.BytesIO(contenido),
            media_type=mime_type,
            headers={
                "Content-Disposition": f"attachment; filename={nombre}"
            }
        )
    except Exception as e:
        print(f"❌ Error descargando documento: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documentos/{estudiante_id}/descargar-zip")
def descargar_documentos_zip(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """Descargar todos los documentos de un estudiante en ZIP"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nombre_archivo, contenido_base64
            FROM documentos
            WHERE estudiante_id = %s
        """, (estudiante_id,))
        
        documentos = cursor.fetchall()
        
        if not documentos:
            raise HTTPException(status_code=404, detail="No hay documentos para descargar")
        
        # Crear ZIP en memoria
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for nombre, contenido_b64 in documentos:
                contenido = base64.b64decode(contenido_b64)
                zip_file.writestr(nombre, contenido)
        
        zip_buffer.seek(0)
        
        cursor.close()
        conn.close()
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=estudiante_{estudiante_id}_documentos.zip"
            }
        )
    except Exception as e:
        print(f"❌ Error creando ZIP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/admin/documentos/{doc_id}/revisar")
def revisar_documento(
    doc_id: int,
    estado: str = Form(...),  # 'aprobado' o 'rechazado'
    comentario: str = Form(None),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Admin revisa y aprueba/rechaza un documento"""
    verificar_token(credentials.credentials)
    
    try:
        if estado not in ['aprobado', 'rechazado']:
            raise HTTPException(status_code=400, detail="Estado inválido")
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Actualizar documento
        cursor.execute("""
            UPDATE documentos
            SET estado_revision = %s,
                comentario_admin = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING estudiante_id, nombre_archivo
        """, (estado, comentario, datetime.now(), doc_id))
        
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        estudiante_id, nombre_archivo = result
        
        # Crear notificación
        icono = '✅' if estado == 'aprobado' else '❌'
        titulo = f"Documento {estado}"
        mensaje = f"Tu documento '{nombre_archivo}' ha sido {estado}"
        if comentario:
            mensaje += f". Comentario: {comentario}"
        
        cursor.execute("""
            INSERT INTO notificaciones (
                estudiante_id, tipo, titulo, mensaje, icono, 
                prioridad, leida, url_accion, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            estudiante_id, 'documento', titulo, mensaje, icono,
            'alta', False, '/estudiante/documentos', datetime.now()
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'message': f'Documento {estado} correctamente',
            'doc_id': doc_id
        }
    except Exception as e:
        print(f"❌ Error revisando documento: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/documentos/todos")
def listar_todos_documentos(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Admin lista todos los estudiantes con sus documentos"""
    verificar_token(credentials.credentials)
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                e.id,
                e.nombre,
                e.email,
                COUNT(d.id) as total_documentos,
                COUNT(CASE WHEN d.estado_revision = 'pendiente' THEN 1 END) as pendientes,
                COUNT(CASE WHEN d.estado_revision = 'aprobado' THEN 1 END) as aprobados,
                COUNT(CASE WHEN d.estado_revision = 'rechazado' THEN 1 END) as rechazados
            FROM estudiantes e
            LEFT JOIN documentos d ON e.id = d.estudiante_id
            GROUP BY e.id, e.nombre, e.email
            HAVING COUNT(d.id) > 0
            ORDER BY COUNT(CASE WHEN d.estado_revision = 'pendiente' THEN 1 END) DESC
        """)
        
        estudiantes = []
        for row in cursor.fetchall():
            estudiantes.append({
                'id': row[0],
                'nombre': row[1] or 'Sin nombre',
                'email': row[2],
                'total_documentos': row[3],
                'pendientes': row[4],
                'aprobados': row[5],
                'rechazados': row[6]
            })
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'estudiantes': estudiantes
        }
    except Exception as e:
        print(f"❌ Error listando documentos admin: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documentos/{doc_id}/eliminar")
def eliminar_documento(
    doc_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un documento"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM documentos WHERE id = %s", (doc_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'message': 'Documento eliminado'
        }
    except Exception as e:
        print(f"❌ Error eliminando documento: {e}")
        raise HTTPException(status_code=500, detail=str(e))
