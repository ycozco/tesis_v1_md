# Guía de Actualización de Contenidos y Alineación de Tesis (UNSA)

Esta guía documenta detalladamente el estado anterior de la tesis, el nuevo contenido académico propuesto y la sustentación metodológica que justifica cada cambio para cumplir con las directrices de la Escuela Profesional de Ingeniería de Sistemas y el jurado examinador.

---

## Punto 1: Viabilidad de la Investigación (Sección 1.6)

### 1.1 Estado Anterior (Antes)
```
La viabilidad de la investigación se sustenta en la disponibilidad de herramientas tecnológicas, fuentes de datos accesibles y un diseño experimental realizable dentro del alcance académico del estudio. La propuesta no requiere una implementación productiva en tiempo real ni infraestructura empresarial compleja, sino un entorno controlado que permita construir el dataset, entrenar los modelos, generar explicaciones, producir reportes trazables y evaluar los resultados mediante métricas técnicas y criterios operativos.
Viabilidad  técnica

La investigación es técnicamente viable debido a que los componentes principales del sistema pueden implementarse mediante herramientas de código abierto y tecnologías ampliamente utilizadas en proyectos de aprendizaje automático, detección de anomalías, explicabilidad y procesamiento de lenguaje natural.

El módulo de predicción tabular puede desarrollarse con modelos como XGBoost y LightGBM, adecuados para datos estructurados de naturaleza empresarial. El módulo de detección de anomalías puede implementarse mediante algoritmos disponibles en librerías como PyOD y scikit-learn, incluyendo Isolation Forest, LOF y ECOD. La explicabilidad del sistema puede abordarse mediante SHAP, permitiendo identificar las variables que influyen en las alertas generadas. Finalmente, la generación de reportes puede desarrollarse mediante una arquitectura RAG, restringida al uso de evidencias estructuradas, metadatos, scores, umbrales y explicaciones previamente calculadas.

Desde el punto de vista computacional, el sistema puede ejecutarse en un ambiente experimental con recursos convencionales de cómputo, sin requerir infraestructura especializada de alto costo. La arquitectura propuesta puede organizarse en capas funcionales independientes, lo que facilita su desarrollo, prueba y validación progresiva. Además, el uso de herramientas reproducibles permite documentar versiones de datos, configuraciones de modelos, resultados experimentales y reportes generados.

La principal restricción técnica no corresponde a la disponibilidad de algoritmos, sino a la correcta integración de fuentes heterogéneas, el control de granularidades, la trazabilidad de los datos y la prevención de generación de información no sustentada por parte del modelo de lenguaje. Estas restricciones serán abordadas mediante reglas de integración, etiquetado metodológico de variables, separación entre datos reales, datos agregados, proxies y datos sintéticos controlados, así como mediante una arquitectura RAG limitada a evidencia verificable.

Por lo tanto, la investigación presenta viabilidad técnica, dado que sus componentes pueden ser implementados con tecnologías disponibles, reproducibles y compatibles con el alcance experimental de una tesis de Ingeniería de Sistemas.

Viabilidad de datos
La investigación es viable desde el punto de vista de los datos, debido a que se cuenta con fuentes públicas, agregadas y documentables que permiten construir un dataset agroexportador integrado. La fuente principal para los registros de comercio exterior corresponde a SUNAT/ADUANET, mientras que Trade Map puede utilizarse como fuente de contraste internacional. Asimismo, SISAP/MIDAGRI permite incorporar información de mercado interno mayorista, BCRP aporta variables macroeconómicas como el tipo de cambio, y fuentes climáticas, logísticas y sanitarias pueden incorporarse como variables contextuales o proxies documentados.
El dataset propuesto no depende exclusivamente de una única fuente, sino de la integración controlada de información real observada, información real agregada, variables derivadas, proxies y datos sintéticos controlados. Esta estrategia permite representar de manera más completa el contexto operativo agroexportador, considerando dimensiones de comercio exterior, mercado interno, clima, logística, sanidad y contexto internacional.
La investigación se focaliza en productos agroexportadores con mayor viabilidad de cobertura y representatividad, priorizando palta, uva y arándano como productos núcleo. El espárrago puede mantenerse como producto secundario sujeto a validación de cobertura suficiente, mientras que el cacao debe excluirse de la evaluación principal si no presenta representatividad adecuada en el dataset real auditado.
Una limitación relevante es que no todas las variables operativas existen públicamente con granularidad por embarque, lote o empresa. Por ello, algunas variables deberán tratarse como proxies, variables agregadas o variables sintéticas controladas. En particular, la etiqueta de anomalía deberá declararse según su origen metodológico: real, derivada por reglas, proxy o sintética controlada. Esta diferenciación es necesaria para evitar afirmar que el sistema detecta anomalías reales cuando, en determinados casos, evalúa escenarios experimentales construidos.
Por tanto, la investigación presenta viabilidad de datos, siempre que se mantenga una documentación rigurosa sobre el origen, granularidad, transformación y uso metodológico de cada variable incorporada al dataset.

Viabilidad  económica.
La investigación es operativamente viable porque el sistema será evaluado en un entorno experimental y no como una solución productiva en tiempo real. Esto permite delimitar el alcance del estudio al diseño, implementación y evaluación de un prototipo funcional capaz de procesar datos históricos o semiestáticos, entrenar modelos, detectar anomalías, generar explicaciones y producir reportes trazables.

La evaluación operativa puede realizarse mediante experimentos controlados, comparación frente a componentes aislados y revisión de indicadores asociados a detección, comprensión, calidad de reportes, tiempo de análisis y trazabilidad documental. Cuando sea posible, se podrá incorporar la evaluación de usuarios o expertos mediante cuestionarios tipo Likert, rúbricas de calidad y registros de tiempo de decisión.

Desde el punto de vista económico, la investigación es viable porque utiliza principalmente herramientas open-source, datos públicos o accesibles y recursos computacionales convencionales. No se requiere adquisición de licencias empresariales, sensores IoT, servidores especializados ni integración directa con sistemas productivos de empresas agroexportadoras. Esto reduce los costos de implementación y hace posible desarrollar la investigación dentro de un entorno académico.

El beneficio económico no se medirá como rentabilidad empresarial directa, sino como impacto potencial asociado a la reducción del tiempo de análisis, mejora en la documentación de alertas, mayor trazabilidad del proceso y detección temprana de desviaciones operativas. Estos beneficios pueden justificar futuras implementaciones en entornos empresariales reales, aunque dicha validación productiva queda fuera del alcance principal de la tesis.

En consecuencia, la investigación presenta viabilidad operativa y económica, dado que puede desarrollarse como prototipo experimental con bajo costo relativo, herramientas disponibles y una evaluación alineada con los objetivos académicos del estudio.
```

### 1.2 Nuevo Contenido Propuesto (Después)
Se consolida, profundiza y enriquece la sección bajo los tres apartados oficiales de la plantilla, eliminando la sección de datos independiente y distribuyendo su lógica técnica dentro de la viabilidad correspondiente:

#### `1.6.1. Viabilidad técnica`
> La viabilidad técnica de la investigación se sustenta en la madurez, disponibilidad y estabilidad de herramientas computacionales de código abierto especializadas en aprendizaje automático, análisis estadístico y procesamiento de lenguaje natural. El pipeline propuesto se implementa en el lenguaje de programación Python (versión 3.11) y se apoya en librerías ampliamente validadas por la comunidad científica: Scikit-Learn (1.5.0) para operaciones básicas de modelamiento, PyOD (1.1.3) para la orquestación del ensemble de anomalías, XGBoost (2.0.3) y LightGBM (4.3.0) para el módulo predictivo tabular, SHAP (0.45.0) para la explicabilidad local, y Sentence-Transformers (2.7.0) junto con rank-bm25 para los mecanismos de recuperación semántica e inyección de contexto RAG.
> 
> Desde el punto de vista de los datos, la viabilidad técnica para la integración multisource está garantizada a través del acceso a repositorios públicos y oficiales. Los registros transaccionales de comercio exterior se procesan mediante microdatos de la SUNAT/ADUANET (archivos DBF anuales y semanales que son parseados utilizando scripts específicos de extracción). El contexto de mercado mayorista interno se recupera del SISAP/MIDAGRI (archivos CSV con series de precios y volúmenes), y el tipo de cambio proviene de las series temporales canonizadas del BCRP (serie mensual PN01207PM). 
> 
> La complejidad técnica derivada de las diferentes granularidades (SUNAT opera por transacción diaria, SISAP por promedio diario, BCRP por promedio mensual y el clima por cuadrículas semanales de la NASA) se resuelve en el pipeline mediante agregaciones matemáticas y alineaciones temporales estrictas, previniendo la fuga de información (*data leakage*). Asimismo, se declaran explícitamente variables proxy (como las estimaciones de mermas y días logísticos calculadas mediante distribuciones de probabilidad calibradas con datos del sector) y se excluye el cacao (379 filas) debido a su baja representatividad transaccional, focalizando el sistema en los productos núcleo: palta, uva y arándano.

#### `1.6.2. Viabilidad operativa.`
> La viabilidad operativa de la investigación se asegura al delimitar el estudio a un entorno experimental controlado y no como un sistema de producción en tiempo real. La investigación cuenta con un dataset histórico integrado y trazable de 40,289 registros reales (periodo 2018-2026), libre de datos de cacao por baja representatividad (379 registros) y con el espárrago como producto secundario de validación condicionada. 
> 
> El diseño operativo contempla la evaluación mediante experimentos cuantitativos y pruebas cualitativas de usabilidad técnica con usuarios evaluadores en un ambiente controlado. Estas pruebas registrarán métricas de tiempo de decisión y niveles de comprensión de alertas asistidas por IA explicable y reportes estructurados con RAG/LLM, de acuerdo con las directrices de gobernanza y supervisión humana establecidas en el D.S. N.° 115-2025-PCM y la Resolución SBS N.° 053-2023.

#### `1.6.3. Viabilidad económica.`
> La viabilidad económica es alta dado que el diseño técnico prioriza la eficiencia en el uso de recursos y el bajo costo de infraestructura. A diferencia de las arquitecturas de aprendizaje profundo que requieren tarjetas gráficas (GPUs) de alto costo para el entrenamiento, los modelos basados en árboles de decisión (GBDT) y los algoritmos no supervisados de PyOD se entrenan y ejecutan eficientemente en CPU comercial estándar (infraestructura local compuesta por un procesador estándar de gama media y 16 GB de RAM), reduciendo a cero el gasto en servidores dedicados.
> 
> Todo el software utilizado es de licencia libre (open-source), eliminando costos de suscripción de software propietario. El único costo operativo directo proviene del uso de tokens de las APIs de modelos de lenguaje (OpenAI o Anthropic) para la Capa 4 de Generación de Reportes. Este costo se encuentra estrictamente acotado al marco de validación experimental del estudio (calculando un promedio de 1,500 tokens por reporte generado, lo que representa un costo aproximado de USD 0.03 por informe), siendo financiado en su totalidad por el investigador. El impacto económico del sistema se justifica por la reducción drástica de horas-hombre requeridas para auditar y documentar manualmente una alerta operativa, traduciéndose en una propuesta rentable y viable dentro del ámbito académico.

### 1.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** La plantilla oficial de tesis de Ingeniería de Sistemas de la UNSA exige explícitamente tres subsecciones numeradas de viabilidad: técnica, operativa y económica. El borrador anterior incluía la "Viabilidad de datos" como una sección independiente, lo cual constituía una desviación formal del reglamento. 
> 
> Al integrar el análisis de datos dentro de la Viabilidad Técnica (dado que la ingesta, limpieza y sincronización de granularidades son desafíos de ingeniería de software) y separar los aspectos de usabilidad/experimentación (Operativa) y costos/licencias (Económica), el documento cumple formalmente con la estructura de la universidad y evita observaciones de formato por parte del jurado.

---

## Punto 2: Justificación e Importancia de la Investigación (Sección 1.7)

### 2.1 Estado Anterior (Antes)
```
Justificación e Importancia de la Investigación.
Justificación
Teórica 


Económica


Social


 Importancia.
```

### 2.2 Nuevo Contenido Propuesto (Después)
Se redactan de forma rigurosa y madura las justificaciones teórica, económica y social, y la importancia del estudio para el sector agroexportador y la ingeniería de sistemas:

#### `1.7.1. Justificación`
##### `A. Teórica`
> La presente investigación se justifica teóricamente al proponer y validar un framework de integración conceptual para la supervisión operativa que unifica cuatro áreas de la inteligencia artificial tradicionalmente aisladas en la literatura: (1) predicción supervisada en datos estructurados mediante árboles de decisión optimizados (XGBoost y LightGBM); (2) detección de anomalías no supervisada en entornos multidimensionales mediante un ensemble unificado probabilísticamente (PyOD); (3) explicabilidad local post-hoc basada en la teoría de juegos cooperativos (SHAP); y (4) generación narrativa en lenguaje natural mediante modelos de lenguaje acotados por contexto (RAG). 
> 
> El principal aporte teórico radica en resolver el problema del acoplamiento débil entre modelos predictivos y modelos generativos, aportando una metodología formal para mitigar el riesgo de alucinación numérica del LLM al forzarlo a operar sobre un espacio de representación cerrado estructurado por scores y vectores de importancia SHAP. Esto contribuye a la teoría de sistemas inteligentes orientados a la auditoría continua, demostrando cómo la explicabilidad matemática puede ser convertida en una interfaz narrativa útil para la supervisión humana, en concordancia con los principios de gobernanza algorítmica.

##### `B. Económica`
> Desde el punto de vista económico, el sector agroexportador peruano constituye una de las columnas vertebrales de la economía nacional, con transacciones que superan los USD 15,000 millones anuales (MIDAGRI, 2026). No obstante, la variabilidad del precio FOB por kilogramo, el descalibrado estacional y las ineficiencias logísticas en puertos representan un riesgo constante para la rentabilidad de las organizaciones. Un solo día de retraso logístico o una desviación en la cadena de frío de productos altamente perecederos (como la palta, uva y arándano) puede reducir la vida útil del cultivo en destino hasta en un 15%, generando reclamos de calidad que deprecian el valor comercial del embarque hasta en un 30%. 
> 
> Esta investigación se justifica económicamente al dotar a las empresas de una herramienta de detección temprana que identifica desviaciones operativas y de precios en los registros aduaneros y contextuales antes de que se consoliden pérdidas irreparables. Al automatizar la documentación y explicación de anomalías, el sistema reduce el costo de auditoría operativa interna de horas a segundos, protegiendo los márgenes de ganancia de los exportadores peruanos frente a la volatilidad internacional.

##### `C. Social`
> Socialmente, la agricultura de exportación representa la mayor fuente de empleo formal, directo y descentralizado en las regiones del Perú, albergando a más de un millón de trabajadores en la costa y valles andinos (con especial concentración en La Libertad, Piura, Ica y Arequipa). La estabilidad laboral y el ingreso de miles de familias dependen directamente de la competitividad y la continuidad de los flujos de exportación de las empresas del sector. 
> 
> Las crisis operativas no detectadas a tiempo o los rechazos fitosanitarios masivos en aduanas extranjeras provocan suspensiones de contratos y despidos masivos en las plantas de empaque y campos de cultivo. Al optimizar y dar visibilidad a la cadena de valor operativa mediante la detección de anomalías, esta tesis contribuye indirectamente a la protección del empleo agrario formal y a la reducción de la vulnerabilidad económica de las comunidades rurales peruanas, promoviendo el desarrollo regional sostenible.

#### `1.7.2. Importancia.`
> La importancia práctica de esta investigación radica en entregar un prototipo auditable y trazable alineado con los desafíos de gobernanza de la inteligencia artificial en el Perú. Bajo el marco regulatorio del Decreto Supremo N.° 115-2025-PCM y el estándar internacional del NIST AI Risk Management Framework, los sistemas basados en IA aplicados a la toma de decisiones críticas deben ser transparentes, seguros y explicables para el usuario. Esta tesis rompe con el paradigma de los modelos predictivos tipo "caja negra" al traducir puntuaciones numéricas abstractas y vectores multidimensionales SHAP en reportes narrativos en lenguaje natural de alta fidelidad factual. 
> 
> La solución es de suma importancia para analistas logísticos, supervisores de operaciones, gerentes de calidad y auditores de TI, puesto que les permite entender instantáneamente qué factores determinan una alerta operativa (por ejemplo, si el desvío es causado por anomalía de volumen o por variables climatológicas extremas) y rastrear la evidencia de vuelta a las bases de datos originales de SUNAT o MIDAGRI. Esto no solo acelera la velocidad de reacción corporativa, sino que democratiza el acceso a la IA para profesionales sin conocimientos en ciencia de datos, garantizando una supervisión humana efectiva y responsable sobre la tecnología.

### 2.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** El reglamento de tesis de la UNSA requiere estructurar la justificación bajo tres enfoques bien definidos: Teórica (el aporte al conocimiento y a la ingeniería), Económica (el impacto financiero en el sector o empresa) y Social (el impacto en las personas o empleo). Adicionalmente, separa la "Importancia" como una sección independiente `1.7.2` orientada a la utilidad práctica. 
> 
> Al redactar detalladamente estos apartados, se dota a la tesis de un sustento académico sólido que justifica el esfuerzo de investigación, conectando los algoritmos de IA con la realidad económica y social de la agroexportación peruana.

---

## Punto 3: Alcance de la Investigación (Sección 1.8)

### 3.1 Estado Anterior (Antes)
El borrador Markdown original definía el alcance en viñetas simples y con una delimitación metodológica general:
```markdown
**Alcance tematico:** prediccion tabular, deteccion de anomalias, explicabilidad SHAP, reportes RAG, trazabilidad de datos y documentacion metodologica. Se excluyen modelos de deep learning puro como propuesta principal, despliegue productivo en tiempo real y reemplazo de decision humana.

**Alcance geografico/productivo:** agroexportacion peruana. Productos nucleo: palta, uva y arandano. Producto secundario: esparrago, condicionado a validacion. Producto excluido: cacao.

**Alcance temporal:** dataset estatico o semiestatico basado en datos historicos disponibles hasta 2026. La evaluacion no implica monitoreo en produccion.
```

### 3.2 Nuevo Contenido Propuesto (Después)
Se define de forma exhaustiva, delimitada y justificada cada dimensión de los alcances y exclusiones de la propuesta de investigación:

#### `1.8. Alcance`
##### `1.8.1. Delimitación Temática y Tecnológica`
> La investigación abarca el diseño, implementación y evaluación experimental de un prototipo de software integrado para la supervisión operativa del sector agroexportador peruano. Tecnológicamente, el sistema se acota a una arquitectura estructurada en cuatro capas analíticas secuenciales y de complejidad incremental:
> 1. **Capa 1: Predicción Tabular de Valores Esperados:** Implementación de modelos de aprendizaje supervisado basados en árboles de decisión de aumento de gradiente (GBDT), específicamente *XGBoost* y *LightGBM*, entrenados para resolver tareas de regresión (estimación de valores esperados de precio FOB por kilogramo o volumen de embarque) sobre datos tabulares multivariados. Se excluyen otros modelos supervisados no basados en árboles debido a su menor eficiencia empírica en el modelado de datos tabulares de escala empresarial.
> 2. **Capa 2: Ensemble Unificado de Detección de Anomalías:** Configuración de un ensemble no supervisado mediante la librería *PyOD*, que combina tres algoritmos con principios matemáticos complementarios: *Isolation Forest* (método inductivo basado en particionamiento de espacio para identificar outliers globales), *Local Outlier Factor* (LOF, método densitométrico local para identificar outliers contextuales en vecindarios locales) y *Empirical Cumulative Distribution Outlier Detection* (ECOD, método estadístico no paramétrico basado en funciones de distribución acumulada para estimar la probabilidad de cola de las observaciones en múltiples dimensiones). La unificación de puntuaciones se realiza mediante escalamiento Min-Max y promedio simple.
> 3. **Capa 3: Explicabilidad Post-Hoc Local:** Generación de explicaciones locales para cada alerta de anomalía aduanera u operativa mediante la librería *SHAP*, implementando la formulación optimizada *TreeSHAP*. Esta capa calcula los valores de Shapley para medir la contribución marginal de cada variable de entrada (comercio exterior, clima, mercado interno, logística, sanidad) en el score de anomalía generado, identificando la magnitud y dirección (positiva o negativa) del impacto de cada variable, sin establecer relaciones de causalidad física o real.
> 4. **Capa 4: Generación Automatizada de Reportes Narrativos (RAG):** Desarrollo de un mecanismo de generación en lenguaje natural utilizando una arquitectura de Recuperación Aumentada por Generación (RAG). El ámbito tecnológico de esta capa se restringe a un modelo de lenguaje de gran tamaño (LLM) acotado mediante *prompt engineering* estricto, donde el prompt de entrada se construye dinámicamente inyectando de forma exclusiva la evidencia estructurada de la alerta (valores reales del registro, score del ensemble, umbral de detección, variables top-k de SHAP con sus respectivas atribuciones numéricas, y metadatos de las fuentes). El LLM tiene prohibido realizar búsquedas libres en internet o recuperar conocimiento externo de sus pesos, limitando su labor a la síntesis narrativa y redacción formal de informes técnicos trazables en español.

##### `1.8.2. Delimitación Geográfica y Productiva`
> * **Ámbito Geográfico:** La investigación se enfoca en el análisis de las operaciones agroexportadoras de la costa y valles interandinos de la República del Perú. Específicamente, el modelado y evaluación se restringe a los cinco departamentos con mayor volumen de agroexportación y densidad de registros aduaneros: La Libertad, Piura, Ica, Lambayeque y Arequipa. Las operaciones de otros departamentos quedan fuera del alcance directo del estudio, aunque el diseño metodológico es genérico y reproducible para otras regiones.
> * **Ámbito Productivo (Cultivos):** El estudio se delimita a tres productos núcleo seleccionados por su alta representatividad comercial y complejidad logística: la palta (*Persea americana*), la uva de mesa (*Vitis vinifera*) y el arándano (*Vaccinium corymbosum*). Adicionalmente, el espárrago (*Asparagus officinalis*) se incorpora como un cultivo secundario con el fin de evaluar la robustez de los modelos ante variaciones en la disponibilidad y granularidad de los datos. Se excluye explícitamente el cultivo de cacao (*Theobroma cacao*) debido a que el análisis forense del dataset aduanero identificó una baja representatividad transaccional (solo 379 registros en la ventana de tiempo evaluada), lo que impide un entrenamiento estadísticamente estable y libre de sesgos para modelos de clasificación o regresión multivariados.

##### `1.8.3. Delimitación Temporal y de Datos`
> * **Ventana Temporal de Evaluación:** La ventana temporal histórica abarca un periodo continuo de 8 años, desde **junio de 2018 hasta mayo de 2026** inclusive. Este rango permite capturar ciclos estacionales completos, eventos macroeconómicos de impacto local y el comportamiento de las exportaciones bajo diferentes condiciones climáticas (incluyendo los efectos de fenómenos del Niño).
> * **Naturaleza del Dataset Integrado:** El dataset utilizado para el entrenamiento y validación de los modelos tiene un volumen total consolidado de **40,289 registros transaccionales**. Metodológicamente, se declara que los datos no provienen de una única fuente homogénea, sino de un dataset agroexportador integrado y trazable estructurado en cuatro tipos de variables según su origen y nivel de agregación:
>   1. *Datos reales observados:* Microdatos transaccionales de aduanas por embarque obtenidos de SUNAT/ADUANET (archivos de manifiestos y declaraciones aduaneras en formato DBF parseados localmente).
>   2. *Datos reales agregados:* Series temporales de precios mayoristas del mercado local obtenidos del SISAP/MIDAGRI (formato CSV diario), estadísticas macroeconómicas del tipo de cambio mensual provenientes del BCRP, y datos de contraste comercial internacional de Trade Map.
>   3. *Variables contextuales proxies:* Estimaciones climáticas de radiación, temperatura y humedad acumuladas por coordenadas semanales obtenidas de la base de datos NASA POWER, y registros de alertas sanitarias mensuales agregadas de SENASA y la FDA.
>   4. *Datos sintéticos controlados:* Empleados estrictamente para complementar vacíos temporales de datos públicos, balanceo de clases altamente desbalanceadas en la evaluación de anomalías o inyectar escenarios experimentales de anomalías simuladas con fines de validación técnica de la Capa 2 y Capa 4, garantizando que el origen metodológico de cada registro esté etiquetado de forma transparente.

##### `1.8.4. Delimitación Operativa y de Evaluación`
> * **Entorno de Ejecución Computacional:** La ejecución, entrenamiento y evaluación de los modelos del pipeline se restringe a un entorno computacional local estándar compuesto por recursos de procesamiento en CPU convencional (procesador comercial de gama media, 16 GB de memoria RAM, sin dependencia de aceleración por GPU corporativa o de alta gama), demostrando la viabilidad de bajo costo del sistema para el sector académico y PYME.
> * **Esquema de Evaluación del Sistema:** La evaluación del sistema integrado se delimita a experimentos controlados (E1 a E5) utilizando una división de datos temporal estricta (70% entrenamiento cronológico, 10% validación de hiperparámetros con Optuna y 20% test cronológico final) para evitar la filtración de información (*data leakage*).
> * **Estudio de Usabilidad Operativa (VD4):** La evaluación de la usabilidad y la reducción del tiempo de decisión se limita a una prueba experimental controlada con un grupo de evaluadores de perfil profesional en ingeniería, administración o logística (tamaño de muestra N = 15 a 27 participantes, bajo un diseño experimental intra-sujetos o *within-subjects*). La prueba evaluará el impacto del uso de reportes integrados y explicaciones SHAP frente a un flujo de salida técnica tradicional (datos crudos y scores sin explicación narrativa). No se contempla una validación con usuarios en entornos productivos de empresas reales ni integraciones de software con sus ERPs activos.

##### `1.8.5. Delimitación Regulatoria y de Principios de Gobernanza`
> La investigación no busca obtener una certificación formal de cumplimiento legal ni auditar procesos comerciales de una corporación real. El alcance se limita a la **conformidad de diseño** con los principios de gobernanza algorítmica y supervisión humana recomendados en los marcos normativos nacionales e internacionales vigentes:
> 1. **Decreto Supremo N° 115-2025-PCM (Reglamento de la Ley de Inteligencia Artificial en Perú):** El diseño de la Capa 4 (RAG) y los anexos de Model Cards (Anexo B) y Datasheets (Anexo C) adoptan los lineamientos de transparencia, trazabilidad de datos y supervisión humana ("humano en el bucle" u *human-in-the-loop*), asegurando que el sistema actúe como un asistente consultivo y no reemplace la firma o decisión del auditor humano.
> 2. **Resolución SBS N° 053-2023 (Reglamento de Gestión de Riesgos de Modelos):** Se toma como estándar metodológico de referencia para la documentación y validación de las variables independientes, la trazabilidad del pipeline de datos y la declaración explícita de limitaciones del modelo, aunque el sector agroexportador no se encuentre bajo la supervisión de la Superintendencia de Banca, Seguros y AFP.
> 3. **NIST AI Risk Management Framework (AI RMF 1.0) y EU AI Act:** El prototipo adopta la categorización de riesgos y las directrices de explicabilidad local para justificar la integración de la Capa 3 (SHAP) como interfaz de auditoría, limitando la validez del cumplimiento normativo a un alineamiento conceptual metodológico de diseño del software.

