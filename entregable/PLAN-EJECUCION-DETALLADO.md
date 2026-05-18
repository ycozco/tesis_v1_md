# PLAN DE EJECUCIÓN DETALLADO
## Sistema Integrado de Predicción y Detección de Anomalías - Agroexportación

**Versión**: 2.0  
**Fecha de Inicio**: 15 Mayo 2026  
**Fecha de Fin**: 07 Agosto 2026  
**Duración**: 12 semanas (60 días hábiles)  
**Responsable**: Yoset Cozco Mauri  
**Asesor Técnico**: Dr. Víctor Manuel Cornejo Aparicio  

---

## ESTRUCTURA GENERAL DEL PLAN

```
FASE I: PREPARACIÓN Y DISEÑO (Semanas 1-2)
├─ Hito 0.1: Requisitos validados
├─ Hito 0.2: Arquitectura diseñada
└─ Hito 0.3: Stack técnico confirmado

FASE II: DESARROLLO DE COMPONENTES (Semanas 3-10)
├─ Hito 1: Ingestión de datos operativa (Semana 4)
├─ Hito 2: Modelo de predicción entrenado (Semana 6)
├─ Hito 3: Detección de anomalías validada (Semana 8)
├─ Hito 4: Explicabilidad integrada (Semana 9)
└─ Hito 5: Sistema de reportes funcional (Semana 10)

FASE III: VALIDACIÓN E INTEGRACIÓN (Semanas 11-12)
├─ Hito 6: Testing completo y auditoría
├─ Hito 7: Validación regulatoria (SBS, D.S.115)
└─ Hito 8: Deployment en producción

FASE IV: POST-LANZAMIENTO (Semanas 13-16 - Post tesis)
├─ Monitoreo en producción
├─ Documentación y capacitación
└─ Mejoras continuas
```

---

## FASE I: PREPARACIÓN Y DISEÑO (Semanas 1-2)

### 1.1 Semana 1: Requisitos y Scope

#### Tarea 1.1.1: Entrevistas con Stakeholders
**Responsable**: Yoset + Dr. Cornejo  
**Duración**: 5 horas  
**Deliverable**: Documento de Requisitos

```
Stakeholders a entrevistar:
├─ Supervisor operativo (empresa agroexportadora)
├─ Auditor interno (SBS/BI)
├─ Jefe de almacén/logística
├─ Especialista en comercio exterior
└─ Responsable de sistemas
```

**Preguntas clave**:
1. ¿Cuáles son las 3 anomalías más costosas en operación?
2. ¿Con qué frecuencia necesita reportes? (diaria, semanal, mensual)
3. ¿Quién revisa/aprueba las recomendaciones del sistema?
4. ¿Cuál es el costo de una decisión incorrecta?

**Output esperado**:
- Documento: `REQUISITOS-FUNCIONALES.md`
- Lista de 10-15 casos de uso específicos
- Matriz de criticidad/frecuencia

#### Tarea 1.1.2: Definición de Métricas de Éxito
**Responsable**: Yoset  
**Duración**: 3 horas  
**Entregable**: `METRICAS-EXITO-PROYECTO.md`

```
MÉTRICAS TÉCNICAS:
├─ Predicción: AUC-PR ≥ 0.85, F1-Score ≥ 0.78
├─ Detección anomalías: Precision ≥ 0.88, Recall ≥ 0.72
├─ Explicabilidad: Completitud SHAP ≥ 95%, Coverage ≥ 85%
├─ Reportes: ROUGE-L ≥ 0.60, Tiempo ≤ 30 segundos
└─ Escalabilidad: Latencia ≤ 100ms para 1000 req/min

MÉTRICAS DE NEGOCIO:
├─ Reducción de mermas: De 4% actual a 2% objetivo
├─ Mejora de precisión en alertas: De 50% a 85%
├─ Tiempo de investigación: De 8h a 1h
└─ Tasa de adopción de recomendaciones: ≥ 80%

MÉTRICAS DE CUMPLIMIENTO:
├─ Trazabilidad: 100% de decisiones auditables
├─ Documentación: 100% de Model Cards y Datasheets completados
└─ Testing: 95%+ cobertura de código
```

#### Tarea 1.1.3: Roadmap de Datos
**Responsable**: Yoset  
**Duración**: 4 horas  
**Entregable**: `ROADMAP-DATOS.md`

```
FUENTES A INTEGRAR (Orden de prioridad):
1. MIDAGRI Precios Mayoristas (Crítica, iniciador)
2. SENAMHI Datos Climáticos (Alta, correlación)
3. INEI IPM/IPC (Alta, normalización)
4. SENASA Requisitos (Media, validación)
5. SUNAT Estadísticas (Media, contexto)
6. FAOSTAT (Baja, validación comparativa)

TIMELINE DE INGESTIÓN:
├─ Week 1-2: Especificación de fuentes
├─ Week 3-4: Desarrollo de extractores
├─ Week 5: Integración y validación
└─ Week 6+: Monitoreo y actualizaciones
```

