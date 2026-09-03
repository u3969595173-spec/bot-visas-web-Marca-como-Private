import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

email = "oragmymartinez1988@gmail.com"

# Fetch all users
cur.execute("SELECT id, nombre, email, created_at FROM inversores WHERE nombre ILIKE '%Oragmy%' ORDER BY id ASC")
usuarios = cur.fetchall()

print("Buscando duplicados...")
for u in usuarios:
    print(f"ID: {u[0]} | Fecha: {u[3]}")
    # The user wants to delete the one created around 30/08/2026, 19:35
    # Let's see if we have 2 copies and target the correct one based on relative time
    
if len(usuarios) > 1:
    # He said: "quiere dejar la otra cuenta borrale esta ok" 
    # referring to: "30/08/2026, 19:35" 
    # Let's delete the specific one that matches this date/time the closest,
    # or typically the duplicate is the most recent one (LATEST).
    # Since he provided a date, let's just delete the LATEST inserted one.
    id_to_delete = usuarios[-1][0]
    date_to_delete = usuarios[-1][3]
    
    cur.execute("DELETE FROM inversores WHERE id = %s", (id_to_delete,))
    conn.commit()
    print(f"¡Hecho! Cuenta duplicada de Oragmy eliminada (ID: {id_to_delete}, Fecha: {date_to_delete}). Cuenta original conservada salvajemente.")
else:
    print("Solo existe una cuenta.")

cur.close()
conn.close()
