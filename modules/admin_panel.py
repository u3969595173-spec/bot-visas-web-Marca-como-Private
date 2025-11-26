"""
Panel administrativo y sistema de reportes
Dashboard con estadísticas, estudiantes activos, pagos, ingresos
"""

from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import func, and_, or_
from database.models import get_db
import json


class PanelAdministrativo:
    """Dashboard y reportes para administradores"""
    
    @staticmethod
    def dashboard() -> Dict:
        """
        Genera dashboard completo con todas las estadísticas principales
        
        Returns:
            Diccionario con métricas y estadísticas
        """
        from modules.estudiantes import Estudiante, EventoEstudiante
        from modules.cursos import Curso
        from modules.alojamiento import Alojamiento, PagoAlquiler
        from modules.fondos import Patrocinador
        from modules.notificaciones import AlertaAdmin
        
        db = get_db()
        hoy = datetime.utcnow()
        hace_30_dias = hoy - timedelta(days=30)
        
        # ===== ESTUDIANTES =====
        total_estudiantes = db.query(Estudiante).count()
        estudiantes_nuevos_mes = db.query(Estudiante).filter(
            Estudiante.created_at >= hace_30_dias
        ).count()
        
        estudiantes_por_estado_visa = db.query(
            Estudiante.estado_visa,
            func.count(Estudiante.id)
        ).group_by(Estudiante.estado_visa).all()
        
        estudiantes_por_prioridad = db.query(
            Estudiante.prioridad,
            func.count(Estudiante.id)
        ).group_by(Estudiante.prioridad).all()
        
        # ===== CURSOS =====
        total_cursos = db.query(Curso).filter(Curso.activo == True).count()
        estudiantes_con_curso = db.query(Estudiante).filter(
            Estudiante.curso_asignado_id != None
        ).count()
        estudiantes_sin_curso = total_estudiantes - estudiantes_con_curso
        
        cursos_mas_populares = db.query(
            Curso.nombre,
            func.count(Estudiante.id).label('num_estudiantes')
        ).join(
            Estudiante, Estudiante.curso_asignado_id == Curso.id
        ).group_by(Curso.id, Curso.nombre).order_by(
            func.count(Estudiante.id).desc()
        ).limit(5).all()
        
        # ===== VISAS =====
        visas_aprobadas = db.query(Estudiante).filter(
            Estudiante.estado_visa == 'aprobado'
        ).count()
        
        visas_rechazadas = db.query(Estudiante).filter(
            Estudiante.estado_visa == 'rechazado'
        ).count()
        
        visas_en_proceso = db.query(Estudiante).filter(
            Estudiante.estado_visa.in_(['documentos', 'cita_agendada'])
        ).count()
        
        tasa_aprobacion = (visas_aprobadas / (visas_aprobadas + visas_rechazadas) * 100) if (visas_aprobadas + visas_rechazadas) > 0 else 0
        
        # ===== EVENTOS PRÓXIMOS =====
        eventos_proximos_7d = db.query(EventoEstudiante).filter(
            EventoEstudiante.fecha_evento >= hoy,
            EventoEstudiante.fecha_evento <= hoy + timedelta(days=7),
            EventoEstudiante.completado == False
        ).count()
        
        citas_consulado_proximas = db.query(EventoEstudiante).filter(
            EventoEstudiante.tipo_evento == 'cita_consulado',
            EventoEstudiante.fecha_evento >= hoy,
            EventoEstudiante.completado == False
        ).count()
        
        # ===== ALOJAMIENTO =====
        total_alojamientos = db.query(Alojamiento).filter(Alojamiento.activo == True).count()
        alojamientos_disponibles = db.query(Alojamiento).filter(
            Alojamiento.disponible == True,
            Alojamiento.activo == True
        ).count()
        
        estudiantes_con_alojamiento = db.query(Estudiante).filter(
            Estudiante.alojamiento_asignado_id != None
        ).count()
        
        estudiantes_sin_alojamiento = db.query(Estudiante).filter(
            Estudiante.necesita_alojamiento == True,
            Estudiante.alojamiento_asignado_id == None
        ).count()
        
        # ===== PAGOS ALQUILER =====
        pagos_pendientes = db.query(PagoAlquiler).filter(
            PagoAlquiler.estado == 'pendiente',
            PagoAlquiler.fecha_vencimiento >= hoy
        ).count()
        
        pagos_atrasados = db.query(PagoAlquiler).filter(
            PagoAlquiler.estado == 'atrasado'
        ).count()
        
        monto_pagos_pendientes = db.query(
            func.sum(PagoAlquiler.monto)
        ).filter(
            PagoAlquiler.estado.in_(['pendiente', 'atrasado'])
        ).scalar() or 0
        
        # ===== FONDOS =====
        total_patrocinadores = db.query(Patrocinador).count()
        patrocinadores_verificados = db.query(Patrocinador).filter(
            Patrocinador.verificado == True
        ).count()
        
        estudiantes_con_fondos_insuficientes = db.query(Estudiante).filter(
            Estudiante.monto_fondos_disponibles < 10000  # Umbral aproximado
        ).count()
        
        # ===== ALERTAS =====
        alertas_pendientes = db.query(AlertaAdmin).filter(
            AlertaAdmin.resuelta == False
        ).count()
        
        alertas_urgentes = db.query(AlertaAdmin).filter(
            AlertaAdmin.resuelta == False,
            AlertaAdmin.prioridad == 'urgente'
        ).count()
        
        alertas_altas = db.query(AlertaAdmin).filter(
            AlertaAdmin.resuelta == False,
            AlertaAdmin.prioridad == 'alta'
        ).count()
        
        # ===== COMPILAR DASHBOARD =====
        dashboard = {
            'fecha_generacion': hoy,
            'resumen': {
                'total_estudiantes': total_estudiantes,
                'estudiantes_nuevos_mes': estudiantes_nuevos_mes,
                'visas_aprobadas': visas_aprobadas,
                'visas_en_proceso': visas_en_proceso,
                'tasa_aprobacion': round(tasa_aprobacion, 1),
                'alertas_pendientes': alertas_pendientes,
                'alertas_urgentes': alertas_urgentes
            },
            'estudiantes': {
                'total': total_estudiantes,
                'nuevos_mes': estudiantes_nuevos_mes,
                'con_curso': estudiantes_con_curso,
                'sin_curso': estudiantes_sin_curso,
                'con_alojamiento': estudiantes_con_alojamiento,
                'sin_alojamiento': estudiantes_sin_alojamiento,
                'por_estado_visa': dict(estudiantes_por_estado_visa),
                'por_prioridad': dict(estudiantes_por_prioridad)
            },
            'cursos': {
                'total_activos': total_cursos,
                'estudiantes_inscritos': estudiantes_con_curso,
                'mas_populares': [
                    {'nombre': c[0], 'estudiantes': c[1]}
                    for c in cursos_mas_populares
                ]
            },
            'visas': {
                'aprobadas': visas_aprobadas,
                'rechazadas': visas_rechazadas,
                'en_proceso': visas_en_proceso,
                'tasa_aprobacion': round(tasa_aprobacion, 1),
                'citas_consulado_proximas': citas_consulado_proximas
            },
            'eventos': {
                'proximos_7_dias': eventos_proximos_7d,
                'citas_consulado': citas_consulado_proximas
            },
            'alojamiento': {
                'total': total_alojamientos,
                'disponibles': alojamientos_disponibles,
                'ocupados': total_alojamientos - alojamientos_disponibles,
                'estudiantes_con_alojamiento': estudiantes_con_alojamiento,
                'estudiantes_sin_alojamiento': estudiantes_sin_alojamiento
            },
            'pagos': {
                'pendientes': pagos_pendientes,
                'atrasados': pagos_atrasados,
                'monto_total_pendiente': round(monto_pagos_pendientes, 2)
            },
            'fondos': {
                'total_patrocinadores': total_patrocinadores,
                'verificados': patrocinadores_verificados,
                'estudiantes_fondos_insuficientes': estudiantes_con_fondos_insuficientes
            },
            'alertas': {
                'pendientes': alertas_pendientes,
                'urgentes': alertas_urgentes,
                'altas': alertas_altas,
                'normales': alertas_pendientes - alertas_urgentes - alertas_altas
            }
        }
        
        return dashboard
    
    @staticmethod
    def reporte_estudiantes_activos() -> List[Dict]:
        """Genera reporte de estudiantes activos con información clave"""
        from modules.estudiantes import Estudiante, GestorEstudiantes
        from modules.cursos import GestorCursos
        from modules.fondos import GestorFondos
        
        db = get_db()
        estudiantes = db.query(Estudiante).filter(
            Estudiante.estado_visa.in_(['no_iniciado', 'documentos', 'cita_agendada'])
        ).all()
        
        reporte = []
        for est in estudiantes:
            # Obtener curso
            curso = None
            if est.curso_asignado_id:
                curso = GestorCursos.obtener_curso_por_id(est.curso_asignado_id)
            
            # Verificar fondos
            verificacion_fondos = GestorFondos.verificar_fondos(est.id)
            
            # Progreso documentos
            total_docs = len(est.documentos_completados) + len(est.documentos_pendientes)
            progreso_docs = (len(est.documentos_completados) / total_docs * 100) if total_docs > 0 else 0
            
            reporte.append({
                'id': est.id,
                'nombre': est.nombre_completo,
                'pasaporte': est.numero_pasaporte,
                'edad': est.edad,
                'curso': curso.nombre if curso else 'Sin asignar',
                'estado_visa': est.estado_visa,
                'progreso_documentos': round(progreso_docs, 1),
                'fondos_estado': verificacion_fondos.get('estado', 'No verificado'),
                'fondos_porcentaje': round(verificacion_fondos.get('porcentaje_cobertura', 0), 1),
                'tiene_alojamiento': est.alojamiento_asignado_id is not None,
                'prioridad': est.prioridad,
                'fecha_cita': est.fecha_cita_consulado,
                'agente_asignado': est.agente_asignado or 'Sin asignar'
            })
        
        return reporte
    
    @staticmethod
    def reporte_financiero(mes: int = None, ano: int = None) -> Dict:
        """
        Genera reporte financiero de ingresos y gastos
        
        Args:
            mes: Mes específico (1-12) o None para mes actual
            ano: Año específico o None para año actual
            
        Returns:
            Diccionario con información financiera
        """
        from modules.alojamiento import PagoAlquiler, AsignacionAlojamiento
        
        db = get_db()
        
        if not mes:
            mes = datetime.utcnow().month
        if not ano:
            ano = datetime.utcnow().year
        
        # Ingresos por alquileres (pagos completados)
        ingresos_alquiler = db.query(
            func.sum(PagoAlquiler.monto)
        ).filter(
            PagoAlquiler.mes == mes,
            PagoAlquiler.ano == ano,
            PagoAlquiler.estado == 'pagado'
        ).scalar() or 0
        
        # Número de estudiantes que pagaron
        estudiantes_pagaron = db.query(
            func.count(func.distinct(PagoAlquiler.estudiante_id))
        ).filter(
            PagoAlquiler.mes == mes,
            PagoAlquiler.ano == ano,
            PagoAlquiler.estado == 'pagado'
        ).scalar() or 0
        
        # Pagos pendientes
        pagos_pendientes_monto = db.query(
            func.sum(PagoAlquiler.monto)
        ).filter(
            PagoAlquiler.mes == mes,
            PagoAlquiler.ano == ano,
            PagoAlquiler.estado.in_(['pendiente', 'atrasado'])
        ).scalar() or 0
        
        # Ingresos esperados totales
        ingresos_esperados = ingresos_alquiler + pagos_pendientes_monto
        
        # Tasa de cobro
        tasa_cobro = (ingresos_alquiler / ingresos_esperados * 100) if ingresos_esperados > 0 else 0
        
        return {
            'periodo': f'{mes:02d}/{ano}',
            'ingresos_alquiler': round(ingresos_alquiler, 2),
            'ingresos_esperados': round(ingresos_esperados, 2),
            'pagos_pendientes': round(pagos_pendientes_monto, 2),
            'tasa_cobro': round(tasa_cobro, 1),
            'estudiantes_pagaron': estudiantes_pagaron
        }
    
    @staticmethod
    def estadisticas_por_especialidad() -> List[Dict]:
        """Estadísticas de estudiantes por especialidad/área de estudio"""
        from modules.estudiantes import Estudiante
        
        db = get_db()
        
        stats = db.query(
            Estudiante.especialidad_interes,
            func.count(Estudiante.id).label('total'),
            func.sum(func.case([(Estudiante.estado_visa == 'aprobado', 1)], else_=0)).label('aprobados'),
            func.sum(func.case([(Estudiante.estado_visa == 'rechazado', 1)], else_=0)).label('rechazados')
        ).group_by(Estudiante.especialidad_interes).all()
        
        resultado = []
        for stat in stats:
            if stat[0]:  # Si tiene especialidad definida
                total = stat[1]
                aprobados = stat[2] or 0
                rechazados = stat[3] or 0
                tasa_exito = (aprobados / (aprobados + rechazados) * 100) if (aprobados + rechazados) > 0 else 0
                
                resultado.append({
                    'especialidad': stat[0],
                    'total_estudiantes': total,
                    'visas_aprobadas': aprobados,
                    'visas_rechazadas': rechazados,
                    'tasa_exito': round(tasa_exito, 1),
                    'en_proceso': total - aprobados - rechazados
                })
        
        return sorted(resultado, key=lambda x: x['total_estudiantes'], reverse=True)
    
    @staticmethod
    def estudiantes_requieren_atencion() -> List[Dict]:
        """
        Lista de estudiantes que requieren atención urgente
        
        Returns:
            Lista de estudiantes con situaciones que requieren acción
        """
        from modules.estudiantes import Estudiante, EventoEstudiante
        from modules.alojamiento import PagoAlquiler
        
        db = get_db()
        estudiantes_atencion = []
        
        # 1. Sin curso asignado (más de 3 días)
        hace_3_dias = datetime.utcnow() - timedelta(days=3)
        sin_curso = db.query(Estudiante).filter(
            Estudiante.curso_asignado_id == None,
            Estudiante.created_at <= hace_3_dias
        ).all()
        
        for est in sin_curso:
            estudiantes_atencion.append({
                'estudiante_id': est.id,
                'nombre': est.nombre_completo,
                'razon': 'Sin curso asignado',
                'prioridad': 'alta',
                'dias': (datetime.utcnow() - est.created_at).days,
                'accion_sugerida': 'Asignar curso según perfil'
            })
        
        # 2. Pagos atrasados
        pagos_atrasados = db.query(PagoAlquiler).filter(
            PagoAlquiler.estado == 'atrasado'
        ).all()
        
        for pago in pagos_atrasados:
            est = db.query(Estudiante).filter(Estudiante.id == pago.estudiante_id).first()
            if est:
                dias_atraso = (datetime.utcnow() - pago.fecha_vencimiento).days
                estudiantes_atencion.append({
                    'estudiante_id': est.id,
                    'nombre': est.nombre_completo,
                    'razon': f'Pago atrasado {dias_atraso} días',
                    'prioridad': 'urgente' if dias_atraso > 7 else 'alta',
                    'monto': pago.monto,
                    'accion_sugerida': 'Contactar para regularizar pago'
                })
        
        # 3. Cita en menos de 3 días sin documentos completos
        en_3_dias = datetime.utcnow() + timedelta(days=3)
        citas_proximas = db.query(EventoEstudiante).filter(
            EventoEstudiante.tipo_evento == 'cita_consulado',
            EventoEstudiante.fecha_evento <= en_3_dias,
            EventoEstudiante.completado == False
        ).all()
        
        for cita in citas_proximas:
            est = db.query(Estudiante).filter(Estudiante.id == cita.estudiante_id).first()
            if est and len(est.documentos_pendientes) > 0:
                estudiantes_atencion.append({
                    'estudiante_id': est.id,
                    'nombre': est.nombre_completo,
                    'razon': f'Cita en {(cita.fecha_evento - datetime.utcnow()).days} días con documentos pendientes',
                    'prioridad': 'urgente',
                    'documentos_pendientes': len(est.documentos_pendientes),
                    'accion_sugerida': 'Completar documentos urgentemente'
                })
        
        # 4. Fondos insuficientes
        estudiantes = db.query(Estudiante).filter(
            Estudiante.estado_visa.in_(['no_iniciado', 'documentos'])
        ).all()
        
        from modules.fondos import GestorFondos
        for est in estudiantes:
            verificacion = GestorFondos.verificar_fondos(est.id)
            if verificacion.get('porcentaje_cobertura', 100) < 80:
                estudiantes_atencion.append({
                    'estudiante_id': est.id,
                    'nombre': est.nombre_completo,
                    'razon': f'Fondos insuficientes ({verificacion.get("porcentaje_cobertura", 0):.0f}% del mínimo)',
                    'prioridad': 'alta',
                    'deficit': verificacion.get('deficit', 0),
                    'accion_sugerida': 'Gestionar fondos adicionales o patrocinador'
                })
        
        return estudiantes_atencion
    
    @staticmethod
    def exportar_dashboard_json(ruta_archivo: str = None) -> str:
        """
        Exporta el dashboard completo a JSON
        
        Args:
            ruta_archivo: Ruta donde guardar el archivo (opcional)
            
        Returns:
            JSON string del dashboard
        """
        dashboard = PanelAdministrativo.dashboard()
        
        # Convertir fechas a strings
        def date_converter(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")
        
        json_data = json.dumps(dashboard, indent=2, default=date_converter)
        
        if ruta_archivo:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(json_data)
        
        return json_data
    
    @staticmethod
    def generar_reporte_mensual(mes: int = None, ano: int = None) -> Dict:
        """
        Genera reporte mensual completo con todas las métricas
        
        Args:
            mes: Mes del reporte (1-12)
            ano: Año del reporte
            
        Returns:
            Diccionario con reporte completo
        """
        if not mes:
            mes = datetime.utcnow().month
        if not ano:
            ano = datetime.utcnow().year
        
        # Dashboard general
        dashboard = PanelAdministrativo.dashboard()
        
        # Reporte financiero
        financiero = PanelAdministrativo.reporte_financiero(mes, ano)
        
        # Estadísticas por especialidad
        especialidades = PanelAdministrativo.estadisticas_por_especialidad()
        
        # Estudiantes que requieren atención
        atencion = PanelAdministrativo.estudiantes_requieren_atencion()
        
        return {
            'periodo': f'{mes:02d}/{ano}',
            'fecha_generacion': datetime.utcnow(),
            'dashboard': dashboard,
            'financiero': financiero,
            'especialidades': especialidades,
            'estudiantes_atencion': atencion,
            'resumen_ejecutivo': {
                'total_estudiantes': dashboard['resumen']['total_estudiantes'],
                'nuevos_este_mes': dashboard['resumen']['estudiantes_nuevos_mes'],
                'visas_aprobadas': dashboard['resumen']['visas_aprobadas'],
                'tasa_aprobacion': dashboard['resumen']['tasa_aprobacion'],
                'ingresos_mes': financiero['ingresos_alquiler'],
                'alertas_urgentes': dashboard['resumen']['alertas_urgentes'],
                'estudiantes_requieren_atencion': len(atencion)
            }
        }
