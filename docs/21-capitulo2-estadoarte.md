## 2.2 Estado del Arte

El estado del arte se organiza en torno a cinco debates fundamentales de la literatura que la presente propuesta debe resolver o posicionarse explícitamente. Cada sub-sección presenta el debate, los trabajos relevantes y la posición de esta tesis. La Tabla 2.1 sintetiza todas las referencias relevantes al final de la sección.

### 2.2.1 GBDT versus Deep Learning para Datos Tabulares Empresariales y Agroexportadores

El desarrollo de modelos para datos tabulares ha seguido una trayectoria diferente a la de visión computacional y procesamiento de lenguaje natural: el Deep Learning no ha conseguido desplazar a los modelos basados en árboles como estándar de facto en datos estructurados. Chen y Guestrin (2016) introdujeron XGBoost como sistema escalable de gradient boosting con regularización L1/L2, manejo nativo de valores faltantes y paralelización por columnas, estableciéndolo como el baseline universal con más de 45,000 citas en la literatura científica. Ke et al. (2017) lo extendieron con LightGBM, que incorpora Gradient-based One-Side Sampling (GOSS) e histogramas para lograr velocidades de entrenamiento hasta 20 veces superiores con rendimiento comparable. Prokhorenkova et al. (2018) resolvieron el problema de target leakage en variables categóricas con Ordered Boosting, siendo especialmente relevante en datos contables con alta cardinalidad (cuentas, departamentos, centros de costo).

El auge del Deep Learning motivó intentos de adaptar estas arquitecturas a datos tabulares. Gorishniy et al. (2021) propusieron FT-Transformer, el primer Transformer robusto para tablas mediante feature embeddings, que en algunos benchmarks iguala pero raramente supera a los GBDT. Arik y Pfister (2021) desarrollaron TabNet, que combina selección secuencial de features con atención interpretable, argumentando que puede ofrecer tanto rendimiento como interpretabilidad en un solo modelo. Sin embargo, el estudio seminal de Grinsztajn et al. (2022), con un benchmark en 45 datasets y hasta 50,000 muestras, zanjó empíricamente este debate: los GBDT superan a todo modelo de Deep Learning en el 95% de los casos para datasets de tamaño empresarial mediano. Los autores identifican tres propiedades estructurales de los datos tabulares que favorecen a los árboles: robustez ante features no informativas, orientación no invariante a rotaciones y presencia de irregularidades en la función objetivo —todas características presentes en los registros transaccionales de auditoría.

En dominios empresariales con datos tabulares heterogéneos, esta evidencia respalda el uso de GBDT como primera opción antes de recurrir a arquitecturas neuronales complejas. En el caso agroexportador, los registros combinan variables numéricas, categóricas, temporales y contextuales —producto, zona, volumen, precio, clima, destino, cumplimiento y logística—, por lo que los modelos basados en árboles son una base técnica adecuada para capturar relaciones no lineales y manejar variables de distinta naturaleza.

**Posición de esta tesis**: XGBoost y LightGBM constituyen el backbone del módulo de predicción tabular. TabNet y FT-Transformer se evalúan como baselines comparativos, no como propuesta principal, dado que la evidencia empírica no justifica su adopción en el contexto de tamaño del dataset empresarial analizado.

### 2.2.2 Detector Único versus Ensemble para Detección de Anomalías

El campo de la detección de anomalías cuenta con una historia de más de dos décadas de métodos en competencia. Breunig et al. (2000) establecieron el Local Outlier Factor (LOF) como referencia para detectar anomalías locales mediante densidad relativa al vecindario k-NN, un enfoque sensible a variaciones locales que permite identificar transacciones con patrones de comportamiento heterogéneos. Liu et al. (2008) revolucionaron el campo con Isolation Forest, que aísla anomalías por particionamiento aleatorio sin necesidad de definir perfiles de normalidad, con complejidad O(n) que lo hace viable en millones de transacciones diarias. Ruff et al. (2018) extendieron la detección a espacios de representación profundos con Deep SVDD, capturando patrones no lineales en los datos mediante redes neuronales. Li et al. (2022) propusieron ECOD, un detector moderno libre de parámetros basado en distribución empírica acumulada que supera a 11 baselines en datasets no supervisados, eliminando el riesgo de sobreajuste al proceso de calibración.

