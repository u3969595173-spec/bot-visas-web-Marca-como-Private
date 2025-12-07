# ✅ Sistema de Notificaciones por Email al Admin

## 📧 Notificaciones Implementadas

### 1. **Nuevo Registro de Estudiante** 🆕
**Cuándo:** Un nuevo estudiante completa el registro
**Endpoint:** `POST /api/estudiantes/registro`
**Archivo:** `api/main.py` línea ~850
**Función:** `notificar_nuevo_registro()`
**Contenido del email:**
- Nombre del estudiante
- Email
- Teléfono
- Código de acceso
- Fecha de registro
- Botón: "Ver en Panel de Admin"

---

### 2. **Solicitud de Presupuesto** 💰
**Cuándo:** Un estudiante solicita un presupuesto de servicios
**Endpoint:** `POST /api/presupuestos/solicitar`
**Archivo:** `api/main.py` línea ~9191
**Función:** `notificar_solicitud_presupuesto()`
**Contenido del email:**
- Datos del estudiante
- Lista de servicios solicitados
- Total en euros
- Botón: "Ver Presupuesto en Admin"

---

### 3. **Perfil Completado** ✅
**Cuándo:** Un estudiante completa su perfil
**Endpoint:** `PUT /api/estudiantes/{id}`
**Archivo:** `api/main.py` línea ~1146
**Función:** `notificar_perfil_completado()`
**Contenido del email:**
- Información del estudiante
- Carrera deseada
- Fecha de nacimiento
- Fecha de completado
- Botón: "Ver Perfil Completo"

---

### 4. **Nuevo Mensaje del Estudiante** 💬
**Cuándo:** Un estudiante envía un mensaje al admin
**Endpoint:** `POST /api/estudiantes/{estudiante_id}/mensajes`
**Archivo:** `api/main.py` línea ~4070
**Función:** `notificar_nuevo_mensaje()`
**Contenido del email:**
- Nombre del estudiante
- Email
- Preview del mensaje (primeros 200 caracteres)
- Hora del mensaje
- Botón: "Responder en el Chat"

---

### 5. **Documentos Subidos** 📄
**Cuándo:** Un estudiante sube documentos (pasaporte, título, notas, etc.)
**Endpoint:** `POST /api/documentos/{estudiante_id}/subir`
**Archivo:** `api/main.py` línea ~5840
**Función:** `notificar_documentos_subidos()`
**Contenido del email:**
- Datos del estudiante
- Lista de documentos subidos con nombres de archivo
- Botón: "Revisar Documentos"

---

### 6. **Presupuesto Aceptado** ✅
**Cuándo:** Un estudiante acepta un presupuesto
**Endpoint:** `PUT /api/presupuestos/{presupuesto_id}/respuesta`
**Archivo:** `api/main.py` línea ~9720
**Función:** `enviar_email_admin()` (custom)
**Contenido del email:**
- Datos del estudiante
- ID del presupuesto
- Modalidad de pago seleccionada (al empezar/con visa/financiado)
- Monto según modalidad
- Fecha de aceptación
- Botón: "Ver en Panel Admin"

---

## 🔧 Configuración SMTP

Las notificaciones requieren que estén configuradas las siguientes variables de entorno en `.env`:

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=estudiovisaespana@gmail.com
SMTP_PASSWORD=tu_contraseña_de_aplicacion_gmail
ADMIN_EMAIL=estudiovisaespana@gmail.com
```

### Obtener Contraseña de Aplicación de Gmail:
1. Ve a https://myaccount.google.com/apppasswords
2. Selecciona "Correo" como aplicación
3. Copia la contraseña de 16 caracteres
4. Agrégala a tu `.env` como `SMTP_PASSWORD`

---

## 🧪 Probar Configuración

Ejecuta el script de prueba:
```bash
python test_smtp.py
```

Este script:
- Verifica las variables de entorno SMTP
- Envía un email de prueba al admin
- Confirma que la configuración funciona correctamente

---

## 📝 Notas Importantes

1. **Render.com**: Si estás usando Render, asegúrate de agregar las variables de entorno SMTP en el panel de configuración del servicio.

2. **Seguridad**: Nunca subas el archivo `.env` al repositorio. Usa `.env.example` como plantilla.

3. **Testing**: Los emails van a `ADMIN_EMAIL`. Revisa la bandeja de spam si no los recibes.

4. **Performance**: Las notificaciones se envían de forma asíncrona para no bloquear las respuestas de la API.

---

## 🎨 Diseño de los Emails

Todos los emails incluyen:
- ✅ HTML responsive
- 🎨 Gradientes de colores según el tipo de notificación
- 📱 Compatible con clientes móviles
- 🔘 Botones de acción directa
- ⚡ Iconos emojis para mejor UX

---

## 🚀 Próximas Mejoras

- [ ] Notificación cuando se completa un pago
- [ ] Notificación cuando se sube un documento al expediente
- [ ] Resumen diario de actividad
- [ ] Notificaciones por Telegram (opcional)
- [ ] Panel de historial de notificaciones enviadas
