# Replanteamiento academico y tecnico de la tesis
## Sistema integrado de supervision operativa con IA explicable para agroexportacion peruana

**Autor:** Yoset Cozco Mauri  
**Fecha:** Mayo de 2026  
**Documento:** Base revisada para reformular Capitulo I, orientar Capitulo III y sustentar el enfoque metodologico  
**Decision de enfoque:** Supervision operativa agroexportadora con fuentes publicas oficiales y dataset sintetico documentado  

---

## 1. Replanteamiento del enfoque

### 1.1 Problema del enfoque anterior

La version previa de la tesis contenia una idea tecnica valiosa: integrar modelos de prediccion, deteccion de anomalias, explicabilidad y generacion de reportes trazables. Sin embargo, el planteamiento mezclaba tres dominios distintos: auditoria financiera, fraude bancario y supervision agroexportadora. Esta mezcla generaba un riesgo academico importante, porque el problema se formulaba para empresas agroexportadoras peruanas, mientras que varias hipotesis, datasets, referencias y argumentos regulatorios provenian del ambito financiero.

El replanteamiento corrige esa tension y ubica la tesis en un dominio unico: **la supervision operativa de empresas agroexportadoras peruanas**. Bajo este enfoque, el sistema no se presenta como detector de fraude financiero ni como herramienta de auditoria bancaria, sino como una arquitectura de inteligencia artificial explicable para apoyar decisiones operativas en cadenas agroexportadoras.

### 1.2 Nuevo eje de investigacion

La investigacion se centrara en la deteccion, explicacion y documentacion de anomalias operativas asociadas a procesos agroexportadores. Estas anomalias pueden manifestarse como variaciones inusuales en precios, volumenes, condiciones climaticas, mermas, calidad, cumplimiento fitosanitario, retrasos logisticos o comportamiento de exportaciones.

El objeto de estudio no es la entidad financiera ni el fraude contable. El objeto de estudio es el **proceso de supervision operativa** en empresas agroexportadoras que necesitan convertir datos dispersos en alertas interpretables y reportes trazables.

### 1.3 Justificacion del cambio

El cambio de enfoque fortalece la tesis por cuatro razones:

1. **Coherencia academica:** problema, objetivos, hipotesis, variables, metodologia y fuentes de datos quedan alineados con el mismo dominio.
2. **Defensa ante jurado:** evita preguntas debiles sobre por que una tesis agroexportadora se valida principalmente con fraude bancario.
3. **Viabilidad metodologica:** permite trabajar con datos publicos oficiales y datos sinteticos documentados, sin depender obligatoriamente de una empresa privada.
4. **Pertinencia nacional:** conecta la tesis con un sector economico relevante para el Peru, sustentado por informacion oficial de MIDAGRI, SENASA, SENAMHI, SUNAT e INEI.

### 1.4 Uso corregido de la normativa

La Resolucion SBS N. 053-2023 debe utilizarse solo como **referencia nacional de buenas practicas para gestion de riesgo de modelos**, validacion, monitoreo y trazabilidad. No debe presentarse como obligacion directa para empresas agroexportadoras, salvo que el caso de aplicacion pertenezca a una entidad supervisada por la SBS.

En cambio, el D.S. N. 115-2025-PCM, que aprueba el Reglamento de la Ley N. 31814 sobre inteligencia artificial en el Peru, si puede sostener el argumento general de gobernanza, transparencia, supervision humana y uso responsable de sistemas de IA.

---

## 2. Redaccion academica corregida

### 2.1 Titulo propuesto

**Sistema integrado de supervision operativa con inteligencia artificial explicable para la deteccion de anomalias y generacion de reportes trazables en empresas agroexportadoras peruanas**

### 2.2 Introduccion replanteada

La agroexportacion peruana constituye un sector estrategico para la economia nacional debido a su crecimiento sostenido, diversificacion de productos y participacion en mercados internacionales exigentes. De acuerdo con informacion oficial del Ministerio de Desarrollo Agrario y Riego, al cierre de 2025 las agroexportaciones peruanas alcanzaron ventas por USD 15 013 millones, con un crecimiento de 17.3% respecto al ano anterior. Entre los principales productos exportados destacaron arandanos, uvas, paltas, cacao y esparragos, lo que evidencia la importancia economica y operativa de las cadenas agroexportadoras peruanas.

