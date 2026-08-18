#!/usr/bin/env python3
"""
Script de prueba para el sistema de retiros e inversiones
Prueba el flujo completo: solicitar -> obtener -> aprobar
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"

# Tokens de prueba (cambiar según tu setup)
ADMIN_TOKEN = None  # Se obtiene del login
ESTUDIANTE_TOKEN = None

def login_admin():
    """Login como administrador"""
    print("\n🔐 Intentando login como admin...")
    response = requests.post(f"{API_URL}/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    if response.status_code == 200:
        data = response.json()
        global ADMIN_TOKEN
        ADMIN_TOKEN = data.get('access_token')
        print(f"✅ Login admin exitoso. Token: {ADMIN_TOKEN[:20]}...")
        return ADMIN_TOKEN
    else:
        print(f"❌ Error login admin: {response.status_code}")
        print(f"   {response.text}")
        return None

def obtener_solicitudes_credito():
    """Obtener todas las solicitudes de crédito"""
    print("\n📋 Obteniendo solicitudes de crédito...")
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"} if ADMIN_TOKEN else {}
    
    response = requests.get(
        f"{API_URL}/api/admin/solicitudes-credito",
        headers=headers
    )
    
    if response.status_code == 200:
        solicitudes = response.json()
        print(f"✅ Solicitudes obtenidas: {len(solicitudes)}")
        
        for sol in solicitudes[:5]:  # Mostrar primeras 5
            print(f"\n  ID: {sol['id']}")
            print(f"  Usuario: {sol['nombre']} ({sol['email']})")
            print(f"  Tipo: {sol['beneficiario_tipo']}")
            print(f"  Monto: {sol['monto']}€")
            print(f"  Estado: {sol['estado']}")
            print(f"  Crédito disponible: {sol['credito_disponible']}€")
        
        return solicitudes
    else:
        print(f"❌ Error obteniendo solicitudes: {response.status_code}")
        print(f"   {response.text}")
        return []

def crear_solicitud_retiro_estudiante(estudiante_id, monto):
    """Crear solicitud de retiro para estudiante"""
    print(f"\n💰 Creando solicitud de retiro para estudiante {estudiante_id}...")
    
    response = requests.post(
        f"{API_URL}/api/referidos/solicitar-uso",
        json={"tipo": "retiro", "monto": monto}
    )
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✅ Solicitud creada exitosamente")
        print(f"   {data}")
        return data
    else:
        print(f"❌ Error creando solicitud: {response.status_code}")
        print(f"   {response.text}")
        return None

def aprobar_solicitud_retiro(solicitud_id, notas=""):
    """Aprobar una solicitud de retiro"""
    print(f"\n✅ Aprobando solicitud {solicitud_id}...")
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"} if ADMIN_TOKEN else {}
    
    response = requests.put(
        f"{API_URL}/api/admin/solicitudes-credito/{solicitud_id}/responder",
        headers=headers,
        json={"accion": "aprobar", "notas": notas}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Solicitud aprobada")
        print(f"   {data}")
        return data
    else:
        print(f"❌ Error aprobando solicitud: {response.status_code}")
        print(f"   {response.text}")
        return None

def rechazar_solicitud_retiro(solicitud_id, notas=""):
    """Rechazar una solicitud de retiro"""
    print(f"\n❌ Rechazando solicitud {solicitud_id}...")
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"} if ADMIN_TOKEN else {}
    
    response = requests.put(
        f"{API_URL}/api/admin/solicitudes-credito/{solicitud_id}/responder",
        headers=headers,
        json={"accion": "rechazar", "notas": notas}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Solicitud rechazada")
        print(f"   {data}")
        return data
    else:
        print(f"❌ Error rechazando solicitud: {response.status_code}")
        print(f"   {response.text}")
        return None

def main():
    print("=" * 60)
    print("🎯 PRUEBA DEL SISTEMA DE RETIROS E INVERSIONES")
    print("=" * 60)
    
    # 1. Login
    if not login_admin():
        print("\n⚠️  No se pudo hacer login. Las pruebas sin token pueden fallar.")
    
    # 2. Obtener solicitudes
    solicitudes = obtener_solicitudes_credito()
    
    if solicitudes:
        # 3. Probar aprobación de primera solicitud pendiente
        pendientes = [s for s in solicitudes if s['estado'].lower() == 'pendiente']
        if pendientes:
            print("\n" + "=" * 60)
            print("APROBANDO SOLICITUD DE PRUEBA")
            print("=" * 60)
            primera = pendientes[0]
            print(f"\nSolicitud a aprobar:")
            print(f"  ID: {primera['id']}")
            print(f"  Usuario: {primera['nombre']}")
            print(f"  Monto: {primera['monto']}€")
            
            respuesta = input("\n¿Deseas aprobar esta solicitud? (s/n): ")
            if respuesta.lower() == 's':
                aprobar_solicitud_retiro(
                    primera['id'],
                    f"Aprobado automáticamente por prueba - {datetime.now().isoformat()}"
                )
        else:
            print("\n⚠️  No hay solicitudes pendientes para probar")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    main()
