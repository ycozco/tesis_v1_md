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

### 1.8.1. Delimitación Temática y Tecnológica
La investigación abarca el diseño, implementación y evaluación experimental de un prototipo de software integrado para la supervisión operativa del sector agroexportador peruano. Tecnológicamente, el sistema se acota a una arquitectura estructurada en cuatro capas analíticas secuenciales y de complejidad incremental:
1. **Capa 1: Predicción Tabular de Valores Esperados:** Implementación de modelos de aprendizaje supervisado basados en árboles de decisión de aumento de gradiente (GBDT), específicamente *XGBoost* y *LightGBM*, entrenados para resolver tareas de regresión (estimación de valores esperados de precio FOB por kilogramo o volumen de embarque) sobre datos tabulares multivariados. Se excluyen otros modelos supervisados no basados en árboles debido a su menor eficiencia empírica en el modelado de datos tabulares de escala empresarial.
2. **Capa 2: Ensemble Unificado de Detección de Anomalías:** Configuración de un ensemble no supervisado mediante la librería *PyOD*, que combina tres algoritmos con principios matemáticos complementarios: *Isolation Forest* (método inductivo basado en particionamiento de espacio para identificar outliers globales), *Local Outlier Factor* (LOF, método densitométrico local para identificar outliers contextuales en vecindarios locales) y *Empirical Cumulative Distribution Outlier Detection* (ECOD, método estadístico no paramétrico basado en funciones de distribución acumulada para estimar la probabilidad de cola de las observaciones en múltiples dimensiones). La unificación de puntuaciones se realiza mediante escalamiento Min-Max y promedio simple.
3. **Capa 3: Explicabilidad Post-Hoc Local:** Generación de explicaciones locales para cada alerta de anomalía aduanera u operativa mediante la librería *SHAP*, implementando la formulación optimizada *TreeSHAP*. Esta capa calcula los valores de Shapley para medir la contribución marginal de cada variable de entrada (comercio exterior, clima, mercado interno, logística, sanidad) en el score de anomalía generado, identificando la magnitud y dirección (positiva o negativa) del impacto de cada variable, sin establecer relaciones de causalidad física o real.
4. **Capa 4: Generación Automatizada de Reportes Narrativos (RAG):** Desarrollo de un mecanismo de generación en lenguaje natural utilizando una arquitectura de Recuperación Aumentada por Generación (RAG). El ámbito tecnológico de esta capa se restringe a un modelo de lenguaje de gran tamaño (LLM) acotado mediante *prompt engineering* estricto, donde el prompt de entrada se construye dinámicamente inyectando de forma exclusiva la evidencia estructurada de la alerta (valores reales del registro, score del ensemble, umbral de detección, variables top-k de SHAP con sus respectivas atribuciones numéricas, y metadatos de las fuentes). El LLM tiene prohibido realizar búsquedas libres en internet o recuperar conocimiento externo de sus pesos, limitando su labor a la síntesis narrativa y redacción formal de informes técnicos trazables en español.

### 1.8.2. Delimitación Geográfica y Productiva
* **Ámbito Geográfico:** La investigación se enfoca en el análisis de las operaciones agroexportadoras de la costa y valles interandinos de la República del Perú. Específicamente, el modelado y evaluación se restringe a los cinco departamentos con mayor volumen de agroexportación y densidad de registros aduaneros: La Libertad, Piura, Ica, Lambayeque y Arequipa. Las operaciones de otros departamentos quedan fuera del alcance directo del estudio, aunque el diseño metodológico es genérico y reproducible para otras regiones.
* **Ámbito Productivo (Cultivos):** El estudio se delimita a tres productos núcleo seleccionados por su alta representatividad comercial y complejidad logística: la palta (*Persea americana*), la uva de mesa (*Vitis vinifera*) y el arándano (*Vaccinium corymbosum*). Adicionalmente, el espárrago (*Asparagus officinalis*) se incorpora como un cultivo secundario con el fin de evaluar la robustez de los modelos ante variaciones en la disponibilidad y granularidad de los datos. Se excluye explícitamente el cultivo de cacao (*Theobroma cacao*) debido a que el análisis forense del dataset aduanero identificó una baja representatividad transaccional (solo 379 registros en la ventana de tiempo evaluada), lo que impide un entrenamiento estadísticamente estable y libre de sesgos para modelos de clasificación o regresión multivariados.

