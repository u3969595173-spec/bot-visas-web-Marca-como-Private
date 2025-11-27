"""
Sistema de sugerencia de cursos según perfil del estudiante
"""

def sugerir_cursos(estudiante_data: dict) -> list:
    """
    Sugiere cursos basados en especialidad, nivel de español y fondos
    """
    especialidad = (estudiante_data.get('especialidad') or '').lower()
    nivel_espanol = estudiante_data.get('nivel_espanol') or 'basico'
    fondos = float(estudiante_data.get('fondos_disponibles') or 0)
    tipo_visa = estudiante_data.get('tipo_visa') or 'estudiante'
    
    cursos = []
    
    # Cursos por especialidad
    if 'ingenier' in especialidad or 'inform' in especialidad or 'tecnolog' in especialidad:
        cursos.extend([
            {
                'nombre': 'Grado en Ingeniería Informática',
                'universidad': 'Universidad Politécnica de Madrid',
                'duracion': '4 años',
                'costo_anual': 1200,
                'nivel_espanol_requerido': 'intermedio',
                'match': 95
            },
            {
                'nombre': 'Máster en Inteligencia Artificial',
                'universidad': 'Universidad de Barcelona',
                'duracion': '1 año',
                'costo_anual': 3500,
                'nivel_espanol_requerido': 'avanzado',
                'match': 90
            }
        ])
    
    elif ('medicina' in especialidad or 'medic' in especialidad or 'salud' in especialidad or 
          'enfermer' in especialidad or 'doctor' in especialidad or 'graduado' in especialidad):
        cursos.extend([
            {
                'nombre': 'Grado en Medicina',
                'universidad': 'Universidad Complutense de Madrid',
                'duracion': '6 años',
                'costo_anual': 2500,
                'nivel_espanol_requerido': 'avanzado',
                'match': 95
            },
            {
                'nombre': 'Máster en Salud Pública',
                'universidad': 'Universidad de Valencia',
                'duracion': '1 año',
                'costo_anual': 3000,
                'nivel_espanol_requerido': 'intermedio',
                'match': 88
            }
        ])
    
    elif 'derecho' in especialidad or 'ley' in especialidad or 'legal' in especialidad:
        cursos.extend([
            {
                'nombre': 'Grado en Derecho',
                'universidad': 'Universidad de Salamanca',
                'duracion': '4 años',
                'costo_anual': 1500,
                'nivel_espanol_requerido': 'avanzado',
                'match': 92
            },
            {
                'nombre': 'Máster en Derecho Internacional',
                'universidad': 'IE University',
                'duracion': '1 año',
                'costo_anual': 25000,
                'nivel_espanol_requerido': 'avanzado',
                'match': 85
            }
        ])
    
    elif 'negocio' in especialidad or 'administra' in especialidad or 'empresa' in especialidad:
        cursos.extend([
            {
                'nombre': 'Grado en Administración de Empresas',
                'universidad': 'ESADE Barcelona',
                'duracion': '4 años',
                'costo_anual': 18000,
                'nivel_espanol_requerido': 'intermedio',
                'match': 94
            },
            {
                'nombre': 'MBA - Master in Business Administration',
                'universidad': 'IE Business School',
                'duracion': '1 año',
                'costo_anual': 70000,
                'nivel_espanol_requerido': 'basico',
                'match': 88
            }
        ])
    
    else:
        # Cursos genéricos
        cursos.extend([
            {
                'nombre': 'Grado en Ciencias Políticas',
                'universidad': 'Universidad Carlos III',
                'duracion': '4 años',
                'costo_anual': 1800,
                'nivel_espanol_requerido': 'intermedio',
                'match': 75
            },
            {
                'nombre': 'Máster en Educación',
                'universidad': 'Universidad Autónoma de Barcelona',
                'duracion': '1 año',
                'costo_anual': 2800,
                'nivel_espanol_requerido': 'intermedio',
                'match': 72
            }
        ])
    
    # Cursos de idiomas si el nivel de español es básico
    if nivel_espanol == 'basico' or tipo_visa == 'idiomas':
        cursos.insert(0, {
            'nombre': 'Curso Intensivo de Español (6 meses)',
            'universidad': 'Instituto Cervantes Madrid',
            'duracion': '6 meses',
            'costo_anual': 3600,
            'nivel_espanol_requerido': 'ninguno',
            'match': 98
        })
    
    # Filtrar por fondos disponibles (costo total estimado para primer año)
    cursos_filtrados = []
    for curso in cursos:
        costo_total_estimado = curso['costo_anual'] + 8000  # +8000 para gastos de vida
        if fondos >= costo_total_estimado * 0.7:  # Al menos 70% del costo
            curso['asequible'] = True
        else:
            curso['asequible'] = False
        cursos_filtrados.append(curso)
    
    # Ordenar por match descendente
    cursos_filtrados.sort(key=lambda x: x['match'], reverse=True)
    
    return cursos_filtrados[:5]  # Retornar top 5
