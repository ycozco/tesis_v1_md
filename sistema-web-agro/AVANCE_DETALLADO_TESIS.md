# 📋 Avance Detallado del Sistema — Integración hacia la Tesis

> **Título de Tesis:** Sistema de Auditoría Aduanera Agroexportadora con IA Explicable  
> **Autor:** Yoset Cozco Mauri  
> **Director:** Dr. Víctor Cornejo Aparicio  
> **Institución:** Universidad Nacional de San Agustín de Arequipa (UNSA)  
> **Fecha de Corte:** Junio 2026

---

## 1. Resumen Ejecutivo

Se ha implementado un prototipo funcional completo del sistema **Agro-Intelligence Oversight**, que ejecuta en caliente una arquitectura de 4 capas de Inteligencia Artificial sobre Declaraciones Aduaneras de Mercancías (DAM) de exportación agroalimentaria. El sistema opera en contenedores Docker y genera explicaciones locales con XGBoost, TreeSHAP, un ensemble de PyOD y un motor de Recuperación Aumentada por Generación (RAG) sobre PostgreSQL con extensión vectorial `pgvector`.

---

## 2. Objetivos de Tesis — Estado de Cumplimiento

| Objetivo | Descripción | Estado |
|---|---|---|
| **OBJ-1** | Diseñar un sistema de detección de anomalías en DAMs aduaneras | ✅ Completado |
| **OBJ-2** | Implementar un modelo GBDT (XGBoost) para predicción de valor FOB esperado | ✅ Completado |
| **OBJ-3** | Integrar un ensemble de detección de outliers (IForest + LOF + ECOD) | ✅ Completado |
| **OBJ-4** | Proveer explicabilidad local mediante TreeSHAP | ✅ Completado |
| **OBJ-5** | Integrar un motor RAG con base vectorial (pgvector) y normativas legales | ✅ Completado |
| **OBJ-6** | Evaluar la usabilidad en condiciones controladas (A/B entre INTEGRADO vs AISLADO) | 🔄 En Progreso |
| **OBJ-7** | Medir el impacto de la explicabilidad en tiempos de decisión y comprensión (Likert) | 🔄 Pendiente datos reales |

---

## 3. Arquitectura Técnica Implementada

### 3.1 Stack Tecnológico

```
Frontend:    React 18 + Vite + Tailwind CSS → Nginx (Docker)
Backend:     Python 3.11 + Flask + Gunicorn (Docker)
Base de Datos: PostgreSQL 15 + pgvector v0.5 (Docker)
ML/IA:       XGBoost 2.0, PyOD 2.0, SHAP 0.45, scikit-learn 1.5
NLP/RAG:     sentence-transformers 3.0 (BAAI/bge-small-en-v1.5, 384-dim)
LLM:         Google Gemini 1.5 Flash (híbrido: online/offline heurístico)
Orquestación: Docker Compose v2
```

### 3.2 Diagrama de Capas de IA

```
                 DAM Aduanera (Entrada)
                        │
           ┌────────────▼────────────┐
           │  CAPA 1: GBDT (XGBoost) │
           │  Predicción FOB Esperado│
           │  Features: FOB, Peso,   │
           │  Temperatura, Retraso   │
           └────────────┬────────────┘
                        │ fob_esperado_predicho
           ┌────────────▼────────────┐
           │  CAPA 2: Ensemble PyOD  │
           │  Isolation Forest 45%  │
           │  LOF              30%  │
           │  ECOD             25%  │
           │  → Score Anomalía      │
           └────────────┬────────────┘
                        │ score_anomalia ∈ [0,1]
           ┌────────────▼────────────┐
           │  CAPA 3: TreeSHAP      │
           │  Explicaciones Locales │
           │  ΔE[f(x)] por variable │
           └────────────┬────────────┘
                        │ shap_values[]
           ┌────────────▼────────────┐
           │  CAPA 4: RAG + pgvector│
           │  Embedding consulta    │
           │  → Similitud coseno    │
           │  → Top-3 normativas    │
           │  → Gemini/Heurístico   │
           │  → Reporte narrativo   │
           └────────────┬────────────┘
                        │ rag_report (texto con citas [FDA-1], [SENASA-2])
                 Auditor Humano (Decisión)
```

