import psycopg2
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    print("Iniciando prueba de insercion en inversores...")
    email = "testfake_334@correo.com"
    password_hash = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cur.execute("""
        INSERT INTO inversores (nombre, email, telefono, pais, password_hash, referido_por, estado)
        VALUES ('Prueba Fake', %s, '12345678', 'España', %s, NULL, 'validada')
        RETURNING id
    """, (email, password_hash))
    inversor_id = cur.fetchone()[0]
    print(f"Inversor insertado con ID: {inversor_id}")

    codigo_propio = f"PRU{inversor_id}99"
    cur.execute("UPDATE inversores SET codigo_referido = %s WHERE id = %s", (codigo_propio, inversor_id))
    print(f"Codigo referido actualizado a {codigo_propio}")

    cur.execute("""
        INSERT INTO notificaciones (es_para_admin, mensaje, tipo) 
        VALUES (TRUE, 'Nuevo usuario registrado: Prueba Fake', 'SISTEMA')
    """)
    print("Notificacion a admin insertada")

    conn.commit()
    print("Registro simulado COMPLETAMENTE EXACTO al API con EXITO")
    
    # Limpiamos
    cur.execute("DELETE FROM inversores WHERE id = %s", (inversor_id,))
    cur.execute("DELETE FROM notificaciones WHERE mensaje LIKE 'Nuevo usuario registrado: Prueba Fake'")
    conn.commit()
    print("Basura limpia.")

except Exception as e:
    import traceback
    print("💥 EL ERROR ES:", str(e))
    traceback.print_exc()
    conn.rollback()
finally:
    cur.close()
    conn.close()
