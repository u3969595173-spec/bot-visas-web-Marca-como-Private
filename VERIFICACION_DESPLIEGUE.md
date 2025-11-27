# ✅ VERIFICACIÓN DE DESPLIEGUE - PASO 6

**Fecha:** 27 de noviembre de 2025  
**Commits desplegados:**
- `078c0d5` - Scripts de testing (PASO 5)
- `bbbe7bb` - Páginas legales + Sistema backups (PASO 4)
- `a773a59` - Documentación PASO 3
- `1dc46ec` - PASO 3 COMPLETO (Sugerencias, Probabilidad, Documentos, Alertas)

---

## 📋 CHECKLIST DE VERIFICACIÓN

### 1️⃣ **VERCEL (Frontend)**

**Acciones a realizar:**

1. Ve a: https://vercel.com/dashboard
2. Busca tu proyecto: `bot-visas-web-Marca-como-Private` o similar
3. Verifica:
   - ✅ Último commit desplegado: `078c0d5` o `bbbe7bb`
   - ✅ Estado: "Ready" (verde)
   - ✅ Copia la URL de producción

**📝 URL del Frontend:**
```
https://_________________________.vercel.app
```

**Pruebas a realizar:**

- [ ] Accede a la URL del frontend
- [ ] Verifica que carga la página de inicio
- [ ] Accede a `/politica-privacidad` (debe cargar la página legal)
- [ ] Accede a `/terminos-condiciones` (debe cargar términos)
- [ ] Accede a `/estudiante/registro` (debe mostrar formulario completo con 16 campos)

---

### 2️⃣ **RENDER (Backend)**

**Acciones a realizar:**

1. Ve a: https://dashboard.render.com
2. Busca tu servicio de backend
3. Verifica:
   - ✅ Branch: `main`
   - ✅ Último commit: `078c0d5` o `bbbe7bb`
   - ✅ Estado: "Live" (verde)
   - ✅ Copia la URL del servicio

**📝 URL del Backend:**
```
https://_________________________.onrender.com
```

**Variables de entorno a verificar:**

En Render → Environment → Verifica que existan:

```env
DATABASE_URL=postgresql://... (ya configurada)
PYTHONIOENCODING=utf-8
SECRET_KEY=visas-estudio-secret-key-2025-production

# Email (OPCIONAL - para notificaciones)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
ADMIN_EMAIL=admin@tuagencia.com

# OCR
OCR_SPACE_API_KEY=K81993791988957

# CORS - IMPORTANTE
FRONTEND_URL=https://TU-URL-DE-VERCEL.vercel.app
```

**Pruebas a realizar:**

- [ ] Accede a `https://TU-BACKEND.onrender.com/docs` (debe mostrar Swagger UI)
- [ ] Verifica endpoints disponibles:
  - `GET /api/estudiantes` (debe responder 401 o 200)
  - `POST /api/estudiantes` (debe estar listado)
  - `GET /api/admin/estudiantes/{id}/sugerir-cursos` (debe estar listado)
  - `GET /api/admin/estudiantes/{id}/calcular-probabilidad` (debe estar listado)

---

### 3️⃣ **CONFIGURAR CORS (Conectar Frontend-Backend)**

**Acción CRÍTICA:**

1. En Render → Environment → Agregar/actualizar:
   ```
   FRONTEND_URL=https://TU-URL-REAL-DE-VERCEL.vercel.app
   ```

2. En Vercel → Settings → Environment Variables → Agregar:
   ```
   VITE_API_URL=https://TU-URL-REAL-DE-RENDER.onrender.com
   ```

3. **Redesplegar ambos:**
   - Vercel: Va al proyecto → Deployments → Tres puntos → Redeploy
   - Render: Automáticamente redespliega al guardar variables

---

### 4️⃣ **PRUEBA COMPLETA END-TO-END**

Una vez configurado CORS, realizar:

**A. Registro de estudiante:**

- [ ] Accede a `https://TU-FRONTEND.vercel.app/estudiante/registro`
- [ ] Completa formulario con todos los campos:
  - Nombre: Test Producción
  - Email: test-produccion@test.com
  - Teléfono: +34600111222
  - Pasaporte: TEST12345
  - Edad: 25
  - Nacionalidad: Colombia
  - Ciudad: Bogotá
  - Especialidad: Medicina
  - Nivel español: Intermedio
  - Tipo visa: Estudiante
  - Fondos: 8000
  - Duración: 12 meses
  - Curso específico: Grado en Medicina
  - Alojamiento: Por definir
  - Seguro médico: No
  - Acepta términos: Sí
