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

### 1.4.1 Hipótesis general

La implementación de un sistema integrado de inteligencia artificial explicable, compuesto por predicción semanal de valor unitario FOB y volumen exportado, detección multivariable de anomalías, explicabilidad SHAP, reportes RAG con validación factual y trazabilidad documental, mejora significativamente la efectividad de la supervisión analítica de operaciones agroexportadoras peruanas respecto del uso de componentes analíticos aislados.

### 1.4.2 Hipótesis nula (H0)

La implementación de un sistema integrado de inteligencia artificial explicable no produce una mejora significativa en la efectividad de la supervisión analítica de operaciones agroexportadoras peruanas respecto del uso de componentes analíticos aislados, considerando rendimiento predictivo, detección de anomalías, comprensión del usuario, tiempo de análisis y trazabilidad documental.

### 1.4.3 Hipótesis específicas

**H1a.** Los modelos globales XGBoost o LightGBM, entrenados sobre el dataset semanal producto-mercado-semana, presentan un error absoluto medio (MAE) significativamente menor que el mejor modelo base para predecir el valor unitario FOB de la siguiente semana.

**H1b.** Los modelos globales XGBoost o LightGBM, entrenados sobre el dataset semanal producto-mercado-semana, presentan un error logarítmico cuadrático medio (RMSLE) significativamente menor que el mejor modelo base para predecir el volumen exportado de la siguiente semana.

**H1c.** El ensemble de Isolation Forest, Local Outlier Factor y ECOD, calibrado por percentiles y alimentado con residuos predictivos y variables agroexportadoras, presenta un F1-Score superior al promedio de sus detectores individuales en un conjunto experimental con anomalías controladas.

**H1d.** Las alertas acompañadas de explicaciones SHAP y reportes RAG trazables producen una mayor comprensión operativa y un menor tiempo de análisis en los usuarios evaluadores que las alertas presentadas únicamente mediante resultados técnicos aislados.

**H1e.** El módulo de trazabilidad basado en identificadores, metadatos y hashes SHA-256 incrementa la proporción de alertas cuyo proceso puede reconstruirse desde los registros de origen, el dataset versionado y el modelo utilizado hasta la explicación, la decisión humana y el reporte final.

---

## 1.5 Variables e indicadores

### 1.5.1 Variable independiente
*   **Tipo de sistema de supervisión analítica (VI):**
    *   *Nivel 1: Sistema integrado* (pipeline secuencial de 4 capas: predicción, ensemble PyOD, SHAP y RAG con validador y trazabilidad de hashes).
    *   *Nivel 2: Componentes aislados* (salidas técnicas de predicción y scores sin contexto lingüístico ni linaje estructurado).

### 1.5.2 Variable dependiente
*   **Efectividad de la supervisión analítica (VD):** evaluada en las dimensiones de rendimiento predictivo, rendimiento de detección, usabilidad subjetiva, tiempo de respuesta de diagnóstico y tasa de trazabilidad documental.

*(La tabla de operacionalización detallada que vincula dimensiones, indicadores, escalas, técnicas e instrumentos se incorpora como anexo compilado de esta tesis: "Matriz de Operacionalización").*

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
*   **Productivo:** El núcleo experimental está acotado a palta (*avocado*), uva fresca (*grape*) y arándano (*blueberry*). El espárrago se conserva como producto secundario o de sensibilidad solo si se declara su menor cobertura y no se mezcla en conclusiones principales. Se excluye permanentemente cacao por baja representatividad.
*   **Temporal:** Ventana continua desde **junio de 2018 hasta mayo de 2026**.
*   **Exclusiones:** No se implementará monitoreo de variables en tiempo real, control autónomo de despachos aduaneros, modelos de Deep Learning como propuesta principal ni integraciones funcionales con sistemas ERP privados de empresas particulares.

---

## 1.9 Línea, tipo y nivel de investigación
*   **Línea de Investigación:** *Inteligencia Artificial y Aprendizaje Automático Aplicado* (línea principal) e *Ingeniería de Software y Gobernanza de TI* (línea secundaria) de la Escuela Profesional de Ingeniería de Sistemas de la UNSA.
*   **Tipo de Investigación:** Aplicada y tecnológica.
*   **Nivel de Investigación:** Explicativo y evaluativo, con un enfoque epistemológico post-positivista.
*   **Diseño de Investigación:** Cuasiexperimental (comparación de VI), longitudinal (análisis temporal 2018-2026) y comparativo (evaluación frente a baselines).

