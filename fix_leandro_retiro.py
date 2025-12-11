"""
Script para investigar la solicitud de retiro de Leandro
y corregir manualmente si es necesario
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def investigar_leandro():
    """Investigar y corregir la solicitud de Leandro"""
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("INVESTIGACIÓN SOLICITUD LEANDRO")
    print("="*60)
    
    # 1. Buscar estudiante Leandro
    print("\n1️⃣ Buscando estudiante Leandro...")
    cursor.execute("""
        SELECT id, nombre, email, 
               COALESCE(credito_disponible, 0) as disponible,
               COALESCE(credito_retirado, 0) as retirado
        FROM estudiantes
        WHERE LOWER(nombre) LIKE '%leandro%'
    """)
    leandro = cursor.fetchone()
    
    if leandro:
        print(f"   ✅ Encontrado: {leandro[1]} (ID: {leandro[0]})")
        print(f"      Email: {leandro[2]}")
        print(f"      💰 Disponible: {leandro[3]:.2f}€")
        print(f"      ✅ Retirado: {leandro[4]:.2f}€")
        leandro_id = leandro[0]
    else:
        print("   ❌ No se encontró a Leandro")
        return
    
    # 2. Buscar solicitud de retiro
    print("\n2️⃣ Buscando solicitud de retiro...")
    cursor.execute("""
        SELECT id, monto, estado, fecha_solicitud, fecha_respuesta, tipo
        FROM solicitudes_credito
        WHERE estudiante_id = %s AND tipo = 'retiro'
        ORDER BY fecha_solicitud DESC
    """, (leandro_id,))
    solicitud = cursor.fetchone()
    
    if solicitud:
        print(f"   ✅ Solicitud encontrada (ID: {solicitud[0]})")
        print(f"      💰 Monto: {solicitud[1]:.2f}€")
        print(f"      Estado: {solicitud[2]}")
        print(f"      📅 Fecha solicitud: {solicitud[3]}")
        print(f"      📅 Fecha respuesta: {solicitud[4]}")
        
        if solicitud[2] == 'aprobada':
            print("\n3️⃣ La solicitud está APROBADA pero el crédito NO se actualizó")
            print("   ⚠️  Esto indica que el UPDATE falló o no se ejecutó")
            
            # Corregir manualmente
            print("\n4️⃣ Corrigiendo manualmente...")
            monto = solicitud[1]
            
            # Verificar que tenga crédito disponible suficiente
            if leandro[3] >= monto:
                cursor.execute("""
                    UPDATE estudiantes
                    SET credito_disponible = credito_disponible - %s,
                        credito_retirado = credito_retirado + %s
                    WHERE id = %s
                """, (monto, monto, leandro_id))
                conn.commit()
                
                print(f"   ✅ Actualizado correctamente")
                print(f"      ➖ Restado de disponible: {monto:.2f}€")
                print(f"      ➕ Sumado a retirado: {monto:.2f}€")
                
                # Verificar
                cursor.execute("""
                    SELECT COALESCE(credito_disponible, 0), COALESCE(credito_retirado, 0)
                    FROM estudiantes WHERE id = %s
                """, (leandro_id,))
                nuevo = cursor.fetchone()
                print(f"\n   📊 Estado final:")
                print(f"      💰 Disponible: {nuevo[0]:.2f}€")
                print(f"      ✅ Retirado: {nuevo[1]:.2f}€")
                print(f"      📈 Total Ganado: {(nuevo[0] + nuevo[1]):.2f}€")
            else:
                print(f"   ❌ ERROR: No tiene crédito suficiente")
                print(f"      Necesita: {monto:.2f}€")
                print(f"      Tiene: {leandro[3]:.2f}€")
                print(f"\n   ⚠️  La solicitud NO debió aprobarse sin crédito")
                print(f"   💡 Cambiar estado a 'rechazada'...")
                
                cursor.execute("""
                    UPDATE solicitudes_credito
                    SET estado = 'rechazada',
                        notas = 'Rechazada automáticamente: crédito insuficiente'
                    WHERE id = %s
                """, (solicitud[0],))
                conn.commit()
                print(f"   ✅ Solicitud marcada como rechazada")
    else:
        print("   ❌ No se encontró solicitud de retiro")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ INVESTIGACIÓN COMPLETA")
    print("="*60 + "\n")

if __name__ == "__main__":
    investigar_leandro()
