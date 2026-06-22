# CAPÍTULO III: ELABORACIÓN DE LA PROPUESTA

## 3.1 Generalidades

### 3.1.1 Propósito
El propósito del sistema inteligente de supervisión agroexportadora es proveer una plataforma unificada para detectar desviaciones operativas y aduaneras en exportaciones peruanas de palta, uva y arándano. El sistema apoya a los encargados de control y analistas en la toma de decisiones informadas mediante la estimación de valores esperados, detección de anomalías multivariables, explicaciones locales SHAP y generación automática de reportes técnicos trazables RAG.

### 3.1.2 Usuarios del Sistema
1.  **Analista de Control Operativo:** Revisa alertas, explora las variables incidentes mediante SHAP e inicia solicitudes de auditoría.
2.  **Supervisor de Operaciones / Auditor Interno:** Encargado de la firma de conformidad de los reportes. Valida y autoriza acciones correctivas.
3.  **Administrador de Datos / Ingeniero de ML:** Monitorea la calidad de datos, el linaje, el ajuste de los modelos y el reentrenamiento.
4.  **Investigador / Usuario Académico:** Analiza patrones históricos de mermas, clima o comportamiento de mercado agregados.

### 3.1.3 Entradas
*   Registros transaccionales de aduanas parseados de SUNAT/ADUANET (formato DBF/CSV).
*   Series de tiempo diarias y mensuales del tipo de cambio PEN/USD de la API o caches de BCRP.
*   Series de tiempo mensuales de precios y volúmenes mayoristas nacionales de SISAP (MIDAGRI).
*   Proxies climáticos semanales de temperatura, humedad y lluvias acumuladas de NASA POWER.
*   Proxies de alertas fitosanitarias mensuales de SENASA y la FDA.
*   Configuraciones en YAML para productos arancelarios, modelos e inyección de anomalías.

### 3.1.4 Salidas
*   Predicciones puntuales de valor unitario FOB y volumen exportado para la semana $t+1$.
*   Scores consolidados de anomalías y alertas clasificadas por severidad (`BAJA`, `MEDIA`, `ALTA`).
*   Visualizaciones y mapas de atribución locales SHAP (PNG/SVG) de las variables predictivas.
*   Informes narrativos en markdown validados factual y numéricamente (con linaje SHA-256).
*   Base de datos de auditoría de trazabilidad en JSON/DuckDB.
*   Dashboard interactivo web de visualización en Streamlit/Flask.

### 3.1.5 Requisitos Funcionales

*   **RF-01 (Importar Datos):** Permitir la ingesta de archivos DBF, CSV y Parquet de las fuentes de origen.
*   **RF-02 (Validar Datos):** Verificar tipos de datos, códigos arancelarios válidos a 10 dígitos y países normalizados ISO alfa-3.
*   **RF-03 (Normalizar y Anonimizar):** Homologar escalas de peso (kg) y valor (USD), y anonimizar exportadores con hashes SHA-256 salteados.
*   **RF-04 (Agregar Semanalmente):** Agrupar y consolidar transacciones por combinación `producto × mercado × semana ISO`.
*   **RF-05 (Entrenar Modelos):** Ajustar de forma global algoritmos XGBoost y LightGBM con búsqueda de hiperparámetros en Optuna.
*   **RF-06 (Predecir FOB y Volumen):** Generar las estimaciones puntuales de valor unitario FOB y volumen para la semana $t+1$.
*   **RF-07 (Detectar Anomalías):** Calcular los percentiles de Isolation Forest, LOF y ECOD, y generar alertas si se cruzan los umbrales.
*   **RF-08 (Explicar con SHAP):** Estimar las contribuciones locales TreeSHAP de las variables predictoras sobre la desviación de la alerta.
*   **RF-09 (Recuperar Contexto):** Buscar y recuperar fragmentos semánticos en el corpus RAG mediante indexado híbrido (BM25 y embeddings).
*   **RF-10 (Reportar con LLM):** Generar el reporte en markdown estructurado inyectando evidencias cuantitativas y textos recuperados.
*   **RF-11 (Validar Reporte):** Analizar sintácticamente el texto del reporte y rechazarlo ante discrepancias numéricas superiores al 0.5%.
*   **RF-12 (Consultar Trazabilidad):** Permitir la reconstrucción de la alerta ingresando su identificador UUID (`alert_id`).
*   **RF-13 (Revisar Alertas):** Proveer filtros en la interfaz por producto, mercado, semana y nivel de severidad.
*   **RF-14 (Exportar Resultados):** Permitir la descarga de reportes markdown firmados y tablas de métricas del pipeline.

