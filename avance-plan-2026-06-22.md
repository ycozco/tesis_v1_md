# Avance-plan: ampliación predictiva y análisis multifuente de la tesis

**Fecha:** 2026-06-22  
**Proyecto:** Sistema integrado de inteligencia artificial explicable para supervisión analítica de operaciones agroexportadoras peruanas  
**Propósito:** analizar qué otras predicciones y proyecciones puede plantear la tesis a partir de los datasets disponibles, sin perder control metodológico ni convertir variables contextuales en objetivos predictivos no defendibles.

---

## 1. Punto de partida actual

La tesis actualmente plantea como núcleo predictivo dos objetivos semanales:

1. **Valor unitario FOB de exportación para la semana siguiente.**
   - Target actual: `target_fob_unit_value_usd_kg_t1`.
   - Unidad: USD/kg.
   - Granularidad: producto, mercado de destino y semana ISO.
   - Fuente modelable: `data/gold/prediction_features.parquet`.

2. **Volumen exportado para la semana siguiente.**
   - Target actual: `target_export_volume_kg_t1`.
   - Unidad: kg.
   - Granularidad: producto, mercado de destino y semana ISO.
   - Fuente modelable: `data/gold/prediction_features.parquet`.

Estos dos objetivos ya están implementados en `src/module1_prediction.py`, mediante modelos globales XGBoost y LightGBM, validación temporal y generación de residuos para alimentar la capa de anomalías.

---

## 2. Datasets disponibles y potencial analítico

| Dataset o fuente | Ruta | Variables relevantes | Uso defendible |
|---|---|---|---|
| Dataset semanal gold | `data/gold/weekly_product_market.parquet` | FOB total, peso neto, peso bruto, conteo de envíos, exportadores, valor unitario FOB, participación por destino, clima, logística, tipo de cambio | Base semanal producto-mercado para análisis descriptivo y variables predictivas. |
| Features predictivas | `data/gold/prediction_features.parquet` | Targets t+1, rezagos, ventanas móviles, variaciones porcentuales, estacionalidad, variables exógenas desplazadas | Entrenamiento de modelos de precio FOB y volumen. |
| Features de anomalías | `data/gold/anomaly_features.parquet` | Predicciones, residuos, robust-z, scores IF/LOF/ECOD, ensemble, severidad | Detección de desviaciones y priorización de alertas. |
| Dataset real maestro | `data/dataset_real_v1.csv` | Producto, fecha, volumen, precio USD/kg, destino, tipo de cambio, clima/proxies, anomalías | Base experimental inicial y validación de estructura. |
| SUNAT/ADUANET | `data/sunat/`, `codex-revision/data_raw/aduanet_bases/` | Exportaciones, FOB, peso, fecha, país, partida | Fuente primaria a normalizar para dataset final. |
| Trade Map | `data-trademap/export_*` | Mercados destino, valor exportado, cantidad, valor unitario, crecimiento, participación | Benchmark internacional y contexto competitivo. |
| SISAP/MIDAGRI | `codex-revision/metadata/sisap_*` y fuente procesada documentada | Precio mayorista, volumen interno, producto, variedad, mercado, fecha | Mercado interno como contexto y posible tercera predicción. |
| BCRP | `data/downloads/bcrp_tipo_cambio.csv`, `data/bcrp/` | Tipo de cambio PEN/USD | Variable de control y conversión de precios internos. |
| NASA/SENAMHI/NDVI | `data/vegetation/`, `codex-revision/data_raw/nasa_power/`, `codex-revision/data_raw/senamhi/` | Temperatura, precipitación, humedad, vigor vegetativo | Proxies climáticos; no representan condiciones por embarque. |
| APN/OSITRAN | `codex-revision/data_raw/apn_*`, `codex-revision/data_raw/ositran_*` | Movimiento portuario, carga, contenedores | Proxy logístico agregado si se normaliza por mes/puerto. |
| SENASA/FDA/RASFF | `codex-revision/data_raw/senasa/`, `fda/`, `rasff/` | Alertas, rechazos o contexto sanitario | Contexto de riesgo; no etiqueta directa por embarque sin llave verificable. |

---

## 3. Predicciones que ya plantea la tesis

### 3.1 Predicción de valor unitario FOB

El valor unitario FOB es el precio declarado de exportación dividido entre el peso neto exportado. Permite estimar el comportamiento esperado de precio de exportación para una combinación producto-mercado-semana.

**Estado:** implementado parcialmente.  
**Ruta principal:** `src/module1_prediction.py`.  
**Datos:** `data/gold/prediction_features.parquet`.  
**Uso en tesis:** hipótesis H1a.

### 3.2 Predicción de volumen exportado

El volumen exportado permite estimar la cantidad esperada de producto enviada a un mercado destino durante la semana siguiente. Es indispensable porque un precio alto con bajo volumen no tiene el mismo significado comercial que un precio alto con volumen elevado.

**Estado:** implementado parcialmente.  
**Ruta principal:** `src/module1_prediction.py`.  
**Datos:** `data/gold/prediction_features.parquet`.  
**Uso en tesis:** hipótesis H1b.

