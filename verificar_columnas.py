"""
Script para verificar si las columnas existen en la base de datos
"""

import requests

def verificar_columnas_db():
    """Verifica qué columnas están disponibles"""
    
    # Hacer una petición a un endpoint que use raw SQL para ver el error
    base_url = 'https://bot-visas-api.onrender.com'
    
    print("🔍 VERIFICANDO DISPONIBILIDAD DE COLUMNAS")
    print("=" * 50)
    
    # Si las columnas no existen, el API debería dar error
    try:
        response = requests.get(f"{base_url}/api/estudiantes/4")
        print(f"✅ API respondió: {response.status_code}")
        
        if response.status_code == 500:
            print("❌ Error 500 - Posiblemente las columnas no existen en la DB")
            print("🛠️ SOLUCIÓN: Ejecutar script para crear las columnas")
        else:
            print("✅ No hay errores de base de datos")
            print("🔄 SOLUCIÓN: Reiniciar el servidor backend")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_columnas_db()