En este contexto, las empresas agroexportadoras articulan procesos de produccion agricola, acopio, almacenamiento, control de calidad, cumplimiento fitosanitario, logistica y comercializacion internacional. Cada uno de estos procesos genera datos que pueden revelar desviaciones relevantes para la gestion operativa: cambios inusuales en precios, variaciones de volumen, condiciones climaticas adversas, incumplimientos de calidad, retrasos logisticos o patrones atipicos en el comportamiento exportador. No obstante, la supervision de estos procesos suele depender de reportes manuales, hojas de calculo, sistemas no integrados o analisis posteriores a la ocurrencia del problema.

La inteligencia artificial ofrece herramientas adecuadas para abordar esta brecha. Los modelos basados en Gradient Boosting Decision Trees han demostrado buen desempeno en datos tabulares; los algoritmos de deteccion de anomalias permiten identificar comportamientos atipicos; los metodos de explicabilidad, como SHAP, ayudan a justificar las predicciones del sistema; y los modelos de lenguaje con arquitectura RAG pueden transformar resultados cuantitativos en reportes comprensibles, siempre que se restrinja su funcion a la generacion narrativa basada en evidencias.

La presente tesis propone un sistema integrado de supervision operativa que combina prediccion tabular, deteccion de anomalias, explicabilidad y generacion de reportes trazables. El sistema se orienta al contexto agroexportador peruano y busca mejorar la capacidad de detectar desviaciones operativas, explicar sus posibles causas y documentar cada alerta de manera comprensible para supervisores, responsables de calidad, gestores logisticos y auditores internos.

### 2.3 Problema principal

**Como mejorar la deteccion, explicacion y documentacion de anomalias operativas en empresas agroexportadoras peruanas mediante un sistema integrado de inteligencia artificial explicable que combine prediccion tabular, deteccion de anomalias, explicabilidad y generacion de reportes trazables?**

### 2.4 Subproblemas

1. Que variables operativas, climaticas, comerciales y fitosanitarias pueden utilizarse para caracterizar el comportamiento normal y anomalo de procesos agroexportadores peruanos?
2. Que arquitectura de inteligencia artificial permite integrar prediccion tabular, deteccion de anomalias, explicabilidad y generacion de reportes en un flujo operativo trazable?
3. De que manera la explicabilidad mediante SHAP contribuye a que supervisores operativos comprendan las causas probables de una alerta?
4. Como generar reportes automaticos que sean comprensibles, accionables y trazables sin permitir que el modelo de lenguaje tome decisiones o invente informacion?
5. Como evaluar si el sistema integrado mejora la trazabilidad, comprension de alertas y tiempo de decision frente al uso de componentes aislados?

### 2.5 Objetivo general

**Disenar, implementar y evaluar un sistema integrado de supervision operativa basado en inteligencia artificial explicable para detectar anomalias en datos agroexportadores, explicar los factores asociados mediante SHAP y generar reportes trazables que apoyen la toma de decisiones en empresas agroexportadoras peruanas.**

### 2.6 Objetivos especificos

1. Identificar y documentar fuentes de datos publicas y sinteticas aplicables a la supervision operativa agroexportadora, considerando variables de precios, volumenes, clima, comercio exterior y cumplimiento fitosanitario.
2. Disenar una arquitectura modular de cuatro capas que integre prediccion tabular, deteccion de anomalias, explicabilidad y generacion de reportes trazables.
3. Implementar modelos de prediccion y deteccion de anomalias sobre datos agroexportadores publicos y sinteticos, utilizando algoritmos adecuados para datos tabulares y series temporales.
4. Integrar explicabilidad mediante SHAP para identificar las variables que mas contribuyen a cada alerta generada por el sistema.
5. Disenar un componente de generacion de reportes mediante RAG que redacte explicaciones operativas basadas exclusivamente en evidencias estructuradas del sistema.
6. Evaluar el sistema integrado mediante metricas tecnicas, trazabilidad documental y prueba de comprension/tiempo de decision con usuarios o evaluadores simulados.

