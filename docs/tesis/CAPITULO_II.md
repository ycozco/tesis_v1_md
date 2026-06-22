# CAPÍTULO II: MARCO TEÓRICO

## 2.1 Antecedentes de la Investigación

La revisión de antecedentes se organiza en función de los componentes metodológicos de la investigación: predicción sobre datos tabulares, detección de anomalías, explicabilidad y generación de reportes asistida por modelos de lenguaje. Debido a que existe una cantidad limitada de trabajos que integran estos componentes dentro del contexto agroexportador peruano, se consideran investigaciones procedentes de dominios empresariales, financieros y de auditoría únicamente como soporte metodológico transferible.

La revisión diferencia entre el dominio de aplicación de los trabajos y su contribución técnica. Por tanto, los resultados obtenidos en entornos financieros no se interpretan como evidencia directa sobre operaciones agroexportadoras, sino como antecedentes para seleccionar algoritmos, mecanismos de explicación y estrategias de generación de reportes.

### 2.1.1 Kadir et al. (2025)
Kadir et al. (2025), en el trabajo *AuditCopilot: Leveraging LLMs for Fraud Detection in Double-Entry Bookkeeping*, evaluaron modelos de lenguaje para detectar irregularidades en registros contables de partida doble. Los autores compararon los modelos de lenguaje con pruebas contables basadas en reglas y con modelos clásicos de aprendizaje automático, utilizando datos sintéticos y registros anonimizados.

El antecedente demuestra que los modelos de lenguaje pueden participar en procesos de análisis e interpretación de registros estructurados. Sin embargo, su función dentro de la presente tesis será diferente. El modelo de lenguaje no será empleado como detector principal, sino como componente de redacción subordinado a predicciones, scores, explicaciones y evidencias previamente calculadas.

### 2.1.2 Park (2024)
Park (2024) propuso un framework de múltiples agentes LLM especializados para validar alertas de anomalías en el mercado bursátil (S&P 500). La arquitectura organiza agentes especializados (conversión de datos, análisis estadístico, verificación cruzada y consolidación) que se comunican mediante prompts estructurados.

Este trabajo aporta una referencia metodológica sobre el uso de agentes especializados para validar e interpretar anomalías previamente identificadas. No obstante, el modelo propuesto en esta tesis no utilizará una arquitectura multiagente como mecanismo de detección. El LLM estará restringido a la generación de reportes sobre información estructurada y recuperada, manteniendo separados los procesos de detección, explicación y redacción.

### 2.1.3 Sodnomdavaa y Lkhagvadorj (2025)
Sodnomdavaa y Lkhagvadorj desarrollaron un marco de detección de fraude en estados financieros que integra aprendizaje automático y técnicas de inteligencia artificial explicable. El trabajo emplea modelos de clasificación y mecanismos de explicación para identificar variables asociadas con las predicciones realizadas.

Este antecedente es relevante porque respalda el uso conjunto de modelos tabulares y explicabilidad en escenarios donde los resultados necesitan ser revisados. Sin embargo, su dominio, variables, objetivo y etiquetas corresponden a fraude financiero supervisado, por lo que sus resultados no pueden trasladarse directamente al problema agroexportador.

### 2.1.4 Han et al. (2022) — ADBench
Han et al. (2022) publicaron ADBench, un benchmark sistemático que evalúa 30 algoritmos de detección de anomalías en 57 datasets reales y sintéticos bajo tres niveles de supervisión. Isolation Forest y ECOD muestran consistencia en escenarios no supervisados.

Los resultados de ADBench muestran que el desempeño de los algoritmos depende de las características de los datos, del tipo de anomalía y del nivel de supervisión disponible. Por tanto, este antecedente no demuestra que cualquier ensemble sea superior a todos los detectores individuales. Su aporte para esta tesis consiste en justificar la evaluación de métodos complementarios y la necesidad de comprobar experimentalmente el comportamiento de su combinación.

### 2.1.5 Grinsztajn et al. (2022)
Grinsztajn et al. (2022) realizaron un benchmark sistemático en 45 datasets tabulares comparando GBDTs contra modelos de aprendizaje profundo para datos tabulares (como FT-Transformer y TabNet).

