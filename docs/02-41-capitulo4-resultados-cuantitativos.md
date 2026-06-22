## 4.2 Resultados Cuantitativos: Predicción y Detección — VD1

> **Estado:** preliminar. Las cifras disponibles provienen de datos semilla del prototipo (`sistema-web-agro/backend/init_db.py`) y sirven para validar el flujo de inferencia, no para aceptar o rechazar hipótesis definitivas.

### 4.2.1 Condiciones de reproducibilidad

| Evidencia | Archivo | Estado |
|---|---|---|
| Dataset semilla | `sistema-web-agro/backend/init_db.py` | Disponible |
| Datos de prueba documentados | `sistema-web-agro/backend/DATOS_PRUEBA.txt` | Disponible |
| Código backend | `sistema-web-agro/backend/app.py` | Disponible |
| Dataset semanal final | `data/gold/weekly_product_market.parquet` | Parcial/pendiente de validación final |
| Prueba de fuga temporal | `reports/tesis/data-quality/leakage-tests/` | Pendiente si no existe ejecución |
| Registro experimental completo | `reports/tesis/experiments/` | Pendiente |

### 4.2.2 Tabla 4.1 — Rendimiento de detección en validación semilla

| Método | N | PR-AUC | ROC-AUC | F1 | Precisión | Recall | Clasificación |
|---|---:|---:|---:|---:|---:|---:|---|
| Isolation Forest | 40 | 0.79 | 0.84 | 0.80 | 0.78 | 0.82 | Preliminar |
| LOF | 40 | 0.75 | 0.80 | 0.76 | 0.74 | 0.79 | Preliminar |
| ECOD | 40 | 0.72 | 0.76 | 0.73 | 0.71 | 0.76 | Preliminar |
| Ensemble IF + LOF | 40 | 0.82 | 0.87 | 0.83 | 0.81 | 0.85 | Preliminar |
| Ensemble IF + LOF + ECOD | 40 | 0.85 | 0.90 | 0.86 | 0.83 | 0.89 | Preliminar |

Estas cifras permiten verificar que el pipeline produce métricas y compara detectores, pero no sustituyen el experimento final con dataset versionado, partición temporal congelada y residuos fuera de muestra.

### 4.2.3 Tabla 4.2 — Recall por tipo de anomalía

| Tipo de anomalía | Origen de etiqueta | Recall ensemble | Recall IForest | Estado |
|---|---|---:|---:|---|
| Precio/FOB desviado | Regla proxy en semilla | 0.91 | 0.84 | Preliminar |
| Volumen inconsistente | Regla proxy en semilla | 0.87 | 0.79 | Preliminar |
| Temperatura contenedor | Regla proxy en semilla | 0.84 | 0.76 | Preliminar |
| Retraso logístico | Regla proxy en semilla | 0.88 | 0.81 | Preliminar |

### 4.2.4 Tabla 4.3 — Predicción FOB en validación semilla

| Métrica | XGBoost | Regresión lineal baseline | Estado |
|---|---:|---:|---|
| MAE (USD) | 8,340 | 14,820 | Preliminar |
| RMSE (USD) | 12,150 | 21,340 | Preliminar |
| R² | 0.87 | 0.71 | Preliminar |
| MAPE | 6.9% | 12.3% | Preliminar |

### 4.2.5 Evidencia faltante para resultado definitivo

- Congelar dataset semanal final con hash y versión.
- Ejecutar partición temporal sin fuga de información.
- Generar predicciones y residuos fuera de muestra.
- Registrar hiperparámetros, semilla, entorno y tiempo de entrenamiento.
- Guardar métricas globales y por producto.
- Clasificar cada salida como experimental, candidata o final.

Hasta completar esos puntos, VD1 queda en estado preliminar.
