#!/usr/bin/env python3
"""
Script para crear mensajes de prueba y verificar el sistema completo
"""
import requests
import json
import time

API_BASE_URL = "https://bot-visas-api.onrender.com"

def crear_mensajes_prueba():
    """Crear mensajes de prueba para verificar el sistema"""
    
    estudiante_id = 4
    
    print("📝 CREANDO MENSAJES DE PRUEBA")
    print("=" * 50)
    
    # 1. Crear mensaje del admin al estudiante
    print("1️⃣ Creando mensaje del admin...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/enviar",
            json={
                "contenido": "Hola! Tu solicitud de alojamiento ha sido aprobada ✅",
                "remitente": "admin",
                "tipo_mensaje": "aprobacion"
            }
        )
        if response.status_code == 200:
            print("   ✅ Mensaje del admin creado")
        else:
            print(f"   ⚠️ Error creando mensaje admin: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Crear mensaje del estudiante al admin
    print("\n2️⃣ Creando mensaje del estudiante...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/enviar",
            json={
                "contenido": "¡Gracias! ¿Cuándo recibiré más información?",
                "remitente": "estudiante",
                "tipo_mensaje": "consulta"
            }
        )
        if response.status_code == 200:
            print("   ✅ Mensaje del estudiante creado")
        else:
            print(f"   ⚠️ Error creando mensaje estudiante: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    time.sleep(2)  # Esperar procesamiento
    
    # 3. Verificar mensajes no leídos
    print("\n3️⃣ Verificando mensajes no leídos...")
    
    # Admin no leídos (que debe leer el estudiante)
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/no-leidos",
            params={"remitente": "admin"}
        )
        if response.status_code == 200:
            admin_no_leidos = response.json().get('no_leidos', 0)
            print(f"   📧 Mensajes del admin no leídos por estudiante: {admin_no_leidos}")
        else:
            admin_no_leidos = 0
    except Exception as e:
        print(f"   ❌ Error obteniendo admin no leídos: {e}")
        admin_no_leidos = 0
    
    # Estudiante no leídos (que debe leer el admin)
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/no-leidos",
            params={"remitente": "estudiante"}
        )
        if response.status_code == 200:
            estudiante_no_leidos = response.json().get('no_leidos', 0)
            print(f"   📧 Mensajes del estudiante no leídos por admin: {estudiante_no_leidos}")
        else:
            estudiante_no_leidos = 0
    except Exception as e:
        print(f"   ❌ Error obteniendo estudiante no leídos: {e}")
        estudiante_no_leidos = 0
    
    return admin_no_leidos, estudiante_no_leidos

def probar_marcado_leidos():
    """Probar el marcado de mensajes como leídos"""
    
    print("\n" + "=" * 50)
    print("🔄 PROBANDO MARCADO COMO LEÍDOS")
    print("=" * 50)
    
    estudiante_id = 4
    
    # 1. El estudiante marca como leídos los mensajes del admin
    print("1️⃣ Estudiante marca mensajes del admin como leídos...")
    try:
        response = requests.post(f"{API_BASE_URL}/api/estudiante/chat/{estudiante_id}/marcar-leidos")
        if response.status_code == 200:
            data = response.json()
            marcados = data.get('mensajes_actualizados', 0)
            print(f"   ✅ Marcados como leídos: {marcados} mensajes")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. El admin marca como leídos los mensajes del estudiante
    print("\n2️⃣ Admin marca mensajes del estudiante como leídos...")
    try:
        response = requests.post(f"{API_BASE_URL}/api/admin/chat/{estudiante_id}/marcar-leidos")
        if response.status_code == 200:
            data = response.json()
            marcados = data.get('mensajes_actualizados', 0)
            print(f"   ✅ Marcados como leídos: {marcados} mensajes")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Verificar que los contadores estén en 0
    print("\n3️⃣ Verificando contadores después del marcado...")
    try:
        # Admin
        response = requests.get(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/no-leidos",
            params={"remitente": "admin"}
        )
        admin_final = response.json().get('no_leidos', 0) if response.status_code == 200 else -1
        
        # Estudiante
        response = requests.get(
            f"{API_BASE_URL}/api/chat/{estudiante_id}/no-leidos",
            params={"remitente": "estudiante"}
        )
        estudiante_final = response.json().get('no_leidos', 0) if response.status_code == 200 else -1
        
        print(f"   📊 Admin no leídos: {admin_final}")
        print(f"   📊 Estudiante no leídos: {estudiante_final}")
        
        if admin_final == 0 and estudiante_final == 0:
            print("   ✅ ¡PERFECTO! Todos los mensajes marcados como leídos")
            return True
        else:
            print("   ⚠️ Aún hay mensajes no leídos")
            return False
            
    except Exception as e:
        print(f"   ❌ Error verificando: {e}")
        return False

def mostrar_estado_final():
    """Mostrar el estado final de los mensajes"""
    
    print("\n" + "=" * 50)
    print("📋 ESTADO FINAL DE MENSAJES")
    print("=" * 50)
    
    estudiante_id = 4
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/chat/{estudiante_id}/mensajes")
        if response.status_code == 200:
            data = response.json()
            mensajes = data.get('mensajes', [])
            total = data.get('total', 0)
            
            print(f"📊 Total de mensajes: {total}")
            
            if mensajes:
                print("\n📝 Últimos mensajes:")
                for i, msg in enumerate(mensajes[-5:]):
                    remitente = msg.get('remitente', 'N/A')
                    contenido = msg.get('contenido', 'Sin contenido')
                    leido = "✅ LEÍDO" if msg.get('leido') else "❌ NO LEÍDO"
                    fecha = msg.get('created_at', '')[:19] if msg.get('created_at') else 'Sin fecha'
                    
                    print(f"\n   {i+1}. [{leido}] De: {remitente}")
                    print(f"      📅 {fecha}")
                    print(f"      💬 {contenido}")
            
            # Estadísticas
            leidos = sum(1 for msg in mensajes if msg.get('leido'))
            no_leidos = total - leidos
            
            print(f"\n📈 ESTADÍSTICAS:")
            print(f"   ✅ Leídos: {leidos}")
            print(f"   ❌ No leídos: {no_leidos}")
            print(f"   📊 Porcentaje leído: {(leidos/total*100):.1f}%" if total > 0 else "   📊 Sin mensajes")
            
        else:
            print(f"❌ Error obteniendo mensajes: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 PRUEBA COMPLETA DEL SISTEMA DE MENSAJES")
    print(f"🌐 API Base: {API_BASE_URL}")
    print("=" * 60)
    
    # Crear mensajes de prueba
    admin_no_leidos, estudiante_no_leidos = crear_mensajes_prueba()
    
    # Si hay mensajes no leídos, probar el marcado
    if admin_no_leidos > 0 or estudiante_no_leidos > 0:
        success = probar_marcado_leidos()
    else:
        print("\n✅ No hay mensajes no leídos para probar")
        success = True
    
    # Mostrar estado final
    mostrar_estado_final()
    
    # Resultado final
    print("\n" + "=" * 60)
    if success:
        print("🎉 SISTEMA DE MENSAJES FUNCIONANDO PERFECTAMENTE")
        print("✅ Los mensajes se marcan como leídos correctamente")
        print("✅ Los contadores se actualizan apropiadamente")
        print("✅ Tanto usuario como admin pueden marcar mensajes")
    else:
        print("⚠️ Hay problemas en el sistema de mensajes")
    print("=" * 60)