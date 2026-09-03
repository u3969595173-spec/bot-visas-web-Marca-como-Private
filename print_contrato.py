import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

cur.execute("SELECT id, inversor_id, importe, ganancia_acelerada, moneda FROM aportaciones WHERE id = 4")
a = cur.fetchall()

with open('output.txt', 'w') as f:
    f.write("CONTRATO MAESTRO LEANDRO:\n")
    for x in a:
        f.write(f"[{x[0]}] Inversor: {x[1]} | Importe: {x[2]} {x[4]} | Bono: {x[3]} USDT\n")

cur.close()
conn.close()
