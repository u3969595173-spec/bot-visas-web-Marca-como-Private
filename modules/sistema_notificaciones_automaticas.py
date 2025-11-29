"""
Sistema de Notificaciones Automáticas
Envía correos y notificaciones internas por cada acción importante
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_FROM = os.getenv('EMAIL_FROM', SMTP_USER)

class SistemaNotificaciones:
    
    @staticmethod
    def _enviar_email(destinatario, asunto, contenido_html):
        """Envía un correo electrónico"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = asunto
            msg['From'] = EMAIL_FROM
            msg['To'] = destinatario
            
            html_part = MIMEText(contenido_html, 'html', 'utf-8')
            msg.attach(html_part)
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
            
            print(f"✅ Email enviado a {destinatario}: {asunto}")
            return True
        except Exception as e:
            print(f"❌ Error enviando email a {destinatario}: {e}")
            return False
    
    @staticmethod
    def _crear_notificacion_interna(estudiante_id, tipo, titulo, mensaje):
        """Crea una notificación en la base de datos"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO notificaciones (estudiante_id, tipo, titulo, mensaje, fecha_creacion, leido)
                VALUES (%s, %s, %s, %s, %s, FALSE)
            """, (estudiante_id, tipo, titulo, mensaje, datetime.now()))
            
            conn.commit()
            cur.close()
            conn.close()
            print(f"✅ Notificación creada para estudiante {estudiante_id}: {titulo}")
            return True
        except Exception as e:
            print(f"❌ Error creando notificación: {e}")
            return False
    
    @staticmethod
    def _obtener_email_estudiante(estudiante_id):
        """Obtiene el email del estudiante"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("SELECT email, nombre FROM estudiantes WHERE id = %s", (estudiante_id,))
            resultado = cur.fetchone()
            cur.close()
            conn.close()
            return resultado if resultado else (None, None)
        except Exception as e:
            print(f"❌ Error obteniendo email: {e}")
            return None, None
    
    # ============================================
    # NOTIFICACIONES DE REGISTRO Y PERFIL
    # ============================================
    
    @staticmethod
    def notificar_registro_exitoso(estudiante_id):
        """Cuando el estudiante se registra"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = "🎉 ¡Bienvenido a tu proceso de visa de estudiante!"
        mensaje = f"Hola {nombre}, tu cuenta ha sido creada exitosamente. Completa tu perfil para comenzar."
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #3b82f6;">🎉 ¡Bienvenido {nombre}!</h2>
            <p>Tu cuenta ha sido creada exitosamente en nuestro sistema de gestión de visas.</p>
            <h3>📋 Próximos pasos:</h3>
            <ol>
                <li><strong>Completa tu perfil</strong> con tu información personal y académica</li>
                <li><strong>Solicita un presupuesto</strong> para los servicios que necesitas</li>
                <li><strong>Recibe tu cotización</strong> personalizada de nuestro equipo</li>
                <li><strong>Comienza tu proceso</strong> de visa de estudiante</li>
            </ol>
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL', 'https://tu-app.vercel.app')}/login" 
                   style="background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Acceder a mi cuenta
                </a>
            </p>
            <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                Si tienes preguntas, no dudes en contactarnos.
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'info', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    @staticmethod
    def notificar_perfil_completado(estudiante_id):
        """Cuando el estudiante completa su perfil"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = "✅ Perfil completado - Solicita tu presupuesto"
        mensaje = f"Tu perfil está completo. Ahora puedes solicitar un presupuesto personalizado."
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #10b981;">✅ ¡Perfil Completado!</h2>
            <p>Hola {nombre},</p>
            <p>Tu perfil ha sido completado exitosamente. Ya estás listo para el siguiente paso.</p>
            <h3>💼 Solicita tu presupuesto</h3>
            <p>Accede a tu panel y solicita un presupuesto personalizado para los servicios que necesitas:</p>
            <ul>
                <li>Búsqueda de Universidad</li>
                <li>Gestión de Matrícula</li>
                <li>Asesoría de Visa</li>
                <li>Traducción y Apostilla de Documentos</li>
                <li>Seguro Médico</li>
                <li>Y mucho más...</li>
            </ul>
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante" 
                   style="background-color: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Solicitar Presupuesto
                </a>
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'success', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    # ============================================
    # NOTIFICACIONES DE PRESUPUESTOS
    # ============================================
    
    @staticmethod
    def notificar_presupuesto_solicitado(estudiante_id, servicios):
        """Cuando el estudiante solicita un presupuesto"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = "📋 Solicitud de presupuesto recibida"
        mensaje = f"Hemos recibido tu solicitud. Nuestro equipo la está revisando y te responderemos pronto."
        
        servicios_html = "".join([f"<li>{s}</li>" for s in servicios])
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #3b82f6;">📋 Solicitud Recibida</h2>
            <p>Hola {nombre},</p>
            <p>Hemos recibido tu solicitud de presupuesto para los siguientes servicios:</p>
            <ul style="background-color: #f3f4f6; padding: 15px; border-radius: 6px;">
                {servicios_html}
            </ul>
            <p><strong>⏱️ Tiempo de respuesta:</strong> 24-48 horas hábiles</p>
            <p>Nuestro equipo está preparando una cotización personalizada para ti.</p>
            <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                Recibirás una notificación cuando tu presupuesto esté listo.
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'info', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    @staticmethod
    def notificar_presupuesto_ofertado(estudiante_id, monto_total):
        """Cuando el admin envía las modalidades de pago"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = "💰 ¡Tu presupuesto está listo!"
        mensaje = f"Hemos preparado tu cotización con {monto_total:.2f}€. Revisa las opciones de pago disponibles."
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #10b981;">💰 ¡Tu Presupuesto Está Listo!</h2>
            <p>Hola {nombre},</p>
            <p>Hemos preparado tu cotización personalizada.</p>
            <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin: 20px 0;">
                <h3 style="color: #059669; margin-top: 0;">Monto Total: €{monto_total:.2f}</h3>
                <p>Tienes 3 modalidades de pago disponibles para elegir la que mejor se adapte a ti.</p>
            </div>
            <p><strong>📋 Revisa tu presupuesto y elige tu modalidad de pago:</strong></p>
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante" 
                   style="background-color: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Ver Mi Presupuesto
                </a>
            </p>
            <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                ⏰ Este presupuesto es válido por 15 días.
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'success', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    @staticmethod
    def notificar_presupuesto_aceptado(estudiante_id, modalidad_elegida):
        """Cuando el estudiante acepta el presupuesto"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = "✅ Presupuesto aceptado - Instrucciones de pago"
        mensaje = f"Has aceptado el presupuesto con modalidad: {modalidad_elegida}. Sigue las instrucciones para realizar el pago."
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #10b981;">✅ ¡Presupuesto Aceptado!</h2>
            <p>Hola {nombre},</p>
            <p>Has aceptado exitosamente tu presupuesto con la modalidad: <strong>{modalidad_elegida}</strong></p>
            
            <div style="background-color: #fef3c7; padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 20px 0;">
                <h3 style="color: #d97706; margin-top: 0;">📋 Próximos Pasos</h3>
                <ol>
                    <li>Recibirás las instrucciones de pago por correo</li>
                    <li>Realiza el pago según la modalidad elegida</li>
                    <li>Tu proceso de visa comenzará una vez confirmado el pago</li>
                </ol>
            </div>
            
            <p><strong>Estado actual:</strong> ⏳ Pendiente de pago inicial</p>
            <p>Nuestro equipo te contactará con los detalles de pago.</p>
            
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante/proceso-visa" 
                   style="background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Ver Mi Proceso
                </a>
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'success', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    # ============================================
    # NOTIFICACIONES DE PAGOS
    # ============================================
    
    @staticmethod
    def notificar_pago_confirmado(estudiante_id, tipo_pago):
        """Cuando el admin confirma un pago"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = "✅ Pago confirmado - Proceso en marcha"
        mensaje = f"Tu pago ({tipo_pago}) ha sido confirmado. Tu proceso de visa está en marcha."
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #10b981;">✅ ¡Pago Confirmado!</h2>
            <p>Hola {nombre},</p>
            <p>Hemos confirmado tu pago: <strong>{tipo_pago}</strong></p>
            
            <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin: 20px 0;">
                <h3 style="color: #059669; margin-top: 0;">🚀 Tu Proceso Está en Marcha</h3>
                <p>Estado: <strong>🔄 En Proceso</strong></p>
                <p>Nuestro equipo ya está trabajando en tu caso.</p>
            </div>
            
            <p><strong>📊 Puedes seguir el progreso en tiempo real:</strong></p>
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante/proceso-visa" 
                   style="background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Ver Mi Progreso
                </a>
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'success', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    # ============================================
    # NOTIFICACIONES DE PROCESO DE VISA
    # ============================================
    
    @staticmethod
    def notificar_paso_completado(estudiante_id, nombre_paso, fase):
        """Cuando se completa un paso del proceso"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = f"✅ Paso completado: {nombre_paso}"
        mensaje = f"Hemos completado: {nombre_paso} en la fase {fase}. ¡Seguimos avanzando!"
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #10b981;">✅ Paso Completado</h2>
            <p>Hola {nombre},</p>
            <p>Excelentes noticias! Hemos completado un paso importante de tu proceso:</p>
            
            <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #059669; margin-top: 0;">📋 {nombre_paso}</h3>
                <p><strong>Fase:</strong> {fase}</p>
            </div>
            
            <p>Revisa el progreso completo de tu proceso de visa en tu panel.</p>
            
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante/proceso-visa" 
                   style="background-color: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Ver Mi Progreso
                </a>
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'success', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    @staticmethod
    def notificar_proceso_completado(estudiante_id):
        """Cuando se completa TODO el proceso de visa"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = "🎉 ¡Proceso completado! - Servicio finalizado"
        mensaje = f"¡Felicitaciones! Has completado el 100% de tu proceso de visa de estudiante."
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #10b981;">🎉 ¡FELICITACIONES {nombre.upper()}!</h2>
            <p>Has completado exitosamente el <strong>100%</strong> de tu proceso de visa de estudiante.</p>
            
            <div style="background-color: #ecfdf5; padding: 30px; border-radius: 12px; text-align: center; margin: 30px 0;">
                <h1 style="color: #059669; font-size: 48px; margin: 0;">✅</h1>
                <h2 style="color: #059669;">Proceso Completado</h2>
                <p style="font-size: 18px; color: #047857;"><strong>Estado: Completado</strong></p>
            </div>
            
            <h3>🎓 Próximos Pasos:</h3>
            <ul>
                <li>Prepara tu viaje a España</li>
                <li>Revisa la documentación final</li>
                <li>Contacta con tu universidad</li>
                <li>¡Disfruta tu nueva aventura!</li>
            </ul>
            
            <p style="margin-top: 30px; padding: 20px; background-color: #f0f9ff; border-radius: 8px;">
                <strong>💙 Gracias por confiar en nosotros</strong><br>
                Ha sido un placer ayudarte en este proceso. ¡Te deseamos mucho éxito en España!
            </p>
            
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante/proceso-visa" 
                   style="background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Ver Mi Resumen Final
                </a>
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'success', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    # ============================================
    # NOTIFICACIONES DE DOCUMENTOS
    # ============================================
    
    @staticmethod
    def notificar_documento_solicitado(estudiante_id, nombre_documento):
        """Cuando el admin solicita un documento"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = f"📄 Documento solicitado: {nombre_documento}"
        mensaje = f"Necesitamos que subas: {nombre_documento}. Por favor, súbelo lo antes posible."
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #f59e0b;">📄 Documento Solicitado</h2>
            <p>Hola {nombre},</p>
            <p>Necesitamos que subas el siguiente documento para continuar con tu proceso:</p>
            
            <div style="background-color: #fef3c7; padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 20px 0;">
                <h3 style="color: #d97706; margin-top: 0;">{nombre_documento}</h3>
                <p><strong>⚠️ Importante:</strong> Este documento es necesario para avanzar en tu proceso.</p>
            </div>
            
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante/documentos" 
                   style="background-color: #f59e0b; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Subir Documento
                </a>
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'warning', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    @staticmethod
    def notificar_documento_aprobado(estudiante_id, nombre_documento):
        """Cuando el admin aprueba un documento"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = f"✅ Documento aprobado: {nombre_documento}"
        mensaje = f"Tu documento {nombre_documento} ha sido aprobado."
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #10b981;">✅ Documento Aprobado</h2>
            <p>Hola {nombre},</p>
            <p>Tu documento ha sido revisado y aprobado:</p>
            
            <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #059669; margin-top: 0;">📄 {nombre_documento}</h3>
                <p style="color: #047857;">Estado: <strong>✅ Aprobado</strong></p>
            </div>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'success', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    @staticmethod
    def notificar_documento_rechazado(estudiante_id, nombre_documento, motivo):
        """Cuando el admin rechaza un documento"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = f"❌ Documento rechazado: {nombre_documento}"
        mensaje = f"Tu documento {nombre_documento} necesita correcciones. Motivo: {motivo}"
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #ef4444;">❌ Documento Rechazado</h2>
            <p>Hola {nombre},</p>
            <p>Tu documento necesita correcciones:</p>
            
            <div style="background-color: #fee2e2; padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444; margin: 20px 0;">
                <h3 style="color: #dc2626; margin-top: 0;">📄 {nombre_documento}</h3>
                <p><strong>Motivo del rechazo:</strong></p>
                <p style="background-color: white; padding: 10px; border-radius: 4px;">{motivo}</p>
            </div>
            
            <p>Por favor, corrige el documento y súbelo nuevamente.</p>
            
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante/documentos" 
                   style="background-color: #ef4444; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Subir Documento Corregido
                </a>
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'error', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    @staticmethod
    def notificar_documento_generado(estudiante_id, documentos):
        """Cuando el admin genera documentos automáticamente"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = "📄 Nuevos documentos listos para descargar"
        mensaje = f"Hemos generado {len(documentos)} documento(s) para ti. Descárgalos desde tu panel."
        
        docs_html = "".join([f"<li>{doc}</li>" for doc in documentos])
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #10b981;">📄 Documentos Listos</h2>
            <p>Hola {nombre},</p>
            <p>Hemos generado los siguientes documentos oficiales para ti:</p>
            
            <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <ul style="list-style-type: none; padding: 0;">
                    {docs_html}
                </ul>
            </div>
            
            <p>Estos documentos están listos para descargar desde tu panel de estudiante.</p>
            <p><strong>💡 Importante:</strong> Revísalos cuidadosamente antes de usarlos en tu proceso.</p>
            
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante/documentos" 
                   style="background-color: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Ver Mis Documentos
                </a>
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'success', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)
    
    # ============================================
    # NOTIFICACIONES DE MENSAJES
    # ============================================
    
    @staticmethod
    def notificar_mensaje_recibido(estudiante_id, asunto):
        """Cuando el admin envía un mensaje"""
        email, nombre = SistemaNotificaciones._obtener_email_estudiante(estudiante_id)
        if not email:
            return
        
        titulo = f"💬 Nuevo mensaje: {asunto}"
        mensaje = f"Tienes un nuevo mensaje del equipo. Asunto: {asunto}"
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #3b82f6;">💬 Nuevo Mensaje</h2>
            <p>Hola {nombre},</p>
            <p>Has recibido un nuevo mensaje de nuestro equipo:</p>
            
            <div style="background-color: #eff6ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #1e40af; margin-top: 0;">📧 {asunto}</h3>
            </div>
            
            <p style="margin-top: 20px;">
                <a href="{os.getenv('FRONTEND_URL')}/estudiante/mensajes" 
                   style="background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Ver Mensaje
                </a>
            </p>
        </body>
        </html>
        """
        
        SistemaNotificaciones._crear_notificacion_interna(estudiante_id, 'info', titulo, mensaje)
        SistemaNotificaciones._enviar_email(email, titulo, html)


