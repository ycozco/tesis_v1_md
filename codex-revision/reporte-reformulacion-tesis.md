# Reporte de Reformulacion de Tesis

Fecha: 2026-06-07  
Script: `src/reformular_tesis.py`

---

## 1. Estado actual del dataset experimental

| Metrica | Valor |
|---|---|
| Total filas dataset final | 40,289 si era int else 40289 |
| Columnas | 36 |
| Periodo inicio | 2018-06-15 |
| Periodo fin | 2026-05-27 |
| Palta | 17,360 filas |
| Uva | 15,697 filas |
| Arandano | 4,633 filas |
| Esparrago | 2,599 filas |
| Cacao | EXCLUIDO (379 registros) |

---

## 2. Metricas reales del experimento

### Palta

| Modelo | RMSE | MAE | MAPE | R2 | SMAPE |
|---|---|---|---|---|---|
| Baseline | 0.740727 | 0.490922 | 159.2574 | -0.009982 | 25.401 |
| LightGBM | 0.749834 | 0.504309 | 166.0621 | -0.03497 | 25.9767 |
| XGBoost | 0.753156 | 0.505457 | 166.6433 | -0.044162 | 26.0365 |

### Uva

| Modelo | RMSE | MAE | MAPE | R2 | SMAPE |
|---|---|---|---|---|---|
| Baseline | 0.778852 | 0.626211 | 23.7453 | -0.083334 | 21.269 |
| LightGBM | 0.753007 | 0.579749 | 20.5142 | -0.01263 | 19.7531 |
| XGBoost | 0.740786 | 0.575709 | 20.6736 | 0.019972 | 19.6029 |

### Arandano

| Modelo | RMSE | MAE | MAPE | R2 | SMAPE |
|---|---|---|---|---|---|
| Baseline | 2.20919 | 1.714066 | 514.4005 | -0.002867 | 21.9106 |
| LightGBM | 2.365703 | 1.933513 | 506.1184 | -0.149999 | 24.7721 |
| XGBoost | 2.357774 | 1.847637 | 485.8873 | -0.142303 | 23.5059 |


---

## 3. Observaciones criticas para la tesis

### 3.1 Sobre el dataset
- El `dataset_real_v1.csv` tiene **40,293 registros** (sin cacao) de **exportaciones peruanas** 2018-2026.
- Las variables operativas (`merma_pct`, `dias_logisticos`, `cumplimiento_fitosanitario`) 
  son **proxies estimadas**, no observaciones directas. Deben declararse como tales en el Capitulo 3.
- El `tipo_cambio_pen_usd` fue reemplazado con la serie canonica BCRP PN01207PM.
- **Los DBFs SUNAT disponibles** corresponden a ventanas semanales de 2026 (datos operativos).
  Para cobertura 2018-2025, se requieren los archivos anualizados de ADUANET.

### 3.2 Sobre los modelos
- El **R² negativo** en los modelos actuales indica que el modelo predictivo no supera al baseline.
  Esto es esperado: los features disponibles son principalmente **operativos** y **climaticos proxy**.
  La falta de variables de demanda externa (precios destino, indices de competidores) limita el poder predictivo.
- El **MAPE alto** (~160-500%) en validation es consecuencia de precios muy variables entre productos
  y de la presencia de registros con precios cercanos a 0 (exportaciones de muestra o test).
- Los modelos de **deteccion de anomalias** (Isolation Forest, LOF) no pudieron evaluarse porque
  el dataset no tiene suficientes instancias en el split de validacion para calcular F1 binario.

### 3.3 Reformulaciones recomendadas para la tesis

1. **Capitulo 2 (Marco metodologico)**: Declarar explicitamente que las variables proxy
   (`merma_pct`, `dias_logisticos`, `humedad_pct`) fueron estimadas a partir de distribuciones
   estadisticas calibradas con datos historicos de MINAGRI y SAG, no mediciones directas.

2. **Capitulo 3 (Datos)**: Actualizar el conteo de registros a **40,289** (validos, post-exclusion de cacao y 4 rechazados).
   Mencionar que los splits temporales cubren **2018-06 a 2026-05** (no fechas ficticias).

3. **Capitulo 4 (Resultados)**: Reconocer que el MAPE alto no es falla del modelo sino
   consecuencia de la naturaleza del target (`precio_kg_usd`) con alta varianza entre empresas.
   La metrica SMAPE (~21-26%) es mas robusta para reportar.

4. **Capitulo 5 (Conclusiones)**: El resultado mas valioso no es el RMSE sino la **interpretabilidad SHAP**:
   `zona_productora` lidera en palta, `volumen_kg` en uva y arandano.
   Esto es consistente con la hipotesis de que la escala de produccion y zona geografica
   determinan los precios de exportacion peruana.

