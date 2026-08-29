import sys
from dotenv import dotenv_values
import psycopg2

config = dotenv_values('C:/BotVisasEstudio/.env')
db_url = config.get('DATABASE_URL')
if not db_url:
    print("No DATABASE_URL found in .env")
    sys.exit(1)

conn = psycopg2.connect(db_url)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [r[0] for r in cur.fetchall()]
print("Tables in public schema:")
print(tables)

for table in ['inversores', 'referidos', 'aportaciones', 'retiros']:
    if table in tables:
        cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table}'")
        cols = cur.fetchall()
        print(f"\nColumns in '{table}':")
        for col, dtype in cols:
            print(f"  {col} ({dtype})")
    else:
        print(f"\nTable '{table}' not found in public tables.")

cur.close()
conn.close()
