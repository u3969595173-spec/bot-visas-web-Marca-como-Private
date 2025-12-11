"""
Ver todos los presupuestos y entender el sistema
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def ver_todos_presupuestos():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("ANÁLISIS COMPLETO DE PRESUPUESTOS")
    print("="*80)
    
    cursor.execute("""
        SELECT p.id, p.estudiante_id, e.nombre, p.estado, 
               p.precio_ofertado, p.modalidad_seleccionada,
               p.created_at, e.referido_por_id
        FROM presupuestos p
        JOIN estudiantes e ON p.estudiante_id = e.id
        ORDER BY p.created_at DESC
        LIMIT 20
    """)
    presupuestos = cursor.fetchall()
    
    print(f"\n📊 Total presupuestos encontrados: {len(presupuestos)}\n")
    
    for pres in presupuestos:
        precio = pres[4] if pres[4] else 0
        referido_por = pres[7] if pres[7] else "Nadie"
        
        print(f"{'='*80}")
        print(f"ID: {pres[0]} | Estudiante: {pres[2]} (ID: {pres[1]})")
        print(f"Estado: {pres[3]} | Precio: {precio:.2f}€")
        print(f"Modalidad: {pres[5] or 'No seleccionada'}")
        print(f"Fecha: {pres[6]}")
        print(f"Referido por: {referido_por}")
        
        if pres[3] == 'aceptado' and precio > 0 and pres[7]:
            comision = precio * 0.05
            print(f"💰 Comisión generada: {comision:.2f}€ para estudiante ID {pres[7]}")
    
    # Resumen de comisiones
    print(f"\n{'='*80}")
    print("RESUMEN DE COMISIONES POR REFERIDOR:")
    print(f"{'='*80}\n")
    
    cursor.execute("""
        SELECT 
            e_referidor.id,
            e_referidor.nombre,
            COUNT(DISTINCT p.id) as presupuestos,
            COUNT(DISTINCT CASE WHEN p.estado = 'aceptado' THEN p.id END) as aceptados,
            COALESCE(SUM(CASE WHEN p.estado = 'aceptado' THEN p.precio_ofertado * 0.05 ELSE 0 END), 0) as comision_total,
            e_referidor.credito_disponible,
            COALESCE(e_referidor.credito_retirado, 0) as credito_retirado
        FROM estudiantes e_referidor
        JOIN estudiantes e_referido ON e_referido.referido_por_id = e_referidor.id
        LEFT JOIN presupuestos p ON p.estudiante_id = e_referido.id
        GROUP BY e_referidor.id, e_referidor.nombre, e_referidor.credito_disponible, e_referidor.credito_retirado
        ORDER BY comision_total DESC
    """)
    
    referidores = cursor.fetchall()
    
    if referidores:
        for ref in referidores:
            print(f"👤 {ref[1]} (ID: {ref[0]})")
            print(f"   📊 Presupuestos de sus referidos: {ref[2]}")
            print(f"   ✅ Aceptados: {ref[3]}")
            print(f"   💰 Comisión que debería tener: {ref[4]:.2f}€")
            print(f"   💳 Crédito disponible actual: {ref[5]:.2f}€")
            print(f"   ✅ Crédito retirado: {ref[6]:.2f}€")
            
            diferencia = ref[4] - ref[5] - ref[6]
            if diferencia > 0.01:  # Si hay diferencia significativa
                print(f"   🔴 FALTA ACREDITAR: {diferencia:.2f}€")
            elif diferencia < -0.01:
                print(f"   ⚠️  TIENE MÁS DE LO QUE DEBERÍA: {abs(diferencia):.2f}€")
            else:
                print(f"   ✅ Todo cuadra")
            print()
    else:
        print("⚠️  No hay estudiantes que hayan referido a otros con presupuestos")
    
    cursor.close()
    conn.close()
    
    print("="*80)
    print("✅ ANÁLISIS COMPLETO")
    print("="*80 + "\n")

if __name__ == "__main__":
    ver_todos_presupuestos()