##### `1.8.6. Exclusiones Explícitas de la Investigación`
> Para salvaguardar la frontera del proyecto frente a observaciones de jurados o exigencias fuera del marco de la tesis, se excluye expresamente del alcance de este trabajo:
> 1. La implementación productiva en tiempo real o integraciones en producción mediante APIs o WebSockets con servidores corporativos activos de empresas agroexportadoras.
> 2. El uso de redes neuronales profundas (Deep Learning) orientadas a datos tabulares (como TabNet o FT-Transformer) como propuesta principal de la arquitectura, quedando estas restringidas exclusivamente a baselines comparativos.
> 3. La automatización de la toma de decisiones directas o el reemplazo del criterio de los supervisores y analistas humanos; el sistema opera estrictamente como soporte a las decisiones bajo el esquema de "humano en el bucle" (*human-in-the-loop*).
> 4. El cacao (*Theobroma cacao*) como producto de estudio principal, debido a que el análisis documental forense inicial identificó una baja densidad transaccional (379 registros) insuficiente para el entrenamiento estable de los modelos tabulares.

### 3.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** El alcance de una tesis de Ingeniería de Sistemas debe delimitar con extrema claridad la frontera tecnológica, física, operativa y de datos de la propuesta. Si no se delimita rigurosamente, el jurado puede exigir integraciones productivas en producción real, el uso de costosas GPUs para modelos de Deep Learning que no se adecúan al volumen de datos tabulares, o culpar al sistema de reemplazar la decisión humana, lo que violaría normativas vigentes sobre ética en IA.
> 
> Al estructurar el alcance en subsecciones específicas para cada dimensión (temático-tecnológica, geográfica, temporal, operativa y regulatoria) y declarar explícitamente las exclusiones clave (como la exclusión del cacao por inviabilidad estadística de muestras y el rol auxiliar del sistema "humano-en-el-bucle"), la tesis se blinda metodológicamente. Esto permite al tesista defender el proyecto dentro de límites realistas, reproducibles y alineados con la normativa nacional (D.S. N° 115-2025-PCM) e internacional (NIST AI RMF).

---

## Punto 4: Estructura de las Técnicas e Instrumentos de Recolección (Sección 1.10)

### 4.1 Estado Anterior (Antes)
La tabla original presentaba campos simplificados y carecía de especificaciones concretas de los instrumentos técnicos de software desarrollados en la tesis:
```markdown
## 1.10 Tecnicas e instrumentos de recoleccion

| Tecnica | Instrumento | Uso |
|---|---|---|
| Revision bibliografica | Bases academicas y literatura tecnica | Estado del arte. |
| Analisis documental | SUNAT, MIDAGRI, BCRP, Trade Map, SENAMHI, SENASA, APN/OSITRAN | Construccion de fuentes y proxies. |
| Experimentacion controlada | Pipeline de modelos y splits temporales | Evaluacion tecnica. |
| Evaluacion con usuarios/evaluadores | Cuestionarios, logs de tiempo, rubricas | VD2, VD3, VD4 y VD5. |
```

### 4.2 Nuevo Contenido Propuesto (Después)
Se implementa y completa la matriz oficial con la terminología académica de la propuesta de sistemas:

| Técnica | Instrumento | Propósito |
| :--- | :--- | :--- |
| **Análisis Documental** | Ficha de registro de datos estructurados (CSV/DBF) | Recolección e integración de microdatos de comercio exterior (SUNAT/ADUANET), mercado interno (SISAP/MIDAGRI), indicadores macroeconómicos (BCRP) y datos climáticos (NASA POWER). |
| **Experimentación Controlada** | Entorno de desarrollo (Python/VS Code) y Scripts de pruebas | Medición del rendimiento predictivo tabular (XGBoost/LightGBM) y de la precisión del ensemble de anomalías operativas (Isolation Forest, LOF, ECOD). |
| **Encuesta** | Cuestionario Tipo Likert y Métricas de logs de decisión | Evaluación cualitativa de la usabilidad del sistema, tiempo de decisión de los analistas, y nivel de confianza y comprensión de las alertas explicadas frente a reportes convencionales. |

### 4.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** En las tesis de Ingeniería de Sistemas, los "instrumentos" no deben limitarse a cuestionarios o encuestas de ciencias sociales. En proyectos de desarrollo tecnológico y de IA, los scripts de prueba, las fichas de registro estructuradas de bases de datos relacionales y las consolas de experimentación de software son los instrumentos de recolección primarios. 
> 
> Este cambio formaliza que la experimentación de los modelos XGBoost/LightGBM/PyOD y el análisis documental de microdatos transaccionales de la SUNAT constituyen herramientas con rigor de ingeniería.

---

## Punto 5: Secciones del Marco Conceptual (Sección 2.3)

### 5.1 Estado Anterior (Antes)
El borrador en Markdown utilizaba subtítulos personalizados libres que no encajaban en la estructura fija definida en la plantilla oficial.

### 5.2 Nuevo Contenido Propuesto (Después)
Se reestructuran los 9 subcapítulos con su contenido y citas bibliográficas exactas:

#### `2.3.1. Reconocimiento de patrones`
### 2.3.1 Reconocimiento de Patrones y Aprendizaje Automático

El reconocimiento de patrones es la disciplina de la inteligencia artificial que busca identificar regularidades, estructuras o relaciones en datos a partir de ejemplos históricos. En el aprendizaje automático, este proceso se formaliza mediante modelos que aprenden una función $f: X \rightarrow Y$ a partir de un conjunto de entrenamiento $\{(x_i, y_i)\}_{i=1}^n$, con el objetivo de generalizar hacia instancias no observadas.

Se distinguen tres paradigmas principales: **aprendizaje supervisado**, donde el modelo aprende de etiquetas explícitas (e.g., operación normal / operación anómala); **aprendizaje no supervisado**, que identifica patrones sin etiquetas y es fundamental en la detección de anomalías; y **aprendizaje semi-supervisado**, que combina ambos cuando el etiquetado es costoso o escaso, escenario habitual en procesos agroexportadores donde no todas las desviaciones quedan registradas formalmente.

En el contexto de esta investigación, el reconocimiento de patrones opera en dos dimensiones complementarias: la detección de registros operativos anómalos (patrones puntuales) y la identificación de secuencias temporales de comportamiento irregular (patrones colectivos), requiriendo tanto modelos de clasificación supervisada como detectores de anomalías no supervisados.

#### `2.3.2. Aprendizaje automático (Machine Learning)`
### 2.3.2 Datos Tabulares en Sistemas Agroexportadores Empresariales

Los datos tabulares son la forma predominante de almacenamiento en los sistemas de información empresarial: cada fila representa una instancia operativa y cada columna una variable. En agroexportación, una instancia puede describir un lote, día, producto, zona, envío o registro de mercado; las columnas pueden incluir precio, volumen, temperatura, precipitación, humedad, destino, cumplimiento fitosanitario, días logísticos, merma y etiqueta de anomalía.

Estas propiedades estructurales explican por qué los GBDT son adecuados para este dominio (Grinsztajn et al., 2022): manejan variables numéricas y categóricas heterogéneas, toleran valores faltantes, capturan relaciones no lineales y requieren menor ingeniería de features que arquitecturas neuronales complejas. Cuando las etiquetas de anomalía son escasas o desbalanceadas, el rendimiento debe evaluarse con métricas orientadas a precisión-recall (PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad)), F1-Score (Medida Armónica de Precisión y Exhaustividad) y análisis de falsos positivos.

#### `2.3.3. Modelos basados en árboles y Gradient Boosting`
### 2.3.3 GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente)

Los Gradient Boosting Decision Trees (GBDT) son una familia de algoritmos de aprendizaje supervisado que construyen modelos predictivos mediante la combinación secuencial de múltiples árboles de decisión débiles. El enfoque fue formalizado por Friedman (2001) como "Greedy Function Approximation", donde cada árbol nuevo se ajusta para corregir los errores residuales del conjunto de árboles previos mediante descenso de gradiente en el espacio funcional de la función de pérdida.

La formulación matemática central de GBDT busca encontrar una función $F(x)$ que minimice la pérdida esperada:

$$F^*(x) = \arg\min_{F} \mathbb{E}_{y,x}[L(y, F(x))]$$

donde $L$ es la función de pérdida (e.g., entropía cruzada para clasificación, MSE para regresión) y la minimización se realiza iterativamente añadiendo árboles de regresión $h_m(x)$ con pesos de aprendizaje $\nu$:

$$F_m(x) = F_{m-1}(x) + \nu \cdot h_m(x)$$

**XGBoost** (Chen & Guestrin, 2016) introduce mejoras clave sobre el GBDT estándar: regularización L1 y L2 en la función objetivo para controlar la complejidad del modelo, manejo nativo de valores faltantes mediante aprendizaje automático de la dirección de ramificación, y paralelización por columnas en lugar de por filas, lo que habilita el procesamiento en datasets de alta dimensión.

**LightGBM** (Ke et al., 2017) acelera el entrenamiento mediante dos innovaciones: Gradient-based One-Side Sampling (GOSS), que retiene las muestras con mayor gradiente y descarta aleatoriamente las de menor gradiente, preservando la distribución sin pérdida estadística significativa; y Exclusive Feature Bundling (EFB), que agrupa features mutuamente excluyentes para reducir dimensionalidad efectiva. El resultado es una aceleración de hasta 20× sobre XGBoost con precisión comparable.

**CatBoost** (Prokhorenkova et al., 2018) resuelve el problema del target leakage en variables categóricas mediante Ordered Boosting: calcula las estadísticas de objetivo para cada categoría usando únicamente las observaciones previas en un orden aleatorio permutado, evitando que la información del objetivo filtre hacia las features de entrada durante el entrenamiento. Esta propiedad es especialmente relevante en datos contables, donde variables como "código de cuenta" o "centro de costo" tienen alta cardinalidad.

La justificación empírica para elegir GBDT sobre Deep Learning en datos tabulares empresariales está sólidamente documentada por (Grinsztajn et al., 2022): en 45 datasets con hasta 50,000 muestras, los GBDT superan a arquitecturas neuronales complejas (como FT-Transformer o TabNet) en la inmensa mayoría de los casos. Dado que el dataset operativo de esta tesis se define como un dataset agroexportador integrado de escala tabular, con datos reales observados, datos agregados, proxies y datos sintéticos controlados, se sitúa en el rango donde los modelos basados en árboles maximizan su ventaja comparativa. Esta superioridad es atribuible a tres propiedades estructurales de los datos tabulares que los árboles aprovechan mejor que las redes neuronales.

### 2.3.4 Detección de Anomalías y Estrategia de Ensemble

La detección de anomalías es el problema de identificar observaciones que se desvían significativamente del comportamiento esperado del conjunto de datos. La literatura distingue tres tipos fundamentales de anomalías (Han et al., 2022): (a) **puntuales** — instancias individuales anómalas (e.g., una transacción de monto atípico); (b) **contextuales** — instancias que son anómalas en un contexto particular pero no en general (e.g., un cargo nocturno inusual para un perfil de usuario); y (c) **colectivas** — secuencias de instancias que son anómalas en conjunto aunque cada una individualmente no lo sea (e.g., un patrón de micro-transacciones).

**Isolation Forest** (Liu et al., 2008) se basa en el principio de que las anomalías son "pocas y diferentes": son más fáciles de aislar que los puntos normales mediante particionamiento aleatorio del espacio. Un árbol de aislamiento selecciona aleatoriamente una feature y un valor de corte; la anomalía será aislada en pocas particiones (camino corto), mientras que los puntos normales requieren muchas particiones (camino largo). El score de anomalía es el inverso de la longitud promedio del camino de aislamiento, normalizada según la longitud esperada para un punto normal en un conjunto de tamaño $n$. La complejidad es O(n log n) en entrenamiento y O(n) en inferencia.

**Local Outlier Factor (LOF (Local Outlier Factor - Factor de Anomalía Local))** (Breunig et al., 2000) cuantifica el grado de anomalía de cada punto en función de la densidad de su vecindario local respecto a la densidad de sus vecinos. El score LOF para el punto $p$ se define como:

$$\text{LOF}_k(p) = \frac{\sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}}{|N_k(p)|}$$

donde $\text{lrd}_k$ es la densidad de alcanzabilidad local. Un valor LOF >> 1 indica que $p$ tiene densidad local mucho menor que sus vecinos, lo que lo caracteriza como anomalía. LOF es sensible a variaciones locales de densidad, lo que lo hace complementario a Isolation Forest en datasets heterogéneos.

**Deep SVDD** (Ruff et al., 2018) extiende el Support Vector Data Description al espacio de representación de redes neuronales: entrena una red para mapear los datos normales hacia el interior de una hipersfera mínima en el espacio latente. Las anomalías se detectan como puntos que caen fuera o lejos de esta hipersfera. La función objetivo minimiza el volumen de la hipersfera:

$$\min_{W, R, c} R^2 + \frac{1}{\nu n} \sum_{i=1}^{n} \max(0, \|f(x_i; W) - c\|^2 - R^2)$$

donde $f(x_i; W)$ es la representación de la red neuronal, $c$ es el centro de la hipersfera y $R$ es su radio.

**ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica)** (Li et al., 2022) calcula el score de anomalía como la probabilidad acumulada de observar un punto tan extremo como $x$ bajo la distribución empírica del dataset, estimada mediante funciones de distribución acumulada (ECDF) multivariadas. Su ventaja principal es que no tiene hiperparámetros que calibrar, eliminando el riesgo de sobreajuste y simplificando el despliegue en producción.

La estrategia de **ensemble** consolida las puntuaciones de múltiples detectores para reducir la varianza del estimador agregando perspectivas de densidad local (LOF), aislamiento espacial (IF) y probabilidad empírica acumulada (ECOD). Sin embargo, un desafío matemático fundamental radica en que los algoritmos marginales producen puntuaciones en escalas y naturalezas numéricas completamente incompatibles:
1. **Isolation Forest** genera puntuaciones acotadas $S_{IF}(x) \in [0, 1]$.
2. **Local Outlier Factor** genera puntuaciones $S_{LOF}(x) \in [1, \infty)$, donde valores cercanos a 1 indican normalidad y valores superiores representan el grado local de desviación.
3. **ECOD** genera puntuaciones acumuladas inversas $S_{ECOD}(x) \in [0, \infty)$ en escalas de log-probabilidad.

Sumar o promediar estos valores en bruto anularía la influencia de IF y ECOD debido a que LOF dominaría la agregación por magnitud. Para resolver esta incompatibilidad, esta tesis implementa la unificación probabilística de puntuaciones basada en el escalamiento Min-Max lineal calibrado sobre el conjunto de entrenamiento (Kriegel et al., 2011). Las puntuaciones brutas de cada detector se transforman en puntuaciones probabilísticas de anomalía acotadas $P_m(a|x) \in [0, 1]$ mediante la función de mapeo:

$$P_m(a|x) = \max\left(0, \min\left(1, \frac{S_m(x) - \min_{x' \in D_{train}}(S_m(x'))}{\max_{x' \in D_{train}}(S_m(x')) - \min_{x' \in D_{train}}(S_m(x'))}\right)\right)$$

donde $\min_{D_{train}}$ y $\max_{D_{train}}$ son los valores extremos de score observados en el conjunto de calibración histórica del detector $m$. La puntuación consolidada de anomalía del ensemble $S_{Ensemble}(x) \in [0, 1]$ se calcula entonces como el promedio simple de estas probabilidades unificadas:

$$S_{Ensemble}(x) = \frac{P_{IF}(a|x) + P_{LOF}(a|x) + P_{ECOD}(a|x)}{3}$$

Una instancia operativa $x$ se clasifica finalmente como alerta anómala si y solo si $S_{Ensemble}(x) \ge \tau$, donde $\tau \in [0, 1]$ es el umbral de decisión operativo global calibrado empíricamente en la fase de validación cruzada. El fundamento teórico de este enfoque de agregación lo proporciona ADBench (Han et al., 2022) y su implementación robusta se realiza mediante la API modular de PyOD (Zhao et al., 2019).

### 2.3.5 Forecasting de Series Temporales con Transformers

Las series temporales agroexportadoras presentan tres desafíos que los modelos de forecasting deben resolver: tendencia no estacionaria, estacionalidad múltiple (diaria, semanal, mensual, anual) y dependencia de covariables exógenas (clima, calendario agrícola, demanda internacional, precios y condiciones logísticas). Los modelos estadísticos clásicos como ARIMA capturan relaciones lineales con eficacia, pero presentan limitaciones en la modelización de no-linealidades y horizontes largos.

**Temporal Fusion Transformer (TFT)** (Lim et al., 2021) propone una arquitectura especializada que combina cuatro mecanismos: (1) codificación LSTM para dependencias secuenciales locales; (2) selección de variables con mecanismo de gating (GLU — Gated Linear Unit) que identifica automáticamente las covariables más informativas; (3) atención multi-cabezal interpretable que pondera los pasos temporales según su relevancia predictiva; y (4) red de cuantiles para cuantificar la incertidumbre de la predicción. TFT acepta tres tipos de entradas: features estáticas conocidas (e.g., producto, zona, destino), covariables futuras conocidas (e.g., calendario agrícola, campañas, feriados) y covariables históricas observadas (e.g., precio, volumen, clima o merma pasada).

El debate sobre la efectividad de los Transformers en series temporales es relevante para esta tesis. Zeng et al. (2023) argumentan que DLinear —un modelo lineal simple— supera a los Transformers en múltiples benchmarks, atribuyendo la limitación de los Transformers al hecho de que el mecanismo de self-attention es permutation-invariant y destruye el orden temporal de las secuencias. Sin embargo, este argumento ha sido rebatido sucesivamente: Nie et al. (2023) demuestran que la tokenización por patches —agrupando segmentos temporales antes de aplicar atención— preserva el orden local y supera a DLinear en la mayoría de benchmarks de horizonte largo. Liu et al. (2024) proponen invertir la tokenización: en lugar de tokenizar por timestamp, tokenizan por variable, aplicando self-attention entre variables en lugar de entre tiempos, obteniendo SOTA en 7 datasets multivariados.

**Posición de esta tesis respecto al debate**: TFT se considera por su interpretabilidad incorporada —el mecanismo de gating y los mapas de atención son legibles por analistas— más que exclusivamente por su rendimiento predictivo. En el contexto agroexportador, la capacidad de justificar qué períodos temporales y qué covariables fundamentan la predicción es un requerimiento funcional comparable en importancia a la precisión numérica.

N-HiTS (Challu et al., 2022) ofrece una alternativa no-Transformer para forecasting de horizonte largo, con interpolación jerárquica multi-tasa que reduce la complejidad computacional respecto a N-BEATS. Chronos (Ansari et al., 2024) representa el paradigma emergente de los foundation models para series temporales, basado en T5, que logra performance zero-shot competitivo en múltiples datasets; sin embargo, su opacidad y dependencia de infraestructura de gran escala limitan su aplicación directa cuando se requiere trazabilidad operativa.

### 2.3.6 Explicabilidad mediante SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)

La explicabilidad en sistemas de IA se clasifica en dos grandes categorías: **inherente** —modelos cuya estructura es intrínsecamente interpretable, como los árboles de decisión— y **post-hoc** —métodos aplicados a cualquier modelo después del entrenamiento para interpretar sus predicciones. SHAP y LIME son los dos métodos post-hoc agnósticos más adoptados en la literatura.

**LIME** (Local Interpretable Model-agnostic Explanations) (Ribeiro et al., 2016) genera explicaciones locales construyendo un modelo lineal sustituto en el vecindario de la instancia a explicar, ponderando las muestras según su proximidad al punto de interés. LIME es rápido y flexible, pero produce explicaciones inestables: pequeñas perturbaciones de la instancia pueden cambiar significativamente la explicación, un problema crítico en contextos forenses.

**SHAP** (Lundberg & Lee, 2017) fundamenta las explicaciones en los valores de Shapley de la teoría de juegos cooperativos. El valor SHAP de la feature $i$ para la predicción $f(x)$ cuantifica la contribución marginal media de $i$ a la predicción, promediando sobre todas las coaliciones posibles de features:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!} [f(S \cup \{i\}) - f(S)]$$

donde $F$ es el conjunto de todas las features y $S$ es una coalición de features sin $i$. Esta formulación garantiza cuatro propiedades axiomáticas: (a) **eficiencia** — la suma de todos los valores SHAP iguala la diferencia entre la predicción y el valor esperado; (b) **simetría** — features con contribución idéntica reciben el mismo valor; (c) **dummy** — features sin efecto tienen valor cero; y (d) **aditividad** — los valores SHAP son consistentes al combinar modelos.

SHAP resuelve las limitaciones de LIME al garantizar consistencia: si un modelo cambia la predicción al aumentar la contribución de una feature, el valor SHAP de esa feature nunca disminuye (Lundberg & Lee, 2017). **TreeSHAP** extiende este cálculo con un algoritmo exacto en O(TLD²) para modelos basados en árboles —donde T es el número de árboles, L es el número de hojas por árbol y D es la profundidad máxima— haciendo el cálculo computacionalmente viable para GBDT en producción.

En el contexto de supervisión operativa, la estabilidad de las explicaciones permite verificar que el modelo asigna importancias consistentes a variables semejantes. Un índice alto de estabilidad fortalece la confianza en el sistema, porque evita que alertas similares reciban justificaciones contradictorias.

La integración SHAP+LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño) de esta tesis opera como sigue: los vectores SHAP de una alerta operativa (una lista de pares variable→contribución cuantitativa) se incorporan como contexto verificado en el RAG, y el LLM genera la narración del informe sin posibilidad de inventar cifras que no estén en esos vectores o en las fuentes recuperadas.

### 2.3.7 Modelos de Lenguaje y Arquitectura RAG para Generación de Reportes

Los LLMs (Large Language Models - Modelos de Lenguaje de Gran Tamaño) son sistemas entrenados mediante autoregresión en corpus masivos de texto para aprender distribuciones probabilísticas sobre secuencias de tokens. Su capacidad de generalización les permite realizar tareas de reasoning, traducción, resumen y generación de texto con calidad próxima a la humana en configuraciones zero-shot y few-shot.

**In-context learning** permite guiar el comportamiento del LLM mediante ejemplos incluidos directamente en el prompt, sin necesidad de ajuste fino (fine-tuning). TabLLM (Hegselmann et al., 2023) demostró que mediante serialización de datos tabulares a texto descriptivo, los LLMs pueden realizar clasificación sobre datos estructurados con rendimiento no trivial en zero-shot, ampliando el espectro de aplicación de estos modelos más allá del texto no estructurado.

Sin embargo, el uso de LLMs como agentes de decisión autónoma introduce el riesgo de **alucinaciones**: el modelo puede generar afirmaciones coherentes en forma pero incorrectas en contenido (Ji et al., 2023; Maynez et al., 2026). La literatura distingue al menos dos tipos: (a) alucinaciones intrínsecas, en las que el texto generado contradice la información del contexto recuperado; y (b) alucinaciones extrínsecas, en las que el modelo inventa información no presente en el contexto. En particular, las "alucinaciones numéricas" —valores específicos de métricas, porcentajes o fechas que no corresponden a los datos reales (Barclays Research, 2025)— son especialmente peligrosas en reportes operativos, porque pueden inducir decisiones equivocadas pese a la apariencia de precisión cuantitativa.

**RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)** (Lewis et al., 2020; Schneider et al., 2025) reduce este riesgo al separar el conocimiento factual del modelo generativo: en lugar de que el LLM "recuerde" información de su entrenamiento, el sistema recupera documentos o datos relevantes de una base de conocimiento externa verificada y los incluye en el contexto del prompt. El LLM entonces genera texto fundamentado en esos datos recuperados, no en su memoria paramétrica. Es importante señalar que RAG **reduce significativamente pero no elimina** el riesgo de alucinación; persisten casos de alucinación intrínseca (faithful hallucination) en los que el modelo genera afirmaciones que se desvían del contexto recuperado. Técnicas avanzadas como GraphRAG incorporan grafos de conocimiento para recuperación semántica más rica, mientras que Self-RAG permite al modelo verificar la pertinencia de los documentos recuperados antes de usarlos.

En la arquitectura de esta tesis, la "base de conocimiento" del RAG son los vectores SHAP de la alerta analizada, las métricas del ensemble de detección, las fuentes agroexportadoras recuperadas y las reglas de reporte definidas. El LLM recibe ese contexto verificado y genera el informe narrativo sin acceso a conocimiento adicional no validado. Adicionalmente se aplican dos controles complementarios: (a) plantillas de prompt estructurado con campos obligatorios (dato, modelo, score, umbral, explicación SHAP, fuente recuperada), y (b) validación posterior del reporte contra los vectores SHAP de entrada para detectar discrepancias numéricas. Este diseño permite que cada afirmación del reporte pueda trazarse hasta una fuente, score, umbral o variable explicativa.

La evaluación de calidad de los reportes generados puede utilizar **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) cuando exista un texto de referencia. Sin embargo, para esta tesis se prioriza una rúbrica operativa de completitud, consistencia, accionabilidad y correspondencia con evidencias, porque la calidad de un reporte de supervisión depende no solo de similitud textual, sino de su utilidad para la toma de decisiones.

### 2.3.8 Gobernanza de IA y MLOps

El despliegue de sistemas de IA en entornos empresariales críticos requiere un marco de gobernanza que trascienda el rendimiento técnico. Sculley et al. (2015) documentaron la "deuda técnica oculta" en sistemas de ML: más del 95% del código de un sistema ML de producción no es el modelo en sí, sino la infraestructura de ingesta, validación, features, servicio y monitoreo. Los pipelines con alto acoplamiento entre componentes generan "entanglement" que dificulta el mantenimiento y aumenta el riesgo de regresiones silenciosas.

**MLOps** (Kreuzberger et al., 2022) establece el conjunto de prácticas para gestionar el ciclo de vida completo de los modelos ML en producción: integración y entrega continua (CI/CD) para modelos, monitoreo de data drift y model drift, automatización del reentrenamiento, y trazabilidad de versiones de datos, código y modelos. En el contexto de supervisión operativa agroexportadora, MLOps permite reproducir qué modelo generó una alerta, con qué datos de entrada, bajo qué versión y con qué umbral.

El **NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0)** (NIST, 2023) proporciona cuatro funciones de gestión de riesgo para sistemas de IA: (1) **Govern** — establecer políticas y roles de responsabilidad; (2) **Map** — identificar el contexto de despliegue y los riesgos asociados; (3) **Measure** — evaluar los riesgos con métricas verificables; y (4) **Manage** — implementar controles y mitigaciones. La arquitectura modular de esta tesis es diseñada para que cada capa corresponda a responsabilidades verificables bajo este framework.

**Datasheets for Datasets** (Gebru et al., 2021) propone una plantilla de documentación estandarizada para datasets que detalla: motivación de recolección, proceso de recolección, composición, preprocesamiento aplicado, distribución permitida y consideraciones éticas. Esta práctica se aplicará al dataset agroexportador integrado y a sus capas de datos reales, agregados, proxies y sintéticos controlados, garantizando que los resultados reportados sean reproducibles y que las limitaciones de cada fuente estén identificadas antes de evaluar el sistema.

**Model Cards** (Mitchell et al., 2019) extiende la documentación al nivel del modelo, especificando para quién fue entrenado, en qué condiciones, cuáles son sus limitaciones conocidas y cómo debe usarse de manera responsable. En esta tesis, se elaboran Model Cards para los modelos XGBoost/LightGBM, detectores de anomalías y el componente LLM+RAG, en conformidad con los principios de documentación del NIST AI RMF (NIST, 2023).

