import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

print("--- REPARACION ALEJANDRO (MONEDA) ---")
cur.execute("SELECT id, nombre, email, moneda, importe FROM aportaciones WHERE nombre ILIKE '%Alej%' OR email ILIKE '%alej%'")
alejandros = cur.fetchall()
for a in alejandros:
    print(f"Aport: {a[0]} | N: {a[1]} | E: {a[2]} | M: {a[3]} | $: {a[4]}")
    cur.execute("UPDATE aportaciones SET moneda = 'USDT' WHERE id = %s", (a[0],))
print(f"[*] {len(alejandros)} contratos de Alejandro forzados absolutamente a USDT.")

print("\n--- REPARACION LEANDRO (BONO) ---")
cur.execute("SELECT id, nombre, email FROM inversores WHERE nombre ILIKE '%Leandro%'")
leandros = cur.fetchall()
for l in leandros:
    print(f"Encontrado Leandro ID: {l[0]} - {l[1]} ({l[2]})")
    cur.execute("SELECT id, importe, ganancia_acelerada, estado FROM aportaciones WHERE inversor_id = %s", (l[0],))
    aports = cur.fetchall()
    
    for ap in aports:
        print(f"  -> Contrato ID {ap[0]} | Importe: {ap[1]} | Acelerador Actual: {ap[2]} | Estado {ap[3]}")
        # Si es el contrato grande de 9000, inyectamos el 45.9
        if float(ap[1] or 0) >= 9000:
            cur.execute("UPDATE aportaciones SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + 45.90 WHERE id = %s", (ap[0],))
            print(f"  [!] -> BONO TACTICO INYECTADO: +45.9 USDT a contrato {ap[0]}")

conn.commit()
print("\nOperacion masiva completada.")

cur.close()
conn.close()