---

### 1.2 Semana 2: Diseño Arquitectónico

#### Tarea 1.2.1: Diseño de Arquitectura de Capas
**Responsable**: Yoset + Dr. Cornejo  
**Duración**: 6 horas  
**Entregable**: `ARQUITECTURA-SISTEMA.md` con diagramas

```
┌─────────────────────────────────────────────────┐
│         ARQUITECTURA DE 4 CAPAS                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────┐          │
│  │ 4. Generación de Reportes        │          │
│  │    (LLM + RAG)                   │          │
│  └──────────────────────────────────┘          │
│           ↑                                     │
│  ┌──────────────────────────────────┐          │
│  │ 3. Explicabilidad                │          │
│  │    (SHAP + LIME)                 │          │
│  └──────────────────────────────────┘          │
│           ↑                                     │
│  ┌─────────────────┬─────────────────┐          │
│  │ 2a. Predicción  │ 2b. Detección   │          │
│  │    (GBDT)       │    (Ensemble)   │          │
│  └─────────────────┴─────────────────┘          │
│           ↑                                     │
│  ┌──────────────────────────────────┐          │
│  │ 1. Ingestión de Datos            │          │
│  │    (Airflow + Pandas)            │          │
│  └──────────────────────────────────┘          │
│           ↑                                     │
│  ┌──────────────────────────────────┐          │
│  │ 0. Fuentes de Datos              │          │
│  │    (MIDAGRI, SENAMHI, INEI)      │          │
│  └──────────────────────────────────┘          │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### Tarea 1.2.2: Definición de Schema de Base de Datos
**Responsable**: Yoset  
**Duración**: 4 horas  
**Entregable**: Script SQL de esquema

```sql
-- TABLA PRINCIPAL: Precios y Contexto
CREATE TABLE price_observations (
    observation_id UUID PRIMARY KEY,
    date DATE NOT NULL,
    product VARCHAR(100) NOT NULL,
    market VARCHAR(100) NOT NULL,
    price_usd DECIMAL(10,2),
    volume_kg BIGINT,
    temp_celsius FLOAT,
    precipitation_mm FLOAT,
    humidity_pct FLOAT,
    ipm_index FLOAT,
    ipc_index FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_date (date),
    INDEX idx_product (product)
);

-- TABLA: Predicciones
CREATE TABLE predictions (
    prediction_id UUID PRIMARY KEY,
    observation_id UUID REFERENCES price_observations,
    model_version VARCHAR(50),
    predicted_anomaly BOOLEAN,
    anomaly_score FLOAT,
    confidence FLOAT,
    created_at TIMESTAMP,
    INDEX idx_observation (observation_id)
);

-- TABLA: Explicabilidad (SHAP)
CREATE TABLE shap_explanations (
    explanation_id UUID PRIMARY KEY,
    prediction_id UUID REFERENCES predictions,
    feature_name VARCHAR(100),
    shap_value FLOAT,
    baseline_value FLOAT,
    feature_value FLOAT,
    created_at TIMESTAMP
);

-- TABLA: Auditoría
CREATE TABLE audit_log (
    audit_id UUID PRIMARY KEY,
    prediction_id UUID REFERENCES predictions,
    action VARCHAR(50), -- GENERATED, REVIEWED, APPROVED, REJECTED
    reviewer_id VARCHAR(100),
    comments TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    INDEX idx_prediction (prediction_id)
);
```

#### Tarea 1.2.3: Plan de Testing
**Responsable**: Yoset  
**Duración**: 3 horas  
**Entregable**: `PLAN-TESTING.md`

```
STRATEGY DE TESTING:

Unit Testing (Semana 7)
├─ Test de extractores de datos: 15 casos
├─ Test de pipelines de preproceso: 20 casos
├─ Test de modelos (mock data): 25 casos
└─ Test de explicabilidad: 15 casos
Total: 75 test cases (Target: 95%+ coverage)

Integration Testing (Semana 9)
├─ End-to-end pipeline: 5 escenarios
├─ Datos reales (primer 1% dataset): 3 casos
└─ APIs y conectores: 10 casos

Validation Testing (Semana 10)
├─ Casos de uso reales: 8 scenarios
├─ Stress test (10K registros): Latencia <100ms
├─ Fairness testing: Desempeño por subgrupo
└─ Security testing: Inyección de datos, auth

