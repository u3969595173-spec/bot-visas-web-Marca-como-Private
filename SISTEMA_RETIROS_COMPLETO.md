# 🎯 Sistema de Retiros - Documentación Completa

## 📋 Resumen del Sistema

Se ha implementado un sistema completo de gestión de retiros que permite a **estudiantes** y **agentes** solicitar retiros de su crédito disponible, y al **administrador** aprobar o rechazar estas solicitudes desde un panel dedicado.

---

## 🔧 Componentes Implementados

### 1. **Backend (API)**

#### Tabla: `solicitudes_credito`
- **Columnas clave**:
  - `beneficiario_tipo`: 'estudiante' o 'agente'
  - `beneficiario_id`: ID del estudiante o agente
  - `tipo`: 'retiro' o 'descuento'
  - `monto`: Cantidad a retirar
  - `estado`: 'pendiente', 'aprobada', 'rechazada'
  - `estudiante_id`: (nullable) - ID del estudiante si aplica

#### Endpoints Modificados:

**GET `/api/admin/solicitudes-credito`**
- Retorna TODAS las solicitudes (estudiantes + agentes)
- Hace LEFT JOIN con tablas `estudiantes` y `agentes`
- Respuesta incluye:
  ```json
  {
    "id": 1,
    "beneficiario_tipo": "agente",
    "beneficiario_id": 5,
    "tipo": "retiro",
    "monto": 150.00,
    "estado": "pendiente",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "credito_disponible": 500.00,
    "fecha_solicitud": "2024-01-15T10:30:00"
  }
  ```

**PUT `/api/admin/solicitudes-credito/{solicitud_id}/responder`**
- Maneja aprobación/rechazo para AMBOS tipos
- Si `beneficiario_tipo === 'agente'`:
  - Descuenta de `agentes.credito_disponible`
- Si `beneficiario_tipo === 'estudiante'`:
  - Descuenta de `estudiantes.credito_disponible`
- Actualiza estado de solicitud
- Registra fecha de respuesta

#### Endpoints Existentes:

**POST `/api/agentes/solicitar-retiro`** (agentes)
- Crea solicitud con `beneficiario_tipo='agente'`
- Valida que tenga crédito disponible
- Requiere autenticación de agente

**POST `/api/referidos/solicitar-uso`** (estudiantes)
- Crea solicitud con `beneficiario_tipo='estudiante'`
- Permite tipo 'retiro' o 'descuento'
- Requiere autenticación de estudiante

---

### 2. **Frontend (React)**

