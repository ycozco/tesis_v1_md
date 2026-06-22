FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer el puerto del API
EXPOSE 5000

# Inicializar base de datos y luego iniciar el servidor con Gunicorn en producción
CMD python init_db.py && gunicorn --workers 4 --threads 2 -b 0.0.0.0:5000 app:app
