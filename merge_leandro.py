import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    # 1. Obtener los bonos del contrato fantasma (ID 16 u otros de leandro@test)
    cur.execute("SELECT id, ganancia_acelerada FROM aportaciones WHERE email = 'leandro@test'")
    fantasmas = cur.fetchall()
    
    total_transferir = 0
    ids_borrar = []
    for f in fantasmas:
        print(f"Borrando contrato fantasma {f[0]} con {f[1]} de bonos")
        total_transferir += f[1] if f[1] else 0
        ids_borrar.append(f[0])

    if ids_borrar:
        # Encontramos la aportacion real de Leandro Tamayo. Asumiendo que es su aportación más antigua (ID más bajo)
        cur.execute("SELECT id FROM aportaciones WHERE nombre ILIKE '%Leandro%' AND email != 'leandro@test' ORDER BY id ASC LIMIT 1")
        real = cur.fetchone()
        if real:
            id_real = real[0]
            # Transferimos
            cur.execute("UPDATE aportaciones SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + %s WHERE id = %s", (total_transferir, id_real))
            print(f"Transferidos {total_transferir} USDT al contrato real de Leandro (ID {id_real})")
            
            # Borramos las fantasmas
            cur.execute("DELETE FROM aportaciones WHERE id = ANY(%s)", (ids_borrar,))
            print(f"Contratos fantasmas eliminados: {ids_borrar}")
            
            conn.commit()
            print("LIMPIEZA DE BBDD COMPLETADA")
        else:
            print("No se encontro un contrato REAL de leandro para depositarle esto.")
    else:
        print("No hay contratos fantasmas que transferir.")

except Exception as e:
    import traceback
    traceback.print_exc()
    conn.rollback()

cur.close()
conn.close()
