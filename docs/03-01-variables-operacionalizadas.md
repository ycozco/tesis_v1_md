# Operacionalizacion formal de variables

Fecha de actualizacion: 2026-06-08  
Estado: alineado al dataset agroexportador integrado

Este documento operacionaliza las variables de la tesis bajo el nuevo enfoque de datos: un dataset agroexportador integrado compuesto por datos reales observados, datos reales agregados, proxies documentados y datos sinteticos controlados.

## 1. Variable independiente

### VI: Tipo de sistema de supervision operativa

| Atributo | Especificacion |
|---|---|
| Definicion conceptual | Configuracion arquitectonica del sistema de supervision que integra o aisla prediccion tabular, deteccion de anomalias, explicabilidad SHAP y reportes RAG. |
| Definicion operacional | Variable categorica que compara el sistema integrado de cuatro capas frente a componentes aislados. |
| Valores | VI1 = `integrado`; VI2 = `aislado`. |
| Instrumento | Configuracion experimental del pipeline. |
| Nivel de medicion | Nominal. |
| Control de confusores | Mismo dataset, mismas particiones temporales, mismas semillas y mismos umbrales por condicion. |

## 2. Variables dependientes

### VD1: Rendimiento de deteccion

| Atributo | Especificacion |
|---|---|
| Definicion conceptual | Capacidad del sistema para identificar registros anomalicos minimizando falsos positivos y falsos negativos. |
| Indicadores | PR-AUC, ROC-AUC, F1, precision, recall. |
| Metrica principal | PR-AUC, por robustez ante desbalance. |
| Instrumento | `sklearn.metrics`, logs del pipeline de anomalos. |
| Criterio | El sistema integrado debe superar o justificar equivalencia frente a baselines con mayor trazabilidad. |
| Subhipotesis | H1a. |
| Experimento | E1. |

### VD2: Calidad de explicabilidad

| Atributo | Especificacion |
|---|---|
| Definicion conceptual | Grado en que las explicaciones SHAP permiten interpretar que variables contribuyeron a una alerta. |
| Indicadores | Cobertura top-k SHAP, estabilidad del ranking, claridad percibida. |
| Instrumento | SHAP/TreeSHAP, reporte de explicabilidad y cuestionario si aplica. |
| Criterio | Top-5 variables relevantes y comprensibles; no se interpreta SHAP como causalidad. |
| Subhipotesis | H1b. |
| Experimento | E2. |

### VD3: Calidad de reportes generados

| Atributo | Especificacion |
|---|---|
| Definicion conceptual | Calidad narrativa y trazabilidad de los reportes LLM+RAG. |
| Indicadores | Completitud, consistencia numerica, accionabilidad, coherencia, correspondencia con evidencias. |
| Instrumento | Rubrica de evaluacion, validador automatico de campos y revision humana si aplica. |
| Criterio | Reportes anclados en datos, scores, SHAP, fuente y recomendacion. |
| Subhipotesis | H1c. |
| Experimento | E3. |

### VD4: Comprension y tiempo de decision

| Atributo | Especificacion |
|---|---|
| Definicion conceptual | Eficiencia y calidad cognitiva con que un evaluador interpreta una alerta. |
| Indicadores | Tiempo-a-decision, comprension Likert, decision correcta. |
| Instrumento | Interfaz experimental, logs de tiempo, cuestionario. |
| Criterio | Menor tiempo y mayor comprension en condicion integrada. |
| Subhipotesis | H1d. |
| Experimento | E4. |

### VD5: Trazabilidad documental

| Atributo | Especificacion |
|---|---|
| Definicion conceptual | Capacidad de reconstruir el origen, procesamiento, explicacion y reporte de cada alerta. |
| Indicador | Porcentaje de alertas con dato, version, modelo, score, umbral, SHAP, fuente y reporte. |
| Instrumento | Checklist de trazabilidad y metadatos del pipeline. |
| Criterio | >= 95% de alertas completas en condicion integrada. |
| Subhipotesis | H1 general. |
| Experimento | E4 y E5. |

## 3. Variables explicativas del modelo

| Grupo | Variables | Fuente preferida | Tipo metodologico | Uso |
|---|---|---|---|---|
| Comercio exterior | `volumen_kg`, `valor_fob_usd`, `precio_kg_usd`, `destino_mercado`, `empresa_exportadora` | SUNAT/ADUANET | real_observada o derivada | Entrenamiento y validacion. |
| Mercado interno | `sisap_precio_prom`, `sisap_volumen` | SISAP/MIDAGRI | real_agregada | Contexto mensual para palta, uva y esparrago. |
| Macroeconomia | `tipo_cambio_pen_usd` | BCRP | real_agregada | Control macroeconomico. |
| Clima | `temperatura_max_c`, `temperatura_min_c`, `precipitacion_mm`, `humedad_pct`, `ndvi` | NASA POWER, SENAMHI, NDVI | proxy | Variables exogenas regionales. |
| Logistica | `dias_logisticos`, `costo_logistico_usd_kg`, `carga_portuaria_mes`, `contenedores_mes` | Dataset real, APN, OSITRAN | proxy o derivada | Riesgo logistico. |
| Sanidad | `cumplimiento_fitosanitario`, `alertas_sanitarias_mes`, `rechazos_mes` | SENASA, FDA, RASFF | proxy o sintetica controlada | Riesgo sanitario contextual. |
| Contexto internacional | `trade_valor_exportado`, `trade_crecimiento`, `trade_participacion`, `arancel_estimado` | Trade Map | real_agregada | Benchmark externo. |

## 4. Variable objetivo experimental

| Variable | Definicion | Cuidado metodologico |
|---|---|---|
| `etiqueta_anomalia` | Marca binaria de anomalia usada para evaluacion experimental. | Debe indicar si proviene de regla, proxy o inyeccion sintetica. |
| `tipo_anomalia` | Clase interpretativa de anomalia. | No afirmar que es evento real si fue generado por regla. |
| `score_anomalia` | Puntaje continuo producido por modelos de Capa 2. | Se interpreta como riesgo/model score, no verdad causal. |

## 5. Trazabilidad obligatoria

Cada variable del dataset final debe tener:

- Fuente.
- Ruta local.
- Granularidad.
- Tipo metodologico: `real_observada`, `real_agregada`, `proxy`, `derivada`, `sintetica` o `descartada`.
- Uso: entrenamiento, validacion, contexto, explicabilidad, reporte RAG, anexo o exclusion.

---
