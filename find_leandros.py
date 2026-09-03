import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

cur.execute("SELECT id, nombre, email, codigo_referido FROM inversores WHERE nombre ILIKE '%Lean%'")
leandros = cur.fetchall()

with open('output_leandros.txt', 'w') as f:
    for l in leandros:
        lid = l[0]
        f.write(f"\n--- INVERSOR: {lid} {l[1]} ({l[3]}) ---\n")
        cur.execute("SELECT id, importe, ganancia_acelerada, estado, moneda FROM aportaciones WHERE inversor_id = %s", (str(lid),))
        for a in cur.fetchall():
            f.write(f"  Contrato {a[0]} | Importe: {a[1]} | Bono: {a[2]} | Estado: {a[3]} | Moneda: {a[4]}\n")

cur.close()
conn.close()
