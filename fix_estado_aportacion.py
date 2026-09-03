import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Transform all stuck "Aprobada" aportaciones to "Activa"
cur.execute("UPDATE aportaciones SET estado = 'Activa' WHERE estado = 'Aprobada'")
conn.commit()

cur.close()
conn.close()
print("Parche aplicado exitosamente.")
