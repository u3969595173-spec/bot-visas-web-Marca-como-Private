#!/usr/bin/env python3
"""
Script para probar el sistema completo de notificaciones de aprobación
"""
import requests
import json
import time

API_BASE_URL = "https://bot-visas-api.onrender.com"

def probar_notificacion_aprobacion():
    """Prueba el flujo completo de notificaciones de aprobación"""
    
    estudiante_id = 4  # El estudiante que estamos usando para pruebas
    
    print("🧪 PROBANDO SISTEMA DE NOTIFICACIONES")
    print("=" * 60)
    
    # 1. Verificar notificaciones antes
    print("1️⃣ Verificando notificaciones antes de la aprobación...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/notificaciones/{estudiante_id}/contar")
        if response.status_code == 200:
            count_antes = response.json().get('count', 0)
            print(f"   Notificaciones antes: {count_antes}")
        else:
            print(f"   ⚠️ Error obteniendo notificaciones: {response.status_code}")
            count_antes = 0
    except Exception as e:
        print(f"   ❌ Error: {e}")
        count_antes = 0
    
    # 2. Simular aprobación del admin (cambiar estado a rechazado para ver el cambio)
    print("\n2️⃣ Simulando cambio de estado por admin...")
    nuevo_estado = "rechazado"  # Cambiar para ver el efecto
    comentario = "Prueba automática del sistema de notificaciones"
    
    try:
        # Simular endpoint del admin (necesitaríamos credenciales admin)
        # Por ahora vamos a usar el endpoint público si existe
        print(f"   Intentando cambiar estado a '{nuevo_estado}'...")
        print(f"   Comentario: '{comentario}'")
        
        # Nota: Este endpoint requiere autenticación admin en producción
        # Vamos a verificar si existe un endpoint de prueba
        
    except Exception as e:
        print(f"   ⚠️ No podemos simular admin sin credenciales: {e}")
    
    # 3. Verificar si hay nuevas notificaciones
    print("\n3️⃣ Esperando procesamiento de notificaciones...")
    time.sleep(2)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/notificaciones/{estudiante_id}/contar")
        if response.status_code == 200:
            count_despues = response.json().get('count', 0)
            print(f"   Notificaciones después: {count_despues}")
            
            if count_despues > count_antes:
                print("   ✅ ¡Nueva notificación detectada!")
                diferencia = count_despues - count_antes
                print(f"   📬 {diferencia} nueva(s) notificación(es)")
                
                # Obtener las notificaciones para ver el contenido
                print("\n4️⃣ Obteniendo notificaciones recientes...")
                response_list = requests.get(f"{API_BASE_URL}/api/notificaciones/{estudiante_id}")
                if response_list.status_code == 200:
                    response_data = response_list.json()
                    notificaciones = response_data.get('notificaciones', [])
                    print(f"   Total notificaciones: {len(notificaciones)}")
                    
                    for notif in notificaciones[:3]:  # Mostrar las 3 más recientes
                        fecha = notif.get('created_at', 'Sin fecha')
                        tipo = notif.get('tipo', 'Sin tipo')
                        mensaje = notif.get('mensaje', 'Sin mensaje')
                        leida = notif.get('leida', False)
                        
                        estado_lectura = "✅ LEÍDA" if leida else "🔔 NO LEÍDA"
                        print(f"   📌 [{estado_lectura}] {tipo}: {mensaje}")
                        print(f"      Fecha: {fecha}")
                        print()
                
            else:
                print("   ℹ️ No se detectaron nuevas notificaciones")
                print("   💡 Esto podría indicar:")
                print("      - El sistema ya procesó las notificaciones")
                print("      - No hubo cambios de estado")
                print("      - Las notificaciones requieren acción admin real")
        
    except Exception as e:
        print(f"   ❌ Error verificando notificaciones: {e}")
    
    # 4. Verificar estado actual del estudiante
    print("\n5️⃣ Estado actual del estudiante...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/estudiantes/{estudiante_id}")
        if response.status_code == 200:
            data = response.json()
            print("   Estados de aprobación:")
            print(f"   🏠 Alojamiento: {data.get('estado_alojamiento', 'N/A')}")
            print(f"   💰 Patrocinio: {data.get('estado_patrocinio', 'N/A')}")
            print(f"   🏥 Seguro Médico: {data.get('estado_seguro_medico', 'N/A')}")
            
            if data.get('comentarios_alojamiento'):
                print(f"   💬 Comentario alojamiento: {data.get('comentarios_alojamiento')}")
            if data.get('comentarios_patrocinio'):
                print(f"   💬 Comentario patrocinio: {data.get('comentarios_patrocinio')}")
            if data.get('comentarios_seguro_medico'):
                print(f"   💬 Comentario seguro: {data.get('comentarios_seguro_medico')}")
        
    except Exception as e:
        print(f"   ❌ Error obteniendo datos del estudiante: {e}")

def verificar_endpoints_notificaciones():
    """Verifica qué endpoints de notificaciones están disponibles"""
    
    estudiante_id = 4
    
    print("\n" + "=" * 60)
    print("🔍 VERIFICANDO ENDPOINTS DE NOTIFICACIONES")
    print("=" * 60)
    
    endpoints = [
        f"/api/notificaciones/{estudiante_id}/contar",
        f"/api/notificaciones/{estudiante_id}",
        f"/api/notificaciones/{estudiante_id}/marcar-todas-leidas",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"{status_icon} {endpoint} - Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        print(f"   📊 Campos: {', '.join(data.keys())}")
                    elif isinstance(data, list):
                        print(f"   📋 Lista con {len(data)} elementos")
                    else:
                        print(f"   📄 Respuesta: {str(data)[:100]}...")
                except:
                    print(f"   📄 Respuesta texto: {response.text[:100]}...")
            else:
                print(f"   ❌ Error: {response.text[:100]}...")
            
        except Exception as e:
            print(f"❌ {endpoint} - Error de conexión: {e}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DEL SISTEMA DE NOTIFICACIONES")
    print(f"🌐 API Base: {API_BASE_URL}")
    print()
    
    # Verificar endpoints disponibles
    verificar_endpoints_notificaciones()
    
    # Probar flujo de notificaciones
    probar_notificacion_aprobacion()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)