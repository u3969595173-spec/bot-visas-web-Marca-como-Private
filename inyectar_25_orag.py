import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

email_target = 'oragmymartinez1988@gmail.com'

# 1. Localizar al usuario
cur.execute("SELECT id, nombre FROM inversores WHERE email = %s LIMIT 1", (email_target,))
inversor = cur.fetchone()

if not inversor:
    print(f"Error: No se encontro ninguna cuenta con el email {email_target}")
else:
    inversor_id, nombre = inversor
    
    # 2. Inyectar los 25 USDT
    cur.execute("""
        INSERT INTO aportaciones (inversor_id, nombre, email, importe, moneda, estado, fecha_aprobacion)
        VALUES (%s, %s, %s, %s, 'USDT', 'Activa', CURRENT_TIMESTAMP)
        RETURNING id
    """, (inversor_id, nombre, email_target, 25.00))
    
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    print(f"¡EXITO! Aportacion (Contrato #{nuevo_id}) de 25 USDT inyectada a la cuenta de {nombre}.")
    print("El sistema iniciara automaticamente el periodo de 72 horas de bloqueo desde este mismo momento.")

cur.close()
conn.close()
