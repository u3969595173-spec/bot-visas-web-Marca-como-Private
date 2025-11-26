# 🎓 Bot Agencia Educativa - Cubanos a España

## Sistema Completo de Gestión de Visas de Estudiante

Bot inteligente especializado en ayudar a estudiantes cubanos (y de otros países) a estudiar en España, gestionando todo el proceso desde el registro hasta la aprobación de visa.

---

## 📦 Módulos Implementados

### ✅ 1. **Gestión de Cursos y Escuelas** (`modules/cursos.py`)

**Funcionalidades:**
- ✅ Conexión con APIs de universidades/escuelas
- ✅ Web scraping legal de páginas públicas
- ✅ Filtrado avanzado de cursos (especialidad, duración, ciudad, idioma, precio)
- ✅ Alertas automáticas de nuevos cursos
- ✅ Búsqueda de texto completo
- ✅ Sincronización automática de cursos (cron job)
- ✅ Base de datos de escuelas predefinidas (Complutense, Barcelona, UAM, etc.)

**Uso:**
```python
from modules.cursos import GestorCursos

# Buscar cursos
cursos = GestorCursos.filtrar_cursos(
    especialidad='informatica',
    ciudad='Madrid',
    precio_max=8000
)

# Alertas de nuevos cursos
alertas = GestorCursos.alertar_nuevos_cursos()
```

---

### ✅ 2. **Gestión de Estudiantes** (`modules/estudiantes.py`)

**Funcionalidades:**
- ✅ Registro completo de estudiantes (datos personales, académicos, contacto)
- ✅ Asignación inteligente de cursos según perfil
- ✅ Checklist personalizado de documentos (obligatorios + recomendados)
- ✅ Seguimiento de documentos completados/pendientes
- ✅ Calendario de eventos importantes
- ✅ Recordatorios automáticos (citas, documentos, pagos)
- ✅ Estados de visa tracking

**Uso:**
```python
from modules.estudiantes import GestorEstudiantes

# Registrar estudiante
estudiante = GestorEstudiantes.registrar_estudiante({
    'telegram_id': 123456,
    'nombre_completo': 'Juan Pérez',
    'numero_pasaporte': 'A1234567',
    'especialidad_interes': 'Ingeniería Informática',
    'nivel_espanol': 'B2'
})

# Asignar curso
GestorEstudiantes.asignar_curso(estudiante.id, curso_id=5)

# Checklist de documentos
checklist = GestorEstudiantes.checklist_documentos(estudiante.id)
```

---

### ✅ 3. **Gestión de Fondos Económicos** (`modules/fondos.py`)

**Funcionalidades:**
- ✅ Verificación automática de fondos (propios, patrocinador, transferencias)
- ✅ Cálculo de fondos mínimos requeridos
- ✅ Evaluación de suficiencia económica
- ✅ Registro de patrocinadores
- ✅ **Generación automática de carta de patrocinio en PDF** ⭐
- ✅ Registro de transferencias internacionales
- ✅ Verificación de patrocinadores

**Uso:**
```python
from modules.fondos import GestorFondos

# Verificar fondos
verificacion = GestorFondos.verificar_fondos(estudiante_id=1)
print(f"Estado: {verificacion['estado']}")
print(f"Cobertura: {verificacion['porcentaje_cobertura']}%")

# Generar carta de patrocinio
pdf_bytes = GestorFondos.generar_carta_patrocinio(
    patrocinador_id=1,
    estudiante_id=1
)
# Guardar PDF
with open('carta_patrocinio.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

---

### ✅ 4. **Sistema de Alertas y Notificaciones** (`modules/notificaciones.py`)

**Funcionalidades:**
- ✅ Notificaciones multicanal (Telegram, Email, WhatsApp*)
- ✅ Alertas internas para administradores
- ✅ Recordatorios automáticos programados
- ✅ Alertas de eventos próximos (citas, documentos, pagos)
- ✅ Sistema de prioridades (baja, normal, alta, urgente)
- ✅ Tarea diaria automática de alertas

*WhatsApp requiere configuración de WhatsApp Business API

**Uso:**
```python
from modules.notificaciones import SistemaNotificaciones

# Notificar estudiante
SistemaNotificaciones.notificar_estudiante(
    estudiante_id=1,
    mensaje="Tu cita en el consulado es mañana a las 10:00",
    titulo="Recordatorio de cita",
    canales=['telegram', 'email'],
    prioridad='urgente'
)

