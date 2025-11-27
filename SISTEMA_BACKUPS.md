# 🗄️ Sistema de Backups Automáticos

## Descripción

Sistema completo de backups automáticos para la base de datos PostgreSQL de Bot Visas Estudio.

## Archivos del Sistema

### 1. `backup_database.py`
Script principal que realiza backups de la base de datos.

**Características:**
- ✅ Backup comprimido formato custom (pg_dump -F c)
- ✅ Nomenclatura con fecha y hora: `backup_{database}_YYYYMMDD_HHMMSS.sql`
- ✅ Limpieza automática de backups antiguos (> 30 días)
- ✅ Notificación por email al admin
- ✅ Logs detallados del proceso

### 2. `restore_database.py`
Script para restaurar la base de datos desde un backup.

**Características:**
- ✅ Lista todos los backups disponibles
- ✅ Selección interactiva
- ✅ Confirmación de seguridad
- ✅ Restauración completa con pg_restore

### 3. `configurar_backups.ps1`
Script de PowerShell para configurar backups automáticos en Windows.

**Características:**
- ✅ Configuración de tarea programada en Windows
- ✅ Múltiples opciones de frecuencia
- ✅ Ejecución automática sin intervención

---

## 📋 Requisitos Previos

### 1. PostgreSQL Client Tools

**Windows:**
```powershell
# Descargar desde: https://www.postgresql.org/download/windows/
# Durante instalación, seleccionar "Command Line Tools"
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql-client
```

**Mac:**
```bash
brew install postgresql
```

### 2. Variables de Entorno

Configurar en `.env`:

```env
DATABASE_URL=postgresql://user:password@host:port/database

# Para notificaciones por email
ADMIN_EMAIL=admin@botvisasestudio.com
EMAIL_FROM=backups@botvisasestudio.com
EMAIL_PASSWORD=your_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

---

## 🚀 Uso Manual

### Crear Backup

```bash
# Ejecutar script de backup
python backup_database.py
```

**Salida esperada:**
```
================================================================================
🗄️  SISTEMA DE BACKUP AUTOMÁTICO - BOT VISAS ESTUDIO
================================================================================

✅ Directorio de backups: C:\BotVisasEstudio\backups
🔄 Iniciando backup de la base de datos: bot_visas_db
📁 Archivo: backup_bot_visas_db_20251127_143022.sql
✅ Backup completado exitosamente
📊 Tamaño: 12.45 MB

🧹 Limpiando backups antiguos (más de 30 días)...
✅ No hay backups antiguos para eliminar

📋 Backups disponibles (3):
--------------------------------------------------------------------------------
1. backup_bot_visas_db_20251127_143022.sql
   📅 Fecha: 2025-11-27 14:30:22 (0 días)
   📊 Tamaño: 12.45 MB

2. backup_bot_visas_db_20251126_020000.sql
   📅 Fecha: 2025-11-26 02:00:00 (1 días)
   📊 Tamaño: 12.20 MB

3. backup_bot_visas_db_20251125_020000.sql
   📅 Fecha: 2025-11-25 02:00:00 (2 días)
   📊 Tamaño: 11.98 MB

📧 Notificación enviada a: admin@botvisasestudio.com

================================================================================
✅ Proceso de backup completado exitosamente
================================================================================
```

### Restaurar Backup

```bash
# Ejecutar script de restauración
python restore_database.py
```

**Proceso interactivo:**
```
================================================================================
🔧 SISTEMA DE RESTAURACIÓN DE BACKUPS - BOT VISAS ESTUDIO
================================================================================

📋 Backups disponibles (3):
================================================================================
1. backup_bot_visas_db_20251127_143022.sql
   📅 Fecha: 2025-11-27 14:30:22 (0 días)
   📊 Tamaño: 12.45 MB

2. backup_bot_visas_db_20251126_020000.sql
   📅 Fecha: 2025-11-26 02:00:00 (1 días)
   📊 Tamaño: 12.20 MB

================================================================================

Selecciona el número del backup a restaurar (0 para cancelar): 1

🔄 Iniciando restauración de backup...
📁 Archivo: backup_bot_visas_db_20251127_143022.sql

