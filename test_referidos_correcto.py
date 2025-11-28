"""
Probar endpoint con la URL correcta del backend
"""
import requests

base_url = "https://bot-visas-api.onrender.com"

print("[TEST] Probando con la URL correcta del backend...\n")

# 1. Root
print("1. Testing /")
try:
    response = requests.get(f"{base_url}/", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Endpoint de referidos - estudiante ID 1
print("\n2. Testing /api/referidos/estadisticas/1")
try:
    response = requests.get(f"{base_url}/api/referidos/estadisticas/1", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Código: {data.get('codigo_referido')}")
        print(f"   ✅ Crédito: {data.get('credito_disponible')}€")
        print(f"   ✅ Total referidos: {data.get('total_referidos')}")
        print(f"   ✅ Total ganado: {data.get('total_ganado')}€")
    else:
        print(f"   ❌ Error {response.status_code}: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Validar código de referido
print("\n3. Testing /api/referidos/validar/CMMBAVBX")
try:
    response = requests.get(f"{base_url}/api/referidos/validar/CMMBAVBX", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Válido: {data.get('valido')}")
        if data.get('valido'):
            print(f"   ✅ Referidor: {data.get('referidor')}")
    else:
        print(f"   ❌ Error: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")