El hallazgo central de Han et al. (2022) en ADBench —57 datasets, 30 algoritmos, tres niveles de supervisión— establece que no existe un algoritmo universalmente superior: el rendimiento depende fuertemente del tipo de anomalía, la distribución de los datos y el nivel de etiquetado disponible. Esta conclusión teórica valida la estrategia de ensemble como la opción más robusta para entornos de producción donde la distribución de anomalías es desconocida a priori. La librería PyOD (Zhao et al., 2019) proporciona la infraestructura técnica para implementar este ensemble de manera estandarizada y reproducible.

**Posición de esta tesis**: El ensemble Isolation Forest + LOF + Deep SVDD (coordinado mediante PyOD) es más robusto que cualquier detector individual. Esta decisión está respaldada por ADBench (Han et al., 2022) como fundamento teórico.

### 2.2.3 LLM como Detector versus LLM como Generador de Reportes

El surgimiento de los LLMs ha generado propuestas de integración en sistemas empresariales con distintos roles. Hegselmann et al. (2023) demostraron con TabLLM que los LLMs pueden clasificar datos tabulares en configuración zero/few-shot mediante serialización a texto, con rendimiento no trivial incluso sin ajuste fino. Park (2024) llevó esta lógica más lejos con un framework multi-agente donde LLMs especializados validan alertas de anomalías. Estos antecedentes muestran potencial metodológico, aunque no resuelven por sí mismos el problema de trazabilidad operativa agroexportadora.

Sin embargo, existe evidencia sustancial de que usar LLMs como detectores o tomadores de decisiones introduce riesgos inaceptables. El survey sobre alucinaciones en LLMs (Maynez et al., 2026) documenta que los modelos pueden generar razonamiento coherente en forma pero incorrecto en contenido, con alta confianza aparente. Este riesgo es especialmente importante en reportes operativos, donde una cifra o causa inventada puede inducir decisiones equivocadas.

La arquitectura RAG (Schneider et al., 2025 (Schneider et al., 2025)) ofrece una solución al anclar las respuestas del LLM a bases de conocimiento verificadas —en este caso, scores, umbrales, vectores SHAP y fuentes agroexportadoras recuperadas— reduciendo el espacio de alucinación al forzar al modelo a narrar únicamente lo que los datos cuantitativos establecen. El LLM no infiere anomalías; las narra con evidencias como fundamento.

**Posición de esta tesis**: El LLM se restringe estrictamente a la capa de generación de reportes mediante RAG. La detección, cuantificación y explicación son realizadas por modelos y evidencias estructuradas (GBDT + ensemble + SHAP). Esta separación se alinea con principios de transparencia, supervisión humana y trazabilidad promovidos por marcos como el D.S. N° 115-2025-PCM (PCM, 2025), el EU AI Act (Parlamento Europeo y Consejo, 2024) y el NIST AI RMF (NIST, 2023).

### 2.2.4 Sistemas Aislados versus Sistema Integrado de Supervisión Operativa Continua

La revisión de la literatura evidencia una fragmentación sistemática en los sistemas de supervisión asistida por IA. Los trabajos pueden agruparse en cuatro categorías según el módulo que abordan: (1) sistemas de predicción tabular (Chen & Guestrin, 2016; Ke et al., 2017; Prokhorenkova et al., 2018); (2) sistemas de forecasting y series temporales (Lim et al., 2021; Challu et al., 2022); (3) sistemas de detección de anomalías (Liu et al., 2008; Han et al., 2022); y (4) sistemas de generación de reportes con LLMs (Kadir et al., 2025; Park, 2024).