---

## 1.10 Técnicas e instrumentos de recolección de información

La investigación combina técnicas documentales, computacionales, funcionales y evaluativas. Debido a que el objeto de estudio es un sistema integrado de inteligencia artificial explicable, la recolección de información incluye literatura, fuentes institucionales, datasets, métricas, logs, reportes automáticos, pruebas de calidad, evidencia de prototipo y registros de interacción de usuarios.

Las técnicas utilizadas son:

- Análisis documental.
- Experimentación computacional.
- Pruebas funcionales del sistema.
- Auditoría de trazabilidad.
- Prueba controlada con usuarios.
- Evaluación mediante rúbricas.

**Tabla 1.3 — Técnicas e instrumentos de recolección de información**

| Técnica | Instrumento | Propósito |
|---|---|---|
| Análisis documental | Matriz de revisión bibliográfica y ficha de antecedentes | Identificar fundamentos teóricos, antecedentes, brechas, algoritmos aplicables y criterios de comparación para sustentar el Capítulo II. |
| Análisis documental | Ficha de fuente de datos | Registrar origen, granularidad, periodo, licencia, ruta local, limitaciones y clasificación de cada fuente como real observada, agregada, proxy o sintética controlada. |
| Experimentación computacional | Scripts de ETL, integración y preparación semanal | Construir el dataset agroexportador integrado a nivel producto, mercado y semana ISO, manteniendo trazabilidad de fuentes y reglas de transformación. |
| Experimentación computacional | Scripts de entrenamiento y evaluación predictiva | Medir el desempeño de modelos basales, XGBoost y LightGBM para predicción semanal de valor unitario FOB y volumen exportado. |
| Experimentación computacional | Scripts de detección de anomalías | Evaluar Isolation Forest, Local Outlier Factor, ECOD y el ensemble propuesto frente a anomalías estadísticas o sintéticas controladas. |
| Pruebas funcionales del sistema | Checklist de rutas, pantallas y endpoints | Verificar que el prototipo funcional ejecute login, dashboard, alertas, detalle, historial, telemetría, integridad, datos, configuración y usuarios. |
| Pruebas funcionales del sistema | Capturas de pantalla documentadas | Registrar visualmente las pantallas del prototipo y dejar evidencia de las figuras que deberán incorporarse al documento final. |
| Auditoría de trazabilidad | Registro de hashes SHA-256, UUID y versiones | Reconstruir el linaje de datasets, modelos, alertas, explicaciones, reportes y artefactos experimentales. |
| Auditoría de trazabilidad | Pruebas automatizadas de calidad y fuga temporal | Confirmar reglas mínimas de calidad, partición temporal, ausencia de fuga de información y reproducibilidad de evidencia. |
| Prueba controlada con usuarios | Cuestionario SUS y escala Likert de comprensión | Medir usabilidad percibida, claridad, utilidad de explicaciones y comprensión de alertas por parte de usuarios evaluadores. |
| Prueba controlada con usuarios | Registro automático de tiempo y decisión | Comparar la condición de sistema integrado frente a la condición de resultados aislados mediante tiempo de análisis y respuestas correctas. |
| Evaluación mediante rúbricas | Rúbrica de reportes automáticos | Validar completitud, coherencia, fidelidad factual, consistencia numérica y presencia de evidencia estructurada en reportes generados. |
| Evaluación mediante rúbricas | Matriz de aceptación de evidencia | Clasificar artefactos como preliminares, candidatos o finales y verificar si cada evidencia puede reproducirse e incorporarse a la tesis. |

Datos pendientes para completar esta sección en la versión final:

- Definir el formato institucional final de las fichas de análisis documental.
- Incorporar las capturas definitivas del prototipo en `docs/figures/`.
- Guardar el instrumento final de consentimiento, tareas, encuesta SUS y escala Likert.
- Registrar la prueba automatizada de fuga temporal en `reports/tesis/data-quality/leakage-tests/`.
- Registrar corridas experimentales con identificador, commit, semilla, configuración, métricas y hashes.
- Incorporar la rúbrica final de validación factual de reportes automáticos.
- Precisar número final y perfil de participantes de la prueba controlada con usuarios.
- Marcar como definitivos solo los artefactos que cuenten con comando, salida esperada, fecha, versión y evidencia reproducible.

