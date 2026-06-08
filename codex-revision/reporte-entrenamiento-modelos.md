# Reporte de Entrenamiento de Modelos

Fecha: 2026-06-07  
Script: `src/train_models.py`

## Metricas por producto y modelo

| producto | modelo | rmse | mae | mape | r2 | smape | n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| palta | baseline | 0.7407 | 0.4909 | 159.2574 | -0.01 | 25.401 | 3142 |
| palta | lgbm_seed42 | 0.7498 | 0.5043 | 166.0621 | -0.035 | 25.9767 | 3142 |
| palta | lgbm_seed123 | 0.7498 | 0.5043 | 166.0621 | -0.035 | 25.9767 | 3142 |
| palta | lgbm_seed456 | 0.7498 | 0.5043 | 166.0621 | -0.035 | 25.9767 | 3142 |
| palta | xgb | 0.7532 | 0.5055 | 166.6433 | -0.0442 | 26.0365 | 3142 |
| palta | baseline_test | 1.6975 | 0.5185 | 27.3839 | -0.0292 | 26.5315 | 6614 |
| uva | baseline | 0.7789 | 0.6262 | 23.7453 | -0.0833 | 21.269 | 273 |
| uva | lgbm_seed42 | 0.753 | 0.5797 | 20.5142 | -0.0126 | 19.7531 | 273 |
| uva | lgbm_seed123 | 0.753 | 0.5797 | 20.5142 | -0.0126 | 19.7531 | 273 |
| uva | lgbm_seed456 | 0.753 | 0.5797 | 20.5142 | -0.0126 | 19.7531 | 273 |
| uva | xgb | 0.7408 | 0.5757 | 20.6736 | 0.02 | 19.6029 | 273 |
| uva | baseline_test | 0.8029 | 0.6388 | 23.2342 | -0.1733 | 21.6059 | 165 |
| arandano | baseline | 2.2092 | 1.7141 | 514.4005 | -0.0029 | 21.9106 | 128 |
| arandano | lgbm_seed42 | 2.3657 | 1.9335 | 506.1184 | -0.15 | 24.7721 | 128 |
| arandano | lgbm_seed123 | 2.3657 | 1.9335 | 506.1184 | -0.15 | 24.7721 | 128 |
| arandano | lgbm_seed456 | 2.3657 | 1.9335 | 506.1184 | -0.15 | 24.7721 | 128 |
| arandano | xgb | 2.3578 | 1.8476 | 485.8873 | -0.1423 | 23.5059 | 128 |
| arandano | baseline_test | 2.2059 | 1.7143 | 24.0087 | -0.0561 | 21.8339 | 363 |

## Notas

- Seeds usadas: [42, 123, 456, 789, 2026]
- Target: `precio_kg_usd`
- Features: 12 numericas + 3 categoricas
- Splits: 70/10/20 temporal sin mezcla aleatoria
- Los modelos `.pkl` estan en `models/`
- Metricas completas en `codex-revision/results_metrics_2026-06-07.json`
