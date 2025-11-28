#!/usr/bin/env python3
"""
Test simple del sistema de modalidades
"""

import requests
import json

def test_simple():
    """Test simple de conexión y crear presupuesto"""
    
    print("🔍 Verificando conexión al servidor...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        print(f"✅ Servidor responde: {response.status_code}")
    except Exception as e:
        print(f"❌ No se puede conectar: {e}")
        return
    
    print("\n📝 Intentando crear presupuesto...")
    
    # Data mínima para crear presupuesto
    data = {
        "estudiante_id": 2,  # Usar un ID diferente
        "servicios_solicitados": ["gestion_basica_documentos"],
        "descripcion": "Test simple del sistema de modalidades"
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/presupuestos",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        
        print(f"📊 Status code: {response.status_code}")
        print(f"📋 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Presupuesto creado con ID: {result.get('id')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple()