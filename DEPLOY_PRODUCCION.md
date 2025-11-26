# 🚀 Guía de Deploy a Producción

## 📋 Necesitarás

1. Cuenta Supabase (base de datos) - gratis
2. Cuenta Vercel (frontend) - gratis
3. Cuenta Render o Railway (backend) - gratis/$7/mes
4. Dominio (opcional) - $10-15/año

---

## PASO 1: Configurar Base de Datos en Supabase

### 1.1 Crear Proyecto
1. Ve a https://supabase.com
2. Click "New Project"
3. Nombre: `bot-visas-estudio`
4. Database Password: **GUARDA ESTA CONTRASEÑA**
5. Region: South America (más cercano)
6. Click "Create new project"

### 1.2 Obtener Connection String
1. En Supabase, ve a Settings → Database
2. Copia la **Connection String** (modo URI)
3. Se ve así:
```
postgresql://postgres.xxx:[YOUR-PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```
4. Reemplaza `[YOUR-PASSWORD]` con tu contraseña

### 1.3 Crear Tablas
1. En Supabase, ve a SQL Editor
2. Copia y pega este SQL:

```sql
-- Tabla Estudiantes
CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    numero_pasaporte VARCHAR(20) UNIQUE NOT NULL,
    edad INTEGER,
    nacionalidad VARCHAR(50),
    ciudad_origen VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    especialidad_interes VARCHAR(100),
    nivel_espanol VARCHAR(20),
    estado_procesamiento VARCHAR(50) DEFAULT 'registrado',
    estado_visa VARCHAR(50) DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT NOW(),
    fecha_procesamiento_automatico TIMESTAMP,
    admin_revisor_id INTEGER,
    curso_seleccionado_id INTEGER,
    notas_admin TEXT
);

-- Tabla Cursos
CREATE TABLE cursos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    universidad VARCHAR(200),
    tipo_curso VARCHAR(50),
    duracion_meses INTEGER,
    costo_total DECIMAL(10,2),
    ciudad VARCHAR(100),
    descripcion TEXT,
    requisitos TEXT,
    fecha_inicio DATE,
    cupos_disponibles INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla Alojamientos
CREATE TABLE alojamientos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    ciudad VARCHAR(100),
    direccion VARCHAR(200),
    precio_mensual DECIMAL(10,2),
    descripcion TEXT,
    habitaciones INTEGER,
    disponible BOOLEAN DEFAULT true,
    contacto VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla Documentos
CREATE TABLE documentos (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER REFERENCES estudiantes(id),
    tipo_documento VARCHAR(100),
    nombre_archivo VARCHAR(200),
    ruta_archivo VARCHAR(500),
    estado VARCHAR(50) DEFAULT 'pendiente',
    fecha_subida TIMESTAMP DEFAULT NOW(),
    revisado_por INTEGER,
    notas_revision TEXT
);

-- Tabla Conversaciones
CREATE TABLE conversaciones (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER REFERENCES estudiantes(id),
    admin_id INTEGER,
    estado VARCHAR(50) DEFAULT 'activa',
    ultima_actividad TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla Mensajes
CREATE TABLE mensajes (
    id SERIAL PRIMARY KEY,
    conversacion_id INTEGER REFERENCES conversaciones(id),
    remitente_tipo VARCHAR(20),
    remitente_id INTEGER,
    contenido TEXT NOT NULL,
    leido BOOLEAN DEFAULT false,
    fecha_envio TIMESTAMP DEFAULT NOW(),
    fecha_lectura TIMESTAMP
);

-- Índices para mejor rendimiento
CREATE INDEX idx_estudiantes_email ON estudiantes(email);
CREATE INDEX idx_estudiantes_estado ON estudiantes(estado_procesamiento);
CREATE INDEX idx_cursos_ciudad ON cursos(ciudad);
CREATE INDEX idx_documentos_estudiante ON documentos(estudiante_id);
CREATE INDEX idx_conversaciones_estudiante ON conversaciones(estudiante_id);
CREATE INDEX idx_mensajes_conversacion ON mensajes(conversacion_id);
```

3. Click "Run" para ejecutar

---

## PASO 2: Deploy Backend en Render

### 2.1 Preparar Repositorio
1. Crea cuenta en https://github.com (si no tienes)
2. Crea nuevo repositorio: `bot-visas-backend`
3. En tu computadora:

```powershell
cd c:\BotVisasEstudio
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU-USUARIO/bot-visas-backend.git
git push -u origin main
```

