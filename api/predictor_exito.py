"""
Predictor de probabilidad de éxito en solicitud de visa de estudiante
Sistema basado en reglas con scoring ponderado
"""
from typing import Dict, List, Tuple
from datetime import datetime


class PredictorExito:
    """Calcula probabilidad de aprobación de visa basado en múltiples factores"""
    
    # Países con diferentes tasas históricas de aprobación
    PAISES_ALTA_APROBACION = ['Colombia', 'México', 'Chile', 'Argentina', 'Perú', 'Uruguay', 'Costa Rica']
    PAISES_MEDIA_APROBACION = ['Brasil', 'Ecuador', 'Venezuela', 'Bolivia', 'Paraguay', 'Panamá']
    PAISES_BAJA_APROBACION = ['Cuba', 'Haití', 'Nicaragua', 'Honduras', 'Guatemala']
    
    # Universidades reconocidas
    UNIVERSIDADES_TOP = ['UCM', 'Complutense', 'UB', 'Barcelona', 'UAM', 'Autónoma', 
                         'UPM', 'Politécnica Madrid', 'UPV', 'Politécnica Valencia',
                         'ESADE', 'IE', 'Deusto', 'Pompeu Fabra', 'UPF']
    
    def __init__(self):
        self.score = 0
        self.max_score = 100
        self.factores = []
        self.recomendaciones = []
    
    def calcular_probabilidad(self, datos_estudiante: Dict) -> Dict:
        """
        Calcula probabilidad de éxito basado en perfil del estudiante
        
        Args:
            datos_estudiante: Dict con:
                - nacionalidad: str
                - fondos_disponibles: float
                - documentos_subidos: int
                - documentos_generados: int
                - curso_asignado: str (nombre universidad/curso)
                - nivel_idioma: str (A1-C2)
                - especialidad: str
                - dias_desde_registro: int
                - antecedentes: bool (True si tiene problemas)
        
        Returns:
            Dict con probabilidad, desglose de factores y recomendaciones
        """
        self.score = 0
        self.factores = []
        self.recomendaciones = []
        
        # Factor 1: País de origen (20 puntos)
        self._evaluar_pais_origen(datos_estudiante.get('nacionalidad', ''))
        
        # Factor 2: Fondos económicos (25 puntos)
        self._evaluar_fondos(datos_estudiante.get('fondos_disponibles', 0))
        
        # Factor 3: Documentación completa (30 puntos)
        self._evaluar_documentacion(
            datos_estudiante.get('documentos_subidos', 0),
            datos_estudiante.get('documentos_generados', 0)
        )
        
        # Factor 4: Universidad/Curso (15 puntos)
        self._evaluar_universidad(datos_estudiante.get('curso_asignado', ''))
        
        # Factor 5: Nivel de idioma (10 puntos)
        self._evaluar_nivel_idioma(datos_estudiante.get('nivel_idioma', ''))
        
        # Factor 6: Antecedentes (penalización)
        self._evaluar_antecedentes(datos_estudiante.get('antecedentes', False))
        
        # Factor 7: Tiempo de preparación
        self._evaluar_tiempo_preparacion(datos_estudiante.get('dias_desde_registro', 0))
        
        # Calcular probabilidad final
        probabilidad = min(max(self.score, 0), 100)
        
        # Clasificar nivel de riesgo
        nivel_riesgo = self._clasificar_riesgo(probabilidad)
        
        # Generar recomendaciones prioritarias
        self._generar_recomendaciones_prioritarias(datos_estudiante, probabilidad)
        
        return {
            'probabilidad': round(probabilidad, 1),
            'nivel_riesgo': nivel_riesgo,
            'score_actual': round(self.score, 1),
            'score_maximo': self.max_score,
            'factores': self.factores,
            'recomendaciones': self.recomendaciones,
            'puede_aplicar': probabilidad >= 60
        }
    
    def _evaluar_pais_origen(self, nacionalidad: str):
        """Evalúa factor país de origen (20 puntos)"""
        if any(pais.lower() in nacionalidad.lower() for pais in self.PAISES_ALTA_APROBACION):
            puntos = 20
            nota = "País con alta tasa de aprobación histórica"
            self.score += puntos
        elif any(pais.lower() in nacionalidad.lower() for pais in self.PAISES_MEDIA_APROBACION):
            puntos = 12
            nota = "País con tasa de aprobación media"
            self.score += puntos
        elif any(pais.lower() in nacionalidad.lower() for pais in self.PAISES_BAJA_APROBACION):
            puntos = 5
            nota = "País con tasa de aprobación más baja (requiere mayor documentación)"
            self.score += puntos
            self.recomendaciones.append("Incluye documentos extras que demuestren arraigo a tu país")
        else:
            puntos = 10
            nota = "País sin historial suficiente"
            self.score += puntos
        
        self.factores.append({
            'factor': 'País de origen',
            'puntos': puntos,
            'maximo': 20,
            'nota': nota
        })
    
    def _evaluar_fondos(self, fondos: float):
        """Evalúa fondos económicos (25 puntos)"""
        # Mínimo recomendado: 15,000€ para año completo
        minimo_recomendado = 15000
        
        if fondos >= minimo_recomendado * 1.5:  # 150%+ del mínimo
            puntos = 25
            nota = "Fondos excelentes (150%+ del mínimo recomendado)"
            self.score += puntos
        elif fondos >= minimo_recomendado * 1.2:  # 120-150%
            puntos = 20
            nota = "Fondos muy buenos (120-150% del mínimo)"
            self.score += puntos
        elif fondos >= minimo_recomendado:  # 100-120%
            puntos = 15
            nota = "Fondos suficientes (cumple mínimo recomendado)"
            self.score += puntos
        elif fondos >= minimo_recomendado * 0.8:  # 80-100%
            puntos = 8
            nota = "Fondos justos (cerca del mínimo)"
            self.score += puntos
            self.recomendaciones.append(f"Intenta aumentar fondos a {minimo_recomendado}€ mínimo")
        else:
            puntos = 0
            nota = "Fondos insuficientes (por debajo del mínimo)"
            self.recomendaciones.append(f"URGENTE: Necesitas al menos {minimo_recomendado}€ demostrados")
        
        self.factores.append({
            'factor': 'Fondos económicos',
            'puntos': puntos,
            'maximo': 25,
            'nota': nota,
            'fondos_actuales': f"{fondos:,.0f}€",
            'minimo_recomendado': f"{minimo_recomendado:,.0f}€"
        })
    
    def _evaluar_documentacion(self, docs_subidos: int, docs_generados: int):
        """Evalúa completitud de documentación (30 puntos)"""
        # Esperados: 3 docs subidos, 4 generados
        docs_esperados_subidos = 3
        docs_esperados_generados = 4
        
        puntos_subidos = min((docs_subidos / docs_esperados_subidos) * 15, 15)
        puntos_generados = min((docs_generados / docs_esperados_generados) * 15, 15)
        puntos_total = puntos_subidos + puntos_generados
        
        self.score += puntos_total
        
        if docs_subidos < docs_esperados_subidos:
            faltantes = docs_esperados_subidos - docs_subidos
            self.recomendaciones.append(f"Sube {faltantes} documento(s) más: Título, Pasaporte, Extracto bancario")
        
        if docs_generados < docs_esperados_generados:
            self.recomendaciones.append("Solicita la generación de todos los documentos oficiales")
        
        nota = f"Documentos subidos: {docs_subidos}/{docs_esperados_subidos}, Generados: {docs_generados}/{docs_esperados_generados}"
        
        self.factores.append({
            'factor': 'Documentación completa',
            'puntos': round(puntos_total, 1),
            'maximo': 30,
            'nota': nota,
            'completitud': f"{(puntos_total/30)*100:.0f}%"
        })
    
    def _evaluar_universidad(self, curso: str):
        """Evalúa prestigio de universidad (15 puntos)"""
        es_top = any(uni.lower() in curso.lower() for uni in self.UNIVERSIDADES_TOP)
        
        if es_top:
            puntos = 15
            nota = "Universidad de alto prestigio reconocida por el consulado"
            self.score += puntos
        elif curso and len(curso) > 0:
            puntos = 10
            nota = "Universidad/centro educativo registrado"
            self.score += puntos
        else:
            puntos = 0
            nota = "Sin curso asignado todavía"
            self.recomendaciones.append("Selecciona y confirma tu curso/universidad")
        
        self.factores.append({
            'factor': 'Universidad/Curso',
            'puntos': puntos,
            'maximo': 15,
            'nota': nota
        })
    
    def _evaluar_nivel_idioma(self, nivel: str):
        """Evalúa nivel de idioma español (10 puntos)"""
        nivel_upper = nivel.upper()
        
        niveles = {'C2': 10, 'C1': 10, 'B2': 8, 'B1': 5, 'A2': 3, 'A1': 1}
        puntos = niveles.get(nivel_upper, 0)
        
        self.score += puntos
        
        if nivel_upper in ['A1', 'A2']:
            nota = f"Nivel {nivel_upper} - Considera curso de español previo"
            self.recomendaciones.append("Mejora tu nivel de español a B1+ antes de aplicar")
        elif nivel_upper == 'B1':
            nota = f"Nivel {nivel_upper} - Aceptable pero mejorable"
        else:
            nota = f"Nivel {nivel_upper} - Excelente para estudios en España"
        
        self.factores.append({
            'factor': 'Nivel de español',
            'puntos': puntos,
            'maximo': 10,
            'nota': nota
        })
    
    def _evaluar_antecedentes(self, tiene_antecedentes: bool):
        """Evalúa antecedentes (penalización hasta -20 puntos)"""
        if tiene_antecedentes:
            penalizacion = -20
            self.score += penalizacion
            nota = "Antecedentes penales o rechazos previos detectados"
            self.recomendaciones.append("Consulta con abogado de inmigración sobre antecedentes")
            
            self.factores.append({
                'factor': 'Antecedentes',
                'puntos': penalizacion,
                'maximo': 0,
                'nota': nota,
                'es_penalizacion': True
            })
    
    def _evaluar_tiempo_preparacion(self, dias: int):
        """Evalúa tiempo de preparación (bonificación hasta +10 puntos)"""
        if dias >= 30:
            puntos = 10
            nota = "Excelente preparación anticipada (más de 1 mes)"
            self.score += puntos
        elif dias >= 14:
            puntos = 5
            nota = "Preparación adecuada (2-4 semanas)"
            self.score += puntos
        elif dias >= 7:
            puntos = 2
            nota = "Preparación apresurada (1-2 semanas)"
            self.score += puntos
            self.recomendaciones.append("Tómate tiempo para revisar todo cuidadosamente")
        else:
            puntos = 0
            nota = "Preparación muy rápida (menos de 1 semana)"
            self.recomendaciones.append("CUIDADO: Revisa todo muy bien, hay riesgo de errores")
        
        self.factores.append({
            'factor': 'Tiempo de preparación',
            'puntos': puntos,
            'maximo': 10,
            'nota': nota,
            'dias': dias
        })
    
    def _clasificar_riesgo(self, probabilidad: float) -> str:
        """Clasifica nivel de riesgo según probabilidad"""
        if probabilidad >= 85:
            return "MUY BAJO"
        elif probabilidad >= 70:
            return "BAJO"
        elif probabilidad >= 55:
            return "MEDIO"
        elif probabilidad >= 40:
            return "ALTO"
        else:
            return "MUY ALTO"
    
    def _generar_recomendaciones_prioritarias(self, datos: Dict, prob: float):
        """Genera recomendaciones adicionales según probabilidad"""
        if prob < 60:
            self.recomendaciones.insert(0, "⚠️ CRÍTICO: Probabilidad baja. Mejora los puntos débiles antes de aplicar")
        
        if prob >= 80:
            self.recomendaciones.append("✅ Excelente perfil. Procede con confianza a la aplicación")
        
        # Recomendación de documentos extras si está en el límite
        if 55 <= prob < 70:
            self.recomendaciones.append("Incluye documentos extras: carta laboral, certificados adicionales")
    
    def comparar_perfiles(self, perfil_actual: Dict, perfil_mejorado: Dict) -> Dict:
        """Compara dos perfiles para mostrar mejora potencial"""
        resultado_actual = self.calcular_probabilidad(perfil_actual)
        resultado_mejorado = self.calcular_probabilidad(perfil_mejorado)
        
        mejora = resultado_mejorado['probabilidad'] - resultado_actual['probabilidad']
        
        return {
            'probabilidad_actual': resultado_actual['probabilidad'],
            'probabilidad_mejorada': resultado_mejorado['probabilidad'],
            'mejora': round(mejora, 1),
            'vale_la_pena': mejora >= 10
        }