# Generar alertas internas
alertas = SistemaNotificaciones.alertas_internas()
```

---

### ✅ 5. **Gestión de Alojamiento** (`modules/alojamiento.py`)

**Funcionalidades:**
- ✅ Registro de pisos y habitaciones disponibles
- ✅ Búsqueda avanzada de alojamientos (ciudad, precio, tipo)
- ✅ Asignación de alojamiento a estudiantes
- ✅ Sistema de pagos mensuales de alquiler
- ✅ Alertas automáticas de pagos próximos/vencidos
- ✅ Gestión de contratos y depósitos
- ✅ Tracking de ocupación y disponibilidad

**Uso:**
```python
from modules.alojamiento import GestorAlojamiento

# Buscar alojamientos
alojamientos = GestorAlojamiento.buscar_alojamientos(
    ciudad='Madrid',
    precio_max=500,
    tipo='habitacion_individual'
)

# Asignar alojamiento
asignacion = GestorAlojamiento.asignar_alojamiento(
    estudiante_id=1,
    alojamiento_id=3,
    fecha_inicio=datetime.now(),
    duracion_meses=12
)

# Alertas de pagos
alertas = GestorAlojamiento.alertas_alquiler(dias_anticipacion=7)
```

---

### ✅ 6. **Panel Administrativo y Reportes** (`modules/admin_panel.py`)

**Funcionalidades:**
- ✅ Dashboard completo con métricas en tiempo real
- ✅ Estadísticas de estudiantes por estado, prioridad, especialidad
- ✅ Reporte financiero (ingresos, pagos pendientes, tasa de cobro)
- ✅ Estudiantes que requieren atención urgente
- ✅ Estadísticas por especialidad y tasa de éxito
- ✅ Exportación a JSON
- ✅ Reporte mensual completo

**Uso:**
```python
from modules.admin_panel import PanelAdministrativo

# Dashboard completo
dashboard = PanelAdministrativo.dashboard()
print(f"Total estudiantes: {dashboard['resumen']['total_estudiantes']}")
print(f"Tasa aprobación: {dashboard['resumen']['tasa_aprobacion']}%")

# Estudiantes que requieren atención
atencion = PanelAdministrativo.estudiantes_requieren_atencion()

# Reporte mensual
reporte = PanelAdministrativo.generar_reporte_mensual()
```

---

### ✅ 7. **Flujo Principal de Negocio** (`modules/flujo_principal.py`)

**Funcionalidades:**
- ✅ Flujo completo automatizado de registro a visa
- ✅ Integración de todos los módulos
- ✅ Tareas automáticas programadas (cron jobs)
- ✅ Workflow paso a paso:
  1. Registro de estudiante
  2. Sugerencia y asignación de cursos
  3. Verificación de fondos
  4. Generación de checklist y recordatorios
  5. Coordinación de alojamiento
  6. Generación de reportes

**Uso:**
```python
from modules.flujo_principal import FlujoPrincipal

# Flujo completo automático
resultado = FlujoPrincipal.flujo_completo_estudiante({
    'telegram_id': 123456,
    'nombre_completo': 'María García',
    'numero_pasaporte': 'B9876543',
    'edad': 25,
    'especialidad_interes': 'Medicina',
    'nivel_espanol': 'C1',
    'email': 'maria@example.com'
})
```

---

## 🗄️ Base de Datos

### Tablas implementadas:

1. **users** - Usuarios del bot
2. **visa_applications** - Solicitudes de visa
3. **estudiantes** - Información completa de estudiantes
4. **cursos** - Catálogo de cursos
5. **escuelas** - Universidades y escuelas
6. **documentos_estudiante** - Documentos subidos
7. **eventos_estudiante** - Calendario de eventos
8. **patrocinadores** - Patrocinadores económicos
9. **transferencias_fondos** - Transferencias internacionales
10. **alojamientos** - Pisos y habitaciones
11. **asignaciones_alojamiento** - Asignaciones de estudiantes
12. **pagos_alquiler** - Pagos mensuales
13. **notificaciones** - Historial de notificaciones
14. **alertas_admin** - Alertas para administradores

---

## 🚀 Instalación y Uso

### 1. Instalar dependencias:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configurar variables de entorno:

Copia `.env.example` a `.env` y completa:

```env
TELEGRAM_BOT_TOKEN=tu_token_bot
OPENAI_API_KEY=tu_api_key (opcional, para IA)
DATABASE_URL=sqlite:///visas_bot.db
STRIPE_SECRET_KEY=tu_stripe_key (opcional)
```

### 3. Inicializar base de datos:

```python
from database.models import init_db
init_db()
```

### 4. Cargar escuelas predefinidas:

```python
from modules.cursos import inicializar_escuelas_predefinidas
inicializar_escuelas_predefinidas()
```

### 5. Ejecutar bot:

```powershell
python bot.py
```

---

## 📅 Tareas Automáticas (Cron Jobs)

Configurar estas funciones para ejecutarse automáticamente:

### Diarias:
```python
# Sincronizar cursos de todas las escuelas
from modules.flujo_principal import tarea_diaria_sincronizar_cursos
tarea_diaria_sincronizar_cursos()