Trabajos como AuditCopilot (Kadir et al., 2025) logran una integración parcial al combinar detección de anomalías con generación de reportes LLM, pero operan en dominio contable y no abordan supervisión agroexportadora. El framework de Park (2024) integra múltiples LLMs pero opera en mercados financieros de alta frecuencia. AuditMAI (Waltersdorfer et al., 2024) propone una infraestructura conceptual para auditoría continua de sistemas de IA. La Tabla 2.2 resume comparativamente los sistemas más cercanos a la propuesta de esta tesis desde una perspectiva metodológica.

**Posición de esta tesis**: Esta investigación cierra la brecha de integración al proponer y evaluar una arquitectura modular de cuatro capas que combina predicción tabular, detección de anomalías, explicabilidad SHAP y generación de reportes LLM-RAG con restricción anti-alucinación, aplicada a supervisión operativa agroexportadora. BAF (Jesus et al., 2022) se utiliza solo como benchmark metodológico complementario; la validación principal se orienta a datos agroexportadores públicos y sintéticos.

### 2.2.5 Contexto Regulatorio Internacional versus Perú

La mayoría de marcos de gobernanza de IA de la literatura operan en contextos regulatorios de EE.UU. (NIST AI RMF (NIST, 2023)), Europa (EU AI Act (Parlamento Europeo y Consejo, 2024), GDPR) o Asia. Estos marcos coinciden en principios relevantes para esta tesis: documentación, transparencia, supervisión humana, gestión de riesgos y trazabilidad.

En el contexto peruano, el marco regulatorio ha madurado significativamente en 2023–2025. La Resolución SBS N° 053-2023 establece lineamientos de gobernanza, trazabilidad y explicabilidad para modelos de riesgo en entidades supervisadas por la SBS (SBS, 2023), por lo que se adopta aquí solo como referencia de buenas prácticas. El Decreto Supremo N° 115-2025-PCM, reglamento de la Ley N° 31814, proporciona un marco nacional general para promover el uso responsable de la inteligencia artificial (PCM, 2025). A nivel internacional, el EU AI Act (Parlamento Europeo y Consejo, 2024) refuerza obligaciones de transparencia y documentación para sistemas de IA.

**Posición de esta tesis**: Esta investigación diseña un sistema de supervisión operativa agroexportadora que incorpora principios de gobernanza, trazabilidad, documentación y supervisión humana. El D.S. N° 115-2025-PCM se adopta como marco peruano general de IA responsable, mientras que la Resolución SBS N° 053-2023 se utiliza solo como referencia nacional de gestión de riesgo de modelos.

### 2.2.6 Síntesis y Tabla del Estado del Arte

La revisión sistemática de los bloques temáticos permite identificar la brecha de investigación central: **no existe en la literatura revisada un sistema orientado al contexto agroexportador peruano que integre de manera modular, con evaluación reproducible y trazabilidad explícita, los cuatro componentes**: predicción tabular, detección de anomalías, explicabilidad SHAP y generación de reportes LLM-RAG basada en evidencias. Esta tesis propone y evalúa dicha integración para supervisión operativa agroexportadora.

**Tabla 2.1 — Comparativa de Sistemas de Supervisión con IA**

