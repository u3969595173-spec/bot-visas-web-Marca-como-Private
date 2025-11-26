"""
Sistema de alertas y notificaciones
Alertas internas para administradores y notificaciones para estudiantes
vía Email, WhatsApp y Telegram
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Bot
import requests
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database.models import get_db
import config

Base = declarative_base()


class Notificacion(Base):
    __tablename__ = 'notificaciones'
    
    id = Column(Integer, primary_key=True)
    destinatario_id = Column(Integer)  # ID del estudiante o admin
    tipo_destinatario = Column(String(50))  # estudiante, admin, patrocinador
    
    tipo_notificacion = Column(String(100))  # recordatorio, alerta, actualizacion, etc.
    canal = Column(String(50))  # email, telegram, whatsapp, sms
    
    titulo = Column(String(500))
    mensaje = Column(Text)
    prioridad = Column(String(20), default='normal')  # baja, normal, alta, urgente
    
    enviado = Column(Boolean, default=False)
    fecha_envio = Column(DateTime)
    error = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class AlertaAdmin(Base):
    __tablename__ = 'alertas_admin'
    
    id = Column(Integer, primary_key=True)
    tipo_alerta = Column(String(100))  # nuevo_estudiante, pago_pendiente, documento_vencido, etc.
    titulo = Column(String(500))
    descripcion = Column(Text)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    
    prioridad = Column(String(20), default='normal')
    leida = Column(Boolean, default=False)
    resuelta = Column(Boolean, default=False)
    
    fecha_resolucion = Column(DateTime)
    resuelto_por = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)


class SistemaNotificaciones:
    """Sistema de notificaciones multiplataforma"""
    
    # Configuración de email
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_FROM = "tu_email@gmail.com"  # Configurar
    EMAIL_PASSWORD = "tu_password"  # Usar variables de entorno
    
    @staticmethod
    def notificar_estudiante(
        estudiante_id: int,
        mensaje: str,
        titulo: str = "Notificación",
        canales: List[str] = ['telegram'],
        prioridad: str = 'normal'
    ) -> Dict:
        """
        Envía notificación a estudiante por múltiples canales
        
        Args:
            estudiante_id: ID del estudiante
            mensaje: Contenido del mensaje
            titulo: Título de la notificación
            canales: Lista de canales (email, telegram, whatsapp)
            prioridad: Nivel de prioridad
            
        Returns:
            Diccionario con resultado de envíos
        """
        from modules.estudiantes import GestorEstudiantes
        
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        resultados = {
            'exitosos': [],
            'fallidos': []
        }
        
        # Telegram
        if 'telegram' in canales and estudiante.telegram_id:
            exito = SistemaNotificaciones._enviar_telegram(
                estudiante.telegram_id,
                titulo,
                mensaje
            )
            
            if exito:
                resultados['exitosos'].append('telegram')
            else:
                resultados['fallidos'].append('telegram')
            
            SistemaNotificaciones._registrar_notificacion(
                estudiante_id, 'estudiante', 'telegram', titulo, mensaje, exito, prioridad
            )
        
        # Email
        if 'email' in canales and estudiante.email:
            exito = SistemaNotificaciones._enviar_email(
                estudiante.email,
                titulo,
                mensaje
            )
            
            if exito:
                resultados['exitosos'].append('email')
            else:
                resultados['fallidos'].append('email')
            
            SistemaNotificaciones._registrar_notificacion(
                estudiante_id, 'estudiante', 'email', titulo, mensaje, exito, prioridad
            )
        
        # WhatsApp (requiere API de WhatsApp Business)
        if 'whatsapp' in canales and estudiante.telefono:
            exito = SistemaNotificaciones._enviar_whatsapp(
                estudiante.telefono,
                mensaje
            )
            
            if exito:
                resultados['exitosos'].append('whatsapp')
            else:
                resultados['fallidos'].append('whatsapp')
            
            SistemaNotificaciones._registrar_notificacion(
                estudiante_id, 'estudiante', 'whatsapp', titulo, mensaje, exito, prioridad
            )
        
        return resultados
    
    @staticmethod
    def _enviar_telegram(telegram_id: int, titulo: str, mensaje: str) -> bool:
        """Envía mensaje por Telegram"""
        try:
            bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
            texto_completo = f"**{titulo}**\n\n{mensaje}"
            bot.send_message(
                chat_id=telegram_id,
                text=texto_completo,
                parse_mode='Markdown'
            )
            return True
        except Exception as e:
            print(f"Error enviando Telegram: {e}")
            return False
    
    @staticmethod
    def _enviar_email(email_destino: str, titulo: str, mensaje: str) -> bool:
        """Envía email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = titulo
            msg['From'] = SistemaNotificaciones.EMAIL_FROM
            msg['To'] = email_destino
            
            # Crear HTML
            html = f"""
            <html>
                <head></head>
                <body>
                    <h2>{titulo}</h2>
                    <p>{mensaje.replace(chr(10), '<br>')}</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        Este es un mensaje automático del Sistema de Gestión de Visas Estudiantiles.
                    </p>
                </body>
            </html>
            """
            
            part = MIMEText(html, 'html')
            msg.attach(part)
            
            # Enviar
            server = smtplib.SMTP(SistemaNotificaciones.SMTP_SERVER, SistemaNotificaciones.SMTP_PORT)
            server.starttls()
            server.login(SistemaNotificaciones.EMAIL_FROM, SistemaNotificaciones.EMAIL_PASSWORD)
            server.sendmail(SistemaNotificaciones.EMAIL_FROM, email_destino, msg.as_string())
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error enviando email: {e}")
            return False
    
    @staticmethod
    def _enviar_whatsapp(telefono: str, mensaje: str) -> bool:
        """
        Envía mensaje por WhatsApp usando API de WhatsApp Business
        Requiere configuración de WhatsApp Business API
        """
        try:
            # EJEMPLO: Usando Twilio WhatsApp API
            # Requiere cuenta de Twilio y configuración
            
            # from twilio.rest import Client
            # client = Client(TWILIO_SID, TWILIO_TOKEN)
            # message = client.messages.create(
            #     from_='whatsapp:+14155238886',
            #     body=mensaje,
            #     to=f'whatsapp:{telefono}'
            # )
            
            # Por ahora retornar False ya que requiere configuración específica
            print(f"WhatsApp a {telefono}: {mensaje}")
            return False
            
        except Exception as e:
            print(f"Error enviando WhatsApp: {e}")
            return False
    
    @staticmethod
    def _registrar_notificacion(
        destinatario_id: int,
        tipo_destinatario: str,
        canal: str,
        titulo: str,
        mensaje: str,
        exitoso: bool,
        prioridad: str
    ):
        """Registra notificación en base de datos"""
        db = get_db()
        
        notificacion = Notificacion(
            destinatario_id=destinatario_id,
            tipo_destinatario=tipo_destinatario,
            canal=canal,
            titulo=titulo,
            mensaje=mensaje,
            prioridad=prioridad,
            enviado=exitoso,
            fecha_envio=datetime.utcnow() if exitoso else None
        )
        
        db.add(notificacion)
        db.commit()
    
    @staticmethod
    def alertas_internas(tipo_alerta: str = None, estudiante_id: int = None) -> Dict:
        """
        Genera y envía alertas internas para administradores
        
        Args:
            tipo_alerta: Tipo específico de alerta o None para todas
            estudiante_id: ID de estudiante específico o None para todos
            
        Returns:
            Diccionario con alertas generadas
        """
        from modules.estudiantes import GestorEstudiantes, EventoEstudiante
        from modules.cursos import GestorCursos
        
        db = get_db()
        alertas_generadas = []
        
        # 1. Nuevos estudiantes sin curso asignado
        if not tipo_alerta or tipo_alerta == 'estudiante_sin_curso':
            from modules.estudiantes import Estudiante
            estudiantes_sin_curso = db.query(Estudiante).filter(
                Estudiante.curso_asignado_id == None,
                Estudiante.created_at >= datetime.utcnow() - timedelta(days=7)
            ).all()
            
            for estudiante in estudiantes_sin_curso:
                alerta = SistemaNotificaciones._crear_alerta_admin(
                    tipo='estudiante_sin_curso',
                    titulo=f'Estudiante sin curso: {estudiante.nombre_completo}',
                    descripcion=f'Estudiante registrado hace {(datetime.utcnow() - estudiante.created_at).days} días sin curso asignado',
                    estudiante_id=estudiante.id,
                    prioridad='alta'
                )
                alertas_generadas.append(alerta)
        
        # 2. Pagos pendientes (próximos módulo de pagos)
        
        # 3. Documentos vencidos o por vencer
        if not tipo_alerta or tipo_alerta == 'documentos_venciendo':
            from modules.estudiantes import DocumentoEstudiante
            en_30_dias = datetime.utcnow() + timedelta(days=30)
            
            docs_venciendo = db.query(DocumentoEstudiante).filter(
                DocumentoEstudiante.fecha_expiracion <= en_30_dias,
                DocumentoEstudiante.fecha_expiracion >= datetime.utcnow(),
                DocumentoEstudiante.estado == 'aprobado'
            ).all()
            
            for doc in docs_venciendo:
                dias_restantes = (doc.fecha_expiracion - datetime.utcnow()).days
                alerta = SistemaNotificaciones._crear_alerta_admin(
                    tipo='documento_venciendo',
                    titulo=f'Documento venciendo: {doc.tipo_documento}',
                    descripcion=f'Documento {doc.tipo_documento} vence en {dias_restantes} días',
                    estudiante_id=doc.estudiante_id,
                    prioridad='alta' if dias_restantes <= 7 else 'normal'
                )
                alertas_generadas.append(alerta)
        
        # 4. Citas próximas en consulado
        if not tipo_alerta or tipo_alerta == 'citas_proximas':
            eventos_proximos = GestorEstudiantes.obtener_eventos_proximos(dias=7)
            
            for evento in eventos_proximos:
                if evento.tipo_evento == 'cita_consulado':
                    dias = (evento.fecha_evento - datetime.utcnow()).days
                    alerta = SistemaNotificaciones._crear_alerta_admin(
                        tipo='cita_proxima',
                        titulo=f'Cita consulado en {dias} días',
                        descripcion=f'{evento.titulo} - {evento.descripcion}',
                        estudiante_id=evento.estudiante_id,
                        prioridad='urgente' if dias <= 2 else 'alta'
                    )
                    alertas_generadas.append(alerta)
        
        # 5. Nuevos cursos disponibles
        if not tipo_alerta or tipo_alerta == 'nuevos_cursos':
            alertas_cursos = GestorCursos.alertar_nuevos_cursos()
            
            for alerta_curso in alertas_cursos:
                if alerta_curso.get('urgente'):
                    alerta = SistemaNotificaciones._crear_alerta_admin(
                        tipo='curso_deadline',
                        titulo=alerta_curso['titulo'],
                        descripcion=alerta_curso['mensaje'],
                        prioridad='alta'
                    )
                    alertas_generadas.append(alerta)
        
        # 6. Estudiantes con fondos insuficientes
        if not tipo_alerta or tipo_alerta == 'fondos_insuficientes':
            from modules.estudiantes import Estudiante
            from modules.fondos import GestorFondos
            
            estudiantes = db.query(Estudiante).filter(
                Estudiante.estado_visa.in_(['no_iniciado', 'documentos'])
            ).all()
            
            for estudiante in estudiantes:
                verificacion = GestorFondos.verificar_fondos(estudiante.id)
                if verificacion.get('porcentaje_cobertura', 100) < 100:
                    alerta = SistemaNotificaciones._crear_alerta_admin(
                        tipo='fondos_insuficientes',
                        titulo=f'Fondos insuficientes: {estudiante.nombre_completo}',
                        descripcion=f'Deficit: {verificacion.get("deficit", 0):,.2f}€ ({verificacion.get("porcentaje_cobertura", 0):.1f}% del mínimo)',
                        estudiante_id=estudiante.id,
                        prioridad='alta'
                    )
                    alertas_generadas.append(alerta)
        
        return {
            'total_alertas': len(alertas_generadas),
            'alertas': alertas_generadas
        }
    
    @staticmethod
    def _crear_alerta_admin(
        tipo: str,
        titulo: str,
        descripcion: str,
        estudiante_id: int = None,
        prioridad: str = 'normal'
    ) -> AlertaAdmin:
        """Crea una alerta para administradores"""
        db = get_db()
        
        # Verificar si ya existe alerta similar reciente
        existe = db.query(AlertaAdmin).filter(
            AlertaAdmin.tipo_alerta == tipo,
            AlertaAdmin.estudiante_id == estudiante_id,
            AlertaAdmin.resuelta == False,
            AlertaAdmin.created_at >= datetime.utcnow() - timedelta(days=1)
        ).first()
        
        if existe:
            return existe
        
        alerta = AlertaAdmin(
            tipo_alerta=tipo,
            titulo=titulo,
            descripcion=descripcion,
            estudiante_id=estudiante_id,
            prioridad=prioridad
        )
        
        db.add(alerta)
        db.commit()
        db.refresh(alerta)
        
        # Enviar notificación a admins por Telegram
        for admin_id in config.ADMIN_USER_IDS:
            SistemaNotificaciones._enviar_telegram(
                admin_id,
                f"⚠️ {titulo}",
                descripcion
            )
        
        return alerta
    
    @staticmethod
    def marcar_alerta_resuelta(alerta_id: int, resuelto_por: str = 'admin') -> bool:
        """Marca una alerta como resuelta"""
        db = get_db()
        alerta = db.query(AlertaAdmin).filter(AlertaAdmin.id == alerta_id).first()
        
        if alerta:
            alerta.resuelta = True
            alerta.fecha_resolucion = datetime.utcnow()
            alerta.resuelto_por = resuelto_por
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def obtener_alertas_pendientes(prioridad: str = None) -> List[AlertaAdmin]:
        """Obtiene alertas pendientes, opcionalmente filtradas por prioridad"""
        db = get_db()
        query = db.query(AlertaAdmin).filter(AlertaAdmin.resuelta == False)
        
        if prioridad:
            query = query.filter(AlertaAdmin.prioridad == prioridad)
        
        return query.order_by(AlertaAdmin.created_at.desc()).all()
    
    @staticmethod
    def enviar_recordatorios_automaticos():
        """
        Envía recordatorios automáticos para eventos próximos
        Debe ejecutarse diariamente (cron job)
        """
        from modules.estudiantes import GestorEstudiantes
        
        eventos_hoy = GestorEstudiantes.obtener_eventos_proximos(dias=3)
        recordatorios_enviados = 0
        
        for evento in eventos_hoy:
            dias_restantes = (evento.fecha_evento - datetime.utcnow()).days
            
            # Mensaje personalizado según tipo de evento
            if evento.tipo_evento == 'cita_consulado':
                titulo = f"🔔 Recordatorio: Cita en consulado en {dias_restantes} días"
                mensaje = f"""
Tienes cita programada en el Consulado de España:

📅 Fecha: {evento.fecha_evento.strftime('%d/%m/%Y %H:%M')}
📍 {evento.descripcion}

⚠️ **Importante:**
• Llega 15 minutos antes
• Lleva todos los documentos originales
• Vestimenta formal
• Apaga el móvil antes de entrar

¡Mucha suerte! 🍀
"""
            elif evento.tipo_evento == 'entrega_documentos':
                titulo = f"📄 Recordatorio: Entrega de documentos en {dias_restantes} días"
                mensaje = f"""
Tienes entrega de documentos programada:

📅 Fecha: {evento.fecha_evento.strftime('%d/%m/%Y')}
📋 {evento.descripcion}

Verifica que tengas todo listo.
"""
            else:
                titulo = f"🔔 Recordatorio: {evento.titulo}"
                mensaje = f"""
📅 Fecha: {evento.fecha_evento.strftime('%d/%m/%Y %H:%M')}
📋 {evento.descripcion}
"""
            
            # Enviar por todos los canales disponibles
            resultados = SistemaNotificaciones.notificar_estudiante(
                evento.estudiante_id,
                mensaje,
                titulo,
                canales=['telegram', 'email'],
                prioridad='alta'
            )
            
            if resultados['exitosos']:
                recordatorios_enviados += 1
        
        return {
            'eventos_procesados': len(eventos_hoy),
            'recordatorios_enviados': recordatorios_enviados
        }


# Tareas automáticas programadas (para ejecutar con APScheduler o cron)
def tarea_diaria_alertas():
    """Ejecutar diariamente para generar alertas y enviar recordatorios"""
    print(f"🔄 Ejecutando tareas diarias de alertas - {datetime.now()}")
    
    # Generar alertas internas
    alertas = SistemaNotificaciones.alertas_internas()
    print(f"✅ {alertas['total_alertas']} alertas generadas")
    
    # Enviar recordatorios
    recordatorios = SistemaNotificaciones.enviar_recordatorios_automaticos()
    print(f"✅ {recordatorios['recordatorios_enviados']} recordatorios enviados")
    
    return {
        'alertas': alertas,
        'recordatorios': recordatorios
    }