# Generar alertas y enviar notificaciones
from modules.flujo_principal import tarea_diaria_alertas
tarea_diaria_alertas()

# Alertas de pagos de alquiler
from modules.flujo_principal import tarea_diaria_alquileres
tarea_diaria_alquileres()
```

### Semanales:
```python
# Reporte semanal para administradores
from modules.flujo_principal import generar_reporte_semanal
generar_reporte_semanal()
```

---

## 📊 Ejemplo de Uso Completo

```python
# 1. REGISTRAR NUEVO ESTUDIANTE
from modules.flujo_principal import FlujoPrincipal

datos = {
    'telegram_id': 123456789,
    'nombre_completo': 'Carlos Rodríguez',
    'numero_pasaporte': 'C1234567',
    'edad': 23,
    'nacionalidad': 'Cuba',
    'ciudad_origen': 'La Habana',
    'carrera_actual': 'Ingeniería',
    'especialidad_interes': 'Inteligencia Artificial',
    'nivel_espanol': 'B2',
    'email': 'carlos@example.com',
    'telefono': '+53 12345678'
}

# Ejecutar flujo completo
resultado = FlujoPrincipal.flujo_completo_estudiante(datos)
print(resultado)

# 2. ASIGNAR CURSO MANUALMENTE
estudiante_id = resultado['estudiante_id']
FlujoPrincipal.sugerir_y_asignar_curso(estudiante_id, curso_id=5)

# 3. REGISTRAR PATROCINADOR
from modules.fondos import GestorFondos

patrocinador = GestorFondos.registrar_patrocinador({
    'nombre_completo': 'José Rodríguez',
    'numero_identificacion': '12345678A',
    'relacion_estudiante': 'padre',
    'pais_residencia': 'España',
    'ciudad_residencia': 'Madrid',
    'email': 'jose@example.com',
    'telefono': '+34 123456789',
    'ocupacion': 'Ingeniero',
    'ingresos_mensuales': 3000,
    'capacidad_patrocinio': 15000
}, estudiante_id=estudiante_id)

# 4. GENERAR CARTA DE PATROCINIO
pdf = GestorFondos.generar_carta_patrocinio(patrocinador.id, estudiante_id)
with open(f'carta_patrocinio_{estudiante_id}.pdf', 'wb') as f:
    f.write(pdf)

# 5. ASIGNAR ALOJAMIENTO
from modules.alojamiento import GestorAlojamiento
from datetime import datetime

alojamiento = GestorAlojamiento.asignar_alojamiento(
    estudiante_id=estudiante_id,
    alojamiento_id=1,
    fecha_inicio=datetime(2026, 1, 15),
    duracion_meses=12
)

# 6. VER DASHBOARD ADMINISTRATIVO
from modules.admin_panel import PanelAdministrativo

dashboard = PanelAdministrativo.dashboard()
print(f"Total estudiantes: {dashboard['resumen']['total_estudiantes']}")
print(f"Visas aprobadas: {dashboard['resumen']['visas_aprobadas']}")
```

---

## 🎯 Características Destacadas

### ⭐ Generación Automática de Documentos
- Carta de patrocinio en PDF con formato oficial
- Checklist personalizado según perfil
- Formularios auto-completados

### ⭐ Sistema Inteligente de Alertas
- Notificaciones multicanal
- Priorización automática
- Recordatorios programados

### ⭐ Panel Administrativo Completo
- Dashboard en tiempo real
- Reportes financieros
- Análisis de éxito por especialidad

### ⭐ Gestión Integral
- Desde registro hasta visa aprobada
- Tracking completo del proceso
- Coordinación de alojamiento

---

## 📈 Roadmap Futuro

### Fase 1 (Actual) ✅
- [x] Todos los módulos base
- [x] Flujo completo integrado
- [x] Sistema de notificaciones
- [x] Panel administrativo

### Fase 2 (Próxima)
- [ ] Validación de documentos con OCR
- [ ] Sistema de pagos con Stripe
- [ ] App móvil (Flutter)
- [ ] Portal web para estudiantes
- [ ] Integración WhatsApp Business API

### Fase 3 (Futuro)
- [ ] Machine Learning para predicción de éxito
- [ ] Chatbot IA para consultas
- [ ] Sistema de referidos
- [ ] Marketplace de servicios

---

## 📝 Licencia

Copyright © 2025. Todos los derechos reservados.

---

## 📧 Soporte

Para preguntas o soporte técnico, contacta al equipo de desarrollo.

**¡Construye el futuro de estudiantes en España! 🎓🇪🇸**
