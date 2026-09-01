import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("SELECT id, nombre, email FROM inversores WHERE nombre ILIKE '%Leandro%'")
    inversores = cur.fetchall()
    print("Perfiles de Leandro en BBDD:")
    for i in inversores:
        print(i)
except Exception as e:
    print(e)
