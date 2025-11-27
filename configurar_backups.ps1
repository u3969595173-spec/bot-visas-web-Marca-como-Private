# Script de PowerShell para Configurar Backups Automáticos
# Bot Visas Estudio - Sistema de Backups

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "  CONFIGURADOR DE BACKUPS AUTOMÁTICOS - BOT VISAS ESTUDIO" -ForegroundColor White
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del proyecto
$ProjectPath = $PSScriptRoot
$PythonScript = Join-Path $ProjectPath "backup_database.py"

# Verificar que existe el script
if (-not (Test-Path $PythonScript)) {
    Write-Host "ERROR: No se encontró backup_database.py" -ForegroundColor Red
    exit 1
}

Write-Host "Ruta del proyecto: $ProjectPath" -ForegroundColor Yellow
Write-Host ""

# Menú de frecuencia
Write-Host "Selecciona la frecuencia de backups:" -ForegroundColor Green
Write-Host "1. Diario (a las 02:00 AM)"
Write-Host "2. Cada 12 horas (02:00 AM y 02:00 PM)"
Write-Host "3. Cada 6 horas"
Write-Host "4. Semanal (Domingos a las 02:00 AM)"
Write-Host "0. Cancelar"
Write-Host ""

$opcion = Read-Host "Ingresa tu opción"

switch ($opcion) {
    "1" {
        $frecuencia = "Diario"
        $trigger = New-ScheduledTaskTrigger -Daily -At "02:00AM"
    }
    "2" {
        $frecuencia = "Cada 12 horas"
        $trigger = @(
            New-ScheduledTaskTrigger -Daily -At "02:00AM"
            New-ScheduledTaskTrigger -Daily -At "02:00PM"
        )
    }
    "3" {
        $frecuencia = "Cada 6 horas"
        $trigger = @(
            New-ScheduledTaskTrigger -Daily -At "00:00AM"
            New-ScheduledTaskTrigger -Daily -At "06:00AM"
            New-ScheduledTaskTrigger -Daily -At "12:00PM"
            New-ScheduledTaskTrigger -Daily -At "06:00PM"
        )
    }
    "4" {
        $frecuencia = "Semanal (Domingos)"
        $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "02:00AM"
    }
    "0" {
        Write-Host "Configuración cancelada" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "Opción inválida" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Configurando tarea programada: Backup $frecuencia" -ForegroundColor Cyan
Write-Host ""

# Configurar acción
$action = New-ScheduledTaskAction -Execute "python" -Argument "`"$PythonScript`"" -WorkingDirectory $ProjectPath

# Configurar settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Crear tarea programada
$taskName = "BotVisasEstudio_Backup_Database"

try {
    # Verificar si ya existe
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    
    if ($existingTask) {
        Write-Host "Ya existe una tarea con este nombre. Eliminando..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }
    
    # Registrar nueva tarea
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Backup automático de base de datos para Bot Visas Estudio ($frecuencia)" `
        -Force
    
    Write-Host ""
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 79) -ForegroundColor Green
    Write-Host "  TAREA PROGRAMADA CREADA EXITOSAMENTE" -ForegroundColor White
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 79) -ForegroundColor Green
    Write-Host ""
    Write-Host "Nombre de la tarea: $taskName" -ForegroundColor Cyan
    Write-Host "Frecuencia: $frecuencia" -ForegroundColor Cyan
    Write-Host "Script: $PythonScript" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Para ver la tarea:" -ForegroundColor Yellow
    Write-Host "  taskschd.msc" -ForegroundColor White
    Write-Host ""
    Write-Host "Para ejecutar manualmente:" -ForegroundColor Yellow
    Write-Host "  python backup_database.py" -ForegroundColor White
    Write-Host ""
    Write-Host "Para eliminar la tarea:" -ForegroundColor Yellow
    Write-Host "  Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "ERROR: No se pudo crear la tarea programada" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "NOTA: Este script requiere permisos de administrador" -ForegroundColor Yellow
    Write-Host "Ejecuta PowerShell como Administrador e intenta nuevamente" -ForegroundColor Yellow
    exit 1
}
