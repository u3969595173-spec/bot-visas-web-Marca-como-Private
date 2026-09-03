import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

inversor_id = 81
# Let's see the duplicate deposits
cur.execute("SELECT id, importe FROM aportaciones WHERE inversor_id=%s AND importe=500 ORDER BY id ASC", (inversor_id,))
aportaciones = cur.fetchall()
print("Aportaciones actuales de 500 para inversor 81:", aportaciones)

if len(aportaciones) > 1:
    # Delete all except the most recent one (ID 32)
    ids_to_delete = [ap[0] for ap in aportaciones[:-1]]
    total_importe_to_reverse = sum([ap[1] for ap in aportaciones[:-1]])
    
    print(f"Borrando IDs duplicados: {ids_to_delete}. Dinero inyectado de mas: {total_importe_to_reverse}")
    
    # 1. Delete the duplicate aportaciones
    cur.execute("DELETE FROM aportaciones WHERE id = ANY(%s)", (ids_to_delete,))
    
    # 2. Reverse accelerator
    cur.execute("SELECT referido_por FROM inversores WHERE id = %s", (inversor_id,))
    ref = cur.fetchone()
    if ref and ref[0]:
        patrocinador_codigo = ref[0]
        cur.execute("SELECT id FROM inversores WHERE codigo_referido = %s", (patrocinador_codigo,))
        patr = cur.fetchone()
        if patr:
            patr_id = patr[0]
            acelerador_pagado = float(total_importe_to_reverse) * 0.10
            print(f"El patrocinador {patr_id} recibio {acelerador_pagado} de mas. Revertiendo...")
            
            # Since the accelerator is added to ganancia_acelerada of the sponsor's active aportaciones,
            # We just subtract it from the most recent active aportacion of the sponsor.
            cur.execute("""
                SELECT id, ganancia_acelerada FROM aportaciones 
                WHERE inversor_id = %s AND ganancia_acelerada > 0
                ORDER BY id DESC
            """, (patr_id,))
            patr_aports = cur.fetchall()
            
            to_subtract = float(total_importe_to_reverse) * 0.10
            for pa in patr_aports:
                if to_subtract <= 0: break
                pa_id = pa[0]
                pa_ganac = float(pa[1])
                
                deduct = min(to_subtract, pa_ganac)
                cur.execute("UPDATE aportaciones SET ganancia_acelerada = ganancia_acelerada - %s, estado = 'Activa' WHERE id = %s", (deduct, pa_id))
                to_subtract -= deduct
                print(f"  -> Se restaron {deduct} USDT del contrato {pa_id} del patrocinador (dejando estado en Activa x si estaba en 300%)")
                
    conn.commit()
    print("Reparación completa.")
else:
    print("No hay duplicados o no aplicable.")
    
cur.close()
conn.close()
