"""
Verificar qué endpoints están disponibles en producción
"""
import requests

base_url = "https://bot-visas-web-marca-como-private.onrender.com"

print("[TEST] Verificando endpoints disponibles...\n")

# 1. Health check
print("1. Testing /health")
try:
    response = requests.get(f"{base_url}/health", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# 2. Root
print("\n2. Testing /")
try:
    response = requests.get(f"{base_url}/", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Version: {data.get('version')}")
        print(f"   Servicio: {data.get('servicio')}")
except Exception as e:
    print(f"   Error: {e}")

# 3. Endpoint de referidos
print("\n3. Testing /api/referidos/estadisticas/1")
try:
    response = requests.get(f"{base_url}/api/referidos/estadisticas/1", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    else:
        print(f"   Error: {response.text if response.text else 'No response body'}")
except Exception as e:
    print(f"   Error: {e}")

# 4. Docs
print("\n4. Testing /docs (OpenAPI)")
try:
    response = requests.get(f"{base_url}/docs", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Docs disponibles: {'SI' if response.status_code == 200 else 'NO'}")
except Exception as e:
    print(f"   Error: {e}")

print("\n✅ Verificación completa")
