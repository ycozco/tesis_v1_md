# MAPA DE ORQUESTACIÓN Y EXPLICABILIDAD DE CÓDIGO
## Sistema Integrado de Supervisión con IA Explicable
### Tesis UNSA — Yoset Cozco Mauri (2026)

Este documento detalla el plan de ordenamiento completo, la estructura de directorios final y el funcionamiento del **Orquestador Maestro (`orchestrator.py`)**, diseñado para proveer **trazabilidad, explicabilidad e inmutabilidad** al pipeline completo de la tesis.

---

```mermaid
flowchart TD
    subgraph Capa de Datos (ETL y Preparación)
        A1[Ficheros DBF SUNAT] -->|pipeline/etl/sunat_scraper.py| A2[dataset_real_v1.csv]
        A2 -->|pipeline/preparation/preprocessing.py| A3[Parquet Limpios y Normalizados]
    end

    subgraph Capa de Modelamiento e IA (Capas 1-6)
        A3 -->|Capa 1: Predicción| B1[pipeline/core/layer1_predictive.py]
        B1 -->|Capa 2: Anomalías| B2[pipeline/core/layer2_anomaly.py]
        B2 -->|Capa 3: TreeSHAP| B3[pipeline/core/layer3_explainability.py]
        B3 -->|Capa 4: RAG & Reportes| B4[pipeline/core/layer4_rag_reporting.py]
        B4 -->|Capa 5: Validación Factual| B5[pipeline/core/layer5_validation.py]
        B5 -->|Capa 6: Trazabilidad| B6[pipeline/core/layer6_traceability.py]
    end

    subgraph Orquestador y Reportabilidad
        B6 -->|Generación de Metadatos| ORC[Orquestador Central orchestrator.py]
        ORC -->|Salida Firmada| TRACE[pipeline_trace.json]
        ORC -->|Actualización Automática| CHAP4[Capítulo IV: Resultados]
    end
```

---

## 1. Estructura y Ordenamiento del Código Python

Todos los scripts de Python del proyecto han sido migrados y organizados físicamente en las siguientes carpetas funcionales:

### A. Extracción e Ingesta de Datos (`pipeline/etl/`)
*   **[sunat_scraper.py](file:///d:/tesis_yoset/pipeline/etl/sunat_scraper.py)**: Descarga programática de paquetes semanales ZIP de SUNAT, descompresión de DBFs y consolidación de datos reales.
*   **[scrape_sunat_all.py](file:///d:/tesis_yoset/pipeline/etl/scrape_sunat_all.py)**: Web scraping de contingencia de datos aduaneros complementarios.
*   **[trademap_parser.py](file:///d:/tesis_yoset/pipeline/etl/trademap_parser.py)**: Parser de datos de Trade Map.
*   **[data_builder.py](file:///d:/tesis_yoset/pipeline/etl/data_builder.py)**: Genera la estructura unificada del dataset real.
*   **[build_dataset_final.py](file:///d:/tesis_yoset/pipeline/etl/build_dataset_final.py)**: Consolidación final del dataset multivariable.
*   **[download_context_data.py](file:///d:/tesis_yoset/pipeline/etl/download_context_data.py)**: Descarga de variables exógenas (clima BCRP, etc.).
*   **[download_sample.py](file:///d:/tesis_yoset/pipeline/etl/download_sample.py)**: Utilidad de descarga de muestras.
*   **[integrate_proxies.py](file:///d:/tesis_yoset/pipeline/etl/integrate_proxies.py)**: Integración de variables climáticas y macroeconómicas como proxies.
*   **[parse_details.py](file:///d:/tesis_yoset/pipeline/etl/parse_details.py)**, **[parse_dicts.py](file:///d:/tesis_yoset/pipeline/etl/parse_dicts.py)**, **[parse_exportemos.py](file:///d:/tesis_yoset/pipeline/etl/parse_exportemos.py)**, **[parse_sunat_dbf.py](file:///d:/tesis_yoset/pipeline/etl/parse_sunat_dbf.py)**: Parseadores especializados de formatos aduaneros.
*   **[prepare_weekly_dataset.py](file:///d:/tesis_yoset/pipeline/etl/prepare_weekly_dataset.py)**: Agregación de transacciones a granularidad semanal.
*   **[summarize_scraped_data.py](file:///d:/tesis_yoset/pipeline/etl/summarize_scraped_data.py)**: Reporte estadístico de variables recuperadas.
*   **[test_dbf.py](file:///d:/tesis_yoset/pipeline/etl/test_dbf.py)**, **[test_extractors.py](file:///d:/tesis_yoset/pipeline/etl/test_extractors.py)**: Validadores unitarios del flujo ETL.
*   **[generate_synthetic_dataset.py](file:///d:/tesis_yoset/pipeline/etl/generate_synthetic_dataset.py)**: Generador determinista del conjunto sintético de control.

### B. Preparación y Calidad de Datos (`pipeline/preparation/`)
*   **[preprocessing.py](file:///d:/tesis_yoset/pipeline/preparation/preprocessing.py)**: Limpieza, imputadores KNN, RobustScaler y SMOTE balanceado.
*   **[quality_audit.py](file:///d:/tesis_yoset/pipeline/preparation/quality_audit.py)**: Auditoría y EDA de calidad de datos.
*   **[feature_eng.py](file:///d:/tesis_yoset/pipeline/preparation/feature_eng.py)**: Construcción de lags, medias móviles e indicadores cíclicos.
*   **[verify_integrity.py](file:///d:/tesis_yoset/pipeline/preparation/verify_integrity.py)**: Comprobación de consistencia y coherencia del dataset.
*   **[segment_datasets.py](file:///d:/tesis_yoset/pipeline/preparation/segment_datasets.py)**: Segmentador de conjuntos de entrenamiento por producto.

### C. Núcleo IA de 6 Capas (`pipeline/core/`)
*   **[layer1_predictive.py](file:///d:/tesis_yoset/pipeline/core/layer1_predictive.py)**: Capa 1. Entrenamiento de modelos predictivos XGBoost y LightGBM.
*   **[layer2_anomaly.py](file:///d:/tesis_yoset/pipeline/core/layer2_anomaly.py)**: Capa 2. Ensemble probabilístico unificado PyOD.
*   **[layer3_explainability.py](file:///d:/tesis_yoset/pipeline/core/layer3_explainability.py)**: Capa 3. Explicabilidad mediante TreeSHAP local.
*   **[layer4_rag_reporting.py](file:///d:/tesis_yoset/pipeline/core/layer4_rag_reporting.py)**: Capa 4. Generación de informes mediante RAG con LLM.
*   **[layer5_validation.py](file:///d:/tesis_yoset/pipeline/core/layer5_validation.py)**: Capa 5. Auditoría factual cuantitativa de reportes.
*   **[layer6_traceability.py](file:///d:/tesis_yoset/pipeline/core/layer6_traceability.py)**: Capa 6. Cómputo de hashes SHA-256 e inmutabilidad de la cadena de bloques operacional.
*   **[benchmark_deep_anomaly.py](file:///d:/tesis_yoset/pipeline/core/benchmark_deep_anomaly.py)**: Comparativa de rendimiento con modelos Deep Learning.
*   **[shap_explainability.py](file:///d:/tesis_yoset/pipeline/core/shap_explainability.py)**: Módulo de análisis SHAP experimental.
*   **[train_models.py](file:///d:/tesis_yoset/pipeline/core/train_models.py)**: Script base de entrenamiento heredado.

### D. Herramientas de Compilación y Soporte (`tools/`)
*   **[compile_thesis.py](file:///d:/tesis_yoset/tools/compile_thesis.py)**: Compilación final del documento Word/PDF.
*   **[compile_tesis.py](file:///d:/tesis_yoset/tools/compile_tesis.py)**: Script alternativo de compilación de tesis.
*   **[generate_gantt.py](file:///d:/tesis_yoset/tools/generate_gantt.py)**: Generador del cronograma de actividades de la tesis en Gantt.
*   **[auditar_referencias.py](file:///d:/tesis_yoset/tools/auditar_referencias.py)**: Consistencia de citas y refs.bib.
*   **[expand_abbreviations.py](file:///d:/tesis_yoset/tools/expand_abbreviations.py)**: Expansión de abreviaturas del glosario.
*   **[generate_update_guide.py](file:///d:/tesis_yoset/tools/generate_update_guide.py)**: Generador de guías de actualización.
*   **[inject_content.py](file:///d:/tesis_yoset/tools/inject_content.py)**: Inyector de microdatos a tablas.
*   **[limpia_duplicados.py](file:///d:/tesis_yoset/tools/limpia_duplicados.py)**: Purga de citas duplicadas en markdown.
*   **[purga_referencias.py](file:///d:/tesis_yoset/tools/purga_referencias.py)**: Normalización de llaves de citación.
*   **[read_pdf.py](file:///d:/tesis_yoset/tools/read_pdf.py)**, **[read_tesis_yoset.py](file:///d:/tesis_yoset/tools/read_tesis_yoset.py)**, **[read_docx.py](file:///d:/tesis_yoset/tools/read_docx.py)**: Lectores de fuentes académicas.
*   **[rebuild_tesis_monolith.py](file:///d:/tesis_yoset/tools/rebuild_tesis_monolith.py)**: Unificador de capítulos en un solo archivo Markdown.
*   **[run_experiments.py](file:///d:/tesis_yoset/tools/run_experiments.py)**: Ejecutor de baterías experimentales multisemilla.
*   **[sync_individual_chapters.py](file:///d:/tesis_yoset/tools/sync_individual_chapters.py)**: Sincronización entre repositorio de desarrollo y de compilación.
*   **[update_capitulo4_tables.py](file:///d:/tesis_yoset/tools/update_capitulo4_tables.py)**: Rellenado de tablas del borrador de resultados.
*   **[inspect_html.py](file:///d:/tesis_yoset/tools/inspect_html.py)**, **[reformular_tesis.py](file:///d:/tesis_yoset/tools/reformular_tesis.py)**, **[run_all.py](file:///d:/tesis_yoset/tools/run_all.py)**, **[serve_thesis.py](file:///d:/tesis_yoset/tools/serve_thesis.py)**: Scripts de revisión e inspección.
*   **[test_extractors_scripts.py](file:///d:/tesis_yoset/tools/test_extractors_scripts.py)**: Validador unitario de scripts de extracción.

### E. Visor Interactivo Tesis Hub (`src/`)
*   **[app.py](file:///d:/tesis_yoset/src/app.py)**: Servidor web Flask del Hub de Tesis.
*   **[helpers.py](file:///d:/tesis_yoset/src/helpers.py)**: Utilidades de conteo de palabras y referencias bibliográficas del Hub.
*   **[constants.py](file:///d:/tesis_yoset/src/constants.py)**: Metadatos de orden de secciones.
*   **[convert_md_to_html.py](file:///d:/tesis_yoset/src/convert_md_to_html.py)**: Convertidor de Markdown a vistas HTML dinámicas.
