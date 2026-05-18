FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    pandoc \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos necesarios
COPY config/requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# Copiar archivos de tesis y configuración
COPY docs/ /app/docs/
COPY entregable/ /app/entregable/
COPY config/refs.bib /app/config/
COPY config/apa.csl /app/config/

# Copiar código fuente
COPY src/ /app/src/
COPY config/entrypoint.sh /app/src/
RUN chmod +x /app/src/entrypoint.sh

# Puerto
EXPOSE 8000

# Servir aplicación
CMD ["/app/src/entrypoint.sh"]
