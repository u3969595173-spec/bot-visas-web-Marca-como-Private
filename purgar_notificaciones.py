import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

columnas_a_relajar = ['titulo', 'icono', 'link', 'es_emergencia', 'usuario_id', 'estudiante_id']

for col in columnas_a_relajar:
    try:
        cur.execute(f"ALTER TABLE notificaciones ALTER COLUMN {col} DROP NOT NULL;")
        conn.commit()
        print(f"Candado NOT NULL de la columna '{col}' aniquilado con exito.")
    except Exception as e:
        conn.rollback()
        print(f"La columna '{col}' no requirio alteracion o no existe: {e}")

cur.close()
conn.close()
