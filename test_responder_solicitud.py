"""
Script para probar el endpoint de responder solicitudes de crédito
"""

import os
from dotenv import load_dotenv
import psycopg2
from decimal import Decimal

load_dotenv()

print("=== PRUEBA DE RESPONDER SOLICITUDES DE CRÉDITO ===\n")

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    # Verificar solicitudes pendientes
    print("📋 SOLICITUDES PENDIENTES:\n")
    cursor.execute("""
        SELECT 
            sc.id,
            COALESCE(e.nombre, a.nombre) as nombre,
            sc.beneficiario_tipo,
            sc.tipo,
            sc.monto,
            sc.estado,
            COALESCE(e.credito_disponible, a.credito_disponible) as credito_disponible
        FROM solicitudes_credito sc
        LEFT JOIN estudiantes e ON e.id = sc.estudiante_id AND sc.beneficiario_tipo = 'estudiante'
        LEFT JOIN agentes a ON a.id = sc.beneficiario_id AND sc.beneficiario_tipo = 'agente'
        WHERE sc.estado = 'pendiente'
        ORDER BY sc.fecha_solicitud DESC
    """)
    
    solicitudes = cursor.fetchall()
    
    if not solicitudes:
        print("❌ No hay solicitudes pendientes")
    else:
        for sol in solicitudes:
            sol_id, nombre, tipo_persona, tipo_solicitud, monto, estado, credito = sol
            print(f"ID: {sol_id}")
            print(f"   Solicitante: {nombre or 'N/A'} ({tipo_persona or 'N/A'})")
            print(f"   Tipo: {tipo_solicitud}")
            print(f"   Monto: €{float(monto) if monto else 0:.2f}")
            print(f"   Crédito disponible: €{float(credito) if credito else 0:.2f}")
            print(f"   Estado: {estado}")
            
            # Verificar datos faltantes
            if not nombre or not tipo_persona:
                print(f"   ⚠️  DATOS INCOMPLETOS - Revisar beneficiario_id y beneficiario_tipo")
            print()
    
    # Verificar tipos de datos
    print("\n🔍 VERIFICACIÓN DE TIPOS DE DATOS:\n")
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'solicitudes_credito' 
        AND column_name IN ('monto', 'estudiante_id', 'beneficiario_id')
    """)
    
    tipos = cursor.fetchall()
    for col, tipo in tipos:
        print(f"   {col}: {tipo}")
    
    # Verificar estructura completa
    print("\n📊 ESTRUCTURA DE TABLA solicitudes_credito:\n")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'solicitudes_credito'
        ORDER BY ordinal_position
    """)
    
    columnas = cursor.fetchall()
    for col in columnas:
        col_name, data_type, nullable, default = col
        print(f"   {col_name}: {data_type} (NULL: {nullable}, Default: {default or 'None'})")
    
    print("\n✅ Verificación completada")
    print("\n⚠️  IMPORTANTE:")
    print("   - El endpoint ahora usa verificar_admin en lugar de obtener_usuario_actual")
    print("   - Convierte Decimal a float para evitar errores de serialización")
    print("   - Tiene manejo de errores con try-catch y rollback")
    print("   - Valida que el crédito sea suficiente antes de aprobar")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
