"""
Sistema de notificaciones por email
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class NotificacionesEmail:
    
    @staticmethod
    def _enviar_email(destinatario: str, asunto: str, html_contenido: str) -> bool:
        """
        Envía un email HTML
        """
        try:
            # Configuración SMTP
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            smtp_user = os.getenv('SMTP_USER', '')
            smtp_password = os.getenv('SMTP_PASSWORD', '')
            
            if not smtp_user or not smtp_password:
                print("⚠️ Configuración SMTP no disponible. Email no enviado.")
                return False
            
            # Crear mensaje
            mensaje = MIMEMultipart('alternative')
            mensaje['Subject'] = asunto
            mensaje['From'] = smtp_user
            mensaje['To'] = destinatario
            
            # Agregar contenido HTML
            parte_html = MIMEText(html_contenido, 'html')
            mensaje.attach(parte_html)
            
            # Enviar
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, destinatario, mensaje.as_string())
            
            print(f"✅ Email enviado a {destinatario}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
            return False
    
    @staticmethod
    def enviar_confirmacion_registro(estudiante: dict) -> bool:
        """Envía email de confirmación de registro"""
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center;">
                <h1>¡Bienvenido a Fortunario Cash!</h1>
            </div>
            
            <div style="padding: 30px;">
                <p>Hola <strong>{estudiante.get('nombre', 'Estudiante')}</strong>,</p>
                
                <p>Tu solicitud de visa de estudio ha sido registrada exitosamente.</p>
                
                <div style="background: #f0f7ff; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Datos de tu Solicitud:</h3>
                    <p><strong>ID:</strong> #{estudiante.get('id')}</p>
                    <p><strong>Email:</strong> {estudiante.get('email')}</p>
                    <p><strong>Especialidad:</strong> {estudiante.get('especialidad', 'No especificado')}</p>
                </div>
                
                <h3>Próximos Pasos:</h3>
                <ol>
                    <li>Completa tu perfil con todos los datos solicitados</li>
                    <li>Sube los documentos requeridos</li>
                    <li>Nuestro equipo revisará tu solicitud en 24-48 horas</li>
                    <li>Te contactaremos para seguimiento personalizado</li>
                </ol>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://fortunariocash.com" 
                       style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Acceder a Mi Portal
                    </a>
                </div>
                
                <p style="color: #666; font-size: 14px; margin-top: 30px;">
                    Si tienes alguna pregunta, responde a este email o contáctanos a través del chat en tu portal.
                </p>
            </div>
            
            <div style="background: #f9fafb; padding: 20px; text-align: center; color: #666; font-size: 12px;">
                <p>© 2024 Fortunario Cash - Agencia Educativa España</p>
                <p>Este es un email automático, por favor no responder.</p>
            </div>
        </body>
        </html>
        """
        
        return NotificacionesEmail._enviar_email(
            estudiante.get('email'),
            '🎓 Confirmación de Registro - Fortunario Cash',
            html
        )
    
    @staticmethod
    def notificar_cambio_estado(estudiante: dict, nuevo_estado: str, notas: str = '') -> bool:
        """Notifica cambio de estado de la solicitud"""
        estados_mensajes = {
            'aprobado': {
                'titulo': '¡Felicidades! Tu solicitud ha sido aprobada',
                'emoji': '✅',
                'mensaje': 'Tu solicitud de visa ha sido aprobada. Nuestro equipo se pondrá en contacto contigo pronto con los siguientes pasos.'
            },
            'rechazado': {
                'titulo': 'Necesitamos más información sobre tu solicitud',
                'emoji': '⚠️',
                'mensaje': 'Tu solicitud requiere información adicional o documentación complementaria. Por favor revisa las notas y contacta a tu asesor.'
            },
            'en_revision': {
                'titulo': 'Tu solicitud está siendo revisada',
                'emoji': '🔍',
                'mensaje': 'Nuestro equipo está revisando tu solicitud y documentación. Te notificaremos cualquier actualización.'
            }
        }
        
        info = estados_mensajes.get(nuevo_estado, {
            'titulo': 'Actualización de tu solicitud',
            'emoji': '📋',
            'mensaje': 'Ha habido una actualización en el estado de tu solicitud.'
        })
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center;">
                <h1 style="font-size: 48px; margin: 0;">{info['emoji']}</h1>
                <h2>{info['titulo']}</h2>
            </div>
            
            <div style="padding: 30px;">
                <p>Hola <strong>{estudiante.get('nombre', 'Estudiante')}</strong>,</p>
                
                <p>{info['mensaje']}</p>
                
                <div style="background: #f0f7ff; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0;">
                    <p><strong>Nuevo Estado:</strong> {nuevo_estado.upper()}</p>
                    {f'<p><strong>Notas:</strong> {notas}</p>' if notas else ''}
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://fortunariocash.com" 
                       style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Ver Mi Portal
                    </a>
                </div>
            </div>
            
            <div style="background: #f9fafb; padding: 20px; text-align: center; color: #666; font-size: 12px;">
                <p>© 2024 Fortunario Cash - Agencia Educativa España</p>
            </div>
        </body>
        </html>
        """
        
        return NotificacionesEmail._enviar_email(
            estudiante.get('email'),
            f'{info["emoji"]} {info["titulo"]}',
            html
        )
