import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema='public' 
    ORDER BY table_name
""")

print("✅ TABLAS EN PRODUCCIÓN:")
print("=" * 50)
for table in cur.fetchall():
    print(f"  ✓ {table[0]}")

cur.close()
conn.close()
