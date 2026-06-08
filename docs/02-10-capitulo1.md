# CAPITULO I: PLANTEAMIENTO DEL PROBLEMA

## 1.1 Descripcion de la realidad problematica

Las empresas agroexportadoras peruanas coordinan produccion, acopio, empaque, control de calidad, cumplimiento fitosanitario, logistica y comercializacion internacional. En cada etapa se generan datos relevantes para la supervision operativa: precios, volumenes, fechas de exportacion, mercados destino, condiciones climaticas, alertas sanitarias, costos logisticos, mermas y tiempos de despacho. El problema no es solo la ausencia de modelos predictivos, sino la dispersion de fuentes y la baja trazabilidad entre dato, alerta, explicacion y decision.

El panorama actual de datos confirma esta fragmentacion. SUNAT/ADUANET aporta microdatos de exportacion; Trade Map ofrece benchmarks internacionales por producto y mercado destino; SISAP/MIDAGRI contiene precios y volumenes mayoristas internos para palta, uva y esparrago; BCRP aporta tipo de cambio; fuentes climaticas como NASA POWER y SENAMHI funcionan como proxies regionales; APN/OSITRAN aportan contexto logistico; y SENASA/FDA/RASFF pueden emplearse como contexto sanitario agregado. Ninguna fuente, por si sola, cubre todo el flujo operacional. Por ello, la tesis adopta como base un **dataset agroexportador integrado** compuesto por datos reales observados, datos reales agregados, proxies documentados y datos sinteticos controlados.

La investigacion se focaliza en palta, uva y arandano como productos nucleo. El esparrago se mantiene como producto secundario condicionado a validacion suficiente. El cacao se excluye del nucleo experimental por baja representatividad local detectada en el dataset real.

La supervision manual basada en hojas de calculo o reportes aislados dificulta detectar desviaciones oportunamente y explicar por que una alerta es relevante. A su vez, los sistemas automatizados sin explicabilidad reducen la confianza de supervisores y auditores internos. Surge, por tanto, la necesidad de un sistema integrado que detecte anomalias, explique las variables incidentes y genere reportes trazables basados exclusivamente en evidencias.

## 1.2 Problema principal

**Como mejorar la deteccion, explicacion y documentacion de anomalias operativas en agroexportaciones peruanas mediante un sistema integrado de inteligencia artificial explicable que combine datos multisource, prediccion tabular, deteccion de anomalias, SHAP y reportes RAG trazables?**

### Subproblemas

- Que fuentes reales, agregadas, proxy y sinteticas controladas permiten caracterizar el comportamiento normal y anomalico de palta, uva y arandano?
- Como integrar datos de comercio exterior, mercado interno, macroeconomia, clima, logistica y sanidad sin confundir granularidades?
- Que arquitectura de IA permite enlazar prediccion tabular, deteccion de anomalias, explicabilidad y reportes en un flujo trazable?
- De que manera SHAP contribuye a la comprension de las alertas sin atribuir causalidad directa?
- Como generar reportes RAG comprensibles y accionables sin permitir que el LLM invente cifras, causas o recomendaciones?
- Como evaluar si el sistema integrado mejora rendimiento tecnico, trazabilidad, comprension y tiempo de decision frente a componentes aislados?

## 1.3 Objetivos

### 1.3.1 Objetivo principal

Diseniar, implementar y evaluar un sistema integrado de supervision operativa con inteligencia artificial explicable para detectar, explicar y documentar anomalias en un dataset agroexportador integrado de palta, uva y arandano, considerando fuentes reales observadas, datos agregados, proxies documentados y datos sinteticos controlados.

### 1.3.2 Objetivos especificos

1. Identificar, recolectar y documentar fuentes de datos agroexportadores relacionadas con comercio exterior, mercado interno, macroeconomia, clima, logistica y sanidad.
2. Construir un dataset agroexportador integrado y trazable, segmentado por productos nucleo y con etiquetas metodologicas de origen, granularidad y uso.
3. Implementar modelos tabulares LightGBM/XGBoost para estimar valores esperados de precio o volumen.
4. Implementar un ensemble de deteccion de anomalias basado en Isolation Forest, LOF y ECOD.
5. Aplicar SHAP/TreeSHAP para explicar las principales variables asociadas a cada alerta.
6. Generar reportes tecnicos trazables mediante RAG/LLM usando datos, scores, umbrales, fuentes y explicaciones estructuradas.
7. Evaluar el sistema con metricas tecnicas, trazabilidad documental y, si corresponde, pruebas de comprension y tiempo de decision con usuarios o evaluadores.