El contexto peruano e internacional consolida la necesidad de este framework de gobernanza. El D.S. N° 115-2025-PCM (PCM, 2025), el NIST AI RMF (NIST, 2023) y el EU AI Act (Parlamento Europeo y Consejo, 2024) refuerzan principios comunes: transparencia, documentación, supervisión humana y gestión de riesgos. Estos principios son adoptados como referencia de diseño para esta tesis. No se afirma cumplimiento formal con ninguno de estos marcos —tal afirmación requeriría auditoría regulatoria externa— sino conformidad de diseño con sus principios, en particular: (a) transparencia mediante SHAP y Model Cards, (b) supervisión humana mediante revisión obligatoria de cada reporte antes de su uso operativo, (c) gestión de riesgos mediante umbrales calibrados y validación cruzada, y (d) trazabilidad documental mediante logs completos por alerta. La aplicabilidad regulatoria efectiva del sistema a una empresa específica depende de su clasificación de riesgo bajo el reglamento correspondiente y queda fuera del alcance de esta tesis.

### 2.3.9 Supervisión Operativa, Trazabilidad e Inteligencia Artificial

La supervisión operativa en agroexportación exige monitorear procesos que combinan producción, acopio, calidad, sanidad, logística y comercio exterior. Las anomalías en este dominio no necesariamente corresponden a fraude; pueden representar variaciones atípicas de precio, caídas de volumen, condiciones climáticas adversas, mermas elevadas, incumplimientos fitosanitarios o retrasos logísticos. Por ello, el sistema propuesto se orienta a detectar desviaciones relevantes para la toma de decisiones, no a sustituir procesos de investigación legal o auditoría financiera.

La **supervisión operativa continua** busca reemplazar ciclos de revisión tardíos por monitoreo frecuente y documentado de indicadores. En este enfoque, cada alerta debe registrar el dato de origen, el modelo aplicado, el score calculado, el umbral utilizado, las variables explicativas y el reporte generado. Esta trazabilidad permite que un supervisor operativo comprenda por qué el sistema marcó un evento como anómalo y qué evidencia respalda la recomendación.

La integración de IA en supervisión operativa plantea el problema de la confianza en decisiones automáticas. Esta exigencia convierte a la explicabilidad (SHAP), la documentación de datasets (Datasheets), la documentación de modelos (Model Cards) y los logs de decisión en componentes funcionales del sistema. En el marco peruano, el D.S. N° 115-2025-PCM (PCM, 2025) proporciona una base general para el uso responsable de IA; la Resolución SBS N° 053-2023 (SBS, 2023) se conserva solo como referencia nacional de buenas prácticas para gestión de riesgo de modelos.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

<div style="background-color: orange; color: white; padding: 10px; text-align: center; font-weight: bold; margin-bottom: 20px; border-radius: 5px;">EN DESARROLLO</div>

# CAPITULO III: PROPUESTA METODOLOGICA

## 3.1 Arquitectura del sistema integrado

La arquitectura propuesta se divide en cuatro capas secuenciales y trazables:

1. **Capa 1: Prediccion tabular.** Modelos GBDT, principalmente XGBoost y LightGBM, estiman valores esperados de precio o volumen usando variables comerciales, macroeconomicas, climaticas, logisticas y de contexto.
2. **Capa 2: Deteccion de anomalias.** Un ensemble de Isolation Forest, LOF y ECOD produce un score de anomalia. El LLM no detecta anomalias.
3. **Capa 3: Explicabilidad.** SHAP/TreeSHAP identifica las variables con mayor contribucion a la alerta. Las explicaciones son atribuciones del modelo, no causalidad.
4. **Capa 4: Reportes RAG/LLM.** Un LLM restringido por evidencias redacta reportes tecnicos a partir de datos, score, umbral, SHAP, fuente y metadatos.

```
[Dataset agroexportador integrado]
        |
        v
[Capa 1: GBDT] -> valor esperado / residuo
        |
        v
[Capa 2: IF + LOF + ECOD] -> score anomalia
        |
        v
[Capa 3: SHAP] -> top variables explicativas
        |
        v
[Capa 4: RAG/LLM] -> reporte trazable
```

## 3.2 Dataset agroexportador integrado y trazable

La validacion principal no dependera de un dataset sintetico aislado. Se trabajara con un **dataset agroexportador integrado**, construido desde cuatro tipos de informacion:

| Capa de datos | Fuentes | Rol |
|---|---|---|
| Datos reales observados | SUNAT/ADUANET, `data/dataset_real_v1.csv` | Base primaria de exportaciones. |
| Datos reales agregados | Trade Map, SISAP/MIDAGRI, BCRP, MIDAGRI compendios, FAOSTAT | Validacion externa y contexto. |
| Proxies documentados | NASA POWER, SENAMHI, APN, OSITRAN, SENASA/FDA/RASFF | Variables explicativas agregadas. |
| Datos sinteticos controlados | `data/dataset_agro_sintetico_v1.csv` y reglas de inyeccion | Escenarios auxiliares, balanceo y etiquetas experimentales. |

### 3.2.1 Segmentacion de productos

| Producto | HS | Decision |
|---|---|---|
| Palta | `080440` | Producto nucleo. |
| Uva | `080610` | Producto nucleo. |
| Arandano | `081040` | Producto nucleo; sin dependencia de SISAP. |
| Esparrago | `070920` | Producto secundario condicionado. |
| Cacao | Verificar | Excluido del nucleo por baja representatividad. |

### 3.2.2 Uso de fuentes

- **SUNAT/ADUANET:** fuente primaria para volumen, valor FOB, partida, fecha, empresa y destino.
- **Trade Map:** benchmark internacional por producto y mercado destino.
- **SISAP/MIDAGRI:** precio y volumen mayorista interno para palta, uva y esparrago; no mide exportaciones.
- **BCRP:** tipo de cambio mensual.
- **Clima/logistica/sanidad:** proxies agregados cuando no existe llave directa por embarque.
- **Sinteticos:** escenarios controlados y balanceo, siempre etiquetados.

## 3.3 Configuracion experimental y metricas

### 3.3.1 Division temporal

Para evitar fuga de informacion temporal:

- Train: 70% inicial.
- Validation: 10% siguiente.
- Test: 20% final.

El split aleatorio no se usara como evaluacion principal.

### 3.3.2 Metricas por variable dependiente

| VD | Metricas |
|---|---|
| VD1 rendimiento | PR-AUC, ROC-AUC, F1, precision, recall. |
| VD2 explicabilidad | Cobertura top-k SHAP, estabilidad, claridad. |
| VD3 reportes | Rubrica de completitud, consistencia, accionabilidad y evidencia. |
| VD4 decision | Tiempo-a-decision, Likert, decision correcta. |
| VD5 trazabilidad | Porcentaje de alertas con campos completos. |

### 3.3.3 Experimentos E1-E5

| Exp. | Nombre | Condicion experimental | Control | VD |
|---|---|---|---|---|
| E1 | Rendimiento de deteccion | Ensemble IF + LOF + ECOD | Detectores individuales | VD1 |
| E2 | Aporte SHAP | Alertas con SHAP | Alertas solo con score | VD2 |
| E3 | Aporte RAG | Reporte RAG anclado | LLM sin RAG | VD3 |
| E4 | Sistema integrado | Pipeline completo | Componentes aislados | VD4, VD5 |
| E5 | Ablation | Variantes por capas | Pipeline completo | VD1, VD5 |

### 3.3.4 Baselines

- B1: Isolation Forest individual.
- B2: Ensemble IF + LOF.
- B3: XGBoost supervisado si existe etiqueta confiable.
- B4: LLM sin RAG ni evidencia SHAP.

## 3.4 Reproducibilidad

Cada corrida debe registrar:

- Version del dataset.
- Fecha de generacion.
- Fuentes usadas.
- Semilla.
- Particion temporal.
- Modelo y parametros.
- Metricas.
- Reporte de trazabilidad.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CAPITULO IV: RESULTADOS Y DISCUSION

> **Estado:** capitulo modularizado. Los resultados finales se completaran unicamente despues de ejecutar los experimentos E1-E5 sobre el dataset agroexportador integrado versionado.

Este capitulo organiza la evaluacion empirica del sistema integrado de supervision operativa. Su funcion actual es dejar preparada la estructura de reporte, los criterios de lectura y las tablas que recibiran los resultados finales.

Los valores obtenidos en corridas previas sobre datasets sinteticos o versiones anteriores se consideran evidencia auxiliar de desarrollo. No deben presentarse como resultados finales de tesis hasta que se regeneren con:

- version del dataset integrado;
- split temporal documentado;
- codigo de experimento;
- fecha de ejecucion;
- semillas utilizadas;
- reporte de calidad de datos;
- trazabilidad de fuente para cada variable.

La estructura del capitulo queda dividida en modulos para facilitar mantenimiento:

| Modulo | Archivo | Contenido |
|---|---|---|
| 4.1 | `docs/02-41-capitulo4-resultados-cuantitativos.md` | Prediccion y deteccion, VD1. |
| 4.2 | `docs/02-42-capitulo4-explicabilidad-reportes.md` | SHAP y reportes RAG, VD2-VD3. |
| 4.3 | `docs/02-43-capitulo4-usabilidad-trazabilidad.md` | Estudio de usuarios y trazabilidad, VD4-VD5. |
| 4.4 | `docs/02-44-capitulo4-discusion.md` | Discusion, contraste con literatura e hipotesis. |
| 4.5-4.6 | `docs/02-45-capitulo4-limitaciones-sintesis.md` | Limitaciones y sintesis final. |

La lectura del capitulo debe conservar una regla metodologica: **ninguna metrica se interpreta sin indicar fuente, version de dataset, granularidad, split y estado de validacion**.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.1 Resultados Cuantitativos: Prediccion y Deteccion, VD1

Esta seccion reportara el rendimiento de la capa predictiva tabular y del ensemble de deteccion de anomalias. La evaluacion principal se realizara sobre el dataset agroexportador integrado, no sobre el dataset sintetico aislado.

### 4.1.1 Condiciones minimas para reportar resultados

Antes de completar las tablas, debe existir evidencia local de:

| Evidencia requerida | Archivo esperado |
|---|---|
| Dataset final versionado | `data/dataset_modelo_v_final.csv` o `codex-revision/data_processed/dataset_modelo_v_final.csv` |
| Split temporal | `dataset_train_raw.csv`, `dataset_validation.csv`, `dataset_test.csv` |
| Reporte de calidad | `reporte-calidad-datos.md` |
| Reporte de entrenamiento | `reporte-entrenamiento-modelos.md` |
| Configuracion de semillas | archivo de experimento o log reproducible |

### 4.1.2 Tabla 4.1 - Rendimiento de deteccion, Experimento E1

| Metodo | Dataset/version | PR-AUC | ROC-AUC | F1 | Precision | Recall | Tiempo inferencia | Estado |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Isolation Forest individual, B1 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| LOF individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| ECOD individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Ensemble IF + LOF | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Ensemble IF + LOF + ECOD, propuesto | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| XGBoost/LightGBM supervisado, upper bound si hay etiqueta | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Condicionado |

> Las corridas historicas sobre versiones sinteticas pueden anexarse como antecedente experimental, pero no reemplazan esta tabla final.

### 4.1.3 Tabla 4.2 - Recall por tipo de anomalia

| Tipo de anomalia | Origen de etiqueta | Recall ensemble | Recall baseline | Diferencia | Estado |
|---|---|---:|---:|---:|---|
| precio | derivada/proxy/sintetica controlada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| volumen | derivada/proxy/sintetica controlada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| clima | proxy o regla documentada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| logistica | proxy o regla documentada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| sanidad/calidad | proxy o regla documentada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

La columna de origen es obligatoria porque `etiqueta_anomalia` puede provenir de observacion real, regla derivada, proxy o inyeccion sintetica controlada. Esa distincion determina el alcance de la interpretacion.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.2 Resultados Cualitativos: Explicabilidad y Reportes, VD2-VD3

Esta seccion evaluara si la capa SHAP mejora la interpretacion de alertas y si los reportes RAG/LLM mantienen fidelidad a la evidencia recuperada.

### 4.2.1 Tabla 4.3 - Calidad de explicabilidad, Experimento E2

| Metrica | Sistema con SHAP | Sistema sin SHAP | p-value | Estado |
|---|---:|---:|---:|---|
| Cobertura top-3 | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Cobertura top-5 | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Estabilidad SHAP | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Claridad operativa Likert 1-5 | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

SHAP se interpretara como atribucion del modelo, no como causalidad. Cada variable explicativa usada en SHAP debe tener fuente, tipo metodologico y granularidad documentados.

### 4.2.2 Tabla 4.4 - Calidad de reportes generados, Experimento E3

| Dimension | RAG/LLM anclado | LLM libre/control | Kappa Cohen | p-value | Estado |
|---|---:|---:|---:|---:|---|
| Completitud | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Consistencia numerica | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Correspondencia con evidencia | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Accionabilidad | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Coherencia textual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

El reporte RAG debe citar o registrar internamente:

- registro evaluado;
- score y umbral;
- top variables SHAP;
- fuente recuperada;
- version de dataset;
- fecha de generacion;
- advertencia cuando una variable sea proxy o sintetica controlada.

### 4.2.3 Ejemplo de reporte generado

El ejemplo final se insertara solo cuando exista una alerta generada desde el dataset integrado. Debe seguir el patron:

`dato -> transformacion -> modelo -> score -> umbral -> SHAP top-k -> evidencia RAG -> reporte`.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.3 Resultados del Estudio de Usabilidad y Trazabilidad, VD4-VD5

Esta seccion medira si el sistema integrado reduce el tiempo de interpretacion y mejora la trazabilidad documental frente a componentes aislados.

### 4.3.1 Tabla 4.5 - Tiempo-a-decision y comprension, Experimento E4

| Metrica | Sistema integrado | Componentes aislados | Diferencia relativa | p-value | Tamano de efecto | Estado |
|---|---:|---:|---:|---:|---:|---|
| Tiempo-a-decision, segundos | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Comprension Likert 1-5 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Decision correcta | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| SUS Score 0-100 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

El tamano muestral y el perfil de participantes se reportaran como estudio piloto especializado si no alcanzan potencia estadistica suficiente para generalizacion amplia.

### 4.3.2 Tabla 4.6 - Trazabilidad documental, VD5

| Configuracion | Alertas con trazabilidad completa | Campos faltantes frecuentes | Estado |
|---|---:|---|---|
| Sistema integrado completo, E5d | _pendiente_ | _pendiente_ | Por ejecutar |
| Ablation sin SHAP, E5b | _pendiente_ | _pendiente_ | Por ejecutar |
| Ablation sin RAG, E5c | _pendiente_ | _pendiente_ | Por ejecutar |
| Componentes aislados/control | _pendiente_ | _pendiente_ | Por ejecutar |

La trazabilidad completa exige, como minimo: `id_alerta`, `producto`, `hs`, `fecha`, `fuentes_usadas`, `score`, `umbral`, `top_shap`, `evidencia_rag`, `version_dataset` y `archivo_origen`.

### 4.3.3 Tabla 4.7 - Ablation study, Experimento E5

| Configuracion | Capa 1 prediccion | Capa 2 anomalias | Capa 3 SHAP | Capa 4 RAG | VD1 | VD3 | VD5 | Estado |
|---|---|---|---|---|---:|---:|---:|---|
| E5a solo deteccion | No | Si | No | No | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| E5b sin SHAP | Si | Si | No | Si | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| E5c sin RAG | Si | Si | Si | No | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| E5d pipeline completo | Si | Si | Si | Si | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

Las comparaciones E5 no deben mezclar resultados de dataset sintetico con resultados del dataset integrado sin una etiqueta explicita de version.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.4 Discusion y Cruce Comparativo

### 4.4.1 Proposito de la discusion

La discusion triangula cuatro bloques: literatura revisada, hipotesis del Capitulo I, variables operacionalizadas y evidencia generada por el pipeline. Su objetivo es explicar los resultados sin convertir correlaciones, scores o valores SHAP en afirmaciones causales.

### 4.4.2 Cruce 1 - Resultados propios versus literatura comparable

| Atributo | Esta tesis | Literatura comparable | Lectura esperada |
|---|---|---|---|
| Prediccion tabular | XGBoost/LightGBM | GBDT en fraude, auditoria y agroexportacion | Comparar cobertura y estabilidad, no valores absolutos entre dominios. |
| Deteccion de anomalias | Isolation Forest, LOF, ECOD | ADBench/PyOD | Justificar ensemble si mejora o estabiliza resultados. |
| Explicabilidad | SHAP/TreeSHAP | XAI tabular | Evaluar claridad y consistencia, no causalidad. |
| Reporte tecnico | RAG/LLM restringido | LLMs para auditoria/reportes | Evaluar fidelidad a evidencia y trazabilidad. |
| Dominio | Agroexportacion peruana | Finanzas, auditoria, agroclima | Declarar limites de comparabilidad. |

### 4.4.3 Cruce 2 - Contraste de hipotesis

| Hipotesis | Evidencia requerida | Decision |
|---|---|---|
| H1a | Mejora de VD1 frente a detector individual con split temporal documentado. | _pendiente_ |
| H1b | Mejora de VD2 con SHAP frente a condicion sin SHAP. | _pendiente_ |
| H1c | Mejora de VD3 con RAG frente a LLM libre/control. | _pendiente_ |
| H1d | Reduccion de tiempo-a-decision o mejora de comprension. | _pendiente_ |
| H1 general | Mejora conjunta de trazabilidad y supervision operativa. | _pendiente_ |

La decision puede ser: aceptar, rechazar o inconclusa. Toda decision debe estar vinculada al reporte de entrenamiento o de usabilidad correspondiente.

### 4.4.4 Cruce 3 - Variables operacionalizadas versus indicadores observados

| Variable | Indicador | Valor observado | Cumple |
|---|---|---:|---|
| VD1 rendimiento | PR-AUC, F1, precision, recall | _pendiente_ | _pendiente_ |
| VD2 explicabilidad | Cobertura top-k, estabilidad, claridad | _pendiente_ | _pendiente_ |
| VD3 reportes | Rubrica, consistencia numerica, evidencia | _pendiente_ | _pendiente_ |
| VD4 decision | Tiempo, comprension, decision correcta | _pendiente_ | _pendiente_ |
| VD5 trazabilidad | Campos completos por alerta | _pendiente_ | _pendiente_ |

### 4.4.5 Cruce 4 - Gobernanza, componente y metrica

| Principio | Componente | Metrica |
|---|---|---|
| Transparencia | Datasheet, Model Cards, logs | Cobertura de metadatos. |
| Explicabilidad | SHAP/TreeSHAP | VD2. |
| Supervision humana | Protocolo de usabilidad y revision | VD4. |
| Gestion de riesgo | Validacion temporal y umbrales | VD1. |
| Anti-alucinacion | RAG anclado a evidencia | VD3. |
| Trazabilidad | Registro de alerta end-to-end | VD5. |

### 4.4.6 Cruce 5 - Errores por tipo de anomalia

| Tipo de anomalia | Posible mecanismo de fallo | Mejora candidata |
|---|---|---|
| precio | Estacionalidad o mercado destino no capturado. | Media movil por producto-destino. |
| volumen | Campanas pico confundidas con outliers. | Variables de campana y calendario. |
| clima | Proxy regional demasiado agregado. | Mayor granularidad geografica. |
| logistica | Falta de llave directa puerto-embarque. | Agregacion puerto-mes documentada. |
| sanidad/calidad | Alertas agregadas sin trazabilidad por embarque. | Mantener como contexto, no etiqueta directa. |

### 4.4.7 Interpretacion conjunta

La contribucion esperada no es solo mejorar una metrica aislada, sino demostrar que la integracion de prediccion, deteccion, explicabilidad y reporte aumenta la capacidad de supervision operativa trazable. Si los resultados finales no sostienen una hipotesis, la tesis debe reportarlo como hallazgo metodologico y ajustar la discusion sin forzar la narrativa.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.5 Limitaciones de los Resultados

Los resultados finales deberan interpretarse considerando:

1. **Naturaleza integrada del dataset:** el dataset combina datos reales observados, datos reales agregados, proxies y datos sinteticos controlados. Cada capa tiene granularidad y alcance distintos.
2. **Etiquetas de anomalia:** cuando `etiqueta_anomalia` derive de reglas o inyeccion sintetica, la evaluacion mide deteccion de desviaciones definidas por protocolo, no necesariamente incidentes reales confirmados por empresa.
3. **SISAP/MIDAGRI:** aporta contexto de mercado interno mayorista y no debe interpretarse como exportacion.
4. **Fuentes sanitarias y logisticas:** pueden operar como contexto agregado si no existe llave directa por embarque.
5. **SHAP:** entrega atribuciones del modelo, no causalidad.
6. **RAG/LLM:** mejora la redaccion y trazabilidad del reporte, pero requiere validacion contra evidencias y supervision humana.
7. **Usabilidad:** si el estudio usa muestra pequena, sus conclusiones deben presentarse como piloto especializado.

## 4.6 Sintesis del Capitulo IV

La sintesis final se completara cuando existan resultados integrados verificables:

1. El ensemble IF + LOF + ECOD _supera/no supera_ al detector individual en VD1.
2. SHAP _mejora/no mejora_ la comprension y trazabilidad explicativa en VD2.
3. RAG anclado _mejora/no mejora_ la calidad documental en VD3.
4. El sistema integrado _reduce/no reduce_ el tiempo-a-decision en VD4.
5. La trazabilidad documental alcanza _pendiente_% de alertas completas en VD5.
6. Las limitaciones por proxies, granularidad y datos sinteticos controlados quedan documentadas para evitar sobreinterpretacion.

Hasta completar esos puntos, el capitulo se considera una estructura de resultados, no una afirmacion empirica final.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CAPÍTULO V: CONCLUSIONES Y TRABAJOS FUTUROS

> **Pendiente:** Capítulo V — depende de los resultados del Capítulo IV


## 5.1 Conclusiones

*(Esqueleto para la síntesis final: el sistema integrado logró los objetivos propuestos, manteniendo el balance entre vanguardia tecnológica y rigor legal. Incluir: conclusión sobre el gap cerrado, métricas alcanzadas vs. objetivos, validación de hipótesis H1a–H1d, aporte al contexto regulatorio peruano).*

## 5.2 Limitaciones de la Investigación

*(Abordar: limitaciones del dataset agroexportador integrado; diferencias de granularidad entre datos reales observados, datos agregados, proxies y datos sintéticos controlados; dependencia de la calidad de datos documentada en Datasheets for Datasets (Gebru et al., 2021); deuda técnica de mantenimiento del pipeline MLOps (Sculley et al., 2015); limitaciones del tamaño de la muestra en la evaluación de comprensión; restricciones de los LLMs actuales en precisión de cálculo aritmético (Maynez et al., 2026)).*

## 5.3 Trabajos Futuros

*(Propuestas: integración de GraphRAG para recuperación semántica más rica sobre conocimiento agroexportador; extensión del ensemble con ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica) (Li et al., 2022) y modelos de concept drift para supervisión en stream; exploración de Chronos (Ansari et al., 2024) para forecasting de horizonte largo; prueba piloto en una empresa agroexportadora peruana; evaluación de sesgos y limitaciones según Datasheets for Datasets (Gebru et al., 2021)).*

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CRONOGRAMA DE ACTIVIDADES

> **Pendiente:** conclusiones finales dependientes de Capitulo IV y Capitulo V.

*(Ver Tabla 1.2 en el Capitulo I, seccion 1.11).*

---

# CONCLUSIONES

*(Por completar con los resultados finales de la investigacion. Estructura sugerida:)*

1. *(Conclusion sobre el gap cerrado: el sistema integrado de cuatro capas constituye una propuesta academica para unificar prediccion GBDT, deteccion de anomalias ensemble, explicabilidad SHAP y generacion de reportes LLM+RAG sobre un dataset agroexportador integrado, trazable y compuesto por datos reales observados, datos reales agregados, proxies documentados y sinteticos controlados.)*

2. *(Conclusion sobre metricas alcanzadas: completar solo despues de ejecutar el entrenamiento final sobre el dataset integrado y reportar PR-AUC, F1, precision, recall, estabilidad SHAP, cobertura de evidencia RAG y tiempo-a-decision sin sobreafirmar resultados preliminares.)*

3. *(Conclusion sobre validacion de hipotesis H1a-H1d: aceptar, rechazar o declarar inconclusa cada subhipotesis segun evidencia reproducible.)*

4. *(Conclusion sobre gobernanza: describir como trazabilidad, documentacion y supervision humana se alinean con principios del D.S. 115-2025-PCM, NIST AI RMF y buenas practicas de gestion de riesgo de modelos.)*

5. *(Conclusion sobre aporte al campo: redactar solo despues de contrastar resultados finales con literatura comparable y con las limitaciones del dataset integrado.)*

---

# CONCLUSIONS

*(To be completed after the final integrated-dataset experiments. Suggested structure:)*

1. *(Conclusion on the research gap: the four-layer system integrates GBDT prediction, anomaly detection, SHAP explainability, and RAG-based reporting over a traceable integrated agro-export dataset.)*

2. *(Conclusion on metrics: complete only after the final run, reporting PR-AUC, F1, precision, recall, SHAP stability, RAG evidence coverage, and time-to-decision with dataset version and reproducibility metadata.)*

3. *(Conclusion on H1a-H1d: accept, reject, or mark each hypothesis as inconclusive based on reproducible evidence.)*

4. *(Conclusion on governance: describe how traceability, documentation, and human oversight are implemented as design principles, without claiming regulatory certification.)*

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# RECOMENDACIONES

1. **Para implementadores**: Se recomienda iniciar el despliegue del sistema con el módulo de predicción GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) y el módulo de explicabilidad SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley) antes de integrar el componente LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación), siguiendo el principio de implementación incremental que reduce la deuda técnica (Sculley et al., 2015) y permite validar cada capa de forma independiente.

2. **Para empresas agroexportadoras**: Antes de adoptar el sistema en producción, se recomienda elaborar Datasheets for Datasets (Gebru et al., 2021) para todos los datasets de entrenamiento y Model Cards (Mitchell et al., 2019) para los modelos XGBoost, detectores de anomalías y LLM+RAG.

3. **Para futuros investigadores**: Se recomienda extender la evaluación del sistema con un diseño experimental longitudinal que capture el efecto del concept drift en precios, volúmenes, clima y comportamiento exportador, utilizando ventanas temporales y fuentes agroexportadoras reales.

4. **Para entidades públicas y sectoriales**: Se recomienda promover guías técnicas de IA explicable y trazabilidad para sistemas de supervisión en cadenas productivas, tomando como referencia marcos nacionales e internacionales de gobernanza de IA.

5. **Para la academia**: Se recomienda replicar el estudio con datos reales de una empresa agroexportadora colaboradora (bajo acuerdo de confidencialidad), ampliar la muestra de evaluación con supervisores operativos y responsables de calidad, e incorporar métricas de sesgo y robustez según las dimensiones de evaluación de ADBench (Han et al., 2022).

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# GLOSARIO DE TÉRMINOS

**ADBench** (*Anomaly Detection Benchmark*): Benchmark sistemático para evaluación comparativa de algoritmos de detección de anomalías, propuesto por Han et al. (2022), que cubre 57 datasets y 30 algoritmos bajo tres niveles de supervisión.

