import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()
cur.execute("UPDATE aportaciones SET estado = 'Validada', fecha_aprobacion = created_at WHERE estado = 'Retenida P2P'")
print(f'Rows updated: {cur.rowcount}')
conn.commit()
cur.close()
conn.close()
