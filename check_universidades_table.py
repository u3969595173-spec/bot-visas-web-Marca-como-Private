import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = conn.cursor()

# Verificar si existe la tabla
cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'universidades_espana'
    )
""")
exists = cursor.fetchone()[0]

if exists:
    print("✅ Tabla universidades_espana existe")
    
    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM universidades_espana")
    count = cursor.fetchone()[0]
    print(f"📊 Total universidades: {count}")
    
    # Mostrar primeras 5
    cursor.execute("SELECT id, nombre, ciudad, tipo FROM universidades_espana LIMIT 5")
    print("\n🏫 Primeras 5 universidades:")
    for row in cursor.fetchall():
        print(f"  {row[0]:3} | {row[1]:40} | {row[2]:15} | {row[3]}")
else:
    print("❌ La tabla universidades_espana NO existe")
    
    # Ver qué tablas existen relacionadas
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name LIKE '%univ%' 
        ORDER BY table_name
    """)
    print("\n📋 Tablas relacionadas con 'univ':")
    for row in cursor.fetchall():
        print(f"  - {row[0]}")

cursor.close()
conn.close()
