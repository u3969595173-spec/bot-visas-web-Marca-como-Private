# Script de inicio del Backend
# Ejecuta este script para arrancar el servidor

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   BOT VISAS ESTUDIO - BACKEND SERVER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurar encoding UTF-8 para evitar errores de caracteres
$env:PYTHONIOENCODING='utf-8'

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "api\main.py")) {
    Write-Host "[ERROR] No se encuentra api\main.py" -ForegroundColor Red
    Write-Host "Ejecuta este script desde la carpeta raíz del proyecto" -ForegroundColor Yellow
    pause
    exit 1
}

# Verificar configuración de email
Write-Host "[INFO] Verificando configuración de email..." -ForegroundColor Yellow
$envContent = Get-Content .env -Raw
if ($envContent -match "SMTP_USER=your-email@gmail.com") {
    Write-Host ""
    Write-Host "[ADVERTENCIA] Email NO configurado" -ForegroundColor Red
    Write-Host "Los emails NO se enviarán hasta que configures:" -ForegroundColor Yellow
    Write-Host "  1. SMTP_USER en el archivo .env" -ForegroundColor Yellow
    Write-Host "  2. SMTP_PASSWORD en el archivo .env" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Lee CONFIGURAR_EMAIL.md para instrucciones" -ForegroundColor Cyan
    Write-Host ""
    $continue = Read-Host "¿Continuar sin configurar email? (S/N)"
    if ($continue -ne "S" -and $continue -ne "s") {
        Write-Host "Configura el email y vuelve a ejecutar este script" -ForegroundColor Yellow
        pause
        exit 0
    }
} else {
    Write-Host "[OK] Configuración de email detectada" -ForegroundColor Green
}

Write-Host ""
Write-Host "[INFO] Iniciando servidor backend..." -ForegroundColor Yellow
Write-Host "URL: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona CTRL+C para detener el servidor" -ForegroundColor Gray
Write-Host ""

# Iniciar servidor
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
