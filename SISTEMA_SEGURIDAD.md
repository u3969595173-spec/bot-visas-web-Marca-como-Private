# 🔐 Sistema de Seguridad y Monitoreo

## ✅ Implementaciones de Seguridad

### 1. **Rate Limiting** (Prevención de Abuso)

#### ¿Qué hace?
Limita la cantidad de peticiones que una IP puede hacer en un periodo de tiempo.

#### Límites Configurados:

**Endpoints Públicos:**
- `POST /api/estudiantes` → **3 registros/hora** por IP
- `POST /api/login` → **5 intentos/minuto** por IP

**Endpoints Admin:**
- Todos los endpoints `/api/admin/*` → Sin límite (autenticados)

#### Ejemplos de Bloqueo:

```json
// Después del 3er registro en 1 hora:
{
  "error": "Rate limit exceeded: 3 per 1 hour",
  "detail": "Too many requests. Try again in 45 minutes."
}

// Después del 5to intento de login en 1 minuto:
{
  "error": "Rate limit exceeded: 5 per 1 minute",
  "detail": "Too many requests. Try again in 30 seconds."
}
```

#### Cómo Funciona:

1. **Identificación:** Usa la IP del usuario
2. **Contador:** Cuenta requests por endpoint
3. **Bloqueo:** Si excede límite → HTTP 429
4. **Reset:** Contador se reinicia después del tiempo

---

### 2. **Logs Estructurados** (Debugging y Auditoría)

#### ¿Qué hace?
Registra todos los eventos importantes en formato JSON para análisis.

#### Eventos Registrados:

**Registros:**
```json
{
  "timestamp": "2025-11-27T15:30:45.123456",
  "event_type": "registro_intento",
  "message": "Intento de registro de estudiante",
  "email": "juan@example.com",
  "nombre": "Juan Pérez",
  "pais_origen": "Colombia",
  "ip": "192.168.1.100"
}

{
  "timestamp": "2025-11-27T15:30:48.789012",
  "event_type": "registro_exitoso",
  "message": "Estudiante registrado correctamente",
  "estudiante_id": 123,
  "codigo_acceso": "ESP-2025-A7B9C2",
  "email": "juan@example.com",
  "carrera_deseada": "Ingeniería",
  "ip": "192.168.1.100"
}
```

**Login:**
```json
{
  "timestamp": "2025-11-27T16:00:12.345678",
  "event_type": "login_exitoso",
  "message": "Login exitoso",
  "email": "admin@example.com",
  "nombre": "Admin",
  "rol": "admin",
  "ip": "10.0.0.1"
}

{
  "timestamp": "2025-11-27T16:05:30.111222",
  "event_type": "login_fallido",
  "message": "Login fallido - contraseña incorrecta",
  "email": "hacker@fake.com",
  "ip": "123.45.67.89"
}
```

**Errores:**
```json
{
  "timestamp": "2025-11-27T17:10:22.999888",
  "level": "ERROR",
  "event_type": "registro_error",
  "message": "Error al registrar estudiante",
  "error_message": "Duplicate key violation",
  "error_class": "IntegrityError",
  "email": "duplicate@test.com",
  "ip": "192.168.1.50"
}
```

#### Dónde Ver los Logs:

**Render:**
1. Dashboard → tu servicio → **Logs** (menú izquierdo)
2. Logs en tiempo real
3. Puedes filtrar, buscar y descargar

**Local (desarrollo):**
```bash
# Los logs aparecen en la consola cuando ejecutas:
uvicorn api.main:app --reload
```

---

## 📊 Análisis de Logs

### Buscar Eventos Específicos:

**En Render:**
```
# Buscar todos los registros exitosos:
"registro_exitoso"

# Buscar registros de un país específico:
"Colombia"

# Buscar errores:
"ERROR"

# Buscar intentos de login fallidos:
"login_fallido"

# Buscar actividad de una IP sospechosa:
"123.45.67.89"
```

### Detectar Ataques:

