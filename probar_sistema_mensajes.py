#!/usr/bin/env python3
"""
Script para probar y arreglar el sistema de mensajes no leídos
"""
import requests
import json

API_BASE_URL = "https://bot-visas-api.onrender.com"

def probar_sistema_mensajes():
    """Probar el sistema completo de mensajes y marcado como leído"""
    
    estudiante_id = 4  # El estudiante de prueba
    
    print("💬 PROBANDO SISTEMA DE MENSAJES")
    print("=" * 50)
    
    # 1. Verificar mensajes no leídos del admin (que el estudiante debe leer)
    print("1️⃣ Verificando mensajes del admin no leídos por estudiante...")
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/no-leidos",
            params={"remitente": "admin"}
        )
        if response.status_code == 200:
            data = response.json()
            admin_no_leidos = data.get('no_leidos', 0)
            print(f"   Mensajes del admin no leídos: {admin_no_leidos}")
        else:
            print(f"   ❌ Error obteniendo mensajes del admin: {response.status_code}")
            admin_no_leidos = 0
    except Exception as e:
        print(f"   ❌ Error: {e}")
        admin_no_leidos = 0
    
    # 2. Verificar mensajes no leídos del estudiante (que el admin debe leer)
    print("\n2️⃣ Verificando mensajes del estudiante no leídos por admin...")
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/no-leidos",
            params={"remitente": "estudiante"}
        )
        if response.status_code == 200:
            data = response.json()
            estudiante_no_leidos = data.get('no_leidos', 0)
            print(f"   Mensajes del estudiante no leídos: {estudiante_no_leidos}")
        else:
            print(f"   ❌ Error obteniendo mensajes del estudiante: {response.status_code}")
            estudiante_no_leidos = 0
    except Exception as e:
        print(f"   ❌ Error: {e}")
        estudiante_no_leidos = 0
    
    # 3. Obtener lista de mensajes para ver el estado
    print("\n3️⃣ Obteniendo lista de mensajes...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/chat/{estudiante_id}/mensajes")
        if response.status_code == 200:
            data = response.json()
            mensajes = data.get('mensajes', [])
            print(f"   Total de mensajes: {len(mensajes)}")
            
            if mensajes:
                print("   📋 Últimos 5 mensajes:")
                for i, msg in enumerate(mensajes[-5:]):
                    remitente = msg.get('remitente', 'N/A')
                    contenido = msg.get('contenido', 'Sin contenido')[:30]
                    leido = "✅ LEÍDO" if msg.get('leido') else "❌ NO LEÍDO"
                    fecha = msg.get('created_at', '')[:16] if msg.get('created_at') else 'Sin fecha'
                    
                    print(f"      {i+1}. [{leido}] {remitente}: {contenido}...")
                    print(f"         📅 {fecha}")
        else:
            print(f"   ❌ Error obteniendo lista: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Probar marcar mensajes como leídos
    if admin_no_leidos > 0:
        print(f"\n4️⃣ Probando marcar {admin_no_leidos} mensajes del admin como leídos...")
        try:
            response = requests.post(f"{API_BASE_URL}/api/estudiante/chat/{estudiante_id}/marcar-leidos")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Marcados como leídos: {data.get('mensajes_actualizados', 0)}")
            else:
                print(f"   ❌ Error marcando como leídos: {response.status_code}")
                print(f"   Respuesta: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    if estudiante_no_leidos > 0:
        print(f"\n5️⃣ Probando marcar {estudiante_no_leidos} mensajes del estudiante como leídos...")
        try:
            response = requests.post(f"{API_BASE_URL}/api/admin/chat/{estudiante_id}/marcar-leidos")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Marcados como leídos: {data.get('mensajes_actualizados', 0)}")
            else:
                print(f"   ❌ Error marcando como leídos: {response.status_code}")
                print(f"   Respuesta: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # 6. Verificar después del marcado
    print("\n6️⃣ Verificando contadores después del marcado...")
    try:
        # Mensajes del admin
        response = requests.get(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/no-leidos",
            params={"remitente": "admin"}
        )
        if response.status_code == 200:
            data = response.json()
            admin_despues = data.get('no_leidos', 0)
            print(f"   Mensajes del admin no leídos: {admin_despues}")
        
        # Mensajes del estudiante  
        response = requests.get(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/no-leidos",
            params={"remitente": "estudiante"}
        )
        if response.status_code == 200:
            data = response.json()
            estudiante_despues = data.get('no_leidos', 0)
            print(f"   Mensajes del estudiante no leídos: {estudiante_despues}")
            
    except Exception as e:
        print(f"   ❌ Error verificando: {e}")

def verificar_endpoints_disponibles():
    """Verificar qué endpoints están disponibles"""
    
    estudiante_id = 4
    
    print("\n" + "=" * 60)
    print("🔍 VERIFICANDO ENDPOINTS DE CHAT")
    print("=" * 60)
    
    endpoints = [
        ("GET", f"/api/chat/{estudiante_id}/mensajes", "Listar mensajes"),
        ("GET", f"/api/chat/{estudiante_id}/no-leidos?remitente=admin", "Contar no leídos del admin"),
        ("GET", f"/api/chat/{estudiante_id}/no-leidos?remitente=estudiante", "Contar no leídos del estudiante"),
        ("POST", f"/api/estudiante/chat/{estudiante_id}/marcar-leidos", "Estudiante marca leídos"),
        ("POST", f"/api/admin/chat/{estudiante_id}/marcar-leidos", "Admin marca leídos"),
        ("POST", f"/api/chat/{estudiante_id}/marcar-todos-leidos?remitente=admin", "Marcar todos del admin"),
        ("POST", f"/api/chat/{estudiante_id}/marcar-todos-leidos?remitente=estudiante", "Marcar todos del estudiante"),
    ]
    
    for metodo, endpoint, descripcion in endpoints:
        try:
            if metodo == "GET":
                response = requests.get(f"{API_BASE_URL}{endpoint}")
            else:  # POST
                response = requests.post(f"{API_BASE_URL}{endpoint}")
            
            status_icon = "✅" if response.status_code in [200, 201] else "❌"
            print(f"{status_icon} {metodo} {endpoint}")
            print(f"   📝 {descripcion}")
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        keys = list(data.keys())[:3]  # Primeras 3 claves
                        print(f"   🔑 Campos: {', '.join(keys)}...")
                except:
                    pass
            else:
                error_text = response.text[:50]
                print(f"   ❌ Error: {error_text}...")
            print()
            
        except Exception as e:
            print(f"❌ {metodo} {endpoint}")
            print(f"   ❌ Error de conexión: {e}")
            print()

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO DE SISTEMA DE MENSAJES")
    print(f"🌐 API Base: {API_BASE_URL}")
    
    # Verificar endpoints disponibles
    verificar_endpoints_disponibles()
    
    # Probar sistema de mensajes
    probar_sistema_mensajes()
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("=" * 60)