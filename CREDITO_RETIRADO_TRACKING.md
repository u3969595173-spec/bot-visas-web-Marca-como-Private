# Sistema de Tracking de Crédito Retirado

## 🎯 Problema Resuelto
Cuando el admin aprobaba un retiro, se descontaba del `credito_disponible` pero no se registraba en ninguna parte el historial de dinero ganado/retirado.

## ✅ Solución Implementada

### 1. Columnas Agregadas
- **estudiantes.credito_retirado** (DECIMAL 10,2, default 0.00)
- **agentes.credito_retirado** (DECIMAL 10,2, default 0.00)

### 2. Lógica de Retiro Actualizada
Cuando admin aprueba un retiro:
```sql
-- ANTES (solo descontaba)
UPDATE estudiantes 
SET credito_disponible = credito_disponible - monto
WHERE id = :id

-- AHORA (descuenta Y registra)
UPDATE estudiantes 
SET credito_disponible = credito_disponible - monto,
    credito_retirado = credito_retirado + monto
WHERE id = :id
```

### 3. Visualización en Admin Panel
Se agregó columna **"Crédito Retirado"** en:
- ✅ Tab "👤 Agentes"
- ✅ Tab "💰 Referidos"

## 📊 Tracking Completo de Comisiones

### Para Estudiantes:
- **credito_disponible**: Dinero disponible para retirar
- **credito_retirado**: Total histórico retirado

### Para Agentes:
- **comision_total**: Total ganado (acumulado histórico)
- **credito_disponible**: Dinero disponible para retirar
- **credito_retirado**: Total histórico retirado

## 🔧 Migración Requerida

**IMPORTANTE:** Ejecutar en producción:
```bash
python add_credito_retirado.py
```

Este script agrega las columnas `credito_retirado` a ambas tablas con valor inicial 0.00.

## 📝 Endpoints Actualizados

### Backend (api/main.py):
1. **admin_responder_solicitud_credito** - Suma a credito_retirado al aprobar
2. **admin_obtener_referidos** - Incluye credito_retirado en response
3. **admin_obtener_estadisticas_agentes** - Incluye credito_retirado

### Frontend (DashboardAdminExpandido.jsx):
- Columna "Crédito Retirado" agregada a tablas de Agentes y Referidos
- Color: #6366f1 (índigo)

## 🎉 Beneficios
- ✅ Historial completo de retiros
- ✅ Transparencia total para admin
- ✅ Métricas de comisiones realmente pagadas
- ✅ Auditoría de sistema de referidos
