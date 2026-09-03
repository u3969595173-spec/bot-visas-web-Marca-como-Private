import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

cur.execute("SELECT id, importe, ganancia_acelerada, moneda FROM aportaciones WHERE inversor_id = 6")
a = cur.fetchall()
print("ESTADO PURO BBDD LEANDRO:")
for x in a:
    print(f"[{x[0]}] Importe: {x[1]} {x[3]} | Bono Total Asignado: {x[2]} USDT")

cur.close()
conn.close()
