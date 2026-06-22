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

### 2.1.2 Antecedentes nacionales y evidencia sectorial verificable

Durante la revisión documental se identificó que algunos antecedentes nacionales usados en borradores previos no contaban todavía con trazabilidad bibliográfica suficiente para sostener autores, año, universidad, muestra y resultados cuantitativos. Por esa razón, esta versión no mantiene afirmaciones no verificadas como reducción de mermas, mejora porcentual de pronóstico o resultados de sensores IoT si no existe documento original localizado. La sección nacional se reestructura con fuentes institucionales verificables y con una lista explícita de antecedentes académicos pendientes de sustitución.

1. **MIDAGRI (2026) — Reporte sectorial de agroexportaciones peruanas**
   * **Objetivo documental:** Caracterizar el crecimiento reciente de la agroexportación peruana y ubicar la relevancia económica del sector.
   * **Datos:** Información institucional de ventas agroexportadoras y productos representativos reportada por el Ministerio de Desarrollo Agrario y Riego.
   * **Aporte a la tesis:** Sustenta el contexto económico que justifica priorizar productos agroexportadores de alta participación, especialmente palta, uva y arándano.
   * **Limitación:** No entrega microdatos transaccionales ni permite por sí sola evaluar modelos predictivos o detectores de anomalías.

2. **SUNAT/ADUANET (2026) — Bases y estadísticas aduaneras**
   * **Objetivo documental:** Proveer registros o series de comercio exterior que permiten reconstruir valor FOB, peso, subpartida, país de destino y periodo de exportación.
   * **Datos usados en el proyecto:** Descargas locales en `data/sunat/raw_downloads/`, `data/sunat/x23290326.DBF`, `data/raw/exports_raw.csv` y capas procesadas `data/bronze/`, `data/silver/` y `data/gold/`.
   * **Aporte a la tesis:** Constituye la fuente primaria para la unidad producto-mercado-semana y para las variables de valor FOB, volumen y destino.
   * **Limitación:** Las descargas locales completas disponibles se concentran en ventanas 2026; la cobertura 2018-2025 requiere documentar si proviene de dataset real local consolidado, fuentes agregadas o reconstrucción complementaria.

3. **BCRP (2018-2026) — Tipo de cambio PEN/USD**
   * **Objetivo documental:** Incorporar una variable macroeconómica exógena para normalizar o contextualizar el comportamiento de valor exportado.
   * **Datos usados en el proyecto:** `data/bcrp/exchange_rates_cache.json` y `data/downloads/bcrp_tipo_cambio.csv`.
   * **Aporte a la tesis:** Permite incluir contexto macroeconómico en los modelos de predicción y detectar semanas donde una desviación comercial puede coincidir con cambios cambiarios.
   * **Limitación:** La frecuencia mensual debe mapearse cuidadosamente a semana ISO sin usar información posterior a la semana objetivo.

4. **SISAP/MIDAGRI y Trade Map — Contexto de mercado interno e internacional**
   * **Objetivo documental:** Incorporar referencias externas de precios, volúmenes y mercados para contextualizar exportaciones por producto.
   * **Datos usados en el proyecto:** Manifiestos SISAP en `codex-revision/metadata/` y archivos Trade Map en `data-trademap/`.
   * **Aporte a la tesis:** Funcionan como fuentes de contraste y contexto, no como sustituto del registro aduanero.
   * **Limitación:** Operan con granularidades distintas al embarque aduanero; por tanto, su integración se declara como variable agregada o proxy.

5. **SENAMHI/NASA POWER y proxies climáticos**
   * **Objetivo documental:** Proveer contexto climático regional para productos perecederos.
   * **Datos usados en el proyecto:** Variables climáticas presentes en `data/dataset_real_v1.csv`, `data/silver/exports_clean.parquet` y `data/gold/weekly_product_market.parquet`.
   * **Aporte a la tesis:** Permiten evaluar si las semanas con mayor estrés climático agregado coinciden con cambios de volumen, valor unitario o anomalías.
   * **Limitación:** No prueban causalidad logística ni falla de cadena de frío por embarque; solo aportan contexto agregado.

**Antecedentes académicos nacionales pendientes de sustitución.** Los trabajos titulados provisionalmente "Modelos GBDT y clima para predicción agroexportadora peruana" y "Detección de anomalías IoT en cadenas de frío de perecederos" se retiran como evidencia académica cerrada hasta localizar documento original, repositorio, autores, institución, año, muestra y resultados. Si no se verifica su existencia, deberán reemplazarse por tesis o artículos reales encontrados en RENATI, Alicia/CONCYTEC, repositorios universitarios peruanos o revistas indizadas.

| Antecedente preliminar | Acción requerida | Estado en esta versión |
|---|---|---|
| Mendoza & Huamán (2024) | Localizar documento original y verificar resultados atribuidos | No usado como evidencia concluyente |
| Chávez & Díaz (2023) | Localizar documento original y verificar reducción de mermas atribuida | No usado como evidencia concluyente |
| Estudios nacionales de cadena de frío | Sustituir por documentos reales con repositorio y metodología verificable | Pendiente |
| Estudios nacionales de forecasting agroexportador | Sustituir por documentos reales con datos y métricas reproducibles | Pendiente |

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
