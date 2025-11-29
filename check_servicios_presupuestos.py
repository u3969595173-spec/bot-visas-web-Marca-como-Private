import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    
    # Check accepted presupuestos
    cur.execute("""
        SELECT p.id, p.estudiante_id, e.nombre, p.servicios, p.estado_servicio, p.estado
        FROM presupuestos p
        JOIN estudiantes e ON p.estudiante_id = e.id
        WHERE p.estado = 'aceptado'
        ORDER BY p.id DESC
    """)
    
    rows = cur.fetchall()
    
    if rows:
        print(f"\n[INFO] Encontrados {len(rows)} presupuestos aceptados:")
        for row in rows:
            presupuesto_id, est_id, nombre, servicios, estado_servicio, estado = row
            print(f"\n  Presupuesto ID: {presupuesto_id}")
            print(f"  Estudiante: {nombre} (ID: {est_id})")
            print(f"  Estado: {estado}")
            print(f"  Estado Servicio: {estado_servicio}")
            print(f"  Servicios: {servicios}")
            if servicios:
                print(f"  Cantidad de servicios: {len(servicios)}")
            else:
                print(f"  ⚠️  NO HAY SERVICIOS REGISTRADOS")
    else:
        print("\n[INFO] No hay presupuestos aceptados")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"[ERROR] {e}")