- [ ] Subir 3 archivos (pueden ser cualquier PDF/imagen)
- [ ] Click "Registrar"
- [ ] Debe recibir código de acceso (6 caracteres)

**B. Login y Dashboard:**

- [ ] Accede a `https://TU-FRONTEND.vercel.app/estudiante/login`
- [ ] Ingresa email y código de acceso
- [ ] Debe mostrar dashboard con:
  - 5 tarjetas (Info Personal, Académica, Visa, Financiera, Documentos)
  - Probabilidad de éxito (calculada automáticamente)
  - Cursos sugeridos (2-5 cursos)
  - Botón "Generar Documentos"

**C. Documentos:**

- [ ] Click en "Generar Documentos"
- [ ] Debe descargar 3 PDFs:
  - Carta de aceptación (borrador)
  - Carta de patrocinio (borrador)
  - Checklist de documentos

**D. Páginas legales:**

- [ ] Accede a `/politica-privacidad` (debe cargar completa)
- [ ] Accede a `/terminos-condiciones` (debe cargar completa)

---

## 🔧 CONFIGURACIÓN DE BACKUPS AUTOMÁTICOS

**Una vez verificado que todo funciona:**

### Windows:

```powershell
# Ejecutar como Administrator
cd C:\BotVisasEstudio
.\configurar_backups.ps1
```

Selecciona opción 1 (Diario a las 2 AM)

### Linux/Mac:

```bash
# Agregar a crontab
crontab -e

# Agregar esta línea (diario a las 2 AM)
0 2 * * * cd /ruta/a/BotVisasEstudio && python backup_database.py
```

---

## 📧 CONFIGURAR NOTIFICACIONES EMAIL (OPCIONAL)

**Para que funcionen las alertas automáticas:**

1. **Crear App Password en Gmail:**
   - Ve a: https://myaccount.google.com/apppasswords
   - Genera contraseña de aplicación
   - Copia el código de 16 caracteres

2. **Agregar en Render:**
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=tu-email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx (16 caracteres)
   ADMIN_EMAIL=admin@tuagencia.com
   ```

3. **Guardar y redesplegar**

4. **Probar:**
   ```bash
   python backup_database.py
   ```
   Deberías recibir email con resultado del backup.

---

## ✅ RESULTADO ESPERADO

Una vez completado TODO:

- ✅ Frontend accesible públicamente con todas las páginas
- ✅ Backend funcionando con todos los endpoints
- ✅ Estudiantes pueden registrarse y ver dashboard
- ✅ Probabilidad y cursos se calculan automáticamente
- ✅ Documentos se generan correctamente
- ✅ Páginas legales accesibles
- ✅ Backups programados diariamente
- ✅ Notificaciones por email (opcional)

**¡PASO 6 COMPLETO!** 🎉

---

## 🐛 TROUBLESHOOTING COMÚN

### Error CORS en Frontend

**Síntoma:** Frontend no se conecta al backend, errores en consola del navegador.

**Solución:**
1. Verifica que `FRONTEND_URL` en Render tenga la URL exacta de Vercel
2. Verifica que `VITE_API_URL` en Vercel tenga la URL exacta de Render
3. Redespliega ambos servicios

### Backend con error 500

**Síntoma:** Backend no responde o da error interno.

**Solución:**
1. Ve a Render → Logs
2. Busca errores de importación o variables faltantes
3. Verifica que `DATABASE_URL` esté configurada
4. Verifica que `SECRET_KEY` esté configurada

### Registro no funciona

**Síntoma:** Formulario no envía datos o da error.

**Solución:**
1. Abre consola del navegador (F12)
2. Ve a Network → Busca la petición POST
3. Verifica que la URL sea la correcta (debe ser la de Render)
4. Verifica respuesta del servidor

### Documentos no generan

**Síntoma:** Botón no funciona o descarga vacía.

**Solución:**
1. Verifica en backend logs que el endpoint se ejecuta
2. Verifica que el estudiante tenga todos los datos necesarios
3. Prueba con el test: `python test_sistema_completo.py`

---

## 📊 MÉTRICAS DE ÉXITO

**Sistema funcionando 100% cuando:**

- ✅ 5+ estudiantes registrados en producción
- ✅ Todos ven su probabilidad calculada
- ✅ Todos reciben sugerencias de cursos
- ✅ Documentos generados sin errores
- ✅ Páginas legales accesibles
- ✅ Sin errores CORS
- ✅ Backups ejecutándose diariamente
- ✅ Base de datos con todos los registros

---

**Siguiente fase:** Admin features (revisar, aprobar, asignar cursos, comentarios internos)