User Acceptance (Semana 11)
├─ Supervisor operativo prueba sistema
├─ Auditor valida trazabilidad
└─ Retroalimentación y ajustes menores
```

---

## FASE II: DESARROLLO DE COMPONENTES (Semanas 3-10)

### 2.1 Semanas 3-4: Ingestión de Datos

#### Hito 1: Sistema de Ingestión Operativo

**Objetivo**: Datos de todas las fuentes disponibles en BD, validados y listos

**Tarea 2.1.1: Extractor MIDAGRI**
```
Input: Boletín de precios (PDF)
Output: Table price_observations (250-500 registros/mes)

Pasos:
1. Descarga automatizada de PDFs (Airflow)
2. Parsing OCR + regex (Tesseract + pandas)
3. Validación: Check duplicados, outliers, NaN
4. Normalización: Conversión de unidades, moneda
5. Carga a BD (upsert por observation_id)
6. QA: Validación manual 10% sample

Responsable: Yoset
Duración: 1 semana
Test: 50+ casos, cobertura 90%
```

**Tarea 2.1.2: Integración SENAMHI API**
```
Input: API SENAMHI (datos climáticos históricos)
Output: Table weather_observations (5,000+ registros/mes)

Pasos:
1. Setup credenciales API
2. Desarrollo de cliente Python
3. Batch retrieval (paralelización)
4. Validación: Rango de temperaturas, precipitación
5. Carga a BD (upsert por fecha/estación)
6. Backfill histórico (2 años)

Responsable: Yoset
Duración: 1 semana
Test: 30+ casos
```

**Tarea 2.1.3: Descarga INEI (IPM, IPC, PBI)**
```
Input: Excel/CSV de INEI
Output: Table economic_indicators (240 registros/año)

Pasos:
1. Descarga manual/automática
2. Parsing CSV
3. Normalización de fechas
4. Validación de continuidad (no gaps)
5. Carga a BD
6. Merge con tablas existentes

Responsable: Yoset
Duración: 3 días
```

**Tarea 2.1.4: Orquestación en Airflow**
```
DAG: price_and_weather_pipeline
Schedule: Diariamente 6:00 AM

Steps:
1. Extract MIDAGRI (monthly)
2. Extract SENAMHI (daily)
3. Extract INEI (monthly)
4. Validate all tables
5. Quality checks
6. Alert if failures

Responsable: Yoset
Duración: 3 días
Monitoring: Email alerts + dashboard
```

**Criterio de éxito del Hito 1**:
- ✅ 100% de registros MIDAGRI ingesta (últimas 24 meses)
- ✅ 100% de estaciones SENAMHI disponibles
- ✅ 100% de indicadores INEI alineados
- ✅ Zero data quality issues en validación
- ✅ Pipeline se ejecuta automáticamente sin errores

---

### 2.2 Semanas 5-6: Modelo de Predicción (GBDT)

#### Hito 2: XGBoost Entrenado y Validado

**Tarea 2.2.1: Feature Engineering**
```
Objetivo: Crear 30-40 features óptimas para predicción

Features de Series Temporales:
├─ Precios (MIDAGRI):
│  ├─ Price MA-7, MA-30, MA-90 (medias móviles)
│  ├─ Price momentum (cambio % en 7d, 30d)
│  ├─ Price volatility (std dev 30d)
│  ├─ Price seasonality (mes-on-month)
│  └─ Price de-trend (residual HP filter)
├─ Volúmenes (MIDAGRI):
│  ├─ Volume MA-7, trend, ratio
│  └─ Seasonal volume decomposition
└─ Clima (SENAMHI):
   ├─ Temp MA-7, min/max range
   ├─ Precip acumulada 7d, 30d
   ├─ Humidity trend
   └─ Growing Degree Days (agrícola)

Features Macroeconómicas:
├─ IPM change (% change mes-a-mes)
├─ IPC change
├─ Real exchange rate (USD/SOL)
└─ Commodity index (café, oro, otros)

Features Categóricas:
├─ Producto (palta, espárrago, berries)
├─ Mercado (GMML, MM Frutas, otros)
├─ Estación (verano, invierno)
└─ Day-of-week (efecto día de semana)

Responsable: Yoset
Duración: 1 semana
Output: Dataset con 40 features, 0% missing
```

**Tarea 2.2.2: Preparación de Datos de Entrenamiento**
```
Dataset de entrenamiento:
├─ Período: Enero 2024 - Marzo 2026 (28 meses)
├─ Frecuencia: Mensual (336 observaciones)
├─ Train/val/test: 70% / 15% / 15%
└─ Balanceo de clases: SMOTE si necesario

Target variable:
├─ Anomalía: Precio > Media + 2.5*StdDev O < Media - 2.5*StdDev
├─ Base rate: ~8% de anomalías esperadas
└─ Labeling manual: Supervisor confirma 20% de casos