### 2.7 Hipotesis

**Hipotesis general:** Un sistema integrado de prediccion, deteccion de anomalias, explicabilidad y generacion de reportes trazables mejora la trazabilidad de decisiones, la comprension de alertas y el tiempo de decision de supervisores operativos frente al uso de componentes aislados.

**Hipotesis especificas:**

1. El uso combinado de modelos tabulares y detectores de anomalias permite identificar desviaciones operativas con mejor rendimiento que detectores individuales aplicados de forma aislada.
2. Las explicaciones SHAP incrementan la comprension de las alertas por parte de supervisores operativos, al identificar variables relevantes y direccion de impacto.
3. Los reportes generados mediante RAG a partir de evidencias estructuradas presentan mayor trazabilidad y consistencia que reportes generados sin recuperacion de contexto.
4. El sistema integrado reduce el tiempo requerido para interpretar una alerta operativa frente a un flujo basado en tablas, graficos o salidas tecnicas aisladas.

### 2.8 Alcance

La investigacion se limita al diseno, implementacion y evaluacion experimental de un sistema de supervision operativa aplicado al contexto agroexportador peruano. No contempla despliegue productivo en una empresa real ni reemplazo de la decision humana. Los datos principales seran fuentes publicas oficiales y un dataset sintetico agroexportador documentado, construido a partir de supuestos trazables. El dataset BAF se podra usar solo como benchmark metodologico complementario para comparar comportamiento de modelos en datos tabulares desbalanceados, sin presentarlo como evidencia directa del dominio agroexportador.

---

## 3. Base tecnica del sistema propuesto

### 3.1 Principio arquitectonico

El sistema se organiza en cuatro capas secuenciales. Cada capa produce una salida verificable que sirve como entrada para la siguiente. Esta separacion evita que el modelo de lenguaje tome decisiones y permite auditar el recorrido desde el dato original hasta el reporte final.

| Capa | Entrada | Proceso | Salida | Evidencia generada |
|---|---|---|---|---|
| Capa 1: Prediccion tabular | Precios, volumenes, clima, calendario, producto, zona, comercio exterior | XGBoost, LightGBM o modelo base comparable | Valor esperado, tendencia o riesgo operativo | Version del modelo, metricas, variables usadas |
| Capa 2: Deteccion de anomalias | Observacion actual, historico y salida predictiva | Isolation Forest, LOF, ECOD, One-Class SVM o ensemble | Score de anomalia, etiqueta normal/anomalo, umbral | Metodo usado, score, umbral, ranking |
| Capa 3: Explicabilidad | Prediccion, score y features originales | SHAP o metodo de explicabilidad compatible | Variables principales que explican la alerta | Top variables, direccion de impacto, contribucion |
| Capa 4: Reporte trazable | Score, SHAP, contexto recuperado, reglas de plantilla | RAG + LLM restringido | Reporte operativo explicable | Fuentes usadas, evidencias citadas, log de generacion |

### 3.2 Rol del LLM

El modelo de lenguaje no detecta anomalias, no calcula scores y no decide si una alerta es critica. Su funcion se limita a redactar un reporte en lenguaje natural a partir de evidencias ya generadas por capas deterministicas o verificables. El reporte debe incluir:

- dato o evento analizado;
- score de anomalia;
- umbral usado;
- variables principales segun SHAP;
- contexto recuperado desde fuentes internas o documentos;
- advertencia de revision humana;
- identificador de modelo y fecha de generacion.

### 3.3 Tipos de anomalias agroexportadoras a modelar

