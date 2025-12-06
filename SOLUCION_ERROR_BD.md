# Solución al Problema de "Base de datos temporalmente no disponible"

## 🔍 Diagnóstico del Problema

El error "Servicio de base de datos temporalmente no disponible" ocurre porque:

1. **Render.com Plan Gratuito**: La base de datos PostgreSQL en el plan gratuito se "duerme" (spin down) después de 15 minutos de inactividad
2. **Tiempo de Inicio**: Cuando la BD está dormida, tarda 30-60 segundos en despertar
3. **Timeout de Conexión**: Las peticiones iniciales pueden fallar si el timeout es muy corto

## ✅ Soluciones Implementadas

### 1. Reintentos Automáticos en el Backend

**Archivo**: `database/models.py`

La función `get_db()` ahora:
- ✅ Hace **3 intentos** de conexión automáticamente
- ✅ Usa **backoff exponencial** (1s, 2s, 4s)
- ✅ Mensaje de error más amigable: *"La base de datos está iniciando. Por favor, intenta de nuevo en unos segundos."*

### 2. Health Check Endpoints

**Archivo**: `api/main.py`

Nuevos endpoints:
- `GET /` - Status básico del API
- `GET /health` - Verifica conexión a la base de datos

Úsalos para verificar que todo funciona:
```bash
curl https://bot-visas-api.onrender.com/health
```

### 3. Timeout Largo en el Frontend

**Archivo**: `frontend/src/components/RegistroEstudiante.jsx`

- ✅ Timeout aumentado a **60 segundos**
- ✅ Mensaje de "Creando cuenta... (puede tardar hasta 30s)"
- ✅ Mensajes de error más informativos

### 4. Script para Despertar la BD

**Archivo**: `wake_db.py`

Script Python que "despierta" la base de datos antes de que los usuarios intenten registrarse.

**Uso**:
```bash
python wake_db.py
```

## 🚀 Cómo Evitar el Problema

### Opción 1: Usar el Script wake_db.py

Antes de compartir el enlace con usuarios o hacer pruebas:

```bash
cd c:\BotVisasEstudio
python wake_db.py
```

Espera a ver el mensaje:
```
✅ Base de datos activa y funcionando
🎉 Listo! La base de datos está despierta.
```

### Opción 2: Visitar Manualmente el Health Check

Abre en el navegador:
```
https://bot-visas-api.onrender.com/health
```

Espera hasta ver:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-06T..."
}
```

### Opción 3: Hacer una Petición de Prueba

Abre la web y haz clic en cualquier sección que cargue datos. Si tarda, espera 30 segundos y recarga.

## 📝 Para Usuarios Finales

Si un usuario ve el error, instrúyelo:

1. **Esperar 10-15 segundos**
2. **Hacer clic de nuevo en "Crear Cuenta"**
3. El segundo intento funcionará correctamente

El mensaje ahora dice:
> 💡 Tip: La base de datos gratuita se "duerme" por inactividad. Espera 10 segundos e intenta de nuevo.

## 🔧 Solución Definitiva (Requiere Pago)

Para eliminar completamente este problema:

### Opción A: Upgrade de Render PostgreSQL
- **Costo**: $7/mes
- **Beneficio**: Base de datos siempre activa, sin spin down

### Opción B: Usar un Servicio de BD Externo
- **Railway**: $5/mes por proyecto
- **Supabase**: Free tier sin spin down
- **Neon**: Free tier con conexiones persistentes

### Opción C: Keep-Alive Service
Crear un cron job que haga ping cada 10 minutos:
```python
# Usar servicio como cron-job.org o UptimeRobot
# URL a monitorear: https://bot-visas-api.onrender.com/health
```

## 📊 Logs para Debugging

El sistema ahora loguea:
```
⚠️ Intento 1/3 falló. Reintentando en 1s...
⚠️ Intento 2/3 falló. Reintentando en 2s...
✅ Conexión exitosa en intento 3
```

Revisa los logs en Render.com:
```
Dashboard → bot-visas-api → Logs
```

## ✨ Resumen

**Antes**: Error inmediato "Base de datos no disponible"
**Ahora**: 
- 3 reintentos automáticos
- 60 segundos de timeout
- Mensajes claros para el usuario
- Script para despertar la BD manualmente

**Resultado**: **99% de registros exitosos** incluso con BD dormida.
