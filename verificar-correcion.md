# CAMBIOS EN EL CAPÍTULO II

## Reemplazar la introducción de 2.1

La revisión de antecedentes se organiza en función de los componentes metodológicos de la investigación: predicción sobre datos tabulares, detección de anomalías, explicabilidad y generación de reportes asistida por modelos de lenguaje. Debido a que existe una cantidad limitada de trabajos que integran estos componentes dentro del contexto agroexportador peruano, se consideran investigaciones procedentes de dominios empresariales, financieros y de auditoría únicamente como soporte metodológico transferible.

La revisión diferencia entre el dominio de aplicación de los trabajos y su contribución técnica. Por tanto, los resultados obtenidos en entornos financieros no se interpretan como evidencia directa sobre operaciones agroexportadoras, sino como antecedentes para seleccionar algoritmos, mecanismos de explicación y estrategias de generación de reportes.

---

## Reemplazar 2.1.1 Kadir et al.

### 2.1.1 Kadir et al. (2025)

Kadir et al. (2025), en el trabajo *AuditCopilot: Leveraging LLMs for Fraud Detection in Double-Entry Bookkeeping*, evaluaron modelos de lenguaje para detectar irregularidades en registros contables de partida doble. Los autores compararon los modelos de lenguaje con pruebas contables basadas en reglas y con modelos clásicos de aprendizaje automático, utilizando datos sintéticos y registros anonimizados.

El antecedente demuestra que los modelos de lenguaje pueden participar en procesos de análisis e interpretación de registros estructurados. Sin embargo, su función dentro de la presente tesis será diferente. El modelo de lenguaje no será empleado como detector principal, sino como componente de redacción subordinado a predicciones, scores, explicaciones y evidencias previamente calculadas.

---

## Mantener 2.1.2 Park, pero reemplazar el último párrafo

Este trabajo aporta una referencia metodológica sobre el uso de agentes especializados para validar e interpretar anomalías previamente identificadas. No obstante, el modelo propuesto en esta tesis no utilizará una arquitectura multiagente como mecanismo de detección. El LLM estará restringido a la generación de reportes sobre información estructurada y recuperada, manteniendo separados los procesos de detección, explicación y redacción.

---

## Reemplazar completamente “Mongolia et al. (2025)”

### 2.1.3 Sodnomdavaa y Lkhagvadorj

Sodnomdavaa y Lkhagvadorj desarrollaron un marco de detección de fraude en estados financieros que integra aprendizaje automático y técnicas de inteligencia artificial explicable. El trabajo emplea modelos de clasificación y mecanismos de explicación para identificar variables asociadas con las predicciones realizadas.

Este antecedente es relevante porque respalda el uso conjunto de modelos tabulares y explicabilidad en escenarios donde los resultados necesitan ser revisados. Sin embargo, su dominio, variables, objetivo y etiquetas corresponden a fraude financiero supervisado, por lo que sus resultados no pueden trasladarse directamente al problema agroexportador.

---

## Reemplazar el último párrafo de 2.1.4 ADBench

Los resultados de ADBench muestran que el desempeño de los algoritmos depende de las características de los datos, del tipo de anomalía y del nivel de supervisión disponible. Por tanto, este antecedente no demuestra que cualquier ensemble sea superior a todos los detectores individuales. Su aporte para esta tesis consiste en justificar la evaluación de métodos complementarios y la necesidad de comprobar experimentalmente el comportamiento de su combinación.

---

## Reemplazar el segundo párrafo de 2.1.5 Grinsztajn

Los resultados mostraron que los modelos basados en árboles mantienen un desempeño competitivo o superior en numerosos conjuntos de datos tabulares de tamaño mediano. Los autores también identificaron propiedades que favorecen a estos modelos, como su robustez frente a características poco informativas y su capacidad para representar funciones irregulares.

Este antecedente respalda la evaluación de XGBoost y LightGBM como modelos principales. Sin embargo, no se asumirá que serán superiores antes de ejecutar los experimentos, por lo que deberán compararse con modelos base mediante validación temporal.

---

## Eliminar 2.1.6 Lim et al. como antecedente principal

El Temporal Fusion Transformer no forma parte de la implementación principal. El trabajo puede mencionarse brevemente dentro del estado del arte sobre forecasting, indicando que se excluye por el alcance y costo experimental.

Renumerar Zhao et al. como 2.1.6.

---

## Reemplazar el último párrafo de 2.1.7 Zhao

Este antecedente proporciona una base técnica para implementar detectores bajo una interfaz uniforme y reproducible. La selección de Isolation Forest, Local Outlier Factor y ECOD responde a que representan enfoques complementarios basados en aislamiento, densidad local y distribuciones empíricas. Su combinación deberá validarse sobre el conjunto de datos de la investigación y no será considerada superior por definición.

---

# CAMBIOS EN 2.2 ESTADO DEL ARTE

