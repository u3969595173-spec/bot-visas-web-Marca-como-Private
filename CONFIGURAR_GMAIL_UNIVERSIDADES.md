# 🔧 CONFIGURAR GMAIL PARA ENVIAR EMAILS A UNIVERSIDADES

## PASO 1: Crear Contraseña de Aplicación en Gmail

### 1.1 Verificar Cuenta Gmail
- Necesitas una cuenta Gmail activa
- **Recomendado**: Usar email profesional tipo `contacto@estudiaenespana.com` (puedes usar Gmail con dominio propio)
- O usa tu Gmail personal temporalmente

### 1.2 Activar Verificación en 2 Pasos

1. Ve a tu cuenta Google: https://myaccount.google.com/
2. Menú izquierdo → **Seguridad**
3. Busca sección **Verificación en 2 pasos**
4. Click **Activar** (si no está activada)
5. Sigue el proceso (SMS, app autenticadora, etc.)

### 1.3 Generar Contraseña de Aplicación

**⚠️ IMPORTANTE: No uses tu contraseña normal de Gmail**

1. Ve a: https://myaccount.google.com/apppasswords
2. O navega: Cuenta Google → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones
3. Selecciona:
   - **App**: Correo
   - **Dispositivo**: Windows/Otro
4. Click **Generar**
5. **COPIA LA CONTRASEÑA DE 16 CARACTERES** (tipo: `abcd efgh ijkl mnop`)
   - ⚠️ Solo se muestra UNA VEZ
   - Anótala en lugar seguro

## PASO 2: Configurar Variables de Entorno

### Opción A: Variables de Entorno Render (Producción)

1. Ve a: https://dashboard.render.com
2. Selecciona tu servicio: `bot-visas-api`
3. Click **Environment** (menú izquierdo)
4. Añadir estas variables:

```
EMAIL_SENDER=tu_email@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop    (La contraseña de 16 caracteres)
NOMBRE_AGENCIA=Estudia en España
TELEFONO_CONTACTO=+53 XXXXXXXX     (Tu WhatsApp)
WEB_AGENCIA=https://fortunariocash.com
```

5. Click **Save Changes**
6. Render reiniciará automáticamente

### Opción B: Archivo .env Local (Desarrollo)

1. Abre el archivo `.env` en la raíz del proyecto
2. Añade estas líneas:

```env
# Configuración Gmail para envío de emails
EMAIL_SENDER=tu_email@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com

# Información de contacto
NOMBRE_AGENCIA=Estudia en España
TELEFONO_CONTACTO=+53 XXXXXXXX
WEB_AGENCIA=https://fortunariocash.com
```

3. **Guarda el archivo**
4. **⚠️ NUNCA subas el .env a GitHub** (ya está en .gitignore)

## PASO 3: Verificar Configuración

### Prueba Local (Opcional)

Crea archivo `test_gmail.py`:

```python
import os
from dotenv import load_dotenv
from api.email_utils import enviar_email

load_dotenv()

# Prueba envío
resultado = enviar_email(
    destinatario="tu_email_personal@gmail.com",
    asunto="✅ Prueba Sistema Universidades",
    cuerpo_html="<h1>Funciona!</h1><p>El sistema de emails está configurado correctamente.</p>"
)

if resultado:
    print("✅ Email enviado correctamente")
else:
    print("❌ Error al enviar email")
```

Ejecutar:
```bash
python test_gmail.py
```

## PASO 4: Usar el Sistema

### Desde la Web Admin

1. Login admin: https://fortunariocash.com/admin/login
2. Click botón morado: **🏛️ Contactar Universidades**
3. Verás 5 universidades precargadas:
   - ✅ UCAM Murcia
   - ✅ UNIR
   - ✅ VIU Valencia
   - ✅ INSA Barcelona
   - ✅ EU Business School

4. Configura:
   - **Número de estudiantes**: 15 (o el número real)
   - **Observaciones**: "Estudiantes interesados principalmente en Ingeniería y Administración"

5. Click **📧 Enviar Email** en cada universidad

### Qué Sucede

- ✅ Email profesional enviado automáticamente
- ✅ Estado cambia a "Contactado"
- ✅ Se registra fecha y hora
- ✅ Email incluye:
  - Tu nombre y rol
  - Número de estudiantes
  - Propuesta profesional
  - Temas a discutir
  - Disponibilidad para reunión
  - Datos de contacto

## SOLUCIÓN DE PROBLEMAS

### Error: "Username and Password not accepted"

**Causa**: Contraseña incorrecta o no es contraseña de aplicación

**Solución**:
1. Verifica que usaste **contraseña de aplicación** (16 caracteres)
2. No uses tu contraseña normal de Gmail
3. Regenera la contraseña en: https://myaccount.google.com/apppasswords

### Error: "SMTP Authentication Error"

**Causa**: Verificación en 2 pasos no activada

**Solución**:
1. Activa verificación en 2 pasos: https://myaccount.google.com/security
2. Genera nueva contraseña de aplicación

### Error: "Connection refused"

**Causa**: Firewall o SMTP bloqueado

**Solución**:
1. Verifica conexión a internet
2. Prueba con otro WiFi/red
3. Contacta proveedor internet (algunos bloquean puerto 587)

### Emails van a SPAM

**Solución**:
1. Primera vez siempre va a SPAM → marca como "No es spam"
2. Añade tu email a contactos de las universidades
3. Usa dominio propio (estudiaenespana.com) en lugar de Gmail personal

## RECOMENDACIONES

### Email Profesional

Si quieres proyectar más profesionalismo:

1. **Compra dominio**: estudiaenespana.com (€10/año en Namecheap)
2. **Configura Google Workspace**: €6/mes
3. **Email profesional**: contacto@estudiaenespana.com
4. Ventajas:
   - ✅ Más credibilidad
   - ✅ Menos probabilidad SPAM
   - ✅ Mejor imagen ante universidades

### Seguimiento

**Día 1**: Enviar emails a las 5 universidades
**Día 3**: Llamar por teléfono si no responden
**Día 5**: Email de seguimiento automático (próxima feature)

### Tracking

El sistema registra automáticamente:
- ✅ Fecha de contacto
- ✅ Estado (pendiente → contactado → respondió)
- ✅ Notas de cada interacción
- ✅ Fecha de reuniones
- ✅ Condiciones acordadas

## PRÓXIMOS PASOS

Una vez configurado:

1. ✅ Enviar emails a las 5 universidades HOY
2. 📞 Preparar script telefónico para seguimiento
3. 📅 Agendar reuniones (usa Calendly o similar)
4. 💼 Negociar condiciones (comisiones, becas, pagos)
5. ✍️ Firmar acuerdos y empezar a operar

## SOPORTE

Si tienes problemas:
1. Revisa logs en Render: https://dashboard.render.com → Logs
2. Verifica variables de entorno están correctas
3. Prueba envío local primero
4. Consulta docs Gmail: https://support.google.com/mail/answer/185833

---

**¿LISTO PARA CONTACTAR UNIVERSIDADES?** 🚀

Una vez configurado Gmail, solo haz click y los emails se envían automáticamente.
¡En 10 minutos puedes contactar las 5 universidades!
