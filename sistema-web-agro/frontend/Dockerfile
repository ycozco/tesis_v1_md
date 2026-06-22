# Etapa 1: Construcción
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar archivos de dependencias
COPY package.json .

# Instalar dependencias
RUN npm install

# Copiar el código fuente y construir
COPY . .
RUN npm run build

# Etapa 2: Servidor Web de Producción (Nginx)
FROM nginx:alpine

# Copiar configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos estáticos compilados desde la etapa anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Exponer puerto de Nginx
EXPOSE 8050

# Iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]
