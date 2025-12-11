"""
Script para verificar el rol del admin en la base de datos
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

print("=== VERIFICACIÓN DE ROLES DE ADMINISTRADOR ===\n")

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    # Verificar usuarios admin
    print("👥 USUARIOS EN LA BASE DE DATOS:\n")
    cursor.execute("""
        SELECT id, email, nombre, rol
        FROM usuarios
        ORDER BY id
    """)
    
    usuarios = cursor.fetchall()
    
    if not usuarios:
        print("❌ No hay usuarios en la base de datos")
    else:
        for usuario in usuarios:
            user_id, email, nombre, rol = usuario
            print(f"ID: {user_id}")
            print(f"   Email: {email}")
            print(f"   Nombre: {nombre}")
            print(f"   Rol: {rol}")
            if rol == 'admin':
                print(f"   ✅ ES ADMINISTRADOR")
            else:
                print(f"   ⚠️  NO es administrador (rol: {rol})")
            print()
    
    # Verificar estructura del token
    print("\n🔑 ESTRUCTURA DEL TOKEN JWT:\n")
    print("El token incluye estos campos:")
    print("   - usuario: email del admin")
    print("   - rol: 'admin' (debe ser exactamente 'admin')")
    print("   - exp: fecha de expiración")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - verificar_admin() ahora busca: rol == 'admin'")
    print("   - Antes buscaba: is_admin == True")
    print("   - Asegúrate que el rol en BD sea exactamente 'admin'")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Verificación completada")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
