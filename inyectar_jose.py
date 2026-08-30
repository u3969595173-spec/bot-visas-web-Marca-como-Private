import psycopg2
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("SELECT id, nombre, referido_por FROM inversores WHERE email = 'josectorres05@gmail.com'")
    jose = cur.fetchone()
    if not jose:
        raise Exception("No se encontro a jose")
    jose_id, jose_nombre, referido_por = jose
    print(f"Jose: {jose_id}, {jose_nombre}, referido_por: {referido_por}")

    cur.execute("SELECT id, nombre FROM inversores WHERE nombre ILIKE '%Leandro%' LIMIT 1")
    leandro = cur.fetchone()
    if not leandro:
        raise Exception("No se encontro a Leandro")
    leandro_id, leandro_nombre = leandro
    print(f"Leandro: {leandro_id}, {leandro_nombre}")

    hace_6_dias = datetime.now() - timedelta(days=6)
    importe = 1500.00
    ganancia = 42.00 # 2.8% de 1500
    comision = 150.00 # 10%

    cur.execute("""
        INSERT INTO aportaciones (inversor_id, nombre, email, importe, moneda, estado, created_at, fecha_aprobacion, ganancia_rentabilidad)
        VALUES (%s, %s, %s, %s, 'USDT BEP-20', 'Activa', %s, %s, %s)
        RETURNING id
    """, (jose_id, jose_nombre, 'josectorres05@gmail.com', importe, hace_6_dias, hace_6_dias, ganancia))
    aportacion_id = cur.fetchone()[0]
    print(f"Aportacion {aportacion_id} insertada con exito")

    # Para meterle los 150 USDT a Leandro en su saldo disponible (ya que las comisiones pasan a Saldo Inversiones en CTI o Retirado)
    # Lo mas limpio para sumarle dinero a un usuario en CTI y que lo vea en "Saldo Disponible" es:
    # O crearle una aportacion de ganancia acelerada a Leandro, o una aportacion Activa con ganancia.
    # Dado que es bono de referido, insertamos en aportaciones (o ganancias_referidos).
    # OJO, Capital Iberia suma en `userAportaciones` todas las aportaciones "Activas", PERO el Capital Inicial se asume bloqueado.
    # En el Frontend (DashboardInversionista):
    # saldo.disponible = (Capital + ganancias + acelerada) - retirado
    # Así que podemos inyectar esto como una ganancia acelerada a alguna aportacion activa de Leandro. O en ganancia_rentabilidad de alguna aportacion de el.
    # O mejor sumarselo a Leandro como una notificacion y registrar en "ganancias_referidos" si la tabla existe.

    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    tables = [t[0] for t in cur.fetchall()]
    
    if 'ganancias_referidos' in tables:
        cur.execute("""
            INSERT INTO ganancias_referidos (inversor_id, referido_id, referido_nombre, importe_inversion, comision_ganada, moneda, nivel, created_at)
            VALUES (%s, %s, %s, %s, %s, 'USDT BEP-20', 1, CURRENT_TIMESTAMP)
        """, (leandro_id, jose_id, jose_nombre, importe, comision))
        print("Comision insertada en ganancias_referidos.")

    # Sumamos la ganancia acelerada o comision directo a la BBDD de Leandro
    cur.execute("SELECT id FROM aportaciones WHERE inversor_id = %s LIMIT 1", (leandro_id,))
    l_aport = cur.fetchone()
    if l_aport:
        cur.execute("UPDATE aportaciones SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + %s WHERE id = %s", (comision, l_aport[0]))
        print(f"Sumados 150 USDT al saldo de Leandro en su contrato {l_aport[0]}")
    else:
        # Si leandro no tiene aportacion, le creamos una ficticia vacia para meterle el bono
        cur.execute("""
            INSERT INTO aportaciones (inversor_id, nombre, email, importe, moneda, estado, ganancia_acelerada, fecha_aprobacion)
            VALUES (%s, %s, %s, 0, 'USDT BEP-20', 'Activa', %s, CURRENT_TIMESTAMP)
        """, (leandro_id, leandro_nombre, 'leandro@test', comision))
        print("Bono inyectado como un contrato base vacio para Leandro")

    conn.commit()
    print("TODO COMPLETADO PERFECTO")
except Exception as e:
    import traceback
    print("HUBO ERROR:", str(e))
    traceback.print_exc()
finally:
    cur.close()
    conn.close()
