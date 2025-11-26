"""
Utilidades para envío de emails automáticos
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional, List
import base64


def enviar_email(
    destinatario: str,
    asunto: str,
    cuerpo_html: str,
    archivos_adjuntos: Optional[List[dict]] = None
) -> bool:
    """
    Envía un email con HTML y archivos adjuntos opcionales
    
    Args:
        destinatario: Email del destinatario
        asunto: Asunto del email
        cuerpo_html: Contenido HTML del email
        archivos_adjuntos: Lista de diccionarios con keys: 'nombre', 'contenido_base64', 'tipo'
    
    Returns:
        bool: True si se envió correctamente, False si hubo error
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('SMTP_USER')
        msg['To'] = destinatario
        msg['Subject'] = asunto
        
        # Adjuntar cuerpo HTML
        msg.attach(MIMEText(cuerpo_html, 'html'))
        
        # Adjuntar archivos si los hay
        if archivos_adjuntos:
            for archivo in archivos_adjuntos:
                contenido = base64.b64decode(archivo['contenido_base64'])
                attachment = MIMEApplication(contenido, _subtype=archivo.get('tipo', 'pdf'))
                attachment.add_header('Content-Disposition', 'attachment', filename=archivo['nombre'])
                msg.attach(attachment)
        
        # Conectar y enviar
        smtp = smtplib.SMTP(os.getenv('SMTP_SERVER', 'smtp.gmail.com'), int(os.getenv('SMTP_PORT', 587)))
        smtp.starttls()
        smtp.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
        smtp.send_message(msg)
        smtp.quit()
        
        return True
    except Exception as e:
        print(f"Error enviando email a {destinatario}: {str(e)}")
        return False


def email_bienvenida(nombre: str, email: str) -> bool:
    """Email de bienvenida al registrarse"""
    asunto = "¡Bienvenido a Estudio Visa España!"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #667eea;">¡Hola {nombre}!</h2>
            <p>Gracias por registrarte en <strong>Estudio Visa España</strong>.</p>
            <p>Hemos recibido tu solicitud y nuestro equipo está revisando tu expediente.</p>
            <p>Te notificaremos por email cuando haya actualizaciones.</p>
            <div style="background: #f7fafc; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #667eea;">Próximos pasos:</h3>
                <ul>
                    <li>Revisión de documentos por nuestro equipo</li>
                    <li>Sugerencia de cursos compatibles</li>
                    <li>Generación de documentos oficiales</li>
                    <li>Preparación para visa de estudiante</li>
                </ul>
            </div>
            <p>Si tienes dudas, no dudes en contactarnos.</p>
            <p style="margin-top: 30px;">Saludos,<br><strong>Equipo de Estudio Visa España</strong></p>
        </div>
    </body>
    </html>
    """
    return enviar_email(email, asunto, cuerpo)


def email_aprobacion(nombre: str, email: str, comentarios: Optional[str] = None) -> bool:
    """Email cuando el estudiante es aprobado"""
    asunto = "✅ ¡Solicitud Aprobada!"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #48bb78;">¡Felicitaciones {nombre}!</h2>
            <p>Tu solicitud ha sido <strong style="color: #48bb78;">APROBADA</strong> ✅</p>
            <p>Estamos generando tus documentos oficiales y pronto estarán disponibles para descarga.</p>
            {f'<div style="background: #f7fafc; padding: 15px; border-radius: 8px; margin: 20px 0;"><p><strong>Comentarios:</strong> {comentarios}</p></div>' if comentarios else ''}
            <p>Accede a tu perfil para:</p>
            <ul>
                <li>Descargar tus documentos aprobados</li>
                <li>Ver el curso asignado</li>
                <li>Revisar tu alojamiento</li>
                <li>Prepararte para la entrevista consular</li>
            </ul>
            <p style="margin-top: 30px;">Saludos,<br><strong>Equipo de Estudio Visa España</strong></p>
        </div>
    </body>
    </html>
    """
    return enviar_email(email, asunto, cuerpo)


