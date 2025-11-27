"""
Script de prueba para verificar envío de emails a universidades
"""
import os
from dotenv import load_dotenv
from api.email_utils import enviar_email

load_dotenv()

print("=" * 60)
print("PRUEBA DE ENVÍO DE EMAIL - SISTEMA UNIVERSIDADES")
print("=" * 60)

# Verificar variables de entorno
email_sender = os.getenv('EMAIL_SENDER') or os.getenv('SMTP_USER')
email_password = os.getenv('EMAIL_PASSWORD') or os.getenv('SMTP_PASSWORD')
nombre_agencia = os.getenv('NOMBRE_AGENCIA', 'Estudia en España')
telefono = os.getenv('TELEFONO_CONTACTO', '+53 XXXXXXXX')
web = os.getenv('WEB_AGENCIA', 'https://fortunariocash.com')

print(f"\n✅ Email configurado: {email_sender}")
print(f"✅ Contraseña: {'*' * len(email_password) if email_password else '❌ NO CONFIGURADA'}")
print(f"✅ Agencia: {nombre_agencia}")
print(f"✅ Teléfono: {telefono}")
print(f"✅ Web: {web}")

# Email de prueba
destinatario = input(f"\n📧 Ingresa email destino para prueba (o Enter para usar {email_sender}): ").strip()
if not destinatario:
    destinatario = email_sender

print(f"\n🚀 Enviando email de prueba a: {destinatario}")

cuerpo_prueba = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; }}
        .content {{ background: #f9f9f9; padding: 30px; margin-top: 20px; border-radius: 10px; }}
        .success {{ background: #d4edda; border: 2px solid #28a745; padding: 20px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 {nombre_agencia}</h1>
            <p>Sistema de Contacto Automatizado</p>
        </div>
        <div class="content">
            <div class="success">
                <h2>✅ ¡Sistema Funcionando Correctamente!</h2>
                <p>Este es un email de prueba del sistema automatizado de contacto con universidades.</p>
            </div>
            
            <h3>📊 Configuración Actual:</h3>
            <ul>
                <li><strong>Email:</strong> {email_sender}</li>
                <li><strong>Agencia:</strong> {nombre_agencia}</li>
                <li><strong>Teléfono:</strong> {telefono}</li>
                <li><strong>Web:</strong> {web}</li>
            </ul>
            
            <h3>✅ Funcionalidades Disponibles:</h3>
            <ul>
                <li>📧 Envío automático de emails profesionales</li>
                <li>🏛️ Contacto con 5 universidades precargadas</li>
                <li>📊 Tracking de estados y respuestas</li>
                <li>📅 Registro de fechas y notas</li>
                <li>🎯 Panel admin completo</li>
            </ul>
            
            <p><strong>El sistema está listo para usar.</strong></p>
            <p>Accede al panel: {web}/admin/login</p>
            <p>Sección: 🏛️ Contactar Universidades</p>
            
            <hr>
            <p style="font-size: 12px; color: #666; text-align: center;">
                Email de prueba enviado desde {nombre_agencia}<br>
                {telefono} | {web}
            </p>
        </div>
    </div>
</body>
</html>
"""

resultado = enviar_email(
    destinatario=destinatario,
    asunto=f"✅ Prueba Sistema Universidades - {nombre_agencia}",
    cuerpo_html=cuerpo_prueba
)

print("\n" + "=" * 60)
if resultado:
    print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
    print(f"📧 Revisa la bandeja de entrada de: {destinatario}")
    print("💡 Si no lo ves, revisa la carpeta de SPAM")
    print("\n🎉 El sistema está configurado correctamente")
    print("🚀 Ya puedes contactar universidades desde el panel admin")
else:
    print("❌ ERROR AL ENVIAR EMAIL")
    print("\n🔍 Posibles causas:")
    print("   1. Contraseña de aplicación incorrecta")
    print("   2. Verificación en 2 pasos no activada")
    print("   3. Conexión a internet bloqueando puerto 587")
    print("\n📖 Revisa: CONFIGURAR_GMAIL_UNIVERSIDADES.md")
print("=" * 60)
