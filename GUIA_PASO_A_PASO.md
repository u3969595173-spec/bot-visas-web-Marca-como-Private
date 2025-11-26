# 🎯 GUÍA PASO A PASO - Configuración y Despliegue

## 📍 DÓNDE ESTÁS AHORA

✅ Backend funcionando localmente (http://127.0.0.1:8000)
✅ Código corregido (sin errores Unicode)
✅ Base de datos PostgreSQL en Render conectada
✅ Frontend desplegado en Vercel
✅ Backend desplegado en Render

---

## 🚀 PASO 1: Obtener tus URLs de producción

### A. URL del Backend en Render

1. Ve a: https://dashboard.render.com
2. Inicia sesión
3. Busca tu servicio (probablemente se llama algo como "bot-visas" o "visas-backend")
4. Copia la URL que aparece arriba (ejemplo: `https://bot-visas-xyz.onrender.com`)

**📋 Anota aquí tu URL de Render:**
```
https://_____________________.onrender.com
```

### B. URL del Frontend en Vercel

1. Ve a: https://vercel.com/dashboard
2. Inicia sesión
3. Busca tu proyecto
4. Copia la URL de producción (ejemplo: `https://bot-visas.vercel.app`)

**📋 Anota aquí tu URL de Vercel:**
```
https://_____________________.vercel.app
```

---

## 🔧 PASO 2: Configurar Variables de Entorno en Render

### A. Ir a configuración

1. Ve a: https://dashboard.render.com
2. Clic en tu servicio de backend
3. Clic en "Environment" en el menú izquierdo

### B. Verificar/Agregar estas variables:

Copia y pega estas variables (reemplaza los valores que digan "TU-XXX"):

```env
DATABASE_URL
(Ya debería estar configurada - no tocar)

PYTHONIOENCODING=utf-8

SECRET_KEY=visas-estudio-secret-key-2025-production

# Email - IMPORTANTE
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=TU-EMAIL@gmail.com
SMTP_PASSWORD=TU-APP-PASSWORD-16-CARACTERES
ADMIN_EMAIL=admin@tuagencia.com

# OCR
OCR_SPACE_API_KEY=K81993791988957

# URLs (reemplaza con tus URLs reales)
FRONTEND_URL=https://TU-APP.vercel.app
API_URL=https://TU-BACKEND.onrender.com
```

### C. Guardar y Redesplegar

1. Clic en "Save Changes"
2. Render automáticamente redesplega
3. Espera 2-3 minutos
4. Verifica que el servicio esté "Live" (verde)

---

## 🎨 PASO 3: Configurar Variable en Vercel

### A. Ir a configuración

1. Ve a: https://vercel.com/dashboard
2. Clic en tu proyecto
3. Clic en "Settings"
4. Clic en "Environment Variables"

### B. Agregar variable

1. **Key:** `VITE_API_URL`
2. **Value:** Tu URL de Render (ejemplo: `https://bot-visas-xyz.onrender.com`)
3. **Environments:** Marca "Production", "Preview", "Development"
4. Clic en "Save"

### C. Redesplegar

1. Ve a "Deployments" (pestaña superior)
2. Busca el último deployment
3. Clic en los 3 puntos (...) → "Redeploy"
4. Espera 1-2 minutos

---

## ✅ PASO 4: Verificar que todo funciona

### A. Verificar Backend

1. Abre en el navegador: `https://TU-BACKEND.onrender.com/docs`
2. Deberías ver la documentación Swagger
3. Si ves error 503 o "Application error":
   - Ve a Render Dashboard → Logs
   - Busca errores en rojo
   - Copia el error y te ayudo a arreglarlo

### B. Verificar Frontend

1. Abre en el navegador: `https://TU-APP.vercel.app`
2. Deberías ver la página principal
3. Abre la consola del navegador (F12)
4. Ve a la pestaña "Network"
5. Recarga la página
6. Verifica que NO haya errores CORS (color rojo)

### C. Probar conexión completa

1. Ve a: `https://TU-APP.vercel.app/registro`
2. Completa el formulario con datos de prueba:
   - Nombre: Test Usuario
   - Email: test@test.com
   - Teléfono: +34600000000
   - Pasaporte: TEST123
   - Edad: 25
   - Nacionalidad: Colombia
   - Ciudad: Bogotá
   - Especialidad: Ingeniería
   - Nivel español: Intermedio
   - Tipo visa: Estudiante

3. Clic en "Registrar"
4. Deberías ver mensaje de éxito
5. Si hay error, abre la consola (F12) y copia el error

---

## 🐛 PASO 5: Solución de Problemas Comunes

### ❌ Error: "Network Error" o "Failed to fetch"

**Causa:** Frontend no puede conectar con backend

**Solución:**
1. Verifica que `VITE_API_URL` esté correcta en Vercel
2. Verifica que tu backend en Render esté "Live"
3. Ve al siguiente paso (configurar CORS)

### ❌ Error: "CORS policy" en la consola

**Causa:** Backend no permite requests desde Vercel

**Solución:** Necesitamos agregar tu dominio de Vercel al CORS del backend.

**Dime tu URL de Vercel y lo arreglo automáticamente.**

### ❌ Error 503 en Render

**Causa:** Backend no pudo iniciar

**Solución:**
1. Ve a Render Dashboard → Logs
2. Busca el error en rojo
3. Copia y pega el error aquí
4. Los errores más comunes:
   - Falta `PYTHONIOENCODING=utf-8` → Agrégala en Environment
   - Error de base de datos → Verifica que `DATABASE_URL` esté correcta
   - Error de importación → Verifica `requirements.txt`

### ❌ Emails no se envían

**Esperado** si no configuraste Gmail

**Solución:**
1. Sigue la guía `CONFIGURAR_EMAIL.md`
2. Genera App Password de Gmail
3. Agrégalo en Render Environment → `SMTP_USER` y `SMTP_PASSWORD`
4. Redesplega

---

## 📝 PASO 6: Configurar CORS (Si hay error CORS)

Necesito que me des tu URL de Vercel para agregar CORS correctamente.

**Ejemplo:** Si tu frontend es `https://bot-visas.vercel.app`, necesito saberlo para actualizar el código.

---

## 🎯 CHECKLIST RÁPIDO

Marca cada paso conforme lo completes:

**Render (Backend):**
- [ ] Obtuve mi URL de Render
- [ ] Verifiqué variables de entorno
- [ ] Agregué `PYTHONIOENCODING=utf-8`
- [ ] Guardé cambios y redesplega
- [ ] Backend está "Live" (verde)
- [ ] Puedo abrir `/docs` sin errores

**Vercel (Frontend):**
- [ ] Obtuve mi URL de Vercel
- [ ] Agregué `VITE_API_URL` con mi URL de Render
- [ ] Redesplega el proyecto
- [ ] Frontend carga sin errores
- [ ] No hay errores CORS en consola

**Prueba completa:**
- [ ] Puedo registrar un estudiante desde el frontend
- [ ] El estudiante se guarda en la base de datos
- [ ] Puedo hacer login como admin
- [ ] Veo el estudiante en el panel admin

---

## 🆘 ¿NECESITAS AYUDA?

**Para cada problema, necesito que me proporciones:**

1. **Tu URL de Render:** `https://_______.onrender.com`
2. **Tu URL de Vercel:** `https://_______.vercel.app`
3. **Error específico:** Copia el mensaje completo
4. **Dónde ocurre:** Backend (Render logs) o Frontend (consola navegador)

Con esa información puedo arreglar cualquier problema en segundos.

---

## 📊 ESTADO ACTUAL

**¿En qué paso estás?**

- [ ] Paso 1: Obtener URLs
- [ ] Paso 2: Configurar Render
- [ ] Paso 3: Configurar Vercel
- [ ] Paso 4: Verificar funcionamiento
- [ ] Paso 5: Solucionar problemas
- [ ] Paso 6: Configurar CORS (si es necesario)

**Dime en qué paso estás y qué necesitas.**
