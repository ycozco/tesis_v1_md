# 🚀 Guía de Despliegue Local — Agro-Intelligence Oversight

> Sistema de Auditoría Aduanera Agroexportadora con IA Explicable  
> Tesis de Ingeniería de Sistemas — UNSA 2026

---

## Prerrequisitos

| Herramienta | Versión mínima | Verificar con |
|---|---|---|
| Docker Desktop | 4.x o superior | `docker --version` |
| Docker Compose | v2 (incluido en Docker Desktop) | `docker compose version` |
| Git | 2.x | `git --version` |

> **Nota:** No es necesario tener Python, Node.js ni PostgreSQL instalados localmente. Todo corre dentro de los contenedores Docker.

---

## Estructura del Proyecto

```
sistema-web-agro/
├── backend/                    # API Flask + modelos de IA
│   ├── app.py                  # Endpoints REST + pipeline de inferencia
│   ├── models.py               # Modelos SQLAlchemy + pgvector
│   ├── init_db.py              # Semillero de DB + entrenamiento de modelos
│   ├── requirements.txt        # Dependencias Python (ML, NLP, Flask)
│   ├── Dockerfile              # Imagen del backend
│   └── DATOS_PRUEBA.txt        # Credenciales y datos de prueba
├── frontend/                   # React SPA
│   ├── src/pages/              # Vistas (Dashboard, Alerts, Detail, Data, ...)
│   ├── Dockerfile              # Imagen multi-stage (Node builder + Nginx)
│   └── nginx.conf              # Proxy inverso → backend :5000
├── docker-compose.yml          # Orquestación de los 3 servicios
└── GUIA_DESPLIEGUE_LOCAL.md    # Este archivo
```

---

## Pasos de Despliegue

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd sistema-web-agro
```

### 2. (Opcional) Configurar API Key de Gemini

Si deseas activar el reporte RAG generado por LLM real (Google Gemini 1.5 Flash), edita `docker-compose.yml` y agrega la variable de entorno al servicio `backend`:

```yaml
environment:
  - GEMINI_API_KEY=tu_clave_aqui
```

Sin esta clave, el sistema operará en **Modo Offline Heurístico** (igualmente funcional para la demostración de tesis).

### 3. Construir e iniciar los contenedores

```bash
docker-compose up --build -d
```

Este comando realiza automáticamente:
- Descarga la imagen `pgvector/pgvector:pg15` (PostgreSQL con extensión vectorial)
- Compila la imagen del backend (instala dependencias de ML: XGBoost, PyOD, SHAP, sentence-transformers, etc.)
- Compila la imagen del frontend (React → bundle estático servido por Nginx)
- Espera a que PostgreSQL esté `HEALTHY` antes de iniciar el backend
- Ejecuta `init_db.py` que:
  - Habilita la extensión `pgvector` en la base de datos
  - Crea todas las tablas del esquema
  - Siembra usuarios, alertas, decisiones y logs
  - Vectoriza las normativas legales (FDA, SENASA, Ley IA) con `BAAI/bge-small-en-v1.5` → pgvector
  - Entrena y serializa los modelos XGBoost + IForest + LOF + ECOD en `models_weights/`

> ⚠️ La primera construcción puede tardar **8-12 minutos** por la descarga de dependencias de ML (~2GB). Las construcciones posteriores usan caché de Docker y tardan segundos.

### 4. Verificar que los servicios estén activos

```bash
docker ps
```

Deberías ver 3 contenedores en estado `Up`:

```
agro_frontend   sistema-web-agro-frontend   Up   0.0.0.0:8050->8050/tcp
agro_backend    sistema-web-agro-backend    Up   0.0.0.0:5000->5000/tcp
agro_db         pgvector/pgvector:pg15      Up   0.0.0.0:5432->5432/tcp (healthy)
```

### 5. Acceder a la aplicación

| Recurso | URL |
|---|---|
| **Aplicación Web** | http://localhost:8050 |
| **API REST** | http://localhost:5000/api |
| **Base de Datos** | `localhost:5432` — DB: `agro_audit` — User: `postgres` — Pass: `postgres` |

---

## Credenciales de Prueba

| Username | Contraseña | Rol | Condición Experimental |
|---|---|---|---|
| `auditor1` | `correct` | AUDITOR | **Condición A** — Ve capas de IA (SHAP + RAG) |
| `auditor2` | `correct` | AUDITOR | **Condición B** — Solo datos, sin explicabilidad |
| `admin` | `correct` | ADMIN | Panel completo de administración |

---

## Reinicio Limpio (Borrar todos los datos y reentrenar)

```bash
# Detener contenedores Y borrar el volumen de datos de PostgreSQL
docker-compose down -v

# Reconstruir e iniciar desde cero
docker-compose up --build -d
```

## Solo reiniciar servicios (sin perder datos)

```bash
docker-compose restart
```

## Ver logs en tiempo real

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend (modelos de IA, errores de inferencia)
docker logs agro_backend -f

# Solo base de datos
docker logs agro_db -f
```

---

## Arquitectura de Contenedores

```
┌──────────────────────────────────────────────────────────────┐
│                    Docker Network (bridge)                   │
│                                                              │
│  ┌─────────────────┐    ┌─────────────────────────────────┐  │
│  │  agro_frontend  │    │          agro_backend           │  │
│  │  Nginx :8050    │───▶│   Flask + Gunicorn :5000        │  │
│  │  React SPA      │    │   XGBoost + PyOD + SHAP         │  │
│  │  (prod bundle)  │    │   sentence-transformers (BGE)   │  │
│  └─────────────────┘    │   google-generativeai (opcional)│  │
│                         └──────────────┬────────────────────┘  │
│                                        │                     │
│                         ┌──────────────▼────────────────────┐  │
│                         │           agro_db                 │  │
│                         │   PostgreSQL 15 + pgvector        │  │
│                         │   Tablas: usuarios, alertas,      │  │
│                         │   decisiones, explicaciones_shap, │  │
│                         │   documentos_normativos (vector)  │  │
│                         └───────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
        │
        ▼ Puerto expuesto al host
  http://localhost:8050  (usuario final)
  http://localhost:5000  (API directa / debug)
```

---

## Flujo de Prueba para Sustentación de Tesis

1. Abrir http://localhost:8050/login
2. Login con `auditor1` / `correct` → **Condición A (INTEGRADO)**
3. En el Dashboard, clic sobre alerta `AL-2026-0012` (Palta, RIESGO CRÍTICO)
4. Observar las 4 capas de IA en la vista de detalle:
   - **Capa 1:** Predicción FOB Esperado por XGBoost vs FOB Declarado
   - **Capa 2:** Score de Anomalía del Ensemble PyOD (IForest + LOF + ECOD)
   - **Capa 3:** Gráfico de atribuciones SHAP (TreeSHAP local)
   - **Capa 4:** Narrativa RAG con citas clickeables `[FDA-1]`, `[SENASA-2]` que abren modales
5. Adjudicar la alerta → registra telemetría (tiempo de decisión, Likert de comprensión)
6. Ir a **Explorador de Datos** → indexar nueva normativa en la biblioteca RAG
7. Cerrar sesión → Login con `auditor2` / `correct` → **Condición B (AISLADO)**
8. Verificar métricas comparativas en `/telemetry` (Admin)