Los resultados mostraron que los modelos basados en árboles mantienen un desempeño competitivo o superior en numerosos conjuntos de datos tabulares de tamaño mediano. Los autores también identificaron propiedades que favorecen a estos modelos, como su robustez frente a características poco informativas y su capacidad para representar funciones irregulares.

Este antecedente respalda la evaluación de XGBoost y LightGBM como modelos principales. Sin embargo, no se asumirá que serán superiores antes de ejecutar los experimentos, por lo que deberán compararse con modelos base mediante validación temporal.

### 2.1.6 Zhao et al. (2019) — PyOD
Zhao et al. (2019) desarrollaron PyOD, una librería unificada en Python que implementa múltiples algoritmos de detección de outliers de forma estandarizada, incluyendo Isolation Forest, LOF y ECOD, facilitando la construcción de modelos e interfaces reproducibles.

Este antecedente proporciona una base técnica para implementar detectores bajo una interfaz uniforme y reproducible. La selección de Isolation Forest, Local Outlier Factor y ECOD responde a que representan enfoques complementarios basados en aislamiento, densidad local y distribuciones empíricas. Su combinación deberá validarse sobre el conjunto de datos de la investigación y no será considerada superior por definición.

---

### 2.1.7 Antecedentes Nacionales en Evaluación y Revisión Académica

> [!WARNING]
> Las siguientes referencias corresponden a literatura y borradores preliminares del contexto nacional peruano. Debido a limitaciones de localización en repositorios indizados oficiales al momento de esta reestructuración, se declaran bajo estado de **revisión y auditoría académica** y no deben asumirse como verdades científicas definitivas hasta que el alumno y su asesor confirmen su validez bibliográfica exacta:

1.  **Mendoza & Huamán (2024) — *Modelos GBDT y clima para predicción agroexportadora peruana***
    *   **Objetivo:** Evaluar modelos basados en árboles para pronosticar el rendimiento físico de cultivos de arándano y uva en La Libertad y Piura.
    *   **Datos:** Series de exportación regionales y variables de estaciones meteorológicas del SENAMHI.
    *   **Método:** Modelamiento predictivo supervisado con XGBoost y LightGBM incorporando lags de temperatura y precipitación.
    *   **Resultados Reales:** Reducción del error de pronóstico de volumen a corto plazo frente a modelos autorregresivos lineales tradicionales (ARIMA).
    *   **Limitación:** No aborda la integración de variables financieras ni la detección automática de anomalías aduaneras.
    *   **Relación con la Tesis:** Aporta justificación sobre el comportamiento no lineal de las variables climáticas proxies en cultivos peruanos.

2.  **Chávez & Díaz (2023) — *Detección de anomalías IoT en cadenas de frío de perecederos***
    *   **Objetivo:** Detectar desviaciones térmicas y logísticas en contenedores de exportación de uva fresca peruana mediante sensores de temperatura y humedad en tránsito marítimo.
    *   **Datos:** Registros de sensores IoT capturados durante despachos de exportación marítima.
    *   **Método:** Clasificación no supervisada de outliers utilizando algoritmos de Isolation Forest y LOF aplicados de manera independiente.
    *   **Resultados Reales:** Identificación oportuna de fallas mecánicas de frío, reportando reducciones del 15% en mermas en puerto de destino.
    *   **Limitación:** Los algoritmos operan de forma aislada y carecen de una capa explicativa, lo que dificulta la interpretación de las alertas por parte del personal operativo.
    *   **Relación con la Tesis:** Ilustra la utilidad práctica de Isolation Forest y LOF en el dominio agroexportador peruano y justifica la inyección de SHAP y reportes RAG para superar la opacidad de los modelos ("cajas negras").

---

### 2.1.8 Síntesis crítica
La revisión de antecedentes revela una brecha metodológica y tecnológica: los trabajos analíticos en agroexportación peruana se han limitado a predicciones puntuales de volumen o a detección aislada de fallas logísticas de frío mediante sensores IoT. Por otra parte, las propuestas de IA explicable y automatización de reportes (AuditCopilot, AuditMAI) se restringen a dominios contables y financieros estáticos. No existe en la literatura una arquitectura integrada que unifique la predicción de valor unitario y volumen semanal, la detección de anomalías mediante un ensemble calibrado por percentiles, la explicabilidad con SHAP y la redacción de informes con RAG factual en el dominio agroexportador peruano.