| Característica | **Esta tesis** | AuditCopilot (Kadir et al., 2025) | Park 2024 (Park, 2024) | AuditMAI (Waltersdorfer et al., 2024) | (JRFM, 2025) |
|---|---|---|---|---|---|
| Predicción tabular GBDT | ✅ XGB+LGBM+CatBoost | ❌ | ❌ Solo LLMs | ❌ | ✅ Stacking |
| Benchmark público reproducible | ✅ Datos públicos + sintéticos agroexportadores; BAF complementario | ❌ Dataset propio | ❌ S&P 500 | ❌ Conceptual | ⚠️ Dataset propio |
| Forecasting series temporales (TFT) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Ensemble de anomalías (ADBench) | ✅ IF+LOF+SVDD | ⚠️ Parcial | ❌ | ❌ | ❌ |
| Explicabilidad SHAP | ✅ TreeSHAP | ❌ | ❌ | ❌ | ✅ SHAP+Anchor |
| Generación LLM de reportes | ✅ RAG determinista | ✅ LLM narrativo | ✅ Multi-agente | ❌ | ❌ |
| Restricción anti-alucinación (RAG+SHAP) | ✅ | ❌ | ❌ | — | — |
| Marco de gobernanza explícito | ✅ DS115+NIST+EU AI Act; SBS como referencia | ❌ | ❌ | ❌ | ❌ |
| Contexto peruano | ✅ Agroexportación peruana | ❌ | ❌ | ❌ | ❌ |
| Evaluación con supervisores/evaluadores | ✅ | ❌ | ❌ | ❌ | ❌ |
| Dominio | Supervisión operativa agroexportadora | Asientos contables | Mercados bursátiles | Auditoría de IA | Fraude en EEFF |

**Tabla 2.2 — Resumen del Estado del Arte**

| N° | Autor(es) | Año | Aporte principal |
|:---:|-----------|:---:|-----------------|
| 1 | Chen & Guestrin (Chen & Guestrin, 2016) | 2016 | XGBoost: gradient boosting escalable con regularización L1/L2, benchmark universal para datos tabulares |
| 2 | Ke et al. (Ke et al., 2017) | 2017 | LightGBM: GOSS + histogramas, 20× más rápido que XGBoost con precisión comparable |
| 3 | Prokhorenkova et al. (Prokhorenkova et al., 2018) | 2018 | CatBoost: Ordered Boosting elimina target leakage en variables categóricas de alta cardinalidad |
| 4 | Gorishniy et al. (Gorishniy et al., 2021) | 2021 | FT-Transformer: primer Transformer robusto para datos tabulares mediante feature embeddings |
| 5 | Arik & Pfister (Arik & Pfister, 2021) | 2021 | TabNet: atención secuencial interpretable para tablas, combina rendimiento e interpretabilidad |
| 6 | Grinsztajn et al. (Grinsztajn et al., 2022) | 2022 | GBDT supera a DL en el 95% de datasets ≤50K muestras; cierra el debate en contexto empresarial |
| 7 | Lim et al. (Lim et al., 2021) | 2021 | TFT: forecasting multi-horizonte con gating de covariables e interpretabilidad incorporada |
| 8 | Liu et al. (Liu et al., 2008) | 2008 | Isolation Forest: aislamiento aleatorio O(n), sin perfil de normalidad, escalable a millones de registros |
| 9 | Breunig et al. (Breunig et al., 2000) | 2000 | LOF: densidad local relativa k-NN, detecta anomalías locales heterogéneas |
| 10 | Ruff et al. (Ruff et al., 2018) | 2018 | Deep SVDD: detección one-class en espacio latente profundo para patrones no lineales |
| 11 | Han et al. (Han et al., 2022) | 2022 | ADBench: benchmark de 30 algoritmos en 57 datasets; ensembles son más robustos que detectores únicos |
| 12 | Lundberg & Lee (Lundberg & Lee, 2017) | 2017 | SHAP: valores Shapley con consistencia axiomática; TreeSHAP exacto para GBDT |
| 13 | Kadir et al. (Kadir et al., 2025) | 2025 | AuditCopilot: LLM+detección en asientos contables; antecedente metodológico para reportes automáticos |
| 14 | Park (Park, 2024) | 2024 | Framework multi-agente LLM para validar anomalías en mercados bursátiles |
| 15 | Schneider et al. (Schneider et al., 2025) | 2025 | RAG avanzado para BI organizacional; arquitectura anti-alucinación base de esta tesis |
| 16 | SBS Perú (SBS, 2023) | 2023 | Resolución N° 053-2023: referencia nacional de buenas prácticas para gestión de riesgo de modelos |

---

