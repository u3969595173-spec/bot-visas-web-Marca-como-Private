import psycopg2
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    # 1. Encontrar a Gabriel
    cur.execute("SELECT id, nombre, email FROM inversores WHERE id = 74")
    gabriel = cur.fetchone()
    if not gabriel:
        raise Exception("No se encontro a Gabriel Perez")
    
    gabriel_id, gabriel_nombre, gabriel_email = gabriel
    print(f"Gabriel encontrado: ID {gabriel_id}, Nombre: {gabriel_nombre}")

    # 2. Encontrar a Leandro 
    cur.execute("SELECT id, nombre, codigo_referido FROM inversores WHERE nombre ILIKE '%Leandro%' LIMIT 1")
    leandro = cur.fetchone()
    if not leandro:
        raise Exception("No se encontro a Leandro")
    leandro_id, leandro_nombre, leandro_codigo = leandro
    print(f"Leandro encontrado: ID {leandro_id}, Nombre: {leandro_nombre}, Codigo: {leandro_codigo}")

    # Forzar a Leandro como patrocinador de Gabriel
    cur.execute("UPDATE inversores SET referido_por = %s WHERE id = %s", (leandro_codigo, gabriel_id))

    # 3. Calcular la ganancia usando un 1.15% (promedio de hoy)
    porcentaje = 1.15
    importe = 25.00
    ganancia = importe * (porcentaje / 100.0) # Ganancia de 1 dia (hoy)
    comision_leandro = importe * 0.10 # 10% de 25 = 2.5 USDT
    moneda = 'USDT BEP-20'

    hace_4_dias = datetime.now() - timedelta(days=4)

    # 4. Inyectar Aportacion Activa para Gabriel
    cur.execute("""
        INSERT INTO aportaciones (inversor_id, nombre, email, importe, moneda, estado, created_at, fecha_aprobacion, ganancia_rentabilidad)
        VALUES (%s, %s, %s, %s, %s, 'Activa', %s, %s, %s)
    """, (gabriel_id, gabriel_nombre, gabriel_email, importe, moneda, hace_4_dias, hace_4_dias, ganancia))
    print(f"Aportacion inyectada a Gabriel: {importe} USDT con ganancia {ganancia} (Porcentaje: {porcentaje}%)")

    # 5. Inyectar comision de referido a Leandro
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    tables = [t[0] for t in cur.fetchall()]
    
    if 'ganancias_referidos' in tables:
        cur.execute("""
            INSERT INTO ganancias_referidos (inversor_id, referido_id, referido_nombre, importe_inversion, comision_ganada, moneda, nivel, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, 1, CURRENT_TIMESTAMP)
        """, (leandro_id, gabriel_id, gabriel_nombre, importe, comision_leandro, moneda))
        print("Comision registrada en ganancias_referidos para Leandro.")

    # Sumar la ganancia acelerada a Leandro en su saldo
    cur.execute("SELECT id FROM aportaciones WHERE inversor_id = %s LIMIT 1", (leandro_id,))
    l_aport = cur.fetchone()
    if l_aport:
        cur.execute("UPDATE aportaciones SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + %s WHERE id = %s", (comision_leandro, l_aport[0]))
        print(f"Sumados {comision_leandro} USDT al saldo de Leandro via contrato {l_aport[0]}")
    else:
        cur.execute("""
            INSERT INTO aportaciones (inversor_id, nombre, email, importe, moneda, estado, ganancia_acelerada, fecha_aprobacion)
            VALUES (%s, %s, %s, 0, %s, 'Activa', %s, CURRENT_TIMESTAMP)
        """, (leandro_id, leandro_nombre, 'leandro@test', moneda, comision_leandro))
        print("Bono inyectado como un contrato base vacio para Leandro.")

    conn.commit()
    print("TRANSACCION CUANTICA COMPLETADA EXITOSAMENTE")

except Exception as e:
    print("ERROR:", str(e))
    conn.rollback()
finally:
    cur.close()
    conn.close()
