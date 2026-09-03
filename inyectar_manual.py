import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def inyectar_usuario():
    email = "emiliojose4002@hotmail.com"
    importe = 500.0
    moneda = "USDT BEP-20"
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # 1. Encontrar usuario
    cur.execute("SELECT id, nombre, email FROM inversores WHERE email = %s", (email,))
    user = cur.fetchone()
    if not user:
        print(f"Error: No se encontró al usuario con email {email}")
        return
        
    inversor_id, nombre_inv, email_inv = user
    print(f"Usuario encontrado: ID {inversor_id} - {nombre_inv}")
    
    # 2. Insertar aportación (Empieza a correr el reloj AHORA)
    tasa_diaria = 0.5
    cur.execute("""
        INSERT INTO aportaciones (inversor_id, nombre, email, importe, moneda, estado, fecha_aprobacion, tasa_diaria) 
        VALUES (%s, %s, %s, %s, %s, 'Aprobada', CURRENT_TIMESTAMP, %s)
        RETURNING id
    """, (inversor_id, nombre_inv, email_inv, importe, moneda, tasa_diaria))
    
    aportacion_id = cur.fetchone()[0]
    print(f"Aportación inyectada exitosamente con ID {aportacion_id}")
    
    # 3. Notificación
    cur.execute("""
        INSERT INTO notificaciones (inversor_id, mensaje, tipo) 
        VALUES (%s, %s, 'INGRESO')
    """, (inversor_id, f"El corporativo ha inyectado 500 {moneda} a tu cuenta. Se encuentra activa y retenida por 72h."))
    
    # 4. Acelerador de bono de referido (10%) = 50 USDT
    monto_acelerador = importe * 0.10
    cur.execute("SELECT referido_por FROM inversores WHERE id = %s", (inversor_id,))
    ref_row = cur.fetchone()
    if ref_row and ref_row[0]:
        patrocinador_codigo = ref_row[0]
        cur.execute("SELECT id FROM inversores WHERE codigo_referido = %s", (patrocinador_codigo,))
        patr_row = cur.fetchone()
        if patr_row:
            patrocinador_id = patr_row[0]
            print(f"Patrocinador encontrado (ID: {patrocinador_id}). Pagando {monto_acelerador} de bono acelerador...")
            cur.execute("""
                SELECT id, importe, COALESCE(ganancia_acelerada, 0) as ganac, COALESCE(ganancia_rentabilidad, 0) as rent
                FROM aportaciones 
                WHERE inversor_id = %s AND (estado = 'Aprobada' OR estado = 'Activa')
                ORDER BY fecha_aprobacion ASC NULLS LAST, id ASC
            """, (patrocinador_id,))
            invs_activas = cur.fetchall()
            
            monto_restante = monto_acelerador
            for inv in invs_activas:
                if monto_restante <= 0: break
                inv_id = inv[0]
                inv_importe = float(inv[1])
                inv_ganac = float(inv[2])
                inv_rent = float(inv[3])
                
                meta = inv_importe * 3.0
                espacio_libre = meta - (inv_rent + inv_ganac)
                
                if espacio_libre > 0:
                    abs_ganado = min(monto_restante, espacio_libre)
                    estado_inv = 'Activa'
                    if (inv_rent + inv_ganac + abs_ganado) >= meta: 
                        estado_inv = 'Completada (300%)'
                        print(f"  -> La inversión {inv_id} se ha COMPLETADO AL 300%")
                    
                    cur.execute("UPDATE aportaciones SET ganancia_acelerada = ganancia_acelerada + %s, estado = %s WHERE id = %s", (abs_ganado, estado_inv, inv_id))
                    monto_restante -= abs_ganado
                    print(f"  -> Pagado {abs_ganado} al contrato {inv_id}")
    
    conn.commit()
    cur.close()
    conn.close()
    print("¡OPERACIÓN COMANDADA EXITOSAMENTE! El reloj cronometrado empezó a correr.")

if __name__ == "__main__":
    inyectar_usuario()
