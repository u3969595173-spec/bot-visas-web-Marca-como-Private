import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE notificaciones ADD COLUMN IF NOT EXISTS es_para_admin BOOLEAN DEFAULT FALSE;")
    conn.commit()
    print("Columna 'es_para_admin' anadida con exito a notificaciones.")
except Exception as e:
    print("Error:", str(e))
    conn.rollback()

try:
    cur.execute("ALTER TABLE notificaciones ADD COLUMN IF NOT EXISTS tipo VARCHAR(50) DEFAULT 'SISTEMA';")
    conn.commit()
    print("Columna 'tipo' anadida con exito a notificaciones.")
except Exception as e:
    pass

cur.close()
conn.close()