---

## 4. Módulos Implementados — Detalle Técnico

### 4.1 Backend — `backend/app.py`

#### Endpoint Principal: `GET /api/alerts/<id_alerta>`

Este endpoint ejecuta el pipeline completo de las 4 capas en tiempo real:

```python
# Capa 1: XGBoost FOB Prediction
features = get_feature_vector(alert)  # [fob_dec, peso, temp, retraso]
pred_fob = xgb_model.predict(DMatrix(features))

# Capa 2: PyOD Ensemble Score
features_scaled = scaler.transform(features)
p_if  = iforest.predict_proba(features_scaled)[0][1]
p_lof = lof.predict_proba(features_scaled)[0][1]
p_eco = ecod.predict_proba(features_scaled)[0][1]
score = p_if*0.45 + p_lof*0.30 + p_eco*0.25  # pesos configurables

# Capa 3: TreeSHAP Local
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(features)

# Capa 4: pgvector Semantic Search
query_emb = embedding_model.encode(query_text)
docs = db.query(DocumentoNormativo)
       .order_by(DocumentoNormativo.embedding.cosine_distance(query_emb))
       .limit(3).all()

# RAG Report (Gemini API o fallback heurístico)
rag_report = gemini_generate(prompt, docs) or offline_heuristic(docs)
```

#### Otros Endpoints Relevantes

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/auth/login` | Autenticación con asignación de condición A/B |
| POST | `/api/alerts/<id>/adjudicate` | Registra decisión + telemetría de tiempo |
| GET | `/api/config` | Lee/escribe pesos del ensemble y umbral global |
| GET | `/api/config/documents` | Lista documentos normativos en pgvector |
| POST | `/api/config/documents` | Vectoriza e indexa nueva normativa en pgvector |
| GET | `/api/telemetry/stats` | Estadísticas de boxplots por condición A/B |
| GET | `/api/integrity/stats` | FPR por producto, Recall por grupo, DPR |

### 4.2 Base de Datos — `backend/models.py`

```
Tablas PostgreSQL (pgvector/pgvector:pg15):

  usuarios               → Autenticación y roles (ADMIN / AUDITOR)
  operaciones_alertas    → DAMs con score_anomalia y valor_fob_esperado (dinámicos)
  decisiones_auditoria   → Telemetría: tiempo decisión, Likert comprensión, condición A/B
  explicaciones_shap     → Valores TreeSHAP por alerta (actualizados en tiempo real)
  security_logs          → Eventos de acceso y auditoría del sistema
  documentos_normativos  → Normativas RAG con columna embedding VECTOR(384)
