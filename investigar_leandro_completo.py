"""
Script para investigar qué pasó con el crédito de Leandro
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def investigar_historial_leandro():
    """Investigar el historial completo de Leandro"""
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("INVESTIGACIÓN COMPLETA DE LEANDRO")
    print("="*60)
    
    # 1. Datos actuales
    print("\n1️⃣ DATOS ACTUALES:")
    cursor.execute("""
        SELECT id, nombre, email, 
               COALESCE(credito_disponible, 0) as disponible,
               COALESCE(credito_retirado, 0) as retirado,
               referido_por_id, referido_por_agente_id,
               created_at
        FROM estudiantes
        WHERE id = 1
    """)
    leandro = cursor.fetchone()
    
    if leandro:
        print(f"   ID: {leandro[0]}")
        print(f"   Nombre: {leandro[1]}")
        print(f"   Email: {leandro[2]}")
        print(f"   💰 Disponible: {leandro[3]:.2f}€")
        print(f"   ✅ Retirado: {leandro[4]:.2f}€")
        print(f"   👤 Referido por estudiante: {leandro[5]}")
        print(f"   👨‍💼 Referido por agente: {leandro[6]}")
        print(f"   📅 Registro: {leandro[7]}")
    
    # 2. Verificar si refirió a alguien
    print("\n2️⃣ ESTUDIANTES QUE LEANDRO REFIRIÓ:")
    cursor.execute("""
        SELECT id, nombre, email, estado, created_at
        FROM estudiantes
        WHERE referido_por_id = 1
        ORDER BY created_at DESC
    """)
    referidos = cursor.fetchall()
    
    if referidos:
        for ref in referidos:
            print(f"\n   👤 {ref[1]} (ID: {ref[0]})")
            print(f"      Estado: {ref[3]}")
            print(f"      Fecha: {ref[4]}")
    else:
        print("   ⚠️  Leandro NO ha referido a nadie")
    
    # 3. Presupuestos de sus referidos
    if referidos:
        print("\n3️⃣ PRESUPUESTOS DE SUS REFERIDOS:")
        cursor.execute("""
            SELECT p.id, p.estudiante_id, e.nombre, p.estado, p.precio_ofertado,
                   p.created_at, p.precio_ofertado * 0.05 as comision
            FROM presupuestos p
            JOIN estudiantes e ON p.estudiante_id = e.id
            WHERE e.referido_por_id = 1
            ORDER BY p.created_at DESC
        """)
        presupuestos = cursor.fetchall()
        
        if presupuestos:
            total_comision = 0
            for pres in presupuestos:
                print(f"\n   📊 Presupuesto #{pres[0]}")
                print(f"      Estudiante: {pres[2]} (ID: {pres[1]})")
                print(f"      Estado: {pres[3]}")
                precio = pres[4] if pres[4] else 0
                comision = pres[6] if pres[6] else 0
                print(f"      Precio: {precio:.2f}€")
                print(f"      Comisión (5%): {comision:.2f}€")
                if pres[3] == 'aceptado' and comision:
                    total_comision += comision
            
            print(f"\n   💰 TOTAL COMISIÓN GANADA: {total_comision:.2f}€")
            print(f"   ⚠️  Pero Leandro tiene: {leandro[3]:.2f}€ disponible")
            
            if total_comision > 0 and leandro[3] == 0:
                print(f"\n   🔴 PROBLEMA: Ganó {total_comision:.2f}€ pero tiene 0€")
                print(f"   💡 Posible causa: No se actualizó credito_disponible al aceptar presupuestos")
        else:
            print("   ⚠️  No hay presupuestos aceptados de sus referidos")
    
    # 4. Solicitudes de crédito
    print("\n4️⃣ SOLICITUDES DE CRÉDITO:")
    cursor.execute("""
        SELECT id, tipo, monto, estado, fecha_solicitud, fecha_respuesta, notas
        FROM solicitudes_credito
        WHERE estudiante_id = 1
        ORDER BY fecha_solicitud DESC
    """)
    solicitudes = cursor.fetchall()
    
    if solicitudes:
        for sol in solicitudes:
            estado_emoji = "✅" if sol[3] == "aprobada" else "⏳" if sol[3] == "pendiente" else "❌"
            print(f"\n   {estado_emoji} {sol[1].upper()} - {sol[2]:.2f}€")
            print(f"      Estado: {sol[3]}")
            print(f"      Solicitud: {sol[4]}")
            print(f"      Respuesta: {sol[5]}")
            if sol[6]:
                print(f"      Notas: {sol[6]}")
    else:
        print("   ⚠️  No hay solicitudes de crédito")
    
    # 5. ¿Leandro refiere a alguien que generó comisión?
    print("\n5️⃣ ANÁLISIS DE COMISIONES:")
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT e.id) as total_referidos,
            COUNT(DISTINCT CASE WHEN p.estado = 'aceptado' THEN p.id END) as presupuestos_aceptados,
            COALESCE(SUM(CASE WHEN p.estado = 'aceptado' THEN p.precio_ofertado * 0.05 ELSE 0 END), 0) as comision_deberia_tener
        FROM estudiantes e
        LEFT JOIN presupuestos p ON p.estudiante_id = e.id
        WHERE e.referido_por_id = 1
    """)
    stats = cursor.fetchone()
    
    print(f"   👥 Total referidos: {stats[0]}")
    print(f"   ✅ Presupuestos aceptados: {stats[1]}")
    print(f"   💰 Comisión que debería tener: {stats[2]:.2f}€")
    print(f"   💰 Comisión que realmente tiene: {leandro[3]:.2f}€")
    
    if stats[2] > 0 and leandro[3] == 0:
        print(f"\n   🔴 CONFIRMADO: Falta acreditar {stats[2]:.2f}€")
        print(f"\n   💡 SOLUCIÓN: Ejecutar script de corrección")
        
        respuesta = input("\n   ¿Acreditar {:.2f}€ a Leandro? (s/n): ".format(stats[2]))
        if respuesta.lower() == 's':
            cursor.execute("""
                UPDATE estudiantes
                SET credito_disponible = credito_disponible + %s
                WHERE id = 1
            """, (stats[2],))
            conn.commit()
            print(f"\n   ✅ Acreditados {stats[2]:.2f}€ a Leandro")
            
            # Verificar
            cursor.execute("""
                SELECT COALESCE(credito_disponible, 0), COALESCE(credito_retirado, 0)
                FROM estudiantes WHERE id = 1
            """)
            nuevo = cursor.fetchone()
            print(f"\n   📊 Estado actualizado:")
            print(f"      💰 Disponible: {nuevo[0]:.2f}€")
            print(f"      ✅ Retirado: {nuevo[1]:.2f}€")
            print(f"      📈 Total: {(nuevo[0] + nuevo[1]):.2f}€")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ INVESTIGACIÓN COMPLETA")
    print("="*60 + "\n")

if __name__ == "__main__":
    investigar_historial_leandro()