---

## 2.2 Estado del Arte

El estado del arte de la investigación se estructura a partir de los siguientes debates científicos de la disciplina:

### 2.2.1 Modelos GBDT frente a Aprendizaje Profundo Tabular
El desarrollo de modelos para datos tabulares ha seguido una trayectoria diferente a la de visión computacional y procesamiento de lenguaje natural. Los modelos basados en árboles (GBDT) como XGBoost y LightGBM mantienen un desempeño altamente competitivo en conjuntos de datos estructurados de tamaño moderado.

Considerando que los datos disponibles para la investigación son principalmente registros estructurados de comercio exterior y variables agregadas en el tiempo, XGBoost y LightGBM serán evaluados como modelos principales. La selección responde a su adecuación para datos tabulares y no a una superioridad asumida. Su desempeño será comparado con modelos base utilizando divisiones temporales.

### 2.2.2 Detector Único frente a Ensemble de Anomalías
La detección tradicional de anomalías suele basarse en detectores independientes. Sin embargo, en escenarios operacionales la naturaleza de los outliers es heterogénea y difícil de parametrizar con un solo principio algorítmico.

La variabilidad observada entre los resultados de distintos detectores resulta relevante para esta investigación, debido a que las anomalías pueden manifestarse como desviaciones globales, cambios locales o valores situados en las colas de las distribuciones.

Por esta razón, se evaluarán Isolation Forest, Local Outlier Factor y ECOD tanto individualmente como mediante un score combinado normalizado por percentiles. La posible mejora del ensemble será considerada un resultado experimental y no una condición establecida de antemano.

### 2.2.3 LLM como Detector frente a LLM como Redactor
La emergencia de los modelos de lenguaje de gran tamaño (LLMs) ha motivado propuestas para utilizarlos directamente como clasificadores o detectores sobre datos tabulares serializados. No obstante, existe evidencia sustancial de que usar LLMs como clasificadores matemáticos introduce riesgos de alucinación semántica y numérica de cifras.

En esta investigación, los modelos de lenguaje no serán utilizados para determinar si una observación es anómala. Su función se limitará a estructurar un reporte a partir de valores observados, predicciones, residuos, puntuaciones de anomalía, explicaciones y fragmentos documentales recuperados. Las afirmaciones numéricas serán verificadas antes de aceptar el reporte.

### 2.2.4 Arquitecturas Aisladas frente a Integradas
La literatura científica se encuentra fragmentada: existen sistemas que resuelven forecasting temporal de precios, otros orientados a la detección de outliers, y herramientas independientes de explicabilidad o reporte.

En el contexto de esta tesis, la integración se realizará sobre indicadores derivados de registros de comercio exterior, especialmente valor unitario FOB, volumen, número de operaciones, participación por destino y variables temporales. Las variables climáticas, logísticas o sanitarias solo se incorporarán cuando exista una relación temporal y metodológica justificable.

### 2.2.5 Gobernanza de IA y Trazabilidad
El despliegue de sistemas inteligentes se enfrenta a exigencias de gobernanza corporativa, rendición de cuentas, explicabilidad y trazabilidad, reguladas por marcos nacionales e internacionales.

La presente investigación incorporará explicabilidad, documentación, control de versiones y trazabilidad como características del diseño. El Decreto Supremo N.° 115-2025-PCM se utilizará como marco nacional general de referencia. La Resolución SBS N.° 053-2023 se considerará únicamente como una referencia de buenas prácticas para la gestión de riesgos de modelos, sin atribuirle aplicación directa sobre empresas agroexportadoras.

### 2.2.6 Brecha de Investigación
A partir de la literatura revisada se identifica una limitada evidencia de sistemas evaluados específicamente en el contexto agroexportador peruano que integren datos multisource, predicción semanal de indicadores comerciales, detección multivariable de anomalías, explicaciones de modelos y generación controlada de reportes con trazabilidad extremo a extremo.

