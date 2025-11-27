"""
Simulador de Entrevistas Consulares con IA
Prepara a los estudiantes con preguntas reales adaptadas a su perfil
"""

import random
from datetime import datetime
from .banco_preguntas_entrevista import BANCO_PREGUNTAS_COMPLETO

class SimuladorEntrevista:
    """
    Simula entrevista consular con preguntas personalizadas según perfil del estudiante
    Banco de 100+ preguntas reales - cada simulación muestra 11 aleatorias
    """
    
    # BANCO COMPLETO DE 100+ PREGUNTAS REALES DE ENTREVISTAS CONSULARES
    BANCO_PREGUNTAS = [
        # === MOTIVACIÓN Y PLANES (20 preguntas) ===
        {
            "pregunta": "¿Por qué quieres estudiar en España y no en tu país?",
            "categoria": "motivacion",
            "tips": "Habla sobre la calidad educativa, programas específicos no disponibles en tu país, reconocimiento internacional del título.",
            "respuesta_modelo": "Quiero estudiar en España porque ofrece programas de alta calidad reconocidos internacionalmente. Específicamente, el programa de [tu carrera] en [universidad] no está disponible con este nivel de especialización en mi país."
        },
        {
            "pregunta": "¿Cómo vas a financiar tus estudios y manutención?",
            "categoria": "fondos",
            "tips": "Menciona tus ahorros, apoyo familiar, becas. Sé específico con cantidades y muestra evidencia.",
            "respuesta_modelo": "Cuento con €[cantidad] en ahorros personales y el apoyo económico de mi familia que puede demostrar ingresos mensuales de €[cantidad]. También he aplicado a [becas]."
        },
        {
            "pregunta": "¿Qué sabes sobre la universidad y el programa al que aplicas?",
            "categoria": "conocimiento",
            "tips": "Investiga ranking, profesores destacados, instalaciones, empleabilidad de egresados.",
            "respuesta_modelo": "La [universidad] está rankeada #[número] en [campo]. El programa incluye [detalles específicos]. Me interesa especialmente el enfoque en [aspecto específico]."
        },
        {
            "pregunta": "¿Planeas regresar a tu país después de terminar los estudios?",
            "categoria": "intencion",
            "tips": "SIEMPRE di que sí planeas regresar. Es una pregunta clave para demostrar no-inmigración.",
            "respuesta_modelo": "Sí, planeo regresar para aplicar los conocimientos adquiridos y contribuir al desarrollo de [sector/industria] en mi país."
        },
        {
            "pregunta": "¿Tienes familiares o conocidos en España?",
            "categoria": "vinculos",
            "tips": "Sé honesto. Si tienes, explica que te ayudarán con adaptación pero no dependerás económicamente.",
            "respuesta_modelo": "Tengo [familiar/amigo] que vive en [ciudad] hace [tiempo], quien me ha orientado sobre el sistema educativo pero soy independiente económicamente."
        }
    ]
    
    PREGUNTAS_ACADEMICAS = [
        {
            "pregunta": "¿Por qué elegiste esta carrera específicamente?",
            "categoria": "academico",
            "tips": "Conecta con tu experiencia previa, tus metas profesionales, y por qué esta carrera específica.",
            "respuesta_modelo": "Elegí [carrera] porque tengo experiencia en [campo relacionado] y mi objetivo es especializarme en [área]. Esta carrera me permitirá [objetivos]."
        },
        {
            "pregunta": "¿Qué harás si no te aceptan en esta universidad?",
            "categoria": "plan_b",
            "tips": "Muestra que tienes opciones pero que esta es tu primera elección por razones específicas.",
            "respuesta_modelo": "Esta es mi primera opción por [razones], pero también he considerado [otras universidades] que ofrecen programas similares de calidad."
        },
        {
            "pregunta": "¿Cómo es tu nivel de español?",
            "categoria": "idioma",
            "tips": "Sé honesto sobre tu nivel. Si es básico, menciona planes de tomar curso intensivo.",
            "respuesta_modelo": "Mi nivel actual es [nivel]. He estado estudiando español por [tiempo] y planeo tomar un curso intensivo antes de iniciar el programa."
        }
    ]
    
    PREGUNTAS_FINANCIERAS = [
        {
            "pregunta": "¿Cuánto dinero traerás a España inicialmente?",
            "categoria": "fondos",
            "tips": "Menciona cantidad específica, muestra extractos bancarios. Mínimo €6,000-€10,000.",
            "respuesta_modelo": "Traeré €[cantidad] inicialmente, que cubre [X meses] de matrícula y manutención. Tengo extractos bancarios que demuestran estos fondos."
        },
        {
            "pregunta": "¿Quién te patrocina económicamente?",
            "categoria": "patrocinio",
            "tips": "Explica relación, muestra carta de patrocinio y evidencia de ingresos del patrocinador.",
            "respuesta_modelo": "Mi [relación] es mi patrocinador. Trabaja como [profesión] con ingresos mensuales de €[cantidad]. Tengo carta de patrocinio notariada."
        },
        {
            "pregunta": "¿Tienes algún tipo de beca o ayuda financiera?",
            "categoria": "becas",
            "tips": "Si aplicas a becas, menciona cuáles y estado de aplicación. Si no, está bien decir que no.",
            "respuesta_modelo": "He aplicado a [beca] y estoy esperando respuesta. También cuento con recursos propios para cubrir los gastos."
        }
    ]
    
    PREGUNTAS_PERSONALES = [
        {
            "pregunta": "¿Dónde planeas vivir en España?",
            "categoria": "alojamiento",
            "tips": "Muestra que has investigado opciones: residencia estudiantil, piso compartido, etc.",
            "respuesta_modelo": "Planeo vivir en [residencia estudiantil/piso compartido] cerca de la universidad. Ya he investigado opciones en [zona] con precios de €[rango]."
        },
        {
            "pregunta": "¿Qué sabes sobre el costo de vida en España?",
            "categoria": "preparacion",
            "tips": "Demuestra que has investigado: alquiler, comida, transporte, seguro médico.",
            "respuesta_modelo": "He investigado que el costo mensual promedio es €800-€1,200 incluyendo alquiler (€300-€500), comida (€200-€300), transporte (€50), y otros gastos."
        },
        {
            "pregunta": "¿Tienes seguro médico?",
            "categoria": "documentacion",
            "tips": "Menciona que contratarás seguro de estudiante internacional o ya tienes uno.",
            "respuesta_modelo": "Sí, contrataré/he contratado seguro médico de estudiante con [compañía] que cubre €[cantidad] con cobertura completa."
        }
    ]
    
    PREGUNTAS_CRITICAS = [
        {
            "pregunta": "¿Por qué deberíamos darte la visa?",
            "categoria": "persuasion",
            "tips": "Resume tus puntos fuertes: preparación académica, fondos suficientes, plan claro, intención de regresar.",
            "respuesta_modelo": "Porque cumplo todos los requisitos: tengo admisión en [universidad], fondos demostrados para [periodo], plan académico claro, y vínculos familiares/laborales en mi país que garantizan mi regreso."
        },
        {
            "pregunta": "¿Qué harías si te rechazan la visa?",
            "categoria": "persistencia",
            "tips": "Muestra determinación pero respeto al proceso. Mencionarías revisar qué mejorar y volver a aplicar.",
            "respuesta_modelo": "Revisaría los motivos del rechazo, mejoraría lo necesario (más fondos, mejor documentación), y aplicaría nuevamente siguiendo las recomendaciones."
        }
    ]

    @classmethod
    def generar_entrevista_personalizada(cls, estudiante_data: dict) -> dict:
        """
        Genera una entrevista personalizada según el perfil del estudiante
        Selecciona 11 preguntas aleatorias del banco de 100+
        """
        nivel_espanol = estudiante_data.get('nivel_espanol', 'basico')
        fondos = float(estudiante_data.get('fondos_disponibles', 0))
        especialidad = estudiante_data.get('especialidad', '')
        edad = int(estudiante_data.get('edad', 25))
        
        # Filtrar preguntas por categorías relevantes
        categorias_importantes = ['intencion_retorno', 'motivacion', 'fondos', 'universidad']
        
        # Separar preguntas por importancia
        preguntas_criticas = [p for p in BANCO_PREGUNTAS_COMPLETO if p['categoria'] in categorias_importantes]
        preguntas_otras = [p for p in BANCO_PREGUNTAS_COMPLETO if p['categoria'] not in categorias_importantes]
        
        # Seleccionar 5 preguntas críticas (siempre incluidas)
        seleccion_criticas = random.sample(preguntas_criticas, min(5, len(preguntas_criticas)))
        
        # Seleccionar 6 preguntas adicionales aleatorias
        seleccion_otras = random.sample(preguntas_otras, min(6, len(preguntas_otras)))
        
        # Combinar y mezclar todas
        preguntas_seleccionadas = seleccion_criticas + seleccion_otras
        random.shuffle(preguntas_seleccionadas)
        
        # Limitar a 11 preguntas totales
        preguntas_seleccionadas = preguntas_seleccionadas[:11]
        
        # Agregar contexto personalizado
        contexto = cls._generar_contexto_personalizado(estudiante_data)
        
        # Consejos generales
        consejos = cls._generar_consejos_generales(estudiante_data)
        
        return {
            "estudiante_id": estudiante_data.get('id'),
            "fecha_generacion": datetime.now().isoformat(),
            "total_preguntas": len(preguntas_seleccionadas),
            "contexto_personalizado": contexto,
            "preguntas": preguntas_seleccionadas,
            "consejos_generales": consejos,
            "duracion_estimada": f"{len(preguntas_seleccionadas) * 2}-{len(preguntas_seleccionadas) * 3} minutos",
            "formato": "simulacion_interactiva",
            "banco_total": len(BANCO_PREGUNTAS_COMPLETO)
        }
        
        return {
            "estudiante_id": estudiante_data.get('id'),
            "fecha_generacion": datetime.now().isoformat(),
            "total_preguntas": len(preguntas_seleccionadas),
            "contexto_personalizado": contexto,
            "preguntas": preguntas_seleccionadas,
            "consejos_generales": consejos,
            "duracion_estimada": f"{len(preguntas_seleccionadas) * 2}-{len(preguntas_seleccionadas) * 3} minutos",
            "formato": "simulacion_interactiva"
        }
    
    @classmethod
    def _generar_contexto_personalizado(cls, estudiante_data: dict) -> dict:
        """
        Genera contexto específico para este estudiante
        """
        fondos = float(estudiante_data.get('fondos_disponibles', 0))
        nivel_espanol = estudiante_data.get('nivel_espanol', 'basico')
        tipo_visa = estudiante_data.get('tipo_visa', 'estudiante')
        edad = int(estudiante_data.get('edad', 25))
        
        puntos_fuertes = []
        areas_mejorar = []
        
        # Evaluar fondos
        fondos_minimos = 6000 if tipo_visa == 'idiomas' else 10000
        if fondos >= fondos_minimos * 1.5:
            puntos_fuertes.append("💪 Fondos muy sólidos (por encima del mínimo)")
        elif fondos >= fondos_minimos:
            puntos_fuertes.append("✅ Fondos suficientes")
        else:
            areas_mejorar.append(f"⚠️ Fondos bajos (tienes €{fondos:,.0f}, recomendado €{fondos_minimos:,.0f}+)")
        
        # Evaluar español
        if nivel_espanol in ['avanzado', 'nativo']:
            puntos_fuertes.append("💪 Excelente nivel de español")
        elif nivel_espanol == 'intermedio':
            puntos_fuertes.append("✅ Nivel de español adecuado")
        else:
            areas_mejorar.append("⚠️ Considera tomar curso intensivo de español antes")
        
        # Evaluar edad
        if 18 <= edad <= 28:
            puntos_fuertes.append("✅ Edad ideal para estudios")
        elif 29 <= edad <= 35:
            puntos_fuertes.append("✅ Edad adecuada")
        else:
            areas_mejorar.append("ℹ️ Prepara una buena justificación sobre por qué estudiar ahora")
        
        return {
            "puntos_fuertes": puntos_fuertes,
            "areas_a_mejorar": areas_mejorar,
            "recomendacion_principal": "Practica tus respuestas en voz alta, mantén contacto visual, sé honesto y específico."
        }
    
    @classmethod
    def _generar_consejos_generales(cls, estudiante_data: dict) -> list:
        """
        Consejos generales para la entrevista
        """
        return [
            {
                "icono": "👔",
                "titulo": "Vestimenta",
                "consejo": "Viste formal pero cómodo. Primera impresión cuenta."
            },
            {
                "icono": "📄",
                "titulo": "Documentos",
                "consejo": "Lleva TODOS los documentos originales + copias organizados en carpeta."
            },
            {
                "icono": "⏰",
                "titulo": "Puntualidad",
                "consejo": "Llega 30 minutos antes. Demuestra seriedad y compromiso."
            },
            {
                "icono": "😊",
                "titulo": "Actitud",
                "consejo": "Mantén contacto visual, sonríe, habla con confianza pero no arrogancia."
            },
            {
                "icono": "🎯",
                "titulo": "Respuestas",
                "consejo": "Sé específico y conciso. Evita respuestas vagas o muy largas."
            },
            {
                "icono": "🚫",
                "titulo": "Evitar",
                "consejo": "NO mientas, NO des respuestas contradictorias, NO muestres nerviosismo excesivo."
            },
            {
                "icono": "📱",
                "titulo": "Preparación",
                "consejo": "Practica con familiares/amigos. Grábate respondiendo las preguntas."
            },
            {
                "icono": "💡",
                "titulo": "Clave",
                "consejo": "Demuestra que REGRESAR a tu país es parte de tu plan. Es la pregunta más importante."
            }
        ]
    
    @classmethod
    def evaluar_respuesta(cls, pregunta_id: int, respuesta_usuario: str, pregunta_obj: dict = None) -> dict:
        """
        Evalúa una respuesta del usuario y da feedback detallado
        """
        # Análisis básico de la respuesta
        longitud = len(respuesta_usuario.split())
        respuesta_lower = respuesta_usuario.lower()
        
        if longitud < 10:
            calidad = "Muy corta"
            feedback = "❌ Tu respuesta es demasiado breve. Expándela con más detalles específicos."
            puntuacion = 40
            recomendaciones = [
                "Agrega más detalles y contexto",
                "Menciona ejemplos concretos",
                "Explica el 'por qué' de tu respuesta"
            ]
        elif longitud < 30:
            calidad = "Corta"
            feedback = "⚠️ Respuesta básica. Agrega ejemplos concretos y más contexto."
            puntuacion = 60
            recomendaciones = [
                "Incluye fechas, nombres o cantidades específicas",
                "Explica más profundamente tus motivaciones",
                "Da ejemplos reales de tu situación"
            ]
        elif longitud < 100:
            calidad = "Adecuada"
            feedback = "✅ Buena respuesta. Asegúrate de ser específico con nombres, fechas y cantidades."
            puntuacion = 80
            recomendaciones = [
                "Mantén este nivel de detalle",
                "Practica diciendo esto en voz alta",
                "Asegúrate de sonar natural y confiado"
            ]
        else:
            calidad = "Muy larga"
            feedback = "⚠️ Respuesta muy extensa. Intenta ser más conciso manteniendo los puntos clave."
            puntuacion = 70
            recomendaciones = [
                "Resume en 3-4 puntos principales",
                "Elimina información redundante",
                "Ve directo al punto"
            ]
        
        # Verificar palabras clave positivas
        palabras_clave = ['porque', 'específicamente', 'demostrar', 'evidencia', 'plan', 'objetivo', 'regresar', 'universidad', 'carrera', 'familia']
        palabras_encontradas = sum(1 for palabra in palabras_clave if palabra.lower() in respuesta_lower)
        
        if palabras_encontradas >= 3:
            puntuacion += 10
            feedback += " ✨ Usas buenos términos específicos."
        
        # Detectar problemas comunes
        problemas = []
        if respuesta_usuario.isupper():
            problemas.append("No escribas en MAYÚSCULAS, parece que estás gritando")
            puntuacion -= 5
        
        errores_ortograficos = ['preparecimn', 'supietso', 'herosos', 'rresignado', 'desaroolo', 'profesioanl']
        if any(error in respuesta_lower for error in errores_ortograficos):
            problemas.append("Revisa la ortografía antes de la entrevista real")
            puntuacion -= 5
        
        # Agregar tips de la pregunta si están disponibles
        tips_pregunta = pregunta_obj.get('tips', '') if pregunta_obj else ''
        respuesta_modelo = pregunta_obj.get('respuesta_modelo', '') if pregunta_obj else ''
        
        return {
            "calidad": calidad,
            "puntuacion": max(0, min(puntuacion, 100)),
            "feedback": feedback,
            "recomendaciones": recomendaciones if 'recomendaciones' in locals() else [],
            "problemas": problemas if 'problemas' in locals() else [],
            "tips": tips_pregunta,
            "respuesta_modelo": respuesta_modelo,
            "longitud_palabras": longitud
        }
