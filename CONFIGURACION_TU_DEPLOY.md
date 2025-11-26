# ✅ CONFIGURACIÓN PARA TU DESPLIEGUE

**Backend Render:** https://bot-visas-api.onrender.com
**Frontend Vercel:** (Por confirmar)

---

## 🎯 PASO 1: Configurar Variables de Entorno en Render

### Acciones inmediatas:

1. Ve a: https://dashboard.render.com
2. Selecciona tu servicio: **bot-visas-api**
3. Ve a **Environment** (menú izquierdo)
4. Agrega/Verifica estas variables:

```env
PYTHONIOENCODING=utf-8

SECRET_KEY=visas-estudio-secret-key-2025-production

# Email - Gmail App Password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
ADMIN_EMAIL=admin@tuagencia.com

# OCR
OCR_SPACE_API_KEY=K81993791988957

# URLs
API_URL=https://bot-visas-api.onrender.com
FRONTEND_URL=https://tu-app.vercel.app
```

5. Clic en **Save Changes**
6. Render redesplega automáticamente (espera 2-3 minutos)

---

## ✅ PASO 2: Verificar Backend en Render

1. Abre: https://bot-visas-api.onrender.com/docs
2. **Deberías ver:** Documentación Swagger con todos los endpoints
3. **Si ves error 503:**
   - Ve a Render Dashboard → **Logs**
   - Busca errores en rojo
   - Copia el error completo aquí

---

## 🎨 PASO 3: Configurar Vercel

### A. Obtener tu URL de Vercel

1. Ve a: https://vercel.com/dashboard
2. Busca tu proyecto
3. Copia la URL (ejemplo: `https://bot-visas.vercel.app`)

### B. Agregar variable de entorno

1. En Vercel → Tu proyecto → **Settings** → **Environment Variables**
2. Agregar nueva variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://bot-visas-api.onrender.com`
   - **Environments:** Marca las 3 (Production, Preview, Development)
3. Clic en **Save**

### C. Redesplegar

1. Ve a **Deployments**
2. Último deployment → **⋯** (3 puntos) → **Redeploy**
3. Espera 1-2 minutos

---

## 🔍 PASO 4: Probar Conexión

### A. Test Backend
```bash
# Desde PowerShell o navegador
curl https://bot-visas-api.onrender.com/docs
```

**✅ Correcto:** Se abre la página con documentación
**❌ Error:** Copia el mensaje de error

### B. Test Frontend → Backend

1. Abre tu URL de Vercel en el navegador
2. Presiona F12 (consola del navegador)
3. Ve a **Network**
4. Intenta registrar un estudiante
5. Busca requests a `bot-visas-api.onrender.com`
6. **Si ves error CORS:** Ya está configurado, solo redesplega el backend

---

## 📋 CAMBIOS REALIZADOS AUTOMÁTICAMENTE

✅ **frontend/.env.production**
```env
VITE_API_URL=https://bot-visas-api.onrender.com
```

✅ **api/main.py** (CORS configurado)
```python
allow_origins=[
    "http://localhost:5173",
    "http://localhost:3000",
    "https://bot-visas-api.onrender.com",
    "https://*.vercel.app",  # Permite todos los dominios de Vercel
]
```

✅ **vercel.json** (Configuración de rewrites)

---

## 🚀 PRÓXIMOS PASOS

### Ahora necesitas:

1. **Subir cambios a GitHub:**
```powershell
cd C:\BotVisasEstudio
git add .
git commit -m "Configurar CORS y URLs de producción"
git push origin main
```

2. **Render redesplega automáticamente** (si configuraste auto-deploy)
   - O manualmente: Render Dashboard → **Manual Deploy**

3. **Vercel redesplega automáticamente** (si está conectado a GitHub)
   - O manualmente: Vercel Dashboard → **Redeploy**

4. **Probar:**
   - Backend: https://bot-visas-api.onrender.com/docs
   - Frontend: https://TU-APP.vercel.app

---

## 🐛 SOLUCIÓN RÁPIDA DE ERRORES

### ❌ Error: "Application failed to respond" (Render)

**Revisa logs en Render:**
```
Dashboard → tu servicio → Logs
```

**Errores comunes:**
- Falta `PYTHONIOENCODING=utf-8` → Agrégala
- Error de importación → Verifica requirements.txt
- Error de DB → Verifica DATABASE_URL

### ❌ Error CORS (Frontend)

**Síntoma:** Consola muestra "blocked by CORS policy"

**Solución:**
1. Ya configuramos CORS en el código
2. Haz push a GitHub: `git push origin main`
3. Render redesplega automáticamente
4. Espera 2-3 minutos y prueba de nuevo

### ❌ Frontend usa localhost en vez de Render

**Síntoma:** En producción intenta conectar a localhost:8000

**Solución:**
1. Verifica que agregaste `VITE_API_URL` en Vercel
2. Redesplega el frontend
3. Limpia caché del navegador (Ctrl+Shift+R)

---

## ✅ CHECKLIST FINAL

Marca cada paso:

**Backend (Render):**
- [ ] Variables de entorno configuradas
- [ ] `PYTHONIOENCODING=utf-8` agregado
- [ ] Redesplega completado
- [ ] `/docs` abre sin errores
- [ ] Servicio en estado "Live" (verde)

**Frontend (Vercel):**
- [ ] Obtuve mi URL de Vercel
- [ ] Agregué `VITE_API_URL` en variables de entorno
- [ ] Redesplega completado
- [ ] Abre sin errores
- [ ] Consola sin errores CORS

**Git:**
- [ ] Hice commit de los cambios
- [ ] Push a GitHub exitoso
- [ ] Render redesplega automáticamente
- [ ] Vercel redesplega automáticamente

**Prueba completa:**
- [ ] Puedo registrar estudiante desde producción
- [ ] Se guarda en base de datos
- [ ] Puedo hacer login como admin
- [ ] Veo el estudiante en el panel

---

## 📞 ¿NECESITAS AYUDA?

**Dime:**
1. ✅ URL de Vercel (cuando la tengas)
2. ❌ Error específico (copia completo)
3. 📍 En qué paso estás

Con eso te ayudo inmediatamente.

---

**Estado actual:** ✅ Backend URL configurada
**Siguiente paso:** Configurar Vercel y probar
