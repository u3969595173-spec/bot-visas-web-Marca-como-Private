import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = conn.cursor()

cursor.execute("""
    SELECT column_name, data_type, is_nullable 
    FROM information_schema.columns 
    WHERE table_name = 'cursos' 
    ORDER BY ordinal_position
""")

print("Columnas en tabla cursos:")
print("-" * 60)
for row in cursor.fetchall():
    print(f"{row[0]:30} {row[1]:20} {'NULL' if row[2] == 'YES' else 'NOT NULL'}")

cursor.close()
conn.close()
