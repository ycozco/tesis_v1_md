# Sistema Agro-Intelligence Oversight — Prototipo Implementado

> **Acceso al prototipo:** Despliegue local con Docker Compose — ver `sistema-web-agro/GUIA_DESPLIEGUE_LOCAL.md`

---

## Descripción General

El sistema **Agro-Intelligence Oversight** es un prototipo funcional completo de supervisión aduanera agroexportadora con IA explicable. Implementado como arquitectura de microservicios Docker, integra un pipeline de 4 capas de Inteligencia Artificial en tiempo real para Declaraciones Aduaneras de Mercancías (DAM).

---

## Pipeline de 4 Capas de IA

### Capa 1 — Predicción FOB (XGBoost)

El modelo XGBoost Regressor estima el **valor FOB esperado** para cada embarque dado un vector de características operacionales: `[fob_declarado, peso_neto, temperatura_contenedor, días_retraso]`. La desviación entre el FOB declarado y el estimado constituye el primer indicador de riesgo financiero.

- **Algoritmo:** XGBoost 2.0 (`reg:squarederror`)
- **Hiperparámetros:** `max_depth=6`, `n_estimators=200`, `learning_rate=0.1`, `subsample=0.8`
- **Serialización:** `models_weights/xgboost_fob_predictor.json`

### Capa 2 — Ensemble de Detección de Anomalías (PyOD)

Un ensemble ponderado de tres detectores no supervisados de PyOD 2.0 produce un **score de anomalía compuesto** ∈ [0,1]:

| Detector | Peso | Rol |
|---|---|---|
| Isolation Forest | 45% | Outliers globales en espacio multidimensional |
| Local Outlier Factor | 30% | Outliers locales en vecindades |
| ECOD | 25% | Sin asunciones de distribución |

Los pesos y el umbral global (default: 0.65) son **configurables en tiempo real** desde la interfaz de administración.

### Capa 3 — Explicabilidad Local (TreeSHAP)

`shap.TreeExplainer` descompone cada predicción XGBoost en contribuciones individuales de Shapley por variable. Los valores SHAP se persisten en `explicaciones_shap` (Numeric 16,6) y se visualizan como gráfico de barras horizontales coloreadas por dirección del efecto:

- 🔴 Positivo: variable impulsa el riesgo
- 🔵 Negativo: variable reduce el riesgo

### Capa 4 — RAG con pgvector (Recuperación Aumentada por Generación)

1. La consulta de alerta es codificada como embedding 384-dim con `BAAI/bge-small-en-v1.5`
2. Búsqueda por similitud coseno (`<=>`) en `documentos_normativos` (PostgreSQL + pgvector)
3. Recuperación de las 3 normativas más relevantes (FDA, SENASA, Ley IA)
4. Generación del informe técnico con Gemini 1.5 Flash o motor heurístico offline
5. Citas `[CAT-ID]` se renderizan como modales interactivos en la UI React

---

## Stack Tecnológico

```
Frontend:     React 18 + Vite + Tailwind CSS → Nginx
Backend:      Python 3.11 + Flask + Gunicorn
Base Datos:   PostgreSQL 15 + pgvector v0.5
ML/IA:        XGBoost 2.0, PyOD 2.0, SHAP 0.45
NLP/RAG:      sentence-transformers 3.0 (BAAI/bge-small-en-v1.5)
LLM:          Google Gemini 1.5 Flash
Orquestación: Docker Compose v2
```

---

## Capturas del Sistema

El sistema cuenta con 10 vistas completas implementadas en React:

| Vista | Función |
|---|---|
| Login | Autenticación + asignación de condición experimental A/B |
| Dashboard | KPIs globales, alertas de mayor riesgo, gráficos de tendencia |
| Gestión de Alertas | Listado filtrable de DAMs con scores y estados |
| **Detalle de Alerta** | **Vista central: 4 capas IA, SHAP, RAG, adjudicación** |
| Telemetría | Boxplots A/B comparativos de tiempos y comprensión |
| Integridad | FPR por producto, Recall por segmento, DPR |
| Explorador de Datos | Explorador de DAMs + Biblioteca RAG interactiva |
| Configuración | Pesos del ensemble, umbral global (ajustable en vivo) |
| Historial | Decisiones pasadas y estados |
| Usuarios | Gestión de auditores y condiciones experimentales |

---

## Despliegue Local

```bash
# Clonar el repositorio
git clone https://github.com/ycozco/tesis_v1_md.git
cd tesis_v1_md/sistema-web-agro

# Construir e iniciar (primera vez: ~10 min)
docker-compose up --build -d

# Acceder a la aplicación
# http://localhost:8050 — Frontend
# http://localhost:5000 — API Backend
```

**Credenciales de prueba:**

| Username | Contraseña | Condición |
|---|---|---|
| `auditor1` | `correct` | Condición A — INTEGRADO (con IA explicable) |
| `auditor2` | `correct` | Condición B — AISLADO (sin explicabilidad) |
| `admin` | `correct` | Panel de administración completo |

---

## Código Fuente

- [`sistema-web-agro/backend/app.py`](https://github.com/ycozco/tesis_v1_md/blob/main/sistema-web-agro/backend/app.py) — Pipeline de inferencia 4 capas
- [`sistema-web-agro/backend/models.py`](https://github.com/ycozco/tesis_v1_md/blob/main/sistema-web-agro/backend/models.py) — Esquema de base de datos + pgvector
- [`sistema-web-agro/backend/init_db.py`](https://github.com/ycozco/tesis_v1_md/blob/main/sistema-web-agro/backend/init_db.py) — Seed + entrenamiento automático de modelos
- [`sistema-web-agro/docker-compose.yml`](https://github.com/ycozco/tesis_v1_md/blob/main/sistema-web-agro/docker-compose.yml) — Orquestación Docker
- [`sistema-web-agro/GUIA_DESPLIEGUE_LOCAL.md`](https://github.com/ycozco/tesis_v1_md/blob/main/sistema-web-agro/GUIA_DESPLIEGUE_LOCAL.md) — Guía completa de despliegue
- [`sistema-web-agro/AVANCE_DETALLADO_TESIS.md`](https://github.com/ycozco/tesis_v1_md/blob/main/sistema-web-agro/AVANCE_DETALLADO_TESIS.md) — Avance técnico completo
