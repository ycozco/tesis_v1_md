# Reporte de Trabajo de Recopilación e Integración de Tesis

*   **Fecha de Registro:** 7 de junio de 2026
*   **Autor/Asistente:** Antigravity (AI Coding Assistant) & Yoset Cozco Mauri
*   **Proyecto:** Sistema de Supervisión Continua Explicable para Operaciones Agroexportadoras Peruanas
*   **Repositorio Local:** `d:\tesis_yoset`

---

## 1. Resumen de Actividades Realizadas Hoy

Hoy se ha consolidado el pipeline completo de ingesta, procesamiento, modelado, experimentación y documentación del proyecto. Las actividades clave completadas se desglosan a continuación:

1.  **Ingesta de Microdatos y Web Scraping:**
    *   Ejecución y documentación del raspador dinámico de SUNAT ([scrape_sunat_all.py](file:///d:/tesis_yoset/src/scrape_sunat_all.py)) que navega y descarga archivos ZIP binarios `.DBF` desde Aduanet.
    *   Ejecución del pipeline de extracción de PROMPERÚ ([summarize_scraped_data.py](file:///d:/tesis_yoset/src/summarize_scraped_data.py)) que raspa el payload Next.js (`__NEXT_DATA__`) de `exportemos.pe` para extraer las fichas estadísticas oficiales de los 5 cultivos (Palta, Uva, Arándano, Espárrago y Cacao).
    *   Consumo de la API del BCRP para obtener el tipo de cambio oficial promedio PEN/USD mensual.
    *   Consolidación de un conjunto de datos real de **40,672 transacciones** aduaneras con control de clave única de serie DUA.
2.  **Preprocesamiento y Calidad:**
    *   Ingeniería de variables (lags de precio y volumen a 1, 7 y 30 días agrupados por cultivo y zona, codificación cíclica temporal sin/cos).
    *   Tratamiento aislado de datos (evitando *data leakage*) en carpetas separadas para muestras reales y sintéticas, aplicando `KNNImputer`, `RobustScaler` y `SMOTE` condicional.
    *   Auditoría de integridad formal de datos aprobada con `verify_integrity.py`.
3.  **Modelado IA y Experimentos (6 Semillas):**
    *   Entrenamiento de la Capa 1 (GBDT Regresor XGBoost + LightGBM con Optuna) logrando un $R^2 > 0.40$ en el modelado del precio FOB normal e inyección de residuos absolutos.
    *   Entrenamiento de la Capa 2 (Ensemble PyOD no supervisado IF + LOF + ECOD) logrando un PR-AUC promedio estable de `0.2014 ± 0.0121` en la calibración y exhaustividad superior al 50% en anomalías logísticas y climáticas.
    *   Evaluación cuantitativa sobre las semillas 42 a 47 y actualización automatizada de las Tablas 4.1, 4.2 y 4.7 en el Capítulo IV de la tesis.
4.  **Generación de Reportes Técnicos Académicos:**
    *   Redacción de 4 informes de sustento metodológico y citas de código en la carpeta de documentación (`docs/`).
5.  **Reconstrucción y Compilación de Tesis:**
    *   Reconstrucción del monolito consolidado `docs/tesis.md`.
    *   Compilación exitosa a formatos **DOCX (Word)** y **PDF** usando Docker/Pandoc y Chrome headless, generando los archivos finales con fecha de hoy.

---

## 2. Inventario de Rutas de Trabajo Utilizadas

A continuación se listan las rutas de los archivos de código, datos y salidas involucradas en el pipeline del proyecto:

### A. Scripts del Pipeline de Scraping, ETL y Auditoría (`src/`)
*   [src/scrape_sunat_all.py](file:///d:/tesis_yoset/src/scrape_sunat_all.py) – Descarga y raspado automatizado de ZIPs de bases de datos de Aduanas SUNAT.
*   [src/summarize_scraped_data.py](file:///d:/tesis_yoset/src/summarize_scraped_data.py) – Raspado de PROMPERÚ mediante JSON block extraction y generación de estadísticas de control.
*   [src/etl_real_data.py](file:///d:/tesis_yoset/src/etl_real_data.py) – Ingesta DBF, mapeo aduanero CADU a zonas productoras, consulta API de BCRP e integración de clima.
*   [src/build_real_dataset.py](file:///d:/tesis_yoset/src/build_real_dataset.py) – Ensamblador de dataset de calibración sintética v1.0 utilizando estadísticas de PROMPERÚ.
*   [src/verify_integrity.py](file:///d:/tesis_yoset/src/verify_integrity.py) – Auditoría física y lógica de completitud, plausibilidad climática, sanitaria y de mermas.

### B. Rutas de Preprocesamiento y Modelos IA (`src/` & `limpieza_de_datos_y_normalizacion/`)
*   [limpieza_de_datos_y_normalizacion/preprocess_data.py](file:///d:/tesis_yoset/limpieza_de_datos_y_normalizacion/preprocess_data.py) – Script de imputación (KNN), escalamiento robusto, codificación cíclica, rezagos (lags) y SMOTE.
*   [src/module1_prediction.py](file:///d:/tesis_yoset/src/module1_prediction.py) – Capa 1: Tuning Optuna y entrenamiento de regresor XGBoost/LightGBM e inyección de residuos.
*   [src/module2_anomaly.py](file:///d:/tesis_yoset/src/module2_anomaly.py) – Capa 2: Ensemble unificado Isolation Forest + LOF + ECOD en PyOD con normalización MinMax.
*   [src/module3_shap.py](file:///d:/tesis_yoset/src/module3_shap.py) – Capa 3: Explicador local TreeSHAP sobre modelo sustituto (surrogate) XGBoost.

### C. Scripts de Experimentos, Reconstrucción y Compilación (`scripts/`)
*   [scripts/run_experiments.py](file:///d:/tesis_yoset/scripts/run_experiments.py) – Ejecutor del protocolo sobre 6 semillas, calculando promedios y desviaciones estándar.
*   [scripts/update_capitulo4_tables.py](file:///d:/tesis_yoset/scripts/update_capitulo4_tables.py) – Inyector automático de resultados en el archivo del Capítulo IV.
*   [scripts/rebuild_tesis_monolith.py](file:///d:/tesis_yoset/scripts/rebuild_tesis_monolith.py) – Reensamblador de los 20 subcapítulos individuales en el archivo unificado `02-95-tesis.md`.
*   [scripts/compile_thesis.py](file:///d:/tesis_yoset/scripts/compile_thesis.py) – Compilador multiformato que invoca Pandoc (Docker) para DOCX y Chrome (headless) para PDF.

### D. Directorio de Datos e Informes Estadísticos (`data/`)
*   [data/dataset_real_v1.csv](file:///d:/tesis_yoset/data/dataset_real_v1.csv) – Archivo plano del conjunto de datos real extraído de SUNAT (40,672 filas).
*   [data/dataset_agro_sintetico_v1.csv](file:///d:/tesis_yoset/data/dataset_agro_sintetico_v1.csv) – Archivo del conjunto de calibración sintética v1.0.
*   `data/real_processed/` – Subcarpeta de sets preprocesados de la muestra real (Train Raw, Train Balanced, Test).
*   `data/synthetic_processed/` – Subcarpeta de sets preprocesados sintéticos.
*   [data/results_metrics.json](file:///d:/tesis_yoset/data/results_metrics.json) – Repositorio estructurado JSON con las métricas cuantitativas completas de los experimentos.

### E. Entregables e Informes Técnicos Generados (`docs/` & `output/`)
*   [docs/03-02-recopilacion-de-data.md](file:///d:/tesis_yoset/docs/03-02-recopilacion-de-data.md) – Informe de scraping (SUNAT, PROMPERÚ, API BCRP), ETL y estadísticas descriptivas de los cultivos.
*   [docs/03-04-preprocesamiento-data.md](file:///d:/tesis_yoset/docs/03-04-preprocesamiento-data.md) – Informe de ingeniería de características, división temporal y prevención de fugas de datos.
*   [docs/03-05-resultado-procesamiento.md](file:///d:/tesis_yoset/docs/03-05-resultado-procesamiento.md) – Informe de regresión tabular (Capa 1), MAE, Optuna y cálculo de residuos.
*   [docs/03-06-informe-de-uso-datos.md](file:///d:/tesis_yoset/docs/03-06-informe-de-uso-datos.md) – Informe de Ensemble PyOD, métricas de PR-AUC, TreeSHAP de Capa 3 y prompts con RAG de Capa 4.
*   [docs/02-95-tesis.md](file:///d:/tesis_yoset/docs/02-95-tesis.md) – Monolito de tesis Markdown consolidado.
*   [output/tesis-v2.docx](file:///d:/tesis_yoset/output/tesis-v2.docx) y `tesis-v2_2026_06_07.docx` – Entregables de tesis compilados en formato Word.
*   [output/tesis-v2.pdf](file:///d:/tesis_yoset/output/tesis-v2.pdf) y `tesis-v2_2026_06_07.pdf` – Entregables de tesis compilados en formato PDF.

---

## 3. Conclusión de la Jornada
El flujo completo de compilación de datos y modelado IA está plenamente integrado, auditado bajo estrictos controles lógicos y compilado en los formatos universitarios exigidos. Todos los scripts operan limpiamente desde la consola local y se conectan sin errores con el entorno de contenedores Docker.
