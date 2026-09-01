import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("SELECT id, nombre, codigo_referido FROM inversores WHERE nombre ILIKE '%Leandro%' OR nombre ILIKE '%Leandro Eloy%'")
    print("LEANDROS:", cur.fetchall())

    cur.execute("SELECT id, nombre, referido_por FROM inversores WHERE id = 74 OR nombre ILIKE '%gabriel%'")
    print("GABRIEL:", cur.fetchall())
except Exception as e:
    print(e)
