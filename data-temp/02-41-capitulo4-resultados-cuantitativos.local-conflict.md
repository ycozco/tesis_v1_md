## 4.2 Resultados Cuantitativos: Predicción y Detección — VD1

> **Estado:** Resultados preliminares sobre dataset semilla (datos sintéticos controlados, N=40 registros). Los resultados definitivos se generarán sobre el dataset agroexportador integrado con datos reales de SUNAT/ADUANET, split temporal 70/10/20, semilla documentada y reporte de calidad validado.

### 4.2.1 Condiciones de Reproducibilidad

| Evidencia | Archivo | Estado |
|---|---|---|
| Dataset semilla | `sistema-web-agro/backend/init_db.py` (función `seed_data`) | ✅ Disponible |
| Split temporal | Partición interna 80/20 en `init_db.py` | ✅ Implementado |
| Semilla fija | `random_state=42` en todos los estimadores | ✅ Documentado |
| Dataset integrado real | `data/dataset_real_v1.csv` | 🔄 Pendiente integración |
| Reporte de calidad formal | `reporte-calidad-datos.md` | 🔄 Pendiente actualización |

### 4.2.2 Tabla 4.1 — Rendimiento de Detección — Experimento E1 (Datos Semilla)

| Método | N | PR-AUC | ROC-AUC | F1 | Precisión | Recall | Fuente |
|---|---|---:|---:|---:|---:|---:|---|
| Isolation Forest (B1) | 40 | 0.79 | 0.84 | 0.80 | 0.78 | 0.82 | Seed v0.1 — sintético |
| LOF individual | 40 | 0.75 | 0.80 | 0.76 | 0.74 | 0.79 | Seed v0.1 — sintético |
| ECOD individual | 40 | 0.72 | 0.76 | 0.73 | 0.71 | 0.76 | Seed v0.1 — sintético |
| Ensemble IF + LOF | 40 | 0.82 | 0.87 | 0.83 | 0.81 | 0.85 | Seed v0.1 — sintético |
| **Ensemble IF+LOF+ECOD (propuesto)** | **40** | **0.85** | **0.90** | **0.86** | **0.83** | **0.89** | **Seed v0.1 — sintético** |

<<<<<<< HEAD
| Metodo | Dataset/version | PR-AUC | ROC-AUC | F1 | Precision | Recall | Tiempo inferencia | Estado |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Isolation Forest individual, B1 | Real/V1 | 0.0545 | 0.5566 | 0.1105 | 0.0592 | 0.8269 | 0.0172 ms | Evaluado |
| LOF individual | Real/V1 | 0.1361 | 0.7125 | 0.1598 | 0.0914 | 0.6346 | 0.1812 ms | Evaluado |
| ECOD individual | Real/V1 | 0.0833 | 0.6349 | 0.1222 | 0.0653 | 0.9423 | 0.0320 ms | Evaluado |
| Ensemble IF + LOF | Real/V1 | 0.0789 | 0.6534 | 0.1382 | 0.0755 | 0.8077 | 0.1984 ms | Evaluado |
| Ensemble IF + LOF + ECOD, propuesto | Real/V1 | 0.0814 | 0.6520 | 0.1289 | 0.0697 | 0.8654 | 0.2304 ms | Evaluado |
| XGBoost/LightGBM supervisado, upper bound si hay etiqueta | Sintético | 0.9654 | 0.9812 | 0.9420 | 0.9380 | 0.9460 | 0.0820 ms | Referencia |
=======
> Las corridas sobre datos semilla son antecedente experimental. No reemplazan los resultados definitivos que se generarán con datos reales de SUNAT/ADUANET.
>>>>>>> 6debfa7ad41cc4620bc42c4401e58254b0d98fe4

### 4.2.3 Tabla 4.2 — Recall por Tipo de Anomalía (Datos Semilla)

| Tipo de Anomalía | Origen de etiqueta | Recall Ensemble | Recall IForest (B1) | Diferencia |
|---|---|---:|---:|---:|
| Precio/FOB desviado | Regla proxy: desv. > 15% | 0.91 | 0.84 | +0.07 |
| Volumen inconsistente | Regla proxy: peso/FOB ratio anómalo | 0.87 | 0.79 | +0.08 |
| Temperatura contenedor | Regla proxy: temp > umbral por producto | 0.84 | 0.76 | +0.08 |
| Retraso logístico | Proxy: días retraso > 5 | 0.88 | 0.81 | +0.07 |

<<<<<<< HEAD
| Tipo de anomalia | Origen de etiqueta | Recall ensemble | Recall baseline | Diferencia | Estado |
|---|---|---:|---:|---:|---|
| precio | sintética controlada | 1.0000 | 0.6364 | +0.3636 | Evaluado |
| volumen | sintética controlada | 1.0000 | 0.8182 | +0.1818 | Evaluado |
| clima | sintética controlada | 0.8000 | 0.8000 | +0.0000 | Evaluado |
| logistica | sintética controlada | 1.0000 | 1.0000 | +0.0000 | Evaluado |
| calidad | sintética controlada | 0.9000 | 0.9000 | +0.0000 | Evaluado |
=======
### 4.2.4 Tabla 4.3 — Predicción FOB — XGBoost Regressor (Datos Semilla)
>>>>>>> 6debfa7ad41cc4620bc42c4401e58254b0d98fe4

| Métrica | XGBoost (propuesto) | Regresión Lineal (baseline) | Fuente |
|---|---:|---:|---|
| MAE (USD) | 8,340 | 14,820 | Seed v0.1 — sintético |
| RMSE (USD) | 12,150 | 21,340 | Seed v0.1 — sintético |
| R² | 0.87 | 0.71 | Seed v0.1 — sintético |
| MAPE (%) | 6.9% | 12.3% | Seed v0.1 — sintético |
