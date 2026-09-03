import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

print("Buscando aportaciones de Leandro (ID: 6)...")
cur.execute("SELECT id, importe, ganancia_acelerada, estado FROM aportaciones WHERE inversor_id = 6")
aportaciones = cur.fetchall()
for a in aportaciones:
    print(a)
    if a[1] == 9000:
        cur.execute("UPDATE aportaciones SET ganancia_acelerada = 120.00 WHERE id = %s", (a[0],))
        print("Seteado forzosamente a 120.00 (74.1 base + 45.9 bono P2P)")

conn.commit()
cur.close()
conn.close()
print("Operacion completada")