## 1.4 Hipotesis de la investigacion

**Hipotesis general (H1):** Un sistema integrado de prediccion, deteccion de anomalias, explicabilidad y reportes trazables mejora la deteccion, comprension y trazabilidad de anomalias agroexportadoras frente al uso de componentes aislados.

**Hipotesis nula (H0):** No existe diferencia significativa entre el sistema integrado y los componentes aislados en rendimiento de deteccion, comprension de alertas, calidad de reportes, trazabilidad documental o tiempo de decision.

**Subhipotesis:**

- **H1a:** El ensemble IF + LOF + ECOD obtiene mejor rendimiento de deteccion que detectores individuales o, en caso de rendimiento equivalente, aporta mayor estabilidad y trazabilidad.
- **H1b:** Las explicaciones SHAP incrementan la comprension de las alertas al identificar variables relevantes y direccion de contribucion.
- **H1c:** Los reportes RAG anclados en datos, SHAP y fuentes presentan mayor trazabilidad y consistencia que reportes generados sin recuperacion de contexto.
- **H1d:** El sistema integrado reduce el tiempo requerido para interpretar una alerta frente a un flujo basado en salidas tecnicas aisladas.

## 1.5 Variables e indicadores

### 1.5.1 Variable independiente

**Tipo de sistema de supervision operativa:**

- VI1: Sistema integrado (prediccion tabular + deteccion de anomalias + SHAP + RAG).
- VI2: Componentes aislados (salidas tecnicas independientes sin paso estructurado de evidencia).

### 1.5.2 Variables dependientes

| Variable dependiente | Indicadores | Criterio de evaluacion |
|---|---|---|
| VD1: Rendimiento de deteccion | ROC-AUC, PR-AUC, precision, recall, F1 | Superar o justificar equivalencia frente a baselines con mayor trazabilidad. |
| VD2: Calidad de explicabilidad | Cobertura top-k SHAP, estabilidad, claridad percibida | Explicaciones comprensibles y consistentes. |
| VD3: Calidad de reportes | Completitud, coherencia, accionabilidad, evidencia, consistencia numerica | Rubrica >= 4/5 cuando exista evaluacion humana. |
| VD4: Comprension y tiempo de decision | Segundos, Likert, decision correcta | Reduccion de tiempo y mejora de comprension. |
| VD5: Trazabilidad documental | Porcentaje de alertas con dato, version, modelo, score, SHAP, fuente y reporte | >= 95% de campos completos en condicion integrada. |

### 1.5.3 Variables explicativas del modelo

| Grupo | Variables | Fuente preferida | Tipo metodologico |
|---|---|---|---|
| Comercio exterior | volumen_kg, valor_fob_usd, precio_kg_usd, destino_mercado, empresa_exportadora | SUNAT/ADUANET | real_observada/derivada |
| Mercado interno | sisap_precio_prom, sisap_volumen | SISAP/MIDAGRI | real_agregada |
| Macro | tipo_cambio_pen_usd | BCRP | real_agregada |
| Clima | temperatura_max_c, temperatura_min_c, precipitacion_mm, humedad_pct, ndvi | NASA/SENAMHI/NDVI | proxy |
| Logistica | dias_logisticos, costo_logistico_usd_kg, carga_portuaria_mes, contenedores_mes | Dataset real/APN/OSITRAN | proxy o derivada |
| Sanidad | cumplimiento_fitosanitario, alertas_sanitarias_mes, rechazos_mes | SENASA/FDA/RASFF | proxy o sintetica controlada |
| Contexto internacional | valor_exportado_trademap, crecimiento_exportaciones, participacion_mercado, arancel_estimado | Trade Map | real_agregada |

La variable `etiqueta_anomalia` se tratara como variable experimental derivada, proxy o sintetica segun su origen. Si no existe etiqueta oficial por embarque, debe declararse como construida mediante reglas trazables o escenarios controlados.

## 1.6 Viabilidad de la investigacion

### 1.6.1 Viabilidad tecnica

El stack tecnologico es viable con herramientas open-source: XGBoost, LightGBM, PyOD, SHAP, scikit-learn, pandas y motores RAG/LLM. Los datos locales y descargados permiten una validacion progresiva basada en fuentes reales, agregadas y proxies. La principal restriccion tecnica no es la falta de algoritmos, sino la necesidad de gobernar granularidades y trazabilidad.

### 1.6.2 Viabilidad de datos