| Tipo de anomalia | Ejemplo operativo | Fuente esperada | Tratamiento tecnico |
|---|---|---|---|
| Precio atipico | Precio de palta se aleja del patron historico | MIDAGRI, SUNAT, FAOSTAT | Series temporales, z-score, GBDT, IF |
| Volumen inusual | Caida abrupta de volumen de ingreso/exportacion | MIDAGRI, SUNAT, UN Comtrade | Deteccion de outliers y drift |
| Riesgo climatico | Temperatura o precipitacion fuera de rango historico | SENAMHI | Features climaticas y alertas contextuales |
| Cumplimiento fitosanitario | Requisito SENASA asociado a producto/destino | SENASA | Variable categorica o regla de contexto |
| Retraso logistico sintetico | Tiempo de despacho mayor al esperado | Dataset sintetico | Clasificacion/anomalia supervisada o semi-supervisada |
| Merma sintetica | Merma superior a umbral esperado por producto | Dataset sintetico | Score de anomalia y explicacion SHAP |

### 3.4 Dataset sintetico agroexportador

El dataset sintetico debe representar registros operativos plausibles de una empresa agroexportadora. No debe inventarse como si fuera real; debe documentarse como simulacion academica basada en patrones y rangos inspirados en fuentes publicas.

Campos minimos sugeridos:

| Campo | Tipo | Descripcion |
|---|---|---|
| fecha | fecha | Dia o semana de operacion |
| producto | categorica | Arandano, uva, palta, cacao, esparrago u otro producto seleccionado |
| zona | categorica | Costa norte, costa sur, sierra u otra segmentacion |
| volumen_kg | numerica | Volumen producido, acopiado o exportado |
| precio_usd_kg | numerica | Precio aproximado por kg o valor unitario |
| temperatura | numerica | Variable climatica asociada |
| precipitacion | numerica | Variable climatica asociada |
| humedad | numerica | Variable climatica asociada |
| destino | categorica | Pais o bloque comercial |
| cumplimiento_fitosanitario | binaria/categorica | Estado documentado o simulado |
| dias_logistica | numerica | Tiempo de traslado/despacho |
| merma_pct | numerica | Porcentaje de merma simulada |
| etiqueta_anomalia | binaria | Normal/anomalo para evaluacion |
| tipo_anomalia | categorica | Precio, volumen, clima, merma, logistica, calidad |

---

## 4. Base de datos y fuentes

### 4.1 Matriz de fuentes principales

| Fuente | Variables posibles | Frecuencia | Formato esperado | Uso en tesis | Limitacion |
|---|---|---|---|---|---|
| MIDAGRI | Agroexportaciones, productos, precios, boletines sectoriales | Mensual/anual segun publicacion | Notas, boletines, PDF, tablas | Contexto sectorial y precios de referencia | Algunas series pueden requerir extraccion manual |
| SENASA | Requisitos fitosanitarios, certificaciones, sanidad agraria | Continua/documental | Web, PDF, documentos normativos | Variables de cumplimiento y contexto sanitario | Datos operativos finos pueden no estar disponibles |
| SENAMHI | Temperatura, precipitacion, humedad, estaciones | Diaria/mensual | Web, tablas, posibles descargas | Features climaticas y riesgos contextuales | Cobertura depende de estaciones disponibles |
| SUNAT | Exportaciones, valor FOB, partidas, destinos | Mensual/anual | Web, tablas, estadisticas | Validacion de comercio exterior | Puede requerir limpieza por partida arancelaria |
| INEI | IPC, IPM, PBI sectorial, indicadores economicos | Mensual/trimestral/anual | Excel, tablas | Contexto macroeconomico y normalizacion | No siempre disponible a granularidad de producto |
| FAOSTAT | Produccion, comercio, precios agricolas | Anual/mensual segun dominio | API, CSV, JSON | Benchmark internacional y comparacion historica | Escala nacional; no captura operacion de empresa |
| UN Comtrade | Comercio por pais, producto, socio comercial | Mensual/anual | API, CSV | Validacion de exportaciones por producto/destino | Requiere mapeo HS/producto |
| World Bank | Indicadores macroeconomicos y agricolas | Anual | API, CSV | Contexto internacional | No sirve para anomalias operativas finas |
| Dataset sintetico | Volumen, precio, clima, merma, logistica, calidad, etiqueta | Definida por tesis | CSV/Parquet | Validacion controlada del sistema | Debe declararse como sintetico, no evidencia real |
| BAF Benchmark | Datos tabulares desbalanceados con drift | Estatica | CSV/Parquet | Benchmark metodologico secundario | Dominio financiero, no agroexportador |

