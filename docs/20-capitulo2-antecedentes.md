# CAPÍTULO II: MARCO TEÓRICO

## 2.1 Antecedentes de la Investigación

Los antecedentes de esta investigación se organizan desde dos perspectivas. La primera corresponde a trabajos técnicos sobre datos tabulares, detección de anomalías, explicabilidad y generación de reportes, incluso cuando fueron desarrollados en dominios financieros o contables. Estos trabajos se utilizan como soporte metodológico. La segunda corresponde al dominio de aplicación de esta tesis: supervisión operativa agroexportadora, donde la contribución principal consiste en adaptar e integrar dichas técnicas para detectar, explicar y documentar desviaciones en procesos agroexportadores peruanos.

El desarrollo de sistemas de predicción, detección de anomalías y generación de reportes en datos empresariales ha seguido una trayectoria de especialización creciente, marcada por tres tendencias paralelas: el auge de los modelos basados en árboles para datos tabulares, la proliferación de benchmarks sistemáticos y la emergencia de los modelos de lenguaje como capa de interpretación. Los siguientes antecedentes fueron seleccionados por su proximidad metodológica con la propuesta de esta investigación, aunque varios provienen de dominios financieros o contables y se emplean aquí solo como soporte técnico transferible.

### 2.1.1 Kadir et al. (2025) — AuditCopilot: LLMs para Reportes de Anomalías

Kadir et al. (2025) desarrollaron AuditCopilot (Kadir et al., 2025), un sistema de auditoría contable que integra LLMs con detección de anomalías en asientos de doble entrada para generar explicaciones automáticas en lenguaje natural. El sistema implementa un pipeline de tres etapas —detección de irregularidades, interpretación contextual con LLM ajustado y generación de narrativas— evaluado sobre un corpus de asientos contables sintéticos y reales. Los resultados reportan mejoras en la tasa de detección y reducción del tiempo de revisión, con valoración positiva de auditores en pruebas de aceptabilidad.

La relevancia de este antecedente para la presente tesis es metodológica: confirma la viabilidad de combinar detección de anomalías con generación de reportes LLM. No obstante, su dominio es contable, por lo que no se adopta como evidencia agroexportadora. Esta tesis traslada el principio de generación narrativa a un contexto operativo, separando estrictamente la detección de la redacción mediante RAG sobre scores y vectores SHAP.

### 2.1.2 Park (2024) — Framework Multi-Agente LLM para Anomalías Financieras

Park (2024) propuso un framework de múltiples agentes LLM especializados para validar alertas de anomalías en el mercado bursátil (S&P 500) (Park, 2024). La arquitectura organiza cuatro agentes —conversión de datos, análisis estadístico, verificación cruzada y consolidación— que se comunican mediante prompts estructurados y alcanzan mejores tasas de verdaderos positivos que un LLM único. La especialización de agentes demuestra ser superior a la generalización en la validación de señales financieras.

Este trabajo aporta a la literatura evidencia de que los LLMs en arquitecturas especializadas pueden mejorar la calidad del análisis automatizado. Sin embargo, opera en mercados de alta frecuencia, un dominio alejado del contexto agroexportador. Esta tesis aplica únicamente el principio de especialización de roles —LLM como intérprete, no como detector— en un sistema de supervisión operativa con trazabilidad y generación restringida a datos verificados (Schneider et al., 2025).

### 2.1.3 Autores varios (2025) — Ensemble GBDT+SHAP en Datos Tabulares Críticos

En el trabajo publicado en el *Journal of Risk and Financial Management* (2025), los autores diseñaron un framework integrado de detección de fraude en estados financieros combinando Stacking Ensemble de XGBoost, LightGBM y CatBoost con explicabilidad SHAP (JRFM, 2025). El ensemble alcanza PR-AUC = 0.93 y F1-Score = 0.83, superando a TabNet y FT-Transformer, con un SHAP Stability Index = 0.87 que certifica la coherencia forense de las explicaciones —requisito indispensable en auditoría.

