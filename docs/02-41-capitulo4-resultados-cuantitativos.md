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

> Las corridas sobre datos semilla son antecedente experimental. No reemplazan los resultados definitivos que se generarán con datos reales de SUNAT/ADUANET.

### 4.2.3 Tabla 4.2 — Recall por Tipo de Anomalía (Datos Semilla)

| Tipo de Anomalía | Origen de etiqueta | Recall Ensemble | Recall IForest (B1) | Diferencia |
|---|---|---:|---:|---:|
| Precio/FOB desviado | Regla proxy: desv. > 15% | 0.91 | 0.84 | +0.07 |
| Volumen inconsistente | Regla proxy: peso/FOB ratio anómalo | 0.87 | 0.79 | +0.08 |
| Temperatura contenedor | Regla proxy: temp > umbral por producto | 0.84 | 0.76 | +0.08 |
| Retraso logístico | Proxy: días retraso > 5 | 0.88 | 0.81 | +0.07 |

### 4.2.4 Tabla 4.3 — Predicción FOB — XGBoost Regressor (Datos Semilla)

| Métrica | XGBoost (propuesto) | Regresión Lineal (baseline) | Fuente |
|---|---:|---:|---|
| MAE (USD) | 8,340 | 14,820 | Seed v0.1 — sintético |
| RMSE (USD) | 12,150 | 21,340 | Seed v0.1 — sintético |
| R² | 0.87 | 0.71 | Seed v0.1 — sintético |
| MAPE (%) | 6.9% | 12.3% | Seed v0.1 — sintético |
