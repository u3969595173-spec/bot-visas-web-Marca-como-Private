from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.models import get_db
from api.auth import verificar_token
from datetime import datetime, timedelta
import os
import psycopg2

router = APIRouter()

@router.get("/admin/analytics/general")
def obtener_analytics_general(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Obtener métricas generales del dashboard"""
    verificar_token(credentials.credentials)
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Total estudiantes
        cursor.execute("SELECT COUNT(*) FROM estudiantes")
        total_estudiantes = cursor.fetchone()[0]
        
        # Estudiantes por estado
        cursor.execute("""
            SELECT estado, COUNT(*) 
            FROM estudiantes 
            WHERE estado IS NOT NULL
            GROUP BY estado
        """)
        estados = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Aprobados y rechazados
        aprobados = estados.get('aprobado', 0) + estados.get('visa_aprobada', 0)
        rechazados = estados.get('rechazado', 0) + estados.get('visa_rechazada', 0)
        pendientes = estados.get('pendiente', 0)
        
        # Tasa de aprobación
        total_procesados = aprobados + rechazados
        tasa_aprobacion = (aprobados / total_procesados * 100) if total_procesados > 0 else 0
        
        # Estudiantes registrados últimos 30 días
        cursor.execute("""
            SELECT COUNT(*) 
            FROM estudiantes 
            WHERE created_at >= NOW() - INTERVAL '30 days'
        """)
        nuevos_30_dias = cursor.fetchone()[0]
        
        # Mensajes chat último mes
        cursor.execute("""
            SELECT COUNT(*) 
            FROM mensajes_chat 
            WHERE created_at >= NOW() - INTERVAL '30 days'
        """)
        mensajes_mes = cursor.fetchone()[0]
        
        # Simulador completados (verificar si tabla existe)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_name = 'resultados_simulador'
        """)
        tabla_existe = cursor.fetchone()[0] > 0
        
        if tabla_existe:
            cursor.execute("""
                SELECT COUNT(DISTINCT estudiante_id) 
                FROM resultados_simulador
            """)
            simulador_completados = cursor.fetchone()[0]
        else:
            simulador_completados = 0
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "metricas": {
                "total_estudiantes": total_estudiantes,
                "aprobados": aprobados,
                "rechazados": rechazados,
                "pendientes": pendientes,
                "tasa_aprobacion": round(tasa_aprobacion, 2),
                "nuevos_30_dias": nuevos_30_dias,
                "mensajes_mes": mensajes_mes,
                "simulador_completados": simulador_completados,
                "engagement_rate": round((simulador_completados / total_estudiantes * 100) if total_estudiantes > 0 else 0, 2)
            }
        }
    except Exception as e:
        print(f"❌ Error obteniendo analytics general: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/analytics/por-pais")
def obtener_estudiantes_por_pais(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Estudiantes agrupados por país de origen"""
    verificar_token(credentials.credentials)
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nacionalidad, COUNT(*) as total
            FROM estudiantes
            WHERE nacionalidad IS NOT NULL
            GROUP BY nacionalidad
            ORDER BY total DESC
            LIMIT 15
        """)
        
        paises = [{"pais": row[0], "total": row[1]} for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "paises": paises
        }
    except Exception as e:
        print(f"❌ Error obteniendo por país: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/analytics/por-especialidad")
def obtener_estudiantes_por_especialidad(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Estudiantes agrupados por especialidad"""
    verificar_token(credentials.credentials)
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT especialidad, COUNT(*) as total
            FROM estudiantes
            WHERE especialidad IS NOT NULL AND especialidad != 'N/A'
            GROUP BY especialidad
            ORDER BY total DESC
            LIMIT 10
        """)
        
        especialidades = [{"especialidad": row[0], "total": row[1]} for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "especialidades": especialidades
        }
    except Exception as e:
        print(f"❌ Error obteniendo por especialidad: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/analytics/crecimiento-mensual")
def obtener_crecimiento_mensual(
    meses: int = 6,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Crecimiento de estudiantes por mes"""
    verificar_token(credentials.credentials)
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT 
                TO_CHAR(created_at, 'YYYY-MM') as mes,
                COUNT(*) as total
            FROM estudiantes
            WHERE created_at >= NOW() - INTERVAL '{meses} months'
            GROUP BY mes
            ORDER BY mes ASC
        """)
        
        crecimiento = [{"mes": row[0], "total": row[1]} for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "crecimiento": crecimiento
        }
    except Exception as e:
        print(f"❌ Error obteniendo crecimiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/analytics/estados-visa")
