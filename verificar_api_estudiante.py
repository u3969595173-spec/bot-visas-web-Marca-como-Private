"""
Script para verificar qué devuelve el API del estudiante
"""

import requests
import json

def verificar_respuesta_api():
    """Verifica qué está devolviendo el API para el estudiante"""
    
    # URL del API
    base_url = 'https://bot-visas-api.onrender.com'
    estudiante_id = 4  # El estudiante que vimos en los logs
    
    print("🔍 VERIFICANDO RESPUESTA DEL API")
    print("=" * 50)
    
    try:
        # Hacer petición al endpoint del estudiante
        response = requests.get(f"{base_url}/api/estudiantes/{estudiante_id}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ API respondió correctamente para estudiante {estudiante_id}")
            print("\n🔍 Estados de aprobación:")
            print(f"   estado_patrocinio: {data.get('estado_patrocinio', 'NO ENCONTRADO')}")
            print(f"   estado_alojamiento: {data.get('estado_alojamiento', 'NO ENCONTRADO')}")
            print(f"   estado_seguro_medico: {data.get('estado_seguro_medico', 'NO ENCONTRADO')}")
            
            print("\n💬 Comentarios del admin:")
            print(f"   comentarios_patrocinio: {data.get('comentarios_patrocinio', 'NO ENCONTRADO')}")
            print(f"   comentarios_alojamiento: {data.get('comentarios_alojamiento', 'NO ENCONTRADO')}")
            print(f"   comentarios_seguro_medico: {data.get('comentarios_seguro_medico', 'NO ENCONTRADO')}")
            
            print("\n🎯 Solicitudes activas:")
            print(f"   patrocinio_solicitado: {data.get('patrocinio_solicitado', 'NO ENCONTRADO')}")
            print(f"   gestion_alojamiento_solicitada: {data.get('gestion_alojamiento_solicitada', 'NO ENCONTRADO')}")
            print(f"   gestion_seguro_solicitada: {data.get('gestion_seguro_solicitada', 'NO ENCONTRADO')}")
            
            # Guardar respuesta completa para debugging
            with open('respuesta_api_estudiante.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"\n📁 Respuesta completa guardada en: respuesta_api_estudiante.json")
            
            # Verificar si hay algún campo con estado aprobado
            estados_aprobados = []
            if data.get('estado_patrocinio') == 'aprobado':
                estados_aprobados.append('Patrocinio')
            if data.get('estado_alojamiento') == 'aprobado':
                estados_aprobados.append('Alojamiento')
            if data.get('estado_seguro_medico') == 'aprobado':
                estados_aprobados.append('Seguro Médico')
            
            if estados_aprobados:
                print(f"\n✅ ESTADOS APROBADOS ENCONTRADOS: {', '.join(estados_aprobados)}")
                print("   ➡️ El frontend debería mostrar estos como APROBADO")
            else:
                print(f"\n❌ PROBLEMA: No se encontraron estados aprobados")
                print("   ➡️ Por eso el frontend sigue mostrando formularios")
                
        else:
            print(f"❌ Error en API: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    verificar_respuesta_api()