================================================================================
⚠️  ADVERTENCIA: Esta operación SOBRESCRIBIRÁ la base de datos actual
================================================================================

¿Estás seguro de continuar? (escribe 'SI' para confirmar): SI

🔄 Restaurando base de datos...
✅ Restauración completada exitosamente

================================================================================
✅ Proceso de restauración completado exitosamente
================================================================================
```

---

## ⏰ Configurar Backups Automáticos (Windows)

### Paso 1: Ejecutar como Administrador

```powershell
# Click derecho en PowerShell -> Ejecutar como Administrador
cd C:\BotVisasEstudio
.\configurar_backups.ps1
```

### Paso 2: Seleccionar Frecuencia

```
Selecciona la frecuencia de backups:
1. Diario (a las 02:00 AM)
2. Cada 12 horas (02:00 AM y 02:00 PM)
3. Cada 6 horas
4. Semanal (Domingos a las 02:00 AM)
0. Cancelar

Ingresa tu opción: 1
```

### Paso 3: Confirmación

```
================================================================================
  TAREA PROGRAMADA CREADA EXITOSAMENTE
================================================================================

Nombre de la tarea: BotVisasEstudio_Backup_Database
Frecuencia: Diario
Script: C:\BotVisasEstudio\backup_database.py

Para ver la tarea:
  taskschd.msc

Para ejecutar manualmente:
  python backup_database.py

Para eliminar la tarea:
  Unregister-ScheduledTask -TaskName 'BotVisasEstudio_Backup_Database' -Confirm:$false
```

---

## 🐧 Configurar Backups Automáticos (Linux/Mac)

### Usando Cron

```bash
# Editar crontab
crontab -e

# Agregar línea para backup diario a las 2 AM
0 2 * * * cd /ruta/a/BotVisasEstudio && /usr/bin/python3 backup_database.py >> /var/log/bot-visas-backup.log 2>&1

# Guardar y salir
```

**Otras frecuencias:**

```bash
# Cada 12 horas (2 AM y 2 PM)
0 2,14 * * * cd /ruta/a/BotVisasEstudio && python3 backup_database.py

# Cada 6 horas
0 */6 * * * cd /ruta/a/BotVisasEstudio && python3 backup_database.py

# Semanal (Domingos a las 2 AM)
0 2 * * 0 cd /ruta/a/BotVisasEstudio && python3 backup_database.py
```

---

## 📁 Estructura de Archivos

```
BotVisasEstudio/
├── backup_database.py          # Script de backup
├── restore_database.py         # Script de restauración
├── configurar_backups.ps1      # Configurador Windows
├── backups/                    # Directorio de backups
│   ├── backup_db_20251127_143022.sql
│   ├── backup_db_20251126_020000.sql
│   └── backup_db_20251125_020000.sql
└── .env                        # Variables de entorno
```

---

## 🔍 Verificar Estado

### Windows (Tarea Programada)

```powershell
# Abrir Task Scheduler
taskschd.msc

# O por PowerShell
Get-ScheduledTask -TaskName "BotVisasEstudio_Backup_Database"

# Ver última ejecución
Get-ScheduledTaskInfo -TaskName "BotVisasEstudio_Backup_Database"
```

### Linux/Mac (Cron)

```bash
# Ver tareas programadas
crontab -l

# Ver logs (si configuraste redirección)
tail -f /var/log/bot-visas-backup.log
```

---

## ⚙️ Configuración Avanzada

### Cambiar Retención de Backups

Editar `backup_database.py`:

```python
BACKUP_RETENTION_DAYS = 30  # Cambiar a días deseados
```

### Cambiar Ubicación de Backups

```python
BACKUP_DIR = Path("backups")  # Cambiar ruta
```

### Deshabilitar Notificaciones Email

Simplemente no configurar `ADMIN_EMAIL` o `EMAIL_PASSWORD` en `.env`.

---

## 🆘 Solución de Problemas

### Error: "pg_dump no encontrado"

**Solución:** Instalar PostgreSQL client tools

**Windows:**
1. Descargar PostgreSQL desde oficial
2. Durante instalación, seleccionar "Command Line Tools"
3. Agregar a PATH: `C:\Program Files\PostgreSQL\15\bin`

**Linux:**
```bash
sudo apt-get install postgresql-client
```

### Error: "DATABASE_URL no configurada"

**Solución:** Verificar archivo `.env`:

```bash
# Ver configuración actual
cat .env | grep DATABASE_URL