### 1.8.3. Delimitación Temporal y de Datos
* **Ventana Temporal de Evaluación:** La ventana temporal histórica abarca un periodo continuo de 8 años, desde **junio de 2018 hasta mayo de 2026** inclusive. Este rango permite capturar ciclos estacionales completos, eventos macroeconómicos de impacto local y el comportamiento de las exportaciones bajo diferentes condiciones climáticas (incluyendo los efectos de fenómenos del Niño).
* **Naturaleza del Dataset Integrado:** El dataset utilizado para el entrenamiento y validación de los modelos tiene un volumen total consolidado de **40,289 registros transaccionales**. Metodológicamente, se declara que los datos no provienen de una única fuente homogénea, sino de un dataset agroexportador integrado y trazable estructurado en cuatro tipos de variables según su origen y nivel de agregación:
  1. *Datos reales observados:* Microdatos transaccionales de aduanas por embarque obtenidos de SUNAT/ADUANET (archivos de manifiestos y declaraciones aduaneras en formato DBF parseados localmente).
  2. *Datos reales agregados:* Series temporales de precios mayoristas del mercado local obtenidos del SISAP/MIDAGRI (formato CSV diario), estadísticas macroeconómicas del tipo de cambio mensual provenientes del BCRP, y datos de contraste comercial internacional de Trade Map.
  3. *Variables contextuales proxies:* Estimaciones climáticas de radiación, temperatura y humedad acumuladas por coordenadas semanales obtenidas de la base de datos NASA POWER, y registros de alertas sanitarias mensuales agregadas de SENASA y la FDA.
  4. *Datos sintéticos controlados:* Empleados estrictamente para complementar vacíos temporales de datos públicos, balanceo de clases altamente desbalanceadas en la evaluación de anomalías o inyectar escenarios experimentales de anomalías simuladas con fines de validación técnica de la Capa 2 y Capa 4, garantizando que el origen metodológico de cada registro esté etiquetado de forma transparente.

### 1.8.4. Delimitación Operativa y de Evaluación
* **Entorno de Ejecución Computacional:** La ejecución, entrenamiento y evaluación de los modelos del pipeline se restringe a un entorno computacional local estándar compuesto por recursos de procesamiento en CPU convencional (procesador comercial de gama media, 16 GB de memoria RAM, sin dependencia de aceleración por GPU corporativa o de alta gama), demostrando la viabilidad de bajo costo del sistema para el sector académico y PYME.
* **Esquema de Evaluación del Sistema:** La evaluación del sistema integrado se delimita a experimentos controlados (E1 a E5) utilizando una división de datos temporal estricta (70% entrenamiento cronológico, 10% validación de hiperparámetros con Optuna y 20% test cronológico final) para evitar la filtración de información (*data leakage*).
* **Estudio de Usabilidad Operativa (VD4):** La evaluación de la usabilidad y la reducción del tiempo de decisión se limita a una prueba experimental controlada con un grupo de evaluadores de perfil profesional en ingeniería, administración o logística (tamaño de muestra N = 15 a 27 participantes, bajo un diseño experimental intra-sujetos o *within-subjects*). La prueba evaluará el impacto del uso de reportes integrados y explicaciones SHAP frente a un flujo de salida técnica tradicional (datos crudos y scores sin explicación narrativa). No se contempla una validación con usuarios en entornos productivos de empresas reales ni integraciones de software con sus ERPs activos.

### 1.8.5. Delimitación Regulatoria y de Principios de Gobernanza
La investigación no busca obtener una certificación formal de cumplimiento legal ni auditar procesos comerciales de una corporación real. El alcance se limita a la **conformidad de diseño** con los principios de gobernanza algorítmica y supervisión humana recomendados en los marcos normativos nacionales e internacionales vigentes:
1. **Decreto Supremo N° 115-2025-PCM (Reglamento de la Ley de Inteligencia Artificial en Perú):** El diseño de la Capa 4 (RAG) y los anexos de Model Cards (Anexo B) y Datasheets (Anexo C) adoptan los lineamientos de transparencia, trazabilidad de datos y supervisión humana ("humano en el bucle" u *human-in-the-loop*), asegurando que el sistema actúe como un asistente consultivo y no reemplace la firma o decisión del auditor humano.
2. **Resolución SBS N° 053-2023 (Reglamento de Gestión de Riesgos de Modelos):** Se toma como estándar metodológico de referencia para la documentación y validación de las variables independientes, la trazabilidad del pipeline de datos y la declaración explícita de limitaciones del modelo, aunque el sector agroexportador no se encuentre bajo la supervisión de la Superintendencia de Banca, Seguros y AFP.
3. **NIST AI Risk Management Framework (AI RMF 1.0) y EU AI Act:** El prototipo adopta la categorización de riesgos y las directrices de explicabilidad local para justificar la integración de la Capa 3 (SHAP) como interfaz de auditoría, limitando la validez del cumplimiento normativo a un alineamiento conceptual metodológico de diseño del software.

