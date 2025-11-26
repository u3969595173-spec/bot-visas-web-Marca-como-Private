# 🎓 Bot Visas Estudio - Dashboard Web

Sistema completo de gestión de estudiantes para agencia educativa con bot de Telegram y dashboard web.

## 🚀 Características

### Para Estudiantes:
- ✅ Registro web con formulario visual
- ✅ Consulta de estado en tiempo real
- ✅ Portal personalizado con seguimiento
- ✅ Notificaciones por email

### Para Administradores:
- ✅ Dashboard completo con estadísticas
- ✅ Gestión de estudiantes (aprobar/rechazar)
- ✅ Filtros avanzados
- ✅ Exportación de reportes
- ✅ Autenticación JWT segura

## 📦 Tecnologías

**Backend:**
- FastAPI (Python 3.11)
- SQLAlchemy ORM
- PostgreSQL / SQLite
- JWT Authentication
- Pydantic Validation

**Frontend:**
- React 18
- Vite
- Axios
- React Router
- CSS moderno

## 🛠️ Instalación

### Opción 1: Docker (Recomendado)

```powershell
# Clonar repositorio
git clone <repo-url>
cd BotVisasEstudio

# Iniciar con Docker Compose
docker-compose up -d

# Acceder a:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Opción 2: Instalación Manual

**Backend:**
```powershell
# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
uvicorn api.main:app --reload
```

**Frontend:**
```powershell
cd frontend

# Instalar dependencias
npm install

# Modo desarrollo
npm run dev

# Build producción
npm run build
```

## 🔐 Credenciales Demo

**Admin:**
- Usuario: `admin`
- Contraseña: `admin123`

⚠️ **IMPORTANTE:** Cambiar en producción

## 📁 Estructura del Proyecto

```
BotVisasEstudio/
├── api/                    # Backend FastAPI
│   ├── main.py            # API endpoints
│   ├── schemas.py         # Modelos Pydantic
│   └── auth.py            # Autenticación JWT
├── frontend/              # Frontend React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── App.jsx        # App principal
│   │   └── main.jsx       # Entry point
│   ├── package.json
│   └── vite.config.js
├── modules/               # Módulos del bot
│   ├── estudiantes.py
│   ├── admin_panel.py
│   └── ...
├── database/              # Modelos de base de datos
├── docker-compose.yml     # Orquestación Docker
├── Dockerfile             # Backend image
└── requirements.txt       # Dependencias Python
```

## 🌐 Endpoints API

### Públicos:
- `POST /api/estudiantes` - Registrar estudiante
- `GET /api/estudiantes/{id}/estado` - Consultar estado

### Admin (requieren JWT):
- `POST /api/login` - Login admin
- `GET /api/admin/estudiantes` - Listar estudiantes
- `GET /api/admin/estadisticas` - Estadísticas
- `POST /api/admin/estudiantes/{id}/aprobar` - Aprobar
- `POST /api/admin/estudiantes/{id}/rechazar` - Rechazar

📄 Documentación completa: `http://localhost:8000/docs`

## 🚀 Deployment

### Render.com (Gratis)

**Backend:**
1. Conectar repositorio
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

**Frontend:**
1. Conectar repositorio (carpeta `frontend`)
2. Build Command: `npm install && npm run build`
3. Publish Directory: `dist`

### Variables de Entorno

```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
JWT_SECRET_KEY=tu-clave-secreta-cambiar
```

## 🔧 Configuración

Editar `config.py`:
```python
# API
API_URL = "http://localhost:8000"

# JWT
JWT_SECRET_KEY = "cambiar-en-produccion"

# Base de datos
DATABASE_URL = "sqlite:///./bot_visas.db"
```

## 📊 Flujo de Trabajo

1. **Estudiante se registra** en la web
2. **Bot procesa automáticamente** (cursos, fondos, documentos)
3. **Admin revisa** en el dashboard
4. **Admin aprueba/rechaza** con un clic
5. **Sistema notifica** al estudiante por email
6. **Estudiante consulta estado** en su portal

## 🐛 Troubleshooting

**Error de CORS:**
```python
# En api/main.py, ajustar allow_origins:
allow_origins=["http://localhost:3000", "https://tudominio.com"]
```

**Error de base de datos:**
```powershell
# Crear tablas
python -c "from database.models import Base, engine; Base.metadata.create_all(engine)"
```

## 📝 Licencia

MIT License

## 👨‍💻 Soporte

Para preguntas o problemas, contactar al equipo de desarrollo.

---

**Hecho con ❤️ para facilitar el proceso de visas de estudiantes**
