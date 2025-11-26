"""
Script para ejecutar la migración: agregar columna fondos_disponibles
"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL no encontrada en .env")
    exit(1)

print("[INFO] Conectando a la base de datos...")

try:
    # Conectar a PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("[INFO] Ejecutando migración: add_fondos_disponibles_column.sql")
    
    # Leer y ejecutar el archivo SQL
    with open('database/migrations/add_fondos_disponibles_column.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
        cursor.execute(sql)
    
    # Commit cambios
    conn.commit()
    
    print("[OK] Migración ejecutada exitosamente")
    print("[OK] Columna 'fondos_disponibles' agregada a tabla 'estudiantes'")
    
    # Verificar que la columna existe
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'estudiantes' AND column_name = 'fondos_disponibles';
    """)
    
    result = cursor.fetchone()
    if result:
        print(f"[OK] Verificación exitosa: {result[0]} ({result[1]})")
    else:
        print("[WARN] No se pudo verificar la columna")
    
    cursor.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"[ERROR] Error de base de datos: {e}")
    exit(1)
except FileNotFoundError:
    print("[ERROR] Archivo de migración no encontrado")
    exit(1)
except Exception as e:
    print(f"[ERROR] Error inesperado: {e}")
    exit(1)
