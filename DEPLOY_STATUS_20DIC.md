# 🔧 Deploy Status - 20 Diciembre 2025

## Problema Reportado
**Usuario:** Manuel (ID: 16)
**Error:** Al completar perfil, obtenía error 500
**Causa:** Campo `fondos_disponibles` era obligatorio pero el frontend no lo enviaba

## Cambios Realizados

### Commit 1: b2be532
- Cambió `fondos_disponibles: float = Form(...)` → `Form(None)` 
- Cambió SQL: `fondos_disponibles = %s` → `COALESCE(%s, fondos_disponibles)`
- Hora: ~10 minutos atrás

### Commit 2: 07db32d  
- Force rebuild con cambio en header
- Hora: Ahora mismo

## Estado del Deploy

### Git Status
✅ Commits pusheados a origin/main
✅ GitHub actualizado

### Render Deploy
⏳ Esperando auto-deploy (3-5 minutos)
- Service: bot-visas-api
- Branch: main
- Último commit: 07db32d

## Verificación

### Probar cuando Render termine:
1. Ir a: https://bot-visas-api.onrender.com/api/estudiantes/16/completar-perfil
2. Enviar datos SIN fondos_disponibles
3. Debe responder 200 OK (no 500)

### Decirle a Manuel:
"Ya está arreglado. Recarga la página (Ctrl+F5) y completa tu perfil. Si aún falla, espera 5 minutos más."

## Tiempo Estimado
- **Deploy en Render:** 3-5 minutos
- **Total desde push:** ~5-7 minutos
- **Hora de completado estimada:** ~[HORA_ACTUAL + 5min]

## Logs a Monitorear
```
# Debe desaparecer este error:
fastapi.exceptions.RequestValidationError: [{'type': 'missing', 'loc': ('body', 'fondos_disponibles'), 'msg': 'Field required'

# Debe aparecer:
INFO: "PUT /api/estudiantes/16/completar-perfil?codigo_acceso=XJKRSKSD HTTP/1.1" 200 OK
```

## Solución Permanente
Campo `fondos_disponibles` ahora es opcional. Se puede agregar después en otra sección del perfil.
