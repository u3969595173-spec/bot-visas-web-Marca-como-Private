import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Normalizar estado P2P en el historial
cur.execute("UPDATE retiros SET estado = 'Aprobado' WHERE estado = 'Completada'")
conn.commit()

cur.close()
conn.close()
print("Base de datos P2P normalizada correctamente.")
