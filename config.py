import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Database Configuration
DATABASE_URL = "postgresql://postgres:BAxjbuTZDB1ATRYk@db.ihdllnlbfcwrbftjzrjz.supabase.co:5432/postgres"

# Stripe Configuration
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Pricing Configuration
PRICE_BASIC = int(os.getenv('PRICE_BASIC', 50))
PRICE_PREMIUM = int(os.getenv('PRICE_PREMIUM', 150))
PRICE_SUCCESS_FEE = int(os.getenv('PRICE_SUCCESS_FEE', 300))

# Bot Configuration
DEBUG_MODE = os.getenv('DEBUG_MODE', 'True').lower() == 'true'
ADMIN_USER_IDS = [int(id) for id in os.getenv('ADMIN_USER_IDS', '').split(',') if id]

# Countries and Universities Data
COUNTRIES = {
    'colombia': {'rejection_rate': 0.2, 'points': 20},
    'mexico': {'rejection_rate': 0.25, 'points': 18},
    'argentina': {'rejection_rate': 0.22, 'points': 19},
    'venezuela': {'rejection_rate': 0.35, 'points': 12},
    'peru': {'rejection_rate': 0.23, 'points': 18},
    'ecuador': {'rejection_rate': 0.28, 'points': 16},
    'chile': {'rejection_rate': 0.18, 'points': 22},
    'brasil': {'rejection_rate': 0.26, 'points': 17},
    'china': {'rejection_rate': 0.32, 'points': 14},
    'india': {'rejection_rate': 0.30, 'points': 15},
    'marruecos': {'rejection_rate': 0.38, 'points': 10},
    'otros': {'rejection_rate': 0.30, 'points': 15}
}

UNIVERSITY_TYPES = {
    'publica_top5': {'points': 30, 'examples': ['UAM', 'Complutense', 'Barcelona', 'Carlos III', 'Pompeu Fabra']},
    'publica': {'points': 25, 'examples': ['Valencia', 'Sevilla', 'Granada', 'Zaragoza']},
    'privada_reconocida': {'points': 22, 'examples': ['IE', 'ESADE', 'Ramon Llull', 'Deusto']},
    'privada': {'points': 18, 'examples': ['Otras privadas']},
    'escuela_idiomas': {'points': 10, 'examples': ['Institutos Cervantes', 'Escuelas de idiomas']}
}

STUDY_TYPES = {
    'doctorado': {'duration_months': 36, 'base_cost': 15000, 'points': 35},
    'master': {'duration_months': 12, 'base_cost': 6000, 'points': 30},
    'grado': {'duration_months': 48, 'base_cost': 10000, 'points': 28},
    'curso_idiomas': {'duration_months': 6, 'base_cost': 3000, 'points': 15}
}

# Economic Requirements
MONTHLY_MAINTENANCE = 600  # € per month minimum required
INSURANCE_COST = 400  # € average annual insurance cost
ACCOMMODATION_ESTIMATE = 500  # € per month estimate

# Document Requirements
MANDATORY_DOCUMENTS = [
    'pasaporte_vigente',
    'carta_aceptacion_universidad',
    'seguro_medico',
    'certificado_antecedentes_penales',
    'certificado_medico',
    'prueba_fondos',
    'formulario_ex00',
    'fotos_carnet'
]

RECOMMENDED_DOCUMENTS = [
    'carta_recomendacion',
    'certificado_nivel_espanol',
    'extractos_bancarios'
]

# === SMTP Email Configuration ===
# Gmail Configuration (Producción)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "estudiovisaespana@gmail.com"
SMTP_PASSWORD = "yhub bwvs fqeh ofaj"  # App Password de Gmail
FROM_EMAIL = "estudiovisaespana@gmail.com"
FROM_NAME = "Visa Estudio España"

# === Web Configuration ===
WEB_URL = "http://localhost:3000"  # URL del frontend (cambiar cuando tengas dominio)
API_URL = "http://localhost:8000"  # URL del backend
ADMIN_EMAIL = "estudiovisaespana@gmail.com"  # Email del administrador para notificaciones
COMPANY_PHONE = ""  # Teléfono de contacto (vacío por ahora)

# === JWT Configuration ===
SECRET_KEY = "tu-clave-secreta-super-segura-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# === Upload Configuration ===
UPLOAD_DIRECTORY = "./uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

"""
INSTRUCCIONES PARA CONFIGURAR GMAIL:

1. Ve a https://myaccount.google.com/security
2. Activa "Verificación en 2 pasos"
3. Ve a https://myaccount.google.com/apppasswords
4. Selecciona "Correo" y "Otro (nombre personalizado)"
5. Escribe "Bot Visas Estudio"
6. Copia la contraseña de 16 caracteres
7. Pégala en SMTP_PASSWORD arriba

⚠️ NUNCA uses tu contraseña normal de Gmail
⚠️ NO subas este archivo a GitHub con credenciales reales
"""