### 3.1.6 Requisitos No Funcionales
*   **Reproducibilidad:** Fijación de semillas aleatorias globales (`42`) y secundarias en todos los modelos e inyección de datos.
*   **Auditabilidad:** Inmutabilidad mediante hashes SHA-256 registrados para cada entrada de datos, configuraciones, modelos y salidas.
*   **Rendimiento:** Tiempos de inferencia combinada por registro en la escala de milisegundos en CPU de uso general.
*   **Modularidad:** Arquitectura modular monolítica desacoplada mediante scripts independientes para ingesta, modelamiento y reporte.
*   **Usabilidad:** Interfaz interactiva fluida con directrices estéticas premium (vibrant dark mode y visualizaciones simplificadas).
*   **Privacidad:** Anonimización irreversible de los identificadores comerciales de exportadores.

### 3.1.7 Restricciones
*   **Procesamiento por Lotes (Batch):** El sistema está acotado a ejecuciones programadas semanales, excluyendo telemetría en tiempo real.
*   **Soporte Consultivo:** El sistema provee soporte a la decisión humana, no autoriza bloqueos automáticos en aduanas ni reemplaza firmas.
*   **Variables Proxies:** Variables críticas como mermas, costos logísticos o riesgos sanitarios se declaran conceptualmente como estimaciones o proxies, no mediciones directas.

### 3.1.8 Principios de Diseño
1.  **Separación de Responsabilidades:** Desacoplamiento estricto del cálculo cuantitativo frente a la redacción narrativa del LLM.
2.  **Evidencia Primero:** El prompt del modelo de lenguaje se restringe exclusivamente a las evidencias cuantitativas inyectadas.
3.  **Human-in-the-Loop:** Cada alerta y reporte requiere revisión y firma del supervisor humano antes de su registro oficial.
4.  **Trazabilidad:** Cada elemento del sistema hereda y propaga el linaje de identificadores y hashes.
5.  **Control Factual:** Rechazo sistemático de reportes con discrepancias numéricas.
6.  **Mínimo Privilegio:** Restricción de permisos y control de acceso local a los datos brutos de aduana.

### 3.1.9 Tecnologías Implementadas
*   *Lenguaje de programación:* Python (versión 3.11.x).
*   *Análisis y manipulación de datos:* Pandas, Numpy, PyArrow (formato Parquet).
*   *Algoritmos de ML y Anomalías:* XGBoost, LightGBM, PyOD (Isolation Forest, LOF, ECOD), Scikit-Learn, Optuna.
*   *Explicabilidad:* SHAP (TreeSHAP).
*   *RAG e Indexado:* Rank-BM25, Sentence-Transformers (`paraphrase-multilingual-MiniLM-L12-v2`).
*   *Servicios y Dashboard:* Flask / Streamlit, Jinja2, HTML5/CSS3 (estilo premium).
*   *Persistencia:* Parquet para almacenamiento analítico y archivos JSON para trazabilidad y configuraciones.

### 3.1.10 Arquitectura de Componentes (Mermaid)

