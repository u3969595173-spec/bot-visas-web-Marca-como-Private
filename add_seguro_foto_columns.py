"""
Migración: Agregar columnas para seguro médico y foto
- archivo_seguro_medico
- archivo_foto_pasaporte
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def migrar():
    print("[INFO] Conectando a la base de datos...")
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("[ERROR] No se encontró DATABASE_URL en las variables de entorno")
        return
    
    conn = psycopg2.connect(database_url, sslmode='require')
    cursor = conn.cursor()
    
    try:
        print("[INFO] Agregando columnas para seguro médico y foto...")
        
        # Agregar archivo_seguro_medico
        try:
            cursor.execute("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS archivo_seguro_medico TEXT;
            """)
            print("✅ Columna archivo_seguro_medico agregada")
        except Exception as e:
            print(f"⚠️  archivo_seguro_medico: {e}")
        
        # Agregar archivo_foto_pasaporte
        try:
            cursor.execute("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS archivo_foto_pasaporte TEXT;
            """)
            print("✅ Columna archivo_foto_pasaporte agregada")
        except Exception as e:
            print(f"⚠️  archivo_foto_pasaporte: {e}")
        
        conn.commit()
        print("\n✅ MIGRACIÓN COMPLETADA")
        print("\nDocumentos que debe subir el estudiante:")
        print("1. Pasaporte")
        print("2. Título Universitario")
        print("3. Notas Académicas")
        print("4. Certificado Médico")
        print("5. Extractos Bancarios")
        print("6. Seguro Médico Internacional")
        print("7. Foto tipo Pasaporte")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrar()