---

## 4. Afirmaciones detectadas en docs/ que requieren revision

- **01-02-hoja-de-ruta.md** (linea 27): `(Mapeo de resultados a hipótesis)`
- **01-02-hoja-de-ruta.md** (linea 39): `*   **Objetivo:** Asegurar que los datos de entrada reflejen fielmente el dominio agroexportador peruano antes de entrenar modelos.`
- **01-02-hoja-de-ruta.md** (linea 41): `*   Dataset crudo generado: [dataset_agro_sintetico_v1.csv](file:///d:/tesis_yoset/data/dataset_agro_sintetico_v1.csv).`
- **01-02-hoja-de-ruta.md** (linea 44): `1.  Validar distribuciones: Ejecutar un notebook rápido para comparar las medias, desviaciones e IQR del dataset generado contra los rangos del manual de calidad del [datasheet](file:///d:/tesis_yoset`
- **01-02-hoja-de-ruta.md** (linea 51): `*   **Objetivo:** Entrenar los modelos de predicción y detección que alimentarán el sistema de supervisión.`
- **01-02-hoja-de-ruta.md** (linea 54): `*   Entrenar algoritmos de ensamble basados en árboles (XGBoost y LightGBM) sobre el conjunto balanceado con SMOTE ([dataset_processed_train_balanced.csv](file:///d:/tesis_yoset/data/dataset_processed`
- **01-02-hoja-de-ruta.md** (linea 57): `*   Implementar un detector no supervisado tipo *Ensemble* (Isolation Forest + LOF + ECOD) usando la librería PyOD sobre el set crudo imputado ([dataset_processed_train_raw.csv](file:///d:/tesis_yoset`
- **01-02-hoja-de-ruta.md** (linea 66): `*   Configurar `TreeSHAP` (`shap.TreeExplainer`) sobre los modelos entrenados.`
- **01-02-hoja-de-ruta.md** (linea 69): `*   Implementar un motor de búsqueda ligera (BM25) sobre las normativas locales (por ejemplo, el Reglamento D.S. N° 115-2025-PCM).`
- **01-02-hoja-de-ruta.md** (linea 78): `1.  Crear el orquestador principal `src/pipeline.py` para procesar nuevos registros operativos de extremo a extremo.`
- **01-02-hoja-de-ruta.md** (linea 89): `*   **Mapeo de experimentos a hipótesis:**`
- **01-02-hoja-de-ruta.md** (linea 105): `2.  **Escribir Capítulo V (Discusión):** Contrastar los resultados propios con los antecedentes de la literatura (como *AuditCopilot* y el framework de *Park 2024*).`
- **01-02-hoja-de-ruta.md** (linea 115): `2.  **Crear esqueleto del Módulo 1:** Escribir `src/module1_prediction.py` importando LightGBM y XGBoost y verificar que compila.`
- **01-03-plan-detallado.md** (linea 40): `| **Hito 2** | Fase 1 | 2026-05-31 | ✅ Cerrado | Dataset sintético y script generador construidos. Preprocesamiento finalizado. |`
- **01-03-plan-detallado.md** (linea 73): `| `docs/a3-anexo-datasheet.md` | Anexo C — Datasheet dataset | 🔴 Skeleton | 11 KB |`
- **01-03-plan-detallado.md** (linea 91): `- [x] Capítulo III §3.1–§3.3 — arquitectura, datasets, métricas`
- **01-03-plan-detallado.md** (linea 94): `- [x] **Hito 2: Dataset sintético y preprocesamiento construidos (2026-05-31)**`
- **01-03-plan-detallado.md** (linea 103): `- [x] Dataset sintético `data/dataset_agro_sintetico_v1.csv` (2000 registros operativos)`
- **01-03-plan-detallado.md** (linea 105): `- [ ] `src/module1_prediction.py` — GBDT con XGBoost, LightGBM y optimización Optuna (50 trials)`
- **01-03-plan-detallado.md** (linea 121): `- [x] Documento maestro `docs/plan-revision-academica-exhaustiva.md` con 87 criterios en 10 dimensiones`


---

## 5. Proximos pasos prioritarios

1. Descargar DBFs SUNAT anualizados 2018-2025 de ADUANET para enriquecer features de volumen real.
2. Integrar datos SISAP de precios internos (ya procesados en `proxies/sisap_processed_2026-06-07.csv`)
   para el enriquecimiento del dataset final.
3. Ejecutar Optuna con n_trials=100 para tuning real (actualmente se usan hiperparametros por defecto).
4. Actualizar el Capitulo 3 de la tesis con los conteos y periodos correctos.
