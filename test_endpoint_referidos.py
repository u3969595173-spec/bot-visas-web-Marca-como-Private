"""
Probar endpoint de estadísticas de referidos directamente
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # URL de producción
    api_url = "https://bot-visas-web-marca-como-private.onrender.com"
    
    # ID de Leandro
    estudiante_id = 1
    
    print(f"[TEST] Probando endpoint de referidos...")
    print(f"[TEST] URL: {api_url}/api/referidos/estadisticas/{estudiante_id}")
    
    try:
        response = requests.get(f"{api_url}/api/referidos/estadisticas/{estudiante_id}")
        print(f"\n[RESPONSE] Status Code: {response.status_code}")
        print(f"[RESPONSE] Datos: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Endpoint funcionando correctamente")
            print(f"  - Código Referido: {data.get('codigo_referido')}")
            print(f"  - Crédito: {data.get('credito_disponible')}€")
            print(f"  - Total Referidos: {data.get('total_referidos')}")
            print(f"  - Total Ganado: {data.get('total_ganado')}€")
        else:
            print(f"\n❌ Error en endpoint")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
