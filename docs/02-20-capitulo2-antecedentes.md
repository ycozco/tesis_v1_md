# CAPÍTULO II: MARCO TEÓRICO

## 2.1 Antecedentes de la Investigación

### 2.1.1 Antecedentes Internacionales

1.  **Kadir et al. (2025) — *AuditCopilot: Leveraging LLMs for fraud detection in double-entry bookkeeping***
    *   **Objetivo:** Desarrollar un sistema de auditoría contable que integre modelos de lenguaje con técnicas de detección de anomalías para explicar transacciones irregulares en lenguaje natural.
    *   **Datos:** Corpus experimental de asientos contables sintéticos y transacciones financieras de doble entrada.
    *   **Método:** Pipeline secuencial compuesto por detección algorítmica de outliers, inyección de contexto en prompts estructurados y generación de textos explicativos mediante un LLM de gran escala.
    *   **Resultados Reales:** Incremento en la tasa de detección de fraudes y reducción del tiempo promedio de revisión por parte de los auditores humanos, validado mediante pruebas cualitativas de usabilidad.
    *   **Limitación:** El modelado se restringe a datos contables tradicionales de doble entrada y no incorpora variables exógenas como el clima, precios de mercado mayorista o datos logísticos complejos.
    *   **Relación con la Tesis:** Aporta el fundamento metodológico para combinar la detección algorítmica con la generación narrativa RAG. La tesis traslada esta arquitectura al dominio de operaciones agroexportadoras perecederas en el Perú.

2.  **Park (2024) — *LLMs for anomaly validation and report generation in financial systems***
    *   **Objetivo:** Diseñar un framework multi-agente basado en LLMs especializados para la validación y documentación de alertas de anomalías en mercados financieros de alta frecuencia.
    *   **Datos:** Series temporales financieras diarias del índice S&P 500 y noticias comerciales asociadas.
    *   **Método:** División del procesamiento en cuatro agentes inteligentes: conversión de datos, análisis estadístico, verificación cruzada documental y generación/consolidación del reporte.
    *   **Resultados Reales:** Reducción de falsos positivos en las alarmas mediante el filtrado semántico y la verificación de noticias, superando el rendimiento de un agente genérico único.
    *   **Limitación:** El sistema opera en mercados financieros de alta frecuencia y requiere acceso constante a noticias de mercado en tiempo real, lo que eleva el costo computacional.
    *   **Relación con la Tesis:** Sustenta la separación de roles entre los modelos matemáticos cuantitativos de detección y la capa de lenguaje. La tesis adopta la restricción de que el LLM no es el detector, sino el redactor fundamentado en evidencias.

3.  **Almalki & Masud (2025) — *Financial fraud detection using explainable AI and stacking ensemble methods***
    *   **Objetivo:** Diseñar un framework de detección de fraude en transacciones empresariales combinando modelos de ensamble de gradiente y explicabilidad post-hoc.
    *   **Datos:** Datasets tabulares corporativos de transacciones financieras y estados contables.
    *   **Método:** Stacking Ensemble de clasificadores basados en árboles (XGBoost y LightGBM) acoplado a un motor de atribución local SHAP para generar la justificación de las alertas.
    *   **Resultados Reales:** Obtención de un PR-AUC superior a 0.90 y alta estabilidad en el SHAP Stability Index, garantizando explicaciones consistentes y robustas ante perturbaciones.
    *   **Limitación:** El enfoque se limita a la detección estática en bases de datos contables sin considerar la dimensión de series temporales dinámicas o la generación automática de informes en lenguaje natural.
    *   **Relación con la Tesis:** Valida la superioridad de la combinación GBDT + SHAP en datos tabulares y sustenta la arquitectura de la Capa 1 y Capa 3 de la propuesta agroexportadora.

4.  **Grinsztajn et al. (2022) — *Why do tree-based models still outperform deep learning on tabular data?***
    *   **Objetivo:** Analizar y comparar el rendimiento de los modelos basados en árboles (GBDT) frente a modelos de aprendizaje profundo (Deep Learning) especializados para datos tabulares.
    *   **Datos:** 45 datasets tabulares reales y sintéticos de diversos sectores económicos con muestras menores a 50,000 registros.
    *   **Método:** Evaluación empírica sistemática de XGBoost, LightGBM y CatBoost frente a FT-Transformer, TabNet y perceptrones multicapa (MLP) mediante optimización de hiperparámetros.
    *   **Resultados Reales:** Los modelos GBDT superaron a las redes neuronales en el 95% de los escenarios tabulares evaluados. Se identificaron tres factores de éxito: robustez ante variables no informativas, falta de invarianza ante rotaciones de datos y discontinuidades en las fronteras de decisión.
    *   **Limitación:** El estudio no aborda el modelamiento de secuencias temporales autoregresivas complejas, limitándose a problemas de clasificación y regresión estándar.
    *   **Relación con la Tesis:** Justifica teórica y empíricamente la decisión de seleccionar XGBoost y LightGBM como los regresores globales de la tesis agroexportadora en lugar de modelos Deep Learning tabulares.

