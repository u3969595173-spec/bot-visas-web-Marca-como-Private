"""
Script para eliminar presupuestos de Onelvis vía API
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def delete_via_api():
    """Eliminar presupuestos de Onelvis usando el endpoint DELETE"""
    
    # URL de producción
    api_url = os.getenv('VITE_API_URL', 'https://tu-backend.onrender.com')
    
    # Token de admin - necesitas loguearte primero
    print("🔐 Necesitas el token de admin")
    print("Opciones:")
    print("1. Loguéate en el admin y copia el token de localStorage")
    print("2. O dame el email y password del admin para obtener el token")
    print()
    
    email = input("Email admin: ").strip()
    password = input("Password: ").strip()
    
    # Login para obtener token
    print("\n🔄 Obteniendo token...")
    login_response = requests.post(
        f"{api_url}/api/login",
        json={"email": email, "password": password}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Error en login: {login_response.text}")
        return
    
    token = login_response.json()['access_token']
    print("✅ Token obtenido")
    
    # Obtener ID de Onelvis
    print("\n🔍 Buscando Onelvis...")
    headers = {"Authorization": f"Bearer {token}"}
    
    estudiantes_response = requests.get(
        f"{api_url}/api/admin/estudiantes",
        headers=headers
    )
    
    if estudiantes_response.status_code != 200:
        print(f"❌ Error obteniendo estudiantes: {estudiantes_response.text}")
        return
    
    estudiantes = estudiantes_response.json()
    onelvis = None
    
    for est in estudiantes:
        if 'onelvis' in est['nombre'].lower():
            onelvis = est
            break
    
    if not onelvis:
        print("❌ No se encontró a Onelvis")
        return
    
    print(f"✅ Onelvis encontrado - ID: {onelvis['id']}, Nombre: {onelvis['nombre']}")
    
    # Eliminar presupuestos
    print(f"\n🗑️  Eliminando presupuestos de Onelvis (ID: {onelvis['id']})...")
    
    delete_response = requests.delete(
        f"{api_url}/api/admin/presupuestos/estudiante/{onelvis['id']}",
        headers=headers
    )
    
    if delete_response.status_code == 200:
        result = delete_response.json()
        print(f"\n✅ {result['message']}")
        print(f"📊 Presupuestos eliminados: {result['presupuestos_eliminados']}")
    else:
        print(f"❌ Error: {delete_response.text}")

if __name__ == "__main__":
    print("=" * 60)
    print("🗑️  ELIMINAR PRESUPUESTOS DE ONELVIS VÍA API")
    print("=" * 60)
    delete_via_api()