### 4.2 Cifras sectoriales verificadas para usar con cuidado

| Afirmacion | Valor | Fuente | Fecha | Uso recomendado |
|---|---:|---|---|---|
| Agroexportaciones peruanas al cierre de 2025 | USD 15 013 millones | MIDAGRI, nota oficial en gob.pe | 9 de febrero de 2026 | Contexto economico del problema |
| Crecimiento anual de agroexportaciones 2025 | 17.3% | MIDAGRI, nota oficial en gob.pe | 9 de febrero de 2026 | Justificacion de relevancia sectorial |
| Agroexportaciones no tradicionales 2025 | USD 13 101 millones | MIDAGRI, nota oficial en gob.pe | 9 de febrero de 2026 | Contexto de productos agroindustriales |
| Principales productos 2025 | Arandanos, uvas, paltas, cacao, esparragos | MIDAGRI, nota oficial en gob.pe | 9 de febrero de 2026 | Seleccion de productos para dataset |
| Balanza comercial agraria 2025 | Superavit USD 8 168 millones | MIDAGRI, nota oficial en gob.pe | 9 de febrero de 2026 | Justificacion macrosectorial |

**Nota metodologica:** no usar cifras como "92% de PYMES incumplen" o "ROI 42x" sin fuente primaria y metodo de calculo. Si se conservan como escenarios, deben presentarse como supuestos exploratorios, no como resultados.

### 4.3 Fuentes web base

- MIDAGRI, agroexportaciones 2025: https://www.gob.pe/institucion/midagri/noticias/1350416-midagri-peru-supero-ventas-por-agroexportaciones-en-mas-de-usd-15-mil-millones-al-cierre-del-2025
- PCM, D.S. N. 115-2025-PCM: https://www.gob.pe/institucion/pcm/normas-legales/7133522-115-2025-pcm
- FAOSTAT API y datos agrarios: https://www.fao.org/statistics/highlights-archive/highlights-detail/faostat-launches-a-new-api-developer-portal-to-make-data-access-easier/en
- SENAMHI: https://www.senamhi.gob.pe/
- SENASA: https://www.gob.pe/senasa
- SUNAT estadisticas: https://www.sunat.gob.pe/estadisticasestudios/
- UN Comtrade Plus: https://comtradeplus.un.org/

---

## 5. Matriz de operacionalizacion

### 5.1 Variable independiente

| Variable | Definicion conceptual | Definicion operacional | Modalidades |
|---|---|---|---|
| Tipo de sistema de supervision | Forma en que se presentan y procesan las alertas operativas | Comparacion entre flujo integrado y componentes aislados | Sistema integrado / componentes aislados |

### 5.2 Variables dependientes

| Variable dependiente | Indicador | Formula o procedimiento | Fuente | Unidad de analisis | Criterio de aceptacion |
|---|---|---|---|---|---|
| Rendimiento de deteccion | Precision, recall, F1, PR-AUC | Evaluacion sobre dataset con etiqueta de anomalia | Dataset sintetico y/o subset etiquetado | Registro operativo | Superar baseline individual o justificar rendimiento equivalente |
| Calidad de explicabilidad | Cobertura top-k SHAP | Porcentaje de contribucion explicada por las k variables principales | Salida SHAP | Alerta | Top-3 variables explican proporcion relevante de la decision |
| Comprension de alerta | Puntaje Likert 1-5 | Evaluador responde cuestionario despues de revisar alerta | Prueba de usuarios/simulada | Participante-alerta | Promedio >= 4/5 o mejora frente a baseline |
| Tiempo de decision | Segundos por caso | Tiempo desde presentacion de alerta hasta decision | Registro de prueba | Participante-alerta | Reduccion frente a componentes aislados |
| Trazabilidad documental | Cobertura de campos obligatorios | Alertas con dato, modelo, score, umbral, SHAP, fuente y reporte / total alertas | Logs del sistema | Alerta | >= 95% de alertas completas |
| Calidad de reporte | Completitud, consistencia, accionabilidad | Rubrica manual y, si aplica, ROUGE frente a referencia | Reportes generados | Reporte | Cumplimiento >= 4/5 en rubrica |