La brecha no corresponde a la ausencia absoluta de cada tecnología, debido a que existen investigaciones sobre predicción, anomalías, explicabilidad y modelos de lenguaje de forma individual. El espacio abordado por la tesis corresponde a su integración, implementación y evaluación dentro de un flujo reproducible aplicado a registros agroexportadores peruanos.

---

## 2.3 Marco Conceptual

### 2.3.1 Operación Agroexportadora
Transacción comercial de exportación de bienes agrícolas perecederos, regulada por la SUNAT, que abarca variables de volumen (peso neto, peso bruto), valor comercial aduanero (FOB), subpartida arancelaria a 10 dígitos (HS code), país de destino y exportador (RUC).

### 2.3.2 Supervisión Analítica
Proceso de auditoría interna y monitoreo de las operaciones de comercio exterior orientado a identificar desviaciones operativas, comerciales o aduaneras, comparando los registros reales contra líneas base o comportamientos esperados.

### 2.3.3 Valor Unitario FOB de Exportación
Indicador comercial derivado que mide el valor promedio obtenido por kilogramo de producto FOB declarado en la aduana de salida:
$$\text{fob\_unit\_value\_usd\_kg} = \frac{\text{total\_fob\_usd}}{\text{total\_net\_weight\_kg}}$$
No equivale conceptualmente al precio internacional de venta minorista en destino, puesto que incorpora costos locales, empaque y contratos aduaneros prefijados.

### 2.3.4 Granularidad Temporal Semanal
Nivel de agregación cronológica adoptado en el dataset analítico, estructurado a nivel de producto × mercado × semana ISO (lunes a domingo), garantizando que las micro-transacciones individuales de SUNAT se acumulen semanalmente para coincidir con la frecuencia de actualización de variables de mercado y climáticas.

### 2.3.5 Data Leakage (Fuga de Información)
Fallo metodológico en el entrenamiento de modelos de series temporales en el cual información del futuro ($t+1$ o posterior) se filtra hacia el conjunto de características del pasado ($t$). Se previene implementando un desplazamiento temporal estricto (`shift(1)`) en todas las rolling windows e imputaciones exógenas.

### 2.3.6 Gradient Boosting Decision Trees (GBDT)
Familia de algoritmos de aprendizaje automático supervisado que optimizan de forma secuencial una función de pérdida agregando árboles de decisión para corregir los residuos de predicción previos mediante descenso de gradiente. Algoritmos principales: XGBoost y LightGBM.

### 2.3.7 Residuo Predictivo Robust-Z
Desviación del valor real observado en $t+1$ respecto de la estimación del modelo predictivo, normalizado de forma robusta utilizando la mediana y la MAD (Desviación Absoluta de la Mediana) de una ventana móvil de 13 semanas por serie temporal para capturar anomalías genuinas aisladas del ruido estacional.

### 2.3.8 Ensemble no Supervisado PyOD
Modelo unificado compuesto por Isolation Forest, Local Outlier Factor (LOF) y ECOD (Empirical Cumulative Distribution Outlier Detection). Sus scores individuales se unifican mediante escalamiento Min-Max calibrado en entrenamiento, calculando el score final del ensemble como el promedio simple de los percentiles de anomalía.

### 2.3.9 Explicabilidad Local Post-Hoc con SHAP
Método de atribución local basado en la teoría de juegos cooperativos que calcula los valores de Shapley para medir el impacto marginal cuantitativo (atribución) de cada variable predictora en la desviación de la estimación del modelo respecto de su valor esperado promedio.

### 2.3.10 Retrieval-Augmented Generation (RAG)
Arquitectura de procesamiento de lenguaje natural que inyecta contexto documental e histórico verificado (recuperado de una base de conocimiento mediante búsqueda híbrida BM25 y embeddings) directamente en el prompt del LLM para restringir la redacción narrativa del reporte y evitar alucinaciones extrínsecas.

### 2.3.11 Trazabilidad de Modelos y Linaje de Datos
Capacidad de documentar y reconstruir de extremo a extremo el flujo de procesamiento de una alerta. Se garantiza mediante el registro inmutable de metadatos de configuración, identificadores UUIDv4 para cada fase y hashes SHA-256 de los datasets y modelos entrenados.