### 1.8.6. Exclusiones Explícitas de la Investigación
Para salvaguardar la frontera del proyecto frente a observaciones de jurados o exigencias fuera del marco de la tesis, se excluye expresamente del alcance de este trabajo:
1. **Monitoreo en Tiempo Real o Integración Productiva:** El software no contempla un despliegue en servidores productivos continuos de empresas agroexportadoras, ni integraciones directas mediante APIs activas o WebSockets con sistemas de información empresarial en tiempo real.
2. **Deep Learning como Propuesta Principal:** Las redes neuronales profundas especializadas en datos tabulares (tales como *TabNet* o *FT-Transformer*) quedan totalmente excluidas como núcleo o propuesta principal del sistema de supervisión. Su uso se limita de forma estricta a baselines comparativos de rendimiento en la sección de discusión de resultados.
3. **Automatización Total de la Decisión:** El sistema bajo ninguna circunstancia reemplaza el criterio, firma o toma de decisiones del personal de supervisión humana. No cuenta con módulos automáticos de bloqueo de carga, generación de órdenes de compra, rechazo de exportación o renegociación de contratos aduaneros.
4. **Cacao como Producto Principal:** Se excluye de forma permanente el análisis y modelamiento del cacao debido a la insuficiente representatividad estadística y volumétrica en el dataset real.

## 1.9 Línea, Tipo y Nivel de la investigación

### 1.9.1. Línea de la investigación
La presente investigación se enmarca formalmente dentro de las líneas de investigación definidas por la Escuela Profesional de Ingeniería de Sistemas de la Universidad Nacional de San Agustín de Arequipa:
*   **Línea Principal: Inteligencia Artificial y Aprendizaje Automático Aplicado.** La tesis propone una arquitectura de software inteligente que integra modelos supervisados (XGBoost y LightGBM) para la predicción de series tabulares y modelos no supervisados (ensemble PyOD compuesto por Isolation Forest, LOF y ECOD) para la detección de anomalías operativas, contribuyendo al modelado y automatización de procesos analíticos complejos en el sector productivo.
*   **Línea Secundaria: Ingeniería de Software y Gobernanza de TI.** La investigación define un pipeline de procesamiento y transferencia estructurada de evidencia (datos $\rightarrow$ predicciones $\rightarrow$ anomalías $\rightarrow$ explicaciones SHAP $\rightarrow$ narrativas RAG) alineado con principios normativos nacionales (D.S. N° 115-2025-PCM) y marcos de control de riesgos (Resolución SBS N° 053-2023), abordando la auditabilidad, reproducibilidad y gobernanza de sistemas de software basados en inteligencia artificial.

### 1.9.2. Tipo de la investigación
De acuerdo con las clasificaciones de la metodología de la investigación (Creswell, 2018; Vargas, 2009), este estudio es de **tipo aplicado y tecnológico**. 
*   Es *aplicado* porque no busca desarrollar nuevas teorías matemáticas o algoritmos de aprendizaje automático desde cero, sino utilizar el conocimiento teórico existente y los algoritmos validados en el estado del arte (GDBTs, algoritmos de densidad y árboles de aislamiento, valores de Shapley y modelos de lenguaje con RAG) para resolver un problema operativo concreto: la fragmentación, falta de explicabilidad y baja trazabilidad en la supervisión de operaciones agroexportadoras en el contexto peruano.
*   Es *tecnológico* porque se centra en el diseño, desarrollo experimental y validación de un artefacto de software (un prototipo de sistema integrado de supervisión operativa) concebido para optimizar la eficiencia y la toma de decisiones asistida por datos en un dominio real.