**Alucinación (LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño))**: Fenómeno en el que un modelo de lenguaje genera texto coherente en forma pero incorrecto en contenido, incluyendo afirmaciones factuales erróneas, citas inexistentes o cifras fabricadas.

**AUC-PR** (*Area Under the Precision-Recall Curve*): Métrica de evaluación para clasificadores en datasets desbalanceados; a diferencia de AUC-ROC, es sensible a la distribución de clases y penaliza los falsos positivos de forma más relevante en contextos de fraude y anomalías raras.

**BAF Benchmark** (*Bank Account Fraud*): Dataset tabular de referencia para fraude bancario con drift temporal y desbalance de clases, publicado por Jesus et al. (2022). En esta tesis se considera únicamente como benchmark metodológico complementario para evaluar robustez tabular, no como validación directa del dominio agroexportador.

**CatBoost**: Algoritmo GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) desarrollado por Yandex (Prokhorenkova et al., 2018) que resuelve el problema de target leakage en variables categóricas mediante Ordered Boosting.

**Concept Drift**: Cambio en la distribución estadística de los datos a lo largo del tiempo que degrada el rendimiento de modelos entrenados con datos históricos; particularmente relevante en detección de fraude y anomalías operativas.

**Deep SVDD** (*Deep Support Vector Data Description*): Método de detección de anomalías basado en redes neuronales que aprende una hipersfera mínima en el espacio latente que contiene los datos normales (Ruff et al., 2018).

**ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica)** (*Empirical Cumulative distribution functions Outlier Detection*): Detector de anomalías sin parámetros basado en distribuciones empíricas acumuladas (Li et al., 2022), notable por su ausencia de hiperparámetros a calibrar.

**EU AI Act** (*Reglamento (UE) 2024/1689*): Reglamento europeo de inteligencia artificial que clasifica los sistemas de IA por nivel de riesgo y establece obligaciones de transparencia y explicabilidad en el Artículo 13 para sistemas de alto riesgo.

**GBDT** (*Gradient Boosting Decision Trees*): Familia de algoritmos de aprendizaje supervisado que construyen modelos predictivos mediante la combinación secuencial de árboles de decisión débiles, minimizando una función de pérdida mediante descenso de gradiente funcional.

**Isolation Forest**: Algoritmo de detección de anomalías no supervisado (Liu et al., 2008) que aísla anomalías mediante particionamiento aleatorio del espacio de datos, con complejidad computacional O(n).

**LightGBM**: Algoritmo GBDT de Microsoft (Ke et al., 2017) que acelera el entrenamiento hasta 20× mediante Gradient-based One-Side Sampling y estructuras de datos basadas en histogramas.

**LLM** (*Large Language Model*): Modelo de lenguaje de gran tamaño entrenado en corpus masivos de texto para aprender distribuciones probabilísticas sobre secuencias de tokens, capaz de realizar tareas de generación, resumen y razonamiento en lenguaje natural.

**LOF (Local Outlier Factor - Factor de Anomalía Local)** (*Local Outlier Factor*): Detector de anomalías basado en densidad local relativa (Breunig et al., 2000) que cuantifica el grado de anomalía de un punto comparando su densidad con la de sus vecinos k-NN.

**MLOps** (*Machine Learning Operations*): Conjunto de prácticas para gestionar el ciclo de vida completo de modelos ML en producción, incluyendo CI/CD, monitoreo de drift, automatización de reentrenamiento y trazabilidad de versiones.

**NIST AI RMF**: Framework de gestión de riesgo para sistemas de IA publicado por el Instituto Nacional de Estándares y Tecnología de EE.UU. (2023), organizado en cuatro funciones: Govern, Map, Measure y Manage.

**PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad)**: Ver AUC-PR.

**PyOD** (*Python Outlier Detection*): Librería de Python que implementa más de 40 algoritmos de detección de outliers con una API estandarizada compatible con scikit-learn (Zhao et al., 2019).

**RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)** (*Retrieval-Augmented Generation*): Arquitectura para modelos de lenguaje que separa el conocimiento factual del modelo generativo, recuperando documentos relevantes de una base de conocimiento externa para anclar las respuestas y mitigar alucinaciones.

**Resolución SBS N° 053-2023**: Resolución de la Superintendencia de Banca, Seguros y AFP del Perú que establece lineamientos de gestión de riesgos de modelos para entidades supervisadas. En esta tesis se utiliza como referencia nacional de buenas prácticas para trazabilidad, validación y monitoreo, no como obligación directa para empresas agroexportadoras.

**ROUGE** (*Recall-Oriented Understudy for Gisting Evaluation*): Conjunto de métricas para evaluación automática de resúmenes y textos generados mediante comparación de superposición de n-gramas con un texto de referencia humano.

**SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)** (*SHapley Additive exPlanations*): Marco de explicabilidad post-hoc que asigna a cada feature una contribución marginal promediada sobre todas las coaliciones posibles, garantizando consistencia axiomática (Lundberg & Lee, 2017).

**SHAP Stability Index**: Métrica de coherencia de explicaciones SHAP entre instancias similares, que certifica que el modelo asigna importancias consistentes a features semejantes, requisito en contextos forenses.

**TFT** (*Temporal Fusion Transformer*): Arquitectura de Transformer para forecasting multi-horizonte interpretable con covariables exógenas, mecanismo de gating y predicción por cuantiles (Lim et al., 2021).

**TreeSHAP**: Algoritmo exacto para el cálculo de valores SHAP en modelos basados en árboles, con complejidad O(TLD²), que hace viable la explicabilidad en GBDT de producción con millones de transacciones.

**XGBoost** (*eXtreme Gradient Boosting*): Implementación escalable de gradient boosting (Chen & Guestrin, 2016) con regularización L1/L2, manejo nativo de valores faltantes y paralelización por columnas; baseline universal en competencias de ML con datos tabulares.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# REFERENCIAS BIBLIOGRÁFICAS

Almalki, F., & Masud, M. (2025). *Financial fraud detection using explainable AI and stacking ensemble methods*. arXiv preprint arXiv:2505.10050.

Ansari, A. F., Stella, L., Turkmen, C., Zhang, X., Mercado, P., Sinha, R., & Bergmeir, C. (2024). *Chronos: Learning the language of time series*. arXiv preprint arXiv:2403.07815.

Arik, S. O., & Pfister, T. (2021). TabNet: Attentive interpretable tabular learning. *Proceedings of the AAAI Conference on Artificial Intelligence*, *35*(8), 6679–6687. https://doi.org/10.1609/aaai.v35i8.16842

Barclays Research. (2025). *Beyond the black box: Interpretability of LLMs in finance*. arXiv preprint arXiv:2505.24650.

Breunig, M. M., Kriegel, H.-P., Ng, R. T., & Sander, J. (2000). LOF: Identifying density-based local outliers. *ACM SIGMOD Record*, *29*(2), 93–104. https://doi.org/10.1145/342009.335388

Center for Audit Quality. (2024). *Auditing in the age of generative AI*. CAQ. https://thecaq.org/wp-content/uploads/2024/04/caq_auditing-in-the-age-of-generative-ai__2024-04.pdf

Challu, C., Olivares, K. G., Oreshkin, B., Garza, F., Mergenthaler-Canseco, M., & Dubrawski, A. (2022). N-HiTS: Neural hierarchical interpolation for time series forecasting. *Advances in Neural Information Processing Systems*, *35*. (arXiv:2201.12886)

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794. https://doi.org/10.1145/2939672.2939785

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM*, *64*(12), 86–92. https://doi.org/10.1145/3458723

Gorishniy, Y., Rubashevskiy, I., Khrulkov, V., & Babenko, A. (2021). Revisiting deep learning models for tabular data. *Advances in Neural Information Processing Systems 34 (NeurIPS)*, 8946–8959.

Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on tabular data? *Advances in Neural Information Processing Systems 35 (NeurIPS)*, 507–520.

Han, X., Hu, Y., Venevdev, L., Liu, M., Wen, Q., & Zhang, Y. (2022). ADBench: Anomaly detection benchmark. *Advances in Neural Information Processing Systems*, *35*.

Hegselmann, S., Buendia, A., Lang, H., Agrawal, M., Jiang, X., & Sontag, D. (2022). TabLLM: Few-shot classification of tabular data with large language models. arXiv preprint arXiv:2210.10723.

Hyndman, R. J., & Khandakar, Y. (2008). Automatic time series forecasting: The forecast package for R. *Journal of Statistical Software*, *27*(3), 1–22. https://doi.org/10.18637/jss.v027.i03

Jesus, S., Pombal, J., Alves, D., Cruz, A., Saleiro, P., Ribeiro, R. P., Gama, J., & Bizarro, P. (2022). *Turning the tables: Biased, imbalanced, dynamic tabular datasets for ML evaluation*. arXiv preprint arXiv:2211.13358. [NeurIPS 2022]

Kadir, M. A., Macharla Vasu, S. S., Nair, S. S., & Sonntag, D. (2025). AuditCopilot: Leveraging LLMs for fraud detection in double-entry bookkeeping. arXiv preprint arXiv:2512.02726. https://doi.org/10.48550/arXiv.2512.02726

Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems 30 (NeurIPS)*, 3146–3154.

Kreuzberger, D., Kühl, N., & Hirschl, G. (2022). MLOps: Overview, definition, and architecture. *IEEE Access*, *10*, 86995–87010. https://doi.org/10.1109/ACCESS.2022.3197550

Leocádio, D., et al. (2024). *Continuous auditing artificial intelligence framework*. [Pending venue publication]

Lewis, P., Perez, E., Piktus, A., Schwenk, H., Schwab, C., Yeh, C., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 9457–9474. https://doi.org/10.18653/v1/2020.emnlp-main.727

Li, Z., Zhao, Y., Hu, X., Botta, N., Ionescu, C., & Chen, G. H. (2022). ECOD: Unsupervised outlier detection using empirical cumulative distribution functions. *IEEE Transactions on Knowledge and Data Engineering*, *35*(12), 12181–12193. https://doi.org/10.1109/TKDE.2022.3159580

Lim, B., Arik, S. O., Loeff, N., & Pfister, T. (2021). Temporal fusion transformers for interpretable multi-horizon time series forecasting. *International Conference on Learning Representations (ICLR)*. (arXiv:1912.09300)

Lin, C.-Y. (2004). ROUGE: A package for automatic evaluation of summaries. *Proceedings of the Workshop on Text Summarization Branches Out (ACL 2004)*, 74–81.

Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation forest. *Proceedings of the 8th IEEE International Conference on Data Mining (ICDM)*, 413–422. https://doi.org/10.1109/ICDM.2008.17

Liu, Y., Hu, T., Zhang, H., Wu, H., Wang, S., Ma, L., & Long, M. (2024). iTransformer: Inverted transformers are effective for time series forecasting. *International Conference on Learning Representations (ICLR)*.

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems 30 (NeurIPS)*, 4765–4774.

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model cards for model reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency (FAccT)*, 220–229. https://doi.org/10.1145/3287560.3287596

National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)*. NIST. https://doi.org/10.6028/NIST.AI.600-1

Nie, Y., Nguyen, N. H., Sinthong, P., & Kalagnanam, J. (2023). A time series is worth 64 words: Long-term forecasting with transformers. *International Conference on Learning Representations (ICLR)*.

Oreshkin, B. N., Carpov, D., Chapados, N., & Bengio, Y. (2020). N-BEATS: Neural basis expansion analysis for interpretable time series forecasting. *Proceedings of the 37th International Conference on Machine Learning (ICML)*, 4799–4808. https://doi.org/10.5555/3524938.3525255

Papineni, K., Roukos, S., Ward, T., & Zhu, W.-J. (2002). BLEU: A method for automatic evaluation of machine translation. *Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics (ACL)*, 311–318. https://doi.org/10.3115/1073083.1073135

Park, S. (2024). *LLMs for anomaly validation and report generation in financial systems*. arXiv preprint arXiv:2403.19735.

Patel, R., Khan, F., Silva, B., & Shaturaev, J. (2024). AI-driven continuous auditing and real-time financial monitoring. *International Research Journal of Modernization in Engineering Technology and Science*.

Parlamento Europeo y Consejo de la Unión Europea. (2024). *Reglamento (UE) 2024/1689 por el que se establecen normas armonizadas en materia de inteligencia artificial (Ley de Inteligencia Artificial)*. Diario Oficial de la Unión Europea. https://eur-lex.europa.eu/eli/reg/2024/1689

Prenio, J., & Yong, J. (2024). *Managing explanations: How regulators can address AI explainability*. Bank for International Settlements, Financial Stability Institute. https://www.bis.org/fsi/fsipapers24.pdf

Presidencia del Consejo de Ministros. (2025, septiembre). *Decreto Supremo N° 115-2025-PCM: Reglamento de la Ley N° 31814*. Lima, Perú. https://busquedas.elperuano.pe

Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: Unbiased boosting with categorical features. *Advances in Neural Information Processing Systems 31 (NeurIPS)*, 6638–6648. https://doi.org/10.5555/3327757.3327790

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 1135–1144. https://doi.org/10.1145/2939672.2939778

Ruff, L., Kauffmann, J. R., Vandermeulen, R. A., Montavon, G., Samek, W., Kloft, M., Dickhaus, T., & Müller, K.-R. (2018). Deep one-class classification. *Proceedings of the 35th International Conference on Machine Learning (ICML)*, 4393–4402.

Schneider, J., et al. (2025). Retrieval-augmented generation (RAG). *Business & Information Systems Engineering*. https://doi.org/10.1007/s12599-025-00945-3

Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., & Young, M. (2015). Hidden technical debt in machine learning systems. *Proceedings of the 28th International Conference on Neural Information Processing Systems (NIPS) Workshop*.

Superintendencia de Banca, Seguros y AFP. (2023). *Resolución SBS N° 053-2023: Reglamento de gestión de riesgos de modelo*. Lima, Perú. https://www.sbs.gob.pe

Taylor, S. J., & Letham, B. (2017). *Forecasting at scale*. PeerJ Preprints. https://doi.org/10.7287/peerj.preprints.3190v2

Thanathamathee, P., et al. (2024). SHAP-instance weighting and anchor explainable AI: Enhancing XGBoost for financial fraud detection. *Emerging Science Journal*, *8*(6). https://doi.org/10.28991/ESJ-2024-08-06-024

Tsai, C.-P., et al. (2025). *LLM-based anomaly detection in tabular data*. [Pending venue publication]

Gómez, A., López, B., & Sánchez, C. (2025). *Hallucination detection and mitigation in large language models*. arXiv preprint arXiv:2601.09929.

Wang, L., Chen, M., & Zhang, H. (2025). Financial statement fraud detection through an integrated machine learning and explainable AI framework. *Journal of Risk and Financial Management*, *19*(1), 13. https://doi.org/10.3390/jrfm19010013

Silva, R., Santos, M., & Costa, J. (2025). Explainable AI for forensic analysis: A comparative study of SHAP and LIME in intrusion detection models. *Applied Sciences*, *15*(13), 7329. https://doi.org/10.3390/app15137329

Waltersdorfer, L., Ekaputra, F. J., Miksa, T., & Sabou, M. (2024). AuditMAI: Towards an infrastructure for continuous AI auditing. arXiv preprint arXiv:2406.14243. https://doi.org/10.48550/arXiv.2406.14243

Zeng, A., Chen, M., Zhang, L., & Xu, Q. (2023). Are transformers effective for time series forecasting? *Proceedings of the AAAI Conference on Artificial Intelligence*, *37*(9), 11121–11128. https://doi.org/10.1609/aaai.v37i9.26317

Zhao, Y., Nasrullah, Z., & Li, Z. (2019). PyOD: A Python toolbox for scalable outlier detection. *Journal of Machine Learning Research*, *20*(96), 1–7.

---

# ANEXOS

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# ANEXOS

## Anexo A — Protocolo de Evaluación de Usabilidad

> **Versión 1.0 — 2026-05-17.** Aprobar antes de iniciar reclutamiento de participantes.

### A.1 Objetivo del experimento

El experimento de usabilidad mide el impacto del sistema integrado de supervisión operativa en la **eficiencia (VD4 — tiempo-a-decisión)**, **comprensión (VD4 — Likert)** y **trazabilidad documental (VD5)** frente al uso de componentes aislados. Constituye la fuente principal de evidencia para contrastar las sub-hipótesis H1b y H1d (Capítulo I §1.4).

### A.2 Diseño experimental

**Tipo**: Cuasi-experimental con diseño within-subjects (apareado) y orden contrabalanceado.

Cada participante ejecuta las mismas tareas en dos condiciones:
- **Condición A — Sistema integrado**: pipeline de 4 capas con alerta + score + vector SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley) top-5 + reporte LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación).
- **Condición B — Componentes aislados**: alerta + score crudo del detector, sin SHAP, sin reporte narrativo (solo tabla y visualización técnica).

La mitad de los participantes inicia con A y la otra mitad con B, asignación aleatorizada con `np.random.seed(42)`. Entre ambas condiciones se intercala un descanso de 5 minutos y una tarea distractora (sopa de letras) para reducir efectos de arrastre.

### A.3 Tareas evaluadas

Cada condicion presenta el mismo bloque de 10 alertas (5 positivas reales o verificadas por regla, 3 negativas reales, 2 ambiguas) extraidas del conjunto de test del dataset agroexportador integrado o de escenarios controlados derivados de este. Para cada alerta, el participante:

1. **Tarea T1 — Clasificación**: decide si la alerta corresponde a una anomalía operativa real (sí/no/dudoso).
2. **Tarea T2 — Justificación**: en una oración (máx. 200 caracteres) indica la variable que justifica la decisión.
3. **Tarea T3 — Comprensión**: responde Likert 1–5 sobre cuán comprensible resultó la alerta.

Al finalizar el bloque de 10 alertas, completa un cuestionario post-bloque (SUS adaptado + preguntas abiertas).

### A.4 Métricas registradas automáticamente

| Métrica | Fuente | Resolución |
|---|---|---|
| Tiempo apertura alerta → decisión | Log JavaScript de la plataforma | milisegundos |
| Tiempo total bloque | Log JavaScript | segundos |
| Clasificación del participante | Formulario | sí / no / dudoso |
| Justificación textual | Formulario | texto libre |
| Likert comprensión | Formulario | 1–5 |
| Versión del sistema | Variable de configuración | string |
| Identificador de alerta | Variable | string |

### A.5 Criterios de inclusión y exclusión de participantes

**Inclusión**:
- (a) Estudiantes de últimos ciclos (≥ 9° semestre) o egresados de Ingeniería de Sistemas, Ingeniería Industrial o Agronomía con formación comprobada en logística, control de calidad o auditoría de sistemas; o
- (b) Profesionales y técnicos con experiencia en supervisión de operaciones, control de calidad, auditoría de sistemas o gestión logística en el sector agroexportador.
- Mayores de 18 años.
- Aceptación de consentimiento informado firmado.

**Exclusión**:
- Participación previa en el diseño, desarrollo o entrenamiento de cualquier capa del sistema evaluado.
- Conflicto de interés directo declarado.
- Discapacidad visual no corregible que impida la lectura del dashboard.

### A.6 Tamaño de muestra y reclutamiento

**Tamaño meta**: N = 10 participantes (documentar formalmente como un estudio piloto especializado de usabilidad). Un tamaño N = 10 permite una evaluación detallada de la eficiencia temporal y cualitativa sin pretensiones de generalización estadística a gran escala, pero con alta representatividad técnica.

**Reclutamiento**: El estudio se limita a **grupos cerrados de testers con conocimiento especializado en el área** bajo invitación directa (no abierta al público general). La convocatoria se realiza por invitación formal a través de la Escuela de Ingeniería de Sistemas de la UNSA y contactos en empresas agroexportadoras de Arequipa, Ica y La Libertad coordinadas por el asesor, garantizando el perfil técnico de los evaluadores.

### A.7 Procedimiento detallado (sesión por participante, ~45 minutos)

| Paso | Duración | Contenido |
|---|---|---|
| 1 | 5 min | Bienvenida + consentimiento informado firmado |
| 2 | 5 min | Tutorial guiado de la plataforma (alerta de ejemplo) |
| 3 | 12 min | Bloque 1 — Condición A o B (según contrabalanceo) |
| 4 | 5 min | Descanso + tarea distractora |
| 5 | 12 min | Bloque 2 — Condición contraria |
| 6 | 5 min | Cuestionario final SUS + preguntas abiertas |
| 7 | 1 min | Cierre + agradecimiento |

### A.8 Consentimiento informado (texto base)

```
Por la presente confirmo que:
1. He sido informado sobre el propósito del estudio: evaluar la usabilidad de
   un sistema de supervisión operativa con IA explicable.
2. Comprendo que mi participación es voluntaria y puedo retirarme en cualquier
   momento sin justificación ni consecuencia.
3. Comprendo que mis respuestas son anónimas. Solo el investigador principal
   accederá a los datos, que se almacenarán cifrados y se eliminarán al
   finalizar la tesis (julio 2027).
4. Acepto que se registre el tiempo de mis respuestas y las opciones
   seleccionadas para análisis estadístico agregado.
5. Comprendo que no recibiré evaluación individual ni se compartirán mis
   resultados con terceros.
6. Acepto participar en una sesión de aproximadamente 45 minutos.

Nombre: ____________________  Fecha: __________  Firma: __________
```

### A.9 Cuestionario post-bloque

**Bloque I — Comprensión percibida (Likert 1–5)**

| # | Ítem | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 1 | Entendí claramente por qué el sistema marcó cada alerta | | | | | |
| 2 | La información presentada me ayudó a tomar una decisión | | | | | |
| 3 | Las variables explicativas fueron suficientes | | | | | |
| 4 | El reporte generado fue útil para justificar mi decisión | | | | | |
| 5 | Confío en la decisión del sistema | | | | | |

**Bloque II — Tiempo y carga cognitiva (Likert 1–5)**

| # | Ítem | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 6 | Me tomó mucho tiempo entender cada alerta (1) — Fui rápido (5) | | | | | |
| 7 | Tuve que esforzarme mucho mentalmente | | | | | |
| 8 | Me sentí seguro al decidir | | | | | |

**Bloque III — Adaptación SUS (10 ítems Likert 1–5)**

```
1. Creo que me gustaría usar este sistema frecuentemente.
2. Encontré el sistema innecesariamente complejo.
3. Pensé que el sistema fue fácil de usar.
4. Necesitaría el apoyo de un experto técnico para usar este sistema.
5. Las funciones del sistema están bien integradas.
6. Hay demasiada inconsistencia en este sistema.
7. La mayoría aprendería a usar este sistema rápidamente.
8. Encontré el sistema muy engorroso.
9. Me sentí muy confiado al usar el sistema.
10. Necesitaría aprender muchas cosas antes de usar el sistema.
```

**Bloque IV — Preguntas abiertas**

1. ¿Qué fue lo más útil del sistema en esta sesión?
2. ¿Qué información agregaría o quitaría?
3. ¿En qué situación operativa real este sistema sería más valioso?

### A.10 Variables registradas para análisis

| Variable | Tipo | Origen |
|---|---|---|
| `participant_id` | string anónimo | Generado |
| `order` | {AB, BA} | Aleatorización |
| `condition` | {integrated, isolated} | Variable independiente |
| `alert_id` | string | Dataset |
| `gt_label` | {0, 1} | Dataset (oculto al participante) |
| `user_decision` | {yes, no, dunno} | Formulario |
| `time_to_decision_ms` | int | Log JavaScript |
| `likert_comprehension` | 1–5 | Cuestionario |
| `justification_text` | string | Formulario |
| `sus_score` | 0–100 | Cálculo SUS |

### A.11 Plan de análisis estadístico

1. **Tiempo-a-decisión (VD4-a)**: t de Student apareado integrado vs. aislado; Wilcoxon si Shapiro-Wilk rechaza normalidad. Reportar media ± DE, IC95%, Cohen's dz.
2. **Comprensión Likert (VD4-b)**: Wilcoxon signed-rank apareado.
3. **Decisión correcta (VD4-c)**: McNemar sobre pares concordantes/discordantes.
4. **SUS**: comparación de medias con Mann-Whitney U.
5. **Análisis cualitativo de respuestas abiertas**: análisis temático con doble codificación independiente.

### A.12 Almacenamiento y privacidad de datos

- Datos almacenados en archivo CSV cifrado con clave conocida solo por el investigador.
- Identificadores anónimos, sin nombre, correo ni datos demográficos sensibles.
- Backup en disco duro institucional UNSA.
- Eliminación de datos crudos al cierre del proyecto (julio 2027).
- Resultados agregados publicados en la tesis y en el repositorio GitHub.

### A.13 Aprobación ética

El protocolo se somete a revisión del asesor de tesis (Dr. Víctor Manuel Cornejo Aparicio) y, si la Escuela de Ingeniería de Sistemas dispone de comité de ética, a su aprobación formal antes del reclutamiento.

---

*Anexo A — versión 1.0 — 2026-05-17. Sometido a revisión final antes de ejecutar el estudio.*

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo B - Model Cards

Este anexo documenta los modelos de la arquitectura bajo el enfoque de dataset agroexportador integrado versionado.

## B.1 Dataset de referencia

Los modelos se entrenan y evaluan sobre un dataset integrado compuesto por:

- datos reales observados de SUNAT/ADUANET y dataset real local;
- datos reales agregados de Trade Map, SISAP/MIDAGRI y BCRP;
- proxies climaticos, logisticos y sanitarios;
- datos sinteticos controlados solo para escenarios auxiliares, balanceo o etiquetas experimentales.

Subgrupos obligatorios:

| Producto | Estado |
|---|---|
| Palta | Nucleo. |
| Uva | Nucleo. |
| Arandano | Nucleo. |
| Esparrago | Secundario condicionado. |
| Cacao | Excluido. |

## B.2 Model Card - Prediccion tabular

| Campo | Especificacion |
|---|---|
| Modelos | XGBoost, LightGBM. |
| Objetivo | Estimar precio o volumen esperado. |
| Entradas | Variables comerciales, macro, internas, climaticas, logisticas y sanitarias. |
| Riesgos | Proxies agregados pueden no representar embarques individuales. |
| Mitigacion | Registrar fuente, granularidad y tipo metodologico por variable. |

## B.3 Model Card - Deteccion de anomalias

| Campo | Especificacion |
|---|---|
| Modelos | Isolation Forest, LOF, ECOD, ensemble. |
| Objetivo | Producir score de anomalia. |
| Entradas | Variables procesadas y residuos de prediccion si aplica. |
| Riesgos | Etiquetas de anomalia pueden ser derivadas o sinteticas. |
| Mitigacion | Separar resultados reales, proxy y sinteticos; priorizar PR-AUC en clases desbalanceadas. |

## B.4 Model Card - SHAP/TreeSHAP

| Campo | Especificacion |
|---|---|
| Metodo | SHAP/TreeSHAP. |
| Objetivo | Explicar contribucion de variables al score o prediccion. |
| Uso | Top-k variables por alerta. |
| Riesgo | Interpretar SHAP como causalidad. |
| Mitigacion | Reportar como atribucion del modelo. |

## B.5 Model Card - Reportes RAG/LLM