```mermaid
graph TD
    subgraph Capa_Datos [Capa de Datos y ETL]
        A[SUNAT raw DBF] -->|parse_sunat_dbf.py| B[Bronze Parquet]
        C[BCRP + SISAP CSV] -->|integrate_proxies.py| D[Silver Parquet]
        B & D -->|prepare_weekly_dataset.py| E[Gold weekly_product_market.parquet]
    end

    subgraph Capa_Modelado [Capa Analítica y de Modelado]
        E -->|feature_engineering.py| F[Prediction Features]
        F -->|module1_prediction.py| G[GBDT Models: XGB/LGBM]
        G -->|Cálculo de Residuos| H[Anomaly Features]
        H -->|module2_anomaly.py| I[PyOD Ensemble: IF+LOF+ECOD]
        I -->|module3_shap.py| J[TreeSHAP Explanations]
    end

    subgraph Capa_Servicios [Capa de Reportes y Servicios RAG]
        I & J -->|Evidencia JSON| K[module4_rag.py: LLM RAG Generator]
        L[Knowledge Base Markdown] -->|Búsqueda Híbrida BM25+Embeddings| K
        K -->|Draft Report| M[module5_validation.py: Factual Validator]
        M -->|Validación Factual| N[Final Report Markdown]
        N -->|module6_traceability.py| O[Traceability Log JSON]
    end

    subgraph Interfaz_Usuario [Capa de Visualización y Dashboard]
        O -->|Visualización de Alertas y Linaje| P[app.py: Flask Dashboard]
    end
```

## 3.2 Esquema de la Propuesta

### 3.2.1 Flujo General de Datos

```mermaid
sequenceDiagram
    autonumber
    participant SUNAT as SUNAT aduanas
    participant ETL as ETL & Agregación
    participant Models as Predicción & Residuos
    participant PyOD as Ensemble Outliers
    participant SHAP as TreeSHAP
    participant RAG as RAG & LLM
    participant Val as Validador Factual
    participant Log as Traceability Log

    SUNAT->>ETL: Enviar registros transaccionales
    ETL->>ETL: Agrupar por producto-mercado-semana ISO
    ETL->>Models: Dataset gold e ingeniería de lags
    Models->>Models: Entrenar XGBoost/LightGBM global
    Models->>PyOD: Residuos robustos y características
    PyOD->>PyOD: Calcular percentiles consolidados
    PyOD->>SHAP: Gatillar alerta (score >= 0.95)
    SHAP->>SHAP: Calcular contribución local de variables
    SHAP->>RAG: Enviar evidencia (valores, SHAP, metadatos)
    RAG->>RAG: Recuperar documentos contextuales
    RAG->>RAG: Redactar reporte en markdown
    RAG->>Val: Enviar reporte de revisión
    alt Reporte válido (error <= 0.5%)
        Val->>Log: Guardar reporte y registrar hash SHA-256
    else Reporte inválido (error > 0.5%)
        Val->>RAG: Solicitar corrección (máx 1 intento)
        alt Corrección fallida
            Val->>Log: Generar reporte determinista con TemplateProvider y registrar
        end
    end
    Log->>Log: Retornar alert_id y confirmar trazabilidad
```

### 3.2.2 Esquema y Capas de Datos
*   **Raw:** Datos crudos originales descargados sin procesar (formatos DBF de SUNAT y CSVs de SISAP/BCRP).
*   **Bronze:** Transformación inicial uno-a-uno a formato estructurado de alto rendimiento (Parquet) sin alterar campos.
*   **Silver:** Limpieza de nulos, homologación de códigos arancelarios a 10 dígitos, normalización de países ISO alfa-3, y anonimización de exportadores con hashes criptográficos. Exclusión sistemática de cacao.
*   **Gold:** Cuadrícula temporal de agregación semanal de combinación única `product_code`, `market_aggregated`, `week_start`. Generación de lags, rolling statistics y características cíclicas calendario.

