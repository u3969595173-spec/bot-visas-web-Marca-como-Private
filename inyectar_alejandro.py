import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Find users related to 'Ale'
cur.execute("SELECT id, nombre, email, referido_por FROM inversores WHERE nombre ILIKE '%Ale%' OR email ILIKE '%Ale%' ORDER BY id DESC LIMIT 5")
users = cur.fetchall()
print("Usuarios potenciales:")
for u in users:
    print(u)

if users:
    # Selecciona al usuario más reciente (que suele ser el que Leandro invitó ayer)
    target = users[0]
    id_receptor = target[0]
    nombre = target[1]
    email = target[2]
    sponsor = target[3]
    importe = 741.00
    
    print(f"\n[+] Procediendo a inyectar {importe} USDT a: {nombre} (ID: {id_receptor})")
    
    # 1. Crear aportacion con estado 'Activa' 
    cur.execute("""
        INSERT INTO aportaciones (inversor_id, nombre, email, importe, moneda, estado, fecha_aprobacion)
        VALUES (%s, %s, %s, %s, 'USDT', 'Activa', CURRENT_TIMESTAMP)
        RETURNING id
    """, (id_receptor, nombre, email, importe))
    aport_id = cur.fetchone()[0]
    print(f"|-- Aportación Creada (ID: {aport_id})")
    
    # 2. Desatar algoritmo 10% Acelerador Referidos
    if sponsor:
        cur.execute("SELECT id FROM inversores WHERE codigo_referido = %s LIMIT 1", (sponsor,))
        sponsor_row = cur.fetchone()
        if sponsor_row:
            sponsor_id = sponsor_row[0]
            bono = importe * 0.10
            
            cur.execute("""
                SELECT id FROM aportaciones 
                WHERE inversor_id = %s AND (estado = 'Activa' OR estado = 'Validada')
                ORDER BY created_at ASC LIMIT 1
            """, (sponsor_id,))
            pa = cur.fetchone()
            
            if pa:
                cur.execute("UPDATE aportaciones SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + %s WHERE id = %s", (bono, pa[0]))
                print(f"|-- Bono 10% (${bono} USDT) transferido al Patrocinador (ID DBMaster: {sponsor_id})")
            else:
                print(f"|-- x El patrocinador {sponsor_id} no tiene contratos Activos. El Bono se quema.")

    conn.commit()
    print("\n✅ Inyección Corporativa completada con éxito. Revisa el Balance.")
else:
    print("No se encontró a nadie llamado Ale")

cur.close()
conn.close()
