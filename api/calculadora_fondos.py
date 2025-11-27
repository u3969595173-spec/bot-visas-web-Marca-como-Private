"""
Calculadora de Fondos para Estudiantes en España
Calcula estimación de fondos necesarios según ciudad, duración, tipo de alojamiento
IMPORTANTE: Son estimaciones generales, los fondos reales pueden variar
"""

class CalculadoraFondos:
    """
    Calcula fondos estimados para estudiar en España
    """
    
    # Costos mensuales por ciudad (en euros)
    COSTOS_CIUDADES = {
        'madrid': {
            'nombre': 'Madrid',
            'alojamiento_residencia': 600,
            'alojamiento_piso_compartido': 450,
            'alojamiento_piso_individual': 800,
            'comida': 300,
            'transporte': 55,
            'costo_vida_base': 250
        },
        'barcelona': {
            'nombre': 'Barcelona',
            'alojamiento_residencia': 650,
            'alojamiento_piso_compartido': 500,
            'alojamiento_piso_individual': 850,
            'comida': 320,
            'transporte': 55,
            'costo_vida_base': 270
        },
        'valencia': {
            'nombre': 'Valencia',
            'alojamiento_residencia': 500,
            'alojamiento_piso_compartido': 350,
            'alojamiento_piso_individual': 650,
            'comida': 250,
            'transporte': 45,
            'costo_vida_base': 200
        },
        'sevilla': {
            'nombre': 'Sevilla',
            'alojamiento_residencia': 450,
            'alojamiento_piso_compartido': 300,
            'alojamiento_piso_individual': 600,
            'comida': 240,
            'transporte': 40,
            'costo_vida_base': 180
        },
        'granada': {
            'nombre': 'Granada',
            'alojamiento_residencia': 400,
            'alojamiento_piso_compartido': 250,
            'alojamiento_piso_individual': 500,
            'comida': 220,
            'transporte': 35,
            'costo_vida_base': 160
        },
        'bilbao': {
            'nombre': 'Bilbao',
            'alojamiento_residencia': 550,
            'alojamiento_piso_compartido': 400,
            'alojamiento_piso_individual': 700,
            'comida': 280,
            'transporte': 50,
            'costo_vida_base': 220
        },
        'salamanca': {
            'nombre': 'Salamanca',
            'alojamiento_residencia': 380,
            'alojamiento_piso_compartido': 230,
            'alojamiento_piso_individual': 450,
            'comida': 200,
            'transporte': 30,
            'costo_vida_base': 150
        },
        'otras': {
            'nombre': 'Otras ciudades',
            'alojamiento_residencia': 420,
            'alojamiento_piso_compartido': 280,
            'alojamiento_piso_individual': 550,
            'comida': 230,
            'transporte': 35,
            'costo_vida_base': 170
        }
    }
    
    # Costos de matrícula estimados por tipo de programa
    COSTOS_MATRICULA = {
        'grado_publico': {
            'nombre': 'Grado en Universidad Pública',
            'costo_anual': 1500,
            'rango': '750-2,500'
        },
        'grado_privado': {
            'nombre': 'Grado en Universidad Privada',
            'costo_anual': 8000,
            'rango': '5,000-15,000'
        },
        'master_publico': {
            'nombre': 'Máster en Universidad Pública',
            'costo_anual': 2500,
            'rango': '1,500-4,000'
        },
        'master_privado': {
            'nombre': 'Máster en Universidad Privada',
            'costo_anual': 12000,
            'rango': '8,000-20,000'
        },
        'doctorado': {
            'nombre': 'Doctorado',
            'costo_anual': 500,
            'rango': '300-800'
        },
        'curso_idiomas': {
            'nombre': 'Curso de Idiomas',
            'costo_anual': 3000,
            'rango': '2,000-5,000'
        }
    }
    
    @classmethod
    def calcular_fondos(cls, datos: dict) -> dict:
        """
        Calcula fondos estimados necesarios
        
        Parámetros:
        - ciudad: clave de COSTOS_CIUDADES
        - tipo_alojamiento: 'residencia', 'piso_compartido', 'piso_individual'
        - tipo_programa: clave de COSTOS_MATRICULA
        - duracion_meses: número de meses del programa
        - con_pareja: bool, si viaja con pareja (aumenta costos 60%)
        - con_hijos: int, número de hijos (aumenta costos significativamente)
        """
        ciudad = datos.get('ciudad', 'otras').lower()
        tipo_alojamiento = datos.get('tipo_alojamiento', 'piso_compartido')
        tipo_programa = datos.get('tipo_programa', 'grado_publico')
        duracion_meses = int(datos.get('duracion_meses', 10))
        con_pareja = datos.get('con_pareja', False)
        num_hijos = int(datos.get('num_hijos', 0))
        
        # Obtener datos de ciudad
        datos_ciudad = cls.COSTOS_CIUDADES.get(ciudad, cls.COSTOS_CIUDADES['otras'])
        
        # Calcular alojamiento mensual
        key_alojamiento = f'alojamiento_{tipo_alojamiento}'
        alojamiento_mensual = datos_ciudad.get(key_alojamiento, datos_ciudad['alojamiento_piso_compartido'])
        
        # Costos mensuales base
        comida_mensual = datos_ciudad['comida']
        transporte_mensual = datos_ciudad['transporte']
        otros_mensual = datos_ciudad['costo_vida_base']
        seguro_medico_mensual = 50
        
        # Total mensual base
        total_mensual = alojamiento_mensual + comida_mensual + transporte_mensual + otros_mensual + seguro_medico_mensual
        
        # Ajustar si va con pareja (60% adicional)
        if con_pareja:
            total_mensual = total_mensual * 1.6
        
        # Ajustar si va con hijos (40% adicional por hijo)
        if num_hijos > 0:
            total_mensual = total_mensual * (1 + (0.4 * num_hijos))
        
        # Total para toda la duración
        total_manutención = total_mensual * duracion_meses
        
        # Calcular matrícula
        datos_matricula = cls.COSTOS_MATRICULA.get(tipo_programa, cls.COSTOS_MATRICULA['grado_publico'])
        matricula_total = datos_matricula['costo_anual']
        
        # Costos iniciales únicos
        costos_iniciales = {
            'vuelo_ida_vuelta': 800,
            'deposito_alojamiento': alojamiento_mensual * 2,  # 2 meses de depósito
            'instalacion': 500,  # muebles básicos, menaje
            'tramites': 200  # NIE, empadronamiento, etc
        }
        
        total_inicial = sum(costos_iniciales.values())
        
        # TOTAL GENERAL
        total_general = matricula_total + total_manutención + total_inicial
        
        # Calcular desglose mensual
        desglose_mensual = {
            'alojamiento': alojamiento_mensual,
            'comida': comida_mensual,
            'transporte': transporte_mensual,
            'seguro_medico': seguro_medico_mensual,
            'otros': otros_mensual,
            'total': total_mensual
        }
        
        # Ajustes por pareja/hijos en desglose
        if con_pareja:
            desglose_mensual['pareja_adicional'] = total_mensual * 0.375  # ~60% del base
        if num_hijos > 0:
            desglose_mensual['hijos_adicional'] = total_mensual * (0.4 * num_hijos) / (1 + (0.4 * num_hijos))
        
        # Recomendaciones
        recomendaciones = cls._generar_recomendaciones(total_general, duracion_meses, con_pareja, num_hijos)
        
        # Comparación con fondos disponibles del estudiante
        fondos_disponibles = float(datos.get('fondos_disponibles', 0))
        suficiente = fondos_disponibles >= total_general
        diferencia = fondos_disponibles - total_general
        
        return {
            'ciudad': datos_ciudad['nombre'],
            'tipo_alojamiento': tipo_alojamiento.replace('_', ' ').title(),
            'tipo_programa': datos_matricula['nombre'],
            'duracion_meses': duracion_meses,
            'con_pareja': con_pareja,
            'num_hijos': num_hijos,
            
            'desglose_mensual': desglose_mensual,
            'total_mensual': round(total_mensual, 2),
            
            'matricula': round(matricula_total, 2),
            'rango_matricula': datos_matricula['rango'],
            
            'costos_iniciales': costos_iniciales,
            'total_inicial': round(total_inicial, 2),
            
            'total_manutención': round(total_manutención, 2),
            'total_general': round(total_general, 2),
            
            'fondos_disponibles': fondos_disponibles,
            'suficiente': suficiente,
            'diferencia': round(diferencia, 2),
            
            'recomendaciones': recomendaciones,
            
            'disclaimer': '⚠️ IMPORTANTE: Estas son estimaciones generales basadas en promedios. Los costos reales pueden variar según tu estilo de vida, universidad específica, y situación personal. Nosotros te ayudamos a planificar tu presupuesto detallado.'
        }
    
    @classmethod
    def _generar_recomendaciones(cls, total: float, duracion: int, con_pareja: bool, num_hijos: int) -> list:
        """
        Genera recomendaciones personalizadas según el cálculo
        """
        recomendaciones = []
        
        # Recomendación de fondo de emergencia
        recomendaciones.append(f"💡 Agrega 15-20% adicional como fondo de emergencia (€{round(total * 0.15)}-€{round(total * 0.20)})")
        
        # Recomendación según duración
        if duracion >= 10:
            recomendaciones.append("📅 Para estancias largas, considera abrir cuenta bancaria española para mejores tasas")
        
        # Recomendación si va con familia
        if con_pareja or num_hijos > 0:
            recomendaciones.append("👨‍👩‍👧 Viajes en familia requieren demostrar más fondos ante consulado")
        
        # Recomendación de trabajo
        if duracion >= 6:
            recomendaciones.append("💼 Con visa de estudiante puedes trabajar hasta 20h/semana para ingresos extra")
        
        # Recomendación de becas
        recomendaciones.append("🎓 Investiga becas MAEC-AECID, Fundación Carolina, o becas de tu universidad")
        
        # Recomendación de ahorro
        recomendaciones.append("💰 Planifica traer al menos 50% del total al inicio, el resto puede enviarse mensualmente")
        
        return recomendaciones
    
    @classmethod
    def obtener_ciudades_disponibles(cls) -> list:
        """
        Retorna lista de ciudades disponibles
        """
        return [
            {'key': key, 'nombre': datos['nombre']} 
            for key, datos in cls.COSTOS_CIUDADES.items()
        ]
    
    @classmethod
    def obtener_tipos_programa(cls) -> list:
        """
        Retorna lista de tipos de programa disponibles
        """
        return [
            {'key': key, 'nombre': datos['nombre'], 'rango': datos['rango']} 
            for key, datos in cls.COSTOS_MATRICULA.items()
        ]
