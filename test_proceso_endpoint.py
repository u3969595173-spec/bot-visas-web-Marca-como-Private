import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# URL de producción
API_URL = "https://bot-visas-api.onrender.com"

# Primero hacer login para obtener token
print("🔑 Obteniendo token de admin...")
login_response = requests.post(
    f"{API_URL}/api/login",
    json={
        "email": "admin@botvisas.com",
        "password": "admin123"
    }
)

if login_response.status_code == 200:
    token = login_response.json()["token"]
    print(f"✅ Token obtenido: {token[:50]}...")
    
    # Ahora probar actualizar proceso
    print("\n📝 Probando actualizar proceso de visa...")
    
    data = {
        "paso": "paso_inscripcion",
        "completado": True,
        "notas": "Test desde script"
    }
    
    print(f"Datos a enviar: {json.dumps(data, indent=2)}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.put(
        f"{API_URL}/api/admin/estudiantes/1/proceso-visa",
        json=data,
        headers=headers
    )
    
    print(f"\n📊 Status Code: {response.status_code}")
    print(f"📄 Response: {response.text}")
    
    if response.status_code == 422:
        print("\n❌ Error 422 - Detalles:")
        try:
            error_detail = response.json()
            print(json.dumps(error_detail, indent=2))
        except:
            print(response.text)
else:
    print(f"❌ Error en login: {login_response.status_code}")
    print(f"Response: {login_response.text}")
