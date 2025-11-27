import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = conn.cursor()

cursor.execute("""
    SELECT column_name, is_nullable, column_default 
    FROM information_schema.columns 
    WHERE table_name = 'documentos' 
    ORDER BY ordinal_position
""")

print("Estructura de la tabla documentos:")
print("-" * 60)
for row in cursor.fetchall():
    nullable = "NULL" if row[1] == "YES" else "NOT NULL"
    default = row[2] if row[2] else "sin default"
    print(f"{row[0]:25} {nullable:10} {default}")

cursor.close()
conn.close()
