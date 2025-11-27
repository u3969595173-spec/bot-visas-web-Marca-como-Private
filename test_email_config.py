"""
Script para probar configuración de email
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE EMAIL")
print("=" * 60)

# Verificar variables
email_sender = os.getenv('EMAIL_SENDER')
smtp_user = os.getenv('SMTP_USER')
email_password = os.getenv('EMAIL_PASSWORD')
smtp_password = os.getenv('SMTP_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
smtp_port = os.getenv('SMTP_PORT', '587')

print("\n📋 Variables de entorno:")
print(f"   EMAIL_SENDER: {email_sender or '❌ NO CONFIGURADO'}")
print(f"   SMTP_USER: {smtp_user or '❌ NO CONFIGURADO'}")
print(f"   EMAIL_PASSWORD: {'✅ Configurado' if email_password else '❌ NO CONFIGURADO'}")
print(f"   SMTP_PASSWORD: {'✅ Configurado' if smtp_password else '❌ NO CONFIGURADO'}")
print(f"   SMTP_SERVER: {smtp_server}")
print(f"   SMTP_PORT: {smtp_port}")

# Determinar qué usar
email_final = email_sender or smtp_user
password_final = email_password or smtp_password

print("\n🎯 Configuración que se usará:")
print(f"   Remitente: {email_final or '❌ NO DISPONIBLE'}")
print(f"   Password: {'✅ Disponible' if password_final else '❌ NO DISPONIBLE'}")

if not email_final or not password_final:
    print("\n❌ ERROR: Configuración incompleta")
    print("\n📝 Solución:")
    print("   1. Abre el archivo .env")
    print("   2. Agrega estas líneas:")
    print("      EMAIL_SENDER=tu-email@gmail.com")
    print("      EMAIL_PASSWORD=tu-app-password-de-16-caracteres")
    print("\n   O usa el formato alternativo:")
    print("      SMTP_USER=tu-email@gmail.com")
    print("      SMTP_PASSWORD=tu-app-password-de-16-caracteres")
    print("\n   ⚠️ No uses tu contraseña normal de Gmail!")
    print("   📌 Genera un App Password en: https://myaccount.google.com/apppasswords")
else:
    print("\n✅ Configuración completa")
    print("\n🧪 Probando conexión...")
    
    try:
        import smtplib
        
        smtp = smtplib.SMTP(smtp_server, int(smtp_port))
        smtp.starttls()
        smtp.login(email_final, password_final)
        smtp.quit()
        
        print("✅ ¡Conexión exitosa! El email está configurado correctamente.")
        
    except Exception as e:
        print(f"❌ Error en la conexión: {e}")
        print("\n📝 Posibles causas:")
        print("   1. Password incorrecto (debe ser App Password, no tu contraseña normal)")
        print("   2. Verificación en 2 pasos no activada en Gmail")
        print("   3. App Password no generado correctamente")
        print("\n🔗 Genera un App Password aquí:")
        print("   https://myaccount.google.com/apppasswords")

print("\n" + "=" * 60)
