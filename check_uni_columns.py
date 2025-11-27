import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = conn.cursor()

cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'universidades_espana' 
    ORDER BY ordinal_position
""")

print("Columnas en universidades_espana:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

cursor.close()
conn.close()
