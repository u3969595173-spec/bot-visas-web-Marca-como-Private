import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Get Leandro exactly by email from logs (u3969595173@gmail.com)
cur.execute("SELECT id FROM inversores WHERE email = 'u3969595173@gmail.com' LIMIT 1")
l_id = cur.fetchone()
if not l_id:
    print("No existe u3969595173@gmail.com")
else:
    l_id = l_id[0]
    print(f"Leandro: ID {l_id}")
    cur.execute("SELECT id, importe, ganancia_acelerada, estado FROM aportaciones WHERE inversor_id = %s", (str(l_id),))
    aport = cur.fetchall()
    print("Aportaciones API RAW DB:")
    for a in aport:
        print(a)
    
    if aport:
        # Fórce a 120 por si acaso
        cur.execute("UPDATE aportaciones SET ganancia_acelerada = 120 WHERE id = %s", (aport[0][0],))
        conn.commit()
        print("Seteado forzosamente a 120.")

cur.close()
conn.close()
