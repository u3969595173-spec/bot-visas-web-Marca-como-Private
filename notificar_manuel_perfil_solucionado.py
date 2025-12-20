"""
Notificar a Manuel que el error del perfil está solucionado
"""
import os
from dotenv import load_dotenv
from modules.notificaciones_email import NotificacionesEmail

load_dotenv()

# Datos de Manuel
nombre = "Manuel Joaquín Izaguirre Barzaga"
email = "izservices90@gmail.com"
estudiante_id = 16
codigo_acceso = "XJKRSKSD"

# HTML del email
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .content {{
            padding: 30px;
            line-height: 1.6;
            color: #333;
        }}
        .alert-box {{
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .code-box {{
            background-color: #f8f9fa;
            border: 2px solid #667eea;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            letter-spacing: 2px;
        }}
        .button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
            font-weight: bold;
        }}
        .steps {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .step {{
            padding: 10px 0;
            border-bottom: 1px solid #dee2e6;
        }}
        .step:last-child {{
            border-bottom: none;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Problema Solucionado</h1>
        </div>
        
        <div class="content">
            <p>Hola <strong>{nombre}</strong>,</p>
            
            <div class="alert-box">
                <strong>✅ Buenas noticias:</strong> Ya solucionamos el error que impedía completar tu perfil.
            </div>
            
            <p>El problema era técnico en nuestro servidor (faltaba un directorio para guardar tus archivos). Ya está resuelto y puedes continuar.</p>
            
            <h3>🔑 Tu Código de Acceso:</h3>
            <div class="code-box">
                {codigo_acceso}
            </div>
            
            <div style="text-align: center;">
                <a href="https://fortunariocash.com/completar-perfil/{estudiante_id}" class="button">
                    📝 Completar Mi Perfil Ahora
                </a>
            </div>
            
            <h3>📋 Pasos a seguir:</h3>
            <div class="steps">
                <div class="step">
                    <strong>1️⃣</strong> Haz clic en el botón de arriba o ve a: <br>
                    <a href="https://fortunariocash.com">fortunariocash.com</a>
                </div>
                <div class="step">
                    <strong>2️⃣</strong> Usa tu código de acceso: <strong>{codigo_acceso}</strong>
                </div>
                <div class="step">
                    <strong>3️⃣</strong> Completa todos los datos de tu perfil
                </div>
                <div class="step">
                    <strong>4️⃣</strong> Sube tus documentos (título, pasaporte, extractos)
                </div>
                <div class="step">
                    <strong>5️⃣</strong> ¡Listo! Te enviaremos tu presupuesto personalizado
                </div>
            </div>
            
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
                <strong>💡 Tip:</strong> Si aún tienes problemas:
                <ul>
                    <li>Cierra completamente tu navegador</li>
                    <li>Abre en modo incógnito/privado</li>
                    <li>Intenta de nuevo</li>
                </ul>
            </div>
            
            <p>Disculpa las molestias. Estamos aquí para ayudarte en todo el proceso.</p>
            
            <p>Saludos,<br>
            <strong>Equipo Fortunario Cash</strong></p>
        </div>
        
        <div class="footer">
            <p>¿Necesitas ayuda? Responde este email o contáctanos.</p>
            <p>© 2025 Fortunario Cash - Tu Agencia de Visas de Estudio</p>
        </div>
    </div>
</body>
</html>
"""

print("📧 Enviando email a Manuel...")
print(f"   Destinatario: {email}")
print(f"   ID: {estudiante_id}")

try:
    sistema = NotificacionesEmail()
    sistema.enviar_email(
        destinatario=email,
        asunto="✅ Ya puedes completar tu perfil - Problema solucionado",
        cuerpo_html=html_content,
        tipo_notificacion='sistema'
    )
    print("✅ Email enviado exitosamente a Manuel")
except Exception as e:
    print(f"❌ Error enviando email: {e}")
    print("\n💡 ALTERNATIVA: Envía este mensaje manualmente a izservices90@gmail.com")
    print("-" * 70)
    print(f"""
Asunto: ✅ Ya puedes completar tu perfil - Problema solucionado

Hola Manuel,

Ya solucionamos el error que impedía completar tu perfil.

🔑 Tu código de acceso: {codigo_acceso}

🔗 Link directo: https://fortunariocash.com/completar-perfil/{estudiante_id}

Pasos:
1. Entra al link
2. Usa tu código: {codigo_acceso}
3. Completa tu perfil
4. Sube tus documentos

Disculpa las molestias.

Saludos,
Equipo Fortunario Cash
    """)
    print("-" * 70)
