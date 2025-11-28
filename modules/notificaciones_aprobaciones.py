"""
Sistema de notificaciones para aprobaciones de admin
Envía notificaciones automáticas cuando el admin aprueba/rechaza solicitudes
"""

from modules.notificaciones import SistemaNotificaciones
from api.notificaciones_routes import crear_notificacion
from database.models import get_db
from sqlalchemy.orm import Session

class NotificacionesAprobaciones:
    """Maneja notificaciones automáticas para aprobaciones del admin"""
    
    @staticmethod
    def notificar_aprobacion_alojamiento(estudiante_id: int, estado: str, comentarios_admin: str = ""):
        """Envía notificación cuando el admin procesa solicitud de alojamiento"""
        
        # Determinar el icono y mensaje según el estado
        if estado == 'aprobado':
            icono = '✅'
            titulo = "🏠 Solicitud de Alojamiento APROBADA"
            mensaje_base = "¡Excelente! Tu solicitud de alojamiento ha sido aprobada por nuestro equipo."
            url_accion = "/estudiante/alojamiento"
        else:  # rechazado
            icono = '❌'
            titulo = "🏠 Solicitud de Alojamiento RECHAZADA"
            mensaje_base = "Tu solicitud de alojamiento ha sido rechazada. Por favor revisa los comentarios."
            url_accion = "/estudiante/alojamiento"
        
        # Construir mensaje completo
        mensaje = mensaje_base
        if comentarios_admin:
            mensaje += f"\n\n💬 Comentarios del equipo:\n{comentarios_admin}"
        
        mensaje += f"\n\n👆 Haz clic para ver los detalles completos."
        
        # Crear notificación en la base de datos (campanita)
        db = next(get_db())
        crear_notificacion(
            db=db,
            estudiante_id=estudiante_id,
            tipo='aprobacion_alojamiento',
            titulo=titulo,
            mensaje=mensaje,
            url_accion=url_accion,
            icono=icono,
            prioridad='alta'
        )
        
        # Enviar email automático
        resultado_email = SistemaNotificaciones.notificar_estudiante(
            estudiante_id=estudiante_id,
            mensaje=f"""
{mensaje_base}

{f'Comentarios del equipo: {comentarios_admin}' if comentarios_admin else ''}

Para ver todos los detalles, accede a tu panel de estudiante en la sección de Alojamiento.

¡Estamos aquí para ayudarte en todo el proceso!
            """,
            titulo=titulo,
            canales=['email'],
            prioridad='alta'
        )
        
        return {
            'notificacion_web': True,
            'email_enviado': 'email' in resultado_email.get('exitosos', [])
        }
    
    @staticmethod
    def notificar_aprobacion_financiera(estudiante_id: int, estado: str, comentarios_admin: str = ""):
        """Envía notificación cuando el admin procesa solicitud financiera"""
        
        if estado == 'aprobado':
            icono = '✅'
            titulo = "💰 Solicitud de Información Financiera APROBADA"
            mensaje_base = "¡Perfecto! Tu información financiera ha sido aprobada por nuestro equipo."
            url_accion = "/estudiante/financiera"
        else:
            icono = '❌'
            titulo = "💰 Solicitud de Información Financiera RECHAZADA"
            mensaje_base = "Tu información financiera necesita ajustes. Por favor revisa los comentarios."
            url_accion = "/estudiante/financiera"
        
        mensaje = mensaje_base
        if comentarios_admin:
            mensaje += f"\n\n💬 Comentarios del equipo:\n{comentarios_admin}"
        
        mensaje += f"\n\n👆 Haz clic para ver los detalles completos."
        
        # Notificación web
        db = next(get_db())
        crear_notificacion(
            db=db,
            estudiante_id=estudiante_id,
            tipo='aprobacion_financiera',
            titulo=titulo,
            mensaje=mensaje,
            url_accion=url_accion,
            icono=icono,
            prioridad='alta'
        )
        
        # Email
        resultado_email = SistemaNotificaciones.notificar_estudiante(
            estudiante_id=estudiante_id,
            mensaje=f"""
{mensaje_base}

{f'Comentarios del equipo: {comentarios_admin}' if comentarios_admin else ''}

Para ver todos los detalles, accede a tu panel de estudiante en la sección de Información Financiera.

¡Estamos aquí para ayudarte en todo el proceso!
            """,
            titulo=titulo,
            canales=['email'],
            prioridad='alta'
        )
        
        return {
            'notificacion_web': True,
            'email_enviado': 'email' in resultado_email.get('exitosos', [])
        }
    
    @staticmethod
    def notificar_aprobacion_seguro_medico(estudiante_id: int, estado: str, comentarios_admin: str = ""):
        """Envía notificación cuando el admin procesa solicitud de seguro médico"""
        
        if estado == 'aprobado':
            icono = '✅'
            titulo = "🏥 Solicitud de Seguro Médico APROBADA"
            mensaje_base = "¡Excelente! Tu solicitud de gestión de seguro médico ha sido aprobada."
            url_accion = "/estudiante/seguro-medico"
        else:
            icono = '❌'
            titulo = "🏥 Solicitud de Seguro Médico RECHAZADA"
            mensaje_base = "Tu solicitud de seguro médico ha sido rechazada. Por favor revisa los comentarios."
            url_accion = "/estudiante/seguro-medico"
        
        mensaje = mensaje_base
        if comentarios_admin:
            mensaje += f"\n\n💬 Comentarios del equipo:\n{comentarios_admin}"
        
        mensaje += f"\n\n👆 Haz clic para ver los detalles completos."
        
        # Notificación web
        db = next(get_db())
        crear_notificacion(
            db=db,
            estudiante_id=estudiante_id,
            tipo='aprobacion_seguro_medico',
            titulo=titulo,
            mensaje=mensaje,
            url_accion=url_accion,
            icono=icono,
            prioridad='alta'
        )
        
        # Email
        resultado_email = SistemaNotificaciones.notificar_estudiante(
            estudiante_id=estudiante_id,
            mensaje=f"""
{mensaje_base}

{f'Comentarios del equipo: {comentarios_admin}' if comentarios_admin else ''}

Para ver todos los detalles, accede a tu panel de estudiante en la sección de Seguro Médico.

Te contactaremos pronto con las opciones de seguro disponibles para ti.

¡Estamos aquí para ayudarte en todo el proceso!
            """,
            titulo=titulo,
            canales=['email'],
            prioridad='alta'
        )
        
        return {
            'notificacion_web': True,
            'email_enviado': 'email' in resultado_email.get('exitosos', [])
        }
    
    @staticmethod
    def notificar_proceso_aprobacion(estudiante_id: int, tipo_solicitud: str, estado: str, comentarios_admin: str = ""):
        """Función general para procesar cualquier tipo de aprobación"""
        
        if tipo_solicitud == 'alojamiento':
            return NotificacionesAprobaciones.notificar_aprobacion_alojamiento(
                estudiante_id, estado, comentarios_admin
            )
        elif tipo_solicitud == 'financiera':
            return NotificacionesAprobaciones.notificar_aprobacion_financiera(
                estudiante_id, estado, comentarios_admin
            )
        elif tipo_solicitud == 'seguro_medico':
            return NotificacionesAprobaciones.notificar_aprobacion_seguro_medico(
                estudiante_id, estado, comentarios_admin
            )
        else:
            print(f"⚠️ Tipo de solicitud no reconocido: {tipo_solicitud}")
            return {'error': 'Tipo de solicitud no válido'}