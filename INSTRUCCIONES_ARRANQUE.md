# 🚀 Guía Rápida de Arranque

## 📋 Pre-requisitos
- Python 3.8+
- Node.js 16+
- Git

## ⚙️ Configuración Inicial

### 1. Configurar Email (OBLIGATORIO)
Editar `config.py` líneas 108-115:

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "tu-email@gmail.com"  # ✏️ CAMBIAR AQUÍ
SMTP_PASSWORD = "xxxx xxxx xxxx xxxx"  # ✏️ PEGAR APP PASSWORD
```

**Obtener App Password de Gmail:**
1. https://myaccount.google.com/security → Activar "Verificación en 2 pasos"
2. https://myaccount.google.com/apppasswords
3. Seleccionar "Correo" > "Otro" > "Bot Visas"
4. Copiar contraseña de 16 caracteres

### 2. Instalar Dependencias

**Backend:**
```powershell
cd c:\BotVisasEstudio
pip install fastapi uvicorn sqlalchemy python-jose passlib bcrypt python-multipart
```

**Frontend:**
```powershell
cd frontend
npm install
```

## 🏃 Arrancar el Sistema

**Terminal 1 - Backend:**
```powershell
cd c:\BotVisasEstudio
uvicorn api.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

## 🌐 Acceder

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Docs API:** http://localhost:8000/docs

## 👤 Credenciales Admin

- **Usuario:** admin
- **Contraseña:** admin123

⚠️ **CAMBIAR EN PRODUCCIÓN**

## 📧 Probar Email

1. Ir a http://localhost:8000/docs
2. Buscar `POST /api/notificaciones/test-email`
3. Ingresar tu email
4. Verificar bandeja de entrada

## ✅ Flujo Completo

1. **Estudiante** → Registrarse en http://localhost:3000
2. **Sistema** → Envía email de confirmación automático
3. **Estudiante** → Accede a "Mi Portal" con su ID
4. **Admin** → Login → Ver estudiante pendiente
5. **Admin** → Aprobar → Sistema envía email
6. **Estudiante** → Recibe notificación por email

## 🗂️ Estructura

```
BotVisasEstudio/
├── api/
│   ├── main.py          # 869 líneas - 25+ endpoints
│   ├── schemas.py       # Modelos Pydantic
│   └── auth.py          # JWT tokens
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── DashboardUsuario.jsx          # 450 líneas - Portal estudiante
│       │   └── DashboardAdminExpandido.jsx   # 650 líneas - Panel admin
│       └── App.jsx
├── modules/
│   ├── mensajeria.py            # 280 líneas - Chat interno
│   └── notificaciones_email.py  # 500 líneas - Sistema email
└── config.py                     # Configuración SMTP
```

## 🐛 Troubleshooting

**Error: "Error conectando a SMTP"**
→ Verificar SMTP_USER y SMTP_PASSWORD en config.py

**Error: "ModuleNotFoundError"**
→ Ejecutar: `pip install -r requirements.txt`

**Puerto 8000 ocupado**
→ Cambiar a otro: `uvicorn api.main:app --port 8001`

**Frontend no carga**
→ Verificar que backend esté corriendo primero
