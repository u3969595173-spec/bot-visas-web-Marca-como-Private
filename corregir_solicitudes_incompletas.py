"""
Script para corregir solicitudes de crédito con datos incompletos
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

print("=== CORRECCIÓN DE SOLICITUDES DE CRÉDITO ===\n")

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    # Buscar solicitudes con datos incompletos
    print("🔍 Buscando solicitudes con datos incompletos...\n")
    cursor.execute("""
        SELECT id, estudiante_id, tipo, monto, beneficiario_tipo, beneficiario_id
        FROM solicitudes_credito
        WHERE beneficiario_tipo IS NULL OR beneficiario_id IS NULL
    """)
    
    incompletas = cursor.fetchall()
    
    if not incompletas:
        print("✅ No hay solicitudes con datos incompletos")
    else:
        print(f"⚠️  Encontradas {len(incompletas)} solicitudes con datos incompletos:\n")
        
        for sol in incompletas:
            sol_id, est_id, tipo, monto, ben_tipo, ben_id = sol
            print(f"ID {sol_id}:")
            print(f"  estudiante_id: {est_id}")
            print(f"  tipo: {tipo}")
            print(f"  monto: €{float(monto):.2f}")
            print(f"  beneficiario_tipo: {ben_tipo}")
            print(f"  beneficiario_id: {ben_id}")
            
            # Corregir datos
            if est_id:
                print(f"  ➡️  Corrigiendo: beneficiario_tipo='estudiante', beneficiario_id={est_id}")
                cursor.execute("""
                    UPDATE solicitudes_credito
                    SET beneficiario_tipo = 'estudiante',
                        beneficiario_id = %s
                    WHERE id = %s
                """, (est_id, sol_id))
            else:
                print(f"  ❌ No se puede corregir: estudiante_id es NULL. Marcando como rechazada.")
                cursor.execute("""
                    UPDATE solicitudes_credito
                    SET estado = 'rechazada',
                        notas = 'Solicitud rechazada automáticamente por datos incompletos',
                        fecha_respuesta = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (sol_id,))
            
            print()
        
        conn.commit()
        print("✅ Solicitudes corregidas exitosamente")
    
    # Verificar resultado
    print("\n📋 SOLICITUDES PENDIENTES DESPUÉS DE LA CORRECCIÓN:\n")
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
        LEFT JOIN estudiantes e ON e.id = sc.beneficiario_id AND sc.beneficiario_tipo = 'estudiante'
        LEFT JOIN agentes a ON a.id = sc.beneficiario_id AND sc.beneficiario_tipo = 'agente'
        WHERE sc.estado = 'pendiente'
        ORDER BY sc.fecha_solicitud DESC
    """)
    
    pendientes = cursor.fetchall()
    
    if not pendientes:
        print("✅ No hay solicitudes pendientes")
    else:
        for sol in pendientes:
            sol_id, nombre, tipo_persona, tipo_solicitud, monto, estado, credito = sol
            print(f"ID: {sol_id}")
            print(f"   Solicitante: {nombre or 'N/A'} ({tipo_persona or 'N/A'})")
            print(f"   Tipo: {tipo_solicitud}")
            print(f"   Monto: €{float(monto) if monto else 0:.2f}")
            print(f"   Crédito disponible: €{float(credito) if credito else 0:.2f}")
            print(f"   Estado: {estado}")
            print()
    
    cursor.close()
    conn.close()
    
    print("\n✅ Corrección completada")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
