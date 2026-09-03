import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

cur.execute("SELECT id FROM inversores WHERE nombre ILIKE '%Leandro%' LIMIT 1")
row = cur.fetchone()
if row:
    leandro_id = row[0]
    cur.execute("SELECT id, importe, ganancia_acelerada, estado FROM aportaciones WHERE inversor_id = %s", (leandro_id,))
    aportaciones = cur.fetchall()
    
    print(f"Leandro ID: {leandro_id}")
    for a in aportaciones:
        print(f"Aport ID: {a[0]} | Importe: {a[1]} | Bono: {a[2]} | Estado: {a[3]}")
else:
    print("Leandro no encontrado")

cur.close()
conn.close()
