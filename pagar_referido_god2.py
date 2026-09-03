import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

email_target = 'oragmymartinez1988@gmail.com'
monto_base = 25.00
bono = monto_base * 0.10

cur.execute("SELECT id, nombre, referido_por FROM inversores WHERE email = %s LIMIT 1", (email_target,))
inversor = cur.fetchone()

if not inversor:
    print(f"Error: Inversor no encontrado.")
else:
    inversor_id, nombre, referido_por = inversor
    
    if not referido_por or str(referido_por).strip() == '':
        print("El usuario no tiene código de patrocinador. Listo.")
    else:
        cur.execute("SELECT id, nombre FROM inversores WHERE codigo_referido = %s LIMIT 1", (referido_por,))
        sponsor = cur.fetchone()
        
        if not sponsor:
            print("El codigo ingresado es huerfano.")
        else:
            sponsor_id, sponsor_nombre = sponsor
            
            cur.execute("""
                SELECT id 
                FROM aportaciones 
                WHERE inversor_id = %s AND (estado = 'Activa' OR estado = 'Validada' OR estado = 'Aprobada') 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (sponsor_id,))
            aport = cur.fetchone()
            
            if aport:
                aport_id = aport[0]
                cur.execute("""
                    UPDATE aportaciones 
                    SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + %s
                    WHERE id = %s
                """, (bono, aport_id))
                
                conn.commit()
                print(f"PAGADO: {bono} USDT sumados con éxito a la cuenta de {sponsor_nombre}.")
            else:
                print(f"ERROR: {sponsor_nombre} no tiene aportacion base para sumar su bono.")

cur.close()
conn.close()
