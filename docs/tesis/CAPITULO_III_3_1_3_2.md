# CAPÍTULO III: ELABORACIÓN DE LA PROPUESTA

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
Y^{FOB}_{t+1} = VUFOB_{t+1}
]

La segunda variable objetivo será:

[
Y^{volumen}_{t+1} =
volumen\ exportado_{t+1}
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