### 3.2.3 Unidad de Análisis
*   Definición metodológica única y obligatoria: la combinación de **producto × mercado de destino × semana ISO** iniciada en la fecha `week_start`.
*   Unidad de registro en los archivos analíticos de entrada a los modelos: cada fila describe el comportamiento acumulado de una subpartida arancelaria para un mercado específico durante una semana ISO (lunes a domingo).

### 3.2.4 Variables Objetivo
*   **FOB Unitario Promedio Semanal ($t+1$):**
    $$Y_{FOB}(t+1) = \frac{\sum \text{FOB\_USD}_{t+1}}{\sum \text{Net\_Weight\_kg}_{t+1}}$$
*   **Volumen Neto Semanal ($t+1$):**
    $$Y_{Vol}(t+1) = \sum \text{Net\_Weight\_kg}_{t+1}$$

### 3.2.5 Integración de Fuentes Exógenas
*   *Tipo de cambio (BCRP):* Mapeado semanalmente a través del mes de la fecha `week_start`.
*   *Precios internos (SISAP):* Incorporados semanalmente mediante correspondencia de producto.
*   *Clima regional (NASA):* Agregado semanalmente y desplazado en una semana (`lag1`) para representar la información disponible al cierre de la semana de predicción.

### 3.2.6 Ingeniería de Características (Prevención de Data Leakage)
Todas las variables de predicción correspondientes a estadísticas móviles (`rolling mean`, `rolling std`, `rolling mad`) y variaciones porcentuales se calculan desplazando los datos observados en una semana (`shift(1)`). Esto asegura que ninguna información correspondiente a la semana $t+1$ o posterior se filtre en el conjunto de entrenamiento de la semana $t$.

### 3.2.7 Modelamiento Predictivo Global
Se entrena un único modelo global de regresión multivariable (un modelo para valor unitario FOB y otro para volumen) para todos los productos y mercados seleccionados, incorporando las características categóricas codificadas mediante One-Hot Encoding. La optimización de hiperparámetros se realiza mediante Optuna sobre el split de validación temporal.

### 3.2.8 Cálculo de Residuos Robustos
Los detectores de anomalías se alimentan de los residuos de predicción fuera de muestra (predicciones OOF generadas mediante validación temporal cruzada). El residuo se escala mediante robust-z score móvil:
$$\text{residual\_robust\_z} = \frac{\text{residuo}(t) - \text{mediana}(\text{residuos}_{t-13..t-1})}{\text{MAD}(\text{residuos}_{t-13..t-1})}$$

### 3.2.9 Ensemble de Anomalías y Percentiles
Las puntuaciones crudas de Isolation Forest, LOF y ECOD se calibran en la distribución del conjunto de entrenamiento para transformarlas a percentiles acotados en el rango $[0, 1]$. El ensemble consolida las puntuaciones promediándolas y gatilla la alerta si se supera el percentil 95.

### 3.2.10 Explicabilidad SHAP y Atribución local
TreeSHAP se aplica sobre los regresores globales de GBDT entrenados para calcular las contribuciones marginales locales de cada característica. El sistema extrae el top-5 de variables que empujaron positivamente la predicción esperada y el top-5 que la redujeron, inyectándolos en el prompt de la alerta.

### 3.2.11 RAG con Validador Factual
El motor RAG recupera información metodológica y limitaciones del corpus documental de `knowledge_base/`. El LLM recibe las evidencias de la alerta y redacta el reporte técnico. El validador determinista realiza un análisis numérico mediante expresiones regulares, comparando los números del reporte contra el JSON de entrada, cayendo en `TemplateProvider` ante discrepancias persistentes.

### 3.2.12 Trazabilidad de Auditoría