### 1.9.3. Nivel de la investigación
La investigación corresponde a un **nivel explicativo y evaluativo**, adoptando un enfoque epistemológico **post-positivista**:
*   Es *explicativo* porque busca analizar la relación entre las variables independientes (el uso del sistema integrado de IA) y las variables dependientes (el nivel de comprensión de las alertas y la reducción del tiempo de decisión de los analistas). Se intenta explicar *cómo* y *por qué* la inyección de contexto narrativo acotado por SHAP incrementa la claridad de las anomalías operativas en comparación con las herramientas técnicas tradicionales que actúan de forma aislada.
*   Es *evaluativo* debido a que se realiza una comparación sistemática del rendimiento cuantitativo del sistema (ROC-AUC, PR-AUC, F1-Score) frente a baselines individuales del estado del arte, y se evalúa cualitativamente el prototipo mediante un estudio de usabilidad que registra tiempos de decisión y tasas de comprensión con evaluadores humanos utilizando pruebas estadísticas (e.g., test de Wilcoxon o t-Student de muestras apareadas).
*   El enfoque es *post-positivista* ya que sostiene que, aunque los fenómenos operativos y aduaneros pueden ser medidos con rigor matemático, la comprensión y el soporte a la decisión por parte de los usuarios contienen elementos subjetivos que deben ser aproximados a través de la triangulación metodológica, combinando métricas algorítmicas de precisión con encuestas Likert y escalas estandarizadas de usabilidad (SUS).

## 1.10 Técnicas e Instrumentos de Recolección de Información

### 1.10.1. Técnicas
Para el desarrollo y evaluación del sistema propuesto se emplean tres técnicas metodológicas fundamentales en la ingeniería de sistemas:
1.  **Análisis Documental:** Aplicado para la recolección, selección, limpieza e integración de la información proveniente de bases de datos públicas y oficiales (SUNAT, SISAP/MIDAGRI, BCRP, NASA POWER, Trade Map). Esta técnica permite caracterizar las series históricas y estructurar el dataset integrado de 40,289 registros aduaneros y contextuales.
2.  **Experimentación Tecnológica Controlada:** Técnica por la cual se configuran y ejecutan pruebas de software en un entorno de desarrollo para evaluar el rendimiento predictivo y la capacidad de detección de anomalías del pipeline en diferentes condiciones de entrenamiento (E1 a E5), incluyendo análisis de varianza con múltiples semillas y estudios de ablación.
3.  **Encuesta:** Técnica empleada en el estudio de usabilidad (Anexo A) para recopilar las valoraciones de los evaluadores respecto a la comprensión de las alertas explicadas con SHAP y RAG, y su percepción general sobre la usabilidad del prototipo en comparación con la interfaz de control aislada.

### 1.10.2. Instrumentos
Los instrumentos utilizados son herramientas técnicas y métricas diseñadas para registrar la evidencia y evaluar los indicadores de efectividad del sistema:
1.  **Ficha de Registro y Normalización de Datos (Análisis Documental):** Estructura lógica y esquema de base de datos relacional que define el origen, la unidad de medida, la granularidad y la naturaleza metodológica (real, derivada, proxy o sintética) de cada una de las variables que componen el dataset integrado.
2.  **Consola de Experimentación y Scripts de Pruebas (Experimentación):** Programas en lenguaje Python para entrenar los modelos, guardar checkpoints, ejecutar validación cruzada y registrar de forma automatizada las métricas de error (RMSE, SMAPE) y rendimiento (ROC-AUC, PR-AUC, F1-Score).
3.  **Cuestionario de Usabilidad Estructurado (Encuesta):** Cuestionario adaptado basado en la escala estándar SUS (System Usability Scale) y preguntas específicas tipo Likert (escala del 1 al 5) para registrar el nivel de comprensión percibida, utilidad práctica y confianza de los usuarios en los reportes generados.
4.  **Logs de Decisión Temporal (Encuesta):** Cronómetros lógicos automatizados dentro de la interfaz experimental que registran con precisión el tiempo (en segundos) que le toma a cada evaluador analizar una alerta aduanera y responder de forma correcta bajo diferentes condiciones experimentales.

| Técnica | Instrumento | Propósito |
| :--- | :--- | :--- |
| **Análisis Documental** | Ficha de registro de datos estructurados (CSV/DBF) | Recolección e integración de microdatos de comercio exterior (SUNAT/ADUANET), mercado interno (SISAP/MIDAGRI), indicadores macroeconómicos (BCRP) y datos climáticos (NASA POWER). |
| **Experimentación Controlada** | Entorno de desarrollo (Python/VS Code) y Scripts de pruebas | Medición del rendimiento predictivo tabular (XGBoost/LightGBM) y de la precisión del ensemble de anomalías operativas (Isolation Forest, LOF, ECOD). |
| **Encuesta** | Cuestionario Tipo Likert, Escala SUS y Logs de decisión temporal | Evaluación cualitativa de la usabilidad del sistema, tiempo de decisión de los analistas, y nivel de confianza y comprensión de las alertas explicadas frente a reportes convencionales. |

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