### 2.2 Crear Procfile
Crear archivo `Procfile` en raíz:
```
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### 2.3 Crear runtime.txt
Crear archivo `runtime.txt`:
```
python-3.11.0
```

### 2.4 Deploy en Render
1. Ve a https://render.com
2. Click "New +" → "Web Service"
3. Conecta tu repositorio GitHub
4. Configuración:
   - Name: `bot-visas-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - Plan: Free

### 2.5 Variables de Entorno en Render
En Render → Environment → Add Environment Variable:

```
DATABASE_URL=postgresql://postgres.xxx:[PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
SMTP_SERVER=sandbox.smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USER=4a2b3c4d5e6f7g
SMTP_PASSWORD=1234567890abcd
FROM_EMAIL=noreply@agenciaeducativa.com
FROM_NAME=Agencia Educativa España
WEB_URL=https://tu-dominio.vercel.app
SECRET_KEY=tu-clave-secreta-super-larga-y-segura-cambiar
ADMIN_EMAIL=admin@agenciaeducativa.com
```

5. Click "Save Changes"
6. Espera 5-10 minutos hasta que diga "Live"
7. Copia la URL (ej: `https://bot-visas-api.onrender.com`)

---

## PASO 3: Deploy Frontend en Vercel

### 3.1 Actualizar API URL
Editar `frontend/src/App.jsx`, buscar:
```javascript
const API_URL = 'http://localhost:8000';
```

Cambiar por:
```javascript
const API_URL = 'https://bot-visas-api.onrender.com';
```

### 3.2 Commit y Push
```powershell
cd c:\BotVisasEstudio
git add .
git commit -m "Update API URL for production"
git push
```

### 3.3 Deploy en Vercel
1. Ve a https://vercel.com
2. Click "Add New..." → "Project"
3. Import tu repositorio GitHub
4. Configuración:
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

5. Click "Deploy"
6. Espera 2-3 minutos
7. Copia la URL (ej: `https://bot-visas.vercel.app`)

---

## PASO 4: Actualizar CORS en Backend

Editar `api/main.py`, línea ~28:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bot-visas.vercel.app",  # Tu URL de Vercel
        "http://localhost:3000"  # Para desarrollo local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit y push:
```powershell
git add .
git commit -m "Update CORS for production"
git push
```

Render detectará el cambio y re-desplegará automáticamente.

---

## PASO 5: Configurar Dominio Personalizado (Opcional)

### 5.1 Comprar Dominio
- Namecheap: https://namecheap.com (~$10/año)
- Google Domains: https://domains.google

### 5.2 Configurar DNS en Vercel
1. En Vercel → Settings → Domains
2. Add Domain: `tudominio.com`
3. Sigue instrucciones para actualizar DNS

### 5.3 Configurar Subdomain para API
En tu proveedor DNS:
```
CNAME  api  bot-visas-api.onrender.com
```

Ahora tendrás:
- Frontend: https://tudominio.com
- Backend: https://api.tudominio.com

---

## PASO 6: Configurar Email Producción (Gmail)

### 6.1 Crear App Password
1. Ve a https://myaccount.google.com/security
2. Activa "Verificación en 2 pasos"
3. Ve a https://myaccount.google.com/apppasswords
4. Crea contraseña para "Bot Visas"

### 6.2 Actualizar Variables en Render
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # App Password de 16 caracteres
```

---

## ✅ Checklist Final

- [ ] Base de datos Supabase creada y tablas migradas
- [ ] Backend desplegado en Render y funcionando
- [ ] Frontend desplegado en Vercel
- [ ] CORS configurado correctamente
- [ ] Variables de entorno configuradas
- [ ] Email funcionando (probar con /api/notificaciones/test-email)
- [ ] Registro de estudiante funciona
- [ ] Login admin funciona
- [ ] Dominio personalizado (opcional)

---

## 🐛 Troubleshooting

**Backend no arranca:**
- Verifica DATABASE_URL en Render
- Revisa logs en Render Dashboard

**Frontend no conecta al backend:**
- Verifica API_URL en App.jsx
- Revisa CORS en api/main.py

**Emails no se envían:**
- Verifica SMTP_USER y SMTP_PASSWORD
- Prueba endpoint /api/notificaciones/test-email

**Base de datos vacía:**
- Ejecuta SQL en Supabase SQL Editor
- Verifica conexión con DATABASE_URL

---

## 💰 Costos Mensuales

- Supabase: $0 (hasta 500MB)
- Render: $0 (free tier) o $7/mes (siempre activo)
- Vercel: $0
- Dominio: ~$1/mes ($12/año)

**Total: $0-8/mes**
