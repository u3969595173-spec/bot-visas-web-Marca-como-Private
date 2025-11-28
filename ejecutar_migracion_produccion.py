#!/usr/bin/env python3
"""
Script para ejecutar la migración de base de datos en producción
"""
import requests
import json

# URL de tu API en producción
API_BASE_URL = "https://bot-visas-api.onrender.com"

def ejecutar_migracion():
    """Ejecutar la migración de columnas en producción"""
    
    print("🔧 Ejecutando migración de base de datos en producción...")
    print(f"URL: {API_BASE_URL}/api/admin/fix-database-columns")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/admin/fix-database-columns",
            timeout=60  # Mayor timeout para operaciones de DB
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ MIGRACIÓN COMPLETADA")
            print(f"Columnas agregadas: {data.get('columnas_agregadas', 0)}")
            print(f"Columnas existentes: {data.get('columnas_existentes', 0)}")
            print(f"Errores: {data.get('errores', 0)}")
            
            print("\n📋 DETALLES:")
            for detalle in data.get('detalles', []):
                print(f"  {detalle}")
            
            return True
            
        else:
            print(f"❌ Error en migración: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 EJECUTANDO MIGRACIÓN DE BASE DE DATOS")
    print("=" * 60)
    
    success = ejecutar_migracion()
    
    if success:
        print("\n✅ Migración completada. Probando API...")
        
        # Probar si ahora funciona el endpoint de estudiantes
        try:
            test_response = requests.get(f"{API_BASE_URL}/api/estudiantes/1")
            if test_response.status_code == 200:
                data = test_response.json()
                print("✅ API funciona correctamente después de migración")
                print("Campos de aprobación encontrados:")
                
                campos_aprobacion = [
                    'estado_patrocinio', 'comentarios_patrocinio',
                    'estado_alojamiento', 'comentarios_alojamiento', 
                    'estado_seguro_medico', 'comentarios_seguro_medico'
                ]
                
                for campo in campos_aprobacion:
                    valor = data.get(campo, "NO ENCONTRADO")
                    print(f"  {campo}: {valor}")
                    
            else:
                print(f"⚠️ API aún reporta error: {test_response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Error probando API: {e}")
    
    print("\n" + "=" * 60)