---

## 1.11 Cronograma de actividades

El cronograma se organiza desde el estado actual del proyecto hasta la primera semana de diciembre de 2026, fecha prevista para la sustentación de tesis. Las fechas podrán ajustarse por calendario académico, disponibilidad del asesor o requisitos administrativos de la escuela, pero la secuencia metodológica debe mantenerse: cierre documental, cierre de datos, experimento, redacción final, revisión, depósito y sustentación.

**Tabla 1.2 — Cronograma de actividades hasta sustentación**

| Fase | Periodo | Actividades principales | Producto verificable | Estado esperado |
|---|---|---|---|---|
| F1. Ordenamiento documental | 22-30 junio 2026 | Completar Capítulos II y III, depurar antecedentes nacionales, consolidar placeholders de figuras y capturas | `docs/02-20`, `02-21`, `02-22`, `02-30`, tesis monolítica regenerada | En curso |
| F2. Cierre de datos | 1-15 julio 2026 | Congelar dataset gold, registrar hashes, validar cobertura, resolver duplicados funcionales y documentar fuentes proxy | `data/gold/`, `codex-revision/reporte-calidad-datos.md`, reporte de dataset | Pendiente |
| F3. Pruebas de calidad y fuga | 16-31 julio 2026 | Ejecutar pruebas de calidad, fuga temporal, escaladores, codificadores y partición temporal | `reports/tesis/data-quality/leakage-tests/` | Pendiente |
| F4. Entrenamiento predictivo | 1-20 agosto 2026 | Entrenar baselines, XGBoost y LightGBM para FOB y volumen; registrar hiperparámetros y residuos fuera de muestra | `reports/tesis/experiments/<run_id>/` | Pendiente |
| F5. Validación de anomalías | 21 agosto-5 septiembre 2026 | Ejecutar IF, LOF, ECOD, ensemble, anomalías sintéticas y métricas por tipo | Métricas PR-AUC, F1, Recall, Precision@k | Pendiente |
| F6. Explicabilidad y reportes | 6-20 septiembre 2026 | Generar SHAP, reportes RAG, validación factual y comparación con plantilla determinística | `data/gold/local_explanations.json`, `validation_metrics.json`, reportes auditados | Pendiente |
| F7. Prototipo y capturas finales | 21 septiembre-5 octubre 2026 | Verificar `sistema-web-agro`, capturar pantallas finales, insertar figuras y actualizar anexos | `docs/figures/`, anexos y evidencia visual | Pendiente |
| F8. Prueba controlada con usuarios | 6-20 octubre 2026 | Ejecutar estudio A/B, consentimiento, anonimización, SUS, tiempos y decisiones | `reports/tesis/user-study/` | Pendiente |
| F9. Capítulo IV final | 21 octubre-5 noviembre 2026 | Reemplazar resultados preliminares por resultados reproducibles, contrastar hipótesis y cerrar discusión | Capítulo IV actualizado | Pendiente |
| F10. Capítulo V y conclusiones | 6-15 noviembre 2026 | Redactar conclusiones, limitaciones, recomendaciones y trabajos futuros según resultados finales | Capítulo V y recomendaciones | Pendiente |
| F11. Revisión integral | 16-22 noviembre 2026 | Revisar formato, APA, citas, tablas, figuras, anexos, índices y coherencia de hipótesis | Borrador final revisado | Pendiente |
| F12. Compilación y depósito | 23-30 noviembre 2026 | Generar PDF/DOCX final, verificar maquetación, firmar anexos y preparar entrega administrativa | `output/tesis_final.pdf`, `output/tesis_final.docx` | Pendiente |
| F13. Sustentación | Primera semana de diciembre 2026 | Presentación, defensa, demostración del prototipo y respuesta a observaciones | Sustentación de tesis | Meta final |

**Hito final:** sustentación de tesis durante la primera semana de diciembre de 2026.
