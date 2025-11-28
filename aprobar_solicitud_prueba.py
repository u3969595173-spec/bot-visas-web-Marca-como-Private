"""
Script para aprobar manualmente una solicitud y probar el sistema
"""

import os
import psycopg2
from urllib.parse import urlparse

def aprobar_solicitud_manualmente():
    """Aprueba manualmente una solicitud para probar el sistema"""
    
    try:
        # Conectar a la base de datos
        db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/bot_visas')
        
        if 'postgres://' in db_url:
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(db_url, sslmode='require' if 'localhost' not in db_url else 'disable')
        cursor = conn.cursor()
        
        print("🧪 APROBANDO SOLICITUD MANUALMENTE PARA PRUEBA")
        print("=" * 50)
        
        # Aprobar solicitud de patrocinio del estudiante 4
        print("1. Aprobando solicitud de patrocinio del estudiante 4...")
        cursor.execute("""
            UPDATE estudiantes 
            SET estado_patrocinio = 'aprobado',
                comentarios_patrocinio = 'Solicitud aprobada manualmente para pruebas del sistema de notificaciones.'
            WHERE id = 4 AND patrocinio_solicitado = true
        """)
        
        # Aprobar solicitud de alojamiento del estudiante 4 (si existe)
        print("2. Aprobando solicitud de alojamiento del estudiante 4...")
        cursor.execute("""
            UPDATE estudiantes 
            SET estado_alojamiento = 'aprobado',
                comentarios_alojamiento = 'Solicitud aprobada manualmente para pruebas del sistema de notificaciones.'
            WHERE id = 4 AND gestion_alojamiento_solicitada = true
        """)
        
        # Aprobar solicitud de seguro médico del estudiante 4 (si existe)
        print("3. Aprobando solicitud de seguro médico del estudiante 4...")
        cursor.execute("""
            UPDATE estudiantes 
            SET estado_seguro_medico = 'aprobado',
                comentarios_seguro_medico = 'Solicitud aprobada manualmente para pruebas del sistema de notificaciones.'
            WHERE id = 4 AND gestion_seguro_solicitada = true
        """)
        
        conn.commit()
        
        # Verificar los cambios
        cursor.execute("""
            SELECT nombre, estado_patrocinio, estado_alojamiento, estado_seguro_medico
            FROM estudiantes 
            WHERE id = 4
        """)
        
        resultado = cursor.fetchone()
        if resultado:
            print(f"\n✅ SOLICITUDES APROBADAS PARA: {resultado[0]}")
            print(f"   💰 Patrocinio: {resultado[1] or 'N/A'}")
            print(f"   🏠 Alojamiento: {resultado[2] or 'N/A'}")
            print(f"   🏥 Seguro: {resultado[3] or 'N/A'}")
            
            print(f"\n🎯 AHORA PRUEBA:")
            print(f"   1. Ve al panel del estudiante ID 4")
            print(f"   2. Ve a las secciones de Información Financiera, Alojamiento y Seguro Médico")
            print(f"   3. Deberías ver los estados APROBADO en lugar del formulario")
            print(f"   4. También deberías ver los comentarios del admin")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ COMPLETADO - Recarga las páginas del estudiante para ver los cambios")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    aprobar_solicitud_manualmente()