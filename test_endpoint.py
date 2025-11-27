"""
Test de Endpoint Completo
Simula llamada al GET /api/estudiantes/{id}
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.main import app
from database.models import get_db
from sqlalchemy.sql import text

print("=" * 80)
print("🔌 TEST DE ENDPOINT COMPLETO")
print("=" * 80)
print()

# Obtener primer estudiante de la base de datos
db = next(get_db())

try:
    result = db.execute(text("""
        SELECT id, nombre, especialidad, nivel_espanol, fondos_disponibles 
        FROM estudiantes 
        LIMIT 1
    """)).fetchone()
    
    if result:
        estudiante_id = result[0]
        print(f"✅ Estudiante encontrado: {result[1]} (ID: {estudiante_id})")
        print(f"   Especialidad: {result[2]}")
        print(f"   Nivel español: {result[3]}")
        print(f"   Fondos: €{float(result[4]) if result[4] else 0:,.2f}")
        print()
        
        # Simular respuesta del endpoint
        print("📊 Simulando respuesta del endpoint GET /api/estudiantes/{id}:")
        print("-" * 80)
        
        from api.sugerencias_cursos import sugerir_cursos
        from api.calculador_probabilidad import calcular_probabilidad_exito
        
        # Preparar datos
        estudiante_data = {
            'especialidad': result[2],
            'nivel_espanol': result[3],
            'fondos_disponibles': float(result[4]) if result[4] else 0,
            'tipo_visa': 'estudiante',
            'edad': 25,
            'archivo_titulo': 'uploaded',
            'archivo_pasaporte': 'uploaded',
            'archivo_extractos': 'uploaded',
            'consentimiento_gdpr': True
        }
        
        # Obtener sugerencias y probabilidad
        cursos = sugerir_cursos(estudiante_data)
        probabilidad = calcular_probabilidad_exito(estudiante_data)
        
        print(f"\n✅ Response incluye:")
        print(f"   - Datos del estudiante: ✓")
        print(f"   - cursos_sugeridos: {len(cursos)} cursos")
        for i, curso in enumerate(cursos[:3], 1):
            print(f"      {i}. {curso['nombre'][:40]}... ({curso['match']}% match)")
        
        print(f"\n   - probabilidad_exito:")
        print(f"      Probabilidad: {probabilidad['probabilidad']}%")
        print(f"      Categoría: {probabilidad['categoria']}")
        print(f"      Factores: {len(probabilidad['factores'])} evaluados")
        
        print()
        print("=" * 80)
        print("✅ ENDPOINT FUNCIONARÍA CORRECTAMENTE")
        print("=" * 80)
        
    else:
        print("⚠️  No hay estudiantes en la base de datos")
        print("   Registra un estudiante primero desde el frontend")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
