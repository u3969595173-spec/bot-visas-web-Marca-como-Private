import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("SELECT id, nombre, importe, moneda, estado, ganancia_acelerada, ganancia_rentabilidad FROM aportaciones WHERE nombre ILIKE '%Leandro%'")
    aportaciones = cur.fetchall()
    print("Aportaciones de Leandro:")
    for a in aportaciones:
        print(a)
except Exception as e:
    print("ERROR:", e)

cur.close()
conn.close()
