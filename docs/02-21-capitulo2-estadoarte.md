# ESTADO DEL ARTE

## 2.2 Estado del Arte

El estado del arte de la investigación se estructura a partir de los siguientes debates científicos de la disciplina:

### 2.2.1 Modelos GBDT frente a Aprendizaje Profundo Tabular
El modelado de datos estructurados empresariales se caracteriza por un debate continuo entre el uso de algoritmos basados en árboles (GBDT) y la adaptación de arquitecturas de aprendizaje profundo (como Transformers tabulares o TabNet). Trabajos como FT-Transformer (Gorishniy et al., 2021) y TabNet (Arik & Pfister, 2021) proponen que los mecanismos de atención capturan relaciones de alta dimensionalidad. Sin embargo, la evidencia sistemática aportada por Grinsztajn et al. (2022) demuestra que para conjuntos de datos empresariales de tamaño moderado ($\le 50,000$ filas), los GBDT (XGBoost y LightGBM) superan a las redes neuronales en precisión, velocidad de entrenamiento y robustez ante características no informativas. La presente tesis adopta esta posición, utilizando XGBoost y LightGBM como base predictiva de la propuesta.

### 2.2.2 Detector Único frente a Ensemble de Anomalías
En la detección de outliers, el debate gira en torno a si un único detector optimizado (como Isolation Forest o LOF) es suficiente frente a un ensemble multi-algoritmo. La investigación de Han et al. (2022) en ADBench concluye que ningún detector domina todos los patrones de desviación, ya que Isolation Forest destaca en outliers globales por aislamiento espacial, LOF en anomalías locales por densidad de vecindario, y ECOD en colas de distribuciones estadísticas. En consecuencia, el diseño de ensembles calibrados por percentiles es la alternativa recomendada en el estado del arte para garantizar estabilidad ante patrones de anomalía desconocidos, enfoque que es implementado en este prototipo.

### 2.2.3 Predicción Esperada y Residuos
La detección tradicional de anomalías suele aplicarse directamente sobre los datos observados en bruto. No obstante, el estado del arte de la supervisión continua sugiere que es más efectivo modelar las desviaciones operativas calculando los **residuos predictivos** (la diferencia entre el valor real observado y el valor esperado estimado por un modelo predictivo robusto). El cálculo de residuos robustos escalados mediante la desviación absoluta de la mediana (MAD) móvil de 13 semanas permite desacoplar los ciclos estacionales naturales de las anomalías operativas genuinas.

### 2.2.4 SHAP y Explicabilidad
La interpretabilidad algorítmica opone a los métodos agnósticos locales como LIME (Ribeiro et al., 2016) frente a formulaciones de la teoría de juegos como SHAP (Lundberg & Lee, 2017). Mientras que LIME construye modelos lineales locales que pueden resultar inestables ante pequeñas perturbaciones de datos, SHAP garantiza consistencia axiomática e invarianza, asegurando que si una variable incrementa su impacto, su valor asignado no disminuye. La formulación TreeSHAP permite el cálculo exacto de las atribuciones locales en tiempo polinómico sobre modelos GBDT, posicionándolo como el estándar de explicabilidad post-hoc.

### 2.2.5 LLM como Detector frente a LLM como Redactor
La emergencia de los modelos de lenguaje de gran tamaño (LLMs) ha motivado propuestas para utilizarlos directamente como clasificadores o detectores de anomalías sobre datos tabulares serializados a texto (Hegselmann et al., 2023). No obstante, el estado del arte advierte sobre el riesgo crítico de alucinaciones intrínsecas y numéricas en tareas lógicas cuantitativas (Maynez et al., 2026). Por ello, el consenso metodológico orienta el uso del LLM exclusivamente a la capa de redacción formal de informes, restringiendo su entrada a un prompt estructurado de evidencias provenientes de modelos matemáticos validados.

### 2.2.6 RAG y Control Factual
La generación de reportes corporativos mediante LLMs requiere mitigar alucinaciones y asegurar consistencia. La arquitectura RAG (Retrieval-Augmented Generation) (Lewis et al., 2020) resuelve esta brecha al alimentar el prompt con documentos y evidencias recuperados. Sin embargo, para entornos de auditoría, se requiere una capa complementaria de **validación factual determinista** que extraiga de forma automatizada las cifras textuales generadas por el modelo y las contraste contra el objeto JSON de evidencias, aplicando tolerancias estrictas por redondeo y cayendo en plantillas predefinidas ante fallos reiterados.

### 2.2.7 Arquitecturas Aisladas frente a Integradas
La literatura científica se encuentra fragmentada: existen sistemas que resuelven forecasting temporal de precios, otros orientados a la detección de outliers, y herramientas independientes de explicabilidad o reporte. La brecha de investigación radica en la falta de arquitecturas integradas y secuenciales que comuniquen de forma estructurada los componentes analíticos, asegurando el linaje desde el microdato transaccional hasta el informe técnico de auditoría.

### 2.2.8 Gobernanza de IA y Trazabilidad
El despliegue de sistemas inteligentes se enfrenta a exigencias de gobernanza corporativa y rendición de cuentas, reguladas por marcos nacionales como el Decreto Supremo N° 115-2025-PCM (Gobernanza y Supervisión Humana en Perú) y metodologías internacionales como el NIST AI Risk Management Framework (AI RMF 1.0) y las directrices de la Resolución SBS N° 053-2023 para riesgos de modelos. El estado del arte exige que cada alerta sea reproducible mediante marcas de tiempo, identificadores únicos y firmas SHA-256 de todas las fases del procesamiento.

---