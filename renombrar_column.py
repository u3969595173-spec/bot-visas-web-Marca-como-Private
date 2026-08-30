import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE notificaciones RENAME COLUMN estudiante_id TO inversor_id;")
    conn.commit()
    print("Columna renombrada exitosamente: estudiante_id -> inversor_id.")
except Exception as e:
    conn.rollback()
    print("Error al renombrar (quizas ya fue renombrada):", str(e))

cur.close()
conn.close()