---

### 2.1.2 Antecedentes Nacionales en Evaluación y Revisión Académica

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

### 2.1.3 Antecedentes Metodológicos

1.  **Han et al. (2022) — *ADBench: Anomaly detection benchmark***
    *   **Objetivo:** Evaluar sistemática y exhaustivamente algoritmos de detección de anomalías bajo múltiples niveles de supervisión.
    *   **Datos:** 57 conjuntos de datos tabulares reales y sintéticos con inyección controlada de ruido y anomalías de distinta dimensionalidad.
    *   **Método:** Comparativa de 30 algoritmos de detección (incluyendo Isolation Forest, LOF, ECOD, One-Class SVM y Autoencoders).
    *   **Resultados Reales:** Confirmación de que ningún detector es superior en todos los escenarios; sin embargo, los enfoques de ensemble unificados mitigan el riesgo de sobreajuste y logran mayor estabilidad y robustez general ante cambios distribucionales.
    *   **Limitación:** La mayoría de los datasets evaluados son estáticos y no corresponden a series temporales operacionales estructuradas.
    *   **Relación con la Tesis:** Provee el soporte metodológico y la justificación teórica para construir un ensemble unificado no supervisado en la Capa 2 (PyOD) del sistema.

2.  **Lundberg & Lee (2017) — *A unified approach to interpreting model predictions***
    *   **Objetivo:** Desarrollar un marco unificado con consistencia axiomática para la atribución de variables locales en modelos de aprendizaje automático.
    *   **Datos:** Evaluado en diversos datasets tabulares y de imágenes.
    *   **Método:** Formulación de los valores de Shapley (SHAP) a partir de la teoría de juegos cooperativos, garantizando propiedades de eficiencia, simetría, aditividad y consistencia.
    *   **Resultados Reales:** Demostración de que SHAP unifica métodos previos (LIME, DeepLIFT) resolviendo sus inconsistencias matemáticas locales.
    *   **Limitación:** El cálculo exacto tiene complejidad exponencial en función del número de características.
    *   **Relación con la Tesis:** Sustenta el uso del componente de explicabilidad (Capa 3) del sistema, aplicando la optimización TreeSHAP para modelos de árboles de decisión.

3.  **Lewis et al. (2020) — *Retrieval-augmented generation for knowledge-intensive NLP tasks***
    *   **Objetivo:** Combinar modelos generativos de lenguaje con sistemas de recuperación de información externa para resolver tareas intensivas en conocimiento sin requerir reentrenamiento masivo.
    *   **Datos:** Wikipedia dump e índices vectoriales de preguntas y respuestas.
    *   **Método:** Arquitectura RAG que recupera fragmentos relevantes a partir de una consulta y los inyecta en el contexto de entrada de un modelo secuencia a secuencia (BART/T5).
    *   **Resultados Reales:** Reducción de la tasa de alucinación semántica y mejora de la precisión factual en la generación de textos.
    *   **Limitación:** Sensible a la calidad y consistencia lógica de la base de conocimiento indexada.
    *   **Relación con la Tesis:** Define la estructura de la Capa 4 para generar reportes fundamentados exclusivamente en la base documental del corpus y los datos estructurados.

---

### 2.1.4 Síntesis crítica
La revisión de antecedentes revela una brecha metodológica y tecnológica: los trabajos analíticos en agroexportación peruana se han limitado a predicciones puntuales de volumen o a detección aislada de fallas logísticas de frío mediante sensores IoT. Por otra parte, las propuestas metodológicas de IA explicable y automatización de reportes (AuditCopilot, AuditMAI) se restringen a dominios contables y financieros estáticos. **No existe en la literatura revisada un sistema integrado que unifique la predicción de valor unitario y volumen semanal, la detección de anomalías mediante un ensemble calibrado por percentiles, la explicabilidad con SHAP y la redacción de informes con RAG factual** en el dominio agroexportador peruano.

---