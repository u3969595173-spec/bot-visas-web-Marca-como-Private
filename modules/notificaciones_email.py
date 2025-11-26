"""
Sistema de Notificaciones por Email
Reemplaza las notificaciones de Telegram con emails profesionales
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Optional
from datetime import datetime
import config


class EmailService:
    """Servicio de envío de emails profesionales"""
    
    # Configuración SMTP (ajustar según proveedor)
    SMTP_SERVER = getattr(config, 'SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = getattr(config, 'SMTP_PORT', 587)
    SMTP_USER = getattr(config, 'SMTP_USER', 'tu-email@gmail.com')
    SMTP_PASSWORD = getattr(config, 'SMTP_PASSWORD', 'tu-password')
    FROM_EMAIL = getattr(config, 'FROM_EMAIL', 'noreply@agenciaeducativa.com')
    FROM_NAME = getattr(config, 'FROM_NAME', 'Agencia Educativa España')
    
    @staticmethod
    def _crear_conexion():
        """Crea conexión SMTP"""
        try:
            server = smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT)
            server.starttls()
            server.login(EmailService.SMTP_USER, EmailService.SMTP_PASSWORD)
            return server
        except Exception as e:
            print(f"❌ Error conectando a SMTP: {e}")
            return None
    
    @staticmethod
    def enviar_email(
        destinatario: str,
        asunto: str,
        contenido_html: str,
        contenido_texto: str = None,
        adjuntos: List[Dict] = None
    ) -> bool:
        """
        Envía un email
        
        Args:
            destinatario: Email del destinatario
            asunto: Asunto del email
            contenido_html: Contenido en HTML
            contenido_texto: Contenido en texto plano (fallback)
            adjuntos: Lista de archivos adjuntos
            
        Returns:
            True si se envió correctamente
        """
        try:
            # Crear mensaje
            mensaje = MIMEMultipart('alternative')
            mensaje['From'] = f"{EmailService.FROM_NAME} <{EmailService.FROM_EMAIL}>"
            mensaje['To'] = destinatario
            mensaje['Subject'] = asunto
            
            # Agregar contenido texto plano
            if contenido_texto:
                parte_texto = MIMEText(contenido_texto, 'plain', 'utf-8')
                mensaje.attach(parte_texto)
            
            # Agregar contenido HTML
            parte_html = MIMEText(contenido_html, 'html', 'utf-8')
            mensaje.attach(parte_html)
            
            # Agregar adjuntos si existen
            if adjuntos:
                for adjunto in adjuntos:
                    parte = MIMEBase('application', 'octet-stream')
                    parte.set_payload(adjunto['contenido'])
                    encoders.encode_base64(parte)
                    parte.add_header(
                        'Content-Disposition',
                        f"attachment; filename= {adjunto['nombre']}"
                    )
                    mensaje.attach(parte)
            
            # Enviar
            server = EmailService._crear_conexion()
            if server:
                server.send_message(mensaje)
                server.quit()
                print(f"✅ Email enviado a {destinatario}")
                return True
            else:
                print(f"❌ No se pudo conectar al servidor SMTP")
                return False
                
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
            return False
    
    @staticmethod
    def generar_template_html(
        titulo: str,
        mensaje: str,
        boton_texto: str = None,
        boton_url: str = None
    ) -> str:
        """
        Genera HTML profesional para emails
        
        Args:
            titulo: Título principal del email
            mensaje: Contenido del mensaje (puede incluir HTML)
            boton_texto: Texto del botón (opcional)
            boton_url: URL del botón (opcional)
            
        Returns:
            HTML formateado
        """
        boton_html = ""
        if boton_texto and boton_url:
            boton_html = f"""
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 30px;">
                <tr>
                    <td align="center">
                        <a href="{boton_url}" style="
                            display: inline-block;
                            padding: 15px 30px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                            font-weight: bold;
                            font-size: 16px;
                        ">{boton_texto}</a>
                    </td>
                </tr>
            </table>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f7fafc; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 10px 10px 0 0; text-align: center;">
                                    <h1 style="color: white; margin: 0; font-size: 28px;">🎓 Agencia Educativa España</h1>
                                </td>
                            </tr>
                            
                            <!-- Contenido -->
                            <tr>
                                <td style="padding: 40px;">
                                    <h2 style="color: #2d3748; margin-top: 0; font-size: 24px;">{titulo}</h2>
                                    <div style="color: #4a5568; line-height: 1.6; font-size: 16px;">
                                        {mensaje}
                                    </div>
                                    {boton_html}
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f7fafc; padding: 30px; border-radius: 0 0 10px 10px; text-align: center;">
                                    <p style="color: #718096; font-size: 14px; margin: 0;">
                                        © 2025 Agencia Educativa España<br>
                                        Tu camino hacia estudiar en España
                                    </p>
                                    <p style="color: #a0aec0; font-size: 12px; margin-top: 15px;">
                                        Este es un email automático, por favor no respondas a este mensaje.<br>
                                        Si tienes preguntas, contáctanos a través de la plataforma.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        return html