### 5.3 Rubrica minima de trazabilidad

Cada alerta generada por el sistema debe registrar:

1. identificador de alerta;
2. fecha y hora;
3. fuente de datos;
4. producto/zona/destino;
5. variables de entrada;
6. modelo y version;
7. score de anomalia;
8. umbral aplicado;
9. variables SHAP principales;
10. reporte generado;
11. fuentes recuperadas por RAG;
12. estado de revision humana.

---

## 6. Plan detallado de busqueda y validacion de informacion

### 6.1 Objetivo de la busqueda

Construir una base documental y de datos que sustente el problema, la metodologia y la evaluacion del sistema integrado de supervision operativa agroexportadora. La busqueda debe producir fuentes citables, datasets o tablas reutilizables, criterios de seleccion y limitaciones documentadas.

### 6.2 Fase 1: Contexto sectorial peruano

**Objetivo:** demostrar la relevancia economica y operativa de la agroexportacion peruana.

**Fuentes prioritarias:**

- MIDAGRI: notas oficiales, boletines, SIEA, publicaciones de comercio agrario.
- SUNAT: estadisticas de exportacion.
- INEI: indicadores macroeconomicos y sectoriales.

**Consultas sugeridas:**

- `agroexportaciones Peru 2025 MIDAGRI`
- `MIDAGRI agroexportaciones arandanos uvas paltas cacao esparragos 2025`
- `SUNAT exportaciones agrarias Peru 2025`
- `INEI PBI agricola Peru 2025`

**Producto esperado:** tabla de contexto con valor exportado, productos principales, mercados principales y fuente exacta.

### 6.3 Fase 2: Datos operativos publicos

**Objetivo:** identificar variables que puedan alimentar o inspirar el dataset de supervision operativa.

**Fuentes prioritarias:**

- MIDAGRI: precios mayoristas, boletines de abastecimiento, reportes de mercado.
- SENAMHI: temperatura, precipitacion, humedad, estaciones.
- SENASA: requisitos fitosanitarios, certificaciones, manuales de buenas practicas.

**Consultas sugeridas:**

- `MIDAGRI boletin precios mayoristas`
- `MIDAGRI abastecimiento mercado mayorista frutas hortalizas`
- `SENAMHI datos historicos temperatura precipitacion Peru`
- `SENASA requisitos fitosanitarios exportacion palta arandano uva`

**Producto esperado:** matriz fuente-variable con frecuencia, granularidad, formato, disponibilidad y limitacion.

### 6.4 Fase 3: Fuentes internacionales de validacion

**Objetivo:** comparar tendencias peruanas con bases internacionales reproducibles.

**Fuentes prioritarias:**

- FAOSTAT: produccion, comercio y precios.
- UN Comtrade: exportaciones por producto, pais y socio comercial.
- World Bank: indicadores macro y agricolas.

**Consultas sugeridas:**

- `FAOSTAT API crops livestock Peru`
- `FAOSTAT producer prices Peru avocado grapes blueberries`
- `UN Comtrade Peru avocado exports HS code`
- `World Bank agriculture value added Peru`

**Producto esperado:** listado de APIs, codigos de producto, variables y procedimiento de descarga.

### 6.5 Fase 4: Literatura tecnica

**Objetivo:** sustentar la arquitectura propuesta y sus decisiones tecnicas.

**Bloques de busqueda:**

- Datos tabulares y GBDT: XGBoost, LightGBM, CatBoost, GBDT vs deep learning.
- Deteccion de anomalias: Isolation Forest, LOF, ECOD, PyOD, ADBench.
- Explicabilidad: SHAP, TreeSHAP, explicabilidad local/global.
- Reportes RAG: RAG, restricciones anti-alucinacion, generacion basada en evidencia.
- Gobernanza: Model Cards, Datasheets for Datasets, NIST AI RMF, Ley 31814.

**Producto esperado:** tabla de referencias con aporte, metodo, dominio y uso exacto en la tesis.

