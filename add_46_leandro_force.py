import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

cur.execute("SELECT id FROM inversores WHERE nombre ILIKE '%Leandro%' LIMIT 1")
leandro_id = cur.fetchone()[0]

cur.execute("""
    SELECT id, importe, ganancia_acelerada, estado 
    FROM aportaciones 
    WHERE inversor_id = %s
    ORDER BY created_at DESC
""", (leandro_id,))
aports = cur.fetchall()

for a in aports:
    print(f"ID: {a[0]} | Importe: {a[1]} | Estado: {a[3]}")
    # Force injection on the 9000 USDT one
    if float(a[1] or 0) == 9000:
        cur.execute("""
            UPDATE aportaciones 
            SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + 45.90
            WHERE id = %s
        """, (a[0],))
        conn.commit()
        print(f"Bono de 45.9 inyectado forzosamente en el contrato (ID {a[0]} de 9000 USDT) estado: {a[3]}")

cur.close()
conn.close()