Responsable: Yoset
Duración: 3 días
```

**Tarea 2.2.3: Entrenamiento y Tuning de XGBoost**
```
Hyperparameter Grid Search:

Base XGBoost:
├─ n_estimators: [100, 200, 500]
├─ max_depth: [4, 6, 8]
├─ learning_rate: [0.01, 0.05, 0.1]
├─ subsample: [0.7, 0.8, 0.9]
├─ colsample_bytree: [0.7, 0.8, 1.0]
└─ min_child_weight: [1, 3, 5]

Cross-validation: 5-fold time-series CV
Metric optimization: AUC-PR (not AUC-ROC)
Best model selection: Highest AUC-PR on validation set

Responsable: Yoset + Dr. Cornejo (review)
Duración: 1 semana
Tools: Optuna, scikit-learn, XGBoost
Output: Best model + hyperparameter report
```

**Tarea 2.2.4: Validación y Documentación**
```
Test metrics required:
├─ AUC-PR ≥ 0.85 (requirement)
├─ F1-Score ≥ 0.78
├─ Precision ≥ 0.85 (minimizar falsos positivos)
├─ Recall ≥ 0.72 (no perder anomalías reales)
└─ Calibration: P(y=1|score=x) well-calibrated

Model Card creado (Mitchell et al. 2018):
├─ Model details (architecture, version)
├─ Intended use (agroexportación peruana)
├─ Evaluation data (28 meses MIDAGRI)
├─ Quantitative analysis (métricas, fairness)
├─ Ethical considerations (sesgos, limitaciones)
└─ Known limitations (datos incompletos, etc)

Responsable: Yoset
Duración: 3 días
Deliverable: model_card_xgboost_v1.0.md
```

**Criterio de éxito del Hito 2**:
- ✅ AUC-PR ≥ 0.85 en test set
- ✅ F1-Score ≥ 0.78
- ✅ Model Card completo y aprobado
- ✅ Modelo serializado (pickle/ONNX)
- ✅ Reproducibilidad documentada (random seed, etc)

---

### 2.3 Semanas 7-8: Detección de Anomalías (Ensemble)

#### Hito 3: Ensemble Entrenado y Benchmarked

**Tarea 2.3.1: Isolation Forest**
```
Propósito: Detectar outliers estadísticos univariados

Config:
├─ n_estimators: 100
├─ contamination: "auto" (0.08, basado en anomalía rate)
├─ random_state: 42

Features:
├─ Price (actual value)
├─ Volume
├─ Temperatura
├─ Precipitación

Evaluación:
├─ Precision ≥ 0.85
├─ Recall ≥ 0.65
└─ F1-Score ≥ 0.73

Responsable: Yoset
Duración: 3 días
```

**Tarea 2.3.2: Local Outlier Factor (LOF)**
```
Propósito: Detectar outliers en contexto local

Config:
├─ n_neighbors: 20
├─ contamination: 0.08
├─ novelty: False (use training samples)

Features:
├─ Price MA-30
├─ Volume MA-30
├─ 3D space: (Price, Volume, Temp)

Evaluación:
├─ Precision ≥ 0.80
├─ Recall ≥ 0.70
└─ F1-Score ≥ 0.74

Responsable: Yoset
Duración: 3 días
```

**Tarea 2.3.3: Deep SVDD (Anomalía profunda)**
```
Propósito: Detectar anomalías en espacio latente

Architecture:
├─ Input: 40 features
├─ Hidden1: 64 neurons (ReLU)
├─ Hidden2: 32 neurons (ReLU)
├─ Latent: 16 neurons (center)
├─ Loss: Deep SVDD objective

Training:
├─ Optimizer: Adam (lr=0.001)
├─ Epochs: 100
├─ Early stopping: patience=10
└─ Data: Train set (80% MIDAGRI 2024-2026)

Evaluación:
├─ Precision ≥ 0.82
├─ Recall ≥ 0.68
└─ F1-Score ≥ 0.74

Responsable: Yoset + TA (PyTorch)
Duración: 1 semana
```

**Tarea 2.3.4: Ensemble Voting**
```
Propósito: Combinar 3 detectores para robustez

Voting Strategy:
├─ Soft voting: Average anomaly scores
├─ Threshold: Score ≥ 0.65 = Anomaly
├─ Confidence: Count votes (1/3, 2/3, 3/3)

Anomaly levels:
├─ LOW (1/3 detectors): Review manual
├─ MEDIUM (2/3 detectors): Alert + report
├─ HIGH (3/3 detectors): Alert + escalate

Calibration:
├─ Threshold tuning en validation set
├─ Target: Precision ≥ 0.88, Recall ≥ 0.72
└─ Confusion matrix analysis

