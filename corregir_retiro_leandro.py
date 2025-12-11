"""
Corregir manualmente el retiro de Leandro
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def corregir_retiro_leandro():
    """Procesar correctamente el retiro de Leandro"""
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("CORRECCIÓN DEL RETIRO DE LEANDRO")
    print("="*60)
    
    # 1. Estado actual
    print("\n📊 ESTADO ANTES DE LA CORRECCIÓN:")
    cursor.execute("""
        SELECT id, nombre, 
               COALESCE(credito_disponible, 0) as disponible,
               COALESCE(credito_retirado, 0) as retirado
        FROM estudiantes WHERE id = 1
    """)
    antes = cursor.fetchone()
    print(f"   💰 Disponible: {antes[2]:.2f}€")
    print(f"   ✅ Retirado: {antes[3]:.2f}€")
    print(f"   📈 Total: {(antes[2] + antes[3]):.2f}€")
    
    # 2. Actualizar créditos
    print("\n🔧 APLICANDO CORRECCIÓN...")
    print("   - Acreditando 100€ de comisión pendiente")
    print("   - Procesando retiro de 100€")
    
    cursor.execute("""
        UPDATE estudiantes
        SET credito_disponible = 100,
            credito_retirado = 0
        WHERE id = 1
    """)
    
    # Ahora procesar el retiro correctamente
    cursor.execute("""
        UPDATE estudiantes
        SET credito_disponible = credito_disponible - 100,
            credito_retirado = COALESCE(credito_retirado, 0) + 100
        WHERE id = 1
    """)
    
    # 3. Actualizar solicitud a aprobada
    cursor.execute("""
        UPDATE solicitudes_credito
        SET estado = 'aprobada',
            notas = 'Aprobada y procesada correctamente (corrección manual)'
        WHERE id = 1
    """)
    
    conn.commit()
    
    # 4. Verificar resultado
    print("\n✅ ESTADO DESPUÉS DE LA CORRECCIÓN:")
    cursor.execute("""
        SELECT COALESCE(credito_disponible, 0) as disponible,
               COALESCE(credito_retirado, 0) as retirado
        FROM estudiantes WHERE id = 1
    """)
    despues = cursor.fetchone()
    print(f"   💰 Disponible: {despues[0]:.2f}€")
    print(f"   ✅ Retirado: {despues[1]:.2f}€")
    print(f"   📈 Total Ganado: {(despues[0] + despues[1]):.2f}€")
    
    # 5. Verificar solicitud
    cursor.execute("""
        SELECT estado, notas FROM solicitudes_credito WHERE id = 1
    """)
    solicitud = cursor.fetchone()
    print(f"\n📋 Solicitud de retiro:")
    print(f"   Estado: {solicitud[0]}")
    print(f"   Notas: {solicitud[1]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ CORRECCIÓN COMPLETADA")
    print("="*60)
    print("\nAhora:")
    print("   • Leandro tiene 0€ disponible (ya retiró todo)")
    print("   • Leandro tiene 100€ retirado (historial)")
    print("   • Total ganado: 100€")
    print("   • La solicitud está marcada como aprobada")
    print("="*60 + "\n")

if __name__ == "__main__":
    corregir_retiro_leandro()
