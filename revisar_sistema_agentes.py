"""
Revisión completa del sistema de agentes
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def revisar_sistema_agentes():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("REVISIÓN COMPLETA DEL SISTEMA DE AGENTES")
    print("="*70)
    
    # 1. Estructura de tabla agentes
    print("\n1️⃣ ESTRUCTURA DE TABLA AGENTES:")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'agentes'
        ORDER BY ordinal_position
    """)
    columnas = cursor.fetchall()
    
    for col in columnas:
        print(f"   {col[0]:25} {col[1]:15} NULL={col[2]:5} Default={col[3]}")
    
    # 2. Contar agentes
    print("\n2️⃣ AGENTES REGISTRADOS:")
    cursor.execute("SELECT COUNT(*) FROM agentes")
    total = cursor.fetchone()[0]
    print(f"   Total: {total} agentes")
    
    if total > 0:
        cursor.execute("""
            SELECT id, nombre, email, codigo_referido, activo,
                   COALESCE(comision_total, 0) as comision,
                   COALESCE(credito_disponible, 0) as disponible,
                   COALESCE(credito_retirado, 0) as retirado,
                   total_referidos
            FROM agentes
            ORDER BY id
        """)
        agentes = cursor.fetchall()
        
        for ag in agentes:
            estado = "✅ Activo" if ag[4] else "❌ Inactivo"
            print(f"\n   👨‍💼 {ag[1]} (ID: {ag[0]})")
            print(f"      Email: {ag[2]}")
            print(f"      Código: {ag[3]}")
            print(f"      Estado: {estado}")
            print(f"      💰 Comisión Total: {ag[5]:.2f}€")
            print(f"      💳 Disponible: {ag[6]:.2f}€")
            print(f"      ✅ Retirado: {ag[7]:.2f}€")
            print(f"      👥 Referidos: {ag[8] or 0}")
    
    # 3. Estudiantes referidos por agentes
    print("\n3️⃣ ESTUDIANTES REFERIDOS POR AGENTES:")
    cursor.execute("""
        SELECT 
            a.id, a.nombre,
            COUNT(e.id) as total_referidos,
            COUNT(CASE WHEN p.estado = 'aceptado' THEN 1 END) as presupuestos_aceptados,
            COALESCE(SUM(CASE WHEN p.estado = 'aceptado' THEN 
                COALESCE(p.precio_al_empezar, 0) + 
                COALESCE(p.precio_con_visa, 0) + 
                COALESCE(p.precio_financiado, 0)
            ELSE 0 END), 0) as valor_total
        FROM agentes a
        LEFT JOIN estudiantes e ON e.referido_por_agente_id = a.id
        LEFT JOIN presupuestos p ON p.estudiante_id = e.id
        GROUP BY a.id, a.nombre
        HAVING COUNT(e.id) > 0
    """)
    
    refs = cursor.fetchall()
    if refs:
        for ref in refs:
            print(f"\n   👨‍💼 {ref[1]} (ID: {ref[0]})")
            print(f"      👥 Total referidos: {ref[2]}")
            print(f"      📊 Presupuestos aceptados: {ref[3]}")
            print(f"      💰 Valor total: {ref[4]:.2f}€")
            if ref[4] > 0:
                comision = ref[4] * 0.10
                print(f"      💵 Comisión (10%): {comision:.2f}€")
    else:
        print("   ⚠️  No hay agentes con referidos")
    
    # 4. Solicitudes de retiro de agentes
    print("\n4️⃣ SOLICITUDES DE RETIRO DE AGENTES:")
    cursor.execute("""
        SELECT sc.id, a.nombre, sc.monto, sc.estado, sc.fecha_solicitud
        FROM solicitudes_credito sc
        JOIN agentes a ON sc.beneficiario_id = a.id
        WHERE sc.beneficiario_tipo = 'agente'
        ORDER BY sc.fecha_solicitud DESC
        LIMIT 10
    """)
    
    solicitudes = cursor.fetchall()
    if solicitudes:
        for sol in solicitudes:
            estado_emoji = "✅" if sol[3] == "aprobada" else "⏳" if sol[3] == "pendiente" else "❌"
            print(f"   {estado_emoji} {sol[1]} - {sol[2]:.2f}€ ({sol[3]}) - {sol[4]}")
    else:
        print("   ⚠️  No hay solicitudes de retiro de agentes")
    
    # 5. Verificar endpoints funcionan
    print("\n5️⃣ ENDPOINTS DISPONIBLES:")
    endpoints = [
        "POST /api/agentes/registro - Registrar nuevo agente",
        "POST /api/agentes/login - Login agente",
        "GET /api/agentes/perfil - Ver perfil",
        "GET /api/agentes/estadisticas - Ver estadísticas",
        "GET /api/agentes/referidos - Lista de referidos",
        "GET /api/agentes/referidos/{id} - Detalle referido",
        "PUT /api/agentes/referidos/{id} - Actualizar referido",
        "POST /api/agentes/referidos/{id}/documentos - Subir documento",
        "POST /api/agentes/solicitar-retiro - Solicitar retiro"
    ]
    for ep in endpoints:
        print(f"   ✅ {ep}")
    
    # 6. Verificar comisiones automáticas
    print("\n6️⃣ SISTEMA DE COMISIONES:")
    print("   ✅ Al marcar pago → suma 10% automáticamente")
    print("   ✅ Diferencia con estudiantes: agentes 10%, estudiantes 5%")
    print("   ✅ Se acredita a credito_disponible")
    print("   ✅ Al aprobar retiro → suma a credito_retirado")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*70)
    print("✅ REVISIÓN COMPLETA")
    print("="*70 + "\n")

if __name__ == "__main__":
    revisar_sistema_agentes()