Responsable: Yoset
Duración: 5 días
Deliverable: ensemble_config.yaml
```

**Criterio de éxito del Hito 3**:
- ✅ Ensemble Precision ≥ 0.88 (high trust)
- ✅ Ensemble Recall ≥ 0.72 (no false negatives)
- ✅ Calibration: Well-calibrated probabilities
- ✅ 3 detectors independently validated
- ✅ Production-ready ensemble (serializable)

---

### 2.4 Semana 9: Explicabilidad (SHAP)

#### Hito 4: SHAP Integrado a Predicciones

**Tarea 2.4.1: SHAP Values para XGBoost**
```
Propósito: Explicar cada predicción del GBDT

Implementation:
├─ Explainer: shap.TreeExplainer(xgb_model)
├─ Base value: Expected model output
└─ SHAP values: Feature contribution

Outputs por predicción:
├─ Force plot: Visualización de contributing forces
├─ Waterfall: Cascada de contribuciones
├─ Dependence: Relación variable-SHAP
└─ Summary: Feature importance global

Validación:
├─ Sum of SHAP values ≈ prediction (completitud)
├─ SHAP ≈ LimE (comparación de métodos)
└─ Interpretability checks (features make sense)

Responsable: Yoset
Duración: 3 días
```

**Tarea 2.4.2: SHAP para Ensemble**
```
Propósito: Explicar anomalías detectadas

Strategy:
├─ Ensemble score = avg(IF score, LOF score, DeepSVDD score)
├─ SHAP para DeepSVDD: Deep SHAP (shapley en red)
├─ SHAP para IF: Tree SHAP
├─ Aggregation: Feature importance across 3 detectors

Interpretabilidad:
├─ "Por qué esta observación es anómala?"
├─ "Cuáles features más contribuyeron?"
├─ "Qué hubiera pasado si X variable fuera diferente?"

Responsable: Yoset + TA (Deep SHAP)
Duración: 4 días
```

**Tarea 2.4.3: Anti-alucinación con RAG**
```
Propósito: Asegurar que reportes se basan en hechos

RAG Setup:
├─ Vector DB: FAISS con embeddings OpenAI
├─ Documentos: Datos históricos MIDAGRI + Papers
├─ Retrieval: Top 5 documentos relevantes
└─ Generation: LLM genera reporte con retrieved context

Validation:
├─ Fact checking: Reporte menciona solo valores reales
├─ Citation: Cada hecho traceable a vector original
└─ Coverage: 95%+ de predicciones con hallucination-free

Responsable: Yoset + TA (LangChain)
Duración: 5 días
```

**Criterio de éxito del Hito 4**:
- ✅ SHAP values completitud ≥ 95% (sum ≈ prediction)
- ✅ 100% de predicciones con explicación
- ✅ Explicaciones validadas por supervisor (legibilidad)
- ✅ RAG hallucination rate = 0%
- ✅ Documentación de SHAP values en auditoría

---

### 2.5 Semana 10: Sistema de Reportes

#### Hito 5: Reportes Automáticos + Auditados

**Tarea 2.5.1: Template de Reportes**
```
Reporte structure (1-2 páginas):

┌─────────────────────────────────────┐
│ SUPERVISIÓN OPERATIVA - MAYO 2026   │
│ Generado: 2026-05-15 08:30 UTC      │
│ (Sistema de IA - Revisar antes usar) │
├─────────────────────────────────────┤
│ 1. RESUMEN EJECUTIVO                │
│    • Anomalías detectadas: 3        │
│    • Gravedad promedio: MEDIUM      │
│    • Acción recomendada: Investigar │
├─────────────────────────────────────┤
│ 2. ANOMALÍAS IDENTIFICADAS          │
│    • Anomalía #1: Precio palta      │
│      Valor: USD 3.50/kg             │
│      Promedio: USD 2.80/kg          │
│      Desviación: +25% (alerta)      │
│      Confianza: 95%                 │
│    • Anomalía #2: Volumen berries   │
│      ...                            │
├─────────────────────────────────────┤
│ 3. ANÁLISIS DE CAUSAS (SHAP)        │
│    Anomalía #1 causas:              │
│    • Precio del mes anterior: +45%  │
│    • Humedad SENAMHI: Muy baja      │
│    • Competencia (México): Baja     │
├─────────────────────────────────────┤
│ 4. RECOMENDACIONES                  │
│    • Investigar causa de precio     │
│    • Revisar inventario             │
│    • Comunicar a exportación        │
├─────────────────────────────────────┤
│ 5. AUDITORÍA (Trazabilidad)         │
│    Modelo: XGBoost v1.0             │
│    Datos: MIDAGRI 2024-2026         │
│    Revisado por: [Firma auditor]    │
└─────────────────────────────────────┘
```

**Tarea 2.5.2: Generación LLM**
```
Pipeline:

1. Fetch datos y SHAP:
   anomalies = get_anomalies(date)
   shap_values = get_shap(anomalies)

2. Retrieve contexto (RAG):
   context = rag_retriever.get_context(
       query=f"anomalía en precio {producto}"
   )

3. Prompt engineering:
   prompt = f"""
   Eres auditor agroexportador.
   Anomalía: {anomaly_desc}
   SHAP: {shap_explanation}
   Contexto histórico: {context}
   Escribe análisis en párrafo (máximo 100 palabras).
   """

4. Generate reporte:
   report = llm.generate(prompt, max_tokens=500)

5. Fact-check:
   assert_no_hallucinations(report, context)

6. Output:
   save_pdf(report, anomaly_id)
```

**Tarea 2.5.3: Auditoría y Firma**
```
Workflow de aprobación:

1. Sistema genera reporte (automático)
2. Reporte marcado como "PENDING REVIEW"
3. Auditor notificado (email)
4. Auditor revisa reporte + SHAP
5. Auditor aprueba O rechaza con comentarios
6. Si aprobado: Report publicado
7. Si rechazado: Sistema regenera con feedback

Auditoría Log:
├─ report_id: UUID
├─ generated_at: timestamp
├─ reviewed_by: username
├─ reviewed_at: timestamp
├─ comments: text
├─ status: APPROVED/REJECTED
└─ signed_hash: cryptographic signature
```

**Criterio de éxito del Hito 5**:
- ✅ Reportes generados en <30 segundos
- ✅ ROUGE-L ≥ 0.60 (vs. gold standard)
- ✅ Zero hallucinations (100% fact-checked)
- ✅ 100% de reportes auditados antes de salida
- ✅ Formato consistente y profesional

---

## FASE III: VALIDACIÓN E INTEGRACIÓN (Semanas 11-12)

### 3.1 Semana 11: Testing Integral

**Hito 6: Testing 95%+ Coverage**

#### Tarea 3.1.1: Unit Tests
```
Cobertura requerida: 95%+ líneas de código

Test suites:
├─ test_data_extraction.py: 15 tests
├─ test_feature_engineering.py: 20 tests
├─ test_xgboost_model.py: 25 tests
├─ test_anomaly_detection.py: 20 tests
├─ test_shap_explanations.py: 15 tests
├─ test_report_generation.py: 10 tests
└─ test_audit_log.py: 10 tests
Total: 115 unit tests

Execution:
├─ Framework: pytest
├─ Coverage: pytest-cov (target: 95%)
├─ Continuous integration: GitHub Actions
└─ Time budget: <10 minutos per run
```

#### Tarea 3.1.2: Integration Tests
```
End-to-end scenarios (5 casos):

Test 1: Happy path
├─ Input: Normal price data
├─ Expected: No anomalies, report generated
└─ Assert: Report valid, no errors

Test 2: Anomaly detection
├─ Input: Outlier price (+40%)
├─ Expected: Anomaly detected with 95%+ confidence
└─ Assert: Correct alert level (HIGH)

Test 3: SHAP explanation
├─ Input: Anomalous prediction
├─ Expected: SHAP explains >90% of prediction
└─ Assert: Completitud ≥ 95%

Test 4: Report generation
├─ Input: 3 anomalies from Ensemble
├─ Expected: Report with all 3 explained
└─ Assert: ROUGE-L ≥ 0.60

Test 5: Audit trail
├─ Input: Approved anomaly
├─ Expected: Full audit log created
└─ Assert: Trazabilidad 100% verificable
```

#### Tarea 3.1.3: Stress & Performance
```
Load testing (10K registros procesados):

Benchmarks:
├─ Ingestión de datos: <5 segundos
├─ Feature engineering: <10 segundos
├─ Predicción GBDT: <20 segundos
├─ Detección ensemble: <15 segundos
├─ SHAP explanation: <30 segundos
├─ Generación de reportes: <30 segundos
└─ Total latency: <120 segundos

Concurrency test:
├─ 1000 usuarios simultáneos
├─ 95th percentile latency: <200ms
├─ Error rate: <0.1%
└─ Memory usage: <2GB

Tools: locust, pytest-benchmark
```

### 3.2 Semana 12: Auditoría Regulatoria

**Hito 7: Cumplimiento SBS + D.S.115**

#### Tarea 3.2.1: Validación SBS N° 053-2023
```
Checklist de conformidad:

[x] Trazabilidad verificable
    ├─ Cada predicción mapea a entradas
    ├─ Audit log completo
    └─ Firma criptográfica de auditor

