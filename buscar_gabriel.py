import psycopg2
import os
from dotenv import load_dotenv
load_dotenv('.env')
conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cur = conn.cursor()
cur.execute("SELECT id, nombre, email FROM inversores ORDER BY id DESC LIMIT 10")
print('Ultimos 10 registrados:', cur.fetchall())
cur.execute("SELECT id, nombre FROM inversores WHERE nombre ILIKE '%gabriel%'")
print('Resultados gabriel:', cur.fetchall())
