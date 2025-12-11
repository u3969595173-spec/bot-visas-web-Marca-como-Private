"""
Sistema de Notificaciones por Email para Admin
Envía alertas inmediatas cuando ocurren acciones importantes
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

def enviar_email_admin(asunto: str, cuerpo_html: str):
    """
    Función base para enviar emails al admin
    """
    try:
        SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
        SMTP_USER = os.getenv('SMTP_USER', 'estudiovisaespana@gmail.com')
        SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
        ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'estudiovisaespana@gmail.com')
        
        if not SMTP_PASSWORD:
            print("⚠️ SMTP_PASSWORD no configurado")
            return False
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['From'] = f"Sistema Bot Visas <{SMTP_USER}>"
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = asunto
        
        # Adjuntar HTML
        html_part = MIMEText(cuerpo_html, 'html')
        msg.attach(html_part)
        
        # Enviar
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email enviado al admin: {asunto}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email al admin: {e}")
        return False


def notificar_nuevo_registro(estudiante: dict):
    """
    Notifica al admin cuando un estudiante se registra
    """
    asunto = f"🆕 Nuevo registro: {estudiante.get('nombre', 'Sin nombre')}"
    
    cuerpo = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; background-color: #f9f9f9; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; 
                    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .info-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
            .label {{ font-weight: bold; color: #667eea; }}
            .button {{ display: inline-block; background-color: #667eea; 
                      color: white; padding: 12px 30px; text-decoration: none; 
                      border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎉 ¡Nuevo Estudiante Registrado!</h1>
            <p>Se ha registrado un nuevo estudiante en la plataforma</p>
        </div>
        <div class="content">
            <div class="card">
                <h2>Datos del Estudiante</h2>
                <div class="info-row">
                    <span class="label">👤 Nombre:</span> {estudiante.get('nombre', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📧 Email:</span> {estudiante.get('email', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📱 Teléfono:</span> {estudiante.get('telefono', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">🔑 Código de acceso:</span> {estudiante.get('codigo_acceso', 'N/A')}
                </div>
                <div class="info-row">
                    <span class="label">🕐 Fecha:</span> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="https://fortunariocash.com/admin" class="button">
                    Ver en Panel de Admin
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return enviar_email_admin(asunto, cuerpo)


def notificar_solicitud_presupuesto(estudiante: dict, servicios: list, total: float):
    """
    Notifica al admin cuando un estudiante solicita presupuesto
    """
    asunto = f"💰 Solicitud de presupuesto: {estudiante.get('nombre', 'Sin nombre')} - €{total:,.2f}"
    
    servicios_html = "<ul style='list-style: none; padding: 0;'>"
    for servicio in servicios:
        servicios_html += f"<li style='padding: 8px; background: #f0f0f0; margin: 5px 0; border-radius: 5px;'>✅ {servicio}</li>"
    servicios_html += "</ul>"
    
    cuerpo = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                      color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; background-color: #f9f9f9; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; 
                    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .total {{ font-size: 32px; color: #f5576c; font-weight: bold; text-align: center; 
                     background: #fff3f4; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .info-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
            .label {{ font-weight: bold; color: #f5576c; }}
            .button {{ display: inline-block; background-color: #f5576c; 
                      color: white; padding: 12px 30px; text-decoration: none; 
                      border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>💰 Nueva Solicitud de Presupuesto</h1>
            <p>Un estudiante ha solicitado presupuesto de servicios</p>
        </div>
        <div class="content">
            <div class="card">
                <h2>Datos del Estudiante</h2>
                <div class="info-row">
                    <span class="label">👤 Nombre:</span> {estudiante.get('nombre', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📧 Email:</span> {estudiante.get('email', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📱 Teléfono:</span> {estudiante.get('telefono', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">🕐 Fecha:</span> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
            </div>
            
            <div class="card">
                <h2>Servicios Solicitados</h2>
                {servicios_html}
            </div>
            
            <div class="total">
                💰 Total: €{total:,.2f}
            </div>
            
            <div style="text-align: center;">
                <a href="https://fortunariocash.com/admin/presupuestos" class="button">
                    Ver Presupuesto en Admin
                </a>
            </div>
            
            <div class="card" style="background: #fffbf0; border-left: 4px solid #ffc107;">
                <p><strong>⚡ Acción requerida:</strong> Revisa y responde al estudiante lo antes posible.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return enviar_email_admin(asunto, cuerpo)


def notificar_perfil_completado(estudiante: dict):
    """
    Notifica al admin cuando un estudiante completa su perfil
    """
    asunto = f"✅ Perfil completado: {estudiante.get('nombre', 'Sin nombre')}"
    
    cuerpo = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                      color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; background-color: #f9f9f9; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; 
                    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .info-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
            .label {{ font-weight: bold; color: #4facfe; }}
            .button {{ display: inline-block; background-color: #4facfe; 
                      color: white; padding: 12px 30px; text-decoration: none; 
                      border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>✅ Perfil Completado</h1>
            <p>Un estudiante ha completado su perfil</p>
        </div>
        <div class="content">
            <div class="card">
                <h2>Información del Estudiante</h2>
                <div class="info-row">
                    <span class="label">👤 Nombre:</span> {estudiante.get('nombre', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📧 Email:</span> {estudiante.get('email', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📱 Teléfono:</span> {estudiante.get('telefono', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">🎓 Carrera:</span> {estudiante.get('carrera_deseada', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">🗓️ Fecha nacimiento:</span> {estudiante.get('fecha_nacimiento', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">🕐 Completado:</span> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="https://fortunariocash.com/admin" class="button">
                    Ver Perfil Completo
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return enviar_email_admin(asunto, cuerpo)


def notificar_nuevo_mensaje(estudiante: dict, mensaje: str):
    """
    Notifica al admin cuando un estudiante envía un mensaje
    """
    asunto = f"💬 Nuevo mensaje de: {estudiante.get('nombre', 'Sin nombre')}"
    
    # Truncar mensaje si es muy largo
    mensaje_preview = mensaje[:200] + "..." if len(mensaje) > 200 else mensaje
    
    cuerpo = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                      color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; background-color: #f9f9f9; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; 
                    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .mensaje {{ background: #f0f0f0; padding: 15px; border-radius: 8px; 
                       font-style: italic; margin: 15px 0; }}
            .info-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
            .label {{ font-weight: bold; color: #fa709a; }}
            .button {{ display: inline-block; background-color: #fa709a; 
                      color: white; padding: 12px 30px; text-decoration: none; 
                      border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>💬 Nuevo Mensaje</h1>
            <p>Un estudiante te ha enviado un mensaje</p>
        </div>
        <div class="content">
            <div class="card">
                <h2>De:</h2>
                <div class="info-row">
                    <span class="label">👤 Nombre:</span> {estudiante.get('nombre', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📧 Email:</span> {estudiante.get('email', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">🕐 Hora:</span> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
            </div>
            
            <div class="card">
                <h2>Mensaje:</h2>
                <div class="mensaje">
                    {mensaje_preview}
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="https://fortunariocash.com/admin/chats" class="button">
                    Responder en el Chat
                </a>
            </div>
            
            <div class="card" style="background: #fff8f0; border-left: 4px solid #ff9800;">
                <p><strong>⏰ Responde pronto:</strong> El estudiante está esperando tu respuesta.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return enviar_email_admin(asunto, cuerpo)


def notificar_documentos_subidos(estudiante: dict, documentos: list):
    """
    Notifica al admin cuando un estudiante sube documentos
    """
    asunto = f"📄 Documentos subidos: {estudiante.get('nombre', 'Sin nombre')}"
    
    docs_html = "<ul style='list-style: none; padding: 0;'>"
    for doc in documentos:
        docs_html += f"<li style='padding: 8px; background: #f0f0f0; margin: 5px 0; border-radius: 5px;'>📎 {doc}</li>"
    docs_html += "</ul>"
    
    cuerpo = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                      color: #333; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; background-color: #f9f9f9; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; 
                    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .info-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
            .label {{ font-weight: bold; color: #00bcd4; }}
            .button {{ display: inline-block; background-color: #00bcd4; 
                      color: white; padding: 12px 30px; text-decoration: none; 
                      border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📄 Nuevos Documentos</h1>
            <p>Un estudiante ha subido documentos</p>
        </div>
        <div class="content">
            <div class="card">
                <h2>Estudiante</h2>
                <div class="info-row">
                    <span class="label">👤 Nombre:</span> {estudiante.get('nombre', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📧 Email:</span> {estudiante.get('email', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">🕐 Hora:</span> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
            </div>
            
            <div class="card">
                <h2>Documentos Subidos</h2>
                {docs_html}
            </div>
            
            <div style="text-align: center;">
                <a href="https://fortunariocash.com/admin/documentos" class="button">
                    Revisar Documentos
                </a>
            </div>
            
            <div class="card" style="background: #e8f5e9; border-left: 4px solid #4caf50;">
                <p><strong>✅ Acción sugerida:</strong> Revisa y valida los documentos subidos.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return enviar_email_admin(asunto, cuerpo)


def notificar_solicitud_credito(estudiante: dict, agente: dict, tipo: str, monto: float):
    """
    Notifica al admin cuando un estudiante o agente solicita retiro/uso de crédito
    """
    tipo_persona = "agente" if agente else "estudiante"
    persona = agente if agente else estudiante
    tipo_accion = "Retiro" if tipo == "retiro" else "Descuento"
    
    asunto = f"💰 Solicitud de {tipo_accion}: {persona.get('nombre', 'Sin nombre')} - €{monto:,.2f}"
    
    cuerpo = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                      color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; background-color: #f9f9f9; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; 
                    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .monto {{ font-size: 32px; color: #f5576c; font-weight: bold; text-align: center; 
                     background: #fff3f4; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .info-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
            .label {{ font-weight: bold; color: #f5576c; }}
            .button {{ display: inline-block; background-color: #f5576c; 
                      color: white; padding: 12px 30px; text-decoration: none; 
                      border-radius: 5px; margin: 10px 5px; }}
            .button.aprobar {{ background-color: #4caf50; }}
            .button.rechazar {{ background-color: #f44336; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>💰 Solicitud de {tipo_accion} de Crédito</h1>
            <p>Un {tipo_persona} ha solicitado {tipo_accion.lower()} de crédito</p>
        </div>
        <div class="content">
            <div class="card">
                <h2>Información del {'Agente' if agente else 'Estudiante'}</h2>
                <div class="info-row">
                    <span class="label">👤 Nombre:</span> {persona.get('nombre', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📧 Email:</span> {persona.get('email', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">💰 Crédito disponible:</span> €{persona.get('credito_disponible', 0):,.2f}
                </div>
                <div class="info-row">
                    <span class="label">📅 Tipo de solicitud:</span> {tipo_accion}
                </div>
                <div class="info-row">
                    <span class="label">🕐 Fecha:</span> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
            </div>
            
            <div class="monto">
                💵 Monto solicitado: €{monto:,.2f}
            </div>
            
            <div style="text-align: center;">
                <a href="https://fortunariocash.com/admin/solicitudes-credito" class="button aprobar">
                    ✅ Revisar y Aprobar/Rechazar
                </a>
            </div>
            
            <div class="card" style="background: #fff8f0; border-left: 4px solid #ffc107;">
                <p><strong>⚡ Acción requerida:</strong> Revisa la solicitud y aprueba o rechaza según corresponda.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return enviar_email_admin(asunto, cuerpo)


def notificar_pago_confirmado(estudiante: dict, presupuesto: dict, modalidad: str, monto: float):
    """
    Notifica al admin cuando se confirma un pago (registro interno, no es que el estudiante pagó)
    """
    modalidad_map = {
        'al_empezar': 'Pago Inicial',
        'con_visa': 'Pago con Visa',
        'financiado': 'Pago Financiado'
    }
    
    tipo_pago = modalidad_map.get(modalidad, modalidad)
    asunto = f"✅ Pago registrado: {estudiante.get('nombre', 'Sin nombre')} - {tipo_pago} - €{monto:,.2f}"
    
    cuerpo = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%); 
                      color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; background-color: #f9f9f9; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; 
                    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .monto {{ font-size: 32px; color: #4caf50; font-weight: bold; text-align: center; 
                     background: #f1f8e9; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .info-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
            .label {{ font-weight: bold; color: #4caf50; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>✅ Pago Confirmado y Registrado</h1>
            <p>Se ha marcado un pago como recibido en el sistema</p>
        </div>
        <div class="content">
            <div class="card">
                <h2>Información del Estudiante</h2>
                <div class="info-row">
                    <span class="label">👤 Nombre:</span> {estudiante.get('nombre', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">📧 Email:</span> {estudiante.get('email', 'No especificado')}
                </div>
                <div class="info-row">
                    <span class="label">💵 Tipo de pago:</span> {tipo_pago}
                </div>
                <div class="info-row">
                    <span class="label">🕐 Fecha:</span> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
            </div>
            
            <div class="monto">
                💰 Monto: €{monto:,.2f}
            </div>
            
            <div class="card" style="background: #e8f5e9; border-left: 4px solid #4caf50;">
                <p><strong>📝 Nota:</strong> Este es un registro interno. El pago ya fue marcado en el sistema.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return enviar_email_admin(asunto, cuerpo)