| Campo | Especificacion |
|---|---|
| Metodo | LLM restringido por RAG. |
| Objetivo | Redactar reporte tecnico trazable. |
| Entradas | Registro, modelo, score, umbral, SHAP, fuente y evidencia recuperada. |
| Riesgo | Alucinacion numerica o causal. |
| Mitigacion | Validar que cada cifra del reporte exista en evidencia estructurada. |

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo C - Datasheet del Dataset Agroexportador Integrado

> Estandar aplicado: Datasheets for Datasets (Gebru et al., 2021).  
> Version metodologica: v2.0 integrada.  
> Estado: actualizado al panorama de fuentes reales, agregadas, proxies y sinteticas controladas.

---

### C.1 Motivacion

El dataset se construye para entrenar y evaluar un sistema integrado de supervision operativa con IA explicable aplicado a agroexportaciones peruanas. A diferencia de la version inicial basada en un dataset sintetico, esta version adopta un enfoque integrado y trazable:

1. Datos reales observados de exportacion.
2. Datos reales agregados de mercado y contexto.
3. Proxies publicos para clima, logistica y sanidad.
4. Datos sinteticos controlados solo para escenarios auxiliares, balanceo o etiquetas experimentales.

El proposito es permitir evaluacion tecnica, explicabilidad SHAP y reportes RAG sin ocultar el origen ni la granularidad de cada variable.

### C.2 Composicion

Productos:

| Producto | HS | Estado |
|---|---|---|
| Palta | `080440` | Nucleo. |
| Uva | `080610` | Nucleo. |
| Arandano | `081040` | Nucleo. |
| Esparrago | `070920` | Secundario condicionado. |
| Cacao | No aplica al nucleo | Excluido por baja representatividad. |

Fuentes:

| Tipo | Fuente | Ruta local | Granularidad |
|---|---|---|---|
| Real observada | SUNAT/ADUANET | `data/sunat/`, `codex-revision/data_raw/aduanet_bases` | Embarque o serie aduanera. |
| Real observada/auditada | Dataset local | `data/dataset_real_v1.csv` | Registro transaccional. |
| Real agregada | Trade Map | `data-trademap/export_*` | Producto-destino-anio. |
| Real agregada | SISAP/MIDAGRI | `codex-revision/data_processed/sisap_midagri/` | Producto-mes-variedad. |
| Real agregada | BCRP | `data/bcrp/`, `codex-revision/data_raw/bcrp/` | Mes. |
| Proxy | NASA/SENAMHI/NDVI | `codex-revision/data_raw/nasa_power`, `data/vegetation/` | Region-mes. |
| Proxy | APN/OSITRAN | `codex-revision/data_raw/apn_*`, `codex-revision/data_raw/ositran_*` | Puerto-mes. |
| Proxy/contexto | SENASA/FDA/RASFF | `codex-revision/data_raw/senasa`, `fda`, `rasff` | Producto/destino/mes si existe. |
| Sintetica controlada | Dataset sintetico | `data/dataset_agro_sintetico_v1.csv` | Escenario experimental. |

### C.3 Variables principales

| Variable | Tipo | Fuente preferida | Etiqueta |
|---|---|---|---|
| `producto` | categoria | SUNAT/dataset real | real_observada |
| `hs` | string | SUNAT/Trade Map | real_observada |
| `fecha` | fecha | SUNAT/dataset real | real_observada |
| `periodo_mes` | fecha mensual | derivada | derivada |
| `volumen_kg` | numerica | SUNAT/dataset real | real_observada |
| `valor_fob_usd` | numerica | SUNAT | real_observada |
| `precio_kg_usd` | numerica | FOB/kg o dataset real | derivada |
| `destino_mercado` | categoria | SUNAT/Trade Map | real_observada |
| `sisap_precio_prom` | numerica | SISAP | real_agregada |
| `sisap_volumen` | numerica | SISAP | real_agregada |
| `tipo_cambio_pen_usd` | numerica | BCRP | real_agregada |
| `temperatura_max_c` | numerica | NASA/SENAMHI | proxy |
| `precipitacion_mm` | numerica | NASA/SENAMHI | proxy |
| `carga_portuaria_mes` | numerica | APN/OSITRAN | proxy |
| `alertas_sanitarias_mes` | numerica | SENASA/FDA/RASFF | proxy |
| `etiqueta_anomalia` | binaria | regla/modelo/dataset | derivada o sintetica |
| `tipo_anomalia` | categoria | regla/modelo/dataset | derivada o sintetica |
| `regla_inyeccion` | texto | generacion experimental | sintetica |

### C.4 Datos sinteticos controlados

Los datos sinteticos no sustituyen a las fuentes reales. Se permiten para:

- Balancear clases de anomalias en entrenamiento.
- Simular escenarios de supervision.
- Probar reportes SHAP/RAG.
- Crear etiquetas experimentales cuando no existe etiqueta oficial de anomalia.

Reglas de inyeccion permitidas:

| Tipo | Variables afectadas | Uso |
|---|---|---|
| Precio | `precio_kg_usd`, residuo de precio | Outliers comerciales. |
| Volumen | `volumen_kg` | Cambios atipicos de escala. |
| Clima | temperatura, precipitacion | Escenarios agroclimaticos. |
| Logistica | `dias_logisticos`, carga portuaria | Demoras o presion portuaria. |
| Calidad | `merma_pct`, cumplimiento | Escenarios de deterioro o riesgo. |

Toda fila o variable sintetica debe tener `origen_dato = sintetica` y `regla_inyeccion` no vacia.

### C.5 Preprocesamiento

El pipeline debe:

- Homologar productos y HS.
- Excluir cacao del dataset final.
- Mantener esparrago como secundario si pasa validacion.
- Convertir fechas a `YYYY-MM-DD` y `YYYY-MM`.
- Preservar `fuente`, `archivo_origen`, `granularidad` y `tipo_variable`.
- Separar train/validation/test de forma temporal.
- Evitar que datos sinteticos o SMOTE entren al test final real.

### C.6 Usos previstos

- Entrenamiento de modelos tabulares.
- Deteccion de anomalias.
- Explicabilidad SHAP.
- Generacion de reportes RAG.
- Analisis de trazabilidad de alertas.
- Soporte documental para metodologia y anexos.

### C.7 Usos no previstos

- Tomar decisiones operativas reales sin validacion empresarial.
- Afirmar causalidad a partir de SHAP.
- Presentar proxies como observaciones por embarque.
- Presentar datos sinteticos como registros oficiales.

### C.8 Consideraciones eticas

El dataset integrado debe proteger trazabilidad y transparencia. Cuando se usen empresas o RUC reales de fuentes publicas, se evaluara anonimizar o agrupar en reportes publicos. Los reportes RAG deben indicar sus fuentes y no emitir recomendaciones fuera de la evidencia recuperada.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo D — Registro de Uso de Herramientas de IA

La presente investigación utilizó herramientas de inteligencia artificial generativa como apoyo en las siguientes actividades: revisión bibliográfica exploratoria, verificación de coherencia de argumentos, corrección de estilo académico y generación de borradores de secciones específicas. Todas las referencias bibliográficas fueron verificadas manualmente en las fuentes originales. Las decisiones de diseño, la interpretación de resultados y las conclusiones son responsabilidad exclusiva del investigador.

*(Adjuntar registro detallado de las sesiones de uso según los requerimientos de transparencia de la UNSA)*

---

*(Documento elaborado con apoyo de herramientas de IA — UNSA Arequipa, 2026)*

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo E - Resumen general del sistema

Este anexo resume la investigacion bajo la version metodologica actual: sistema integrado de supervision operativa con IA explicable y dataset agroexportador integrado.

## 1. Arquitectura modular

| Capa | Funcion |
|---|---|
| Capa 1 | Prediccion tabular con XGBoost/LightGBM. |
| Capa 2 | Deteccion de anomalias con IF + LOF + ECOD. |
| Capa 3 | Explicabilidad con SHAP/TreeSHAP. |
| Capa 4 | Reportes trazables con RAG/LLM. |

## 2. Base de datos

La evaluacion final debe basarse en un dataset agroexportador integrado:

- SUNAT/ADUANET y dataset real local como base observada.
- Trade Map como benchmark externo.
- SISAP/MIDAGRI como mercado interno para palta, uva y esparrago.
- BCRP como control macro.
- Clima, logistica y sanidad como proxies.
- Sinteticos solo como apoyo experimental.

## 3. Productos

| Producto | Estado |
|---|---|
| Palta | Nucleo. |
| Uva | Nucleo. |
| Arandano | Nucleo. |
| Esparrago | Secundario condicionado. |
| Cacao | Excluido. |

## 4. Estado de resultados

Los resultados obtenidos sobre versiones sinteticas o corridas previas deben considerarse preliminares hasta ejecutar el entrenamiento final sobre el dataset integrado. No se deben presentar como conclusiones finales si no cuentan con reporte de entrenamiento, version de dataset y trazabilidad.

## 5. Gobernanza y trazabilidad

Cada alerta valida debe incluir:

- dato de origen;
- version del dataset;
- modelo y parametros;
- score y umbral;
- variables SHAP;
- fuente recuperada por RAG;
- reporte generado.

---

#### `2.3.4. Datos tabulares en sistemas empresariales`
*(Sección no encontrada para el patrón ### 2.3.4 Deteccin de Anomalas)*

#### `2.3.5. Series temporales y predicción`
### 2.3.5 Forecasting de Series Temporales con Transformers

Las series temporales agroexportadoras presentan tres desafíos que los modelos de forecasting deben resolver: tendencia no estacionaria, estacionalidad múltiple (diaria, semanal, mensual, anual) y dependencia de covariables exógenas (clima, calendario agrícola, demanda internacional, precios y condiciones logísticas). Los modelos estadísticos clásicos como ARIMA capturan relaciones lineales con eficacia, pero presentan limitaciones en la modelización de no-linealidades y horizontes largos.

**Temporal Fusion Transformer (TFT)** (Lim et al., 2021) propone una arquitectura especializada que combina cuatro mecanismos: (1) codificación LSTM para dependencias secuenciales locales; (2) selección de variables con mecanismo de gating (GLU — Gated Linear Unit) que identifica automáticamente las covariables más informativas; (3) atención multi-cabezal interpretable que pondera los pasos temporales según su relevancia predictiva; y (4) red de cuantiles para cuantificar la incertidumbre de la predicción. TFT acepta tres tipos de entradas: features estáticas conocidas (e.g., producto, zona, destino), covariables futuras conocidas (e.g., calendario agrícola, campañas, feriados) y covariables históricas observadas (e.g., precio, volumen, clima o merma pasada).

El debate sobre la efectividad de los Transformers en series temporales es relevante para esta tesis. Zeng et al. (2023) argumentan que DLinear —un modelo lineal simple— supera a los Transformers en múltiples benchmarks, atribuyendo la limitación de los Transformers al hecho de que el mecanismo de self-attention es permutation-invariant y destruye el orden temporal de las secuencias. Sin embargo, este argumento ha sido rebatido sucesivamente: Nie et al. (2023) demuestran que la tokenización por patches —agrupando segmentos temporales antes de aplicar atención— preserva el orden local y supera a DLinear en la mayoría de benchmarks de horizonte largo. Liu et al. (2024) proponen invertir la tokenización: en lugar de tokenizar por timestamp, tokenizan por variable, aplicando self-attention entre variables en lugar de entre tiempos, obteniendo SOTA en 7 datasets multivariados.

**Posición de esta tesis respecto al debate**: TFT se considera por su interpretabilidad incorporada —el mecanismo de gating y los mapas de atención son legibles por analistas— más que exclusivamente por su rendimiento predictivo. En el contexto agroexportador, la capacidad de justificar qué períodos temporales y qué covariables fundamentan la predicción es un requerimiento funcional comparable en importancia a la precisión numérica.

N-HiTS (Challu et al., 2022) ofrece una alternativa no-Transformer para forecasting de horizonte largo, con interpolación jerárquica multi-tasa que reduce la complejidad computacional respecto a N-BEATS. Chronos (Ansari et al., 2024) representa el paradigma emergente de los foundation models para series temporales, basado en T5, que logra performance zero-shot competitivo en múltiples datasets; sin embargo, su opacidad y dependencia de infraestructura de gran escala limitan su aplicación directa cuando se requiere trazabilidad operativa.

#### `2.3.6. Detección de anomalías`
### 2.3.6 Explicabilidad mediante SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)

La explicabilidad en sistemas de IA se clasifica en dos grandes categorías: **inherente** —modelos cuya estructura es intrínsecamente interpretable, como los árboles de decisión— y **post-hoc** —métodos aplicados a cualquier modelo después del entrenamiento para interpretar sus predicciones. SHAP y LIME son los dos métodos post-hoc agnósticos más adoptados en la literatura.

**LIME** (Local Interpretable Model-agnostic Explanations) (Ribeiro et al., 2016) genera explicaciones locales construyendo un modelo lineal sustituto en el vecindario de la instancia a explicar, ponderando las muestras según su proximidad al punto de interés. LIME es rápido y flexible, pero produce explicaciones inestables: pequeñas perturbaciones de la instancia pueden cambiar significativamente la explicación, un problema crítico en contextos forenses.

**SHAP** (Lundberg & Lee, 2017) fundamenta las explicaciones en los valores de Shapley de la teoría de juegos cooperativos. El valor SHAP de la feature $i$ para la predicción $f(x)$ cuantifica la contribución marginal media de $i$ a la predicción, promediando sobre todas las coaliciones posibles de features:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!} [f(S \cup \{i\}) - f(S)]$$

donde $F$ es el conjunto de todas las features y $S$ es una coalición de features sin $i$. Esta formulación garantiza cuatro propiedades axiomáticas: (a) **eficiencia** — la suma de todos los valores SHAP iguala la diferencia entre la predicción y el valor esperado; (b) **simetría** — features con contribución idéntica reciben el mismo valor; (c) **dummy** — features sin efecto tienen valor cero; y (d) **aditividad** — los valores SHAP son consistentes al combinar modelos.

SHAP resuelve las limitaciones de LIME al garantizar consistencia: si un modelo cambia la predicción al aumentar la contribución de una feature, el valor SHAP de esa feature nunca disminuye (Lundberg & Lee, 2017). **TreeSHAP** extiende este cálculo con un algoritmo exacto en O(TLD²) para modelos basados en árboles —donde T es el número de árboles, L es el número de hojas por árbol y D es la profundidad máxima— haciendo el cálculo computacionalmente viable para GBDT en producción.

En el contexto de supervisión operativa, la estabilidad de las explicaciones permite verificar que el modelo asigna importancias consistentes a variables semejantes. Un índice alto de estabilidad fortalece la confianza en el sistema, porque evita que alertas similares reciban justificaciones contradictorias.

La integración SHAP+LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño) de esta tesis opera como sigue: los vectores SHAP de una alerta operativa (una lista de pares variable→contribución cuantitativa) se incorporan como contexto verificado en el RAG, y el LLM genera la narración del informe sin posibilidad de inventar cifras que no estén en esos vectores o en las fuentes recuperadas.

#### `2.3.7. Detección de fraude y auditoría inteligente`
> La detección de fraude y la auditoría inteligente constituyen áreas críticas de los sistemas empresariales modernos. Tradicionalmente orientadas al análisis de estados financieros y registros contables (como el framework *AuditCopilot* propuesto por Kadir et al., 2025), estas disciplinas aplican algoritmos de inteligencia artificial para identificar irregularidades transaccionales y de control interno. En esta tesis, se adapta conceptualmente la lógica de la auditoría inteligente para estructurar un proceso de **supervisión operativa continua** en la agroexportación peruana. Esto permite auditar la calidad, consistencia y trazabilidad de los datos operativos transaccionales (volumen, precio, clima, logística) y mapear cada alerta del ensemble de anomalías a sus evidencias cuantitativas de origen, cumpliendo con los principios de gobernanza y auditabilidad tecnológica.

#### `2.3.8. Modelos de lenguaje (LLMs) y generación de reportes`
### 2.3.7 Modelos de Lenguaje y Arquitectura RAG para Generación de Reportes

Los LLMs (Large Language Models - Modelos de Lenguaje de Gran Tamaño) son sistemas entrenados mediante autoregresión en corpus masivos de texto para aprender distribuciones probabilísticas sobre secuencias de tokens. Su capacidad de generalización les permite realizar tareas de reasoning, traducción, resumen y generación de texto con calidad próxima a la humana en configuraciones zero-shot y few-shot.

**In-context learning** permite guiar el comportamiento del LLM mediante ejemplos incluidos directamente en el prompt, sin necesidad de ajuste fino (fine-tuning). TabLLM (Hegselmann et al., 2023) demostró que mediante serialización de datos tabulares a texto descriptivo, los LLMs pueden realizar clasificación sobre datos estructurados con rendimiento no trivial en zero-shot, ampliando el espectro de aplicación de estos modelos más allá del texto no estructurado.

Sin embargo, el uso de LLMs como agentes de decisión autónoma introduce el riesgo de **alucinaciones**: el modelo puede generar afirmaciones coherentes en forma pero incorrectas en contenido (Ji et al., 2023; Maynez et al., 2026). La literatura distingue al menos dos tipos: (a) alucinaciones intrínsecas, en las que el texto generado contradice la información del contexto recuperado; y (b) alucinaciones extrínsecas, en las que el modelo inventa información no presente en el contexto. En particular, las "alucinaciones numéricas" —valores específicos de métricas, porcentajes o fechas que no corresponden a los datos reales (Barclays Research, 2025)— son especialmente peligrosas en reportes operativos, porque pueden inducir decisiones equivocadas pese a la apariencia de precisión cuantitativa.

**RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)** (Lewis et al., 2020; Schneider et al., 2025) reduce este riesgo al separar el conocimiento factual del modelo generativo: en lugar de que el LLM "recuerde" información de su entrenamiento, el sistema recupera documentos o datos relevantes de una base de conocimiento externa verificada y los incluye en el contexto del prompt. El LLM entonces genera texto fundamentado en esos datos recuperados, no en su memoria paramétrica. Es importante señalar que RAG **reduce significativamente pero no elimina** el riesgo de alucinación; persisten casos de alucinación intrínseca (faithful hallucination) en los que el modelo genera afirmaciones que se desvían del contexto recuperado. Técnicas avanzadas como GraphRAG incorporan grafos de conocimiento para recuperación semántica más rica, mientras que Self-RAG permite al modelo verificar la pertinencia de los documentos recuperados antes de usarlos.

En la arquitectura de esta tesis, la "base de conocimiento" del RAG son los vectores SHAP de la alerta analizada, las métricas del ensemble de detección, las fuentes agroexportadoras recuperadas y las reglas de reporte definidas. El LLM recibe ese contexto verificado y genera el informe narrativo sin acceso a conocimiento adicional no validado. Adicionalmente se aplican dos controles complementarios: (a) plantillas de prompt estructurado con campos obligatorios (dato, modelo, score, umbral, explicación SHAP, fuente recuperada), y (b) validación posterior del reporte contra los vectores SHAP de entrada para detectar discrepancias numéricas. Este diseño permite que cada afirmación del reporte pueda trazarse hasta una fuente, score, umbral o variable explicativa.

La evaluación de calidad de los reportes generados puede utilizar **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) cuando exista un texto de referencia. Sin embargo, para esta tesis se prioriza una rúbrica operativa de completitud, consistencia, accionabilidad y correspondencia con evidencias, porque la calidad de un reporte de supervisión depende no solo de similitud textual, sino de su utilidad para la toma de decisiones.

#### `2.3.9. Gobernanza y calidad en sistemas de IA`
> ### 2.3.8 Gobernanza de IA y MLOps

El despliegue de sistemas de IA en entornos empresariales críticos requiere un marco de gobernanza que trascienda el rendimiento técnico. Sculley et al. (2015) documentaron la "deuda técnica oculta" en sistemas de ML: más del 95% del código de un sistema ML de producción no es el modelo en sí, sino la infraestructura de ingesta, validación, features, servicio y monitoreo. Los pipelines con alto acoplamiento entre componentes generan "entanglement" que dificulta el mantenimiento y aumenta el riesgo de regresiones silenciosas.

**MLOps** (Kreuzberger et al., 2022) establece el conjunto de prácticas para gestionar el ciclo de vida completo de los modelos ML en producción: integración y entrega continua (CI/CD) para modelos, monitoreo de data drift y model drift, automatización del reentrenamiento, y trazabilidad de versiones de datos, código y modelos. En el contexto de supervisión operativa agroexportadora, MLOps permite reproducir qué modelo generó una alerta, con qué datos de entrada, bajo qué versión y con qué umbral.

El **NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0)** (NIST, 2023) proporciona cuatro funciones de gestión de riesgo para sistemas de IA: (1) **Govern** — establecer políticas y roles de responsabilidad; (2) **Map** — identificar el contexto de despliegue y los riesgos asociados; (3) **Measure** — evaluar los riesgos con métricas verificables; y (4) **Manage** — implementar controles y mitigaciones. La arquitectura modular de esta tesis es diseñada para que cada capa corresponda a responsabilidades verificables bajo este framework.

**Datasheets for Datasets** (Gebru et al., 2021) propone una plantilla de documentación estandarizada para datasets que detalla: motivación de recolección, proceso de recolección, composición, preprocesamiento aplicado, distribución permitida y consideraciones éticas. Esta práctica se aplicará al dataset agroexportador integrado y a sus capas de datos reales, agregados, proxies y sintéticos controlados, garantizando que los resultados reportados sean reproducibles y que las limitaciones de cada fuente estén identificadas antes de evaluar el sistema.

**Model Cards** (Mitchell et al., 2019) extiende la documentación al nivel del modelo, especificando para quién fue entrenado, en qué condiciones, cuáles son sus limitaciones conocidas y cómo debe usarse de manera responsable. En esta tesis, se elaboran Model Cards para los modelos XGBoost/LightGBM, detectores de anomalías y el componente LLM+RAG, en conformidad con los principios de documentación del NIST AI RMF (NIST, 2023).

El contexto peruano e internacional consolida la necesidad de este framework de gobernanza. El D.S. N° 115-2025-PCM (PCM, 2025), el NIST AI RMF (NIST, 2023) y el EU AI Act (Parlamento Europeo y Consejo, 2024) refuerzan principios comunes: transparencia, documentación, supervisión humana y gestión de riesgos. Estos principios son adoptados como referencia de diseño para esta tesis. No se afirma cumplimiento formal con ninguno de estos marcos —tal afirmación requeriría auditoría regulatoria externa— sino conformidad de diseño con sus principios, en particular: (a) transparencia mediante SHAP y Model Cards, (b) supervisión humana mediante revisión obligatoria de cada reporte antes de su uso operativo, (c) gestión de riesgos mediante umbrales calibrados y validación cruzada, y (d) trazabilidad documental mediante logs completos por alerta. La aplicabilidad regulatoria efectiva del sistema a una empresa específica depende de su clasificación de riesgo bajo el reglamento correspondiente y queda fuera del alcance de esta tesis.

### 2.3.9 Supervisión Operativa, Trazabilidad e Inteligencia Artificial

La supervisión operativa en agroexportación exige monitorear procesos que combinan producción, acopio, calidad, sanidad, logística y comercio exterior. Las anomalías en este dominio no necesariamente corresponden a fraude; pueden representar variaciones atípicas de precio, caídas de volumen, condiciones climáticas adversas, mermas elevadas, incumplimientos fitosanitarios o retrasos logísticos. Por ello, el sistema propuesto se orienta a detectar desviaciones relevantes para la toma de decisiones, no a sustituir procesos de investigación legal o auditoría financiera.

La **supervisión operativa continua** busca reemplazar ciclos de revisión tardíos por monitoreo frecuente y documentado de indicadores. En este enfoque, cada alerta debe registrar el dato de origen, el modelo aplicado, el score calculado, el umbral utilizado, las variables explicativas y el reporte generado. Esta trazabilidad permite que un supervisor operativo comprenda por qué el sistema marcó un evento como anómalo y qué evidencia respalda la recomendación.

La integración de IA en supervisión operativa plantea el problema de la confianza en decisiones automáticas. Esta exigencia convierte a la explicabilidad (SHAP), la documentación de datasets (Datasheets), la documentación de modelos (Model Cards) y los logs de decisión en componentes funcionales del sistema. En el marco peruano, el D.S. N° 115-2025-PCM (PCM, 2025) proporciona una base general para el uso responsable de IA; la Resolución SBS N° 053-2023 (SBS, 2023) se conserva solo como referencia nacional de buenas prácticas para gestión de riesgo de modelos.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

<div style="background-color: orange; color: white; padding: 10px; text-align: center; font-weight: bold; margin-bottom: 20px; border-radius: 5px;">EN DESARROLLO</div>

# CAPITULO III: PROPUESTA METODOLOGICA

## 3.1 Arquitectura del sistema integrado

La arquitectura propuesta se divide en cuatro capas secuenciales y trazables:

1. **Capa 1: Prediccion tabular.** Modelos GBDT, principalmente XGBoost y LightGBM, estiman valores esperados de precio o volumen usando variables comerciales, macroeconomicas, climaticas, logisticas y de contexto.
2. **Capa 2: Deteccion de anomalias.** Un ensemble de Isolation Forest, LOF y ECOD produce un score de anomalia. El LLM no detecta anomalias.
3. **Capa 3: Explicabilidad.** SHAP/TreeSHAP identifica las variables con mayor contribucion a la alerta. Las explicaciones son atribuciones del modelo, no causalidad.
4. **Capa 4: Reportes RAG/LLM.** Un LLM restringido por evidencias redacta reportes tecnicos a partir de datos, score, umbral, SHAP, fuente y metadatos.

```
[Dataset agroexportador integrado]
        |
        v
[Capa 1: GBDT] -> valor esperado / residuo
        |
        v
[Capa 2: IF + LOF + ECOD] -> score anomalia
        |
        v
[Capa 3: SHAP] -> top variables explicativas
        |
        v
[Capa 4: RAG/LLM] -> reporte trazable
```

## 3.2 Dataset agroexportador integrado y trazable

La validacion principal no dependera de un dataset sintetico aislado. Se trabajara con un **dataset agroexportador integrado**, construido desde cuatro tipos de informacion:

| Capa de datos | Fuentes | Rol |
|---|---|---|
| Datos reales observados | SUNAT/ADUANET, `data/dataset_real_v1.csv` | Base primaria de exportaciones. |
| Datos reales agregados | Trade Map, SISAP/MIDAGRI, BCRP, MIDAGRI compendios, FAOSTAT | Validacion externa y contexto. |
| Proxies documentados | NASA POWER, SENAMHI, APN, OSITRAN, SENASA/FDA/RASFF | Variables explicativas agregadas. |
| Datos sinteticos controlados | `data/dataset_agro_sintetico_v1.csv` y reglas de inyeccion | Escenarios auxiliares, balanceo y etiquetas experimentales. |

### 3.2.1 Segmentacion de productos

| Producto | HS | Decision |
|---|---|---|
| Palta | `080440` | Producto nucleo. |
| Uva | `080610` | Producto nucleo. |
| Arandano | `081040` | Producto nucleo; sin dependencia de SISAP. |
| Esparrago | `070920` | Producto secundario condicionado. |
| Cacao | Verificar | Excluido del nucleo por baja representatividad. |

### 3.2.2 Uso de fuentes