# Debe contener algo como:
# DATABASE_URL=postgresql://user:password@host:port/database
```

### Error: "Timeout" en backup/restauración

**Solución:** Aumentar timeout en scripts:

```python
# En backup_database.py o restore_database.py
timeout=600  # Cambiar a 1200 (20 minutos) o más
```

### Backups no se ejecutan automáticamente

**Windows:**
- Verificar que el servicio "Task Scheduler" está corriendo
- Revisar permisos de la tarea programada
- Verificar que Python está en PATH

**Linux:**
- Verificar que cron está corriendo: `sudo service cron status`
- Revisar logs: `grep CRON /var/log/syslog`
- Verificar permisos del script

---

## 📊 Mejores Prácticas

### 1. Frecuencia Recomendada

- **Producción activa:** Cada 12 horas o diario
- **Desarrollo:** Semanal
- **Alta carga de datos:** Cada 6 horas

### 2. Almacenamiento Externo

Considerar copiar backups a:
- ☁️ Google Drive / OneDrive
- 💾 Disco externo
- 🌐 Servidor remoto (rsync, scp)

### 3. Pruebas de Restauración

**Realizar pruebas mensuales:**
```bash
# En entorno de prueba, no producción
python restore_database.py
```

### 4. Monitoreo

- ✅ Verificar emails de notificación
- ✅ Revisar tamaño de backups (detectar anomalías)
- ✅ Verificar espacio en disco

---

## 🔐 Seguridad

### Proteger Backups

```bash
# Permisos solo para usuario actual (Linux/Mac)
chmod 700 backups/
chmod 600 backups/*.sql

# Windows: Usar propiedades de carpeta -> Seguridad
```

### Encriptar Backups (Opcional)

```bash
# Encriptar con GPG
gpg -c backup_db_20251127.sql

# Desencriptar
gpg backup_db_20251127.sql.gpg
```

---

## 📧 Notificaciones por Email

### Configuración Gmail

1. Habilitar "Acceso de aplicaciones menos seguras" o usar contraseña de aplicación
2. Configurar en `.env`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=tu_email@gmail.com
EMAIL_PASSWORD=tu_contraseña_o_app_password
ADMIN_EMAIL=admin@botvisasestudio.com
```

### Email de Éxito

```
Asunto: ✅ Backup Exitoso - bot_visas_db - 2025-11-27 14:30:22

Base de datos: bot_visas_db
Fecha y hora: 2025-11-27 14:30:22
Archivo: backup_bot_visas_db_20251127_143022.sql
Tamaño: 12.45 MB
Ubicación: C:\BotVisasEstudio\backups\backup_bot_visas_db_20251127_143022.sql
```

### Email de Error

```
Asunto: ❌ Backup Fallido - bot_visas_db - 2025-11-27 14:30:22

Base de datos: bot_visas_db
Fecha y hora: 2025-11-27 14:30:22
Error: [detalles del error]

ACCIÓN REQUERIDA: Revisar logs y configuración del sistema de backups.
```

---

## ✅ Checklist de Implementación

- [ ] PostgreSQL client tools instalados
- [ ] Variables de entorno configuradas en `.env`
- [ ] Probado backup manual: `python backup_database.py`
- [ ] Probado restauración: `python restore_database.py` (en ambiente de prueba)
- [ ] Configurado backup automático (Windows/Linux)
- [ ] Verificado recepción de emails de notificación
- [ ] Documentado ubicación y contraseñas de acceso
- [ ] Establecido plan de almacenamiento externo (opcional)
- [ ] Calendario de pruebas de restauración (mensual)

---

## 📞 Soporte

Para problemas o consultas:
- 📧 Email: soporte@botvisasestudio.com
- 📖 Documentación: README.md
- 🐛 Issues: GitHub Issues

---

**Versión:** 1.0  
**Última actualización:** 27 de noviembre de 2025  
**Autor:** Bot Visas Estudio Team