#### Nuevo Tab: "💰 Retiros"
- **Ubicación**: Dashboard de Admin (`DashboardAdminExpandido.jsx`)
- **Posición**: Entre "💎 Referidos" y "📊 Reportes"
- **Color**: Verde degradado (#10b981 → #059669)

#### Tabla de Retiros
Muestra:
- **Usuario**: Nombre y email
- **Tipo**: Badge indicando si es Agente (👤) o Estudiante (🎓)
- **Monto**: Cantidad solicitada en rojo
- **Saldo Actual**: Crédito disponible antes del retiro
- **Estado**: Pendiente ⏳ / Aprobada ✅ / Rechazada ❌
- **Fecha**: Fecha y hora de solicitud
- **Acciones**: Botones para aprobar o rechazar (solo si pendiente)

#### Funcionalidad
- Al cargar el tab, hace fetch de todas las solicitudes
- Botón "✅ Aprobar":
  - Confirma con el usuario
  - Descuenta automáticamente del crédito disponible
  - Actualiza estado a 'aprobada'
  - Recarga la tabla
- Botón "❌ Rechazar":
  - Confirma con el usuario
  - Actualiza estado a 'rechazada'
  - NO descuenta crédito
  - Recarga la tabla

---

## 🔄 Flujo Completo

### Para Estudiantes:
1. Estudiante acumula comisión (5% por pago)
2. Va a "Crédito Disponible" en su dashboard
3. Solicita retiro ingresando monto
4. Solicitud queda en estado 'pendiente'
5. Admin la ve en tab "Retiros"
6. Admin aprueba → Se descuenta de `estudiantes.credito_disponible`

### Para Agentes:
1. Agente acumula comisión (10% por pago)
2. Va a su dashboard de agente
3. Solicita retiro ingresando monto
4. Solicitud queda en estado 'pendiente'
5. Admin la ve en tab "Retiros"
6. Admin aprueba → Se descuenta de `agentes.credito_disponible`

---

## 📊 Sistema de Comisiones

### Estudiantes: **5% por pago**
- Se calcula en endpoint: `/api/admin/tesoro/{id}/marcar-pago-individual`
- Se agrega a `estudiantes.credito_disponible`
- Trigger: Cuando admin marca pago como realizado

### Agentes: **10% por pago**
- Se calcula en el mismo endpoint
- Se agrega a `agentes.comision_total` y `agentes.credito_disponible`
- Trigger: Cuando admin marca pago como realizado

---

## 🎨 Interfaz de Usuario

### Tab "Retiros" en Admin
```
💰 Gestión de Retiros
Solicitudes de retiro de estudiantes y agentes

┌─────────────────────────────────────────────────────────────────────┐
│ Usuario        │ Tipo       │ Monto    │ Saldo    │ Estado   │ ... │
├─────────────────────────────────────────────────────────────────────┤
│ Juan Pérez     │ 👤 Agente  │ 150.00€  │ 500.00€  │ ⏳ Pend. │ ✅❌│
│ juan@mail.com  │            │          │          │          │     │
├─────────────────────────────────────────────────────────────────────┤
│ María López    │ 🎓 Est.    │ 50.00€   │ 200.00€  │ ⏳ Pend. │ ✅❌│
│ maria@mail.com │            │          │          │          │     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing

### Probar el Sistema:
1. **Crear solicitud de estudiante**:
   ```bash
   curl -X POST http://localhost:8000/api/referidos/solicitar-uso \
     -H "Authorization: Bearer TOKEN_ESTUDIANTE" \
     -H "Content-Type: application/json" \
     -d '{"tipo": "retiro", "monto": 50.00}'
   ```

2. **Crear solicitud de agente**:
   ```bash
   curl -X POST http://localhost:8000/api/agentes/solicitar-retiro \
     -H "Authorization: Bearer TOKEN_AGENTE" \
     -H "Content-Type: application/json" \
     -d '{"monto": 150.00}'
   ```

3. **Ver solicitudes (Admin)**:
   ```bash
   curl -X GET http://localhost:8000/api/admin/solicitudes-credito \
     -H "Authorization: Bearer TOKEN_ADMIN"
   ```

4. **Aprobar solicitud**:
   ```bash
   curl -X PUT http://localhost:8000/api/admin/solicitudes-credito/1/responder \
     -H "Authorization: Bearer TOKEN_ADMIN" \
     -H "Content-Type: application/json" \
     -d '{"accion": "aprobar"}'
   ```

---

## 🚀 Estado del Proyecto

### ✅ Completado:
- [x] Tabla `solicitudes_credito` con soporte dual (estudiantes + agentes)
- [x] Endpoint GET modificado para retornar ambos tipos
- [x] Endpoint PUT modificado para aprobar/rechazar ambos tipos
- [x] Lógica de descuento automático según `beneficiario_tipo`
- [x] Tab "Retiros" en frontend de admin
- [x] Tabla visual con todos los campos necesarios
- [x] Botones de aprobar/rechazar con confirmación
- [x] Badges de color para diferenciar tipos
- [x] Recarga automática después de acciones

### 🎯 Próximos Pasos (Opcional):
- [ ] Historial de retiros aprobados/rechazados
- [ ] Notificaciones push cuando admin responde
- [ ] Export de reporte de retiros en Excel
- [ ] Límite de retiros por mes
- [ ] Verificación bancaria integrada

---

## 📝 Notas Importantes

1. **Seguridad**: Todas las operaciones requieren autenticación JWT
2. **Validación**: Backend valida que el crédito disponible sea suficiente
3. **Atomicidad**: Descuentos se hacen en transacción de base de datos
4. **Auditoría**: Todas las acciones quedan registradas con fecha
5. **UX**: Confirmaciones antes de aprobar/rechazar para evitar errores

---

## 🐛 Solución de Problemas

### Problema: "No aparecen solicitudes en el tab"
**Solución**: Verificar que:
- Backend esté corriendo en puerto 8000
- Token de admin sea válido
- Existan solicitudes en base de datos

### Problema: "Error al aprobar retiro"
**Solución**: Verificar que:
- El crédito disponible sea >= monto solicitado
- La solicitud esté en estado 'pendiente'
- El `beneficiario_id` sea válido

### Problema: "El crédito no se descuenta"
**Solución**: Revisar logs del backend
- Verificar que la transacción SQL se complete
- Confirmar que `beneficiario_tipo` esté correctamente asignado

---

## 📞 Contacto y Soporte

Si encuentras algún problema o necesitas ayuda:
1. Revisa los logs del backend: `python -m uvicorn api.main:app --reload`
2. Revisa la consola del navegador (F12)
3. Verifica la base de datos directamente si es necesario

---

**Sistema implementado exitosamente ✅**
Fecha: 2024
Versión: 1.0
