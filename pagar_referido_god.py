import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

email_target = 'oragmymartinez1988@gmail.com'
monto_base = 25.00
bono = monto_base * 0.10

print(f"Iniciando pago manual de patente P2P (Bono: {bono} USDT)...")

# 1. Encontrar al usuario y a su patrocinador
cur.execute("SELECT id, nombre, referido_por FROM inversores WHERE email = %s LIMIT 1", (email_target,))
inversor = cur.fetchone()

if not inversor:
    print(f"Error: Inversor {email_target} no encontrado.")
else:
    inversor_id, nombre, referido_por = inversor
    
    if not referido_por:
        print("El usuario no tiene patrocinador (fue registro limpio). Nada que pagar.")
    else:
        # 2. Localizar al patrocinador
        cur.execute("SELECT id, nombre FROM inversores WHERE codigo_referido = %s LIMIT 1", (referido_por,))
        sponsor = cur.fetchone()
        
        if not sponsor:
            print(f"El codigo de patrocinio '{referido_por}' existe pero no enlaza a ninguna cuenta valida. Nada que pagar.")
        else:
            sponsor_id, sponsor_nombre = sponsor
            
            # 3. Pagar el 10% sumandolo a la ultima bolsa activa del patrocinador
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
                
                # 4. Registrar en historial de comisiones para la trazabilidad
                cur.execute("""
                    INSERT INTO referidos_ganancias (codigo_referido, inversor_origen_id, importe_generado, tipo, es_p2p, estado)
                    VALUES (%s, %s, %s, 'Acelerador Inmediato (10%)', TRUE, 'Pagado')
                """, (referido_por, inversor_id, bono))
                
                conn.commit()
                print(f"¡EXITO! Pagados {bono} USDT al patrocinador {sponsor_nombre} (Contrato #{aport_id}).")
            else:
                print(f"El patrocinador {sponsor_nombre} no tiene aportaciones activas para absorber el bono. Requiere intervencion.")

cur.close()
conn.close()