```mermaid
classDiagram
    class IngestionRun {
        +String ingestion_run_id
        +String dataset_version_id
        +String sunat_source_hash
        +DateTime timestamp
    }
    class ModelRun {
        +String model_version_id
        +String dataset_version_id
        +String model_parameters_hash
        +Float mae_fob_val
        +Float rmsle_vol_val
    }
    class AlertLog {
        +String alert_id
        +String model_version_id
        +String product_code
        +String market_aggregated
        +DateTime week_start
        +Float ensemble_score
        +String severity
    }
    class ExplanationLog {
        +String explanation_id
        +String alert_id
        +List top_k_shap_variables
        +String shap_plot_path
    }
    class ReportLog {
        +String report_id
        +String alert_id
        +String explanation_id
        +String report_text_hash
        +Boolean is_factual_valid
        +String template_used
    }

    IngestionRun --> ModelRun : "alimenta"
    ModelRun --> AlertLog : "evalúa y detecta"
    AlertLog --> ExplanationLog : "explica"
    ExplanationLog --> ReportLog : "documenta"
```

### 3.2.13 Seguridad y Privacidad
El sistema opera localmente y no expone datos aduaneros crudos al exterior. Los identificadores fiscales (RUC) y nombres de las empresas exportadoras se anonimizan de manera irreversible mediante algoritmo criptográfico SHA-256 con sal fija:
$$\text{exporter\_hash} = \text{SHA256}(\text{RUC} + \text{salt\_salt\_42})$$
Las claves de API de los LLMs se cargan mediante variables de entorno estrictamente privadas en el archivo `.env`.

### 3.2.14 Esquema de Despliegue Local

```mermaid
graph LR
    subgraph Servidor_Local [Servidor Local / Entorno Virtual]
        A[SQLite / DuckDB Metadata] <--> B[FastAPI Backend / App Logic]
        C[Parquet/JSON Gold Store] <--> B
        D[Model Binaries .joblib] --> B
        B <--> E[Streamlit / Flask Dashboard]
    end

    subgraph Clientes [Clientes de Red Local]
        E <--> F[Navegador Analista]
        E <--> G[Navegador Supervisor]
    end
```

## 3.3 Obtención y Preparación de Datos

La preparación de datos se organiza como un flujo reproducible por capas. Esta estructura evita mezclar archivos crudos, datos intermedios, resultados experimentales y evidencias finales. La unidad de análisis se mantiene constante en todo el proceso: producto agroexportador, mercado de destino y semana ISO.

### 3.3.1 Fuentes de datos y estado de uso

| Fuente | Ruta o evidencia | Uso en la tesis | Estado |
|---|---|---|---|
| SUNAT/ADUANET | `data/raw/`, `data/sunat/` | Base transaccional aduanera para exportaciones | Parcial, sujeta a depuración y versionado |
| TradeMap | `data-trademap/` | Contraste internacional y contexto de mercado | Parcial |
| BCRP/SISAP/MIDAGRI | `data/` y scripts de integración | Variables exógenas de precio, tipo de cambio y contexto interno | Parcial |
| Dataset analítico | `data/gold/weekly_product_market.parquet` | Entrada esperada para predicción y detección | En validación |
| Prototipo funcional | `sistema-web-agro/backend/init_db.py` | Datos semilla para validar flujo de interfaz y telemetría | Implementado como prototipo |

Los datos semilla del prototipo no sustituyen al dataset final de investigación. Se usan para demostrar integración funcional de backend, frontend, alertas, explicaciones, reportes y telemetría. Los resultados finales deberán provenir del dataset semanal reproducible y documentado.

### 3.3.2 Capas de procesamiento

| Capa | Descripción | Evidencia esperada |
|---|---|---|
| Raw | Archivos originales sin transformación metodológica | Hash de origen, fecha de descarga, ruta cruda |
| Bronze | Conversión estructural a formatos tabulares/parquet | Script de extracción y conteo de registros |
| Silver | Limpieza, normalización, homologación y anonimización | Diccionario de datos y reporte de calidad |
| Gold | Agregación semanal por producto-mercado-semana | Dataset final, hash, versión y pruebas |
| Features | Variables predictivas, rezagos y ventanas móviles | Matriz de entrenamiento y prueba de fuga |
| Evidence | Métricas, residuos, alertas, explicaciones y reportes | Artefactos en `reports/tesis/` |

