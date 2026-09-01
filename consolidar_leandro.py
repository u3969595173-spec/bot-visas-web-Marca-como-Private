import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("SELECT id, ganancia_acelerada FROM aportaciones WHERE nombre ILIKE '%Leandro%' AND importe < 1")
    aportaciones_fantasma = cur.fetchall()
    
    if len(aportaciones_fantasma) > 1:
        # Sumamos todo
        total_bonos = sum(a[1] for a in aportaciones_fantasma if a[1])
        id_principal = aportaciones_fantasma[0][0]
        
        # Actualizamos el primero
        cur.execute("UPDATE aportaciones SET ganancia_acelerada = %s, nombre = 'Leandro Eloy (Fondo Referidos)' WHERE id = %s", (total_bonos, id_principal))
        
        # Borramos los demas
        ids_borrar = [a[0] for a in aportaciones_fantasma[1:]]
        cur.execute("DELETE FROM aportaciones WHERE id = ANY(%s)", (ids_borrar,))
        
        conn.commit()
        print(f"Fusion completa. Fondo de consolidados = {total_bonos} USDT en ID {id_principal}. Borradas: {ids_borrar}")
    else:
        print("No hay multiples aportaciones para fusionar.")

except Exception as e:
    import traceback
    traceback.print_exc()
    conn.rollback()

cur.close()
conn.close()
