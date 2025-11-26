"""
Panel de Revisión para Administradores
Sistema semi-automatizado: Bot procesa, Admin revisa y aprueba manualmente antes de enviar
"""

from datetime import datetime
from typing import Dict, List, Optional
from modules.estudiantes import GestorEstudiantes, Estudiante
from modules.cursos import GestorCursos
from modules.fondos import GestorFondos
from modules.alojamiento import GestorAlojamiento
from modules.notificaciones import SistemaNotificaciones
from database.models import get_db


class PanelRevisionAdmin:
    """
    Panel de control para que admin revise toda la información
    procesada automáticamente por el bot antes de enviarla al estudiante
    """
    
    @staticmethod
    def obtener_estudiantes_pendientes_revision() -> List[Dict]:
        """
        Obtiene todos los estudiantes que han sido procesados automáticamente
        por el bot y están esperando revisión del admin
        
        Returns:
            Lista de estudiantes pendientes con toda su información
        """
        db = get_db()
        
        try:
            # Buscar estudiantes con estado procesado_automaticamente o pendiente_revision_admin
            estudiantes = db.query(Estudiante).filter(
                Estudiante.estado_procesamiento.in_([
                    'procesado_automaticamente',
                    'pendiente_revision_admin'
                ])
            ).order_by(Estudiante.fecha_procesamiento_automatico.desc()).all()
            
            resultado = []
            
            for est in estudiantes:
                # Obtener toda la información procesada
                info_completa = PanelRevisionAdmin._obtener_info_completa_estudiante(est.id)
                resultado.append(info_completa)
            
            return resultado
            
        except Exception as e:
            print(f"Error obteniendo estudiantes pendientes: {e}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def _obtener_info_completa_estudiante(estudiante_id: int) -> Dict:
        """
        Obtiene TODA la información procesada automáticamente para un estudiante:
        - Datos personales
        - Cursos sugeridos
        - Checklist de documentos
        - Verificación de fondos
        - Opciones de alojamiento
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Diccionario con toda la información
        """
        db = get_db()
        
        try:
            estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
            
            if not estudiante:
                return {'error': 'Estudiante no encontrado'}
            
            # 1. Datos personales del estudiante
            datos_personales = {
                'id': estudiante.id,
                'nombre_completo': estudiante.nombre_completo,
                'numero_pasaporte': estudiante.numero_pasaporte,
                'edad': estudiante.edad,
                'nacionalidad': estudiante.nacionalidad,
                'ciudad_origen': estudiante.ciudad_origen,
                'carrera_actual': estudiante.carrera_actual,
                'especialidad_interes': estudiante.especialidad_interes,
                'nivel_espanol': estudiante.nivel_espanol,
                'email': estudiante.email,
                'telefono': estudiante.telefono,
                'estado_procesamiento': estudiante.estado_procesamiento,
                'fecha_procesamiento_automatico': estudiante.fecha_procesamiento_automatico
            }
            
            # 2. Cursos sugeridos por el bot
            cursos_sugeridos = []
            if estudiante.especialidad_interes:
                cursos = GestorCursos.filtrar_cursos(
                    especialidad=estudiante.especialidad_interes.lower(),
                    nivel_idioma=estudiante.nivel_espanol.lower() if estudiante.nivel_espanol else None
                )
                
                for curso in cursos[:5]:  # Top 5 cursos
                    cursos_sugeridos.append({
                        'id': curso.id,
                        'nombre': curso.nombre,
                        'escuela': curso.escuela,
                        'ciudad': curso.ciudad,
                        'precio': curso.precio,
                        'duracion_meses': curso.duracion_meses,
                        'fecha_inicio': curso.fecha_inicio,
                        'nivel_idioma_requerido': curso.nivel_idioma_requerido,
                        'enlace_inscripcion': curso.enlace_inscripcion,
                        'curso_asignado': curso.id == estudiante.curso_asignado_id
                    })
            
            # 3. Checklist de documentos
            checklist = GestorEstudiantes.checklist_documentos(estudiante_id)
            
            # 4. Verificación de fondos
            verificacion_fondos = GestorFondos.verificar_fondos(estudiante_id)
            
            # 5. Opciones de alojamiento
            alojamientos_sugeridos = []
            if estudiante.curso_asignado_id:
                curso = db.query(GestorCursos.Curso).filter_by(id=estudiante.curso_asignado_id).first()
                if curso:
                    alojamientos = GestorAlojamiento.buscar_alojamientos(
                        ciudad=curso.ciudad,
                        disponible=True
                    )
                    
                    for aloj in alojamientos[:5]:  # Top 5 alojamientos
                        alojamientos_sugeridos.append({
                            'id': aloj.id,
                            'tipo': aloj.tipo,
                            'ciudad': aloj.ciudad,
                            'direccion': aloj.direccion,
                            'precio_mensual': aloj.precio_mensual,
                            'num_habitaciones': aloj.num_habitaciones,
                            'amueblado': aloj.amueblado,
                            'gastos_incluidos': aloj.gastos_incluidos,
                            'disponible_desde': aloj.disponible_desde
                        })
            
            return {
                'datos_personales': datos_personales,
                'cursos_sugeridos': cursos_sugeridos,
                'checklist_documentos': checklist,
                'verificacion_fondos': verificacion_fondos,
                'alojamientos_sugeridos': alojamientos_sugeridos,
                'fecha_procesamiento': estudiante.fecha_procesamiento_automatico,
                'notas_admin': estudiante.notas_admin,
                'modificaciones_admin': estudiante.modificaciones_admin
            }
            
        except Exception as e:
            return {'error': str(e)}
        finally:
            db.close()
    
    @staticmethod
    def ver_panel_estudiante(estudiante_id: int) -> Dict:
        """
        Ver el panel completo de revisión para un estudiante específico
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Información completa formateada para revisión
        """
        info = PanelRevisionAdmin._obtener_info_completa_estudiante(estudiante_id)
        
        if 'error' in info:
            return info
        
        # Formatear para visualización
        panel = {
            'estudiante': info['datos_personales'],
            'resumen': {
                'cursos_encontrados': len(info['cursos_sugeridos']),
                'documentos_completos': info['checklist_documentos']['porcentaje_completado'],
                'fondos_suficientes': info['verificacion_fondos']['fondos_suficientes'],
                'alojamientos_disponibles': len(info['alojamientos_sugeridos'])
            },
            'detalles': {
                'cursos': info['cursos_sugeridos'],
                'documentos': info['checklist_documentos'],
                'fondos': info['verificacion_fondos'],
                'alojamientos': info['alojamientos_sugeridos']
            },
            'estado_procesamiento': info['datos_personales']['estado_procesamiento'],
            'fecha_procesamiento': info['fecha_procesamiento'],
            'notas_admin_previas': info['notas_admin']
        }
        
        return panel
    
    @staticmethod
    def aprobar_y_preparar_envio(
        estudiante_id: int,
        admin_id: int,
        curso_seleccionado_id: Optional[int] = None,
        alojamiento_seleccionado_id: Optional[int] = None,
        notas_admin: Optional[str] = None,
        modificaciones: Optional[Dict] = None
    ) -> Dict:
        """
        Admin aprueba la información procesada y la prepara para envío manual
        
        Args:
            estudiante_id: ID del estudiante
            admin_id: ID del admin que aprueba
            curso_seleccionado_id: ID del curso seleccionado por admin (opcional)
            alojamiento_seleccionado_id: ID del alojamiento seleccionado (opcional)
            notas_admin: Notas u observaciones del admin
            modificaciones: Cambios realizados por el admin
            
        Returns:
            Confirmación de aprobación y paquete listo para enviar
        """
        db = get_db()
        
        try:
            estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
            
            if not estudiante:
                return {'exito': False, 'error': 'Estudiante no encontrado'}
            
            # Actualizar estado a aprobado
            estudiante.estado_procesamiento = 'aprobado_admin'
            estudiante.fecha_revision_admin = datetime.now()
            estudiante.admin_revisor_id = admin_id
            
            if notas_admin:
                estudiante.notas_admin = notas_admin
            
            if modificaciones:
                estudiante.modificaciones_admin = modificaciones
            
            # Si admin seleccionó curso específico
            if curso_seleccionado_id:
                resultado_curso = GestorEstudiantes.asignar_curso(estudiante_id, curso_seleccionado_id)
                if not resultado_curso.get('exito'):
                    return {'exito': False, 'error': 'Error asignando curso'}
            
            # Si admin seleccionó alojamiento
            if alojamiento_seleccionado_id:
                # Asignar alojamiento (con fecha tentativa)
                from datetime import timedelta
                fecha_inicio = datetime.now() + timedelta(days=60)  # Inicio en ~2 meses
                
                GestorAlojamiento.asignar_alojamiento(
                    estudiante_id=estudiante_id,
                    alojamiento_id=alojamiento_seleccionado_id,
                    fecha_inicio=fecha_inicio,
                    duracion_meses=12  # Por defecto 12 meses
                )
            
            db.commit()
            
            # Preparar paquete de información listo para enviar
            paquete_envio = PanelRevisionAdmin._preparar_paquete_envio(estudiante_id)
            
            # Notificar a otros admins
            SistemaNotificaciones._crear_alerta_admin(
                tipo='revision_completada',
                titulo=f'Revisión aprobada: {estudiante.nombre_completo}',
                descripcion=f'Admin {admin_id} ha aprobado la información. Lista para enviar al estudiante.',
                estudiante_id=estudiante_id,
                prioridad='normal'
            )
            
            return {
                'exito': True,
                'mensaje': 'Información aprobada y lista para envío manual',
                'estudiante_id': estudiante_id,
                'estado': 'aprobado_admin',
                'paquete_envio': paquete_envio
            }
            
        except Exception as e:
            db.rollback()
            return {'exito': False, 'error': str(e)}
        finally:
            db.close()
    
    @staticmethod
    def rechazar_y_solicitar_revision(
        estudiante_id: int,
        admin_id: int,
        motivo: str,
        acciones_requeridas: List[str]
    ) -> Dict:
        """
        Admin rechaza la información y solicita correcciones
        
        Args:
            estudiante_id: ID del estudiante
            admin_id: ID del admin
            motivo: Motivo del rechazo
            acciones_requeridas: Lista de acciones que deben tomarse
            
        Returns:
            Confirmación de rechazo
        """
        db = get_db()
        
        try:
            estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
            
            if not estudiante:
                return {'exito': False, 'error': 'Estudiante no encontrado'}
            
            # Actualizar estado
            estudiante.estado_procesamiento = 'rechazado_admin'
            estudiante.fecha_revision_admin = datetime.now()
            estudiante.admin_revisor_id = admin_id
            estudiante.notas_admin = f"RECHAZADO: {motivo}\n\nAcciones requeridas:\n" + "\n".join(f"- {accion}" for accion in acciones_requeridas)
            
            db.commit()
            
            # Notificar a admins sobre el rechazo
            SistemaNotificaciones._crear_alerta_admin(
                tipo='revision_rechazada',
                titulo=f'Información rechazada: {estudiante.nombre_completo}',
                descripcion=f'Motivo: {motivo}',
                estudiante_id=estudiante_id,
                prioridad='alta'
            )
            
            return {
                'exito': True,
                'mensaje': 'Información rechazada. Se requiere revisión manual.',
                'motivo': motivo,
                'acciones_requeridas': acciones_requeridas
            }
            
        except Exception as e:
            db.rollback()
            return {'exito': False, 'error': str(e)}
        finally:
            db.close()
    
    @staticmethod
    def _preparar_paquete_envio(estudiante_id: int) -> Dict:
        """
        Prepara el paquete completo de información listo para enviar al estudiante
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Paquete completo con toda la información
        """
        info = PanelRevisionAdmin._obtener_info_completa_estudiante(estudiante_id)
        
        if 'error' in info:
            return info
        
        # Formatear mensaje para el estudiante
        estudiante = info['datos_personales']
        
        mensaje = f"""
¡Hola {estudiante['nombre_completo']}! 👋

Hemos procesado tu solicitud y tenemos excelentes noticias para ti.

📚 **CURSO SELECCIONADO:**
"""
        
        # Curso asignado
        curso_asignado = next((c for c in info['cursos_sugeridos'] if c['curso_asignado']), None)
        if curso_asignado:
            mensaje += f"""
• Nombre: {curso_asignado['nombre']}
• Escuela: {curso_asignado['escuela']}
• Ciudad: {curso_asignado['ciudad']}
• Duración: {curso_asignado['duracion_meses']} meses
• Precio: {curso_asignado['precio']:,.2f}€
• Inicio: {curso_asignado['fecha_inicio'].strftime('%d/%m/%Y') if curso_asignado['fecha_inicio'] else 'Por confirmar'}
• Inscripción: {curso_asignado['enlace_inscripcion']}
"""
        
        # Documentos
        mensaje += f"""

📄 **DOCUMENTOS NECESARIOS:**
Progreso actual: {info['checklist_documentos']['porcentaje_completado']:.0f}%

Documentos obligatorios:
"""
        for doc in info['checklist_documentos']['obligatorios']:
            estado = "✅" if doc['completado'] else "⏳"
            mensaje += f"{estado} {doc['nombre']}\n"
        
        # Fondos
        fondos = info['verificacion_fondos']
        mensaje += f"""

💰 **SITUACIÓN ECONÓMICA:**
• Fondos necesarios: {fondos['fondos_minimos_requeridos']:,.2f}€
• Fondos disponibles: {fondos['fondos_disponibles']:,.2f}€
• Estado: {'✅ Suficiente' if fondos['fondos_suficientes'] else '⚠️ Requiere atención'}
"""
        
        if fondos.get('carta_patrocinio_generada'):
            mensaje += "• Carta de patrocinio: ✅ Generada\n"
        
        # Alojamiento
        if info['alojamientos_sugeridos']:
            aloj = info['alojamientos_sugeridos'][0]  # Primero recomendado
            mensaje += f"""

🏠 **ALOJAMIENTO RECOMENDADO:**
• Tipo: {aloj['tipo']}
• Ubicación: {aloj['direccion']}, {aloj['ciudad']}
• Precio: {aloj['precio_mensual']}€/mes
• Habitaciones: {aloj['num_habitaciones']}
• Amueblado: {'Sí' if aloj['amueblado'] else 'No'}
• Gastos incluidos: {'Sí' if aloj['gastos_incluidos'] else 'No'}
"""
        
        mensaje += """

📞 **PRÓXIMOS PASOS:**
1. Revisa toda la información
2. Confirma tu interés en el curso
3. Prepara los documentos pendientes
4. Nuestro equipo te guiará en el proceso de inscripción

¿Tienes preguntas? ¡Estamos aquí para ayudarte! 🇪🇸
"""
        
        return {
            'estudiante_id': estudiante_id,
            'mensaje_formateado': mensaje,
            'datos_completos': info,
            'archivos_adjuntos': []  # Aquí irían PDFs, cartas, etc.
        }
    
    @staticmethod
    def enviar_informacion_manual(
        estudiante_id: int,
        admin_id: int,
        canales: List[str] = None,
        mensaje_personalizado: Optional[str] = None
    ) -> Dict:
        """
        ENVÍO MANUAL: Admin envía la información aprobada al estudiante
        
        Args:
            estudiante_id: ID del estudiante
            admin_id: ID del admin que envía
            canales: Lista de canales de comunicación ['telegram', 'email', 'whatsapp']
            mensaje_personalizado: Mensaje adicional del admin (opcional)
            
        Returns:
            Confirmación de envío
        """
        db = get_db()
        
        try:
            estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
            
            if not estudiante:
                return {'exito': False, 'error': 'Estudiante no encontrado'}
            
            # Verificar que esté aprobado
            if estudiante.estado_procesamiento != 'aprobado_admin':
                return {
                    'exito': False,
                    'error': 'El estudiante debe estar aprobado antes de enviar'
                }
            
            # Obtener paquete de envío
            paquete = PanelRevisionAdmin._preparar_paquete_envio(estudiante_id)
            
            if 'error' in paquete:
                return {'exito': False, 'error': paquete['error']}
            
            # Mensaje final
            mensaje_final = paquete['mensaje_formateado']
            
            if mensaje_personalizado:
                mensaje_final = f"{mensaje_personalizado}\n\n{'-'*50}\n\n{mensaje_final}"
            
            # Enviar por los canales especificados
            if not canales:
                canales = ['telegram', 'email']
            
            resultado_envio = SistemaNotificaciones.notificar_estudiante(
                estudiante_id=estudiante_id,
                mensaje=mensaje_final,
                titulo="📬 Tu Plan de Estudios en España está listo",
                canales=canales,
                prioridad='alta'
            )
            
            # Actualizar estado a enviado
            estudiante.estado_procesamiento = 'enviado_estudiante'
            db.commit()
            
            # Alerta interna
            SistemaNotificaciones._crear_alerta_admin(
                tipo='informacion_enviada',
                titulo=f'Información enviada: {estudiante.nombre_completo}',
                descripcion=f'Admin {admin_id} envió la información por: {", ".join(canales)}',
                estudiante_id=estudiante_id,
                prioridad='normal'
            )
            
            return {
                'exito': True,
                'mensaje': 'Información enviada exitosamente al estudiante',
                'canales_enviados': resultado_envio['exitosos'],
                'canales_fallidos': resultado_envio['fallidos'],
                'fecha_envio': datetime.now(),
                'estado_final': 'enviado_estudiante'
            }
            
        except Exception as e:
            db.rollback()
            return {'exito': False, 'error': str(e)}
        finally:
            db.close()
    
    @staticmethod
    def estadisticas_revision() -> Dict:
        """
        Estadísticas del panel de revisión para admins
        
        Returns:
            Estadísticas generales
        """
        db = get_db()
        
        try:
            total_pendientes = db.query(Estudiante).filter(
                Estudiante.estado_procesamiento.in_([
                    'procesado_automaticamente',
                    'pendiente_revision_admin'
                ])
            ).count()
            
            total_aprobados = db.query(Estudiante).filter(
                Estudiante.estado_procesamiento == 'aprobado_admin'
            ).count()
            
            total_enviados = db.query(Estudiante).filter(
                Estudiante.estado_procesamiento == 'enviado_estudiante'
            ).count()
            
            total_rechazados = db.query(Estudiante).filter(
                Estudiante.estado_procesamiento == 'rechazado_admin'
            ).count()
            
            return {
                'pendientes_revision': total_pendientes,
                'aprobados_pendiente_envio': total_aprobados,
                'enviados_estudiante': total_enviados,
                'rechazados': total_rechazados,
                'total_procesados': total_aprobados + total_enviados + total_rechazados
            }
            
        except Exception as e:
            return {'error': str(e)}
        finally:
            db.close()