### 3.3.3 Controles de calidad temporal

Para prevenir fuga de información, las variables predictivas solo deben utilizar información disponible antes de la semana objetivo. Los rezagos, medias móviles y desviaciones móviles se calculan con desplazamiento explícito de una semana. Los escaladores, codificadores y selectores de características se ajustan únicamente con el conjunto de entrenamiento. La partición temporal se congela antes de entrenar los modelos definitivos.

| Control | Regla de aceptación | Estado actual |
|---|---|---|
| Rezagos y ventanas | Toda ventana móvil usa `shift(1)` antes del objetivo | Parcial, requiere prueba automatizada final |
| Escaladores/codificadores | Ajuste solo en entrenamiento | Pendiente de evidencia definitiva |
| Selección de características | Sin acceso al conjunto de prueba | Pendiente |
| Predicciones fuera de muestra | Residuos generados con validación temporal | Pendiente para dataset final |
| Reporte de fuga | Guardar en `reports/tesis/data-quality/leakage-tests/` | Pendiente si no existe ejecución |

### 3.3.4 Registro de artefactos experimentales

Cada corrida experimental debe registrar identificador único, commit, dataset, semilla, configuración, hiperparámetros, entorno, métricas globales, métricas por producto, predicciones, residuos y hashes de salida. Hasta que esos campos existan, el artefacto se clasifica como preliminar o pendiente, no como definitivo.

## 3.4 Diseño e Implementación del Prototipo

El prototipo funcional se encuentra en `sistema-web-agro/`. Su propósito es demostrar la integración de los componentes de supervisión aduanera con IA explicable, no cerrar por sí solo la validación estadística final de la tesis.

### 3.4.1 Estructura técnica del prototipo

| Componente | Ruta | Función | Estado |
|---|---|---|---|
| Backend Flask | `sistema-web-agro/backend/app.py` | API de alertas, configuración, telemetría y reportes | Implementado |
| Modelos de datos | `sistema-web-agro/backend/models.py` | Entidades de alerta, decisión, usuario y documentos | Implementado |
| Semilla de base | `sistema-web-agro/backend/init_db.py` | Carga de datos de prueba y configuración inicial | Implementado |
| Frontend React | `sistema-web-agro/frontend/src/` | Interfaz de auditoría, detalle, telemetría e integridad | Implementado |
| Despliegue local | `sistema-web-agro/docker-compose.yml`, `run.ps1` | Orquestación local del prototipo | Implementado |
| Evidencia visual | `sistema-web-agro/*/screen.png` | Capturas de pantallas funcionales | Disponible |

### 3.4.2 Vistas funcionales del prototipo

El prototipo incluye vistas para autenticación, panel del auditor, gestión de alertas, detalle de operación con IA explicable, historial, telemetría, integridad, exploración de datos, configuración de modelo y control de usuarios. La vista de detalle de alerta concentra la integración de predicción, score de anomalía, explicación SHAP, reporte RAG y decisión humana.

| Vista | Ruta esperada | Evidencia |
|---|---|---|
| Login | `/login` | `frontend/src/pages/Login.jsx` |
| Dashboard | `/dashboard` | `frontend/src/pages/Dashboard.jsx` |
| Alertas | `/alerts` | `frontend/src/pages/Alerts.jsx` |
| Detalle de alerta | `/alerts/:id` | `frontend/src/pages/Detail.jsx`, `AuditDetail.jsx` |
| Historial | `/history` | `frontend/src/pages/History.jsx` |
| Telemetría | `/telemetry` | `frontend/src/pages/Telemetry.jsx` |
| Integridad | `/integrity` | `frontend/src/pages/Integrity.jsx` |
| Datos/RAG | `/data` | `frontend/src/pages/Data.jsx` |
| Configuración | `/config` | `frontend/src/pages/Config.jsx` |
| Usuarios | `/users` | `frontend/src/pages/Users.jsx` |

