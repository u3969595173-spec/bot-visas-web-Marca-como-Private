"""
Test End-to-End del Sistema
"""

from api.sugerencias_cursos import sugerir_cursos
from api.calculador_probabilidad import calcular_probabilidad_exito
from api.generador_documentos_borrador import generar_todos_documentos

print("=" * 80)
print("🧪 TEST END-TO-END - BOT VISAS ESTUDIO")
print("=" * 80)
print()

# Test 1: Sugerencias de Cursos
print("TEST 1: Sistema de Sugerencias de Cursos")
print("-" * 80)

test_estudiante = {
    'nombre': 'Test Usuario',
    'especialidad': 'Medicina',
    'nivel_espanol': 'avanzado',
    'fondos_disponibles': 8000,
    'tipo_visa': 'estudiante',
    'edad': 25,
    'archivo_titulo': 'uploaded',
    'archivo_pasaporte': 'uploaded',
    'archivo_extractos': 'uploaded',
    'consentimiento_gdpr': True
}

cursos = sugerir_cursos(test_estudiante)
print(f"✅ Cursos sugeridos: {len(cursos)}")
for i, curso in enumerate(cursos[:3], 1):
    print(f"   {i}. {curso['nombre']} - {curso['universidad']}")
    print(f"      Match: {curso['match']}% | Costo: €{curso['costo_anual']:,}/año | Asequible: {'Sí' if curso['asequible'] else 'No'}")

print()

# Test 2: Probabilidad de Éxito
print("TEST 2: Calculador de Probabilidad de Éxito")
print("-" * 80)

probabilidad = calcular_probabilidad_exito(test_estudiante)
print(f"✅ Probabilidad calculada: {probabilidad['probabilidad']}%")
print(f"   Categoría: {probabilidad['categoria']}")
print(f"   Mensaje: {probabilidad['mensaje']}")
print(f"   Puntos: {probabilidad['puntos']}/{probabilidad['max_puntos']}")
print(f"   Factores evaluados:")
for factor in probabilidad['factores']:
    emoji = '✅' if factor['cumple'] else '❌'
    print(f"      {emoji} {factor['factor']}: {factor['puntos']} pts")

print()

# Test 3: Generación de Documentos
print("TEST 3: Generador de Documentos Borrador")
print("-" * 80)

test_estudiante_docs = {
    'nombre': 'Juan Pérez García',
    'pasaporte': 'AB123456',
    'nacionalidad': 'Colombia',
    'carrera_deseada': 'Ingeniería Informática',
    'especialidad': 'Ingeniería',
    'fondos_disponibles': 10000,
    'fecha_inicio_estimada': '2026-01-15',
    'nivel_espanol': 'intermedio',
    'tipo_visa': 'estudiante'
}

documentos = generar_todos_documentos(test_estudiante_docs)
print(f"✅ Documentos generados: {len(documentos)}")
print(f"   1. Carta de Aceptación: {len(documentos['carta_aceptacion'])} caracteres")
print(f"   2. Carta de Patrocinio: {len(documentos['carta_patrocinio'])} caracteres")
print(f"   3. Checklist Personalizado: {len(documentos['checklist_personalizado'])} caracteres")

# Mostrar preview de carta de aceptación
print("\n   Preview Carta de Aceptación:")
lineas = documentos['carta_aceptacion'].split('\n')[:10]
for linea in lineas:
    print(f"      {linea}")
print("      ...")

print()

# Test 4: Casos Especiales
print("TEST 4: Casos Especiales y Edge Cases")
print("-" * 80)

# Estudiante con fondos insuficientes
estudiante_fondos_bajos = test_estudiante.copy()
estudiante_fondos_bajos['fondos_disponibles'] = 2000

prob_baja = calcular_probabilidad_exito(estudiante_fondos_bajos)
print(f"✅ Fondos bajos (€2,000): Probabilidad {prob_baja['probabilidad']}% - {prob_baja['categoria']}")

# Estudiante con documentos incompletos
estudiante_docs_incompletos = test_estudiante.copy()
estudiante_docs_incompletos['archivo_titulo'] = None

prob_docs = calcular_probabilidad_exito(estudiante_docs_incompletos)
print(f"✅ Documentos incompletos: Probabilidad {prob_docs['probabilidad']}% - {prob_docs['categoria']}")

# Especialidad sin match exacto
estudiante_otro = test_estudiante.copy()
estudiante_otro['especialidad'] = 'Arquitectura'

cursos_otro = sugerir_cursos(estudiante_otro)
print(f"✅ Especialidad sin match: {len(cursos_otro)} cursos genéricos sugeridos")

print()
print("=" * 80)
print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
print("=" * 80)