class NotificacionesEmail:
    """Gestiona notificaciones por email para estudiantes y admins"""
    
    @staticmethod
    def enviar_confirmacion_registro(estudiante: Dict) -> bool:
        """Envía email de confirmación de registro"""
        
        mensaje = f"""
        <p>Hola <strong>{estudiante['nombre_completo']}</strong>,</p>
        
        <p>¡Bienvenido a nuestra agencia educativa! Hemos recibido tu registro exitosamente.</p>
        
        <div style="background: #f7fafc; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Tu ID de seguimiento:</strong></p>
            <p style="font-size: 32px; font-weight: bold; color: #667eea; margin: 10px 0;">#{estudiante['id']}</p>
            <p style="margin: 0; font-size: 14px; color: #718096;">Guarda este número para consultar tu estado</p>
        </div>
        
        <p><strong>¿Qué sigue ahora?</strong></p>
        <ul>
            <li>Nuestro sistema está procesando tu información automáticamente</li>
            <li>Buscaremos los mejores cursos según tu perfil</li>
            <li>Verificaremos tu situación económica</li>
            <li>Generaremos tu checklist de documentos</li>
        </ul>
        
        <p>Un miembro de nuestro equipo revisará toda tu información y te contactará en las próximas 24-48 horas.</p>
        
        <p>¡Gracias por confiar en nosotros para tu futuro en España! 🇪🇸</p>
        """
        
        html = EmailService.generar_template_html(
            titulo="¡Registro Exitoso!",
            mensaje=mensaje,
            boton_texto="Acceder a Mi Portal",
            boton_url=f"{getattr(config, 'WEB_URL', 'http://localhost:3000')}/estudiante/dashboard"
        )
        
        return EmailService.enviar_email(
            destinatario=estudiante['email'],
            asunto="✅ Registro Confirmado - Agencia Educativa España",
            contenido_html=html
        )
    
    @staticmethod
    def enviar_solicitud_aprobada(estudiante: Dict) -> bool:
        """Envía email cuando solicitud es aprobada"""
        
        mensaje = f"""
        <p>Hola <strong>{estudiante['nombre_completo']}</strong>,</p>
        
        <p style="font-size: 18px; color: #48bb78;"><strong>¡Excelentes noticias! 🎉</strong></p>
        
        <p>Tu solicitud ha sido <strong>aprobada</strong> por nuestro equipo. Hemos preparado un paquete completo con toda la información que necesitas para tu proceso de visa.</p>
        
        <div style="background: #c6f6d5; padding: 20px; border-radius: 5px; border-left: 4px solid #48bb78; margin: 20px 0;">
            <p style="margin: 0; color: #22543d;"><strong>Estado:</strong> APROBADA ✅</p>
            <p style="margin: 5px 0 0 0; color: #22543d;">Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <p><strong>Próximos pasos:</strong></p>
        <ol>
            <li>Accede a tu portal para ver toda la información</li>
            <li>Descarga los documentos preparados para ti</li>
            <li>Revisa el curso seleccionado y opciones de alojamiento</li>
            <li>Sigue las instrucciones para completar tu documentación</li>
        </ol>
        
        <p>Nuestro equipo está disponible para resolver cualquier duda que tengas. ¡Estás un paso más cerca de estudiar en España!</p>
        """
        
        html = EmailService.generar_template_html(
            titulo="¡Solicitud Aprobada! 🎉",
            mensaje=mensaje,
            boton_texto="Ver Mi Información Completa",
            boton_url=f"{getattr(config, 'WEB_URL', 'http://localhost:3000')}/estudiante/dashboard"
        )
        
        return EmailService.enviar_email(
            destinatario=estudiante['email'],
            asunto="🎉 ¡Tu solicitud ha sido aprobada! - Agencia Educativa",
            contenido_html=html
        )
    
    @staticmethod
    def enviar_solicitud_pendiente_revision(estudiante: Dict, motivo: str) -> bool:
        """Envía email cuando solicitud requiere revisión"""
        
        mensaje = f"""
        <p>Hola <strong>{estudiante['nombre_completo']}</strong>,</p>
        
        <p>Nuestro equipo ha revisado tu solicitud y necesitamos información adicional antes de continuar.</p>
        
        <div style="background: #feebc8; padding: 20px; border-radius: 5px; border-left: 4px solid #ed8936; margin: 20px 0;">
            <p style="margin: 0; color: #744210;"><strong>Motivo:</strong></p>
            <p style="margin: 5px 0 0 0; color: #744210;">{motivo}</p>
        </div>
        
        <p><strong>¿Qué debes hacer?</strong></p>
        <ul>
            <li>Accede a tu portal de estudiante</li>
            <li>Revisa los detalles específicos que necesitamos</li>
            <li>Completa o actualiza la información solicitada</li>
            <li>Contáctanos si tienes dudas</li>
        </ul>
        
        <p>Una vez que completes los requisitos, revisaremos tu solicitud nuevamente lo antes posible.</p>
        """
        
        html = EmailService.generar_template_html(
            titulo="Información Adicional Requerida",
            mensaje=mensaje,
            boton_texto="Revisar Mi Solicitud",
            boton_url=f"{getattr(config, 'WEB_URL', 'http://localhost:3000')}/estudiante/dashboard"
        )
        
        return EmailService.enviar_email(
            destinatario=estudiante['email'],
            asunto="⚠️ Información adicional requerida - Tu solicitud",
            contenido_html=html
        )
    
    @staticmethod
    def enviar_recordatorio_documentos(estudiante: Dict, documentos_pendientes: List[str]) -> bool:
        """Envía recordatorio de documentos pendientes"""
        
        lista_documentos = "".join([f"<li>{doc}</li>" for doc in documentos_pendientes])
        
        mensaje = f"""
        <p>Hola <strong>{estudiante['nombre_completo']}</strong>,</p>
        
        <p>Este es un recordatorio amigable sobre los documentos que aún necesitamos de ti:</p>
        
        <div style="background: #f7fafc; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 0 0 10px 0;"><strong>Documentos pendientes:</strong></p>
            <ul style="margin: 0; color: #2d3748;">
                {lista_documentos}
            </ul>
        </div>
        
        <p>Completa tu documentación lo antes posible para que podamos avanzar con tu solicitud de visa.</p>
        
        <p><strong>Puedes subir tus documentos directamente desde tu portal.</strong></p>
        """
        
        html = EmailService.generar_template_html(
            titulo="📄 Recordatorio de Documentos",
            mensaje=mensaje,
            boton_texto="Subir Documentos",
            boton_url=f"{getattr(config, 'WEB_URL', 'http://localhost:3000')}/estudiante/dashboard?tab=documentos"
        )
        
        return EmailService.enviar_email(
            destinatario=estudiante['email'],
            asunto="📄 Recordatorio: Documentos pendientes",
            contenido_html=html
        )
    
    @staticmethod
    def enviar_nuevo_mensaje(estudiante: Dict, admin_nombre: str, mensaje_preview: str) -> bool:
        """Notifica nuevo mensaje del admin"""
        
        mensaje = f"""
        <p>Hola <strong>{estudiante['nombre_completo']}</strong>,</p>
        
        <p>Has recibido un nuevo mensaje de <strong>{admin_nombre}</strong>:</p>
        
        <div style="background: #e6fffa; padding: 20px; border-radius: 5px; border-left: 4px solid #4299e1; margin: 20px 0;">
            <p style="margin: 0; color: #2c5282; font-style: italic;">"{mensaje_preview[:200]}..."</p>
        </div>
        
        <p>Accede a tu portal para ver el mensaje completo y responder.</p>
        """
        
        html = EmailService.generar_template_html(
            titulo="💬 Nuevo Mensaje",
            mensaje=mensaje,
            boton_texto="Ver Mensaje",
            boton_url=f"{getattr(config, 'WEB_URL', 'http://localhost:3000')}/estudiante/dashboard?tab=mensajes"
        )
        
        return EmailService.enviar_email(
            destinatario=estudiante['email'],
            asunto=f"💬 Nuevo mensaje de {admin_nombre}",
            contenido_html=html
        )
    
    @staticmethod
    def notificar_admin_nuevo_estudiante(admin_email: str, estudiante: Dict) -> bool:
        """Notifica a admin sobre nuevo estudiante"""
        
        mensaje = f"""
        <p>Se ha registrado un nuevo estudiante en la plataforma:</p>
        
        <div style="background: #f7fafc; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Nombre:</strong> {estudiante['nombre_completo']}</p>
            <p style="margin: 5px 0 0 0;"><strong>ID:</strong> #{estudiante['id']}</p>
            <p style="margin: 5px 0 0 0;"><strong>Especialidad:</strong> {estudiante.get('especialidad_interes', 'No especificada')}</p>
            <p style="margin: 5px 0 0 0;"><strong>Nacionalidad:</strong> {estudiante.get('nacionalidad', 'No especificada')}</p>
        </div>
        
        <p>El sistema ha iniciado el procesamiento automático. La solicitud estará lista para revisión pronto.</p>
        """
        
        html = EmailService.generar_template_html(
            titulo="👤 Nuevo Estudiante Registrado",
            mensaje=mensaje,
            boton_texto="Ver en Panel Admin",
            boton_url=f"{getattr(config, 'WEB_URL', 'http://localhost:3000')}/admin/dashboard"
        )
        
        return EmailService.enviar_email(
            destinatario=admin_email,
            asunto=f"👤 Nuevo estudiante: {estudiante['nombre_completo']}",
            contenido_html=html
        )