**Señales de alerta:**
```
# Muchos login_fallido desde una IP:
→ Posible ataque de fuerza bruta

# Rate limit exceeded repetido:
→ Posible intento de DDoS

# Muchos registros con datos similares:
→ Posible spam automatizado

# Errores repetidos del mismo tipo:
→ Problema técnico que requiere atención
```

---

## 🛠️ Configuración

### Cambiar Límites de Rate Limiting:

```python
# En api/main.py

# Más restrictivo (menos peticiones):
@limiter.limit("2/hour")  # Solo 2 registros por hora

# Más permisivo (más peticiones):
@limiter.limit("10/hour")  # Hasta 10 registros por hora

# Por minuto en vez de por hora:
@limiter.limit("1/minute")  # 1 registro por minuto

# Múltiples límites:
@limiter.limit("10/hour;2/minute")  # Máx 10/hora Y máx 2/minuto
```

### Agregar Rate Limiting a Otros Endpoints:

```python
@app.post("/api/nuevo-endpoint")
@limiter.limit("20/minute")  # Agregar límite
async def nuevo_endpoint(...):
    pass
```

### Agregar Logging a Otros Endpoints:

```python
from utils.logger import log_event, log_error

@app.post("/api/nuevo-endpoint")
async def nuevo_endpoint(...):
    # Log evento
    log_event(
        "nuevo_evento",
        "Descripción del evento",
        campo1="valor1",
        campo2="valor2"
    )
    
    try:
        # ... código
        
        log_event(
            "evento_exitoso",
            "Operación completada",
            resultado="success"
        )
    except Exception as e:
        log_error(
            "evento_error",
            "Error en operación",
            error=e,
            contexto="adicional"
        )
```

---

## 📈 Métricas y Estadísticas

### Eventos que Puedes Rastrear:

- ✅ Registros por día/hora
- ✅ Países de origen más comunes
- ✅ Intentos de login fallidos
- ✅ Errores más frecuentes
- ✅ Tiempos de respuesta
- ✅ IPs bloqueadas por rate limit
- ✅ Carreras más solicitadas

### Ejemplo de Análisis:

```bash
# Contar registros exitosos hoy:
grep "registro_exitoso" logs.txt | wc -l

# Ver países de origen:
grep "pais_origen" logs.txt | sort | uniq -c

# Detectar IPs problemáticas:
grep "login_fallido" logs.txt | grep -o '"ip":"[^"]*"' | sort | uniq -c | sort -nr
```

---

## 🚨 Alertas Recomendadas

### Configurar Notificaciones:

1. **Más de 10 login fallidos en 5 minutos** → Alerta de seguridad
2. **Más de 5 errores del mismo tipo en 1 hora** → Problema técnico
3. **Rate limit exceeded > 20 veces/hora** → Posible ataque
4. **Registro exitoso** → Notificación al admin (ya implementado)

---

## ✅ Checklist de Seguridad

- ✅ Rate limiting en endpoints públicos
- ✅ Logs estructurados de todos los eventos
- ✅ Autenticación con JWT
- ✅ Passwords con bcrypt
- ✅ HTTPS en producción
- ✅ CORS configurado
- ✅ Repositorio privado en GitHub
- ✅ Variables de entorno para credenciales
- ⏳ **TODO:** Backup automático de logs
- ⏳ **TODO:** Monitoreo con Sentry (opcional)

---

## 🎓 Buenas Prácticas

1. **Revisa logs diariamente** para detectar anomalías
2. **Ajusta rate limits** según el uso real
3. **Documenta eventos nuevos** cuando agregues funcionalidades
4. **Mantén logs por 30 días** mínimo (Render lo hace automático)
5. **Alerta inmediata** si ves múltiples login_fallido

---

## 📞 Soporte

Si ves logs que no entiendes o necesitas ayuda:
1. Copia el log completo (JSON)
2. Anota fecha y hora exacta
3. Describe qué estabas haciendo
4. Contacta soporte con toda esa info
