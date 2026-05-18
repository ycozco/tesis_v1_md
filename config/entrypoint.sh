#!/bin/bash
# Entrypoint script para Docker - Inicia servicios de tesis

set -e

echo "🚀 Iniciando Servidor de Tesis..."
echo "=================================="

# Variables de entorno
export FLASK_APP=/app/src/app.py
export FLASK_ENV=${FLASK_ENV:-production}

# Crear directorios necesarios
mkdir -p /app/output

# Instalar/actualizar dependencias si es necesario
if [ ! -f "/app/.deps-installed" ]; then
    echo "📦 Instalando dependencias..."
    pip install --no-cache-dir -q flask markdown
    touch /app/.deps-installed
fi

# Convertir Markdown a HTML
echo "🔄 Convirtiendo Markdown a HTML..."
if [ -f "/app/src/convert_md_to_html.py" ]; then
    python3 /app/src/convert_md_to_html.py 2>&1 || true
fi

# Iniciar servidor Flask
echo "🌐 Iniciando Flask en puerto 8000..."
echo "=================================="
echo "📍 Acceso: http://localhost:8000"
echo "=================================="

exec python3 -u /app/src/app.py
