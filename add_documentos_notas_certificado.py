"""
Migración: Agregar columnas para documentos adicionales
- archivo_notas (notas académicas)
- archivo_certificado_medico
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
        print("[INFO] Agregando columnas para documentos adicionales...")
        
        # Agregar archivo_notas
        try:
            cursor.execute("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS archivo_notas TEXT;
            """)
            print("✅ Columna archivo_notas agregada")
        except Exception as e:
            print(f"⚠️  archivo_notas: {e}")
        
        # Agregar archivo_certificado_medico
        try:
            cursor.execute("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS archivo_certificado_medico TEXT;
            """)
            print("✅ Columna archivo_certificado_medico agregada")
        except Exception as e:
            print(f"⚠️  archivo_certificado_medico: {e}")
        
        conn.commit()
        print("\n✅ MIGRACIÓN COMPLETADA")
        print("\nDocumentos disponibles ahora:")
        print("1. archivo_titulo (Título Universitario)")
        print("2. archivo_pasaporte (Pasaporte)")
        print("3. archivo_notas (Notas Académicas)")
        print("4. archivo_certificado_medico (Certificado Médico)")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrar()
