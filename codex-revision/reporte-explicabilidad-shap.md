# Reporte de Explicabilidad SHAP

Fecha: 2026-06-07  
Script: `src/shap_explainability.py`

## 1. Importancia de features (SHAP o nativa)

### Palta

| feature | importancia_media | modelo | metodo |
|---|---|---|---|
| zona_productora_enc | 0.0102 | lgbm | shap_tree |
| empresa_exportadora_enc | 0.0101 | lgbm | shap_tree |
| volumen_kg | 0.0097 | lgbm | shap_tree |
| destino_mercado_enc | 0.0068 | lgbm | shap_tree |
| humedad_pct | 0.0053 | lgbm | shap_tree |
### Uva

| feature | importancia_media | modelo | metodo |
|---|---|---|---|
| volumen_kg | 0.0453 | xgb | shap_tree |
| empresa_exportadora_enc | 0.0330 | xgb | shap_tree |
| volumen_kg | 0.0217 | lgbm | shap_tree |
| mes | 0.0178 | xgb | shap_tree |
| empresa_exportadora_enc | 0.0148 | lgbm | shap_tree |
### Arandano

| feature | importancia_media | modelo | metodo |
|---|---|---|---|
| mes | 0.4380 | xgb | shap_tree |
| volumen_kg | 0.3170 | xgb | shap_tree |
| temperatura_min_c | 0.2735 | xgb | shap_tree |
| destino_mercado_enc | 0.1916 | xgb | shap_tree |
| humedad_pct | 0.1599 | xgb | shap_tree |

## 2. Interpretaciones por producto


### Palta

La feature mas importante para predecir `precio_kg_usd` en palta es **`zona_productora_enc`** segun el metodo shap_tree. Esto sugiere que los modelos estan capturando principalmente variabilidad de mercado.

### Uva

La feature mas importante para predecir `precio_kg_usd` en uva es **`volumen_kg`** segun el metodo shap_tree. Esto sugiere que los modelos estan capturando principalmente variabilidad de mercado.

### Arandano

La feature mas importante para predecir `precio_kg_usd` en arandano es **`volumen_kg`** segun el metodo shap_tree. Esto sugiere que los modelos estan capturando principalmente variabilidad de mercado.


## 3. Implicaciones para la tesis

- Las features con mayor importancia SHAP son los candidatos principales
  para el analisis de factores determinantes de precio (Capitulo 4 de la tesis).
- El dominio de variables operativas (merma, dias_logisticos) sobre variables
  externas (clima, tipo de cambio) sugiere que el dataset tiene sesgos de construccion.
- Se recomienda complementar con SISAP (precios internos) y variables de demanda
  (Trade Map) en versiones posteriores del modelo.
- Los archivos CSV de importancias estan en:
  `codex-revision/data_processed/eda/figuras/`