- **SUNAT/ADUANET:** fuente primaria para volumen, valor FOB, partida, fecha, empresa y destino.
- **Trade Map:** benchmark internacional por producto y mercado destino.
- **SISAP/MIDAGRI:** precio y volumen mayorista interno para palta, uva y esparrago; no mide exportaciones.
- **BCRP:** tipo de cambio mensual.
- **Clima/logistica/sanidad:** proxies agregados cuando no existe llave directa por embarque.
- **Sinteticos:** escenarios controlados y balanceo, siempre etiquetados.

## 3.3 Configuracion experimental y metricas

### 3.3.1 Division temporal

Para evitar fuga de informacion temporal:

- Train: 70% inicial.
- Validation: 10% siguiente.
- Test: 20% final.

El split aleatorio no se usara como evaluacion principal.

### 3.3.2 Metricas por variable dependiente

| VD | Metricas |
|---|---|
| VD1 rendimiento | PR-AUC, ROC-AUC, F1, precision, recall. |
| VD2 explicabilidad | Cobertura top-k SHAP, estabilidad, claridad. |
| VD3 reportes | Rubrica de completitud, consistencia, accionabilidad y evidencia. |
| VD4 decision | Tiempo-a-decision, Likert, decision correcta. |
| VD5 trazabilidad | Porcentaje de alertas con campos completos. |

### 3.3.3 Experimentos E1-E5

| Exp. | Nombre | Condicion experimental | Control | VD |
|---|---|---|---|---|
| E1 | Rendimiento de deteccion | Ensemble IF + LOF + ECOD | Detectores individuales | VD1 |
| E2 | Aporte SHAP | Alertas con SHAP | Alertas solo con score | VD2 |
| E3 | Aporte RAG | Reporte RAG anclado | LLM sin RAG | VD3 |
| E4 | Sistema integrado | Pipeline completo | Componentes aislados | VD4, VD5 |
| E5 | Ablation | Variantes por capas | Pipeline completo | VD1, VD5 |

### 3.3.4 Baselines

- B1: Isolation Forest individual.
- B2: Ensemble IF + LOF.
- B3: XGBoost supervisado si existe etiqueta confiable.
- B4: LLM sin RAG ni evidencia SHAP.

## 3.4 Reproducibilidad

Cada corrida debe registrar:

- Version del dataset.
- Fecha de generacion.
- Fuentes usadas.
- Semilla.
- Particion temporal.
- Modelo y parametros.
- Metricas.
- Reporte de trazabilidad.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CAPITULO IV: RESULTADOS Y DISCUSION

> **Estado:** capitulo modularizado. Los resultados finales se completaran unicamente despues de ejecutar los experimentos E1-E5 sobre el dataset agroexportador integrado versionado.

Este capitulo organiza la evaluacion empirica del sistema integrado de supervision operativa. Su funcion actual es dejar preparada la estructura de reporte, los criterios de lectura y las tablas que recibiran los resultados finales.

Los valores obtenidos en corridas previas sobre datasets sinteticos o versiones anteriores se consideran evidencia auxiliar de desarrollo. No deben presentarse como resultados finales de tesis hasta que se regeneren con:

- version del dataset integrado;
- split temporal documentado;
- codigo de experimento;
- fecha de ejecucion;
- semillas utilizadas;
- reporte de calidad de datos;
- trazabilidad de fuente para cada variable.

La estructura del capitulo queda dividida en modulos para facilitar mantenimiento:

| Modulo | Archivo | Contenido |
|---|---|---|
| 4.1 | `docs/02-41-capitulo4-resultados-cuantitativos.md` | Prediccion y deteccion, VD1. |
| 4.2 | `docs/02-42-capitulo4-explicabilidad-reportes.md` | SHAP y reportes RAG, VD2-VD3. |
| 4.3 | `docs/02-43-capitulo4-usabilidad-trazabilidad.md` | Estudio de usuarios y trazabilidad, VD4-VD5. |
| 4.4 | `docs/02-44-capitulo4-discusion.md` | Discusion, contraste con literatura e hipotesis. |
| 4.5-4.6 | `docs/02-45-capitulo4-limitaciones-sintesis.md` | Limitaciones y sintesis final. |

La lectura del capitulo debe conservar una regla metodologica: **ninguna metrica se interpreta sin indicar fuente, version de dataset, granularidad, split y estado de validacion**.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.1 Resultados Cuantitativos: Prediccion y Deteccion, VD1

Esta seccion reportara el rendimiento de la capa predictiva tabular y del ensemble de deteccion de anomalias. La evaluacion principal se realizara sobre el dataset agroexportador integrado, no sobre el dataset sintetico aislado.

### 4.1.1 Condiciones minimas para reportar resultados

Antes de completar las tablas, debe existir evidencia local de:

| Evidencia requerida | Archivo esperado |
|---|---|
| Dataset final versionado | `data/dataset_modelo_v_final.csv` o `codex-revision/data_processed/dataset_modelo_v_final.csv` |
| Split temporal | `dataset_train_raw.csv`, `dataset_validation.csv`, `dataset_test.csv` |
| Reporte de calidad | `reporte-calidad-datos.md` |
| Reporte de entrenamiento | `reporte-entrenamiento-modelos.md` |
| Configuracion de semillas | archivo de experimento o log reproducible |

### 4.1.2 Tabla 4.1 - Rendimiento de deteccion, Experimento E1

| Metodo | Dataset/version | PR-AUC | ROC-AUC | F1 | Precision | Recall | Tiempo inferencia | Estado |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Isolation Forest individual, B1 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| LOF individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| ECOD individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Ensemble IF + LOF | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Ensemble IF + LOF + ECOD, propuesto | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| XGBoost/LightGBM supervisado, upper bound si hay etiqueta | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Condicionado |

> Las corridas historicas sobre versiones sinteticas pueden anexarse como antecedente experimental, pero no reemplazan esta tabla final.

### 4.1.3 Tabla 4.2 - Recall por tipo de anomalia

| Tipo de anomalia | Origen de etiqueta | Recall ensemble | Recall baseline | Diferencia | Estado |
|---|---|---:|---:|---:|---|
| precio | derivada/proxy/sintetica controlada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| volumen | derivada/proxy/sintetica controlada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| clima | proxy o regla documentada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| logistica | proxy o regla documentada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| sanidad/calidad | proxy o regla documentada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

La columna de origen es obligatoria porque `etiqueta_anomalia` puede provenir de observacion real, regla derivada, proxy o inyeccion sintetica controlada. Esa distincion determina el alcance de la interpretacion.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.2 Resultados Cualitativos: Explicabilidad y Reportes, VD2-VD3

Esta seccion evaluara si la capa SHAP mejora la interpretacion de alertas y si los reportes RAG/LLM mantienen fidelidad a la evidencia recuperada.

### 4.2.1 Tabla 4.3 - Calidad de explicabilidad, Experimento E2

| Metrica | Sistema con SHAP | Sistema sin SHAP | p-value | Estado |
|---|---:|---:|---:|---|
| Cobertura top-3 | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Cobertura top-5 | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Estabilidad SHAP | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Claridad operativa Likert 1-5 | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

SHAP se interpretara como atribucion del modelo, no como causalidad. Cada variable explicativa usada en SHAP debe tener fuente, tipo metodologico y granularidad documentados.

### 4.2.2 Tabla 4.4 - Calidad de reportes generados, Experimento E3

| Dimension | RAG/LLM anclado | LLM libre/control | Kappa Cohen | p-value | Estado |
|---|---:|---:|---:|---:|---|
| Completitud | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Consistencia numerica | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Correspondencia con evidencia | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Accionabilidad | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Coherencia textual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

El reporte RAG debe citar o registrar internamente:

- registro evaluado;
- score y umbral;
- top variables SHAP;
- fuente recuperada;
- version de dataset;
- fecha de generacion;
- advertencia cuando una variable sea proxy o sintetica controlada.

### 4.2.3 Ejemplo de reporte generado

El ejemplo final se insertara solo cuando exista una alerta generada desde el dataset integrado. Debe seguir el patron:

`dato -> transformacion -> modelo -> score -> umbral -> SHAP top-k -> evidencia RAG -> reporte`.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.3 Resultados del Estudio de Usabilidad y Trazabilidad, VD4-VD5

Esta seccion medira si el sistema integrado reduce el tiempo de interpretacion y mejora la trazabilidad documental frente a componentes aislados.

### 4.3.1 Tabla 4.5 - Tiempo-a-decision y comprension, Experimento E4

| Metrica | Sistema integrado | Componentes aislados | Diferencia relativa | p-value | Tamano de efecto | Estado |
|---|---:|---:|---:|---:|---:|---|
| Tiempo-a-decision, segundos | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Comprension Likert 1-5 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Decision correcta | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| SUS Score 0-100 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

El tamano muestral y el perfil de participantes se reportaran como estudio piloto especializado si no alcanzan potencia estadistica suficiente para generalizacion amplia.

### 4.3.2 Tabla 4.6 - Trazabilidad documental, VD5

| Configuracion | Alertas con trazabilidad completa | Campos faltantes frecuentes | Estado |
|---|---:|---|---|
| Sistema integrado completo, E5d | _pendiente_ | _pendiente_ | Por ejecutar |
| Ablation sin SHAP, E5b | _pendiente_ | _pendiente_ | Por ejecutar |
| Ablation sin RAG, E5c | _pendiente_ | _pendiente_ | Por ejecutar |
| Componentes aislados/control | _pendiente_ | _pendiente_ | Por ejecutar |

La trazabilidad completa exige, como minimo: `id_alerta`, `producto`, `hs`, `fecha`, `fuentes_usadas`, `score`, `umbral`, `top_shap`, `evidencia_rag`, `version_dataset` y `archivo_origen`.

### 4.3.3 Tabla 4.7 - Ablation study, Experimento E5

| Configuracion | Capa 1 prediccion | Capa 2 anomalias | Capa 3 SHAP | Capa 4 RAG | VD1 | VD3 | VD5 | Estado |
|---|---|---|---|---|---:|---:|---:|---|
| E5a solo deteccion | No | Si | No | No | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| E5b sin SHAP | Si | Si | No | Si | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| E5c sin RAG | Si | Si | Si | No | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| E5d pipeline completo | Si | Si | Si | Si | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

Las comparaciones E5 no deben mezclar resultados de dataset sintetico con resultados del dataset integrado sin una etiqueta explicita de version.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.4 Discusion y Cruce Comparativo

### 4.4.1 Proposito de la discusion

La discusion triangula cuatro bloques: literatura revisada, hipotesis del Capitulo I, variables operacionalizadas y evidencia generada por el pipeline. Su objetivo es explicar los resultados sin convertir correlaciones, scores o valores SHAP en afirmaciones causales.

### 4.4.2 Cruce 1 - Resultados propios versus literatura comparable

| Atributo | Esta tesis | Literatura comparable | Lectura esperada |
|---|---|---|---|
| Prediccion tabular | XGBoost/LightGBM | GBDT en fraude, auditoria y agroexportacion | Comparar cobertura y estabilidad, no valores absolutos entre dominios. |
| Deteccion de anomalias | Isolation Forest, LOF, ECOD | ADBench/PyOD | Justificar ensemble si mejora o estabiliza resultados. |
| Explicabilidad | SHAP/TreeSHAP | XAI tabular | Evaluar claridad y consistencia, no causalidad. |
| Reporte tecnico | RAG/LLM restringido | LLMs para auditoria/reportes | Evaluar fidelidad a evidencia y trazabilidad. |
| Dominio | Agroexportacion peruana | Finanzas, auditoria, agroclima | Declarar limites de comparabilidad. |

### 4.4.3 Cruce 2 - Contraste de hipotesis

| Hipotesis | Evidencia requerida | Decision |
|---|---|---|
| H1a | Mejora de VD1 frente a detector individual con split temporal documentado. | _pendiente_ |
| H1b | Mejora de VD2 con SHAP frente a condicion sin SHAP. | _pendiente_ |
| H1c | Mejora de VD3 con RAG frente a LLM libre/control. | _pendiente_ |
| H1d | Reduccion de tiempo-a-decision o mejora de comprension. | _pendiente_ |
| H1 general | Mejora conjunta de trazabilidad y supervision operativa. | _pendiente_ |

La decision puede ser: aceptar, rechazar o inconclusa. Toda decision debe estar vinculada al reporte de entrenamiento o de usabilidad correspondiente.

### 4.4.4 Cruce 3 - Variables operacionalizadas versus indicadores observados

| Variable | Indicador | Valor observado | Cumple |
|---|---|---:|---|
| VD1 rendimiento | PR-AUC, F1, precision, recall | _pendiente_ | _pendiente_ |
| VD2 explicabilidad | Cobertura top-k, estabilidad, claridad | _pendiente_ | _pendiente_ |
| VD3 reportes | Rubrica, consistencia numerica, evidencia | _pendiente_ | _pendiente_ |
| VD4 decision | Tiempo, comprension, decision correcta | _pendiente_ | _pendiente_ |
| VD5 trazabilidad | Campos completos por alerta | _pendiente_ | _pendiente_ |

### 4.4.5 Cruce 4 - Gobernanza, componente y metrica

| Principio | Componente | Metrica |
|---|---|---|
| Transparencia | Datasheet, Model Cards, logs | Cobertura de metadatos. |
| Explicabilidad | SHAP/TreeSHAP | VD2. |
| Supervision humana | Protocolo de usabilidad y revision | VD4. |
| Gestion de riesgo | Validacion temporal y umbrales | VD1. |
| Anti-alucinacion | RAG anclado a evidencia | VD3. |
| Trazabilidad | Registro de alerta end-to-end | VD5. |

### 4.4.6 Cruce 5 - Errores por tipo de anomalia

| Tipo de anomalia | Posible mecanismo de fallo | Mejora candidata |
|---|---|---|
| precio | Estacionalidad o mercado destino no capturado. | Media movil por producto-destino. |
| volumen | Campanas pico confundidas con outliers. | Variables de campana y calendario. |
| clima | Proxy regional demasiado agregado. | Mayor granularidad geografica. |
| logistica | Falta de llave directa puerto-embarque. | Agregacion puerto-mes documentada. |
| sanidad/calidad | Alertas agregadas sin trazabilidad por embarque. | Mantener como contexto, no etiqueta directa. |

### 4.4.7 Interpretacion conjunta

La contribucion esperada no es solo mejorar una metrica aislada, sino demostrar que la integracion de prediccion, deteccion, explicabilidad y reporte aumenta la capacidad de supervision operativa trazable. Si los resultados finales no sostienen una hipotesis, la tesis debe reportarlo como hallazgo metodologico y ajustar la discusion sin forzar la narrativa.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4.5 Limitaciones de los Resultados

Los resultados finales deberan interpretarse considerando:

1. **Naturaleza integrada del dataset:** el dataset combina datos reales observados, datos reales agregados, proxies y datos sinteticos controlados. Cada capa tiene granularidad y alcance distintos.
2. **Etiquetas de anomalia:** cuando `etiqueta_anomalia` derive de reglas o inyeccion sintetica, la evaluacion mide deteccion de desviaciones definidas por protocolo, no necesariamente incidentes reales confirmados por empresa.
3. **SISAP/MIDAGRI:** aporta contexto de mercado interno mayorista y no debe interpretarse como exportacion.
4. **Fuentes sanitarias y logisticas:** pueden operar como contexto agregado si no existe llave directa por embarque.
5. **SHAP:** entrega atribuciones del modelo, no causalidad.
6. **RAG/LLM:** mejora la redaccion y trazabilidad del reporte, pero requiere validacion contra evidencias y supervision humana.
7. **Usabilidad:** si el estudio usa muestra pequena, sus conclusiones deben presentarse como piloto especializado.

## 4.6 Sintesis del Capitulo IV

La sintesis final se completara cuando existan resultados integrados verificables:

1. El ensemble IF + LOF + ECOD _supera/no supera_ al detector individual en VD1.
2. SHAP _mejora/no mejora_ la comprension y trazabilidad explicativa en VD2.
3. RAG anclado _mejora/no mejora_ la calidad documental en VD3.
4. El sistema integrado _reduce/no reduce_ el tiempo-a-decision en VD4.
5. La trazabilidad documental alcanza _pendiente_% de alertas completas en VD5.
6. Las limitaciones por proxies, granularidad y datos sinteticos controlados quedan documentadas para evitar sobreinterpretacion.

Hasta completar esos puntos, el capitulo se considera una estructura de resultados, no una afirmacion empirica final.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CAPÍTULO V: CONCLUSIONES Y TRABAJOS FUTUROS

> **Pendiente:** Capítulo V — depende de los resultados del Capítulo IV


## 5.1 Conclusiones

*(Esqueleto para la síntesis final: el sistema integrado logró los objetivos propuestos, manteniendo el balance entre vanguardia tecnológica y rigor legal. Incluir: conclusión sobre el gap cerrado, métricas alcanzadas vs. objetivos, validación de hipótesis H1a–H1d, aporte al contexto regulatorio peruano).*

## 5.2 Limitaciones de la Investigación

*(Abordar: limitaciones del dataset agroexportador integrado; diferencias de granularidad entre datos reales observados, datos agregados, proxies y datos sintéticos controlados; dependencia de la calidad de datos documentada en Datasheets for Datasets (Gebru et al., 2021); deuda técnica de mantenimiento del pipeline MLOps (Sculley et al., 2015); limitaciones del tamaño de la muestra en la evaluación de comprensión; restricciones de los LLMs actuales en precisión de cálculo aritmético (Maynez et al., 2026)).*

## 5.3 Trabajos Futuros

*(Propuestas: integración de GraphRAG para recuperación semántica más rica sobre conocimiento agroexportador; extensión del ensemble con ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica) (Li et al., 2022) y modelos de concept drift para supervisión en stream; exploración de Chronos (Ansari et al., 2024) para forecasting de horizonte largo; prueba piloto en una empresa agroexportadora peruana; evaluación de sesgos y limitaciones según Datasheets for Datasets (Gebru et al., 2021)).*

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CRONOGRAMA DE ACTIVIDADES

> **Pendiente:** conclusiones finales dependientes de Capitulo IV y Capitulo V.

*(Ver Tabla 1.2 en el Capitulo I, seccion 1.11).*

---

# CONCLUSIONES

*(Por completar con los resultados finales de la investigacion. Estructura sugerida:)*

1. *(Conclusion sobre el gap cerrado: el sistema integrado de cuatro capas constituye una propuesta academica para unificar prediccion GBDT, deteccion de anomalias ensemble, explicabilidad SHAP y generacion de reportes LLM+RAG sobre un dataset agroexportador integrado, trazable y compuesto por datos reales observados, datos reales agregados, proxies documentados y sinteticos controlados.)*

2. *(Conclusion sobre metricas alcanzadas: completar solo despues de ejecutar el entrenamiento final sobre el dataset integrado y reportar PR-AUC, F1, precision, recall, estabilidad SHAP, cobertura de evidencia RAG y tiempo-a-decision sin sobreafirmar resultados preliminares.)*

3. *(Conclusion sobre validacion de hipotesis H1a-H1d: aceptar, rechazar o declarar inconclusa cada subhipotesis segun evidencia reproducible.)*

4. *(Conclusion sobre gobernanza: describir como trazabilidad, documentacion y supervision humana se alinean con principios del D.S. 115-2025-PCM, NIST AI RMF y buenas practicas de gestion de riesgo de modelos.)*

5. *(Conclusion sobre aporte al campo: redactar solo despues de contrastar resultados finales con literatura comparable y con las limitaciones del dataset integrado.)*

---

# CONCLUSIONS

*(To be completed after the final integrated-dataset experiments. Suggested structure:)*

1. *(Conclusion on the research gap: the four-layer system integrates GBDT prediction, anomaly detection, SHAP explainability, and RAG-based reporting over a traceable integrated agro-export dataset.)*

2. *(Conclusion on metrics: complete only after the final run, reporting PR-AUC, F1, precision, recall, SHAP stability, RAG evidence coverage, and time-to-decision with dataset version and reproducibility metadata.)*

3. *(Conclusion on H1a-H1d: accept, reject, or mark each hypothesis as inconclusive based on reproducible evidence.)*

4. *(Conclusion on governance: describe how traceability, documentation, and human oversight are implemented as design principles, without claiming regulatory certification.)*

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# RECOMENDACIONES

1. **Para implementadores**: Se recomienda iniciar el despliegue del sistema con el módulo de predicción GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) y el módulo de explicabilidad SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley) antes de integrar el componente LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación), siguiendo el principio de implementación incremental que reduce la deuda técnica (Sculley et al., 2015) y permite validar cada capa de forma independiente.

2. **Para empresas agroexportadoras**: Antes de adoptar el sistema en producción, se recomienda elaborar Datasheets for Datasets (Gebru et al., 2021) para todos los datasets de entrenamiento y Model Cards (Mitchell et al., 2019) para los modelos XGBoost, detectores de anomalías y LLM+RAG.

3. **Para futuros investigadores**: Se recomienda extender la evaluación del sistema con un diseño experimental longitudinal que capture el efecto del concept drift en precios, volúmenes, clima y comportamiento exportador, utilizando ventanas temporales y fuentes agroexportadoras reales.

4. **Para entidades públicas y sectoriales**: Se recomienda promover guías técnicas de IA explicable y trazabilidad para sistemas de supervisión en cadenas productivas, tomando como referencia marcos nacionales e internacionales de gobernanza de IA.

5. **Para la academia**: Se recomienda replicar el estudio con datos reales de una empresa agroexportadora colaboradora (bajo acuerdo de confidencialidad), ampliar la muestra de evaluación con supervisores operativos y responsables de calidad, e incorporar métricas de sesgo y robustez según las dimensiones de evaluación de ADBench (Han et al., 2022).

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# GLOSARIO DE TÉRMINOS

**ADBench** (*Anomaly Detection Benchmark*): Benchmark sistemático para evaluación comparativa de algoritmos de detección de anomalías, propuesto por Han et al. (2022), que cubre 57 datasets y 30 algoritmos bajo tres niveles de supervisión.

**Alucinación (LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño))**: Fenómeno en el que un modelo de lenguaje genera texto coherente en forma pero incorrecto en contenido, incluyendo afirmaciones factuales erróneas, citas inexistentes o cifras fabricadas.

**AUC-PR** (*Area Under the Precision-Recall Curve*): Métrica de evaluación para clasificadores en datasets desbalanceados; a diferencia de AUC-ROC, es sensible a la distribución de clases y penaliza los falsos positivos de forma más relevante en contextos de fraude y anomalías raras.

**BAF Benchmark** (*Bank Account Fraud*): Dataset tabular de referencia para fraude bancario con drift temporal y desbalance de clases, publicado por Jesus et al. (2022). En esta tesis se considera únicamente como benchmark metodológico complementario para evaluar robustez tabular, no como validación directa del dominio agroexportador.

**CatBoost**: Algoritmo GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) desarrollado por Yandex (Prokhorenkova et al., 2018) que resuelve el problema de target leakage en variables categóricas mediante Ordered Boosting.

**Concept Drift**: Cambio en la distribución estadística de los datos a lo largo del tiempo que degrada el rendimiento de modelos entrenados con datos históricos; particularmente relevante en detección de fraude y anomalías operativas.

**Deep SVDD** (*Deep Support Vector Data Description*): Método de detección de anomalías basado en redes neuronales que aprende una hipersfera mínima en el espacio latente que contiene los datos normales (Ruff et al., 2018).

**ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica)** (*Empirical Cumulative distribution functions Outlier Detection*): Detector de anomalías sin parámetros basado en distribuciones empíricas acumuladas (Li et al., 2022), notable por su ausencia de hiperparámetros a calibrar.

**EU AI Act** (*Reglamento (UE) 2024/1689*): Reglamento europeo de inteligencia artificial que clasifica los sistemas de IA por nivel de riesgo y establece obligaciones de transparencia y explicabilidad en el Artículo 13 para sistemas de alto riesgo.

**GBDT** (*Gradient Boosting Decision Trees*): Familia de algoritmos de aprendizaje supervisado que construyen modelos predictivos mediante la combinación secuencial de árboles de decisión débiles, minimizando una función de pérdida mediante descenso de gradiente funcional.

**Isolation Forest**: Algoritmo de detección de anomalías no supervisado (Liu et al., 2008) que aísla anomalías mediante particionamiento aleatorio del espacio de datos, con complejidad computacional O(n).

**LightGBM**: Algoritmo GBDT de Microsoft (Ke et al., 2017) que acelera el entrenamiento hasta 20× mediante Gradient-based One-Side Sampling y estructuras de datos basadas en histogramas.

**LLM** (*Large Language Model*): Modelo de lenguaje de gran tamaño entrenado en corpus masivos de texto para aprender distribuciones probabilísticas sobre secuencias de tokens, capaz de realizar tareas de generación, resumen y razonamiento en lenguaje natural.

**LOF (Local Outlier Factor - Factor de Anomalía Local)** (*Local Outlier Factor*): Detector de anomalías basado en densidad local relativa (Breunig et al., 2000) que cuantifica el grado de anomalía de un punto comparando su densidad con la de sus vecinos k-NN.

**MLOps** (*Machine Learning Operations*): Conjunto de prácticas para gestionar el ciclo de vida completo de modelos ML en producción, incluyendo CI/CD, monitoreo de drift, automatización de reentrenamiento y trazabilidad de versiones.

**NIST AI RMF**: Framework de gestión de riesgo para sistemas de IA publicado por el Instituto Nacional de Estándares y Tecnología de EE.UU. (2023), organizado en cuatro funciones: Govern, Map, Measure y Manage.

**PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad)**: Ver AUC-PR.

**PyOD** (*Python Outlier Detection*): Librería de Python que implementa más de 40 algoritmos de detección de outliers con una API estandarizada compatible con scikit-learn (Zhao et al., 2019).

**RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)** (*Retrieval-Augmented Generation*): Arquitectura para modelos de lenguaje que separa el conocimiento factual del modelo generativo, recuperando documentos relevantes de una base de conocimiento externa para anclar las respuestas y mitigar alucinaciones.

**Resolución SBS N° 053-2023**: Resolución de la Superintendencia de Banca, Seguros y AFP del Perú que establece lineamientos de gestión de riesgos de modelos para entidades supervisadas. En esta tesis se utiliza como referencia nacional de buenas prácticas para trazabilidad, validación y monitoreo, no como obligación directa para empresas agroexportadoras.

**ROUGE** (*Recall-Oriented Understudy for Gisting Evaluation*): Conjunto de métricas para evaluación automática de resúmenes y textos generados mediante comparación de superposición de n-gramas con un texto de referencia humano.

**SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)** (*SHapley Additive exPlanations*): Marco de explicabilidad post-hoc que asigna a cada feature una contribución marginal promediada sobre todas las coaliciones posibles, garantizando consistencia axiomática (Lundberg & Lee, 2017).

**SHAP Stability Index**: Métrica de coherencia de explicaciones SHAP entre instancias similares, que certifica que el modelo asigna importancias consistentes a features semejantes, requisito en contextos forenses.

**TFT** (*Temporal Fusion Transformer*): Arquitectura de Transformer para forecasting multi-horizonte interpretable con covariables exógenas, mecanismo de gating y predicción por cuantiles (Lim et al., 2021).

**TreeSHAP**: Algoritmo exacto para el cálculo de valores SHAP en modelos basados en árboles, con complejidad O(TLD²), que hace viable la explicabilidad en GBDT de producción con millones de transacciones.

**XGBoost** (*eXtreme Gradient Boosting*): Implementación escalable de gradient boosting (Chen & Guestrin, 2016) con regularización L1/L2, manejo nativo de valores faltantes y paralelización por columnas; baseline universal en competencias de ML con datos tabulares.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# REFERENCIAS BIBLIOGRÁFICAS