Este antecedente respalda la decisión arquitectónica de combinar GBDT y SHAP en datos tabulares críticos. La diferencia clave es que dicho trabajo se limita a detección de fraude en estados financieros; la presente investigación adapta la lógica de modelos tabulares explicables al contexto agroexportador, incorporando fuentes públicas, dataset sintético documentado y generación de reportes LLM+RAG para supervisión operativa.

### 2.1.4 Han et al. (2022) — ADBench: Benchmark para Detección de Anomalías

Han et al. (2022) publicaron ADBench (Han et al., 2022), un benchmark sistemático que evalúa 30 algoritmos de detección de anomalías en 57 datasets reales y sintéticos bajo tres niveles de supervisión —no supervisado, semisupervisado y supervisado. El hallazgo central es que no existe un algoritmo universalmente superior: el rendimiento depende del tipo de anomalía, la distribución de datos y el nivel de etiquetado. Isolation Forest y ECOD muestran consistencia en escenarios no supervisados, y los ensembles de múltiples detectores superan sistemáticamente a los detectores individuales en escenarios de alta variabilidad distribucional.

ADBench justifica formalmente la estrategia de ensemble adoptada en esta tesis y proporciona la metodología experimental de referencia para el Capítulo III. La librería PyOD (Zhao et al., 2019), compatible con todos los algoritmos evaluados en ADBench, asegura la reproducibilidad directa de los resultados.

### 2.1.5 Grinsztajn et al. (2022) — GBDT vs. Deep Learning en Datos Tabulares

Grinsztajn et al. (2022) realizaron un benchmark sistemático en 45 datasets tabulares comparando GBDT contra FT-Transformer, TabNet y MLP (Grinsztajn et al., 2022). El resultado es contundente: en datasets con menos de 50,000 muestras, los GBDT superan a cualquier modelo de Deep Learning en el 95% de los casos. Los autores identifican tres propiedades estructurales de los datos tabulares que favorecen a los árboles: robustez ante features no informativas, orientación no invariante a rotaciones e irregularidades en la función objetivo.

Este trabajo cierra el debate GBDT versus Deep Learning para el tamaño de dataset típico en entornos empresariales medianos y justifica de manera irrefutable la elección de XGBoost y LightGBM como backbone del módulo de predicción de esta tesis. Es el argumento bibliográfico central de la primera batalla del estado del arte (§2.2.1).

### 2.1.6 Lim et al. (2021) — Temporal Fusion Transformer para Forecasting Interpretable

Lim et al. (2021) propusieron el Temporal Fusion Transformer (TFT) (Lim et al., 2021), una arquitectura que combina codificación LSTM, selección de variables mediante mecanismo de gating, atención multi-cabezal interpretable y predicción por cuantiles para forecasting multi-horizonte con covariables exógenas. TFT supera a LSTMs, N-BEATS y Transformers vanilla en cuatro de seis datasets de referencia, con mapas de atención legibles por analistas de negocio.

TFT es seleccionado como arquitectura del módulo de forecasting por su doble ventaja: rendimiento predictivo e interpretabilidad incorporada. En el contexto de supervisión operativa, la capacidad de justificar qué períodos temporales y qué covariables (indicadores de producción, calendarios logísticos) fundamentan la predicción es un requisito funcional equivalente en importancia a la precisión numérica.

### 2.1.7 Zhao et al. (2019) — PyOD: Librería Estándar para Detección de Outliers

Zhao et al. (2019) desarrollaron PyOD (Zhao et al., 2019), una librería unificada en Python que implementa más de 40 algoritmos de detección de outliers con una API compatible con scikit-learn. Cubre métodos basados en proximidad (LOF), proyección (PCA), ensembles (Isolation Forest) y redes neuronales (Deep SVDD, AutoEncoder). Con más de 7,000 estrellas en GitHub y adopción en publicaciones de NeurIPS, ICDM e ICML, PyOD es la infraestructura técnica de referencia para implementar el ensemble de detección de anomalías de esta tesis, garantizando reproducibilidad directa con los 30 algoritmos de ADBench (Han et al., 2022).

---