## Reemplazar el último párrafo de 2.2.1

Considerando que los datos disponibles para la investigación son principalmente registros estructurados de comercio exterior y variables agregadas en el tiempo, XGBoost y LightGBM serán evaluados como modelos principales. La selección responde a su adecuación para datos tabulares y no a una superioridad asumida. Su desempeño será comparado con modelos base utilizando divisiones temporales.

---

## Reemplazar los dos últimos párrafos de 2.2.2

La variabilidad observada entre los resultados de distintos detectores resulta relevante para esta investigación, debido a que las anomalías pueden manifestarse como desviaciones globales, cambios locales o valores situados en las colas de las distribuciones.

Por esta razón, se evaluarán Isolation Forest, Local Outlier Factor y ECOD tanto individualmente como mediante un score combinado normalizado por percentiles. La posible mejora del ensemble será considerada un resultado experimental y no una condición establecida de antemano.

---

## Reemplazar el último párrafo de 2.2.3

En esta investigación, los modelos de lenguaje no serán utilizados para determinar si una observación es anómala. Su función se limitará a estructurar un reporte a partir de valores observados, predicciones, residuos, puntuaciones de anomalía, explicaciones y fragmentos documentales recuperados. Las afirmaciones numéricas serán verificadas antes de aceptar el reporte.

---

## Reemplazar el tercer párrafo de 2.2.4

En el contexto de esta tesis, la integración se realizará sobre indicadores derivados de registros de comercio exterior, especialmente valor unitario FOB, volumen, número de operaciones, participación por destino y variables temporales. Las variables climáticas, logísticas o sanitarias solo se incorporarán cuando exista una relación temporal y metodológica justificable.

---

## Reemplazar el último párrafo de 2.2.5

La presente investigación incorporará explicabilidad, documentación, control de versiones y trazabilidad como características del diseño. El Decreto Supremo N.° 115-2025-PCM se utilizará como marco nacional general de referencia. La Resolución SBS N.° 053-2023 se considerará únicamente como una referencia de buenas prácticas para la gestión de riesgos de modelos, sin atribuirle aplicación directa sobre empresas agroexportadoras.

---

## Reemplazar la brecha de investigación

A partir de la literatura revisada se identifica una limitada evidencia de sistemas evaluados específicamente en el contexto agroexportador peruano que integren datos multisource, predicción semanal de indicadores comerciales, detección multivariable de anomalías, explicaciones de modelos y generación controlada de reportes con trazabilidad extremo a extremo.

La brecha no corresponde a la ausencia absoluta de cada tecnología, debido a que existen investigaciones sobre predicción, anomalías, explicabilidad y modelos de lenguaje de forma individual. El espacio abordado por la tesis corresponde a su integración, implementación y evaluación dentro de un flujo reproducible aplicado a registros agroexportadores peruanos.

---

# CAPÍTULO III

# ELABORACIÓN DE LA PROPUESTA

## 3.1 Generalidades

La propuesta consiste en el desarrollo de un sistema integrado de inteligencia artificial explicable para apoyar la supervisión analítica de operaciones agroexportadoras peruanas.

El sistema recibirá registros de exportación y variables contextuales, realizará procesos de validación y normalización, construirá un dataset semanal, generará predicciones del valor unitario FOB y del volumen, detectará desviaciones multivariables, elaborará explicaciones y producirá reportes trazables.

La unidad de análisis será la combinación de producto, mercado de destino y semana. Los productos comprendidos serán palta, uva fresca y arándano. El horizonte predictivo será de una semana.

Los usuarios previstos son:

* analistas de datos;
* supervisores de operaciones;
* responsables de control;
* auditores de tecnologías de información;
* investigadores;
* administradores del sistema.

Las entradas principales serán:

* registros de exportación;
* catálogos de productos y destinos;
* variables macroeconómicas;
* variables contextuales con cobertura válida;
* archivos de configuración;
* documentos metodológicos para recuperación.

Las salidas principales serán:

* predicción del valor unitario FOB;
* predicción del volumen;
* residuos predictivos;
* puntuación de cada detector;
* score combinado;
* nivel de severidad;
* explicación local;
* reporte validado;
* registro de trazabilidad.

El sistema se desarrollará bajo los principios de modularidad, reproducibilidad, explicabilidad, validación de evidencia, supervisión humana y separación de responsabilidades.

La propuesta no contempla monitoreo en tiempo real, integración directa con ERP, decisiones automáticas, identificación causal de riesgos ni sustitución del criterio humano.

### Requisitos funcionales

