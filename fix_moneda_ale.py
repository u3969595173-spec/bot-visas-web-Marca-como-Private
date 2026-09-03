import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Actualizar divisa a USDT
cur.execute("""
    UPDATE aportaciones 
    SET moneda = 'USDT' 
    WHERE nombre ILIKE '%Ale%' AND importe = 741
""")
conn.commit()

print(f"[{cur.rowcount}] contrato(s) corregidos a USDT exitosamente.")

cur.close()
conn.close()
