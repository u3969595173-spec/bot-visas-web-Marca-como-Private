import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Leandro ID es 5 por lo visto en logs anteriores, pero confirmemos
cur.execute("SELECT id FROM inversores WHERE nombre ILIKE '%Leandro%' LIMIT 1")
leandro_id = cur.fetchone()[0]

cur.execute("""
    SELECT id, importe, ganancia_acelerada 
    FROM aportaciones 
    WHERE inversor_id = %s AND (estado = 'Activa' OR estado = 'Validada')
    ORDER BY created_at DESC LIMIT 1
""", (leandro_id,))
aport = cur.fetchone()

if aport:
    aport_id = aport[0]
    # Sumamos forzosamente 45.9 (10% de 459) al contrato activo más reciente
    cur.execute("""
        UPDATE aportaciones 
        SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + 45.90
        WHERE id = %s
    """, (aport_id,))
    conn.commit()
    print(f"ÉXITO: Se sumaron +45.90 USDT al contrato {aport_id} de Leandro.")
else:
    print("ERROR: Leandro no tiene contratos Activos para recibir el Bono.")

cur.close()
conn.close()
