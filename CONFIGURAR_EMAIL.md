# 📧 Configuración de Email (Gmail)

## ⚠️ IMPORTANTE: Sin esta configuración, NO se enviarán emails

El sistema envía emails automáticos para:
- ✉️ Bienvenida al registrarse
- ✅ Aprobación de documentos
- ❌ Rechazo de documentos
- 📄 Documentos listos para descargar
- ⏰ Recordatorios de documentos pendientes
- 🎓 Asignación de curso

---

## 🔧 PASOS PARA CONFIGURAR (5 minutos)

### 1️⃣ Crear/Usar cuenta Gmail

Usa una cuenta Gmail existente o crea una nueva:
- **Recomendado:** Crear cuenta nueva tipo `tueagencia@gmail.com`
- **No usar:** Tu email personal

### 2️⃣ Activar verificación en 2 pasos

1. Ve a: https://myaccount.google.com/security
2. Busca "Verificación en 2 pasos"
3. Clic en "Activar" y sigue los pasos
4. ✅ Deberías ver "Verificación en 2 pasos: Activada"

### 3️⃣ Generar App Password (Contraseña de aplicación)

1. Ve a: https://myaccount.google.com/apppasswords
2. Si no ves la página:
   - Asegúrate de que activaste la verificación en 2 pasos
   - Cierra sesión y vuelve a entrar
3. Selecciona:
   - **Aplicación:** Correo
   - **Dispositivo:** Otro (personalizado)
   - **Nombre:** `Bot Visas Estudio`
4. Clic en "Generar"
5. 📋 **COPIA** la contraseña de 16 caracteres (con espacios)
   - Ejemplo: `abcd efgh ijkl mnop`

### 4️⃣ Editar archivo .env

Abre el archivo `.env` en la raíz del proyecto y modifica estas líneas:

```env
# === EMAIL (SMTP) ===
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tueagencia@gmail.com              # ← TU EMAIL AQUI
SMTP_PASSWORD=abcd efgh ijkl mnop           # ← TU APP PASSWORD AQUI
ADMIN_EMAIL=admin@tueagencia.com            # ← EMAIL ADMIN (puedes usar el mismo)
```

**⚠️ IMPORTANTE:**
- Usa el App Password de 16 caracteres, NO tu contraseña normal de Gmail
- Puedes dejar los espacios en el App Password
- NO compartas este archivo con nadie

### 5️⃣ Reiniciar servidor

```powershell
# Detén el servidor (Ctrl+C) y vuelve a iniciar:
cd C:\BotVisasEstudio
uvicorn api.main:app --reload
```

---

## ✅ PROBAR QUE FUNCIONA

### Opción 1: Probar endpoint directo

1. Ve a: http://localhost:8000/docs
2. Busca `POST /api/notificaciones/test-email`
3. Clic en "Try it out"
4. Ingresa tu email de prueba
5. Clic en "Execute"
6. Revisa tu bandeja de entrada

### Opción 2: Registrar estudiante

1. Ve a: http://localhost:3000/registro
2. Completa el formulario
3. Enviar
4. ✅ Deberías recibir email de bienvenida

---

## 🐛 PROBLEMAS COMUNES

### ❌ Error: "Authentication failed"
**Causa:** App Password incorrecto
**Solución:** 
1. Genera un nuevo App Password
2. Copia sin errores
3. Actualiza `.env`

### ❌ Error: "Username and Password not accepted"
**Causa:** No activaste verificación en 2 pasos
**Solución:** 
1. Ve a https://myaccount.google.com/security
2. Activa verificación en 2 pasos
3. Luego genera App Password

### ❌ Email llega a SPAM
**Normal al principio**
**Solución:**
1. Marca como "No es spam"
2. Agrega el email a contactos
3. Considera usar servicio profesional (SendGrid, Mailgun)

---

## 🚀 ALTERNATIVA: Usar otro servicio SMTP

Si prefieres NO usar Gmail:

### SendGrid (Gratis hasta 100 emails/día)
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=tu-api-key-de-sendgrid
```

### Mailgun (Gratis hasta 100 emails/día)
```env
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@tu-dominio.mailgun.org
SMTP_PASSWORD=tu-password-de-mailgun
```

---

## ℹ️ Configuración actual

Para ver tu configuración actual:

```powershell
Get-Content .env | Select-String "SMTP"
```

**Debería mostrar:**
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tuemail@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
```

---

## 📞 AYUDA

Si sigues teniendo problemas:
1. Verifica que copiaste bien el App Password (16 caracteres)
2. Verifica que el email existe y puede enviar emails
3. Intenta con otro email de Gmail
4. Considera usar SendGrid como alternativa

**Estado del sistema de emails:**
- ✅ Código implementado y funcionando
- ✅ Templates de emails creados
- ⏳ Solo falta configurar credenciales SMTP

Una vez configurado, los emails se enviarán automáticamente sin necesidad de intervención manual.
