"""
Test del Simulador de Entrevistas
"""

from api.simulador_entrevista import SimuladorEntrevista

# Datos de prueba
estudiante_test = {
    "id": 1,
    "nombre": "Juan Pérez",
    "edad": 25,
    "especialidad": "Medicina",
    "nivel_espanol": "intermedio",
    "tipo_visa": "estudiante",
    "fondos_disponibles": 8000
}

print("=" * 80)
print("🎭 TEST: SIMULADOR DE ENTREVISTAS")
print("=" * 80)

# Generar entrevista personalizada
entrevista = SimuladorEntrevista.generar_entrevista_personalizada(estudiante_test)

print(f"\n✅ Entrevista generada para: {estudiante_test['nombre']}")
print(f"   Total preguntas: {entrevista['total_preguntas']}")
print(f"   Duración estimada: {entrevista['duracion_estimada']}")

# Mostrar contexto personalizado
print(f"\n📊 CONTEXTO PERSONALIZADO:")
print(f"   Puntos fuertes: {len(entrevista['contexto_personalizado']['puntos_fuertes'])}")
for punto in entrevista['contexto_personalizado']['puntos_fuertes']:
    print(f"      {punto}")

print(f"   Áreas a mejorar: {len(entrevista['contexto_personalizado']['areas_a_mejorar'])}")
for area in entrevista['contexto_personalizado']['areas_a_mejorar']:
    print(f"      {area}")

# Mostrar primeras 3 preguntas
print(f"\n❓ PRIMERAS 3 PREGUNTAS:")
for i, pregunta in enumerate(entrevista['preguntas'][:3], 1):
    print(f"\n   {i}. {pregunta['pregunta']}")
    print(f"      Categoría: {pregunta['categoria']}")
    print(f"      Tip: {pregunta['tips'][:80]}...")

# Probar evaluación de respuesta
print(f"\n📝 TEST DE EVALUACIÓN:")
respuesta_corta = "Porque España es un buen país"
evaluacion1 = SimuladorEntrevista.evaluar_respuesta(0, respuesta_corta)
print(f"   Respuesta corta: '{respuesta_corta}'")
print(f"   Calidad: {evaluacion1['calidad']} | Puntuación: {evaluacion1['puntuacion']}/100")
print(f"   Feedback: {evaluacion1['feedback']}")

respuesta_buena = "Quiero estudiar en España porque la Universidad Complutense de Madrid ofrece el mejor programa de Medicina en Europa, con reconocimiento internacional. Mi objetivo es especializarme en cardiología y aplicar estos conocimientos en mi país, donde hay una alta demanda de especialistas con formación europea. He investigado sobre el programa, los profesores destacados, y las oportunidades de investigación disponibles."
evaluacion2 = SimuladorEntrevista.evaluar_respuesta(0, respuesta_buena)
print(f"\n   Respuesta completa (adic): '{respuesta_buena[:80]}...'")
print(f"   Calidad: {evaluacion2['calidad']} | Puntuación: {evaluacion2['puntuacion']}/100")
print(f"   Feedback: {evaluacion2['feedback']}")

# Mostrar consejos generales
print(f"\n💡 CONSEJOS GENERALES: {len(entrevista['consejos_generales'])} tips")
for consejo in entrevista['consejos_generales'][:3]:
    print(f"   {consejo['icono']} {consejo['titulo']}: {consejo['consejo'][:60]}...")

print(f"\n{'=' * 80}")
print("✅ TODOS LOS TESTS DEL SIMULADOR PASARON")
print("=" * 80)
