# Script de inicio del Frontend
# Ejecuta este script para arrancar el frontend React

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   BOT VISAS ESTUDIO - FRONTEND APP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "frontend\package.json")) {
    Write-Host "[ERROR] No se encuentra frontend\package.json" -ForegroundColor Red
    Write-Host "Ejecuta este script desde la carpeta raíz del proyecto" -ForegroundColor Yellow
    pause
    exit 1
}

# Cambiar al directorio frontend
Set-Location frontend

# Verificar que node_modules existe
if (-not (Test-Path "node_modules")) {
    Write-Host "[INFO] Instalando dependencias (primera vez)..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

Write-Host "[INFO] Iniciando servidor frontend..." -ForegroundColor Yellow
Write-Host "URL: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona CTRL+C para detener el servidor" -ForegroundColor Gray
Write-Host ""

# Iniciar servidor
npm run dev
