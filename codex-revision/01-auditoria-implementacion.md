# Auditoría de implementación

## Alcance revisado

Se revisó la carpeta local `d:\tesis_yoset`, incluyendo código fuente, documentación, datasets, salidas compiladas y scripts de procesamiento. La revisión no modificó datasets ni scripts existentes; solo creó esta carpeta `codex-revision` y archivos `.md` de supervisión.

## Estructura relevante del proyecto

| Ruta | Rol observado |
|---|---|
| `src/scrape_sunat_all.py` | Scraper de enlaces ZIP desde Aduanet/SUNAT hacia `data/sunat/raw_downloads`. |
| `src/etl_real_data.py` | ETL de DBF SUNAT, filtrado por partidas, integración BCRP y variables climáticas simuladas por zona. |
| `src/build_real_dataset.py` | Ensamblador de dataset calibrado desde BCRP y fichas Exportemos/PROMPERÚ; el nombre sugiere real, pero genera un dataset sintético/calibrado. |
| `src/summarize_scraped_data.py` | Raspado/resumen de fichas de Exportemos por producto. |
| `src/segment_datasets.py` | Segmentación actual solo para palta, uva y arándano. |
| `limpieza_de_datos_y_normalizacion/preprocess_data.py` | Preprocesamiento con lags, codificación cíclica, KNNImputer, RobustScaler y SMOTE. |
| `src/module1_prediction.py` | Capa predictiva tabular. |
| `src/module2_anomaly.py` | Detección de anomalías con ensemble IF/LOF/ECOD. |
| `src/module3_shap.py` | Explicabilidad SHAP con modelo sustituto. |
| `scripts/run_experiments.py` | Ejecución de experimentos por semillas. |
| `scripts/compile_thesis.py` | Compilación DOCX/PDF de la tesis. |
| `docs/03-08-trabajo-de-recopilacion-2026-06-07.md` | Bitácora previa de ingesta, preprocesamiento, modelado y compilación. |

## Flujo implementado actualmente

1. Descarga de zips desde Aduanet/SUNAT.
2. Extracción/lectura de DBF.
3. Filtrado por partidas arancelarias.
4. Construcción de dataset real consolidado.
5. Segmentación de productos principales.
6. Preprocesamiento de dataset real y sintético.
7. Entrenamiento/evaluación de modelos.
8. Explicabilidad con SHAP.
9. Documentación y compilación de tesis.

## Hallazgos principales

### 1. Cacao todavía está implementado en scripts y datasets

Aunque el planteamiento metodológico actualizado exige excluir cacao, se encontró incluido en:

- `src/etl_real_data.py`: `CULTIVOS` incluye `"cacao": 1801001900`.
- `src/build_real_dataset.py`: `CULTIVOS` incluye `"cacao": "1801001900"`.
- `src/generate_synthetic_dataset.py`: `PRODUCTOS` incluye `"cacao"`.
- `src/summarize_scraped_data.py`: incluye cacao en las fichas de producto.
- `data/dataset_real_v1.csv`: 379 registros de cacao.
- `data/dataset_agro_sintetico_v1.csv`: 554 registros sintéticos de cacao.

Esto debe corregirse antes de usar resultados como definitivos.

### 2. Espárrago aparece en el dataset real, pero no está segmentado

El dataset real consolidado contiene 2,599 registros de espárrago, pero no existe:

`data/real_processed/esparrago/dataset_esparrago_raw.csv`

El script `src/segment_datasets.py` solo segmenta:

- palta
- uva
- arándano

Si espárrago se mantiene como producto secundario, debe generarse su segmento y auditarse por separado.

### 3. El dataset real combina microdato real con variables no públicas

`data/dataset_real_v1.csv` contiene variables como:

- `dias_logisticos`
- `costo_logistico_usd_kg`
- `cumplimiento_fitosanitario`
- `merma_pct`
- `temperatura_max_c`
- `temperatura_min_c`
- `precipitacion_mm`
- `humedad_pct`
- `etiqueta_anomalia`
- `tipo_anomalia`
- `regla_inyeccion`

Estas columnas no parecen provenir de SUNAT como observaciones públicas por DUA. Según el código revisado, varias son simuladas, calibradas o proxy. Deben etiquetarse como tales en el datasheet y en la tesis.

### 4. `build_real_dataset.py` tiene nombre ambiguo

El archivo indica que ensambla `data/dataset_agro_sintetico_v1.csv` usando estadísticas reales de BCRP/PROMPERÚ. Por trazabilidad académica, conviene renombrar o documentar claramente:

- Dataset real observado: SUNAT/Aduanet + BCRP real.
- Dataset sintético calibrado: generado desde distribuciones y estadísticas externas.

### 5. Verificación de integridad pasó con el entorno `.venv`

El comando con `py` falló porque ese intérprete no tenía `pandas`. Con el entorno del proyecto sí pasó:

`d:\tesis_yoset\.venv\Scripts\python.exe src\verify_integrity.py`

Resultado:

- Dataset sintético: completitud y plausibilidad aprobadas; 2,472 nulos iniciales; 0 duplicados.
- Dataset real: completitud y plausibilidad aprobadas; 42,847 nulos iniciales; 4,684 duplicados detectados.

La auditoría lógica pasa, pero los duplicados del dataset real deben documentarse y tratarse antes de la versión final.

