# CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA

## 1.1 Descripción de la realidad problemática

### Contexto
Las operaciones agroexportadoras peruanas representan uno de los motores económicos principales del país, impulsando el desarrollo agrícola y la balanza comercial. La comercialización de productos agrícolas perecederos, como la palta, la uva fresca y el arándano, requiere una coordinación precisa de la producción, el empaque, el control fitosanitario, la logística de frío y el despacho aduanero. Durante estas etapas, se genera un volumen masivo y continuo de información: registros aduaneros, reportes de precios mayoristas nacionales, variables macroeconómicas, condiciones climáticas regionales, tiempos de despacho portuario y alertas sanitarias en mercados de destino. 

### Problema de datos
A pesar de la abundancia de registros, la información en este dominio se encuentra fragmentada entre múltiples organizaciones e instituciones públicas y privadas (SUNAT, MIDAGRI, BCRP, SENASA, NASA POWER). Los datos poseen granularidades y formatos heterogéneos: microdatos transaccionales aduaneros por contenedor, precios mayoristas diarios agregados a nivel de mercado mayorista local, tipos de cambio mensuales, y datos climáticos georreferenciados semanales. No existe una estructura unificada o canal que integre estas fuentes para obtener una perspectiva operativa única. Por ende, la tesis propone y adopta la construcción de un **dataset agroexportador integrado** que consolida datos reales observados de aduanas, datos agregados macroeconómicos y sectoriales, proxies documentados y datos sintéticos controlados para simulaciones.

### Problema analítico
En la gestión de las operaciones, la simple observación de una cifra de exportación (ej. un valor FOB o un volumen por contenedor) no permite determinar si la transacción se encuentra dentro de los parámetros normales de comportamiento o si constituye una desviación crítica. Para realizar una supervisión efectiva, es indispensable construir un **valor esperado** histórico que sirva de línea base de comparación y permita calcular el residuo predictivo (la desviación respecto de lo esperado). La falta de estimaciones semanales de valor unitario FOB y volumen exportado impide parametrizar el comportamiento histórico normal y multivariable de las exportaciones.

### Problema explicativo
Los modelos predictivos o algoritmos de detección de anomalías tradicionales (como Isolation Forest o LOF) operan como cajas negras. Aunque un ensemble unificado genere una alerta de riesgo sobre una operación específica (determinando que es una desviación con severidad baja, media o alta), la ausencia de explicabilidad reduce la confianza de los analistas de negocio. Sin una justificación local del peso marginal de cada característica (ej. a través de valores SHAP), los analistas no pueden determinar qué variables exógenas o comerciales empujaron la transacción hacia el rango de anomalía.

### Problema documental
Finalmente, incluso si el sistema detecta una anomalía y explica sus variables, persiste una brecha documental importante. Los analistas y auditores internos requieren reportes en lenguaje natural claros y trazables que vinculen la alerta con el sustento de datos reales. La automatización tradicional de reportes mediante modelos de lenguaje (LLMs) carece de controles factuales deterministas, lo que introduce el riesgo de alucinaciones (cifras e interpretaciones inventadas por el modelo). Asimismo, se requiere garantizar el linaje inmutable de cada alerta desde los datos de origen de SUNAT hasta el informe final.

### Síntesis
En consecuencia, se identifica la necesidad de diseñar, implementar y evaluar un sistema integrado de inteligencia artificial explicable que resuelva de forma unificada la ingesta y agregación de datos multisource, la estimación predictiva de valores esperados, la detección de desviaciones multivariables mediante un ensemble de anomalías, la interpretación de factores mediante SHAP y la redacción de informes técnicos trazables mediante RAG con control factual.

---

## 1.2 Problema principal

¿En qué medida la implementación de un sistema integrado de inteligencia artificial basado en la predicción semanal del valor unitario FOB y del volumen exportado, la detección multivariable de anomalías, la explicabilidad y la generación automática de reportes trazables mejora la efectividad de la supervisión analítica de operaciones agroexportadoras peruanas respecto del uso de componentes aislados?

### Subproblemas

1.  ¿Cómo integrar fuentes heterogéneas de datos reales de comercio exterior, mercado interno, macroeconomía, clima, logística y sanidad sin confundir granularidades ni inducir fuga de información temporal?
2.  ¿Qué desempeño predictivo logran los algoritmos globales de regresión XGBoost y LightGBM para estimar el valor unitario FOB esperado de la siguiente semana frente a los baselines históricos y Elastic Net?
3.  ¿Qué desempeño predictivo logran para estimar el volumen de exportación de la siguiente semana?
4.  ¿Qué desempeño de detección obtiene el ensemble de Isolation Forest, Local Outlier Factor y ECOD frente a los detectores individuales en un conjunto de anomalías sintéticas controladas?
5.  ¿De qué manera las explicaciones locales SHAP y el contexto de RAG mejoran la comprensión operativa de las alertas aduaneras?
6.  ¿Cómo validar la consistencia numérica de los reportes narrativos autogenerados y garantizar el linaje inmutable de cada alerta desde el dato de origen?
7.  ¿Qué mejora cuantitativa existe en la tasa de comprensión, usabilidad y tiempo de decisión de los analistas humanos al interactuar con el sistema integrado frente a componentes aislados?

