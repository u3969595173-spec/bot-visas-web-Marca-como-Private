"""
Calculador de probabilidad de éxito de visa de estudiante
"""

def calcular_probabilidad_exito(estudiante_data: dict) -> dict:
    """
    Calcula la probabilidad de éxito basada en múltiples factores
    Retorna diccionario con score, probabilidad y factores evaluados
    """
    puntos = 0
    factores = []
    max_puntos = 100
    
    # FACTOR 1: Fondos disponibles (30 puntos)
    fondos = float(estudiante_data.get('fondos_disponibles') or 0)
    tipo_visa = estudiante_data.get('tipo_visa') or 'estudiante'
    
    if tipo_visa == 'idiomas':
        fondos_requeridos = 4000  # 6 meses
    else:
        fondos_requeridos = 10000  # 1 año
    
    if fondos >= fondos_requeridos:
        puntos += 30
        factores.append({'factor': 'Fondos suficientes', 'puntos': 30, 'cumple': True})
    elif fondos >= fondos_requeridos * 0.7:
        puntos += 20
        factores.append({'factor': 'Fondos aceptables', 'puntos': 20, 'cumple': True})
    elif fondos >= fondos_requeridos * 0.5:
        puntos += 10
        factores.append({'factor': 'Fondos insuficientes', 'puntos': 10, 'cumple': False})
    else:
        factores.append({'factor': 'Fondos muy bajos', 'puntos': 0, 'cumple': False})
    
    # FACTOR 2: Nivel de español (30 puntos)
    nivel_espanol = estudiante_data.get('nivel_espanol') or 'basico'
    nivel_puntos = {
        'nativo': 30,
        'avanzado': 25,
        'intermedio': 15,
        'basico': 10
    }
    puntos_nivel = nivel_puntos.get(nivel_espanol, 10)
    puntos += puntos_nivel
    factores.append({
        'factor': f'Nivel de español: {nivel_espanol}',
        'puntos': puntos_nivel,
        'cumple': puntos_nivel >= 15
    })
    
    # FACTOR 3: Documentos completos (25 puntos)
    archivo_titulo = estudiante_data.get('archivo_titulo')
    archivo_pasaporte = estudiante_data.get('archivo_pasaporte')
    archivo_extractos = estudiante_data.get('archivo_extractos')
    consentimiento_gdpr = estudiante_data.get('consentimiento_gdpr', False)
    
    docs_completos = all([archivo_titulo, archivo_pasaporte, archivo_extractos, consentimiento_gdpr])
    if docs_completos:
        puntos += 25
        factores.append({'factor': 'Documentación completa', 'puntos': 25, 'cumple': True})
    else:
        docs_faltantes = []
        if not archivo_titulo:
            docs_faltantes.append('título académico')
        if not archivo_pasaporte:
            docs_faltantes.append('pasaporte')
        if not archivo_extractos:
            docs_faltantes.append('extractos bancarios')
        if not consentimiento_gdpr:
            docs_faltantes.append('consentimiento GDPR')
        
        puntos += 10
        factores.append({
            'factor': f'Documentos incompletos (faltan: {", ".join(docs_faltantes)})',
            'puntos': 10,
            'cumple': False
        })
    
    # FACTOR 4: Edad (15 puntos)
    edad = int(estudiante_data.get('edad') or 0)
    if 18 <= edad <= 35:
        puntos += 15
        factores.append({'factor': 'Edad ideal (18-35)', 'puntos': 15, 'cumple': True})
    elif 36 <= edad <= 50:
        puntos += 10
        factores.append({'factor': 'Edad aceptable (36-50)', 'puntos': 10, 'cumple': True})
    elif edad > 50:
        puntos += 5
        factores.append({'factor': 'Edad avanzada (>50)', 'puntos': 5, 'cumple': False})
    else:
        factores.append({'factor': 'Edad no válida', 'puntos': 0, 'cumple': False})
    
    # Calcular probabilidad
    probabilidad = round((puntos / max_puntos) * 100, 1)
    
    # Determinar categoría
    if probabilidad >= 80:
        categoria = 'Excelente'
        color = 'success'
        mensaje = '¡Tu perfil es muy fuerte! Alta probabilidad de aprobación.'
    elif probabilidad >= 60:
        categoria = 'Buena'
        color = 'info'
        mensaje = 'Tu perfil es sólido. Revisa los factores pendientes para mejorar.'
    elif probabilidad >= 40:
        categoria = 'Regular'
        color = 'warning'
        mensaje = 'Necesitas mejorar varios aspectos antes de aplicar.'
    else:
        categoria = 'Baja'
        color = 'danger'
        mensaje = 'Tu perfil necesita trabajo significativo antes de aplicar.'
    
    return {
        'puntos': puntos,
        'max_puntos': max_puntos,
        'probabilidad': probabilidad,
        'categoria': categoria,
        'color': color,
        'mensaje': mensaje,
        'factores': factores
    }
