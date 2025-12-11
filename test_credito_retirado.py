"""
Script para probar que el credito_retirado se suma correctamente
al aprobar retiros y se refleja en total_ganado
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def test_credito_retirado():
    """Verificar que credito_retirado funciona correctamente"""
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("VERIFICACIÓN DE CRÉDITO RETIRADO")
    print("="*60)
    
    # 1. Verificar columna credito_retirado existe
    print("\n1️⃣ Verificando columna credito_retirado en estudiantes...")
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'estudiantes' AND column_name = 'credito_retirado'
    """)
    col = cursor.fetchone()
    if col:
        print(f"   ✅ Columna existe: {col[0]} ({col[1]})")
    else:
        print("   ❌ Columna NO existe - ejecutar migración")
        return
    
    print("\n2️⃣ Verificando columna credito_retirado en agentes...")
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'agentes' AND column_name = 'credito_retirado'
    """)
    col = cursor.fetchone()
    if col:
        print(f"   ✅ Columna existe: {col[0]} ({col[1]})")
    else:
        print("   ❌ Columna NO existe - ejecutar migración")
        return
    
    # 2. Ver estudiantes con crédito
    print("\n3️⃣ Estudiantes con crédito disponible:")
    cursor.execute("""
        SELECT id, nombre, email, 
               COALESCE(credito_disponible, 0) as disponible,
               COALESCE(credito_retirado, 0) as retirado,
               COALESCE(credito_disponible, 0) + COALESCE(credito_retirado, 0) as total_ganado
        FROM estudiantes
        WHERE credito_disponible > 0 OR credito_retirado > 0
        ORDER BY credito_disponible DESC
        LIMIT 5
    """)
    estudiantes = cursor.fetchall()
    
    if estudiantes:
        for est in estudiantes:
            print(f"\n   👤 {est[1]} ({est[2]})")
            print(f"      💰 Disponible: {est[3]:.2f}€")
            print(f"      ✅ Retirado: {est[4]:.2f}€")
            print(f"      📊 Total Ganado: {est[5]:.2f}€")
    else:
        print("   ⚠️  No hay estudiantes con crédito")
    
    # 3. Ver agentes con comisión
    print("\n4️⃣ Agentes con comisión:")
    cursor.execute("""
        SELECT id, nombre, email,
               COALESCE(credito_disponible, 0) as disponible,
               COALESCE(credito_retirado, 0) as retirado,
               COALESCE(credito_disponible, 0) + COALESCE(credito_retirado, 0) as total_ganado
        FROM agentes
        WHERE credito_disponible > 0 OR credito_retirado > 0
        ORDER BY credito_disponible DESC
        LIMIT 5
    """)
    agentes = cursor.fetchall()
    
    if agentes:
        for ag in agentes:
            print(f"\n   👨‍💼 {ag[1]} ({ag[2]})")
            print(f"      💰 Disponible: {ag[3]:.2f}€")
            print(f"      ✅ Retirado: {ag[4]:.2f}€")
            print(f"      📊 Total Ganado: {ag[5]:.2f}€")
    else:
        print("   ⚠️  No hay agentes con comisión")
    
    # 4. Ver solicitudes de retiro
    print("\n5️⃣ Solicitudes de retiro:")
    cursor.execute("""
        SELECT sc.id, sc.estado, sc.tipo, sc.monto,
               COALESCE(e.nombre, a.nombre) as nombre,
               COALESCE(e.email, a.email) as email,
               sc.beneficiario_tipo
        FROM solicitudes_credito sc
        LEFT JOIN estudiantes e ON sc.estudiante_id = e.id
        LEFT JOIN agentes a ON sc.beneficiario_tipo = 'agente' AND sc.beneficiario_id = a.id
        WHERE sc.tipo = 'retiro'
        ORDER BY sc.fecha_solicitud DESC
        LIMIT 10
    """)
    solicitudes = cursor.fetchall()
    
    if solicitudes:
        for sol in solicitudes:
            estado_emoji = "✅" if sol[1] == "aprobada" else "⏳" if sol[1] == "pendiente" else "❌"
            tipo_usuario = "👨‍💼" if sol[6] == "agente" else "👤"
            print(f"\n   {estado_emoji} {tipo_usuario} {sol[4]} - {sol[3]:.2f}€ ({sol[1]})")
    else:
        print("   ⚠️  No hay solicitudes de retiro")
    
    # 5. Resumen contabilidad
    print("\n6️⃣ Resumen de Contabilidad:")
    cursor.execute("""
        SELECT 
            COALESCE(SUM(credito_disponible), 0) as total_disponible,
            COALESCE(SUM(credito_retirado), 0) as total_retirado
        FROM estudiantes
    """)
    est_totals = cursor.fetchone()
    
    cursor.execute("""
        SELECT 
            COALESCE(SUM(credito_disponible), 0) as total_disponible,
            COALESCE(SUM(credito_retirado), 0) as total_retirado
        FROM agentes
    """)
    ag_totals = cursor.fetchone()
    
    print(f"\n   📊 ESTUDIANTES:")
    print(f"      💰 Crédito Disponible: {est_totals[0]:.2f}€")
    print(f"      ✅ Crédito Retirado: {est_totals[1]:.2f}€")
    print(f"      📈 Total Ganado: {(est_totals[0] + est_totals[1]):.2f}€")
    
    print(f"\n   📊 AGENTES:")
    print(f"      💰 Crédito Disponible: {ag_totals[0]:.2f}€")
    print(f"      ✅ Crédito Retirado: {ag_totals[1]:.2f}€")
    print(f"      📈 Total Ganado: {(ag_totals[0] + ag_totals[1]):.2f}€")
    
    print(f"\n   📊 GLOBAL:")
    print(f"      💰 Total Disponible: {(est_totals[0] + ag_totals[0]):.2f}€")
    print(f"      ✅ Total Retirado: {(est_totals[1] + ag_totals[1]):.2f}€")
    print(f"      📈 Total Ganado: {(est_totals[0] + est_totals[1] + ag_totals[0] + ag_totals[1]):.2f}€")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ VERIFICACIÓN COMPLETA")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_credito_retirado()
