"""
Sistema de alertas internas por email al admin
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

def enviar_alerta_admin(estudiante_data: dict, tipo_alerta: str = "registro"):
    """
    Envía email de alerta al admin cuando hay problemas o acciones requeridas
    """
    # Configuración de email (usando variables de entorno)
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'bot@visasestudio.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@visasestudio.com')
    
    if not EMAIL_PASSWORD or not ADMIN_EMAIL:
        print("⚠️ Configuración de email no disponible. Alerta no enviada.")
        return False
    
    # Analizar problemas
    problemas = []
    advertencias = []
    
    # Verificar documentos
    if not estudiante_data.get('archivo_titulo'):
        problemas.append("❌ Falta título académico")
    if not estudiante_data.get('archivo_pasaporte'):
        problemas.append("❌ Falta pasaporte")
    if not estudiante_data.get('archivo_extractos'):
        problemas.append("❌ Faltan extractos bancarios")
    if not estudiante_data.get('consentimiento_gdpr'):
        problemas.append("❌ No aceptó consentimiento GDPR")
    
    # Verificar datos críticos
    if not estudiante_data.get('fecha_nacimiento'):
        advertencias.append("⚠️ Falta fecha de nacimiento")
    if not estudiante_data.get('carrera_deseada'):
        advertencias.append("⚠️ No especificó carrera deseada")
    
    # Verificar fondos
    fondos = float(estudiante_data.get('fondos_disponibles', 0))
    tipo_visa = estudiante_data.get('tipo_visa', 'estudiante')
    fondos_minimos = 4000 if tipo_visa == 'idiomas' else 6000
    
    if fondos < fondos_minimos:
        advertencias.append(f"⚠️ Fondos insuficientes: €{fondos:,.2f} (mínimo recomendado: €{fondos_minimos:,.2f})")
    
    # Verificar nivel de español
    nivel_espanol = estudiante_data.get('nivel_espanol', 'basico')
    if nivel_espanol == 'basico' and tipo_visa == 'estudiante':
        advertencias.append("⚠️ Nivel de español básico puede dificultar admisión universitaria")
    
    # Si no hay problemas críticos, no enviar alerta
    if not problemas and not advertencias:
        print("✅ Registro completo. No se requiere alerta al admin.")
        return True
    
    # Construir email
    asunto = f"⚠️ Nuevo estudiante requiere revisión: {estudiante_data.get('nombre', 'Sin nombre')}"
    
    if tipo_alerta == "documentos_incompletos":
        asunto = f"📄 Documentos incompletos: {estudiante_data.get('nombre', 'Sin nombre')}"
    elif tipo_alerta == "datos_incompletos":
        asunto = f"📝 Datos incompletos: {estudiante_data.get('nombre', 'Sin nombre')}"
    elif tipo_alerta == "fondos_insuficientes":
        asunto = f"💰 Fondos insuficientes: {estudiante_data.get('nombre', 'Sin nombre')}"
    
    # Cuerpo del email en HTML
    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .section {{ margin-bottom: 20px; border-left: 4px solid #007bff; padding-left: 15px; }}
            .problema {{ color: #dc3545; font-weight: bold; }}
            .advertencia {{ color: #ffc107; }}
            .info-item {{ margin: 5px 0; }}
            .button {{ 
                display: inline-block; 
                background-color: #007bff; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>🚨 ALERTA: NUEVO ESTUDIANTE REQUIERE REVISIÓN</h2>
        </div>
        
        <div class="content">
            <div class="section">
                <h3>📋 Datos del Estudiante</h3>
                <p class="info-item"><strong>Nombre:</strong> {estudiante_data.get('nombre', 'No especificado')}</p>
                <p class="info-item"><strong>Email:</strong> {estudiante_data.get('email', 'No especificado')}</p>
                <p class="info-item"><strong>Teléfono:</strong> {estudiante_data.get('telefono', 'No especificado')}</p>
                <p class="info-item"><strong>Pasaporte:</strong> {estudiante_data.get('pasaporte', 'No especificado')}</p>
                <p class="info-item"><strong>Nacionalidad:</strong> {estudiante_data.get('nacionalidad', 'No especificado')}</p>
                <p class="info-item"><strong>Edad:</strong> {estudiante_data.get('edad', 'No especificado')}</p>
                <p class="info-item"><strong>Carrera deseada:</strong> {estudiante_data.get('carrera_deseada', 'No especificado')}</p>
                <p class="info-item"><strong>Tipo de visa:</strong> {estudiante_data.get('tipo_visa', 'No especificado')}</p>
                <p class="info-item"><strong>Fondos disponibles:</strong> €{fondos:,.2f}</p>
                <p class="info-item"><strong>Fecha de registro:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
            
            {''.join([f'<div class="section"><h3 class="problema">❌ PROBLEMAS CRÍTICOS</h3><ul>{"".join([f"<li>{p}</li>" for p in problemas])}</ul></div>']) if problemas else ''}
            
            {''.join([f'<div class="section"><h3 class="advertencia">⚠️ ADVERTENCIAS</h3><ul>{"".join([f"<li>{a}</li>" for a in advertencias])}</ul></div>']) if advertencias else ''}
            
            <div class="section">
                <h3>🔔 ACCIÓN REQUERIDA</h3>
                <p>Por favor, revisa el perfil del estudiante y contacta para solicitar los documentos o datos faltantes.</p>
                <p>El estudiante puede acceder a su perfil con el código: <strong>{estudiante_data.get('codigo_acceso', 'No disponible')}</strong></p>
            </div>
            
            <a href="https://bot-visas-api.onrender.com/admin/estudiantes/{estudiante_data.get('id', 0)}" class="button">
                Ver Perfil Completo en Panel Admin
            </a>
        </div>
        
        <div style="padding: 20px; background-color: #f8f9fa; text-align: center; margin-top: 20px;">
            <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">
                Bot Visas Estudio - Sistema de Alertas Automáticas<br>
                Este es un email automático generado por el sistema.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Crear mensaje
    mensaje = MIMEMultipart('alternative')
    mensaje['From'] = EMAIL_FROM
    mensaje['To'] = ADMIN_EMAIL
    mensaje['Subject'] = asunto
    
    # Agregar contenido HTML
    parte_html = MIMEText(html_body, 'html')
    mensaje.attach(parte_html)
    
    # Enviar email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_FROM, EMAIL_PASSWORD)
            servidor.send_message(mensaje)
        
        print(f"✅ Alerta enviada al admin: {ADMIN_EMAIL}")
        return True
    
    except Exception as e:
        print(f"❌ Error al enviar alerta: {str(e)}")
        return False


def verificar_y_alertar(estudiante_data: dict):
    """
    Verifica el perfil del estudiante y envía alertas si es necesario
    Retorna un resumen de los problemas encontrados
    """
    problemas = {
        "criticos": [],
        "advertencias": [],
        "alerta_enviada": False
    }
    
    # Verificar documentos
    if not estudiante_data.get('archivo_titulo'):
        problemas["criticos"].append("Falta título académico")
    if not estudiante_data.get('archivo_pasaporte'):
        problemas["criticos"].append("Falta pasaporte")
    if not estudiante_data.get('archivo_extractos'):
        problemas["criticos"].append("Faltan extractos bancarios")
    if not estudiante_data.get('consentimiento_gdpr'):
        problemas["criticos"].append("No aceptó consentimiento GDPR")
    
    # Verificar datos
    if not estudiante_data.get('fecha_nacimiento'):
        problemas["advertencias"].append("Falta fecha de nacimiento")
    if not estudiante_data.get('carrera_deseada'):
        problemas["advertencias"].append("No especificó carrera deseada")
    
    # Verificar fondos
    fondos = float(estudiante_data.get('fondos_disponibles', 0))
    tipo_visa = estudiante_data.get('tipo_visa', 'estudiante')
    fondos_minimos = 4000 if tipo_visa == 'idiomas' else 6000
    
    if fondos < fondos_minimos:
        problemas["advertencias"].append(f"Fondos insuficientes: €{fondos:,.2f}")
    
    # Enviar alerta si hay problemas
    if problemas["criticos"] or problemas["advertencias"]:
        alerta_enviada = enviar_alerta_admin(estudiante_data, tipo_alerta="registro")
        problemas["alerta_enviada"] = alerta_enviada
    
    return problemas