---

## 1.3 Objetivos

### 1.3.1 Objetivo principal

Diseñar, implementar y evaluar un sistema integrado de inteligencia artificial explicable para predecir semanalmente el valor unitario FOB y el volumen exportado, detectar anomalías multivariables, explicar las predicciones e interpretar las alertas mediante SHAP, y generar reportes trazables sustentados en evidencia estructurada para apoyar la supervisión analítica de operaciones agroexportadoras peruanas.

### 1.3.2 Objetivos específicos

1.  Identificar, auditar, normalizar e integrar las fuentes de datos agroexportadores reales de SUNAT, BCRP y SISAP con proxies climáticos, logísticos y sanitarios.
2.  Construir un dataset agroexportador integrado semanal a nivel de producto × mercado de destino × semana ISO con marcas metodológicas y sin fuga de información temporal.
3.  Implementar y optimizar modelos globales GBDT (XGBoost/LightGBM) para predecir el valor unitario FOB de exportación de la siguiente semana ($t+1$) y evaluar su desempeño frente a baselines.
4.  Implementar y optimizar modelos globales GBDT para predecir el volumen de exportación de la siguiente semana ($t+1$).
5.  Implementar un ensemble unificado no supervisado de Isolation Forest, Local Outlier Factor y ECOD calibrado por percentiles para la detección de anomalías operativas.
6.  Integrar explicaciones locales de Shapley (SHAP) basadas en TreeSHAP para justificar la contribución de variables en los modelos predictivos de las alertas.
7.  Implementar un generador de reportes basado en arquitectura RAG y un LLM, incorporando un módulo validador factual que compare determinísticamente las cifras textuales con la evidencia de datos.
8.  Evaluar la efectividad del sistema integrado mediante experimentos de usabilidad (escala SUS, tiempo de decisión y tasa de acierto) y auditoría de linaje con hashes SHA-256 frente a componentes aislados.

---

## 1.4 Hipótesis de la investigación

### Hipótesis general (H1)
El sistema integrado de predicción, detección de anomalías, explicabilidad y reportes trazables mejora significativamente la efectividad de la supervisión analítica de operaciones agroexportadoras peruanas en comparación con el uso de componentes analíticos aislados.

### Hipótesis predictiva de FOB (H1a)
Los modelos globales de aprendizaje supervisado (XGBoost o LightGBM) presentan un error absoluto medio (MAE) significativamente menor en la predicción del valor unitario FOB esperado de la semana $t+1$ que el mejor baseline histórico y Elastic Net en el conjunto de test.

### Hipótesis predictiva de volumen (H1b)
Los regresores globales de GBDT obtienen un error cuadrático medio logarítmico (RMSLE) menor que la mediana móvil y el baseline estacional en el pronóstico del volumen semanal en el conjunto de test.

### Hipótesis de anomalías (H1c)
El ensemble no supervisado (IF + LOF + ECOD) calibrado por percentiles presenta una puntuación F1-score superior al promedio de sus detectores individuales sobre el conjunto de validación de anomalías sintéticas controladas.

### Hipótesis de usabilidad (H1d)
Las explicaciones de SHAP combinadas con reportes narrativos RAG incrementan significativamente la tasa de comprensión operativa y reducen el tiempo de decisión de los evaluadores humanos frente a salidas técnicas y scores aislados.

### Hipótesis de trazabilidad (H1e)
El sistema integrado de metadatos y hashes SHA-256 permite alcanzar una proporción del 100% de alertas con trazabilidad documental completa y linaje reconstruible desde el microdato SUNAT hasta el informe técnico final.

---

## 1.5 Variables e indicadores

### 1.5.1 Variable independiente
*   **Tipo de sistema de supervisión analítica (VI):**
    *   *Nivel 1: Sistema integrado* (pipeline secuencial de 4 capas: predicción, ensemble PyOD, SHAP y RAG con validador y trazabilidad de hashes).
    *   *Nivel 2: Componentes aislados* (salidas técnicas de predicción y scores sin contexto lingüístico ni linaje estructurado).

### 1.5.2 Variable dependiente
*   **Efectividad de la supervisión analítica (VD):** evaluada en las dimensiones de rendimiento predictivo, rendimiento de detección, usabilidad subjetiva, tiempo de respuesta de diagnóstico y tasa de trazabilidad documental.