---

## 4. Predicción adicional más defendible

### 4.1 Precio mayorista nacional de la semana siguiente

La ampliación predictiva más coherente es incorporar una tercera predicción: el **precio mayorista nacional** por producto y semana o mes, usando SISAP/MIDAGRI. Esta predicción no reemplaza al FOB, sino que permite comparar dos perspectivas de precio:

- precio de exportación declarado;
- precio mayorista interno.

**Variable propuesta:** `target_precio_mayorista_usd_kg_t1` o `target_precio_mayorista_pen_kg_t1`.  
**Unidad recomendada:** PEN/kg y USD/kg, documentando conversión con BCRP.  
**Granularidad esperada:** producto, mercado mayorista nacional y semana o mes.  
**Productos viables:** palta, uva y espárrago.  
**Limitación:** arándano no tiene cobertura directa SISAP según la auditoría actual.

**Decisión metodológica recomendada:** incluir precio mayorista como ampliación del sistema, no como hipótesis principal hasta contar con dataset integrado y validación temporal.

---

## 5. Indicadores derivados que no requieren nuevos modelos

Estos indicadores agregan valor al sistema sin multiplicar innecesariamente los objetivos predictivos.

| Indicador | Fórmula o base | Uso analítico | Estado |
|---|---|---|---|
| FOB total esperado | `pred_price * pred_volume` | Estimar valor comercial semanal esperado por producto-destino | Viable inmediato desde predicciones actuales. |
| Brecha FOB-mayorista | `fob_unit_value_usd_kg - precio_mayorista_usd_kg` | Comparar exportación frente a mercado interno | Requiere integrar SISAP + BCRP. |
| Brecha relativa FOB-mayorista | `(FOB - mayorista) / mayorista * 100` | Medir diferencia porcentual de precios | Requiere integrar SISAP + BCRP. |
| Brecha internacional | `FOB Perú - valor_unitario_referencia` | Contextualizar competitividad por destino | Requiere normalizar Trade Map. |
| Índice relativo de precio | `FOB actual / mediana móvil histórica` | Detectar semanas caras/baratas frente al histórico | Viable con `prediction_features`. |
| Volatilidad de precio | rolling std, IQR, MAD, variación porcentual | Medir inestabilidad comercial | Viable con features actuales. |
| Participación por destino | `FOB destino / FOB total producto` o `volumen destino / volumen total producto` | Analizar concentración y cambios de mercado | Ya existe como `destination_fob_share` y `destination_volume_share`. |
| Concentración de mercados | HHI o cuota top-N | Medir dependencia de pocos destinos | Viable desde `weekly_product_market`. |
| Residuo predictivo | observado - predicho | Base para anomalías explicables | Ya existe en `anomaly_features`. |
| Riesgo de alerta | ensemble IF + LOF + ECOD | Priorizar revisión operativa | Ya existe en `anomaly_features`. |

---

## 6. Opciones de proyección y análisis por nivel de prioridad

### Nivel 1: obligatorio y defendible para la tesis actual

1. Mantener la predicción de valor unitario FOB semanal.
2. Mantener la predicción de volumen exportado semanal.
3. Calcular residuos fuera de muestra.
4. Alimentar el ensemble de anomalías con residuos y variables agroexportadoras.
5. Reportar métricas por producto y mercado destino.
6. Separar resultados preliminares de resultados definitivos.

**Razón:** este nivel ya coincide con la tesis, el código y los datasets `gold`.

### Nivel 2: ampliación recomendada del sistema

1. Normalizar SISAP/MIDAGRI y crear una tabla de precio mayorista por producto-fecha.
2. Convertir precio mayorista PEN/kg a USD/kg con BCRP.
3. Crear target `precio_mayorista_t1`.
4. Entrenar modelo separado para precio mayorista si la cobertura temporal es suficiente.
5. Calcular brecha FOB-mayorista observada y esperada.
6. Incorporar esta brecha al dashboard y a los reportes RAG como contexto comercial.

**Razón:** aprovecha datos existentes y amplía el valor del sistema sin cambiar el núcleo de la tesis.

### Nivel 3: exploratorio, útil para discusión y anexos

1. Normalizar Trade Map para generar valores unitarios internacionales por producto-destino-año.
2. Calcular brecha FOB frente a referencia internacional.
3. Medir participación de mercado y crecimiento por destino.
4. Calcular concentración de mercados por producto.
5. Construir indicadores de volatilidad y cambio de composición de destinos.
6. Usar APN/OSITRAN como proxy mensual de presión logística si se logra llave temporal compatible.
7. Usar SENASA/FDA/RASFF como contexto sanitario agregado, no como etiqueta por embarque.

**Razón:** fortalece análisis y discusión, pero no debe convertirse en afirmación predictiva principal sin integración y validación.

---

## 7. Qué no conviene predecir todavía

Las siguientes variables aparecen o podrían aparecer como contexto, pero no deberían formularse como objetivos predictivos principales en la tesis actual:

- Merma real por embarque.
- Días logísticos reales por embarque.
- Costo logístico real por kg.
- Cumplimiento fitosanitario por operación.
- Rechazo sanitario por embarque.
- Utilidad o margen neto del exportador.
- Temperatura de cadena de frío por contenedor.
- Calidad comercial por lote.

**Motivo:** no existe evidencia suficiente de que esas variables sean observadas directamente para cada operación. Si se usan, deben marcarse como proxy, sintéticas o contextuales.

---

## 8. Propuesta de reformulación controlada

La tesis puede evolucionar desde:

> predicción de valor unitario FOB y volumen exportado

hacia:

> predicción y análisis multifuente de precio agroexportador, volumen, brechas de mercado y anomalías trazables.

La reformulación no debe multiplicar hipótesis principales. La estructura recomendada es:

1. **Objetivos predictivos principales:** FOB unitario y volumen exportado.
2. **Objetivo predictivo ampliado:** precio mayorista nacional, si se valida la cobertura SISAP.
3. **Indicadores derivados:** FOB total esperado, brechas, volatilidad, participación y concentración.
4. **Capa de anomalías:** residuos predictivos, robust-z y ensemble.
5. **Capa explicativa:** SHAP + reportes RAG con validación factual.

---

## 9. Cambios técnicos propuestos

| ID | Acción | Ruta sugerida | Salida esperada | Prioridad |
|---|---|---|---|---|
| AP-01 | Crear script de normalización SISAP | `src/prepare_sisap_prices.py` | `data/silver/sisap_weekly_prices.parquet` | Alta |
| AP-02 | Integrar BCRP para conversión PEN/USD | `src/prepare_macro_context.py` | `data/silver/exchange_rate_weekly.parquet` | Alta |
| AP-03 | Crear tabla de brechas FOB-mayorista | `src/build_price_gap_features.py` | `data/gold/price_gap_features.parquet` | Alta |
| AP-04 | Calcular FOB total esperado | `src/module1_prediction.py` o script posterior | columna `pred_total_fob_usd` | Alta |
| AP-05 | Normalizar Trade Map exportación | `src/prepare_trademap.py` | `data/silver/trademap_export_reference.parquet` | Media |
| AP-06 | Calcular concentración de mercado | `src/build_market_concentration.py` | `data/gold/market_concentration.parquet` | Media |
| AP-07 | Evaluar precio mayorista como tercer target | `src/module1b_wholesale_prediction.py` | métricas MAE/RMSE por producto | Media |
| AP-08 | Actualizar Capítulo III | `docs/02-30-capitulo3.md` | subsección de análisis multifuente de precios | Alta |
| AP-09 | Actualizar Capítulo I solo si se acepta ampliación | `docs/02-10-capitulo1.md` | objetivos/hipótesis ajustados con cautela | Media |
| AP-10 | Agregar anexos de trazabilidad de variables | `docs/tesis/DICCIONARIO_DATOS.md` | clasificación real/proxy/sintética/derivada | Alta |

---

## 10. Checklist verificable

- [ ] Confirmar archivos canónicos SISAP/MIDAGRI disponibles y su estructura final.
- [ ] Confirmar si el precio mayorista se trabajará semanal o mensual.
- [ ] Convertir precio mayorista de PEN/kg a USD/kg usando una sola serie BCRP documentada.
- [ ] Definir productos cubiertos por mercado interno: palta, uva y espárrago; excluir arándano de SISAP si no hay fuente directa.
- [ ] Normalizar Trade Map solo con archivos `export_*`; dejar `import_colado_*` fuera del dataset final.
- [ ] Crear indicadores de brecha sin interpretarlos como margen de ganancia.
- [ ] Calcular `pred_total_fob_usd` como indicador derivado, no como tercera hipótesis principal.
- [ ] Mantener predicción de FOB y volumen como núcleo de H1a y H1b.
- [ ] Registrar si precio mayorista queda como extensión del sistema o como experimento adicional.
- [ ] Documentar granularidad, moneda, unidad, fecha de publicación y limitaciones de cada fuente.
- [ ] Ejecutar prueba de fuga temporal antes de usar nuevas features en entrenamiento.
- [ ] Registrar métricas, commit, hashes y configuración si se entrena un nuevo modelo.

---

## 11. Recomendación final

La opción más sólida es mantener la tesis con dos predicciones principales ya implementadas: **FOB unitario** y **volumen exportado**. Como avance metodológico, se debe proponer un módulo ampliado de **análisis multifuente de precios**, donde el **precio mayorista nacional** sea la tercera predicción candidata solo si SISAP queda normalizado y validado.

El resto de proyecciones debe manejarse como indicadores derivados y análisis contextual:

- FOB total esperado.
- Brecha FOB-mayorista.
- Brecha frente a referencia internacional.
- Volatilidad de precio.
- Participación por destino.
- Concentración de mercados.
- Residuo predictivo.
- Riesgo de anomalía.

Así la tesis gana capacidad analítica sin perder defendibilidad académica.
