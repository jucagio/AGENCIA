# ============================================================================
#  Asesor de Imagen AI — Arranque MVP local (Sasha)
#  Doble clic o ejecutar:  powershell -ExecutionPolicy Bypass -File START_MVP.ps1
# ============================================================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $ScriptDir "backend"
$VenvPython = Join-Path $BackendDir "venv\Scripts\python.exe"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Asesor de Imagen AI - MVP Local Backend" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $VenvPython)) {
    Write-Host "[ERROR] No se encontro venv en $BackendDir\venv" -ForegroundColor Red
    Write-Host "        Ejecuta: py -3.12 -m venv backend\venv" -ForegroundColor Yellow
    Write-Host "        Luego:   backend\venv\Scripts\pip install -r backend\requirements.txt" -ForegroundColor Yellow
    Read-Host "Presiona ENTER para cerrar"
    exit 1
}

Set-Location $BackendDir

Write-Host "[1/3] Verificando Python..." -ForegroundColor Green
& $VenvPython --version

Write-Host ""
Write-Host "[2/3] Iniciando servidor en http://127.0.0.1:8000" -ForegroundColor Green
Write-Host ""
Write-Host "  -> Documentacion interactiva:  http://127.0.0.1:8000/docs" -ForegroundColor Yellow
Write-Host "  -> Health check:               http://127.0.0.1:8000/health" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Para detener: Ctrl+C" -ForegroundColor Gray
Write-Host ""

# Abre el navegador automaticamente despues de 2.5s
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://127.0.0.1:8000/docs"
} | Out-Null

Write-Host "[3/3] Servidor arrancando..." -ForegroundColor Green
& $VenvPython -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
