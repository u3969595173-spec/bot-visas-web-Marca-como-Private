import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS transferencias_p2p (
        id SERIAL PRIMARY KEY,
        origen_id INT,
        origen_nombre VARCHAR(200),
        receptor_id INT,
        receptor_nombre VARCHAR(200),
        importe DECIMAL(12,2),
        moneda VARCHAR(30),
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

cur.execute("SELECT id, inversor_id, importe, estado, fecha_aprobacion FROM aportaciones WHERE estado IN ('Validada', 'Retenida P2P', 'Activa') ORDER BY id DESC LIMIT 10")
print('Aportaciones:', cur.fetchall())

cur.close()
conn.close()
