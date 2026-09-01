import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("SELECT id, nombre, email, codigo_referido FROM inversores WHERE nombre ILIKE '%Leandro%'")
    rows = cur.fetchall()
    print("::: LISTA DE LEANDROS :::")
    for r in rows:
        print(f"ID {r[0]} | Nombre: {r[1]} | Email: {r[2]} | Codigo: {r[3]}")
except Exception as e:
    print(e)
