# ✅ CHECKLIST DE VERIFICACIÓN - Sistema de Partnerships

## 🎯 **QUÉ TIENES QUE HACER AHORA**

### **PASO 1: Configurar Base de Datos (5 minutos)**

#### Opción A: PostgreSQL Local (Recomendado para desarrollo)
```powershell
# 1. Crear archivo .env (copia de .env.example)
Copy-Item .env.example .env

# 2. Editar el archivo .env con tus credenciales
# Abre .env y cambia esta línea:
DATABASE_URL=postgresql://user:password@localhost:5432/visas_bot

# Por ejemplo (con tus credenciales reales):
DATABASE_URL=postgresql://postgres:mipassword@localhost:5432/visas_bot
```

#### Opción B: SQLite (Más simple, para testing)
```powershell
# En el archivo .env, usa:
DATABASE_URL=sqlite:///visas_bot.db
```

---

### **PASO 2: Instalar Dependencias (2 minutos)**

```powershell
# Backend
cd C:\BotVisasEstudio
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic pillow requests

# Frontend (si aún no lo hiciste)
cd frontend
npm install
```

---

### **PASO 3: Iniciar Backend (Auto-crea tablas y seed)**

```powershell
cd C:\BotVisasEstudio
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Deberías ver:**
```
✅ Tabla documentos_generados verificada/creada
✅ Campos OCR agregados a documentos
✅ Sistema de partnerships universitarios creado
📚 Insertando 52 universidades partner iniciales...
✅ Insertadas 45 universidades partner
```

**❌ Si ves error de conexión a BD:**
- Verifica que PostgreSQL está corriendo
- O cambia a SQLite en el `.env`

---

### **PASO 4: Iniciar Frontend**

```powershell
# En otra terminal
cd C:\BotVisasEstudio\frontend
npm run dev
```

**Debería abrir:** `http://localhost:5173`

---

### **PASO 5: Verificar que TODO funciona**

#### ✅ **Backend - Probar endpoints:**

Abre el navegador en: `http://localhost:8000/docs`

**Prueba estos endpoints:**

1. **GET /api/admin/partners/universidades** 
   - ✅ Debe devolver las 45 universidades
   
2. **GET /api/admin/partners/dashboard**
   - ✅ Debe mostrar estadísticas (0 estudiantes por ahora)

3. **POST /api/admin/partners/universidades** 
   - ✅ Crear una universidad de prueba

#### ✅ **Frontend - Probar interfaz:**

1. Abre `http://localhost:5173`
2. Inicia sesión como admin (usuario: admin, password: tu configuración)
3. Haz clic en la pestaña **"🤝 Partnerships"**
4. Deberías ver:
   - **Tab "Dashboard"**: 6 tarjetas con estadísticas
   - **Tab "Universidades"**: Grid con las 45 universidades
   - **Tab "Comisiones"**: Tabla vacía (aún no hay)

---

## 🔍 **VERIFICACIÓN RÁPIDA (3 comandos)**

```powershell
# 1. Verificar que el seed funciona
python -c "from api.seed_universidades import UNIVERSIDADES_DATA; print(f'✅ Seed OK: {len(UNIVERSIDADES_DATA)} universidades')"

# 2. Verificar que el backend arranca sin errores
python -c "from api.main import app; print('✅ Backend importa correctamente')"

# 3. Verificar archivos frontend
Test-Path frontend\src\components\PartnersAdmin.jsx
Test-Path frontend\src\components\PartnersAdmin.css
```

**Resultado esperado:**
```
✅ Seed OK: 45 universidades
✅ Backend importa correctamente
True
True
```

---

## 🐛 **TROUBLESHOOTING (Si algo falla)**

### ❌ Error: "No module named 'psycopg2'"
```powershell
pip install psycopg2-binary
```

### ❌ Error: "Connection refused" (PostgreSQL)
**Solución 1:** Inicia PostgreSQL
```powershell
# Windows (si instalaste con instalador)
net start postgresql-x64-14
```

**Solución 2:** Usa SQLite (más fácil)
```
# En .env:
DATABASE_URL=sqlite:///visas_bot.db
```

### ❌ Error: "Cannot find module './PartnersAdmin'"
```powershell
# Verifica que el archivo existe
Test-Path frontend\src\components\PartnersAdmin.jsx
# Si es False, haz git pull
git pull origin main
```

