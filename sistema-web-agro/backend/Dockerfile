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

# Inicializar base de datos SOLO si no existen tablas, luego iniciar el servidor
CMD python -c "import sys; sys.path.insert(0,'.'); from models import engine, Base, SessionLocal, init_tables, Usuario; from sqlalchemy import text; \
db_name = engine.dialect.name; \
db = engine.connect(); \
tables = engine.dialect.get_table_names(db); \
db.close(); \
needs_init = 'usuarios' not in tables; \
print(f'Tablas existentes: {tables}'); \
print(f'Necesita inicializar: {needs_init}'); \
needs_init and exec(open('init_db.py').read()) or print('Base de datos ya inicializada, saltando seed.')" && gunicorn --workers 4 --threads 2 -b 0.0.0.0:5000 app:app