### 6.6 Fase 5: Validacion de calidad de fuentes

Cada fuente debe evaluarse con los siguientes criterios:

| Criterio | Pregunta de validacion | Resultado esperado |
|---|---|---|
| Autoridad | La fuente pertenece a entidad oficial, organismo internacional o publicacion cientifica? | Si |
| Accesibilidad | El enlace esta disponible y se puede recuperar? | Si |
| Reutilizacion | El dato puede descargarse, copiarse o transformarse? | Si o limitacion documentada |
| Fecha | La fuente tiene fecha de publicacion o actualizacion? | Si |
| Granularidad | La frecuencia sirve para el objetivo de la tesis? | Si o limitacion explicita |
| Trazabilidad | Puede citarse en APA/BibTeX? | Si |

### 6.7 Fase 6: Documentacion de datasets

Cada dataset usado o sintetizado debe tener una ficha tipo Datasheet:

- nombre del dataset;
- fuente;
- fecha de acceso;
- periodo cubierto;
- variables;
- unidad de observacion;
- transformaciones;
- valores faltantes;
- sesgos conocidos;
- usos permitidos;
- limitaciones;
- razon de inclusion en la tesis.

---

## 7. Argumentos de sustentacion

### Pregunta 1: Por que ya no se plantea como auditoria financiera?

Porque el problema real de la tesis se ubica en la supervision de procesos agroexportadores. El enfoque financiero servia como referencia tecnica para datos tabulares y anomalias, pero no era coherente como dominio principal. El replanteamiento alinea el sistema con variables agroexportadoras: precios, volumenes, clima, calidad, logistica, sanidad y exportaciones.

### Pregunta 2: Si no hay datos privados, como se valida la tesis?

La tesis se valida con dos niveles. Primero, fuentes publicas oficiales para construir contexto, variables y rangos plausibles. Segundo, un dataset sintetico agroexportador documentado que permite evaluar tecnicamente el sistema bajo condiciones controladas. Esta estrategia es valida si se declara con transparencia y se documentan sus limitaciones.

### Pregunta 3: Por que usar datos sinteticos?

Porque los datos operativos reales de empresas agroexportadoras suelen ser sensibles y no siempre estan disponibles para investigacion. El dataset sintetico permite evaluar la arquitectura, la trazabilidad y el flujo de explicacion sin exponer informacion privada. No reemplaza una validacion industrial futura, pero permite una evaluacion academica reproducible.

### Pregunta 4: Que aporta la tesis si usa algoritmos conocidos?

El aporte no es inventar un nuevo algoritmo, sino integrar tecnicas existentes en un sistema trazable orientado a supervision operativa. La contribucion esta en la arquitectura, el flujo de evidencias, la explicabilidad de alertas y la generacion de reportes controlados por RAG.

### Pregunta 5: Como se evita que el LLM invente informacion?

El LLM no toma decisiones. Solo redacta reportes a partir de evidencias estructuradas: score de anomalia, variables SHAP, umbral, datos de entrada y contexto recuperado. El reporte debe incluir fuentes, identificadores y advertencia de revision humana.

### Pregunta 6: Por que citar SBS si el caso es agroexportador?

La SBS N. 053-2023 no se cita como obligacion directa para agroexportadoras. Se usa como referencia nacional de buenas practicas para gestion de riesgo de modelos, validacion, monitoreo y trazabilidad. La base normativa general de IA en Peru se sostiene en la Ley N. 31814 y su reglamento aprobado por D.S. N. 115-2025-PCM.

### Pregunta 7: Que resultados se esperan?

Se espera demostrar que el sistema integrado mejora la trazabilidad de las alertas, facilita la comprension de las causas probables y reduce el tiempo de interpretacion frente a salidas tecnicas aisladas. El rendimiento predictivo se evaluara con metricas de clasificacion y deteccion; la utilidad operativa se evaluara con rubricas, tiempos y trazabilidad documental.

---

## 8. Cambios posteriores sugeridos en `docs/tesis.md`

Cuando este replanteamiento sea aprobado, se recomienda modificar `docs/tesis.md` en este orden:

1. **Titulo, resumen y abstract:** reemplazar enfoque generico/financiero por supervision operativa agroexportadora.
2. **Introduccion:** incorporar contexto MIDAGRI 2025 y problema de fragmentacion operativa.
3. **Capitulo I, seccion 1.1:** reemplazar magnitud basada en fraude financiero por cifras sectoriales agroexportadoras.
4. **Problema principal y subproblemas:** usar los textos replanteados en este documento.
5. **Objetivos:** alinear todos los objetivos con datos agroexportadores, supervision operativa, SHAP y reportes trazables.
6. **Hipotesis:** eliminar referencias a "datos financieros" y "auditores financieros".
7. **Variables e indicadores:** cambiar "sistema de auditoria" por "sistema de supervision operativa".
8. **Viabilidad:** sustituir costos de auditoria financiera por viabilidad de datos publicos, sintesis de dataset y evaluacion experimental.
9. **Justificacion:** reescribir justificacion economica y social desde agroexportacion, calidad, logistica y cumplimiento.
10. **Marco teorico:** conservar literatura tecnica de GBDT, anomalias, SHAP y RAG; mover trabajos financieros a antecedentes metodologicos secundarios.
11. **Capitulo III:** ampliar metodologia con fuentes publicas, dataset sintetico, datasheets, arquitectura de cuatro capas y protocolo de evaluacion.
12. **Referencias:** corregir claves BibTeX y agregar fuentes oficiales verificadas.

---

## 9. Referencias base recomendadas

### Fuentes sectoriales y normativas

- Ministerio de Desarrollo Agrario y Riego. (2026). *MIDAGRI: Peru supero ventas por agroexportaciones en mas de USD 15 mil millones al cierre del 2025*. https://www.gob.pe/institucion/midagri/noticias/1350416-midagri-peru-supero-ventas-por-agroexportaciones-en-mas-de-usd-15-mil-millones-al-cierre-del-2025
- Presidencia del Consejo de Ministros. (2025). *Decreto Supremo N. 115-2025-PCM: Reglamento de la Ley N. 31814*. https://www.gob.pe/institucion/pcm/normas-legales/7133522-115-2025-pcm
- Servicio Nacional de Sanidad Agraria. (s. f.). *Portal institucional SENASA*. https://www.gob.pe/senasa
- Servicio Nacional de Meteorologia e Hidrologia del Peru. (s. f.). *Portal institucional SENAMHI*. https://www.senamhi.gob.pe/
- Superintendencia Nacional de Aduanas y de Administracion Tributaria. (s. f.). *Estadisticas y estudios*. https://www.sunat.gob.pe/estadisticasestudios/
- Food and Agriculture Organization of the United Nations. (2026). *FAOSTAT launches API developer portal*. https://www.fao.org/statistics/highlights-archive/highlights-detail/faostat-launches-a-new-api-developer-portal-to-make-data-access-easier/en
- United Nations. (s. f.). *UN Comtrade Plus*. https://comtradeplus.un.org/

### Fuentes tecnicas

- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system.
- Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on tabular data?
- Han, X., Hu, Y., Liu, M., Wen, Q., & Zhang, Y. (2022). ADBench: Anomaly detection benchmark.
- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions.
- Zhao, Y., Nasrullah, Z., & Li, Z. (2019). PyOD: A Python toolbox for scalable outlier detection.
- Gebru, T., et al. (2021). Datasheets for datasets.
- Mitchell, M., et al. (2019). Model cards for model reporting.
- National Institute of Standards and Technology. (2023). Artificial Intelligence Risk Management Framework.

---

## 10. Cierre

El replanteamiento propuesto conserva la fortaleza tecnica de la tesis, pero la ubica en un dominio mas coherente y defendible. La idea central ya no es auditar fraude financiero, sino mejorar la supervision operativa agroexportadora mediante un sistema integrado que detecta anomalias, explica sus causas probables y documenta las alertas en reportes trazables.

La frase guia para las siguientes correcciones debe ser:

> La integracion trazable de prediccion, deteccion de anomalias, explicabilidad y reportes mejora la supervision operativa agroexportadora frente al uso de componentes aislados.

