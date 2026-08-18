# ✅ VERIFICACIÓN DE BOTONES - ADMIN & INVERSOR

## 🔐 ADMIN DASHBOARD

### TAB: APORTACIONES
- [ ] **✓ Validar** → `updateAportacionStatus(id, 'Activa')` → PUT /api/aportaciones/{id}
- [ ] **✗ Rechazar** → `updateAportacionStatus(id, 'Rechazada')` → PUT /api/aportaciones/{id}
- [ ] **⏱ Solicitar información** → `updateAportacionStatus(id, 'Información solicitada')` → PUT /api/aportaciones/{id}
- [ ] **Descargar justificante** → Link a archivo (si existe)

### TAB: RETIROS
- [ ] **Validar/Rechazar retiros** → RetirosCreditoPanel component

### TAB: USUARIOS
- [ ] **Ver inversores pendientes**
- [ ] **✓ Aprobar inversor** → updateSolicitud(id, 'Validada') 
- [ ] **✗ Rechazar inversor** → updateSolicitud(id, 'Rechazada')

### TAB: OPERACIONES
- [ ] **Mostrar data de aportaciones/retiros**

### TAB: SOLICITUDES
- [ ] **✓ Validar solicitud** → updateSolicitud(id, 'Validada')
- [ ] **✗ Rechazar solicitud** → updateSolicitud(id, 'Rechazada')

### TAB: CHAT
- [ ] **Enviar respuesta al inversor** → POST /api/comunidad/mensajes
- [ ] **Ver mensajes en tiempo real** → GET /api/comunidad/mensajes (polling)

### TAB: RENTABILIDAD
- [ ] **💰 Pagar rentabilidad semanal** → pagarRentabilidadSemanal()

### TAB: COMISIONES
- [ ] **💰 Pagar comisiones referidos** → pagarComisionesReferidos()

### TAB: CONFIGURACIÓN
- [ ] **💾 Guardar cambios** → PUT /api/admin/config (minimos)
- [ ] **Editar minimos EUR/CUP/MLC**
- [ ] **Editar cuentas bancarias**

### HEADER
- [ ] **🚪 Cerrar sesión** → handleLogout()

---

## 💼 INVERSOR DASHBOARD

### TAB: PORTAFOLIO
- [ ] **Mostrar aportaciones** → GET /api/aportaciones (polling)
- [ ] **Mostrar retiros** → GET /api/retiros (polling)
- [ ] **Mostrar capital disponible**

### TAB: HACER INVERSIÓN
- [ ] **💱 Seleccionar moneda** (EUR/CUP/MLC)
- [ ] **📝 Ingreso de monto**
- [ ] **📤 Crear solicitud de inversión** → POST /api/solicitudes-inversion
- [ ] **📎 Subir justificante**

### TAB: RETIRAR
- [ ] **💰 Ingreso de monto retiro**
- [ ] **📝 Notas (opcional)**
- [ ] **📤 Solicitar retiro** → POST /api/retiros

### TAB: MIS SOLICITUDES
- [ ] **Ver todas mis solicitudes de inversión**
- [ ] **Ver estado de cada solicitud**
- [ ] **Descargar justificantes**

### TAB: COMUNIDAD
- [ ] **💬 Ver mensajes públicos**
- [ ] **✍️ Escribir mensaje** → POST /api/comunidad/mensajes
- [ ] **Actualización en tiempo real** (polling 3-5s)

### TAB: PERFIL
- [ ] **Ver datos personales**

### HEADER
- [ ] **🚪 Cerrar sesión** → handleLogout()

---

## 🔌 ENDPOINTS VERIFICADOS

✅ POST   /api/aportaciones                  → Crear aportación
✅ GET    /api/aportaciones                  → Listar aportaciones
✅ PUT    /api/aportaciones/{id}             → Actualizar estado
✅ POST   /api/retiros                       → Crear retiro
✅ GET    /api/retiros                       → Listar retiros
✅ PUT    /api/retiros/{id}                  → Actualizar estado
✅ GET    /api/inversores/pendientes         → Ver inversores sin validar
✅ GET    /api/inversores/validados          → Ver inversores aprobados
✅ PUT    /api/inversores/{id}/estado        → Validar/Rechazar inversor
✅ POST   /api/solicitudes-inversion         → Crear solicitud
✅ GET    /api/comunidad/mensajes            → Ver mensajes
✅ POST   /api/comunidad/mensajes            → Enviar mensaje
✅ GET    /api/admin/config                  → Obtener config
✅ PUT    /api/admin/config                  → Guardar config
✅ GET    /api/admin/cuentas                 → Listar cuentas
✅ POST   /api/admin/cuentas                 → Crear cuenta
✅ PUT    /api/admin/cuentas/{id}            → Actualizar cuenta

---

## ⚠️ BOTONES A VERIFICAR EN EJECUCIÓN

Algunos botones son funciones legacy que podrían necesitar revisión:
- [ ] pagarRentabilidadSemanal() - ¿API o localStorage?
- [ ] pagarComisionesReferidos() - ¿API o localStorage?
- [ ] RetirosCreditoPanel - ¿Conectado a API?