# Función auxiliar para uso rápido
def notificar(tipo_evento, estudiante_id, **kwargs):
    """
    Función helper para enviar notificaciones rápidamente
    
    Tipos de eventos soportados:
    - 'registro'
    - 'perfil_completado'
    - 'presupuesto_solicitado'
    - 'presupuesto_ofertado'
    - 'presupuesto_aceptado'
    - 'pago_confirmado'
    - 'paso_completado'
    - 'proceso_completado'
    - 'documento_solicitado'
    - 'documento_aprobado'
    - 'documento_rechazado'
    - 'mensaje_recibido'
    """
    
    sistema = SistemaNotificaciones()
    
    if tipo_evento == 'registro':
        sistema.notificar_registro_exitoso(estudiante_id)
    
    elif tipo_evento == 'perfil_completado':
        sistema.notificar_perfil_completado(estudiante_id)
    
    elif tipo_evento == 'presupuesto_solicitado':
        sistema.notificar_presupuesto_solicitado(estudiante_id, kwargs.get('servicios', []))
    
    elif tipo_evento == 'presupuesto_ofertado':
        sistema.notificar_presupuesto_ofertado(estudiante_id, kwargs.get('monto_total', 0))
    
    elif tipo_evento == 'presupuesto_aceptado':
        sistema.notificar_presupuesto_aceptado(estudiante_id, kwargs.get('modalidad_elegida', ''))
    
    elif tipo_evento == 'pago_confirmado':
        sistema.notificar_pago_confirmado(estudiante_id, kwargs.get('tipo_pago', ''))
    
    elif tipo_evento == 'paso_completado':
        sistema.notificar_paso_completado(
            estudiante_id, 
            kwargs.get('nombre_paso', ''), 
            kwargs.get('fase', '')
        )
    
    elif tipo_evento == 'proceso_completado':
        sistema.notificar_proceso_completado(estudiante_id)
    
    elif tipo_evento == 'documento_solicitado':
        sistema.notificar_documento_solicitado(estudiante_id, kwargs.get('nombre_documento', ''))
    
    elif tipo_evento == 'documento_aprobado':
        sistema.notificar_documento_aprobado(estudiante_id, kwargs.get('nombre_documento', ''))
    
    elif tipo_evento == 'documento_rechazado':
        sistema.notificar_documento_rechazado(
            estudiante_id, 
            kwargs.get('nombre_documento', ''),
            kwargs.get('motivo', '')
        )
    
    elif tipo_evento == 'documento_generado':
        sistema.notificar_documento_generado(estudiante_id, kwargs.get('documentos', []))
    
    elif tipo_evento == 'mensaje_recibido':
        sistema.notificar_mensaje_recibido(estudiante_id, kwargs.get('asunto', ''))
    
    else:
        print(f"❌ Tipo de evento desconocido: {tipo_evento}")
