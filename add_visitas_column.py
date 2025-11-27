import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = conn.cursor()

try:
    # Agregar columna visitas
    print("Agregando columna 'visitas' a universidades_espana...")
    cursor.execute("""
        ALTER TABLE universidades_espana 
        ADD COLUMN IF NOT EXISTS visitas INTEGER DEFAULT 0
    """)
    
    conn.commit()
    print("✅ Columna 'visitas' agregada correctamente")
    
    # Verificar
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'universidades_espana' AND column_name = 'visitas'
    """)
    
    if cursor.fetchone():
        print("✅ Columna verificada - existe en la tabla")
    else:
        print("❌ Error - columna no encontrada")
        
except Exception as e:
    conn.rollback()
    print(f"❌ Error: {e}")
finally:
    cursor.close()
    conn.close()
