import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE notificaciones ALTER COLUMN estudiante_id DROP NOT NULL;")
    conn.commit()
    print("El candado NOT NULL sobre estudiante_id ha sido aniquilado con exito.")
except Exception as e:
    print("Error:", str(e))
    conn.rollback()

cur.close()
conn.close()
