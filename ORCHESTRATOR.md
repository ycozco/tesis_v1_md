# MAPA DE ORQUESTACIÓN Y EXPLICABILIDAD DE CÓDIGO
## Sistema Integrado de Supervisión con IA Explicable
### Tesis UNSA — Yoset Cozco Mauri (2026)

Este documento detalla el plan de ordenamiento, la estructura de directorios y el funcionamiento del **Orquestador Maestro (`orchestrator.py`)**, diseñado para proveer **trazabilidad, explicabilidad e inmutabilidad** al pipeline completo de la tesis, vinculando el código de Python con los capítulos de resultados científicos.

---

```mermaid
flowchart TD
    subgraph Capa de Datos (ETL y Preparación)
        A1[Ficheros DBF SUNAT] -->|etl_real_data.py| A2[dataset_real_v1.csv]
        A2 -->|preprocess_data.py| A3[Parquet Limpios y Normalizados]
    end

    subgraph Capa de Modelamiento e IA (Capas 1-6)
        A3 -->|Capa 1: Predicción| B1[module1_prediction.py]
        B1 -->|Capa 2: Anomalías| B2[module2_anomaly.py]
        B2 -->|Capa 3: TreeSHAP| B3[module3_shap.py]
        B3 -->|Capa 4: RAG & Reportes| B4[module4_rag.py]
        B4 -->|Capa 5: Validación Factual| B5[module5_validation.py]
        B5 -->|Capa 6: Trazabilidad| B6[module6_traceability.py]
    end

    subgraph Orquestador y Reportabilidad
        B6 -->|Generación de Metadatos| ORC[Orquestador Central]
        ORC -->|Salida Firmada| TRACE[pipeline_trace.json]
        ORC -->|Actualización Automática| CHAP4[Capítulo IV: Resultados]
    end
```

---

## 1. Estructura y Ordenamiento del Código Python

Para facilitar la trazabilidad y la lectura del jurado, los scripts de Python del proyecto se categorizan en cuatro bloques funcionales:

### A. Extracción e Ingesta de Datos (ETL)
*   **[etl_real_data.py](file:///d:/tesis_yoset/src/etl_real_data.py)**: Descarga programática de paquetes semanales ZIP de SUNAT, descompresión y lectura de archivos DBF, mapeo de aduanas y filtrado de partidas agroexportadoras.
*   **[scrape_sunat_all.py](file:///d:/tesis_yoset/src/scrape_sunat_all.py)**: Web scraping de contingencia de datos aduaneros complementarios.
*   **[parse_trademap.py](file:///d:/tesis_yoset/src/parse_trademap.py)**: Parseador de datos de comercio internacional de Trade Map para benchmark.

### B. Preparación y Calidad (Preprocessing)
*   **[preprocess_data.py](file:///d:/tesis_yoset/limpieza_de_datos_y_normalizacion/preprocess_data.py)**: Imputación de nulos, escalamiento robusto, partición temporal estricta de series (Desarrollo/Prueba) para evitar fugas de información (*data leakage*).
*   **[eda_calidad.py](file:///d:/tesis_yoset/src/eda_calidad.py)**: Auditoría de la calidad de datos y consistencia estadística de las variables.
*   **[feature_engineering.py](file:///d:/tesis_yoset/src/feature_engineering.py)**: Creación de rezagos (*lags*), medias móviles, indicadores climáticos exógenos y ciclicidad temporal (seno/coseno).

### C. Núcleo IA de 6 Capas (Core Pipeline)
*   **[module1_prediction.py](file:///d:/tesis_yoset/src/module1_prediction.py)**: **Capa 1 (Predicción Tabular)**. Entrena XGBoost/LightGBM optimizados con Optuna para predecir precio FOB y volumen, inyectando los residuos robustos normalizados.
*   **[module2_anomaly.py](file:///d:/tesis_yoset/src/module2_anomaly.py)**: **Capa 2 (Ensemble de Anomalías)**. Corre Isolation Forest, LOF y ECOD, y calcula el score de consenso unificado (Ensemble PyOD).
*   **[module3_shap.py](file:///d:/tesis_yoset/src/module3_shap.py)**: **Capa 3 (Explicabilidad SHAP)**. Calcula atribuciones TreeSHAP sobre las anomalías detectadas para identificar factores causales (precio, volumen, clima, retraso logístico).
*   **[module4_rag.py](file:///d:/tesis_yoset/src/module4_rag.py)**: **Capa 4 (RAG & Reportes)**. Integra el contexto SHAP y las bases normativas para generar reportes textuales estructurados y accionables mediante LLM.
*   **[module5_validation.py](file:///d:/tesis_yoset/src/module5_validation.py)**: **Capa 5 (Validación Factual)**. Evalúa la completitud e integridad de los reportes generados contra la base de datos (con métricas de consistencia numérica y alucinación).
*   **[module6_traceability.py](file:///d:/tesis_yoset/src/module6_traceability.py)**: **Capa 6 (Registro de Trazabilidad e Integridad)**. Genera hashes SHA-256 de todas las entradas/salidas, garantizando la inmutabilidad y auditoría de la cadena de inferencia.

### D. Utilitarios de Soporte y Compilación
*   **[compile_thesis.py](file:///d:/tesis_yoset/scripts/compile_thesis.py)**: Genera y compila los borradores `.md` de la tesis hacia formatos PDF/Word mediante Pandoc.
*   **[auditar_referencias.py](file:///d:/tesis_yoset/scripts/auditar_referencias.py)**: Valida la consistencia cruzada de citas bibliográficas.
*   **[app.py](file:///d:/tesis_yoset/src/app.py)**: Servidor Flask interactivo que levanta el "Tesis Hub".

---

## 2. Mapa Detallado del Core Pipeline (Capas 1-6)

A continuación se define la firma de ejecución y flujo de datos de las 6 capas integradas:

| Capa | Script Python | Datos de Entrada | Datos de Salida | Métricas y Trazabilidad Registrada |
| :--- | :--- | :--- | :--- | :--- |
| **Capa 1** | `module1_prediction.py` | `data/gold/prediction_features.parquet` | `data/gold/anomaly_features.parquet` | Error Medio Absoluto (MAE), $R^2$, Hiperparámetros Optuna, Hash del modelo `.pkl` |
| **Capa 2** | `module2_anomaly.py` | `data/gold/anomaly_features.parquet` | `data/gold/anomaly_metrics.json` | PR-AUC, ROC-AUC, F1, Recall por tipo de anomalía, Semillas probadas |
| **Capa 3** | `module3_shap.py` | `data/gold/anomaly_features.parquet` | `data/gold/local_explanations.json` | Atribuciones base, Importancia global de características, JSON de explicaciones locales |
| **Capa 4** | `module4_rag.py` | `data/gold/local_explanations.json` | `data/gold/generated_reports.json` | UUID por reporte, Prompts contextuales, Texto RAG final generado |
| **Capa 5** | `module5_validation.py` | `data/gold/generated_reports.json` | `data/gold/validation_metrics.json` | Puntuación de fidelidad de datos (Fidelity), Completitud (Completeness), Coherencia |
| **Capa 6** | `module6_traceability.py`| Todo el flujo anterior | `data/gold/traceability_log.json` | Hashes SHA-256 de base de datos, modelos, reportes y log de auditoría completo |

---

## 3. Orquestador Maestro (`orchestrator.py`)

El orquestador centraliza la ejecución del pipeline y proporciona metadatos interactivos de la tesis.

### Interfaz CLI:
*   `python orchestrator.py --list`: Muestra la explicación interactiva de cada módulo Python.
*   `python orchestrator.py --check`: Valida la integridad física de los archivos y dependencias.
*   `python orchestrator.py --run [capas/all]`: Ejecuta secuencialmente los módulos indicados, genera el log unificado de trazabilidad en JSON y actualiza automáticamente los borradores de tablas del Capítulo IV.
