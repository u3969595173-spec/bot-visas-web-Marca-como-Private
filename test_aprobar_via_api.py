"""
Script para aprobar solicitudes usando el API directamente
Esto funcionará con el sistema en producción
"""

import requests
import os

def aprobar_solicitudes_via_api():
    """Aprueba solicitudes usando el API para probar el sistema"""
    
    # URL del API (usar la URL de producción si es necesario)
    base_url = os.getenv('API_URL', 'https://bot-visas-api.onrender.com')
    
    print("🧪 APROBANDO SOLICITUDES VIA API PARA PRUEBA")
    print("=" * 50)
    
    # Datos de prueba - ajustar según tu sistema
    estudiante_id = 4  # El estudiante que vi en los logs
    
    try:
        # 1. Aprobar solicitud de patrocinio/financiera
        print("1. Aprobando solicitud de patrocinio...")
        response = requests.put(
            f"{base_url}/api/admin/gestionar-patrocinio/{estudiante_id}",
            json={
                "accion": "aprobar",
                "comentarios": "Solicitud aprobada para prueba del sistema de notificaciones. Los fondos son suficientes para la estancia."
            }
        )
        if response.status_code == 200:
            print("✅ Patrocinio aprobado exitosamente")
        else:
            print(f"❌ Error aprobando patrocinio: {response.status_code} - {response.text}")
        
        # 2. Aprobar solicitud de alojamiento (si existe)
        print("2. Aprobando solicitud de alojamiento...")
        response = requests.put(
            f"{base_url}/api/admin/gestionar-alojamiento/{estudiante_id}",
            json={
                "accion": "aprobar", 
                "comentarios": "Solicitud aprobada para prueba. Te ayudaremos a encontrar el mejor alojamiento para tu estancia."
            }
        )
        if response.status_code == 200:
            print("✅ Alojamiento aprobado exitosamente")
        else:
            print(f"❌ Error aprobando alojamiento: {response.status_code} - {response.text}")
        
        # 3. Aprobar solicitud de seguro médico (si existe)
        print("3. Aprobando solicitud de seguro médico...")
        response = requests.put(
            f"{base_url}/api/admin/gestionar-seguro-medico/{estudiante_id}",
            json={
                "accion": "aprobar",
                "comentarios": "Solicitud aprobada para prueba. Te contactaremos con las opciones de seguro médico disponibles en las próximas 24 horas."
            }
        )
        if response.status_code == 200:
            print("✅ Seguro médico aprobado exitosamente")
        else:
            print(f"❌ Error aprobando seguro médico: {response.status_code} - {response.text}")
        
        print(f"\n🎯 AHORA PRUEBA:")
        print(f"   1. Ve al panel del estudiante ID {estudiante_id}")
        print(f"   2. Ve a las secciones de Información Financiera, Alojamiento y Seguro Médico")
        print(f"   3. Deberías ver los estados APROBADO en lugar del formulario")
        print(f"   4. También deberías ver los comentarios del admin")
        print(f"   5. Debería aparecer campanita con notificaciones")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    aprobar_solicitudes_via_api()