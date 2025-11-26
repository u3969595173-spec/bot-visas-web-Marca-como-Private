# Guía del Flujo Semi-Automatizado

## 🎯 Concepto General

El sistema funciona en **5 pasos clave**:

1. **Estudiante registra TODOS sus datos** de una vez
2. **Bot procesa automáticamente** (cursos, fondos, documentos, alojamiento)
3. **Admin revisa** toda la información en panel de control
4. **Admin aprueba/modifica** según sea necesario
5. **Admin envía manualmente** al estudiante

---

## 📋 Estados del Flujo

Cada estudiante pasa por estos estados:

| Estado | Descripción |
|--------|-------------|
| `registrado` | Estudiante acaba de registrarse |
| `procesado_automaticamente` | Bot terminó de procesar toda la información |
| `pendiente_revision_admin` | Esperando que admin revise |
| `aprobado_admin` | Admin aprobó, listo para enviar |
| `rechazado_admin` | Admin rechazó, requiere correcciones |
| `enviado_estudiante` | Información enviada al estudiante |

---

## 🚀 Uso del Sistema

### 1. Registro del Estudiante

```python
from modules.flujo_principal import FlujoPrincipal

# El estudiante proporciona TODA su información
datos_completos = {
    # Datos personales
    'telegram_id': 123456789,
    'nombre_completo': 'Juan Pérez',
    'numero_pasaporte': 'CB123456',
    'fecha_nacimiento': datetime(1995, 3, 15),
    'edad': 28,
    'nacionalidad': 'Cuba',
    'ciudad_origen': 'La Habana',
    
    # Datos académicos
    'carrera_actual': 'Ingeniero Civil',
    'nivel_educacion': 'universitario',
    'especialidad_interes': 'Ingeniería Civil',
    'nivel_espanol': 'B2',
    
    # Contacto
    'email': 'juan.perez@example.com',
    'telefono': '+53 5 123 4567',
    
    # Preferencias
    'ciudad_preferida': 'Madrid',
    'presupuesto_curso': 10000,
    'presupuesto_alojamiento': 600,
    
    # Fondos
    'fondos_propios': 8000,
    'tiene_patrocinador': True,
    'necesita_alojamiento': True
}

# Ejecutar flujo completo (registro + procesamiento)
resultado = FlujoPrincipal.flujo_semi_automatizado(datos_completos)

print(f"Estudiante ID: {resultado['estudiante_id']}")
print(f"Estado: {resultado['estado']}")
# Estado: procesado_automaticamente
```

### 2. Panel de Revisión del Admin

```python
from modules.panel_revision_admin import PanelRevisionAdmin

# Ver todos los estudiantes pendientes
pendientes = PanelRevisionAdmin.obtener_estudiantes_pendientes_revision()

print(f"Estudiantes pendientes: {len(pendientes)}")

# Ver panel completo de un estudiante
estudiante_id = 1
panel = PanelRevisionAdmin.ver_panel_estudiante(estudiante_id)

# El panel contiene:
# - Datos personales del estudiante
# - Cursos sugeridos automáticamente
# - Checklist de documentos
# - Verificación de fondos
# - Opciones de alojamiento
# - Resumen general

print(f"Cursos encontrados: {panel['resumen']['cursos_encontrados']}")
print(f"Fondos suficientes: {panel['resumen']['fondos_suficientes']}")
print(f"Documentos completos: {panel['resumen']['documentos_completos']}%")
```

### 3. Aprobar y Preparar Envío

```python
# Admin aprueba la información
aprobacion = PanelRevisionAdmin.aprobar_y_preparar_envio(
    estudiante_id=1,
    admin_id=100,  # ID del admin que aprueba
    curso_seleccionado_id=5,  # Opcional: curso específico
    alojamiento_seleccionado_id=3,  # Opcional: alojamiento específico
    notas_admin="Revisado y aprobado. Todo en orden.",
    modificaciones={'campo': 'valor'}  # Opcional: cambios realizados
)

if aprobacion['exito']:
    print("✅ Aprobado y listo para enviar")
    # Estado cambia a: aprobado_admin
```

### 4. Envío Manual al Estudiante

```python
# Admin envía la información al estudiante
envio = PanelRevisionAdmin.enviar_informacion_manual(
    estudiante_id=1,
    admin_id=100,
    canales=['telegram', 'email'],
    mensaje_personalizado="""
Hola Juan,

Hemos revisado tu solicitud personalmente y todo está en orden.
Aquí está tu plan completo para estudiar en España.

Saludos,
Tu asesor educativo
    """
)

if envio['exito']:
    print(f"✅ Enviado por: {envio['canales_enviados']}")
    print(f"Fecha: {envio['fecha_envio']}")
    # Estado cambia a: enviado_estudiante
```

