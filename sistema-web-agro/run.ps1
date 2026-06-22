# Script para ejecutar el prototipo de Sistema Web Agro
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  AGRO-INTELLIGENCE OVERSIGHT - PROTOTIPO" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Inicializando base de datos SQLite..." -ForegroundColor Yellow
python init_db.py

Write-Host "[2/2] Iniciando servidor Flask en puerto 8050..." -ForegroundColor Yellow
Write-Host "Abra su navegador en: http://localhost:8050" -ForegroundColor Green
python -m flask run --host=0.0.0.0 --port=8050