def obtener_distribucion_estados(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Distribución de estudiantes por estado de visa"""
    verificar_token(credentials.credentials)
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COALESCE(estado, 'sin_estado') as estado,
                COUNT(*) as total
            FROM estudiantes
            GROUP BY estado
            ORDER BY total DESC
        """)
        
        estados = [{"estado": row[0], "total": row[1]} for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "estados": estados
        }
    except Exception as e:
        print(f"❌ Error obteniendo estados: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/analytics/universidades-populares")
def obtener_universidades_populares(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Top universidades más buscadas"""
    verificar_token(credentials.credentials)
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nombre, COALESCE(visitas, 0) as visitas
            FROM universidades_espana
            ORDER BY visitas DESC
            LIMIT 10
        """)
        
        universidades = [{"nombre": row[0], "visitas": row[1]} for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "universidades": universidades
        }
    except Exception as e:
        print(f"❌ Error obteniendo universidades: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/analytics/engagement")
def obtener_metricas_engagement(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Métricas de engagement de estudiantes"""
    verificar_token(credentials.credentials)
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Total estudiantes
        cursor.execute("SELECT COUNT(*) FROM estudiantes")
        total = cursor.fetchone()[0]
        
        # Simulador completados (verificar si tabla existe)
        try:
            cursor.execute("SELECT COUNT(DISTINCT estudiante_id) FROM resultados_simulador")
            simulador = cursor.fetchone()[0]
        except:
            simulador = 0
        
        # Alertas creadas (verificar si tabla existe)
        try:
            cursor.execute("SELECT COUNT(DISTINCT estudiante_id) FROM alertas_fechas")
            alertas = cursor.fetchone()[0]
        except:
            alertas = 0
        
        # Chat activo
        try:
            cursor.execute("SELECT COUNT(DISTINCT estudiante_id) FROM mensajes_chat")
            chat = cursor.fetchone()[0]
        except:
            chat = 0
        
        # Documentos subidos
        try:
            cursor.execute("SELECT COUNT(DISTINCT estudiante_id) FROM documentos WHERE tipo_documento IS NOT NULL")
            documentos = cursor.fetchone()[0]
        except:
            documentos = 0
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "engagement": {
                "total_estudiantes": total,
                "simulador_completado": simulador,
                "alertas_configuradas": alertas,
                "chat_activo": chat,
                "documentos_subidos": documentos,
                "porcentajes": {
                    "simulador": round((simulador / total * 100) if total > 0 else 0, 2),
                    "alertas": round((alertas / total * 100) if total > 0 else 0, 2),
                    "chat": round((chat / total * 100) if total > 0 else 0, 2),
                    "documentos": round((documentos / total * 100) if total > 0 else 0, 2)
                }
            }
        }
    except Exception as e:
        print(f"❌ Error obteniendo engagement: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/analytics/exportar-csv")
def exportar_estudiantes_csv(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Exportar todos los estudiantes a CSV"""
    verificar_token(credentials.credentials)
    
    try:
        import io
        import csv
        from fastapi.responses import StreamingResponse
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nombre, email, telefono, pasaporte, nacionalidad, ciudad_origen,
                   especialidad, nivel_espanol, tipo_visa, estado, created_at
            FROM estudiantes
            ORDER BY created_at DESC
        """)
        
        # Crear CSV en memoria
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            'ID', 'Nombre', 'Email', 'Teléfono', 'Pasaporte', 'Nacionalidad',
            'Ciudad Origen', 'Especialidad', 'Nivel Español', 'Tipo Visa',
            'Estado', 'Fecha Registro'
        ])
        
        # Datos
        for row in cursor.fetchall():
            writer.writerow([
                row[0],
                row[1] or '',
                row[2] or '',
                row[3] or '',
                row[4] or '',
                row[5] or '',
                row[6] or '',
                row[7] or '',
                row[8] or '',
                row[9] or '',
                row[10] or '',
                row[11].strftime('%Y-%m-%d %H:%M:%S') if row[11] else ''
            ])
        
        cursor.close()
        conn.close()
        
        # Preparar respuesta
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=estudiantes_{datetime.now().strftime('%Y%m%d')}.csv"
            }
        )
    except Exception as e:
        print(f"❌ Error exportando CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))
