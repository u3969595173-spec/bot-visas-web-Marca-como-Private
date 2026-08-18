#!/usr/bin/env python3
"""
SCRIPT DE PRUEBA COMPLETO - Verificar que todos los endpoints funcionan
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000"
ADMIN_USER = os.getenv('ADMIN_USUARIO', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASSWORD', '')

print("=" * 80)
print("🧪 PRUEBA COMPLETA - CAPITAL TRADE IBERIA")
print("=" * 80)

# ============================================================================
# 1. LOGIN ADMIN
# ============================================================================
print("\n1️⃣ LOGIN ADMIN")
print("-" * 80)

try:
    response = requests.post(f"{API_URL}/api/admin/login", json={
        "usuario": ADMIN_USER,
        "password": ADMIN_PASS
    })
    
    if response.status_code == 200:
        admin_token = response.json()['token']
        print("✅ Login admin exitoso")
        print(f"   Token: {admin_token[:50]}...")
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(f"   {response.text}")
        admin_token = None
except Exception as e:
    print(f"❌ Excepción: {e}")
    admin_token = None

# ============================================================================
# 2. REGISTRO E INVERSOR
# ============================================================================
print("\n2️⃣ REGISTRO DE INVERSOR")
print("-" * 80)

if admin_token:
    try:
        response = requests.post(f"{API_URL}/api/inversores/registro", json={
            "nombre": f"Test Inversor {int(__import__('time').time())}",
            "email": f"test{int(__import__('time').time())}@example.com",
            "password": "Password123!",
            "telefono": "+34 666 777 888",
            "pais": "España"
        })
        
        if response.status_code in [200, 201]:
            inversor_data = response.json()
            print("✅ Registro inversor exitoso")
            print(f"   ID: {inversor_data.get('inversor_id')}")
            print(f"   Email: {inversor_data.get('email')}")
            inversor_id = inversor_data.get('inversor_id')
            inversor_email = inversor_data.get('email')
        else:
            print(f"❌ Error en registro: {response.status_code}")
            print(f"   {response.text}")
            inversor_id = None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        inversor_id = None
else:
    print("⏭️ Saltando (no hay token admin)")
    inversor_id = None

# ============================================================================
# 3. LOGIN INVERSOR
# ============================================================================
print("\n3️⃣ LOGIN INVERSOR")
print("-" * 80)

if inversor_id:
    try:
        response = requests.post(f"{API_URL}/api/inversores/login", json={
            "email": inversor_email,
            "password": "Password123!"
        })
        
        if response.status_code == 200:
            inversor_token = response.json()['token']
            print("✅ Login inversor exitoso")
            print(f"   Token: {inversor_token[:50]}...")
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   {response.text}")
            inversor_token = None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        inversor_token = None
else:
    print("⏭️ Saltando (no hay inversor registrado)")
    inversor_token = None

# ============================================================================
# 4. CREAR APORTACIÓN (desde inversor)
# ============================================================================
print("\n4️⃣ CREAR APORTACIÓN")
print("-" * 80)

if inversor_token and inversor_id:
    try:
        response = requests.post(f"{API_URL}/api/aportaciones", 
            headers={"Authorization": f"Bearer {inversor_token}"},
            json={
                "inversor_id": inversor_id,
                "nombre": "Test Inversor",
                "email": inversor_email,
                "importe": 5000.00,
                "moneda": "EUR",
                "estado": "Pendiente de validación"
            }
        )
        
        if response.status_code in [200, 201]:
            aportacion_data = response.json()
            print("✅ Aportación creada")
            print(f"   ID: {aportacion_data.get('id')}")
            print(f"   Monto: €{aportacion_data.get('importe')}")
            aportacion_id = aportacion_data.get('id')
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            aportacion_id = None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        aportacion_id = None
else:
    print("⏭️ Saltando (no hay token inversor)")
    aportacion_id = None

# ============================================================================
# 5. VALIDAR APORTACIÓN (desde admin)
# ============================================================================
print("\n5️⃣ VALIDAR APORTACIÓN (Admin)")
print("-" * 80)

if admin_token and aportacion_id:
    try:
        response = requests.put(f"{API_URL}/api/aportaciones/{aportacion_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"estado": "Activa"}
        )
        
        if response.status_code == 200:
            print("✅ Aportación validada")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Excepción: {e}")
else:
    print("⏭️ Saltando (no hay aportación)")

# ============================================================================
# 6. CREAR RETIRO (desde inversor)
# ============================================================================
print("\n6️⃣ CREAR RETIRO")
print("-" * 80)

if inversor_token and inversor_id:
    try:
        response = requests.post(f"{API_URL}/api/retiros",
            headers={"Authorization": f"Bearer {inversor_token}"},
            json={
                "inversor_id": inversor_id,
                "nombre": "Test Inversor",
                "email": inversor_email,
                "importe": 1000.00,
                "moneda": "EUR",
                "estado": "Pendiente de validación"
            }
        )
        
        if response.status_code in [200, 201]:
            retiro_data = response.json()
            print("✅ Retiro creado")
            print(f"   ID: {retiro_data.get('id')}")
            print(f"   Monto: €{retiro_data.get('importe')}")
            retiro_id = retiro_data.get('id')
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            retiro_id = None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        retiro_id = None
else:
    print("⏭️ Saltando")
    retiro_id = None

# ============================================================================
# 7. VALIDAR RETIRO (desde admin)
# ============================================================================
print("\n7️⃣ VALIDAR RETIRO (Admin)")
print("-" * 80)

if admin_token and retiro_id:
    try:
        response = requests.put(f"{API_URL}/api/retiros/{retiro_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"estado": "Aprobado"}
        )
        
        if response.status_code == 200:
            print("✅ Retiro validado")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Excepción: {e}")
else:
    print("⏭️ Saltando")

# ============================================================================
# 8. OBTENER CONFIGURACIÓN (desde admin)
# ============================================================================
print("\n8️⃣ OBTENER CONFIGURACIÓN")
print("-" * 80)

if admin_token:
    try:
        response = requests.get(f"{API_URL}/api/admin/config",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if response.status_code == 200:
            config = response.json()
            print("✅ Config obtenida")
            print(f"   Minimos: {config.get('minimos')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Excepción: {e}")
else:
    print("⏭️ Saltando")

# ============================================================================
# 9. OBTENER APORTACIONES (desde admin)
# ============================================================================
print("\n9️⃣ OBTENER APORTACIONES (Admin)")
print("-" * 80)

if admin_token:
    try:
        response = requests.get(f"{API_URL}/api/aportaciones",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            aportaciones = data.get('aportaciones', [])
            print(f"✅ Total de aportaciones: {len(aportaciones)}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Excepción: {e}")
else:
    print("⏭️ Saltando")

# ============================================================================
# 10. ENVIAR MENSAJE (chat comunidad)
# ============================================================================
print("\n🔟 ENVIAR MENSAJE CHAT")
print("-" * 80)

if inversor_token:
    try:
        response = requests.post(f"{API_URL}/api/comunidad/mensajes",
            headers={"Authorization": f"Bearer {inversor_token}"},
            json={"mensaje": "Mensaje de prueba desde inversor"}
        )
        
        if response.status_code in [200, 201]:
            print("✅ Mensaje enviado")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Excepción: {e}")
else:
    print("⏭️ Saltando")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 80)
print("✅ PRUEBA COMPLETA FINALIZADA")
print("=" * 80)
print("\n✅ Si todos los pasos están verde, TODO FUNCIONA AL 100%")
print("❌ Si hay rojos, revisar los errores mostrados arriba")
print("\n")