### 3.4.3 Algoritmos propuestos e implementación vinculada

| Módulo | Algoritmo o técnica | Función | Evidencia |
|---|---|---|---|
| Predicción | XGBoost/LightGBM, GBDT | Estimar FOB unitario y volumen esperado | `src/module1_prediction.py`, prototipo backend |
| Detección de anomalías | Isolation Forest, LOF, ECOD | Calcular score anómalo individual y ensemble | `src/module2_anomaly.py`, `backend/app.py` |
| Explicabilidad | TreeSHAP/SHAP | Atribuir variables que impulsan el riesgo | `src/module3_shap.py`, vista de detalle |
| Reportes automáticos | RAG con recuperación documental y plantilla determinística | Generar narrativa técnica anclada a evidencia | `src/module4_rag.py`, `src/module5_validation.py` |
| Validación factual | Reglas determinísticas y comparación numérica | Rechazar cifras no sustentadas | `src/module5_validation.py` |
| Trazabilidad | Hashes, IDs, logs y relaciones alerta-decisión | Auditar evidencia de extremo a extremo | `src/module6_traceability.py`, modelos del backend |

En el estado actual, el prototipo respalda la arquitectura, las rutas funcionales, la telemetría y la experiencia de auditoría. La validación cuantitativa definitiva sigue condicionada al dataset semanal final, a las pruebas de fuga de información y a los experimentos formales.

## 3.5 Diseño Experimental y Validación

La validación se plantea en cinco bloques: rendimiento predictivo y detección, explicabilidad, calidad de reportes, usabilidad y trazabilidad. Cada bloque debe producir evidencia reproducible antes de ser incorporado como resultado definitivo en el Capítulo IV.

### 3.5.1 Validación de predicción y anomalías

La comparación principal evalúa el ensemble IF + LOF + ECOD frente a detectores individuales y baselines. Las métricas previstas son Precision, Recall, F1, PR-AUC, ROC-AUC y Precision@k. Cuando se usen anomalías sintéticas, se debe registrar tipo, magnitud, proporción de inyección y etiqueta generada.

### 3.5.2 Validación de explicabilidad

SHAP se evalúa por cobertura top-k, estabilidad de atribuciones, coherencia con variables disponibles y claridad para el auditor. Las atribuciones se interpretan como contribuciones del modelo, no como causalidad empresarial.

### 3.5.3 Validación de reportes automáticos

Los reportes se validan con una rúbrica de completitud, coherencia, fidelidad factual y consistencia numérica. Cada cifra citada en el reporte debe existir en evidencia estructurada. Si el reporte RAG no supera la validación, se registra rechazo y se genera una versión determinística.

### 3.5.4 Evaluación controlada con usuarios

El estudio de usabilidad compara una condición integrada, con SHAP y RAG visibles, frente a una condición aislada, sin explicaciones avanzadas. Las métricas son tiempo de análisis, decisión registrada, comprensión percibida y utilidad. Hasta contar con participantes reales y consentimiento documentado, esta sección permanece como diseño experimental y no como resultado concluyente.

### 3.5.5 Puertas de control

| Puerta | Criterio | Estado actual |
|---|---|---|
| A. Datos | Dataset semanal reproducible, documentado, versionado y sin duplicidad de clave | Parcial |
| B. Implementación | Cada módulo con ruta, entrada, salida, configuración, prueba y evidencia | Parcialmente aprobado por prototipo |
| C. Experimento | Split temporal, métricas, semillas y criterios congelados | Pendiente |
| D. Capítulo III | Arquitectura e implementación documentadas sin resultados finales | En desarrollo |
| E. Capítulo IV preliminar | Resultados reproducibles y claramente marcados como preliminares o definitivos | Parcial |

---

