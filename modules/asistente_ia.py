"""
Sistema de Sugerencias Automáticas con IA
Bot sugiere acciones al admin según situación del estudiante
"""

from typing import Dict, List
from modules.estudiantes import Estudiante
from modules.fondos import GestorFondos


class AsistenteIA:
    """Asistente inteligente para admins"""
    
    @staticmethod
    def analizar_estudiante(estudiante_id: int) -> Dict:
        """
        Analiza situación y sugiere acciones
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Dict con análisis y sugerencias
        """
        from modules.estudiantes import GestorEstudiantes
        from modules.panel_revision_admin import PanelRevisionAdmin
        
        # Obtener información completa
        info = PanelRevisionAdmin._obtener_info_completa_estudiante(estudiante_id)
        estudiante = info['datos_personales']
        
        sugerencias = []
        prioridad_general = 'normal'
        
        # ANÁLISIS DE FONDOS
        fondos = info['verificacion_fondos']
        if not fondos['fondos_suficientes']:
            deficit = fondos.get('deficit', 0)
            
            if deficit > 5000:
                sugerencias.append({
                    'tipo': 'fondos_critico',
                    'titulo': '💰 Déficit significativo de fondos',
                    'descripcion': f'Faltan {deficit:,.2f}€. Requiere solución urgente.',
                    'acciones': [
                        'Buscar patrocinador (familiar en España)',
                        'Generar carta de patrocinio automática',
                        'Explorar becas disponibles (hasta 30% descuento)',
                        'Proponer plan de pago mensual con escuela'
                    ],
                    'prioridad': 'urgente'
                })
                prioridad_general = 'urgente'
            else:
                sugerencias.append({
                    'tipo': 'fondos_insuficientes',
                    'titulo': '💰 Fondos insuficientes',
                    'descripcion': f'Faltan {deficit:,.2f}€.',
                    'acciones': [
                        'Solicitar comprobantes adicionales de fondos',
                        'Verificar si tiene ahorros no declarados',
                        'Generar carta de patrocinio'
                    ],
                    'prioridad': 'alta'
                })
                if prioridad_general == 'normal':
                    prioridad_general = 'alta'
        
        # ANÁLISIS DE DOCUMENTOS
        checklist = info['checklist_documentos']
        porcentaje_docs = checklist['porcentaje_completado']
        
        if porcentaje_docs < 50:
            sugerencias.append({
                'tipo': 'documentos_incompletos',
                'titulo': '📄 Muchos documentos pendientes',
                'descripcion': f'Solo {porcentaje_docs:.0f}% completado.',
                'acciones': [
                    'Enviar recordatorio urgente al estudiante',
                    'Ofrecer asistencia para obtener documentos',
                    'Programar llamada de seguimiento',
                    'Enviar guía paso a paso para cada documento'
                ],
                'prioridad': 'alta'
            })
            if prioridad_general == 'normal':
                prioridad_general = 'alta'
        elif porcentaje_docs < 100:
            docs_pendientes = len(checklist.get('pendientes', []))
            sugerencias.append({
                'tipo': 'documentos_casi_completos',
                'titulo': '📄 Últimos documentos pendientes',
                'descripcion': f'{docs_pendientes} documentos por completar.',
                'acciones': [
                    'Recordar documentos específicos faltantes',
                    'Verificar fechas de vencimiento'
                ],
                'prioridad': 'normal'
            })
        
        # ANÁLISIS DE CURSOS
        if not info['cursos_sugeridos']:
            sugerencias.append({
                'tipo': 'sin_cursos',
                'titulo': '🎓 No se encontraron cursos',
                'descripcion': 'No hay cursos disponibles para esta especialidad.',
                'acciones': [
                    'Ampliar búsqueda a especialidades relacionadas',
                    'Contactar escuelas directamente',
                    'Ofrecer alternativas de estudio'
                ],
                'prioridad': 'alta'
            })
            prioridad_general = 'alta'
        elif len(info['cursos_sugeridos']) == 1:
            sugerencias.append({
                'tipo': 'pocas_opciones',
                'titulo': '🎓 Solo 1 curso disponible',
                'descripcion': 'Opciones limitadas.',
                'acciones': [
                    'Buscar más opciones en otras ciudades',
                    'Verificar próximas convocatorias'
                ],
                'prioridad': 'normal'
            })
        
        # ANÁLISIS DE ALOJAMIENTO
        if estudiante.get('necesita_alojamiento') and not info['alojamientos_sugeridos']:
            sugerencias.append({
                'tipo': 'sin_alojamiento',
                'titulo': '🏠 No hay alojamientos disponibles',
                'descripcion': 'Estudiante necesita alojamiento pero no hay opciones.',
                'acciones': [
                    'Buscar en plataformas adicionales (Idealista, Fotocasa)',
                    'Ofrecer residencias estudiantiles',
                    'Contactar con escuela para opciones'
                ],
                'prioridad': 'alta'
            })
            if prioridad_general == 'normal':
                prioridad_general = 'alta'
        
        # ANÁLISIS TEMPORAL
        if estudiante.get('fecha_procesamiento_automatico'):
            from datetime import datetime
            horas_esperando = (datetime.now() - estudiante['fecha_procesamiento_automatico']).total_seconds() / 3600
            
            if horas_esperando > 48:
                sugerencias.append({
                    'tipo': 'tiempo_espera_critico',
                    'titulo': '⏰ Esperando revisión hace mucho tiempo',
                    'descripcion': f'{horas_esperando:.0f} horas sin atención.',
                    'acciones': [
                        'PRIORIZAR REVISIÓN INMEDIATA',
                        'Enviar disculpa al estudiante',
                        'Asignar a admin disponible'
                    ],
                    'prioridad': 'urgente'
                })
                prioridad_general = 'urgente'
        
        # RECOMENDACIÓN GENERAL
        if not sugerencias:
            recomendacion_general = "✅ Todo en orden. Proceder con aprobación estándar."
        else:
            recomendacion_general = f"⚠️ Se detectaron {len(sugerencias)} áreas que requieren atención."
        
        return {
            'estudiante_id': estudiante_id,
            'nombre': estudiante.get('nombre_completo'),
            'prioridad_general': prioridad_general,
            'total_sugerencias': len(sugerencias),
            'sugerencias': sugerencias,
            'recomendacion_general': recomendacion_general,
            'resumen_ejecutivo': AsistenteIA._generar_resumen(info, sugerencias)
        }
    
    @staticmethod
    def _generar_resumen(info: Dict, sugerencias: List[Dict]) -> str:
        """Genera resumen ejecutivo"""
        estudiante = info['datos_personales']
        fondos = info['verificacion_fondos']
        checklist = info['checklist_documentos']
        
        resumen = f"""
RESUMEN EJECUTIVO - {estudiante['nombre_completo']}

📊 ESTADO ACTUAL:
   • Fondos: {fondos['porcentaje_cobertura']:.0f}% cubiertos
   • Documentos: {checklist['porcentaje_completado']:.0f}% completados
   • Cursos disponibles: {len(info['cursos_sugeridos'])}
   • Alojamientos: {len(info['alojamientos_sugeridos'])}

⚠️ ACCIONES REQUERIDAS: {len(sugerencias)}
"""
        
        for sug in sugerencias[:3]:  # Top 3
            resumen += f"\n   • [{sug['prioridad'].upper()}] {sug['titulo']}"
        
        return resumen
