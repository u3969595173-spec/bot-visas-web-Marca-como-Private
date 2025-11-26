"""
Sistema de Prioridades Inteligente
Ordena estudiantes por urgencia, completitud y probabilidad de éxito
"""

from datetime import datetime, timedelta
from typing import List, Dict
from modules.estudiantes import Estudiante
from modules.cursos import GestorCursos
from modules.fondos import GestorFondos
from database.models import get_db


class SistemaPrioridades:
    """Calcula prioridades para revisión de estudiantes"""
    
    @staticmethod
    def calcular_score_prioridad(estudiante: Estudiante) -> Dict:
        """
        Calcula un score de prioridad para un estudiante
        
        Factores considerados:
        - Urgencia temporal (fecha de inicio de curso cercana)
        - Completitud de información
        - Probabilidad de éxito
        - Tiempo esperando revisión
        - Nivel de fondos
        
        Args:
            estudiante: Objeto Estudiante
            
        Returns:
            Dict con score y desglose
        """
        score = 0
        desglose = {}
        
        # 1. URGENCIA TEMPORAL (0-40 puntos)
        urgencia_score = 0
        dias_hasta_inicio = None
        
        if estudiante.curso_asignado_id:
            curso = GestorCursos.obtener_curso_por_id(estudiante.curso_asignado_id)
            if curso and curso.fecha_inicio:
                dias_hasta_inicio = (curso.fecha_inicio - datetime.now()).days
                
                if dias_hasta_inicio <= 30:
                    urgencia_score = 40  # Muy urgente
                elif dias_hasta_inicio <= 60:
                    urgencia_score = 30  # Urgente
                elif dias_hasta_inicio <= 90:
                    urgencia_score = 20  # Moderado
                else:
                    urgencia_score = 10  # No urgente
        
        score += urgencia_score
        desglose['urgencia_temporal'] = {
            'puntos': urgencia_score,
            'dias_hasta_inicio': dias_hasta_inicio,
            'nivel': 'muy_urgente' if urgencia_score >= 35 else 'urgente' if urgencia_score >= 25 else 'moderado' if urgencia_score >= 15 else 'normal'
        }
        
        # 2. COMPLETITUD DE INFORMACIÓN (0-25 puntos)
        completitud_score = 0
        
        total_docs = len(estudiante.documentos_completados or []) + len(estudiante.documentos_pendientes or [])
        if total_docs > 0:
            porcentaje_docs = (len(estudiante.documentos_completados or []) / total_docs) * 100
            completitud_score = int(porcentaje_docs * 0.25)  # Max 25 puntos
        
        score += completitud_score
        desglose['completitud'] = {
            'puntos': completitud_score,
            'porcentaje_documentos': porcentaje_docs if total_docs > 0 else 0,
            'nivel': 'completo' if completitud_score >= 20 else 'alto' if completitud_score >= 15 else 'medio' if completitud_score >= 10 else 'bajo'
        }
        
        # 3. FONDOS ECONÓMICOS (0-20 puntos)
        fondos_score = 0
        
        try:
            verificacion = GestorFondos.verificar_fondos(estudiante.id)
            porcentaje_fondos = verificacion.get('porcentaje_cobertura', 0)
            
            if porcentaje_fondos >= 100:
                fondos_score = 20  # Fondos suficientes
            elif porcentaje_fondos >= 80:
                fondos_score = 15  # Casi suficientes
            elif porcentaje_fondos >= 50:
                fondos_score = 10  # Parciales
            else:
                fondos_score = 5   # Insuficientes (pero igual requiere atención)
        except:
            fondos_score = 10  # Default si no se puede verificar
        
        score += fondos_score
        desglose['fondos'] = {
            'puntos': fondos_score,
            'porcentaje_cobertura': porcentaje_fondos if 'verificacion' in locals() else 0,
            'nivel': 'suficiente' if fondos_score >= 18 else 'casi_suficiente' if fondos_score >= 13 else 'parcial' if fondos_score >= 8 else 'insuficiente'
        }
        
        # 4. TIEMPO ESPERANDO REVISIÓN (0-10 puntos)
        tiempo_espera_score = 0
        
        if estudiante.fecha_procesamiento_automatico:
            horas_esperando = (datetime.now() - estudiante.fecha_procesamiento_automatico).total_seconds() / 3600
            
            if horas_esperando >= 48:
                tiempo_espera_score = 10  # Más de 2 días
            elif horas_esperando >= 24:
                tiempo_espera_score = 7   # Más de 1 día
            elif horas_esperando >= 12:
                tiempo_espera_score = 5   # Más de 12 horas
            else:
                tiempo_espera_score = 3   # Menos de 12 horas
        
        score += tiempo_espera_score
        desglose['tiempo_espera'] = {
            'puntos': tiempo_espera_score,
            'horas_esperando': horas_esperando if 'horas_esperando' in locals() else 0,
            'nivel': 'critico' if tiempo_espera_score >= 9 else 'alto' if tiempo_espera_score >= 6 else 'moderado' if tiempo_espera_score >= 4 else 'reciente'
        }
        
        # 5. CALIDAD DEL PERFIL (0-5 puntos)
        calidad_score = 0
        
        # Perfil completo
        if all([
            estudiante.email,
            estudiante.telefono,
            estudiante.especialidad_interes,
            estudiante.nivel_espanol,
            estudiante.curso_asignado_id
        ]):
            calidad_score = 5
        else:
            calidad_score = 2
        
        score += calidad_score
        desglose['calidad_perfil'] = {
            'puntos': calidad_score,
            'nivel': 'completo' if calidad_score >= 4 else 'incompleto'
        }
        
        # SCORE TOTAL (0-100)
        return {
            'score_total': min(score, 100),  # Máximo 100
            'prioridad': 'URGENTE' if score >= 70 else 'ALTA' if score >= 50 else 'MEDIA' if score >= 30 else 'BAJA',
            'desglose': desglose,
            'recomendacion': SistemaPrioridades._generar_recomendacion(desglose)
        }
    
    @staticmethod
    def _generar_recomendacion(desglose: Dict) -> str:
        """Genera recomendación de acción basada en el desglose"""
        
        recomendaciones = []
        
        # Urgencia temporal
        if desglose['urgencia_temporal']['nivel'] == 'muy_urgente':
            recomendaciones.append("⚠️ REVISAR INMEDIATAMENTE - Curso inicia pronto")
        
        # Completitud
        if desglose['completitud']['nivel'] in ['bajo', 'medio']:
            recomendaciones.append("📋 Solicitar documentos faltantes")
        
        # Fondos
        if desglose['fondos']['nivel'] == 'insuficiente':
            recomendaciones.append("💰 Gestionar patrocinador o plan de pago")
        
        # Tiempo de espera
        if desglose['tiempo_espera']['nivel'] in ['critico', 'alto']:
            recomendaciones.append("⏰ Esperando revisión hace tiempo")
        
        if not recomendaciones:
            recomendaciones.append("✅ Caso estándar - Revisar cuando sea posible")
        
        return " | ".join(recomendaciones)
    
    @staticmethod
    def ordenar_estudiantes_por_prioridad(
        estudiantes: List[Estudiante] = None,
        limite: int = None
    ) -> List[Dict]:
        """
        Ordena estudiantes por prioridad
        
        Args:
            estudiantes: Lista de estudiantes (si None, busca todos los pendientes)
            limite: Número máximo de resultados
            
        Returns:
            Lista ordenada de estudiantes con sus scores
        """
        db = get_db()
        
        try:
            # Si no se pasan estudiantes, buscar todos los pendientes
            if estudiantes is None:
                estudiantes = db.query(Estudiante).filter(
                    Estudiante.estado_procesamiento.in_([
                        'procesado_automaticamente',
                        'pendiente_revision_admin'
                    ])
                ).all()
            
            # Calcular score para cada estudiante
            estudiantes_con_score = []
            
            for est in estudiantes:
                score_info = SistemaPrioridades.calcular_score_prioridad(est)
                
                estudiantes_con_score.append({
                    'estudiante': est,
                    'estudiante_id': est.id,
                    'nombre': est.nombre_completo,
                    'especialidad': est.especialidad_interes,
                    'score': score_info['score_total'],
                    'prioridad': score_info['prioridad'],
                    'desglose': score_info['desglose'],
                    'recomendacion': score_info['recomendacion'],
                    'fecha_procesamiento': est.fecha_procesamiento_automatico
                })
            
            # Ordenar por score descendente
            estudiantes_con_score.sort(key=lambda x: x['score'], reverse=True)
            
            # Limitar resultados si se especifica
            if limite:
                estudiantes_con_score = estudiantes_con_score[:limite]
            
            return estudiantes_con_score
            
        finally:
            db.close()
    
    @staticmethod
    def obtener_estudiantes_urgentes(
        score_minimo: int = 70
    ) -> List[Dict]:
        """
        Obtiene solo los estudiantes con prioridad urgente
        
        Args:
            score_minimo: Score mínimo para considerar urgente
            
        Returns:
            Lista de estudiantes urgentes
        """
        todos = SistemaPrioridades.ordenar_estudiantes_por_prioridad()
        
        urgentes = [est for est in todos if est['score'] >= score_minimo]
        
        return urgentes
    
    @staticmethod
    def generar_reporte_prioridades() -> str:
        """
        Genera un reporte visual de prioridades
        
        Returns:
            String con el reporte formateado
        """
        estudiantes = SistemaPrioridades.ordenar_estudiantes_por_prioridad(limite=20)
        
        if not estudiantes:
            return "No hay estudiantes pendientes de revisión."
        
        reporte = f"""
╔══════════════════════════════════════════════════════════════╗
║              REPORTE DE PRIORIDADES - TOP 20                 ║
╚══════════════════════════════════════════════════════════════╝

Total pendientes: {len(estudiantes)}

"""
        
        for i, est in enumerate(estudiantes, 1):
            icono_prioridad = {
                'URGENTE': '🔴',
                'ALTA': '🟠',
                'MEDIA': '🟡',
                'BAJA': '🟢'
            }.get(est['prioridad'], '⚪')
            
            reporte += f"""
{i}. {icono_prioridad} [{est['prioridad']}] {est['nombre']}
   • Score: {est['score']}/100
   • Especialidad: {est['especialidad'] or 'No especificada'}
   • Urgencia: {est['desglose']['urgencia_temporal']['nivel']}
   • Completitud: {est['desglose']['completitud']['porcentaje_documentos']:.0f}%
   • Fondos: {est['desglose']['fondos']['nivel']}
   • Esperando: {est['desglose']['tiempo_espera']['horas_esperando']:.1f}h
   
   📋 {est['recomendacion']}

{'-' * 60}
"""
        
        return reporte
    
    @staticmethod
    def estadisticas_prioridades() -> Dict:
        """
        Genera estadísticas de distribución de prioridades
        
        Returns:
            Dict con estadísticas
        """
        estudiantes = SistemaPrioridades.ordenar_estudiantes_por_prioridad()
        
        if not estudiantes:
            return {'total': 0}
        
        urgente = len([e for e in estudiantes if e['prioridad'] == 'URGENTE'])
        alta = len([e for e in estudiantes if e['prioridad'] == 'ALTA'])
        media = len([e for e in estudiantes if e['prioridad'] == 'MEDIA'])
        baja = len([e for e in estudiantes if e['prioridad'] == 'BAJA'])
        
        score_promedio = sum([e['score'] for e in estudiantes]) / len(estudiantes)
        
        return {
            'total': len(estudiantes),
            'urgente': urgente,
            'alta': alta,
            'media': media,
            'baja': baja,
            'score_promedio': score_promedio,
            'distribucion': {
                'urgente_pct': (urgente / len(estudiantes)) * 100,
                'alta_pct': (alta / len(estudiantes)) * 100,
                'media_pct': (media / len(estudiantes)) * 100,
                'baja_pct': (baja / len(estudiantes)) * 100
            }
        }