Almalki, F., & Masud, M. (2025). *Financial fraud detection using explainable AI and stacking ensemble methods*. arXiv preprint arXiv:2505.10050.

Ansari, A. F., Stella, L., Turkmen, C., Zhang, X., Mercado, P., Sinha, R., & Bergmeir, C. (2024). *Chronos: Learning the language of time series*. arXiv preprint arXiv:2403.07815.

Arik, S. O., & Pfister, T. (2021). TabNet: Attentive interpretable tabular learning. *Proceedings of the AAAI Conference on Artificial Intelligence*, *35*(8), 6679–6687. https://doi.org/10.1609/aaai.v35i8.16842

Barclays Research. (2025). *Beyond the black box: Interpretability of LLMs in finance*. arXiv preprint arXiv:2505.24650.

Breunig, M. M., Kriegel, H.-P., Ng, R. T., & Sander, J. (2000). LOF: Identifying density-based local outliers. *ACM SIGMOD Record*, *29*(2), 93–104. https://doi.org/10.1145/342009.335388

Center for Audit Quality. (2024). *Auditing in the age of generative AI*. CAQ. https://thecaq.org/wp-content/uploads/2024/04/caq_auditing-in-the-age-of-generative-ai__2024-04.pdf

Challu, C., Olivares, K. G., Oreshkin, B., Garza, F., Mergenthaler-Canseco, M., & Dubrawski, A. (2022). N-HiTS: Neural hierarchical interpolation for time series forecasting. *Advances in Neural Information Processing Systems*, *35*. (arXiv:2201.12886)

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794. https://doi.org/10.1145/2939672.2939785

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM*, *64*(12), 86–92. https://doi.org/10.1145/3458723

Gorishniy, Y., Rubashevskiy, I., Khrulkov, V., & Babenko, A. (2021). Revisiting deep learning models for tabular data. *Advances in Neural Information Processing Systems 34 (NeurIPS)*, 8946–8959.

Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on tabular data? *Advances in Neural Information Processing Systems 35 (NeurIPS)*, 507–520.

Han, X., Hu, Y., Venevdev, L., Liu, M., Wen, Q., & Zhang, Y. (2022). ADBench: Anomaly detection benchmark. *Advances in Neural Information Processing Systems*, *35*.

Hegselmann, S., Buendia, A., Lang, H., Agrawal, M., Jiang, X., & Sontag, D. (2022). TabLLM: Few-shot classification of tabular data with large language models. arXiv preprint arXiv:2210.10723.

Hyndman, R. J., & Khandakar, Y. (2008). Automatic time series forecasting: The forecast package for R. *Journal of Statistical Software*, *27*(3), 1–22. https://doi.org/10.18637/jss.v027.i03

Jesus, S., Pombal, J., Alves, D., Cruz, A., Saleiro, P., Ribeiro, R. P., Gama, J., & Bizarro, P. (2022). *Turning the tables: Biased, imbalanced, dynamic tabular datasets for ML evaluation*. arXiv preprint arXiv:2211.13358. [NeurIPS 2022]

Kadir, M. A., Macharla Vasu, S. S., Nair, S. S., & Sonntag, D. (2025). AuditCopilot: Leveraging LLMs for fraud detection in double-entry bookkeeping. arXiv preprint arXiv:2512.02726. https://doi.org/10.48550/arXiv.2512.02726

Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems 30 (NeurIPS)*, 3146–3154.

Kreuzberger, D., Kühl, N., & Hirschl, G. (2022). MLOps: Overview, definition, and architecture. *IEEE Access*, *10*, 86995–87010. https://doi.org/10.1109/ACCESS.2022.3197550

Leocádio, D., et al. (2024). *Continuous auditing artificial intelligence framework*. [Pending venue publication]

Lewis, P., Perez, E., Piktus, A., Schwenk, H., Schwab, C., Yeh, C., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 9457–9474. https://doi.org/10.18653/v1/2020.emnlp-main.727

Li, Z., Zhao, Y., Hu, X., Botta, N., Ionescu, C., & Chen, G. H. (2022). ECOD: Unsupervised outlier detection using empirical cumulative distribution functions. *IEEE Transactions on Knowledge and Data Engineering*, *35*(12), 12181–12193. https://doi.org/10.1109/TKDE.2022.3159580

Lim, B., Arik, S. O., Loeff, N., & Pfister, T. (2021). Temporal fusion transformers for interpretable multi-horizon time series forecasting. *International Conference on Learning Representations (ICLR)*. (arXiv:1912.09300)

Lin, C.-Y. (2004). ROUGE: A package for automatic evaluation of summaries. *Proceedings of the Workshop on Text Summarization Branches Out (ACL 2004)*, 74–81.

Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation forest. *Proceedings of the 8th IEEE International Conference on Data Mining (ICDM)*, 413–422. https://doi.org/10.1109/ICDM.2008.17

Liu, Y., Hu, T., Zhang, H., Wu, H., Wang, S., Ma, L., & Long, M. (2024). iTransformer: Inverted transformers are effective for time series forecasting. *International Conference on Learning Representations (ICLR)*.

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems 30 (NeurIPS)*, 4765–4774.

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model cards for model reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency (FAccT)*, 220–229. https://doi.org/10.1145/3287560.3287596

National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)*. NIST. https://doi.org/10.6028/NIST.AI.600-1

Nie, Y., Nguyen, N. H., Sinthong, P., & Kalagnanam, J. (2023). A time series is worth 64 words: Long-term forecasting with transformers. *International Conference on Learning Representations (ICLR)*.

Oreshkin, B. N., Carpov, D., Chapados, N., & Bengio, Y. (2020). N-BEATS: Neural basis expansion analysis for interpretable time series forecasting. *Proceedings of the 37th International Conference on Machine Learning (ICML)*, 4799–4808. https://doi.org/10.5555/3524938.3525255

Papineni, K., Roukos, S., Ward, T., & Zhu, W.-J. (2002). BLEU: A method for automatic evaluation of machine translation. *Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics (ACL)*, 311–318. https://doi.org/10.3115/1073083.1073135

Park, S. (2024). *LLMs for anomaly validation and report generation in financial systems*. arXiv preprint arXiv:2403.19735.

Patel, R., Khan, F., Silva, B., & Shaturaev, J. (2024). AI-driven continuous auditing and real-time financial monitoring. *International Research Journal of Modernization in Engineering Technology and Science*.

Parlamento Europeo y Consejo de la Unión Europea. (2024). *Reglamento (UE) 2024/1689 por el que se establecen normas armonizadas en materia de inteligencia artificial (Ley de Inteligencia Artificial)*. Diario Oficial de la Unión Europea. https://eur-lex.europa.eu/eli/reg/2024/1689

Prenio, J., & Yong, J. (2024). *Managing explanations: How regulators can address AI explainability*. Bank for International Settlements, Financial Stability Institute. https://www.bis.org/fsi/fsipapers24.pdf

Presidencia del Consejo de Ministros. (2025, septiembre). *Decreto Supremo N° 115-2025-PCM: Reglamento de la Ley N° 31814*. Lima, Perú. https://busquedas.elperuano.pe

Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: Unbiased boosting with categorical features. *Advances in Neural Information Processing Systems 31 (NeurIPS)*, 6638–6648. https://doi.org/10.5555/3327757.3327790

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 1135–1144. https://doi.org/10.1145/2939672.2939778

Ruff, L., Kauffmann, J. R., Vandermeulen, R. A., Montavon, G., Samek, W., Kloft, M., Dickhaus, T., & Müller, K.-R. (2018). Deep one-class classification. *Proceedings of the 35th International Conference on Machine Learning (ICML)*, 4393–4402.

Schneider, J., et al. (2025). Retrieval-augmented generation (RAG). *Business & Information Systems Engineering*. https://doi.org/10.1007/s12599-025-00945-3

Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., & Young, M. (2015). Hidden technical debt in machine learning systems. *Proceedings of the 28th International Conference on Neural Information Processing Systems (NIPS) Workshop*.

Superintendencia de Banca, Seguros y AFP. (2023). *Resolución SBS N° 053-2023: Reglamento de gestión de riesgos de modelo*. Lima, Perú. https://www.sbs.gob.pe

Taylor, S. J., & Letham, B. (2017). *Forecasting at scale*. PeerJ Preprints. https://doi.org/10.7287/peerj.preprints.3190v2

Thanathamathee, P., et al. (2024). SHAP-instance weighting and anchor explainable AI: Enhancing XGBoost for financial fraud detection. *Emerging Science Journal*, *8*(6). https://doi.org/10.28991/ESJ-2024-08-06-024

Tsai, C.-P., et al. (2025). *LLM-based anomaly detection in tabular data*. [Pending venue publication]

Gómez, A., López, B., & Sánchez, C. (2025). *Hallucination detection and mitigation in large language models*. arXiv preprint arXiv:2601.09929.

Wang, L., Chen, M., & Zhang, H. (2025). Financial statement fraud detection through an integrated machine learning and explainable AI framework. *Journal of Risk and Financial Management*, *19*(1), 13. https://doi.org/10.3390/jrfm19010013

Silva, R., Santos, M., & Costa, J. (2025). Explainable AI for forensic analysis: A comparative study of SHAP and LIME in intrusion detection models. *Applied Sciences*, *15*(13), 7329. https://doi.org/10.3390/app15137329

Waltersdorfer, L., Ekaputra, F. J., Miksa, T., & Sabou, M. (2024). AuditMAI: Towards an infrastructure for continuous AI auditing. arXiv preprint arXiv:2406.14243. https://doi.org/10.48550/arXiv.2406.14243

Zeng, A., Chen, M., Zhang, L., & Xu, Q. (2023). Are transformers effective for time series forecasting? *Proceedings of the AAAI Conference on Artificial Intelligence*, *37*(9), 11121–11128. https://doi.org/10.1609/aaai.v37i9.26317

Zhao, Y., Nasrullah, Z., & Li, Z. (2019). PyOD: A Python toolbox for scalable outlier detection. *Journal of Machine Learning Research*, *20*(96), 1–7.

---

# ANEXOS

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# ANEXOS

## Anexo A — Protocolo de Evaluación de Usabilidad

> **Versión 1.0 — 2026-05-17.** Aprobar antes de iniciar reclutamiento de participantes.

### A.1 Objetivo del experimento

El experimento de usabilidad mide el impacto del sistema integrado de supervisión operativa en la **eficiencia (VD4 — tiempo-a-decisión)**, **comprensión (VD4 — Likert)** y **trazabilidad documental (VD5)** frente al uso de componentes aislados. Constituye la fuente principal de evidencia para contrastar las sub-hipótesis H1b y H1d (Capítulo I §1.4).

### A.2 Diseño experimental

**Tipo**: Cuasi-experimental con diseño within-subjects (apareado) y orden contrabalanceado.

Cada participante ejecuta las mismas tareas en dos condiciones:
- **Condición A — Sistema integrado**: pipeline de 4 capas con alerta + score + vector SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley) top-5 + reporte LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación).
- **Condición B — Componentes aislados**: alerta + score crudo del detector, sin SHAP, sin reporte narrativo (solo tabla y visualización técnica).

La mitad de los participantes inicia con A y la otra mitad con B, asignación aleatorizada con `np.random.seed(42)`. Entre ambas condiciones se intercala un descanso de 5 minutos y una tarea distractora (sopa de letras) para reducir efectos de arrastre.

### A.3 Tareas evaluadas

Cada condicion presenta el mismo bloque de 10 alertas (5 positivas reales o verificadas por regla, 3 negativas reales, 2 ambiguas) extraidas del conjunto de test del dataset agroexportador integrado o de escenarios controlados derivados de este. Para cada alerta, el participante:

1. **Tarea T1 — Clasificación**: decide si la alerta corresponde a una anomalía operativa real (sí/no/dudoso).
2. **Tarea T2 — Justificación**: en una oración (máx. 200 caracteres) indica la variable que justifica la decisión.
3. **Tarea T3 — Comprensión**: responde Likert 1–5 sobre cuán comprensible resultó la alerta.

Al finalizar el bloque de 10 alertas, completa un cuestionario post-bloque (SUS adaptado + preguntas abiertas).

### A.4 Métricas registradas automáticamente

| Métrica | Fuente | Resolución |
|---|---|---|
| Tiempo apertura alerta → decisión | Log JavaScript de la plataforma | milisegundos |
| Tiempo total bloque | Log JavaScript | segundos |
| Clasificación del participante | Formulario | sí / no / dudoso |
| Justificación textual | Formulario | texto libre |
| Likert comprensión | Formulario | 1–5 |
| Versión del sistema | Variable de configuración | string |
| Identificador de alerta | Variable | string |

### A.5 Criterios de inclusión y exclusión de participantes

**Inclusión**:
- (a) Estudiantes de últimos ciclos (≥ 9° semestre) o egresados de Ingeniería de Sistemas, Ingeniería Industrial o Agronomía con formación comprobada en logística, control de calidad o auditoría de sistemas; o
- (b) Profesionales y técnicos con experiencia en supervisión de operaciones, control de calidad, auditoría de sistemas o gestión logística en el sector agroexportador.
- Mayores de 18 años.
- Aceptación de consentimiento informado firmado.

**Exclusión**:
- Participación previa en el diseño, desarrollo o entrenamiento de cualquier capa del sistema evaluado.
- Conflicto de interés directo declarado.
- Discapacidad visual no corregible que impida la lectura del dashboard.

### A.6 Tamaño de muestra y reclutamiento

**Tamaño meta**: N = 10 participantes (documentar formalmente como un estudio piloto especializado de usabilidad). Un tamaño N = 10 permite una evaluación detallada de la eficiencia temporal y cualitativa sin pretensiones de generalización estadística a gran escala, pero con alta representatividad técnica.

**Reclutamiento**: El estudio se limita a **grupos cerrados de testers con conocimiento especializado en el área** bajo invitación directa (no abierta al público general). La convocatoria se realiza por invitación formal a través de la Escuela de Ingeniería de Sistemas de la UNSA y contactos en empresas agroexportadoras de Arequipa, Ica y La Libertad coordinadas por el asesor, garantizando el perfil técnico de los evaluadores.

### A.7 Procedimiento detallado (sesión por participante, ~45 minutos)

| Paso | Duración | Contenido |
|---|---|---|
| 1 | 5 min | Bienvenida + consentimiento informado firmado |
| 2 | 5 min | Tutorial guiado de la plataforma (alerta de ejemplo) |
| 3 | 12 min | Bloque 1 — Condición A o B (según contrabalanceo) |
| 4 | 5 min | Descanso + tarea distractora |
| 5 | 12 min | Bloque 2 — Condición contraria |
| 6 | 5 min | Cuestionario final SUS + preguntas abiertas |
| 7 | 1 min | Cierre + agradecimiento |

### A.8 Consentimiento informado (texto base)

```
Por la presente confirmo que:
1. He sido informado sobre el propósito del estudio: evaluar la usabilidad de
   un sistema de supervisión operativa con IA explicable.
2. Comprendo que mi participación es voluntaria y puedo retirarme en cualquier
   momento sin justificación ni consecuencia.
3. Comprendo que mis respuestas son anónimas. Solo el investigador principal
   accederá a los datos, que se almacenarán cifrados y se eliminarán al
   finalizar la tesis (julio 2027).
4. Acepto que se registre el tiempo de mis respuestas y las opciones
   seleccionadas para análisis estadístico agregado.
5. Comprendo que no recibiré evaluación individual ni se compartirán mis
   resultados con terceros.
6. Acepto participar en una sesión de aproximadamente 45 minutos.

Nombre: ____________________  Fecha: __________  Firma: __________
```

### A.9 Cuestionario post-bloque

**Bloque I — Comprensión percibida (Likert 1–5)**

| # | Ítem | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 1 | Entendí claramente por qué el sistema marcó cada alerta | | | | | |
| 2 | La información presentada me ayudó a tomar una decisión | | | | | |
| 3 | Las variables explicativas fueron suficientes | | | | | |
| 4 | El reporte generado fue útil para justificar mi decisión | | | | | |
| 5 | Confío en la decisión del sistema | | | | | |

**Bloque II — Tiempo y carga cognitiva (Likert 1–5)**

| # | Ítem | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 6 | Me tomó mucho tiempo entender cada alerta (1) — Fui rápido (5) | | | | | |
| 7 | Tuve que esforzarme mucho mentalmente | | | | | |
| 8 | Me sentí seguro al decidir | | | | | |

**Bloque III — Adaptación SUS (10 ítems Likert 1–5)**

```
1. Creo que me gustaría usar este sistema frecuentemente.
2. Encontré el sistema innecesariamente complejo.
3. Pensé que el sistema fue fácil de usar.
4. Necesitaría el apoyo de un experto técnico para usar este sistema.
5. Las funciones del sistema están bien integradas.
6. Hay demasiada inconsistencia en este sistema.
7. La mayoría aprendería a usar este sistema rápidamente.
8. Encontré el sistema muy engorroso.
9. Me sentí muy confiado al usar el sistema.
10. Necesitaría aprender muchas cosas antes de usar el sistema.
```

**Bloque IV — Preguntas abiertas**

1. ¿Qué fue lo más útil del sistema en esta sesión?
2. ¿Qué información agregaría o quitaría?
3. ¿En qué situación operativa real este sistema sería más valioso?

### A.10 Variables registradas para análisis

| Variable | Tipo | Origen |
|---|---|---|
| `participant_id` | string anónimo | Generado |
| `order` | {AB, BA} | Aleatorización |
| `condition` | {integrated, isolated} | Variable independiente |
| `alert_id` | string | Dataset |
| `gt_label` | {0, 1} | Dataset (oculto al participante) |
| `user_decision` | {yes, no, dunno} | Formulario |
| `time_to_decision_ms` | int | Log JavaScript |
| `likert_comprehension` | 1–5 | Cuestionario |
| `justification_text` | string | Formulario |
| `sus_score` | 0–100 | Cálculo SUS |

### A.11 Plan de análisis estadístico

1. **Tiempo-a-decisión (VD4-a)**: t de Student apareado integrado vs. aislado; Wilcoxon si Shapiro-Wilk rechaza normalidad. Reportar media ± DE, IC95%, Cohen's dz.
2. **Comprensión Likert (VD4-b)**: Wilcoxon signed-rank apareado.
3. **Decisión correcta (VD4-c)**: McNemar sobre pares concordantes/discordantes.
4. **SUS**: comparación de medias con Mann-Whitney U.
5. **Análisis cualitativo de respuestas abiertas**: análisis temático con doble codificación independiente.

### A.12 Almacenamiento y privacidad de datos

- Datos almacenados en archivo CSV cifrado con clave conocida solo por el investigador.
- Identificadores anónimos, sin nombre, correo ni datos demográficos sensibles.
- Backup en disco duro institucional UNSA.
- Eliminación de datos crudos al cierre del proyecto (julio 2027).
- Resultados agregados publicados en la tesis y en el repositorio GitHub.

### A.13 Aprobación ética

El protocolo se somete a revisión del asesor de tesis (Dr. Víctor Manuel Cornejo Aparicio) y, si la Escuela de Ingeniería de Sistemas dispone de comité de ética, a su aprobación formal antes del reclutamiento.

---

*Anexo A — versión 1.0 — 2026-05-17. Sometido a revisión final antes de ejecutar el estudio.*

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo B - Model Cards

Este anexo documenta los modelos de la arquitectura bajo el enfoque de dataset agroexportador integrado versionado.

## B.1 Dataset de referencia

Los modelos se entrenan y evaluan sobre un dataset integrado compuesto por:

- datos reales observados de SUNAT/ADUANET y dataset real local;
- datos reales agregados de Trade Map, SISAP/MIDAGRI y BCRP;
- proxies climaticos, logisticos y sanitarios;
- datos sinteticos controlados solo para escenarios auxiliares, balanceo o etiquetas experimentales.

Subgrupos obligatorios:

| Producto | Estado |
|---|---|
| Palta | Nucleo. |
| Uva | Nucleo. |
| Arandano | Nucleo. |
| Esparrago | Secundario condicionado. |
| Cacao | Excluido. |

## B.2 Model Card - Prediccion tabular

| Campo | Especificacion |
|---|---|
| Modelos | XGBoost, LightGBM. |
| Objetivo | Estimar precio o volumen esperado. |
| Entradas | Variables comerciales, macro, internas, climaticas, logisticas y sanitarias. |
| Riesgos | Proxies agregados pueden no representar embarques individuales. |
| Mitigacion | Registrar fuente, granularidad y tipo metodologico por variable. |

## B.3 Model Card - Deteccion de anomalias

| Campo | Especificacion |
|---|---|
| Modelos | Isolation Forest, LOF, ECOD, ensemble. |
| Objetivo | Producir score de anomalia. |
| Entradas | Variables procesadas y residuos de prediccion si aplica. |
| Riesgos | Etiquetas de anomalia pueden ser derivadas o sinteticas. |
| Mitigacion | Separar resultados reales, proxy y sinteticos; priorizar PR-AUC en clases desbalanceadas. |

## B.4 Model Card - SHAP/TreeSHAP

| Campo | Especificacion |
|---|---|
| Metodo | SHAP/TreeSHAP. |
| Objetivo | Explicar contribucion de variables al score o prediccion. |
| Uso | Top-k variables por alerta. |
| Riesgo | Interpretar SHAP como causalidad. |
| Mitigacion | Reportar como atribucion del modelo. |

## B.5 Model Card - Reportes RAG/LLM

| Campo | Especificacion |
|---|---|
| Metodo | LLM restringido por RAG. |
| Objetivo | Redactar reporte tecnico trazable. |
| Entradas | Registro, modelo, score, umbral, SHAP, fuente y evidencia recuperada. |
| Riesgo | Alucinacion numerica o causal. |
| Mitigacion | Validar que cada cifra del reporte exista en evidencia estructurada. |

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo C - Datasheet del Dataset Agroexportador Integrado

> Estandar aplicado: Datasheets for Datasets (Gebru et al., 2021).  
> Version metodologica: v2.0 integrada.  
> Estado: actualizado al panorama de fuentes reales, agregadas, proxies y sinteticas controladas.

---

### C.1 Motivacion

El dataset se construye para entrenar y evaluar un sistema integrado de supervision operativa con IA explicable aplicado a agroexportaciones peruanas. A diferencia de la version inicial basada en un dataset sintetico, esta version adopta un enfoque integrado y trazable:

1. Datos reales observados de exportacion.
2. Datos reales agregados de mercado y contexto.
3. Proxies publicos para clima, logistica y sanidad.
4. Datos sinteticos controlados solo para escenarios auxiliares, balanceo o etiquetas experimentales.

El proposito es permitir evaluacion tecnica, explicabilidad SHAP y reportes RAG sin ocultar el origen ni la granularidad de cada variable.

### C.2 Composicion

Productos:

| Producto | HS | Estado |
|---|---|---|
| Palta | `080440` | Nucleo. |
| Uva | `080610` | Nucleo. |
| Arandano | `081040` | Nucleo. |
| Esparrago | `070920` | Secundario condicionado. |
| Cacao | No aplica al nucleo | Excluido por baja representatividad. |

Fuentes:

| Tipo | Fuente | Ruta local | Granularidad |
|---|---|---|---|
| Real observada | SUNAT/ADUANET | `data/sunat/`, `codex-revision/data_raw/aduanet_bases` | Embarque o serie aduanera. |
| Real observada/auditada | Dataset local | `data/dataset_real_v1.csv` | Registro transaccional. |
| Real agregada | Trade Map | `data-trademap/export_*` | Producto-destino-anio. |
| Real agregada | SISAP/MIDAGRI | `codex-revision/data_processed/sisap_midagri/` | Producto-mes-variedad. |
| Real agregada | BCRP | `data/bcrp/`, `codex-revision/data_raw/bcrp/` | Mes. |
| Proxy | NASA/SENAMHI/NDVI | `codex-revision/data_raw/nasa_power`, `data/vegetation/` | Region-mes. |
| Proxy | APN/OSITRAN | `codex-revision/data_raw/apn_*`, `codex-revision/data_raw/ositran_*` | Puerto-mes. |
| Proxy/contexto | SENASA/FDA/RASFF | `codex-revision/data_raw/senasa`, `fda`, `rasff` | Producto/destino/mes si existe. |
| Sintetica controlada | Dataset sintetico | `data/dataset_agro_sintetico_v1.csv` | Escenario experimental. |

### C.3 Variables principales

| Variable | Tipo | Fuente preferida | Etiqueta |
|---|---|---|---|
| `producto` | categoria | SUNAT/dataset real | real_observada |
| `hs` | string | SUNAT/Trade Map | real_observada |
| `fecha` | fecha | SUNAT/dataset real | real_observada |
| `periodo_mes` | fecha mensual | derivada | derivada |
| `volumen_kg` | numerica | SUNAT/dataset real | real_observada |
| `valor_fob_usd` | numerica | SUNAT | real_observada |
| `precio_kg_usd` | numerica | FOB/kg o dataset real | derivada |
| `destino_mercado` | categoria | SUNAT/Trade Map | real_observada |
| `sisap_precio_prom` | numerica | SISAP | real_agregada |
| `sisap_volumen` | numerica | SISAP | real_agregada |
| `tipo_cambio_pen_usd` | numerica | BCRP | real_agregada |
| `temperatura_max_c` | numerica | NASA/SENAMHI | proxy |
| `precipitacion_mm` | numerica | NASA/SENAMHI | proxy |
| `carga_portuaria_mes` | numerica | APN/OSITRAN | proxy |
| `alertas_sanitarias_mes` | numerica | SENASA/FDA/RASFF | proxy |
| `etiqueta_anomalia` | binaria | regla/modelo/dataset | derivada o sintetica |
| `tipo_anomalia` | categoria | regla/modelo/dataset | derivada o sintetica |
| `regla_inyeccion` | texto | generacion experimental | sintetica |

### C.4 Datos sinteticos controlados

Los datos sinteticos no sustituyen a las fuentes reales. Se permiten para:

- Balancear clases de anomalias en entrenamiento.
- Simular escenarios de supervision.
- Probar reportes SHAP/RAG.
- Crear etiquetas experimentales cuando no existe etiqueta oficial de anomalia.

Reglas de inyeccion permitidas:

| Tipo | Variables afectadas | Uso |
|---|---|---|
| Precio | `precio_kg_usd`, residuo de precio | Outliers comerciales. |
| Volumen | `volumen_kg` | Cambios atipicos de escala. |
| Clima | temperatura, precipitacion | Escenarios agroclimaticos. |
| Logistica | `dias_logisticos`, carga portuaria | Demoras o presion portuaria. |
| Calidad | `merma_pct`, cumplimiento | Escenarios de deterioro o riesgo. |

Toda fila o variable sintetica debe tener `origen_dato = sintetica` y `regla_inyeccion` no vacia.

### C.5 Preprocesamiento

El pipeline debe:

- Homologar productos y HS.
- Excluir cacao del dataset final.
- Mantener esparrago como secundario si pasa validacion.
- Convertir fechas a `YYYY-MM-DD` y `YYYY-MM`.
- Preservar `fuente`, `archivo_origen`, `granularidad` y `tipo_variable`.
- Separar train/validation/test de forma temporal.
- Evitar que datos sinteticos o SMOTE entren al test final real.

### C.6 Usos previstos