[x] Reproducibilidad documentada
    ├─ Versioning de modelos
    ├─ Dataset lineage
    └─ Hyperparameter logs

[x] Supervisión humana
    ├─ Auditor revisa antes de acción
    ├─ SLA < 24h para aprobación
    └─ Rechazo documentado

[x] Documentación técnica
    ├─ Model Card XGBoost
    ├─ Datasheets para datos
    ├─ Architecture documentation
    └─ Known limitations

Responsable: Yoset + Dr. Cornejo (revisión)
Duración: 3 días
Output: COMPLIANCE-REPORT-SBS.md
```

#### Tarea 3.2.2: Validación D.S. N° 115-2025-PCM
```
Requisitos Ley de IA Perú:

[x] Transparencia
    ├─ Banner: "Generado por sistema IA"
    ├─ Documentación de capacidades
    └─ Limitaciones explícitas

[x] Supervisión humana
    ├─ Workflow requiere aprobación
    ├─ Trazabilidad de aprobaciones
    └─ Escalado a gerencia si necesario

[x] Derechos ciudadano
    ├─ Derecho a explicación (SHAP)
    ├─ Derecho a reconsideración
    └─ Derecho a no ser perfilado

[x] Responsabilidad
    ├─ Identificación clara de operador
    ├─ Contacto para quejas
    └─ Registro de incidentes

Responsable: Yoset + Legal (consultoría)
Duración: 2 días
Output: COMPLIANCE-REPORT-DS115.md
```

---

## FASE IV: DEPLOYMENT Y POST-LANZAMIENTO (Semanas 13-16)

### Semana 13: Capacitación y Deployment

**Tarea 4.1: Documentación de Usuario**
```
Artefactos:
├─ User Guide (5 páginas)
├─ Quick start (2 páginas)
├─ Troubleshooting guide
├─ Video tutorial (15 minutos)
└─ FAQ

Audiencias:
├─ Supervisor operativo
├─ Auditor interno
├─ IT administrator
└─ Ejecutivos
```

**Tarea 4.2: Training**
```
Sessions:
├─ Workshop 1 (2h): Para supervisores
├─ Workshop 2 (2h): Para auditores
├─ Session 3 (1h): Para IT ops
└─ Executive briefing (1h): Para C-level

Topics:
├─ Cómo leer reportes
├─ Cómo revisar anomalías
├─ Cómo escalar (si es necesario)
├─ SLA y supportabilities
└─ Escalation path
```

**Tarea 4.3: Deployment a Producción**
```
Pre-deployment:
├─ Final security audit
├─ Backup del sistema anterior
├─ Rollback plan listo
└─ On-call team designado

Deployment:
├─ Deploy en staging (test definitivo)
├─ Deploy en producción (off-hours si es posible)
├─ Monitoring en tiempo real
└─ First 24h: hourly checks

Post-deployment:
├─ Production monitoring (semana 1)
├─ Hotfix readiness
├─ Daily reports a stakeholders
└─ Iterative improvements
```

### Semanas 14-16: Monitoreo y Mejora Continua

**Tarea 4.4: Monitoring en Producción**
```
Métricas de monitoreo:

System health:
├─ Pipeline uptime: Target ≥99%
├─ Latency p95: Target <100ms
└─ Error rate: Target <0.1%

Model health:
├─ Precision en producción: Monitor vs. baseline
├─ Recall en producción: Monitor vs. baseline
├─ Data drift: Alert si shift en distribución
└─ Model drift: Alert si desempeño degrada

Business metrics:
├─ Adoption rate: % de reportes revisados
├─ False positive rate en producción
├─ Time-to-action (cuánto tarda supervisor en actuar)
└─ ROI impact (mermas reducidas)

Tools: Prometheus + Grafana, DataDog, o similar
Dashboard: Real-time alertas y trends
```

**Tarea 4.5: Iteración y Mejora**
```
Monthly review:
├─ Retrain XGBoost con nuevos datos
├─ Ajustar umbrales de detección si necesario
├─ Incorporar feedback de usuarios
└─ Documentar cambios en Model Card

Quarterly review:
├─ Revisión de business impact
├─ Análisis de fairness (performance por subgrupo)
├─ Roadmap para mejoras mayores
└─ Planning de nueva funcionalidad
```

---

## CRONOGRAMA DE GANTT (Simplificado)

```
              |May15  |May22  |May29  |Jun5   |Jun12  |Jun19  |Jun26  |Jul3   |Jul10  |Jul17  |Jul24  |Jul31  |
              |--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
FASE I        
├─Requisitos  |████████|        |        |        |        |        |        |        |        |        |        |        |
├─Diseño Arq. |        |████████|        |        |        |        |        |        |        |        |        |        |
└─Scope       |████████████████|        |        |        |        |        |        |        |        |        |        |

