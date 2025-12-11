"""
Script para simular la validación del endpoint de responder solicitudes
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

print("=== SIMULACIÓN DE VALIDACIÓN verificar_admin ===\n")

# Simular payload del token
token_viejo = {
    "usuario": "leandroeloytamayoreyes@gmail.com",
    "is_admin": True,  # ❌ Token viejo
    "exp": 1234567890
}

token_nuevo = {
    "usuario": "leandroeloytamayoreyes@gmail.com",
    "rol": "admin",  # ✅ Token nuevo
    "exp": 1234567890
}

print("🔑 TOKEN VIEJO (antes de logout/login):")
print(f"   {token_viejo}")
print(f"   Tiene 'is_admin': {token_viejo.get('is_admin')}")
print(f"   Tiene 'rol': {token_viejo.get('rol')}")
print(f"   verificar_admin busca 'rol': {token_viejo.get('rol') == 'admin'}")
print(f"   ❌ RESULTADO: 403 Forbidden (rol es None)\n")

print("🔑 TOKEN NUEVO (después de logout/login):")
print(f"   {token_nuevo}")
print(f"   Tiene 'is_admin': {token_nuevo.get('is_admin')}")
print(f"   Tiene 'rol': {token_nuevo.get('rol')}")
print(f"   verificar_admin busca 'rol': {token_nuevo.get('rol') == 'admin'}")
print(f"   ✅ RESULTADO: Autorizado\n")

print("\n📊 VERIFICANDO SOLICITUD EN BD:\n")

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            sc.id,
            sc.estudiante_id,
            sc.tipo,
            sc.monto,
            sc.estado,
            sc.beneficiario_tipo,
            sc.beneficiario_id,
            e.nombre,
            e.credito_disponible
        FROM solicitudes_credito sc
        LEFT JOIN estudiantes e ON e.id = sc.beneficiario_id
        WHERE sc.id = 5
    """)
    
    sol = cursor.fetchone()
    
    if not sol:
        print("❌ Solicitud 5 no encontrada")
    else:
        sol_id, est_id, tipo, monto, estado, ben_tipo, ben_id, nombre, credito = sol
        print(f"✅ Solicitud encontrada:")
        print(f"   ID: {sol_id}")
        print(f"   estudiante_id: {est_id}")
        print(f"   tipo: {tipo}")
        print(f"   monto: €{float(monto):.2f}")
        print(f"   estado: {estado}")
        print(f"   beneficiario_tipo: {ben_tipo}")
        print(f"   beneficiario_id: {ben_id}")
        print(f"   nombre: {nombre}")
        print(f"   credito_disponible: €{float(credito) if credito else 0:.2f}")
        print()
        
        # Verificar si la conversión Decimal->float funcionará
        print("🔍 VERIFICANDO CONVERSIÓN DE TIPOS:")
        print(f"   tipo de monto: {type(monto)}")
        print(f"   float(monto): {float(monto)}")
        print(f"   ✅ Conversión exitosa")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n\n⚠️  DIAGNÓSTICO DEL ERROR 500:")
print("   Si el admin YA hizo logout/login y sigue dando 500:")
print("   1. El error NO es de autenticación (sería 403)")
print("   2. Hay un error en la lógica del endpoint")
print("   3. Revisar logs de Render para ver el error exacto")
print()
print("   Si el admin NO ha hecho logout/login:")
print("   1. Todavía tiene token viejo (sin campo 'rol')")
print("   2. verificar_admin() debería dar 403, no 500")
print("   3. El 500 sugiere que hay otro error en el código")