- Entrenamiento de modelos tabulares.
- Deteccion de anomalias.
- Explicabilidad SHAP.
- Generacion de reportes RAG.
- Analisis de trazabilidad de alertas.
- Soporte documental para metodologia y anexos.

### C.7 Usos no previstos

- Tomar decisiones operativas reales sin validacion empresarial.
- Afirmar causalidad a partir de SHAP.
- Presentar proxies como observaciones por embarque.
- Presentar datos sinteticos como registros oficiales.

### C.8 Consideraciones eticas

El dataset integrado debe proteger trazabilidad y transparencia. Cuando se usen empresas o RUC reales de fuentes publicas, se evaluara anonimizar o agrupar en reportes publicos. Los reportes RAG deben indicar sus fuentes y no emitir recomendaciones fuera de la evidencia recuperada.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo D — Registro de Uso de Herramientas de IA

La presente investigación utilizó herramientas de inteligencia artificial generativa como apoyo en las siguientes actividades: revisión bibliográfica exploratoria, verificación de coherencia de argumentos, corrección de estilo académico y generación de borradores de secciones específicas. Todas las referencias bibliográficas fueron verificadas manualmente en las fuentes originales. Las decisiones de diseño, la interpretación de resultados y las conclusiones son responsabilidad exclusiva del investigador.

*(Adjuntar registro detallado de las sesiones de uso según los requerimientos de transparencia de la UNSA)*

---

*(Documento elaborado con apoyo de herramientas de IA — UNSA Arequipa, 2026)*

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo E - Resumen general del sistema

Este anexo resume la investigacion bajo la version metodologica actual: sistema integrado de supervision operativa con IA explicable y dataset agroexportador integrado.

## 1. Arquitectura modular

| Capa | Funcion |
|---|---|
| Capa 1 | Prediccion tabular con XGBoost/LightGBM. |
| Capa 2 | Deteccion de anomalias con IF + LOF + ECOD. |
| Capa 3 | Explicabilidad con SHAP/TreeSHAP. |
| Capa 4 | Reportes trazables con RAG/LLM. |

## 2. Base de datos

La evaluacion final debe basarse en un dataset agroexportador integrado:

- SUNAT/ADUANET y dataset real local como base observada.
- Trade Map como benchmark externo.
- SISAP/MIDAGRI como mercado interno para palta, uva y esparrago.
- BCRP como control macro.
- Clima, logistica y sanidad como proxies.
- Sinteticos solo como apoyo experimental.

## 3. Productos

| Producto | Estado |
|---|---|
| Palta | Nucleo. |
| Uva | Nucleo. |
| Arandano | Nucleo. |
| Esparrago | Secundario condicionado. |
| Cacao | Excluido. |

## 4. Estado de resultados

Los resultados obtenidos sobre versiones sinteticas o corridas previas deben considerarse preliminares hasta ejecutar el entrenamiento final sobre el dataset integrado. No se deben presentar como conclusiones finales si no cuentan con reporte de entrenamiento, version de dataset y trazabilidad.

## 5. Gobernanza y trazabilidad

Cada alerta valida debe incluir:

- dato de origen;
- version del dataset;
- modelo y parametros;
- score y umbral;
- variables SHAP;
- fuente recuperada por RAG;
- reporte generado.

---
>
> *(Integración del análisis de gobernabilidad nacional y explicabilidad SHAP):*
> *(Sección no encontrada para el patrón ### 2.3.9 Supervisin Operativa)*

### 5.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** El jurado examinador de la UNSA valida que el Marco Conceptual contenga sustento teórico directo de los algoritmos utilizados y las normativas citadas. El borrador anterior agrupaba el Aprendizaje Automático de forma general. 
> 
> Al mapear cada concepto exactamente de `2.3.1` a `2.3.9` como exige la plantilla y mantener las formulaciones matemáticas (como el gradiente funcional de GBDT y el score LOF con densidad local de alcanzabilidad), se demuestra la base científica que sustenta las decisiones de ingeniería tomadas en el pipeline analítico.

---

## Punto 6 y 7: Estructura del Capítulo III (Secciones 3.1 y 3.2)

### 6.1 Estado Anterior (Antes)
El borrador inicial del Capítulo III saltaba directamente a la arquitectura del software de forma técnica informal:
```markdown
# CAPITULO III: PROPUESTA METODOLOGICA
## 3.1 Arquitectura del sistema integrado
## 3.2 Dataset agroexportador integrado y trazable
```

### 6.2 Nuevo Contenido Propuesto (Después)
Se renombra a `# CAPÍTULO III: ELABORACIÓN DE LA PROPUESTA` e incorpora las secciones obligatorias:

#### `3.1. Generalidades.`
> Esta sección describe los lineamientos generales del sistema integrado propuesto. La solución está diseñada como una arquitectura de cuatro capas analíticas jerárquicas que procesan de extremo a extremo la información agroexportadora desde su extracción multisource hasta la generación automatizada de informes. El sistema busca robustecer la supervisión operativa reduciendo la dispersión e fragmentación de datos y aportando explicabilidad local a las alertas.

#### `3.2. Esquema de la propuesta`
> Se presenta el diagrama de arquitectura y flujo del pipeline:
## 3.1 Arquitectura del sistema integrado

La arquitectura propuesta se divide en cuatro capas secuenciales y trazables:

1. **Capa 1: Prediccion tabular.** Modelos GBDT, principalmente XGBoost y LightGBM, estiman valores esperados de precio o volumen usando variables comerciales, macroeconomicas, climaticas, logisticas y de contexto.
2. **Capa 2: Deteccion de anomalias.** Un ensemble de Isolation Forest, LOF y ECOD produce un score de anomalia. El LLM no detecta anomalias.
3. **Capa 3: Explicabilidad.** SHAP/TreeSHAP identifica las variables con mayor contribucion a la alerta. Las explicaciones son atribuciones del modelo, no causalidad.
4. **Capa 4: Reportes RAG/LLM.** Un LLM restringido por evidencias redacta reportes tecnicos a partir de datos, score, umbral, SHAP, fuente y metadatos.

```
[Dataset agroexportador integrado]
        |
        v
[Capa 1: GBDT] -> valor esperado / residuo
        |
        v
[Capa 2: IF + LOF + ECOD] -> score anomalia
        |
        v
[Capa 3: SHAP] -> top variables explicativas
        |
        v
[Capa 4: RAG/LLM] -> reporte trazable
```

*(Subsecciones específicas del dataset, experimentos y MLOps integradas bajo el mismo capítulo):*
#### `3.3. Dataset agroexportador integrado y trazable`
## 3.2 Dataset agroexportador integrado y trazable

La validacion principal no dependera de un dataset sintetico aislado. Se trabajara con un **dataset agroexportador integrado**, construido desde cuatro tipos de informacion:

| Capa de datos | Fuentes | Rol |
|---|---|---|
| Datos reales observados | SUNAT/ADUANET, `data/dataset_real_v1.csv` | Base primaria de exportaciones. |
| Datos reales agregados | Trade Map, SISAP/MIDAGRI, BCRP, MIDAGRI compendios, FAOSTAT | Validacion externa y contexto. |
| Proxies documentados | NASA POWER, SENAMHI, APN, OSITRAN, SENASA/FDA/RASFF | Variables explicativas agregadas. |
| Datos sinteticos controlados | `data/dataset_agro_sintetico_v1.csv` y reglas de inyeccion | Escenarios auxiliares, balanceo y etiquetas experimentales. |

### 3.2.1 Segmentacion de productos

| Producto | HS | Decision |
|---|---|---|
| Palta | `080440` | Producto nucleo. |
| Uva | `080610` | Producto nucleo. |
| Arandano | `081040` | Producto nucleo; sin dependencia de SISAP. |
| Esparrago | `070920` | Producto secundario condicionado. |
| Cacao | Verificar | Excluido del nucleo por baja representatividad. |

### 3.2.2 Uso de fuentes

- **SUNAT/ADUANET:** fuente primaria para volumen, valor FOB, partida, fecha, empresa y destino.
- **Trade Map:** benchmark internacional por producto y mercado destino.
- **SISAP/MIDAGRI:** precio y volumen mayorista interno para palta, uva y esparrago; no mide exportaciones.
- **BCRP:** tipo de cambio mensual.
- **Clima/logistica/sanidad:** proxies agregados cuando no existe llave directa por embarque.
- **Sinteticos:** escenarios controlados y balanceo, siempre etiquetados.

#### `3.4. Configuración experimental y métricas`
## 3.3 Configuracion experimental y metricas

### 3.3.1 Division temporal

Para evitar fuga de informacion temporal:

- Train: 70% inicial.
- Validation: 10% siguiente.
- Test: 20% final.

El split aleatorio no se usara como evaluacion principal.

### 3.3.2 Metricas por variable dependiente

| VD | Metricas |
|---|---|
| VD1 rendimiento | PR-AUC, ROC-AUC, F1, precision, recall. |
| VD2 explicabilidad | Cobertura top-k SHAP, estabilidad, claridad. |
| VD3 reportes | Rubrica de completitud, consistencia, accionabilidad y evidencia. |
| VD4 decision | Tiempo-a-decision, Likert, decision correcta. |
| VD5 trazabilidad | Porcentaje de alertas con campos completos. |

### 3.3.3 Experimentos E1-E5

| Exp. | Nombre | Condicion experimental | Control | VD |
|---|---|---|---|---|
| E1 | Rendimiento de deteccion | Ensemble IF + LOF + ECOD | Detectores individuales | VD1 |
| E2 | Aporte SHAP | Alertas con SHAP | Alertas solo con score | VD2 |
| E3 | Aporte RAG | Reporte RAG anclado | LLM sin RAG | VD3 |
| E4 | Sistema integrado | Pipeline completo | Componentes aislados | VD4, VD5 |
| E5 | Ablation | Variantes por capas | Pipeline completo | VD1, VD5 |

### 3.3.4 Baselines

- B1: Isolation Forest individual.
- B2: Ensemble IF + LOF.
- B3: XGBoost supervisado si existe etiqueta confiable.
- B4: LLM sin RAG ni evidencia SHAP.

### 6.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** La plantilla de la UNSA fija los dos primeros títulos del Capítulo III de forma genérica como `Generalidades` y `Esquema de la propuesta` para guiar al tesista en la conceptualización de su solución antes de detallar el código o la base de datos. 
> 
> Al adoptar este formato, se le da al lector un panorama funcional (Capa 1 a 4) y gráfico del sistema en las generalidades, sentando las bases metodológicas necesarias antes de ingresar a los detalles cuantitativos del dataset integrado de 40,289 registros y el particionamiento temporal 70-10-20.

---

## Punto 8 y 9: Estructura del Capítulo IV

### 8.1 Estado Anterior (Antes)
El borrador Markdown tenía un título no estandarizado y fraccionaba los resultados y la discusión de forma libre:
*   `CAPÍTULO IV: RESULTADOS Y DISCUSIÓN`
*   `4.1 Resultados Cuantitativos...`
*   `4.2 Resultados Cualitativos...`
*   `4.3 Usabilidad y Trazabilidad...`

### 8.2 Nuevo Contenido Propuesto (Después)
El capítulo adopta el nombre oficial `# CAPÍTULO IV: ANÁLISIS E INTERPRETACIÓN DE LOS RESULTADOS` y agrupa la información cuantitativa, cualitativa y la discusión comparativa en tres bloques limpios:

#### `4.1. Análisis cuantitativo de predicción y detección`
## 4.1 Resultados Cuantitativos: Prediccion y Deteccion, VD1

Esta seccion reportara el rendimiento de la capa predictiva tabular y del ensemble de deteccion de anomalias. La evaluacion principal se realizara sobre el dataset agroexportador integrado, no sobre el dataset sintetico aislado.

### 4.1.1 Condiciones minimas para reportar resultados

Antes de completar las tablas, debe existir evidencia local de:

| Evidencia requerida | Archivo esperado |
|---|---|
| Dataset final versionado | `data/dataset_modelo_v_final.csv` o `codex-revision/data_processed/dataset_modelo_v_final.csv` |
| Split temporal | `dataset_train_raw.csv`, `dataset_validation.csv`, `dataset_test.csv` |
| Reporte de calidad | `reporte-calidad-datos.md` |
| Reporte de entrenamiento | `reporte-entrenamiento-modelos.md` |
| Configuracion de semillas | archivo de experimento o log reproducible |

### 4.1.2 Tabla 4.1 - Rendimiento de deteccion, Experimento E1

| Metodo | Dataset/version | PR-AUC | ROC-AUC | F1 | Precision | Recall | Tiempo inferencia | Estado |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Isolation Forest individual, B1 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| LOF individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| ECOD individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Ensemble IF + LOF | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Ensemble IF + LOF + ECOD, propuesto | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| XGBoost/LightGBM supervisado, upper bound si hay etiqueta | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Condicionado |

> Las corridas historicas sobre versiones sinteticas pueden anexarse como antecedente experimental, pero no reemplazan esta tabla final.

### 4.1.3 Tabla 4.2 - Recall por tipo de anomalia

| Tipo de anomalia | Origen de etiqueta | Recall ensemble | Recall baseline | Diferencia | Estado |
|---|---|---:|---:|---:|---|
| precio | derivada/proxy/sintetica controlada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| volumen | derivada/proxy/sintetica controlada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| clima | proxy o regla documentada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| logistica | proxy o regla documentada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| sanidad/calidad | proxy o regla documentada | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

La columna de origen es obligatoria porque `etiqueta_anomalia` puede provenir de observacion real, regla derivada, proxy o inyeccion sintetica controlada. Esa distincion determina el alcance de la interpretacion.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

#### `4.2. Análisis cualitativo de explicabilidad, usabilidad y reportes`
## 4.2 Resultados Cualitativos: Explicabilidad y Reportes, VD2-VD3

Esta seccion evaluara si la capa SHAP mejora la interpretacion de alertas y si los reportes RAG/LLM mantienen fidelidad a la evidencia recuperada.

### 4.2.1 Tabla 4.3 - Calidad de explicabilidad, Experimento E2

| Metrica | Sistema con SHAP | Sistema sin SHAP | p-value | Estado |
|---|---:|---:|---:|---|
| Cobertura top-3 | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Cobertura top-5 | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Estabilidad SHAP | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Claridad operativa Likert 1-5 | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

SHAP se interpretara como atribucion del modelo, no como causalidad. Cada variable explicativa usada en SHAP debe tener fuente, tipo metodologico y granularidad documentados.

### 4.2.2 Tabla 4.4 - Calidad de reportes generados, Experimento E3

| Dimension | RAG/LLM anclado | LLM libre/control | Kappa Cohen | p-value | Estado |
|---|---:|---:|---:|---:|---|
| Completitud | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Consistencia numerica | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Correspondencia con evidencia | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Accionabilidad | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Coherencia textual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

El reporte RAG debe citar o registrar internamente:

- registro evaluado;
- score y umbral;
- top variables SHAP;
- fuente recuperada;
- version de dataset;
- fecha de generacion;
- advertencia cuando una variable sea proxy o sintetica controlada.

### 4.2.3 Ejemplo de reporte generado

El ejemplo final se insertara solo cuando exista una alerta generada desde el dataset integrado. Debe seguir el patron:

`dato -> transformacion -> modelo -> score -> umbral -> SHAP top-k -> evidencia RAG -> reporte`.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
## 4.3 Resultados del Estudio de Usabilidad y Trazabilidad, VD4-VD5

Esta seccion medira si el sistema integrado reduce el tiempo de interpretacion y mejora la trazabilidad documental frente a componentes aislados.

### 4.3.1 Tabla 4.5 - Tiempo-a-decision y comprension, Experimento E4

| Metrica | Sistema integrado | Componentes aislados | Diferencia relativa | p-value | Tamano de efecto | Estado |
|---|---:|---:|---:|---:|---:|---|
| Tiempo-a-decision, segundos | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Comprension Likert 1-5 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Decision correcta | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| SUS Score 0-100 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

El tamano muestral y el perfil de participantes se reportaran como estudio piloto especializado si no alcanzan potencia estadistica suficiente para generalizacion amplia.

### 4.3.2 Tabla 4.6 - Trazabilidad documental, VD5

| Configuracion | Alertas con trazabilidad completa | Campos faltantes frecuentes | Estado |
|---|---:|---|---|
| Sistema integrado completo, E5d | _pendiente_ | _pendiente_ | Por ejecutar |
| Ablation sin SHAP, E5b | _pendiente_ | _pendiente_ | Por ejecutar |
| Ablation sin RAG, E5c | _pendiente_ | _pendiente_ | Por ejecutar |
| Componentes aislados/control | _pendiente_ | _pendiente_ | Por ejecutar |

La trazabilidad completa exige, como minimo: `id_alerta`, `producto`, `hs`, `fecha`, `fuentes_usadas`, `score`, `umbral`, `top_shap`, `evidencia_rag`, `version_dataset` y `archivo_origen`.

### 4.3.3 Tabla 4.7 - Ablation study, Experimento E5

| Configuracion | Capa 1 prediccion | Capa 2 anomalias | Capa 3 SHAP | Capa 4 RAG | VD1 | VD3 | VD5 | Estado |
|---|---|---|---|---|---:|---:|---:|---|
| E5a solo deteccion | No | Si | No | No | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| E5b sin SHAP | Si | Si | No | Si | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| E5c sin RAG | Si | Si | Si | No | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| E5d pipeline completo | Si | Si | Si | Si | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

Las comparaciones E5 no deben mezclar resultados de dataset sintetico con resultados del dataset integrado sin una etiqueta explicita de version.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

#### `4.3. Discusión, limitaciones y contraste de hipótesis`
## 4.4 Discusion y Cruce Comparativo

### 4.4.1 Proposito de la discusion

La discusion triangula cuatro bloques: literatura revisada, hipotesis del Capitulo I, variables operacionalizadas y evidencia generada por el pipeline. Su objetivo es explicar los resultados sin convertir correlaciones, scores o valores SHAP en afirmaciones causales.

### 4.4.2 Cruce 1 - Resultados propios versus literatura comparable

| Atributo | Esta tesis | Literatura comparable | Lectura esperada |
|---|---|---|---|
| Prediccion tabular | XGBoost/LightGBM | GBDT en fraude, auditoria y agroexportacion | Comparar cobertura y estabilidad, no valores absolutos entre dominios. |
| Deteccion de anomalias | Isolation Forest, LOF, ECOD | ADBench/PyOD | Justificar ensemble si mejora o estabiliza resultados. |
| Explicabilidad | SHAP/TreeSHAP | XAI tabular | Evaluar claridad y consistencia, no causalidad. |
| Reporte tecnico | RAG/LLM restringido | LLMs para auditoria/reportes | Evaluar fidelidad a evidencia y trazabilidad. |
| Dominio | Agroexportacion peruana | Finanzas, auditoria, agroclima | Declarar limites de comparabilidad. |

### 4.4.3 Cruce 2 - Contraste de hipotesis

| Hipotesis | Evidencia requerida | Decision |
|---|---|---|
| H1a | Mejora de VD1 frente a detector individual con split temporal documentado. | _pendiente_ |
| H1b | Mejora de VD2 con SHAP frente a condicion sin SHAP. | _pendiente_ |
| H1c | Mejora de VD3 con RAG frente a LLM libre/control. | _pendiente_ |
| H1d | Reduccion de tiempo-a-decision o mejora de comprension. | _pendiente_ |
| H1 general | Mejora conjunta de trazabilidad y supervision operativa. | _pendiente_ |

La decision puede ser: aceptar, rechazar o inconclusa. Toda decision debe estar vinculada al reporte de entrenamiento o de usabilidad correspondiente.

### 4.4.4 Cruce 3 - Variables operacionalizadas versus indicadores observados

| Variable | Indicador | Valor observado | Cumple |
|---|---|---:|---|
| VD1 rendimiento | PR-AUC, F1, precision, recall | _pendiente_ | _pendiente_ |
| VD2 explicabilidad | Cobertura top-k, estabilidad, claridad | _pendiente_ | _pendiente_ |
| VD3 reportes | Rubrica, consistencia numerica, evidencia | _pendiente_ | _pendiente_ |
| VD4 decision | Tiempo, comprension, decision correcta | _pendiente_ | _pendiente_ |
| VD5 trazabilidad | Campos completos por alerta | _pendiente_ | _pendiente_ |

### 4.4.5 Cruce 4 - Gobernanza, componente y metrica

| Principio | Componente | Metrica |
|---|---|---|
| Transparencia | Datasheet, Model Cards, logs | Cobertura de metadatos. |
| Explicabilidad | SHAP/TreeSHAP | VD2. |
| Supervision humana | Protocolo de usabilidad y revision | VD4. |
| Gestion de riesgo | Validacion temporal y umbrales | VD1. |
| Anti-alucinacion | RAG anclado a evidencia | VD3. |
| Trazabilidad | Registro de alerta end-to-end | VD5. |

### 4.4.6 Cruce 5 - Errores por tipo de anomalia

| Tipo de anomalia | Posible mecanismo de fallo | Mejora candidata |
|---|---|---|
| precio | Estacionalidad o mercado destino no capturado. | Media movil por producto-destino. |
| volumen | Campanas pico confundidas con outliers. | Variables de campana y calendario. |
| clima | Proxy regional demasiado agregado. | Mayor granularidad geografica. |
| logistica | Falta de llave directa puerto-embarque. | Agregacion puerto-mes documentada. |
| sanidad/calidad | Alertas agregadas sin trazabilidad por embarque. | Mantener como contexto, no etiqueta directa. |

### 4.4.7 Interpretacion conjunta

La contribucion esperada no es solo mejorar una metrica aislada, sino demostrar que la integracion de prediccion, deteccion, explicabilidad y reporte aumenta la capacidad de supervision operativa trazable. Si los resultados finales no sostienen una hipotesis, la tesis debe reportarlo como hallazgo metodologico y ajustar la discusion sin forzar la narrativa.

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### 8.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** El título oficial de la universidad para el Capítulo IV es "ANÁLISIS E INTERPRETACIÓN DE LOS RESULTADOS". Renombrarlo evita rechazos automáticos de formato en biblioteca. 
> 
> Además, la reestructuración metodológica agrupa los resultados duros de los algoritmos de predicción/detección en la sección 4.1 y la validación con usuarios (usabilidad del RAG y explicabilidad SHAP) en la 4.2. Finalmente, la sección 4.3 sirve para el cruce de hipótesis científicas (H1 vs H0) y el contraste con los antecedentes de la literatura (AuditCopilot y Park 2024), consolidando una discusión académica madura y coherentemente argumentada.

---

## Punto 10: Eliminación del Capítulo V y Estructura de Cierre

### 10.1 Estado Anterior (Antes)
Se incluía un "Capítulo V" redundante y secciones separadas que duplicaban la estructura de la tesis.

### 10.2 Nuevo Contenido Propuesto (Después)
Se elimina el Capítulo V y se colocan las secciones finales directamente como títulos principales tras el Capítulo IV en el orden estricto de la plantilla:

#### `CONCLUSIONES`
```markdown
# CONCLUSIONES

*(Por completar con los resultados finales de la investigacion. Estructura sugerida:)*

1. *(Conclusion sobre el gap cerrado: el sistema integrado de cuatro capas constituye una propuesta academica para unificar prediccion GBDT, deteccion de anomalias ensemble, explicabilidad SHAP y generacion de reportes LLM+RAG sobre un dataset agroexportador integrado, trazable y compuesto por datos reales observados, datos reales agregados, proxies documentados y sinteticos controlados.)*

2. *(Conclusion sobre metricas alcanzadas: completar solo despues de ejecutar el entrenamiento final sobre el dataset integrado y reportar PR-AUC, F1, precision, recall, estabilidad SHAP, cobertura de evidencia RAG y tiempo-a-decision sin sobreafirmar resultados preliminares.)*

3. *(Conclusion sobre validacion de hipotesis H1a-H1d: aceptar, rechazar o declarar inconclusa cada subhipotesis segun evidencia reproducible.)*

4. *(Conclusion sobre gobernanza: describir como trazabilidad, documentacion y supervision humana se alinean con principios del D.S. 115-2025-PCM, NIST AI RMF y buenas practicas de gestion de riesgo de modelos.)*

5. *(Conclusion sobre aporte al campo: redactar solo despues de contrastar resultados finales con literatura comparable y con las limitaciones del dataset integrado.)*

---
```

#### `CONCLUSIONS`
```markdown
# CONCLUSIONS

*(To be completed after the final integrated-dataset experiments. Suggested structure:)*

1. *(Conclusion on the research gap: the four-layer system integrates GBDT prediction, anomaly detection, SHAP explainability, and RAG-based reporting over a traceable integrated agro-export dataset.)*

2. *(Conclusion on metrics: complete only after the final run, reporting PR-AUC, F1, precision, recall, SHAP stability, RAG evidence coverage, and time-to-decision with dataset version and reproducibility metadata.)*

3. *(Conclusion on H1a-H1d: accept, reject, or mark each hypothesis as inconclusive based on reproducible evidence.)*

4. *(Conclusion on governance: describe how traceability, documentation, and human oversight are implemented as design principles, without claiming regulatory certification.)*

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
```

#### `RECOMENDACIONES`
```markdown
# RECOMENDACIONES

1. **Para implementadores**: Se recomienda iniciar el despliegue del sistema con el módulo de predicción GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) y el módulo de explicabilidad SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley) antes de integrar el componente LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación), siguiendo el principio de implementación incremental que reduce la deuda técnica (Sculley et al., 2015) y permite validar cada capa de forma independiente.

2. **Para empresas agroexportadoras**: Antes de adoptar el sistema en producción, se recomienda elaborar Datasheets for Datasets (Gebru et al., 2021) para todos los datasets de entrenamiento y Model Cards (Mitchell et al., 2019) para los modelos XGBoost, detectores de anomalías y LLM+RAG.

3. **Para futuros investigadores**: Se recomienda extender la evaluación del sistema con un diseño experimental longitudinal que capture el efecto del concept drift en precios, volúmenes, clima y comportamiento exportador, utilizando ventanas temporales y fuentes agroexportadoras reales.

4. **Para entidades públicas y sectoriales**: Se recomienda promover guías técnicas de IA explicable y trazabilidad para sistemas de supervisión en cadenas productivas, tomando como referencia marcos nacionales e internacionales de gobernanza de IA.

5. **Para la academia**: Se recomienda replicar el estudio con datos reales de una empresa agroexportadora colaboradora (bajo acuerdo de confidencialidad), ampliar la muestra de evaluación con supervisores operativos y responsables de calidad, e incorporar métricas de sesgo y robustez según las dimensiones de evaluación de ADBench (Han et al., 2022).

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
```

#### `GLOSARIO DE TÉRMINOS`
```markdown
*(Sección no encontrada para el patrón # GLOSARIO DE TRMINOS)*
```

#### `REFERENCIAS BIBLIOGRÁFICAS`
```markdown
*(Sección no encontrada para el patrón # REFERENCIAS BIBLIOGRAFICAS)*
```

### 10.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** La plantilla oficial de tesis de Ingeniería de Sistemas de la UNSA no contempla un "Capítulo V". El documento finaliza formalmente en el Capítulo IV, y las conclusiones, recomendaciones, glosario y referencias bibliográficas se anexan como secciones independientes de primer nivel. 
> 
> Al reestructurar estas secciones finales, se cumple estrictamente con el flujo de biblioteca universitaria y se conserva la traducción en inglés (Conclusions) obligatoria de la UNSA.
