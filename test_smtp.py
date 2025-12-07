"""
Script para probar la configuración SMTP
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_smtp_config():
    """Verifica la configuración SMTP"""
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN SMTP")
    print("=" * 60)
    
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    
    print(f"\n📧 SMTP_SERVER: {SMTP_SERVER}")
    print(f"🔌 SMTP_PORT: {SMTP_PORT}")
    print(f"👤 SMTP_USER: {SMTP_USER}")
    print(f"🔑 SMTP_PASSWORD: {'✅ Configurado' if SMTP_PASSWORD else '❌ NO CONFIGURADO'}")
    print(f"📨 ADMIN_EMAIL: {ADMIN_EMAIL}")
    
    if not SMTP_PASSWORD:
        print("\n❌ ERROR: SMTP_PASSWORD no está configurado en el archivo .env")
        print("\n📝 INSTRUCCIONES:")
        print("1. Ve a https://myaccount.google.com/apppasswords")
        print("2. Genera una contraseña de aplicación para 'Mail'")
        print("3. Agrégala a tu archivo .env como:")
        print("   SMTP_PASSWORD=tu_contraseña_de_16_caracteres")
        return False
    
    # Intentar enviar email de prueba
    print("\n🚀 Intentando enviar email de prueba...")
    try:
        from api.notificaciones_admin import enviar_email_admin
        
        resultado = enviar_email_admin(
            asunto="🧪 Test de SMTP - Bot Visas",
            cuerpo_html="""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #667eea;">✅ Configuración SMTP Correcta</h2>
                <p>Este es un email de prueba del sistema de notificaciones.</p>
                <p>Si recibes este mensaje, la configuración SMTP está funcionando correctamente.</p>
                <hr>
                <p style="color: #999; font-size: 12px;">Bot Visas - Sistema de Notificaciones</p>
            </body>
            </html>
            """
        )
        
        if resultado:
            print("✅ Email enviado exitosamente!")
            print(f"📬 Revisa la bandeja de entrada de: {ADMIN_EMAIL}")
            return True
        else:
            print("❌ No se pudo enviar el email")
            return False
            
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        return False

if __name__ == "__main__":
    test_smtp_config()