```

**Columna vectorial de pgvector:**
```sql
embedding VECTOR(384)  -- 384 dimensiones → BAAI/bge-small-en-v1.5
```
Búsqueda semántica por distancia coseno:
```sql
ORDER BY embedding <=> query_vector LIMIT 3
```

### 4.3 Frontend — Vistas React

| Vista | Ruta | Descripción |
|---|---|---|
| Login | `/login` | Autenticación + asignación de condición experimental |
| Dashboard | `/dashboard` | Estadísticas globales, alertas prioritarias, telemetría |
| Alertas | `/alerts` | Listado filtrable de DAMs con scores y estados |
| Detalle | `/alerts/:id` | **Vista central:** 4 capas de IA, SHAP, RAG, adjudicación |
| Historial | `/history` | Decisiones pasadas y su estado |
| Telemetría | `/telemetry` | Boxplots A/B de tiempos de decisión + comprensión |
| Integridad | `/integrity` | FPR por producto, Recall por grupo exportador, DPR |
| Datos | `/data` | Explorador + **Biblioteca RAG** con indexador de normativas |
| Configuración | `/config` | Pesos del ensemble, umbral global |
| Usuarios | `/users` | Gestión de auditoría y condiciones experimentales |

---

## 5. Explicabilidad — Fundamento para la Tesis

### 5.1 TreeSHAP (Capa 3)

Se utiliza `shap.TreeExplainer` sobre el modelo XGBoost entrenado, que calcula los valores SHAP de Shapley locales para cada operación:

- **Variable positiva (rojo):** Aumenta la probabilidad de anomalía. Ej: alta temperatura de contenedor, retraso logístico.
- **Variable negativa (azul):** Reduce el riesgo. Ej: bajo FOB declarado correlacionado con peso histórico normal.

Los valores SHAP se persisten en `explicaciones_shap` y se actualizan dinámicamente en cada consulta, asegurando que el auditor vea siempre la explicación local real y no precalculada.

### 5.2 RAG (Recuperación Aumentada por Generación — Capa 4)

El motor RAG sigue el siguiente flujo:

1. **Construcción de la consulta:** Se genera un texto descriptivo de la alerta (producto, FOB, temperatura, retraso).
2. **Embedding:** Se codifica con `BAAI/bge-small-en-v1.5` (384 dimensiones) usando `sentence-transformers`.
3. **Búsqueda vectorial:** Se consulta `documentos_normativos` por similitud coseno (`<=>`) en pgvector.
4. **Recuperación:** Los 3 documentos más relevantes se pasan al generador de texto.
5. **Generación:** Gemini 1.5 Flash (si hay clave API) o motor heurístico offline producen el informe final en español, con citas en formato `[CATEGORIA-ID]` (ej. `[FDA-1]`, `[SENASA-2]`).
6. **Renderizado interactivo:** React parsea las citas con regex y las convierte en enlaces que abren modales con el texto completo de la normativa.

### 5.3 Condiciones Experimentales (Diseño A/B)

Para medir el impacto de la explicabilidad en la toma de decisiones aduaneras:

| | Condición A (INTEGRADO) | Condición B (AISLADO) |
|---|---|---|
| Datos de la DAM | ✅ | ✅ |
| FOB Esperado (XGBoost) | ✅ | ✅ |
| Score Ensemble | ✅ | ✅ |
| SHAP (Capa 3) | ✅ | ❌ |
| Narrativa RAG (Capa 4) | ✅ | ❌ |
| **Hipótesis:** | Menor tiempo de decisión, mayor comprensión | — |

**Métricas capturadas automáticamente:**
- `time_to_decision_ms`: tiempo desde que carga la alerta hasta submit
- `likert_comprehension`: escala 1-5 de comprensión percibida de la IA
- `user_decision`: 0=Falsa alarma, 1=Anomalía confirmada, 2=Requiere inspección

---

## 6. Normativas Legales en la Biblioteca RAG

Las siguientes normativas fueron indexadas y vectorizadas en la base de datos pgvector:

| ID | Categoría | Normativa | Relevancia |
|---|---|---|---|
| 1 | FDA | CFR Title 21 - Importación de Perecederos (Cap. 1) | Inspección física ante desvíos FOB >15% |
| 2 | SENASA | Directiva de Control Fitosanitario N° 04-2026 | Inspección fitosanitaria por retrasos >48h |
| 3 | LEY_IA | Reglamento Ley de IA del Perú (D.S. N° 115-2025-PCM) | Obligatoriedad de explicabilidad en IA de alto riesgo |

Los usuarios con rol ADMIN pueden añadir nuevas normativas desde la vista **Explorador de Datos**, que las vectoriza en tiempo real y las incorpora al motor RAG de todas las alertas subsiguientes.

---

## 7. Métricas del Sistema — Estado Actual

### 7.1 Métricas de Fairness / Integridad del Modelo

Calculadas dinámicamente desde las decisiones auditadas:

| Métrica | Descripción | Datos Actuales |
|---|---|---|
| **FPR por Producto** | Tasa de falsos positivos por categoría (Palta, Uva, Arándano, Mango) | Seed: 12.8%, 6.0%, 5.2%, 4.0% |
| **Recall por Grupo** | Recall segmentado por tamaño exportador (FOB) | Seed: Pequeño 82%, Mediano 91%, Grande 94% |
| **DPR** | Razón de Paridad Demográfica (equidad entre grupos) | ~0.94 |
| **F1 por Puerto** | F1-Score por puerto de destino | Rotterdam 0.96, Philadelphia 0.93 |

### 7.2 Telemetría del Experimento (datos semilla)

| Condición | Auditor | Tiempo Decisión | Comprensión |
|---|---|---|---|
| INTEGRADO | auditor1 | 25.6 s | 5/5 |
| AISLADO | auditor1 | 49.2 s | 3/5 |
| INTEGRADO | auditor2 | 31.2 s | 4/5 |
| AISLADO | auditor2 | 65.4 s | 2/5 |

> Hipótesis preliminar: la condición INTEGRADO (con IA explicable) reduce el tiempo de decisión ~48% y mejora la comprensión en ~1.75 puntos Likert.

---

## 8. Lo que QUEDA PENDIENTE

### 8.1 Pendientes de Implementación

| # | Tarea | Prioridad | Descripción |
|---|---|---|---|
| P1 | **Pruebas de Usabilidad Reales** | 🔴 Alta | Ejecutar la sesión experimental con auditorías reales (10+ participantes), capturar datos auténticos de tiempo y comprensión |
| P2 | **Análisis Estadístico A/B** | 🔴 Alta | Aplicar prueba de Mann-Whitney U o t-test sobre tiempos de decisión reales entre condiciones A y B |
| P3 | **Entrenamiento con Datos Reales SUNAT** | 🟡 Media | Reemplazar datos sintéticos por datos históricos reales de DAMs de Aduana Lima-Callao |
| P4 | **Validación de Modelos (Hold-out)** | 🟡 Media | Evaluar XGBoost con MAE, RMSE, R² sobre dataset real; PyOD con AUC-ROC sobre casos etiquetados |
| P5 | **Prueba de Carga** | 🟡 Media | Stress test del API con múltiples auditorías concurrentes (Locust o k6) |
| P6 | **Autenticación JWT** | 🟢 Baja | Reemplazar mock-token por JWT real con expiración |
| P7 | **Clave Gemini API** | 🟢 Baja | Configurar `GEMINI_API_KEY` en docker-compose para activar reporte LLM adaptativo en vivo |
| P8 | **Tests Automatizados** | 🟢 Baja | Unit tests para `get_feature_vector`, endpoints REST y pipeline SHAP |

### 8.2 Pendientes de Documentación para Tesis

| # | Capítulo / Sección | Estado |
|---|---|---|
| D1 | Capítulo 3 — Marco Teórico de XGBoost y SHAP | Pendiente redacción |
| D2 | Capítulo 3 — RAG: Fundamentos y Arquitectura pgvector | Pendiente redacción |
| D3 | Capítulo 4 — Descripción de la implementación de contenedores | Pendiente redacción |
| D4 | Capítulo 5 — Resultados del experimento A/B (requiere datos reales) | Bloqueado por P1 |
| D5 | Capítulo 5 — Análisis de fairness del modelo | Pendiente (requiere datos reales) |
| D6 | Anexos — Manual de Usuario del sistema | Parcial (usar GUIA_DESPLIEGUE_LOCAL.md) |

---

## 9. Contenido Listo para Integrar a la Tesis

### 9.1 Descripción del Sistema (Capítulo 4)

> El prototipo Agro-Intelligence Oversight implementa una arquitectura de microservicios orquestada con Docker Compose, compuesta por tres contenedores: (1) una base de datos PostgreSQL 15 con la extensión pgvector habilitada para búsqueda semántica vectorial, (2) un servicio backend en Python 3.11 con Flask y Gunicorn que ejecuta el pipeline de inferencia de cuatro capas, y (3) un frontend React 18 servido por Nginx como servidor web de producción.

### 9.2 Descripción del Pipeline de IA (Capítulo 4)

> El pipeline de auditoría ejecuta cuatro capas de análisis en tiempo real para cada DAM inspeccionada:
>
> **Capa 1 (GBDT):** Un modelo XGBoost regressor, entrenado sobre vectores de características `[valor_fob_declarado, peso_neto, temperatura_contenedor, días_retraso]`, estima el valor FOB esperado para el envío. La desviación porcentual entre el FOB declarado y el estimado es el primer indicador de riesgo financiero.
>
> **Capa 2 (Ensemble de Detección de Anomalías):** Un ensemble ponderado de tres detectores no supervisados de PyOD —Isolation Forest (45%), Local Outlier Factor (30%) y ECOD (25%)— calcula un score de anomalía compuesto ∈ [0,1]. El umbral global configurable (por defecto 0.65) determina si la operación activa una alerta.
>
> **Capa 3 (Explicabilidad Local — TreeSHAP):** Para cada alerta, se computa el valor SHAP de Shapley mediante `shap.TreeExplainer` sobre el modelo XGBoost. Los valores SHAP descomponen la contribución individual de cada variable sobre la predicción, permitiendo al auditor identificar qué factor (precio residual, temperatura, retraso logístico) impulsa principalmente el score de riesgo.
>
> **Capa 4 (RAG — Recuperación Aumentada por Generación):** El texto de consulta es codificado como un embedding de 384 dimensiones con el modelo `BAAI/bge-small-en-v1.5` de sentence-transformers. Se realiza una búsqueda por similitud coseno (`<=>`) sobre la tabla `documentos_normativos` en pgvector, recuperando las tres normativas legales más relevantes. El motor de generación (Gemini 1.5 Flash o fallback heurístico offline) produce un informe técnico estructurado en español, con citas explícitas a las normativas recuperadas (ej. `[FDA-1]`, `[SENASA-2]`), que el auditor puede consultar mediante modales interactivos.

### 9.3 Justificación de Herramientas (Capítulo 3)

| Herramienta | Justificación |
|---|---|
| **XGBoost** | Estado del arte en regresión tabular, interpretable vía SHAP, ampliamente validado en literatura de detección de fraude aduanero |
| **PyOD** | Librería unificada de detección de outliers no supervisada; el ensemble reduce el sesgo de un solo detector |
| **SHAP TreeExplainer** | Valores de Shapley con complejidad O(TLD²) exactos para modelos de árbol; garantizan fidelidad local |
| **pgvector** | Extensión nativa de PostgreSQL que elimina la necesidad de un vector store externo (Pinecone, Weaviate); reduce la latencia y simplifica el despliegue |
| **BAAI/bge-small-en-v1.5** | Modelo de embeddings multilingüe de 384 dimensiones, equilibrio óptimo entre precisión semántica y costo computacional sin GPU |
| **Docker Compose** | Reproducibilidad del entorno; garantiza que el prototipo ejecute idénticamente en cualquier máquina para la evaluación de usabilidad |

---

## 10. Registro de Cambios Técnicos Principales

| Fecha | Cambio | Archivos |
|---|---|---|
| Jun 2026 | Migración de imagen DB a `pgvector/pgvector:pg15` | `docker-compose.yml` |
| Jun 2026 | Adición de dependencias ML/NLP en backend | `requirements.txt` |
| Jun 2026 | Nuevo modelo `DocumentoNormativo` con columna `VECTOR(384)` | `models.py` |
| Jun 2026 | Auto-entrenamiento de XGBoost + PyOD + scaler al iniciar contenedor | `init_db.py` |
| Jun 2026 | Vectorización de normativas FDA/SENASA/Ley-IA en pgvector al seed | `init_db.py` |
| Jun 2026 | Pipeline 4-capas en caliente en `GET /api/alerts/<id>` | `app.py` |
| Jun 2026 | Endpoints RAG: `GET/POST /api/config/documents` | `app.py` |
| Jun 2026 | Motor heurístico offline de reportes RAG con citas reales | `app.py` |
| Jun 2026 | Renderizado dinámico de citas `[CAT-ID]` como links en Detail | `Detail.jsx` |
| Jun 2026 | Biblioteca RAG + formulario de indexación en Explorador de Datos | `Data.jsx` |
| Jun 2026 | Precisión de `shap_value` ampliada a `Numeric(16,6)` | `models.py` |