### ❌ Frontend no muestra la pestaña "Partnerships"
Verifica que `DashboardAdminExpandido.jsx` tiene:
```javascript
import PartnersAdmin from './PartnersAdmin'
```

---

## 📊 **ARQUITECTURA DEL SISTEMA**

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │  DashboardAdminExpandido.jsx                     │   │
│  │    ├─ Tab: Partnerships                          │   │
│  │    └─ <PartnersAdmin />                          │   │
│  │         ├─ Dashboard (stats)                     │   │
│  │         ├─ Universidades (CRUD)                  │   │
│  │         └─ Comisiones (tracking)                 │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP (axios)
┌─────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  api/main.py                                     │   │
│  │    ├─ Startup: Crea tablas                       │   │
│  │    ├─ Startup: Inserta seed (45 universidades)   │   │
│  │    └─ 10 endpoints REST                          │   │
│  │         ├─ GET /api/admin/partners/universidades │   │
│  │         ├─ POST /api/admin/partners/universidades│   │
│  │         ├─ PUT /api/admin/partners/universidades │   │
│  │         ├─ GET /api/admin/partners/dashboard     │   │
│  │         └─ ... (comisiones, estudiantes, etc)    │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  api/seed_universidades.py                       │   │
│  │    └─ UNIVERSIDADES_DATA[] (45 items)           │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         ↕ SQL
┌─────────────────────────────────────────────────────────┐
│                  BASE DE DATOS                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  universidades_partner                           │   │
│  │    ├─ nombre, pais, email_contacto               │   │
│  │    ├─ codigo_referido (único)                    │   │
│  │    ├─ tipo_comision, valor_comision              │   │
│  │    └─ estado, sitio_web, notas                   │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  comisiones                                      │   │
│  │    ├─ universidad_id → universidades_partner     │   │
│  │    ├─ estudiante_id → estudiantes                │   │
│  │    ├─ monto_curso, monto_comision                │   │
│  │    └─ estado (pendiente/pagado)                  │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  estudiantes                                     │   │
│  │    ├─ ... (campos existentes)                    │   │
│  │    ├─ universidad_referidora_id                  │   │
│  │    └─ codigo_referido                            │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 **RESUMEN DE ARCHIVOS CREADOS/MODIFICADOS**

### ✅ **Backend:**
- `api/seed_universidades.py` ← **45 universidades con datos**
- `api/main.py` ← **Startup event con auto-insert**
- `database/migrations/insert_universidades_partners.sql` ← **SQL manual (backup)**

### ✅ **Frontend:**
- `frontend/src/components/PartnersAdmin.jsx` ← **Componente principal (500 líneas)**
- `frontend/src/components/PartnersAdmin.css` ← **Estilos (400 líneas)**
- `frontend/src/components/DashboardAdminExpandido.jsx` ← **Modificado (import + tab)**

### ✅ **Documentación:**
- `outreach/email_templates.md` ← **6 templates de email**
- `outreach/plan_contacto_52_universidades.md` ← **Plan de contacto priorizado**

---

## 🚀 **COMANDO ÚNICO PARA PROBAR TODO**

```powershell
# En una terminal
cd C:\BotVisasEstudio
uvicorn api.main:app --reload

# En otra terminal (espera 5 segundos)
cd C:\BotVisasEstudio\frontend
npm run dev

# Abre navegador:
# http://localhost:8000/docs (API docs)
# http://localhost:5173 (Frontend)
```

---

## ✅ **CRITERIOS DE ÉXITO**

### El sistema funciona si:
1. ✅ Backend arranca sin errores
2. ✅ Se insertan 45 universidades automáticamente
3. ✅ Frontend muestra pestaña "🤝 Partnerships"
4. ✅ Puedes ver las universidades en el panel
5. ✅ Puedes copiar links de referido (ej: `https://tuagencia.com/?ref=DONQUIJOTE2025`)

---

## 📞 **SIGUIENTE PASO (Después de verificar)**

Una vez que TODO funcione:

1. **Personaliza los templates** de email con tu información
2. **Empieza el outreach** con las 5 escuelas de idiomas prioritarias
3. **Trackea respuestas** en Excel/Notion
4. **Cierra los primeros 2-3 partnerships** en 2 semanas

---

¿Qué paso te da problemas? Te ayudo a solucionarlo 🔧
