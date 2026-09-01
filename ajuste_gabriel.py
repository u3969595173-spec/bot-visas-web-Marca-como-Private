import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    # Ajustar ganancia de Gabriel (ID 74) a exactamente 1.2% de 25 USDT = 0.30
    cur.execute("UPDATE aportaciones SET ganancia_rentabilidad = 0.30 WHERE inversor_id = 74")
    conn.commit()
    print("Correccion hecha.")
except Exception as e:
    print(e)

cur.close()
conn.close()
