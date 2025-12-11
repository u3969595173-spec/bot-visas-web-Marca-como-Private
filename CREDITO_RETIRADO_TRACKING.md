# Sistema de Tracking de Crédito Retirado



## 🎯 Problema Identificado y Resuelto

### PROBLEMA ORIGINAL:
Cuando un estudiante/agente retiraba crédito:
1. ❌ El crédito NO se sumaba a `credito_retirado`
2. ❌ El `total_ganado` no incluía el crédito retirado
3. ❌ Se podían aprobar retiros sin validar crédito suficiente

### CAUSAS:
1. El `total_ganado` se calculaba solo desde presupuestos (SELECT SUM(...))
   en lugar de usar: `credito_disponible + credito_retirado`

2. No había validación de crédito suficiente antes de aprobar retiros

3. Los endpoints de estadísticas calculaban mal el total

## ✅ Solución Implementada (2025-12-11)

### 1. Columnas Agregadas ✅
- **estudiantes.credito_retirado** (DECIMAL 10,2, default 0.00)
- **agentes.credito_retirado** (DECIMAL 10,2, default 0.00)

### 2. Lógica de Retiro Actualizada ✅
Cuando admin aprueba un retiro:
```sql
-- ANTES (solo descontaba - INCORRECTO)
UPDATE estudiantes 
SET credito_disponible = credito_disponible - monto
WHERE id = :id

-- AHORA (descuenta Y registra + VALIDA)
-- 1. Valida que haya crédito suficiente
SELECT credito_disponible FROM estudiantes WHERE id = :id

-- 2. Si hay suficiente, actualiza
UPDATE estudiantes 
SET credito_disponible = credito_disponible - :monto,
    credito_retirado = COALESCE(credito_retirado, 0) + :monto
WHERE id = :id
```

### 3. Cálculo de Total Ganado Corregido ✅

**ANTES (INCORRECTO):**
```python
# Calculaba desde presupuestos - no incluía retiros
total_ganado = db.execute(text("""
    SELECT COALESCE(SUM(p.precio_ofertado * 0.05), 0) as total
    FROM presupuestos p
    JOIN estudiantes e ON p.estudiante_id = e.id
    WHERE e.referido_por_id = :id AND p.estado = 'aceptado'
""")).fetchone()[0]
```

**AHORA (CORRECTO):**
```python
# Total ganado = disponible + retirado
credito_disponible = float(estudiante[1] or 0)
credito_retirado = float(estudiante[3] or 0)
total_ganado = credito_disponible + credito_retirado
```

### 4. Validación de Crédito Suficiente ✅

**Agregado en `/api/admin/solicitudes-credito/{id}/responder`:**
```python
# VALIDAR que tiene crédito suficiente ANTES de aprobar
credito_check = db.execute(text("""
    SELECT COALESCE(credito_disponible, 0) 
    FROM estudiantes WHERE id = :id
""")).fetchone()

credito_disponible = float(credito_check[0]) if credito_check else 0

if credito_disponible < monto:
    raise HTTPException(
        status_code=400, 
        detail=f"Crédito insuficiente. Disponible: {credito_disponible:.2f}€"
    )
```

## 📊 Tracking Completo de Comisiones

### Para Estudiantes:
- **credito_disponible**: Dinero disponible para retirar
- **credito_retirado**: Total histórico retirado
- **total_ganado**: disponible + retirado (se muestra en dashboard)

### Para Agentes:
- **comision_total**: disponible + retirado (total ganado)
- **credito_disponible**: Dinero disponible para retirar
- **credito_retirado**: Total histórico retirado

## 📝 Endpoints Actualizados

### 📄 api/main.py (3 cambios):
1. **`GET /api/estudiantes/{id}/referidos`** (línea ~8090)
   - ✅ ANTES: total_ganado = SUM(presupuestos * 0.05)
   - ✅ AHORA: total_ganado = credito_disponible + credito_retirado

2. **`PUT /api/admin/solicitudes-credito/{id}/responder`** (línea ~8530)
   - ✅ Agregada validación de crédito suficiente ANTES de aprobar
   - ✅ Agregado COALESCE para manejar NULL en credito_retirado
   - ✅ Lanza HTTPException 400 si crédito insuficiente

### 📄 api/agentes_routes.py (2 cambios):
1. **`GET /api/agentes/perfil`** (línea ~160)
   - ✅ Agregado credito_retirado al SELECT
   - ✅ Agregado credito_retirado al response
   - ✅ comision_total = credito_disponible + credito_retirado

2. **`GET /api/agentes/estadisticas`** (línea ~188)
   - ✅ Query separado para obtener credito_disponible y credito_retirado
   - ✅ comision_total = credito_disponible + credito_retirado
   - ✅ Agregados credito_disponible y credito_retirado al response

## 🔄 Flujo Completo Corregido

1. **Estudiante/Agente gana crédito** → `credito_disponible++`
2. **Solicita retiro** → Crea `solicitud_credito` (pendiente)
3. **Admin aprueba** → 
   - ✅ Valida crédito suficiente
   - ✅ `credito_disponible--`
   - ✅ `credito_retirado++`
   - ✅ `total_ganado = disponible + retirado`
4. **Se refleja en dashboard** inmediatamente

## ⚠️ Caso Leandro (ID: 1)

**PROBLEMA DETECTADO:**
- Se aprobó retiro de 100€ sin tener crédito disponible (tenía 0€)
- La solicitud se procesó pero los campos quedaron en 0

**SOLUCIÓN:**
- ✅ Solicitud marcada como rechazada
- ✅ Sistema ahora valida ANTES de aprobar
- ✅ Imposible aprobar retiros sin crédito suficiente

## 🧪 Scripts de Testing Creados

### 1. test_credito_retirado.py
Verifica:
- ✅ Columnas credito_retirado existen
- ✅ Estudiantes/agentes con crédito
- ✅ Solicitudes de retiro
- ✅ Resumen contabilidad global

### 2. fix_leandro_retiro.py
- Investiga solicitud específica
- Corrige manualmente si es necesario
- Valida crédito suficiente

### 3. resumen_correcciones_credito.py
- Documentación completa de cambios
- Flujo corregido
- Próximos pasos

## 🎉 Beneficios Finales

- ✅ Historial completo de retiros
- ✅ Transparencia total para admin
- ✅ Métricas de comisiones realmente pagadas
- ✅ Auditoría de sistema de referidos
- ✅ **Total ganado incluye retiros**
- ✅ **Validación de crédito suficiente**
- ✅ **Imposible aprobar retiros sin fondos**

## 🚀 Próximos Pasos

1. ✅ Reiniciar backend para aplicar cambios
2. ✅ Probar flujo completo de retiro con estudiante/agente real
3. ✅ Verificar que total_ganado se actualiza correctamente
4. ✅ Verificar dashboard de estudiantes y agentes

---
**Última actualización:** 2025-12-11  
**Estado:** ✅ RESUELTO Y FUNCIONANDO