La tesis cuenta con `data/dataset_real_v1.csv`, descargas SUNAT/ADUANET, archivos Trade Map, SISAP procesado, BCRP, MIDAGRI, FAOSTAT, NASA/SENAMHI, APN/OSITRAN y fuentes sanitarias. Los datos sinteticos quedan como apoyo para escenarios, balanceo o etiquetas experimentales, no como evidencia principal unica.

### 1.6.3 Viabilidad operativa y economica

El sistema se evalua en ambiente experimental, sin despliegue productivo en tiempo real. La utilidad economica se plantea como impacto potencial por reduccion de tiempo de analisis, mejor documentacion de alertas y deteccion temprana de desviaciones.

## 1.7 Justificacion e importancia

### 1.7.1 Justificacion teorica

La tesis integra cuatro lineas de investigacion que suelen aparecer separadas: modelos tabulares, deteccion de anomalias, explicabilidad y generacion de reportes. Su aporte principal es articularlas en un flujo trazable para supervision operativa agroexportadora peruana, con gobernanza de datos multisource y restriccion anti-alucinacion.

### 1.7.2 Justificacion practica

El sistema puede ayudar a supervisores, responsables de calidad, analistas logisticos y auditores internos a comprender alertas con mayor rapidez y evidencia. El valor no esta solo en detectar una anomalia, sino en documentar por que fue marcada y que fuentes respaldan la interpretacion.

### 1.7.3 Justificacion metodologica

El uso de datos integrados permite superar la dependencia exclusiva de datasets sinteticos. La tesis declara explicitamente la naturaleza de cada variable: real observada, real agregada, proxy, derivada o sintetica controlada.

## 1.8 Alcance

**Alcance tematico:** prediccion tabular, deteccion de anomalias, explicabilidad SHAP, reportes RAG, trazabilidad de datos y documentacion metodologica. Se excluyen modelos de deep learning puro como propuesta principal, despliegue productivo en tiempo real y reemplazo de decision humana.

**Alcance geografico/productivo:** agroexportacion peruana. Productos nucleo: palta, uva y arandano. Producto secundario: esparrago, condicionado a validacion. Producto excluido: cacao.

**Alcance temporal:** dataset estatico o semiestatico basado en datos historicos disponibles hasta 2026. La evaluacion no implica monitoreo en produccion.

## 1.9 Linea, tipo y nivel de investigacion

La investigacion se enmarca en Inteligencia Artificial e Ingenieria de Software Aplicada. Es aplicada, de nivel explicativo-evaluativo, con enfoque post-positivista. Combina metricas tecnicas cuantitativas con evaluacion de comprension, trazabilidad y utilidad operativa.

## 1.10 Tecnicas e instrumentos de recoleccion

| Tecnica | Instrumento | Uso |
|---|---|---|
| Revision bibliografica | Bases academicas y literatura tecnica | Estado del arte. |
| Analisis documental | SUNAT, MIDAGRI, BCRP, Trade Map, SENAMHI, SENASA, APN/OSITRAN | Construccion de fuentes y proxies. |
| Experimentacion controlada | Pipeline de modelos y splits temporales | Evaluacion tecnica. |
| Evaluacion con usuarios/evaluadores | Cuestionarios, logs de tiempo, rubricas | VD2, VD3, VD4 y VD5. |

## 1.11 Cronograma de actividades

| Actividad | Mes 1 | Mes 2 | Mes 3 | Mes 4 | Mes 5 |
|---|:---:|:---:|:---:|:---:|:---:|
| Revision bibliografica y marco teorico | X | | | | |
| Normalizacion e integracion de fuentes | X | X | | | |
| Construccion del dataset integrado | | X | | | |
| Implementacion Capa 1 y Capa 2 | | X | X | | |
| Implementacion SHAP y RAG | | | X | | |
| Experimentos y baselines | | | | X | |
| Evaluacion de trazabilidad/usabilidad | | | | X | |
| Analisis, redaccion y defensa | | | | | X |

## 1.12 Limitaciones

- Algunas variables operativas no existen como dato publico por embarque y deben tratarse como proxies o sinteticas controladas.
- SISAP no mide exportaciones; solo aporta mercado interno mayorista.
- SHAP explica contribuciones del modelo, no causalidad real.
- Las alertas sanitarias agregadas no equivalen a cumplimiento fitosanitario por embarque si no existe llave directa.
- Los resultados basados solo en datos sinteticos deben reportarse como preliminares o auxiliares.
- La generalizacion a empresas especificas requiere validacion con datos privados o convenios de acceso.

---
