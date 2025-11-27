from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import FechaImportante, Estudiante
from api.email_utils import enviar_email
import os

class GestorAlertasFechas:
    """Gestor de alertas automáticas para fechas importantes"""
    
    TIPOS_FECHA = {
        'entrevista_consular': 'Entrevista Consular',
        'vencimiento_pasaporte': 'Vencimiento de Pasaporte',
        'vencimiento_documento': 'Vencimiento de Documento',
        'deadline_aplicacion': 'Fecha Límite de Aplicación',
        'cita_visa': 'Cita para Visa',
        'inicio_clases': 'Inicio de Clases',
        'pago_matricula': 'Pago de Matrícula',
        'renovacion_visa': 'Renovación de Visa',
        'entrega_documentos': 'Entrega de Documentos',
        'otro': 'Otro'
    }
    
    @staticmethod
    def agregar_fecha(db: Session, estudiante_id: int, tipo_fecha: str, fecha: datetime, descripcion: str = None):
        """Agrega una nueva fecha importante para seguimiento"""
        nueva_fecha = FechaImportante(
            estudiante_id=estudiante_id,
            tipo_fecha=tipo_fecha,
            fecha=fecha,
            descripcion=descripcion
        )
        db.add(nueva_fecha)
        db.commit()
        db.refresh(nueva_fecha)
        return nueva_fecha
    
    @staticmethod
    def obtener_fechas_estudiante(db: Session, estudiante_id: int, incluir_completadas: bool = False):
        """Obtiene todas las fechas importantes de un estudiante"""
        query = db.query(FechaImportante).filter(FechaImportante.estudiante_id == estudiante_id)
        
        if not incluir_completadas:
            query = query.filter(FechaImportante.completada == False)
        
        return query.order_by(FechaImportante.fecha).all()
    
    @staticmethod
    def obtener_fechas_proximas(db: Session, dias: int = 30):
        """Obtiene todas las fechas próximas (próximos N días) de todos los estudiantes"""
        fecha_limite = datetime.utcnow() + timedelta(days=dias)
        return db.query(FechaImportante).filter(
            FechaImportante.fecha <= fecha_limite,
            FechaImportante.fecha >= datetime.utcnow(),
            FechaImportante.completada == False
        ).order_by(FechaImportante.fecha).all()
    
    @staticmethod
    def marcar_completada(db: Session, fecha_id: int):
        """Marca una fecha como completada"""
        fecha = db.query(FechaImportante).filter(FechaImportante.id == fecha_id).first()
        if fecha:
            fecha.completada = True
            db.commit()
            return True
        return False
    
    @staticmethod
    def eliminar_fecha(db: Session, fecha_id: int):
        """Elimina una fecha importante"""
        fecha = db.query(FechaImportante).filter(FechaImportante.id == fecha_id).first()
        if fecha:
            db.delete(fecha)
            db.commit()
            return True
        return False
    
    @staticmethod
    def verificar_alertas_pendientes(db: Session):
        """
        Verifica todas las fechas y envía alertas según corresponda
        Debe ejecutarse diariamente (scheduler)
        """
        hoy = datetime.utcnow()
        alertas_enviadas = []
        
        # Obtener todas las fechas activas
        fechas_activas = db.query(FechaImportante).filter(
            FechaImportante.completada == False,
            FechaImportante.fecha >= hoy
        ).all()
        
        for fecha in fechas_activas:
            dias_restantes = (fecha.fecha - hoy).days
            
            # Verificar si corresponde enviar alerta de 30 días
            if dias_restantes <= 30 and not fecha.alertado_30d:
                if GestorAlertasFechas._enviar_alerta(db, fecha, 30):
                    fecha.alertado_30d = True
                    alertas_enviadas.append({
                        'fecha_id': fecha.id,
                        'tipo': '30 días',
                        'estudiante_id': fecha.estudiante_id
                    })
            
            # Verificar si corresponde enviar alerta de 15 días
            if dias_restantes <= 15 and not fecha.alertado_15d:
                if GestorAlertasFechas._enviar_alerta(db, fecha, 15):
                    fecha.alertado_15d = True
                    alertas_enviadas.append({
                        'fecha_id': fecha.id,
                        'tipo': '15 días',
                        'estudiante_id': fecha.estudiante_id
                    })
            
            # Verificar si corresponde enviar alerta de 7 días
            if dias_restantes <= 7 and not fecha.alertado_7d:
                if GestorAlertasFechas._enviar_alerta(db, fecha, 7):
                    fecha.alertado_7d = True
                    alertas_enviadas.append({
                        'fecha_id': fecha.id,
                        'tipo': '7 días',
                        'estudiante_id': fecha.estudiante_id
                    })
            
            # Verificar si corresponde enviar alerta de 1 día
            if dias_restantes <= 1 and not fecha.alertado_1d:
                if GestorAlertasFechas._enviar_alerta(db, fecha, 1):
                    fecha.alertado_1d = True
                    alertas_enviadas.append({
                        'fecha_id': fecha.id,
                        'tipo': '1 día',
                        'estudiante_id': fecha.estudiante_id
                    })
        
        db.commit()
        return alertas_enviadas
    
    @staticmethod
    def _enviar_alerta(db: Session, fecha: FechaImportante, dias_restantes: int):
        """Envía email de alerta al estudiante"""
        # Obtener datos del estudiante
        estudiante = db.query(Estudiante).filter(Estudiante.id == fecha.estudiante_id).first()
        if not estudiante or not estudiante.email:
            return False
        
        # Determinar urgencia
        if dias_restantes <= 1:
            urgencia = "¡URGENTE!"
            color = "#dc3545"
            emoji = "🚨"
        elif dias_restantes <= 7:
            urgencia = "IMPORTANTE"
            color = "#ffc107"
            emoji = "⚠️"
        else:
            urgencia = "Recordatorio"
            color = "#667eea"
            emoji = "📅"
        
        # Obtener nombre del tipo de fecha
        tipo_nombre = GestorAlertasFechas.TIPOS_FECHA.get(fecha.tipo_fecha, fecha.tipo_fecha)
        
        # Formatear fecha
        fecha_formateada = fecha.fecha.strftime("%d/%m/%Y")
        if fecha.fecha.hour > 0:
            fecha_formateada += f" a las {fecha.fecha.strftime('%H:%M')}"
        
        # Template HTML del email
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, {color} 0%, {color}dd 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .content {{ background: white; padding: 30px; border: 1px solid #e2e8f0; border-top: none; }}
                .fecha-box {{ background: #f8f9fa; border-left: 4px solid {color}; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .fecha-box h2 {{ margin: 0 0 10px 0; color: {color}; font-size: 22px; }}
                .dias-restantes {{ font-size: 48px; font-weight: bold; color: {color}; text-align: center; margin: 20px 0; }}
                .descripcion {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                .acciones {{ margin-top: 30px; text-align: center; }}
                .btn {{ display: inline-block; background: {color}; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 5px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #718096; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{emoji} {urgencia}</h1>
                    <p style="margin: 10px 0 0 0; font-size: 18px;">Recordatorio de Fecha Importante</p>
                </div>
                <div class="content">
                    <p>Hola <strong>{estudiante.nombre}</strong>,</p>
                    
                    <div class="fecha-box">
                        <h2>{tipo_nombre}</h2>
                        <p style="margin: 5px 0; font-size: 16px;">📅 <strong>{fecha_formateada}</strong></p>
                    </div>
                    
                    <div class="dias-restantes">
                        {dias_restantes} día{"s" if dias_restantes != 1 else ""}
                    </div>
                    <p style="text-align: center; color: #718096;">{"Quedan solo" if dias_restantes > 1 else "Queda solo"} <strong>{dias_restantes} día{"s" if dias_restantes != 1 else ""}</strong> para esta fecha importante.</p>
                    
                    {f'<div class="descripcion"><strong>Detalles:</strong><br>{fecha.descripcion}</div>' if fecha.descripcion else ''}
                    
                    <div style="background: #e8f4fd; border-left: 4px solid #2196f3; padding: 15px; margin: 20px 0; border-radius: 5px;">
                        <strong>💡 Recomendaciones:</strong>
                        <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                            {"<li>Verifica que tengas todos los documentos necesarios</li>" if fecha.tipo_fecha in ['entrevista_consular', 'cita_visa'] else ""}
                            {"<li>Revisa los requisitos específicos de tu cita</li>" if fecha.tipo_fecha == 'cita_visa' else ""}
                            {"<li>Practica tus respuestas con nuestro simulador</li>" if fecha.tipo_fecha == 'entrevista_consular' else ""}
                            {"<li>Llega con 15-30 minutos de anticipación</li>" if fecha.tipo_fecha in ['entrevista_consular', 'cita_visa'] else ""}
                            {"<li>Renueva este documento con anticipación</li>" if 'vencimiento' in fecha.tipo_fecha else ""}
                            {"<li>Completa tu aplicación con todos los datos requeridos</li>" if fecha.tipo_fecha == 'deadline_aplicacion' else ""}
                            <li>Contacta a nuestro equipo si necesitas ayuda</li>
                        </ul>
                    </div>
                    
                    <div class="acciones">
                        <a href="{os.getenv('FRONTEND_URL', 'https://bot-visas-estudio.vercel.app')}/estudiante/dashboard" class="btn">
                            📋 Ver Mi Dashboard
                        </a>
                        <a href="{os.getenv('FRONTEND_URL', 'https://bot-visas-estudio.vercel.app')}/estudiante/alertas" class="btn" style="background: #28a745;">
                            📅 Ver Todas Mis Fechas
                        </a>
                    </div>
                    
                    <div class="footer">
                        <p>Recibiste este email porque tienes fechas importantes registradas en tu perfil.</p>
                        <p>🎓 <strong>Agencia Educativa España</strong><br>
                        Tu éxito es nuestra misión</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Asunto del email
        if dias_restantes <= 1:
            asunto = f"🚨 ¡MAÑANA! {tipo_nombre} - {fecha_formateada}"
        elif dias_restantes <= 7:
            asunto = f"⚠️ {tipo_nombre} en {dias_restantes} días - {fecha_formateada}"
        else:
            asunto = f"📅 Recordatorio: {tipo_nombre} - {fecha_formateada}"
        
        # Enviar email
        try:
            enviar_email(
                destinatario=estudiante.email,
                asunto=asunto,
                contenido_html=html
            )
            return True
        except Exception as e:
            print(f"❌ Error enviando alerta: {e}")
            return False
    
    @staticmethod
    def generar_ics(fecha: FechaImportante, estudiante: Estudiante):
        """Genera archivo .ics para agregar a calendario"""
        tipo_nombre = GestorAlertasFechas.TIPOS_FECHA.get(fecha.tipo_fecha, fecha.tipo_fecha)
        
        # Formato fecha para iCalendar (YYYYMMDDTHHMMSS)
        fecha_inicio = fecha.fecha.strftime("%Y%m%dT%H%M%S")
        fecha_fin = (fecha.fecha + timedelta(hours=1)).strftime("%Y%m%dT%H%M%S")
        
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Agencia Educativa España//Alertas//ES
BEGIN:VEVENT
UID:{fecha.id}@agenciaeducativaespana.com
DTSTAMP:{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}
DTSTART:{fecha_inicio}
DTEND:{fecha_fin}
SUMMARY:{tipo_nombre}
DESCRIPTION:{fecha.descripcion if fecha.descripcion else tipo_nombre}
LOCATION:
STATUS:CONFIRMED
BEGIN:VALARM
TRIGGER:-P1D
ACTION:DISPLAY
DESCRIPTION:Recordatorio: {tipo_nombre} mañana
END:VALARM
BEGIN:VALARM
TRIGGER:-P7D
ACTION:DISPLAY
DESCRIPTION:Recordatorio: {tipo_nombre} en 7 días
END:VALARM
END:VEVENT
END:VCALENDAR"""
        
        return ics_content
