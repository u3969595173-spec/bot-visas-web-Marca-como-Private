"""
Migración: Agregar nuevos campos al formulario de estudiantes
- fecha_nacimiento, pais_origen, carrera_deseada
- fondos_disponibles, fecha_inicio_estimada
- archivo_titulo, archivo_pasaporte, archivo_extractos
- consentimiento_gdpr, fecha_consentimiento
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def migrar():
    print("[INFO] Conectando a la base de datos...")
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    try:
        print("[INFO] Agregando nuevas columnas...")
        
        # Agregar columnas una por una para evitar errores si alguna ya existe
        columnas = [
            ("fecha_nacimiento", "DATE"),
            ("pais_origen", "VARCHAR(100)"),
            ("carrera_deseada", "VARCHAR(200)"),
            ("fondos_disponibles", "DECIMAL(10, 2)"),
            ("fecha_inicio_estimada", "DATE"),
            ("archivo_titulo", "TEXT"),
            ("archivo_pasaporte", "TEXT"),
            ("archivo_extractos", "TEXT"),
            ("consentimiento_gdpr", "BOOLEAN DEFAULT FALSE"),
            ("fecha_consentimiento", "TIMESTAMP"),
        ]
        
        for nombre_columna, tipo in columnas:
            try:
                cursor.execute(f"""
                    ALTER TABLE estudiantes 
                    ADD COLUMN IF NOT EXISTS {nombre_columna} {tipo}
                """)
                print(f"[OK] Columna {nombre_columna} agregada")
            except Exception as e:
                print(f"[SKIP] {nombre_columna}: {e}")
        
        conn.commit()
        print("[OK] Migración completada exitosamente")
        
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Error en migración: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrar()
