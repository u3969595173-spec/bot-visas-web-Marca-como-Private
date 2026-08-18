"""
Script para verificar si el fix de fondos_disponibles está desplegado
Ejecutar: python verificar_fix_manuel.py
"""
import requests
import json
from datetime import datetime

API_URL = "https://bot-visas-api.onrender.com"

print("=" * 60)
print("🔍 VERIFICANDO FIX DE COMPLETAR PERFIL")
print("=" * 60)
print(f"Hora: {datetime.now().strftime('%H:%M:%S')}")
print(f"API: {API_URL}")
print()

# Test 1: Verificar que el endpoint existe
print("Test 1: Verificando endpoint...")
try:
    response = requests.options(f"{API_URL}/api/estudiantes/16/completar-perfil?codigo_acceso=TEST")
    if response.status_code == 200:
        print("✅ Endpoint responde")
    else:
        print(f"⚠️  Endpoint responde con: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Test 2: Verificar health endpoint
print("Test 2: Verificando salud del servidor...")
try:
    response = requests.get(f"{API_URL}/health", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Servidor OK: {data.get('status')}")
        print(f"   Timestamp: {data.get('timestamp')}")
    else:
        print(f"⚠️  Health check: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Test 3: Simular request sin fondos_disponibles
print("Test 3: Simulando request sin fondos_disponibles...")
print("(Este test fallará con 403 por código de acceso inválido, pero nos dice si el parámetro es aceptado)")

test_data = {
    "pasaporte": "TEST123",
    "fecha_nacimiento": "1990-01-01",
    "edad": 30,
    "nacionalidad": "Mexicana",
    "pais_origen": "México",
    "ciudad_origen": "CDMX",
    "carrera_deseada": "Test",
    "especialidad": "Test",
    "nivel_espanol": "basico",
    "tipo_visa": "estudiante"
    # NOTA: NO incluye fondos_disponibles
}

try:
    response = requests.put(
        f"{API_URL}/api/estudiantes/999/completar-perfil?codigo_acceso=INVALID",
        data=test_data,
        timeout=10
    )
    
    if response.status_code == 422:
        error = response.json()
        if "fondos_disponibles" in str(error):
            print("❌ ERROR: Aún requiere fondos_disponibles")
            print(f"   Detalle: {error}")
            print()
            print("🔄 El deploy AÚN NO HA TERMINADO. Espera 2-3 minutos más.")
        else:
            print(f"⚠️  Otro error 422: {error}")
    elif response.status_code == 403:
        print("✅ FIX APLICADO! (Error 403 es esperado por código inválido)")
        print("   El servidor ya NO requiere fondos_disponibles")
        print()
        print("🎉 DEPLOY EXITOSO - Manuel ya puede completar su perfil")
    elif response.status_code == 500:
        print("⚠️  Error 500 en servidor")
        error_text = response.text[:200]
        if "fondos_disponibles" in error_text:
            print("   Causa: Aún requiere fondos_disponibles")
            print("   🔄 Deploy pendiente...")
        else:
            print(f"   Otro error: {error_text}")
    else:
        print(f"⚠️  Respuesta inesperada: {response.status_code}")
        print(f"   {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Error en request: {e}")

print()
print("=" * 60)
print("Vuelve a ejecutar este script en 2-3 minutos si el deploy")
print("aún no está completo.")
print("=" * 60)