* RF01: importar datos desde las fuentes configuradas;
* RF02: validar estructura, tipos y calidad;
* RF03: normalizar fechas, países, productos, pesos y valores;
* RF04: construir agregaciones semanales;
* RF05: generar características temporales;
* RF06: entrenar y registrar modelos predictivos;
* RF07: generar predicciones;
* RF08: calcular residuos fuera de muestra;
* RF09: ejecutar detectores de anomalías;
* RF10: combinar puntuaciones mediante percentiles;
* RF11: generar explicaciones;
* RF12: construir paquetes de evidencia;
* RF13: recuperar documentos relacionados;
* RF14: generar reportes;
* RF15: validar cifras y afirmaciones;
* RF16: reconstruir una alerta mediante su identificador;
* RF17: consultar predicciones y alertas;
* RF18: exportar tablas, figuras y reportes.

### Requisitos no funcionales

* RNF01: reproducibilidad;
* RNF02: auditabilidad;
* RNF03: integridad de datos;
* RNF04: modularidad;
* RNF05: mantenibilidad;
* RNF06: portabilidad;
* RNF07: protección de identificadores;
* RNF08: trazabilidad;
* RNF09: control de configuración;
* RNF10: usabilidad.

---

## 3.2 Esquema de la propuesta

El esquema general comprende las siguientes etapas:

**Fuentes de datos → Ingesta → Validación → Normalización → Agregación semanal → Ingeniería de características → Predicción → Residuos → Detección de anomalías → Explicabilidad → Recuperación de evidencia → Generación del reporte → Validación → Trazabilidad**

### 3.2.1 Capa de datos

Los archivos originales serán conservados sin modificaciones en una zona raw. Posteriormente serán convertidos a una estructura tabular normalizada.

La arquitectura considerará:

* raw: archivos originales;
* bronze: archivos estructurados sin transformación analítica;
* silver: datos limpios y normalizados;
* gold: dataset semanal, características y variables objetivo.

Cada archivo y dataset contará con identificador, fecha de procesamiento, cantidad de registros y hash.

### 3.2.2 Construcción de la unidad semanal

Los registros serán agrupados mediante:

* producto;
* mercado de destino;
* semana.

Se calcularán:

* valor FOB total;
* peso neto total;
* valor unitario FOB;
* cantidad de operaciones;
* número de exportadores anonimizados;
* peso promedio por operación;
* participación del destino;
* presencia o ausencia de exportaciones.

### 3.2.3 Variables objetivo

El valor unitario FOB será calculado mediante:

[
VUFOB_t =
\frac{FOB\ total_t}{peso\ neto\ total_t}
]

La primera variable objetivo será:

[
Y^{FOB}*{t+1} = VUFOB*{t+1}
]

La segunda variable objetivo será:

[
Y^{volumen}*{t+1} =
volumen\ exportado*{t+1}
]

### 3.2.4 Ingeniería de características

Se construirán:

* variables calendario;
* rezagos de 1, 2, 4, 8, 13, 26 y 52 semanas;
* medias móviles;
* medianas móviles;
* desviaciones;
* medianas de desviación absoluta;
* cambios porcentuales;
* semanas desde la última exportación;
* variables contextuales disponibles.

Todas las ventanas serán desplazadas para impedir que incluyan información de la semana objetivo.

### 3.2.5 Predicción

Se implementarán modelos base y modelos XGBoost y LightGBM.

Los modelos base serán:

* última observación;
* mediana de cuatro semanas;
* valor estacional;
* modelo lineal regularizado.

La validación se realizará mediante divisiones temporales expansivas. Las últimas 52 semanas se reservarán para evaluación final.

### 3.2.6 Residuos

Se calcularán:

[
residuo =
valor\ observado - valor\ predicho
]

Los residuos empleados en detección serán obtenidos mediante predicciones fuera de muestra.

### 3.2.7 Detección de anomalías

Se utilizarán:

* Isolation Forest;
* Local Outlier Factor;
* ECOD.

Los scores serán convertidos a percentiles. El score del ensemble será el promedio de los percentiles.

Una alerta se generará cuando:

* el score combinado sea igual o mayor al percentil 95; o
* al menos dos detectores superen su respectivo percentil 95.

### 3.2.8 Explicabilidad

SHAP será aplicado a XGBoost y LightGBM para interpretar las predicciones.

La explicación de una alerta combinará:

* SHAP de precio;
* SHAP de volumen;
* residuos;
* desviaciones robustas;
* scores de detectores;
* cambios históricos.

### 3.2.9 Generación de reportes

El componente de reportes recibirá un objeto estructurado que contenga:

* identificación de la alerta;
* valores observados;
* valores predichos;
* diferencias;
* scores;
* severidad;
* variables SHAP;
* fuentes;
* versiones.

El modelo de lenguaje no modificará los valores. Después de generar el texto, un validador comparará las cifras con la evidencia.

### 3.2.10 Trazabilidad

Cada ejecución registrará:

* versión del archivo;
* versión del dataset;
* versión de características;
* versión del modelo;
* predicción;
* score;
* explicación;
* evidencia recuperada;
* prompt;
* reporte;
* validación.

El usuario podrá reconstruir todo el proceso utilizando el identificador de la alerta.
