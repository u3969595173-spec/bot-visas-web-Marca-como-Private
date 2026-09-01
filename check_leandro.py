import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("SELECT id, nombre, importe, ganancia_acelerada FROM aportaciones WHERE nombre ILIKE '%Leandro%'")
    rows = cur.fetchall()
    print("Aportaciones exactas de Leandro:")
    for r in rows:
        print(r)
except Exception as e:
    print(e)
