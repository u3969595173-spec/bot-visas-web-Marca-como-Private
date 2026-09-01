import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    # Restar 152.50 a la ganancia_acelerada de la aportacion real de Leandro
    cur.execute("UPDATE aportaciones SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) - 152.50 WHERE nombre ILIKE '%Leandro%' AND email != 'leandro@test' AND ganancia_acelerada >= 152.50")
    if cur.rowcount > 0:
        print("Correccion: -152.50 extraidos exitosamente de ganancia_acelerada para corregir la doble contabilidad.")
    else:
        # Por si ya lo restamos o no tenia suficiente
        print("No se encontraron 152.50 en la ganancia_acelerada. Reajustando a 0 para forzar limpieza...")
        cur.execute("UPDATE aportaciones SET ganancia_acelerada = 0 WHERE nombre ILIKE '%Leandro%' AND email != 'leandro@test'")
        print("ganancia_acelerada forzada a 0.")
    
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()

cur.close()
conn.close()