def email_rechazo(nombre: str, email: str, motivo: str) -> bool:
    """Email cuando el estudiante es rechazado"""
    asunto = "Actualización sobre tu Solicitud"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #f56565;">Hola {nombre},</h2>
            <p>Lamentamos informarte que tu solicitud no ha sido aprobada en este momento.</p>
            <div style="background: #fff5f5; border-left: 4px solid #f56565; padding: 15px; margin: 20px 0;">
                <p><strong>Motivo:</strong></p>
                <p>{motivo}</p>
            </div>
            <p>Puedes volver a aplicar una vez que hayas resuelto los puntos mencionados.</p>
            <p>Si tienes preguntas, contáctanos para mayor orientación.</p>
            <p style="margin-top: 30px;">Saludos,<br><strong>Equipo de Estudio Visa España</strong></p>
        </div>
    </body>
    </html>
    """
    return enviar_email(email, asunto, cuerpo)


def email_documentos_listos(nombre: str, email: str, documentos: List[str]) -> bool:
    """Email cuando los documentos están listos para descargar"""
    lista_docs = "".join([f"<li>{doc}</li>" for doc in documentos])
    asunto = "📄 Tus Documentos Están Listos"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #667eea;">¡Hola {nombre}!</h2>
            <p>Tus documentos oficiales han sido generados y aprobados.</p>
            <div style="background: #f7fafc; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Documentos disponibles:</h3>
                <ul>{lista_docs}</ul>
            </div>
            <p>Accede a tu perfil para descargarlos.</p>
            <p style="margin-top: 30px;">Saludos,<br><strong>Equipo de Estudio Visa España</strong></p>
        </div>
    </body>
    </html>
    """
    return enviar_email(email, asunto, cuerpo)


def email_recordatorio_documentos(nombre: str, email: str, documentos_faltantes: List[str]) -> bool:
    """Email recordatorio de documentos faltantes"""
    lista_docs = "".join([f"<li>{doc}</li>" for doc in documentos_faltantes])
    asunto = "⏰ Recordatorio: Documentos Pendientes"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #ed8936;">Hola {nombre},</h2>
            <p>Te recordamos que aún faltan algunos documentos en tu expediente:</p>
            <div style="background: #fffaf0; border-left: 4px solid #ed8936; padding: 15px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Documentos faltantes:</h3>
                <ul>{lista_docs}</ul>
            </div>
            <p>Por favor, súbelos lo antes posible para continuar con tu proceso.</p>
            <p style="margin-top: 30px;">Saludos,<br><strong>Equipo de Estudio Visa España</strong></p>
        </div>
    </body>
    </html>
    """
    return enviar_email(email, asunto, cuerpo)


def email_curso_asignado(nombre: str, email: str, curso_nombre: str, curso_detalles: dict) -> bool:
    """Email cuando se asigna un curso al estudiante"""
    asunto = f"📚 Curso Asignado: {curso_nombre}"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #667eea;">¡Hola {nombre}!</h2>
            <p>Te hemos asignado el siguiente curso:</p>
            <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #667eea;">{curso_nombre}</h3>
                <p><strong>Duración:</strong> {curso_detalles.get('duracion_meses', 'N/A')} meses</p>
                <p><strong>Ciudad:</strong> {curso_detalles.get('ciudad', 'N/A')}</p>
                <p><strong>Nivel requerido:</strong> {curso_detalles.get('nivel_espanol_requerido', 'N/A')}</p>
                <p><strong>Precio:</strong> €{curso_detalles.get('precio_eur', 'N/A')}</p>
            </div>
            <p>Revisa los detalles completos en tu perfil.</p>
            <p style="margin-top: 30px;">Saludos,<br><strong>Equipo de Estudio Visa España</strong></p>
        </div>
    </body>
    </html>
    """
    return enviar_email(email, asunto, cuerpo)
