#!/usr/bin/env python3
"""
Script para despertar la base de datos en Render
Ejecutar antes de mostrar la web a usuarios
"""
import requests
import time

API_URL = "https://bot-visas-api.onrender.com"

def wake_database():
    """Despertar la base de datos haciendo una petición simple"""
    print("🔄 Despertando base de datos...")
    
    try:
        # Hacer petición al health check
        response = requests.get(f"{API_URL}/health", timeout=60)
        
        if response.status_code == 200:
            print("✅ Base de datos activa y funcionando")
            print(f"   Respuesta: {response.json()}")
            return True
        else:
            print(f"⚠️ Base de datos respondió con código {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - la base de datos está despertando (tarda ~30-60 segundos)")
        print("   Esperando 30 segundos más...")
        time.sleep(30)
        return wake_database()  # Reintentar
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("WAKE DB - Despertar Base de Datos Render")
    print("=" * 50)
    
    wake_database()
    
    print("\n🎉 Listo! La base de datos está despierta.")
    print("   Los usuarios ahora pueden registrarse sin problemas.")