FASE II       
├─Ingestión   |        |        |████████████████|        |        |        |        |        |        |        |        |
├─Predicción  |        |        |        |████████████████|        |        |        |        |        |        |        |
├─Detección   |        |        |        |        |████████████████|        |        |        |        |        |        |
├─SHAP        |        |        |        |        |        |████████████████|        |        |        |        |        |
└─Reportes    |        |        |        |        |        |        |████████████████|        |        |        |        |

FASE III      
├─Testing     |        |        |        |        |        |        |        |████████████████|        |        |        |
└─Auditoría   |        |        |        |        |        |        |        |        |████████████████|        |        |

FASE IV       
├─Capacit.    |        |        |        |        |        |        |        |        |        |████████████████|        |
└─Monitoreo   |        |        |        |        |        |        |        |        |        |        |████████████████████|
```

---

## HITOS PRINCIPALES Y CRITERIOS DE ÉXITO

| # | Hito | Fecha Objetivo | Criterio de Éxito | Owner |
|---|------|-----------------|-------------------|-------|
| 0 | Scope & Design | 2026-05-22 | Req. doc + Arch doc aprobados | Yoset |
| 1 | Data Ingestion | 2026-05-29 | 100% MIDAGRI, SENAMHI, INEI | Yoset |
| 2 | GBDT Trained | 2026-06-12 | AUC-PR ≥0.85, Model Card listo | Yoset |
| 3 | Anomaly Ensemble | 2026-06-26 | Precision ≥0.88, Recall ≥0.72 | Yoset |
| 4 | SHAP + RAG | 2026-07-03 | Completitud ≥95%, Zero hallucin. | Yoset |
| 5 | Reports Ready | 2026-07-10 | <30s latency, ROUGE-L ≥0.60 | Yoset |
| 6 | Testing 95%+ | 2026-07-17 | 115 unit tests + integration tests | Yoset |
| 7 | Compliance OK | 2026-07-24 | SBS + D.S.115 compliance verified | Yoset + Legal |
| 8 | Prod Deploy | 2026-07-31 | System live, monitoring active | Yoset + Ops |

---

## MATRIZ DE RESPONSABILIDADES (RACI)

| Actividad | Yoset | Dr. Cornejo | Auditor | IT Ops |
|-----------|-------|-----------|---------|--------|
| Requisitos | R/A | C | C | - |
| Diseño Arquitectura | R | A | - | C |
| Desarrollo Componentes | R/A | C | - | - |
| Model Validation | R | A | - | - |
| Testing | R/A | C | - | - |
| Compliance Check | R | A | R | - |
| Deployment | R/A | - | - | C |
| Training | R | - | A | - |
| Production Support | R | - | - | A |

R = Responsible (hace el trabajo)  
A = Accountable (final decisión)  
C = Consulted (input)  
I = Informed (notificación)

---

## RIESGOS Y MITIGACIÓN

| Risk | Probab. | Impact | Mitigation |
|------|---------|--------|-----------|
| Calidad MIDAGRI data | Media | Alto | Validación manual, backups |
| Sesgo en entrenamiento | Alta | Medio | Fairness testing, subgroup analysis |
| Hallucinations en LLM | Media | Alto | RAG + fact-checking, human review |
| Compliance delay | Baja | Alto | Early engagement con SBS, legal review |
| Production performance | Baja | Alto | Load testing, monitoring, rollback ready |

---

## BUDGET Y RECURSOS

### Personal Requerido:
- 1 ML Engineer (Yoset) - Tiempo completo 12 semanas
- 1 Senior Advisor (Dr. Cornejo) - 5 horas/semana
- 1 QA Tester (TA) - 2 semanas (testing phase)
- 1 IT Ops - 1 semana (deployment phase)

### Herramientas:
- Cloud: AWS/Azure (~USD 2,000)
- APIs: OpenAI/Cohere (~USD 500)
- Licenses: GitHub, Jira, Slack (~USD 100)

**Total investment**: USD 73,000 development + USD 2,600 tools = **USD 75,600**

---

## CONCLUSIÓN

Este plan detallado proporciona:
✅ Roadmap claro de 12 semanas  
✅ Hitos mensurables y criterios de éxito definidos  
✅ Asignación clara de responsabilidades  
✅ Risk mitigation proactiva  
✅ Cumplimiento regulatorio integrado desde el inicio  

**Next step**: Kickoff meeting semana 15-17 Mayo para validar scope y recursos.

---

**Preparado por**: Yoset Cozco Mauri  
**Aprobado por**: Dr. Víctor Manuel Cornejo Aparicio  
**Fecha**: Mayo 15, 2026  
**Versión**: 2.0 Final  

