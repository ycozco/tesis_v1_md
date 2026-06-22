## 4.1 Resultados Cuantitativos: Prediccion y Deteccion, VD1

Esta seccion reportara el rendimiento de la capa predictiva tabular y del ensemble de deteccion de anomalias. La evaluacion principal se realizara sobre el dataset agroexportador integrado, no sobre el dataset sintetico aislado.

### 4.1.1 Condiciones minimas para reportar resultados

Antes de completar las tablas, debe existir evidencia local de:

| Evidencia requerida | Archivo esperado |
|---|---|
| Dataset final versionado | `data/dataset_modelo_v_final.csv` o `codex-revision/data_processed/dataset_modelo_v_final.csv` |
| Split temporal | `dataset_train_raw.csv`, `dataset_validation.csv`, `dataset_test.csv` |
| Reporte de calidad | `reporte-calidad-datos.md` |
| Reporte de entrenamiento | `reporte-entrenamiento-modelos.md` |
| Configuracion de semillas | archivo de experimento o log reproducible |

### 4.1.2 Tabla 4.1 - Rendimiento de deteccion, Experimento E1

| Metodo | Dataset/version | PR-AUC | ROC-AUC | F1 | Precision | Recall | Tiempo inferencia | Estado |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Isolation Forest individual, B1 | Real/V1 | 0.0545 | 0.5566 | 0.1105 | 0.0592 | 0.8269 | 0.0172 ms | Evaluado |
| LOF individual | Real/V1 | 0.1361 | 0.7125 | 0.1598 | 0.0914 | 0.6346 | 0.1812 ms | Evaluado |
| ECOD individual | Real/V1 | 0.0833 | 0.6349 | 0.1222 | 0.0653 | 0.9423 | 0.0320 ms | Evaluado |
| Ensemble IF + LOF | Real/V1 | 0.0789 | 0.6534 | 0.1382 | 0.0755 | 0.8077 | 0.1984 ms | Evaluado |
| Ensemble IF + LOF + ECOD, propuesto | Real/V1 | 0.0814 | 0.6520 | 0.1289 | 0.0697 | 0.8654 | 0.2304 ms | Evaluado |
| XGBoost/LightGBM supervisado, upper bound si hay etiqueta | Sintético | 0.9654 | 0.9812 | 0.9420 | 0.9380 | 0.9460 | 0.0820 ms | Referencia |

> Las corridas historicas sobre versiones sinteticas pueden anexarse como antecedente experimental, pero no reemplazan esta tabla final.

### 4.1.3 Tabla 4.2 - Recall por tipo de anomalia

| Tipo de anomalia | Origen de etiqueta | Recall ensemble | Recall baseline | Diferencia | Estado |
|---|---|---:|---:|---:|---|
| precio | sintética controlada | 1.0000 | 0.6364 | +0.3636 | Evaluado |
| volumen | sintética controlada | 1.0000 | 0.8182 | +0.1818 | Evaluado |
| clima | sintética controlada | 0.8000 | 0.8000 | +0.0000 | Evaluado |
| logistica | sintética controlada | 1.0000 | 1.0000 | +0.0000 | Evaluado |
| calidad | sintética controlada | 0.9000 | 0.9000 | +0.0000 | Evaluado |

La columna de origen es obligatoria porque `etiqueta_anomalia` puede provenir de observacion real, regla derivada, proxy o inyeccion sintetica controlada. Esa distincion determina el alcance de la interpretacion.
