import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

email = "oragmymartinez1988@gmail.com"

# Check if there are multiple users with similar names or emails
cur.execute("SELECT id, nombre, email, created_at FROM inversores WHERE email = %s OR nombre ILIKE '%Oragmy%'", (email,))
usuarios = cur.fetchall()

print("Usuarios encontrados:")
for u in usuarios:
    # check if they have any aportaciones
    cur.execute("SELECT count(*) FROM aportaciones WHERE inversor_id = %s", (u[0],))
    aport = cur.fetchone()[0]
    
    cur.execute("SELECT count(*) FROM retiros WHERE inversor_id = %s", (u[0],))
    retiros = cur.fetchone()[0]
    
    print(f"ID: {u[0]} | Nombre: {u[1]} | Email: {u[2]} | Creado: {u[3]} | Aportaciones: {aport} | Retiros: {retiros}")

cur.close()
conn.close()
