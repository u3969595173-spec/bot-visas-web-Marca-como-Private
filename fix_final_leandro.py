import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# 1. Sumar 45.90 al Contrato 4 de Leandro 16
cur.execute("""
    UPDATE aportaciones 
    SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + 45.90
    WHERE id = 4
""")

# 2. Corregir el 459 P2P de Leandro a Alejandro para que coincida en su balance (pasa de EUR a USDT)
cur.execute("""
    UPDATE retiros
    SET moneda = 'USDT'
    WHERE inversor_id = '16' AND importe = 459
""")

# 3. Y aprovechando, el voucher en transferencias_p2p para trazabilidad
cur.execute("""
    UPDATE transferencias_p2p
    SET moneda = 'USDT'
    WHERE origen_id = 16 AND importe = 459
""")

conn.commit()
print("¡Limpieza Perfecta Ejecutada!")

cur.close()
conn.close()
