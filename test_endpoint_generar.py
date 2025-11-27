import requests
import json

# Probar en Render (tu deploy actual)
API_URL = input("Ingresa la URL de tu API (ej: https://tu-app.onrender.com): ").strip() or "http://localhost:8000"

# Test generar documentos
estudiante_id = 1

print(f"🧪 Testing: GET {API_URL}/api/estudiantes/{estudiante_id}/generar-documentos")
print("=" * 70)

try:
    response = requests.get(f"{API_URL}/api/estudiantes/{estudiante_id}/generar-documentos", timeout=10)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print("\n📄 Response Body:")
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"\n✅ SUCCESS: Generados {len(data.get('documentos', []))} documentos")
    else:
        print(f"❌ ERROR: {response.text}")
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")