### 5. Rechazar y Solicitar Correcciones

```python
# Si admin encuentra problemas
rechazo = PanelRevisionAdmin.rechazar_y_solicitar_revision(
    estudiante_id=1,
    admin_id=100,
    motivo="Fondos insuficientes y documentos incompletos",
    acciones_requeridas=[
        "Conseguir patrocinador adicional o incrementar fondos",
        "Completar documentos pendientes",
        "Verificar fechas de pasaporte"
    ]
)

# Estado cambia a: rechazado_admin
# Se crea alerta para que otro admin revise manualmente
```

---

## 📊 Estadísticas y Monitoreo

```python
# Ver estadísticas generales
stats = PanelRevisionAdmin.estadisticas_revision()

print(f"""
Pendientes de revisión: {stats['pendientes_revision']}
Aprobados (pendiente envío): {stats['aprobados_pendiente_envio']}
Enviados: {stats['enviados_estudiante']}
Rechazados: {stats['rechazados']}
""")
```

---

## 🔄 Comparación: Antes vs Ahora

### ❌ Flujo Anterior (Completamente Automático)

```
Estudiante registra → Bot procesa → Bot envía directamente ⚡
```

**Problema:** Sin revisión humana, posibles errores automáticos

### ✅ Flujo Nuevo (Semi-Automatizado)

```
Estudiante registra → Bot procesa → Admin revisa → Admin envía ✋
```

**Ventajas:**
- Bot hace el trabajo pesado (búsquedas, cálculos, etc.)
- Admin valida y personaliza antes de enviar
- Control total sobre la comunicación
- Estudiante recibe información verificada

---

## 📁 Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `modules/flujo_principal.py` | Flujo semi-automatizado principal |
| `modules/panel_revision_admin.py` | Panel de control para admins |
| `modules/estudiantes.py` | Modelo actualizado con estados de revisión |
| `ejemplo_flujo_semi_automatizado.py` | Ejemplo completo interactivo |

---

## 🎯 Ejemplo de Uso Completo

Ver archivo: `ejemplo_flujo_semi_automatizado.py`

Ejecutar:
```bash
python ejemplo_flujo_semi_automatizado.py
```

Este ejemplo muestra:
1. Registro completo del estudiante
2. Procesamiento automático del bot
3. Revisión en panel de admin
4. Aprobación y modificaciones
5. Envío manual al estudiante

---

## 🔧 Configuración

### Estados en Base de Datos

Agregar a tu base de datos el nuevo campo en la tabla `estudiantes`:

```sql
ALTER TABLE estudiantes ADD COLUMN estado_procesamiento VARCHAR(50) DEFAULT 'registrado';
ALTER TABLE estudiantes ADD COLUMN fecha_procesamiento_automatico DATETIME;
ALTER TABLE estudiantes ADD COLUMN fecha_revision_admin DATETIME;
ALTER TABLE estudiantes ADD COLUMN admin_revisor_id INTEGER;
ALTER TABLE estudiantes ADD COLUMN notas_admin TEXT;
ALTER TABLE estudiantes ADD COLUMN modificaciones_admin JSON;
```

O simplemente ejecuta `init_db()` para crear las tablas actualizadas.

---

## 💡 Buenas Prácticas

1. **Registrar TODO de una vez**: Asegúrate que el estudiante proporcione toda la información necesaria
2. **Revisar diariamente**: Admin debe revisar estudiantes pendientes al menos 1 vez al día
3. **Personalizar mensajes**: Siempre agregar mensaje personalizado del admin al enviar
4. **Documentar cambios**: Usar `notas_admin` para documentar decisiones
5. **Monitorear estadísticas**: Revisar stats para identificar cuellos de botella

---

## 🚨 Manejo de Errores

```python
resultado = FlujoPrincipal.flujo_semi_automatizado(datos)

if not resultado['exito']:
    print(f"Error: {resultado['error']}")
    # Manejar error apropiadamente
else:
    # Procesar exitosamente
    estudiante_id = resultado['estudiante_id']
```

---

## 📞 Flujo de Notificaciones

1. **Registro**: Estudiante recibe confirmación simple
2. **Procesamiento**: Admin recibe alerta de nuevo caso
3. **Aprobación**: Admin recibe confirmación
4. **Envío**: Estudiante recibe paquete completo personalizado

---

## ✅ Checklist de Implementación

- [x] Agregar estados de revisión a modelo Estudiante
- [x] Crear módulo panel_revision_admin.py
- [x] Actualizar flujo_principal.py
- [x] Crear funciones de aprobación/rechazo
- [x] Implementar envío manual
- [x] Crear documentación
- [x] Crear ejemplo interactivo

---

¡Sistema listo para usar! 🎉