*(La tabla de operacionalización detallada que vincula dimensiones, indicadores, escalas, técnicas e instrumentos se presenta en la [Matriz de Operacionalización](file:///d:/tesis_yoset/docs/tesis/MATRIZ_OPERACIONALIZACION.md)).*

---

## 1.6 Viabilidad de la investigación

### 1.6.1 Viabilidad técnica
El desarrollo del prototipo de software integrado es factible mediante el uso de librerías de código abierto y de amplia validación en la industria en lenguaje Python (pandas, numpy, scikit-learn, XGBoost, LightGBM, PyOD, SHAP, sentence-transformers, Flask). El hardware requerido consiste en equipos de cómputo convencionales en CPU sin requerir costosas estaciones de trabajo con GPU.

### 1.6.2 Viabilidad operativa
El sistema operará bajo una modalidad de procesamiento por lotes (batch), compatible con la recolección semanal de registros de exportación de la SUNAT. No requiere una integración intrusiva en tiempo real con los sistemas de aduanas o ERPs empresariales privados, actuando como una herramienta analítica de soporte de auditoría interna y supervisión independiente "human-in-the-loop" (gobernanza de IA).

### 1.6.3 Viabilidad económica
El costo financiero del proyecto es mínimo al sustentarse en licencias de software libre y recursos informáticos ya disponibles. La descarga de microdatos públicos es gratuita. La factibilidad económica del sistema se fundamenta en su potencial para optimizar los tiempos de auditoría de las agencias de comercio exterior y empresas comercializadoras, reduciendo mermas de control.

---

## 1.7 Justificación e importancia

### 1.7.1 Justificación teórica
El estudio aporta valor académico al integrar en una arquitectura única cuatro campos de la ciencia de la computación y la IA que suelen abordarse por separado en la literatura: el modelamiento tabular GBDT global, los ensembles de detección no supervisada, la teoría de Shapley para interpretabilidad algorítmica y los LLMs restringidos por RAG para redacción técnica.

### 1.7.2 Justificación metodológica
La investigación formula un marco estructurado de auditoría del origen de los datos, clasificando formalmente las variables por su naturaleza (real observada, agregada, proxy, sintética controlada) y forzando marcas de trazabilidad SHA-256. Esto mitiga el problema recurrente de opacidad y falta de reproducibilidad experimental en tesis tecnológicas.

### 1.7.3 Justificación práctica
El prototipo provee a los supervisores aduaneros y gestores agroexportadores peruanos una interfaz de control analítico. El sistema traduce matrices matemáticas de residuos y scores a reportes técnicos comprensibles con validación factual de cifras, facilitando la toma de decisiones basada en evidencias.

---

## 1.8 Alcance
*   **Temático y Tecnológico:** Diseño, desarrollo experimental y evaluación de una arquitectura modular de cuatro capas (Predicción, Detección de Anomalías con PyOD, Explicabilidad con TreeSHAP y Reporte con RAG/LLM) y un módulo registrador de trazabilidad con hashes SHA-256.
*   **Geográfico:** Microdatos de exportaciones agrícolas peruanas registradas en las aduanas nacionales, principalmente asociadas a las zonas productoras y puertos de La Libertad, Piura, Ica, Lambayeque y Arequipa.
*   **Productivo:** Acotado estrictamente a palta (*avocado*), uva fresca (*grape*) y arándano (*blueberry*). Se excluye permanentemente cacao por baja representatividad, y espárrago por limitación analítica.
*   **Temporal:** Ventana continua desde **junio de 2018 hasta mayo de 2026**.
*   **Exclusiones:** No se implementará monitoreo de variables en tiempo real, control autónomo de despachos aduaneros, modelos de Deep Learning como propuesta principal ni integraciones funcionales con sistemas ERP privados de empresas particulares.

---

## 1.9 Línea, tipo y nivel de investigación
*   **Línea de Investigación:** *Inteligencia Artificial y Aprendizaje Automático Aplicado* (línea principal) e *Ingeniería de Software y Gobernanza de TI* (línea secundaria) de la Escuela Profesional de Ingeniería de Sistemas de la UNSA.
*   **Tipo de Investigación:** Aplicada y tecnológica.
*   **Nivel de Investigación:** Explicativo y evaluativo, con un enfoque epistemológico post-positivista.
*   **Diseño de Investigación:** Cuasiexperimental (comparación de VI), longitudinal (análisis temporal 2018-2026) y comparativo (evaluación frente a baselines).

---

## 1.10 Técnicas e instrumentos
*   **Técnicas:** Análisis documental para estructuración de datos; experimentación tecnológica controlada para entrenamiento y pruebas de rendimiento del pipeline; encuestas para la evaluación de usabilidad y comprensión con usuarios.
*   **Instrumentos:** Ficha de normalización de datos; consola y scripts de entrenamiento y evaluación computacional en Python; cuestionario de usabilidad SUS; y scripts de registro automático de tiempos y validación factual de reportes.
