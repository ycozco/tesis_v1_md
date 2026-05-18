---
title: "Sistema Integrado de Auditoría Continua con IA: Predicción, Detección de Anomalías y Generación de Reportes Automáticos"
author: "Tu Nombre"
date: "2026-05-12"
bibliography: refs.bib
csl: apa.csl
---

# CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA

## 1.1 Descripción de la Realidad Problemática

### Contexto empresarial y financiero

En instituciones financieras (bancos, cooperativas, financieras), la auditoría de transacciones es crítica para detectar fraude, incumplimiento normativo y lavado de dinero. Actualmente, los sistemas de detección operan en silos: modelos de predicción (XGBoost), algoritmos de anomalías (Isolation Forest), y reportería manual o semiautomática.

La magnitud del problema es significativa: en contextos con millones de transacciones diarias, la auditoría manual es inviable. Sin embargo, sistemas automatizados sin explicabilidad erosionan confianza regulatoria y corporativa. Las autoridades (SBS en Perú, Basilea III a nivel internacional, NIST AI RMF) demandan audibilidad: ¿por qué el sistema tomó esta decisión?

### Problemas identificados

1. **Falta de integración**: Cada componente funciona independientemente; las decisiones del modelo no se comunican a los auditores con contexto completo.

2. **Baja explicabilidad**: Los modelos GBDT producen predicciones numéricas, pero sin explicación de por qué un cliente/transacción se marcó como anómala. Auditores requieren justificación clara para acciones.

3. **Reportería manual**: Los hallazgos de anomalías requieren redacción manual de reportes, con riesgo de inconsistencia, ineficiencia a escala e incumplimiento de SLA.

4. **Falta de trazabilidad regulatoria**: Reguladores demandan audibilidad end-to-end. Los silos no permiten rastrabilidad de decisiones automáticas.

5. **Ausencia de validación cruzada**: Las anomalías detectadas por un método no se validan contra múltiples perspectivas (temporal, comportamental, multidimensional).

6. **Riesgos de sesgo sin control**: Modelos no explicables pueden incrustar sesgos discriminatorios; sin explicabilidad, es difícil detectarlos.

## 1.2 Problema Principal

**¿Cómo diseñar e implementar un sistema integrado de auditoría continua que unifique predicción, detección de anomalías, explicabilidad y generación de reportes, manteniendo trazabilidad regulatoria y explicabilidad en cada componente, superior en usabilidad y confianza respecto a sistemas con componentes aislados?**

### Sub-problemas

- ¿Qué arquitectura modular minimiza acoplamiento entre componentes pero garantiza coherencia de decisiones?
- ¿Cuál es el trade-off entre precisión de detección y explicabilidad?
- ¿Cómo evaluar que reportes generados automáticamente son de calidad aceptable para auditores?
- ¿Es viable integrar LLMs en sistemas de auditoría financiera manteniendo trazabilidad?

## 1.3 Objetivos

### 1.3.1 Objetivo Principal

Diseñar, implementar y evaluar un sistema integrado de auditoría continua que combine predicción tabular, detección de anomalías mediante ensemble, explicabilidad mediante SHAP, y generación automática de reportes con LLMs en arquitectura RAG, demostrando que la integración produce mejor trazabilidad, usabilidad y confianza que sistemas aislados.

### 1.3.2 Objetivos Específicos

1. **Arquitectura y modularidad**: Definir una arquitectura en capas (predicción → detección → explicación → reporte) que separe responsabilidades según principios de gobernanza NIST AI RMF, permitiendo reemplazo de componentes sin breaking changes.

2. **Predicción y detección robusto**: Implementar pipeline de predicción (XGBoost/LightGBM) + ensemble de detectores (Isolation Forest, LOF, Deep SVDD) y demostrar superioridad respecto a métodos aislados usando BAF Benchmark (AUC ≥ 0.92).

3. **Explicabilidad verificable**: Integrar SHAP para generar explicaciones de decisiones del modelo; validar que top-3 features explican ≥70% de varianza por muestra.

4. **Generación de reportes de calidad**: Implementar componente LLM+RAG que traduzca anomalías + explicaciones SHAP a reportes en lenguaje natural; alcanzar ROUGE-1 ≥ 0.50 vs. referencia humana.

5. **Evaluación integrada y usabilidad**: Diseñar experimento comparativo (sistema integrado vs. componentes aislados) con métricas de tiempo-a-decisión (reducción ≥30%), confianza auditor (+1 punto escala 5), y precisión de decisiones.

## 1.4 Hipótesis de la Investigación

**Hipótesis General (H1)**: Un sistema integrado que combina predicción GBDT, detección de anomalías mediante ensemble, explicabilidad SHAP y generación de reportes con LLM+RAG produce mayor trazabilidad regulatoria, usabilidad y confianza en auditores que sistemas con componentes aislados.

**Hipótesis Nula (H0)**: No existe diferencia estadísticamente significativa entre sistema integrado y componentes aislados en trazabilidad, usabilidad o confianza.

**Sub-hipótesis**:
- H1a: El ensemble de anomalías (IF+LOF+SVDD) supera métodos aislados en robustez ante diversas distribuciones de datos.
- H1b: Explicaciones SHAP son suficientemente interpretables para auditores (coherencia ≥80% en evaluación cualitativa).
- H1c: Reportes LLM+RAG alcanzan calidad comparable a referencia humana (ROUGE-1 ≥0.50).
- H1d: Sistema integrado reduce tiempo-a-decisión ≥30% sin sacrificar precisión.

## 1.5 Variables e Indicadores

### 1.5.1 Variable Independiente

**Sistema de auditoría (categoría)**:
- VI1: Sistema integrado (predicción + detección + SHAP + LLM+RAG)
- VI2: Componentes aislados (baseline)

**Indicador**: Tipo de sistema utilizado (categórico: integrado vs. aislado)

### 1.5.2 Variables Dependientes

**VD1: Rendimiento de detección**
- Indicador: ROC-AUC, Precision, Recall, F1-score
- Métrica: Score numérico [0, 1]
- Rango aceptable: AUC ≥ 0.90

**VD2: Calidad de explicabilidad**
- Indicador: Coverage (% features en top-3), Consistency (coherencia cualitativa)
- Métrica: Porcentaje explicado, puntuación Likert 1-5
- Rango aceptable: Coverage ≥70%, Consistency ≥4

**VD3: Calidad de reportes**
- Indicador: ROUGE-1, ROUGE-L, coherencia, completitud
- Métrica: Score ROUGE [0, 1], evaluación manual
- Rango aceptable: ROUGE-1 ≥0.50

**VD4: Usabilidad y confianza**
- Indicador: Tiempo-a-decisión (segundos), confianza (Likert 1-5), precisión decisión
- Métrica: Δ tiempo, Δ confianza, % correcto
- Rango aceptable: Δ tiempo ≥30%, Δ confianza ≥+1, % correcto ≥85%

**VD5: Trazabilidad regulatoria**
- Indicador: Audibilidad de decisiones (escala NIST AI RMF), documentación
- Métrica: Cumplimiento con NIST RMF (Govern, Map, Measure, Manage)
- Rango aceptable: Cumplimiento ≥80% de requisitos

## 1.6 Viabilidad de la Investigación

### 1.6.1 Viabilidad Técnica

**✓ Disponibilidad de tecnologías**:
- Modelos GBDT: XGBoost, LightGBM, CatBoost (open-source, bien documentados)
- Detección anomalías: scikit-learn (IF, LOF), torch (Deep SVDD)
- Explicabilidad: SHAP library (estándar académico)
- LLMs: acceso a APIs (OpenAI, Anthropic) o modelos locales (Llama 2)
- Infraestructura: Python 3.9+, PyTorch/TensorFlow, Pandas

**✓ Datos disponibles**:
- BAF Benchmark (público, reproducible) para evaluación
- Posibilidad de acceso a datos anonimizados de institución financiera (confidencial)

**✓ Metodologías establecidas**:
- Pipelines ML maduros (scikit-learn, MLOps best practices)
- Evaluación estándar (ROC-AUC, ROUGE, métricas usabilidad)

**Riesgos técnicos identificados**:
- Latencia SHAP en datasets grandes (>1M filas): mitigación con approximation methods
- Variabilidad de LLMs: requerir fine-tuning y prompt engineering robusto
- **Mitigación**: Pruebas piloto con datos subconjunto, benchmarking iterativo

### 1.6.2 Viabilidad Operativa

**✓ Recursos humanos**:
- Investigador principal (diseño, implementación, análisis)
- Acceso a expertos en ML y auditoría (asesoría)
- Posibilidad de reclutamiento de auditores voluntarios para evaluación

**✓ Timeline realista**:
- Fase 1 (Meses 1-2): Preparación datos, implementación arquitectura base
- Fase 2 (Meses 2-3): Entrenamiento modelos, validación
- Fase 3 (Mes 4): Test de usabilidad con usuarios
- Fase 4 (Mes 5): Análisis, escritura, defensa

**✓ Acceso a datos**:
- BAF Benchmark es abierto (GitHub)
- Negociaciones en curso con institución financiera para dataset real

**Riesgos operativos**:
- Confidencialidad de datos financieros: requerir NDA, anonimización
- Disponibilidad de auditores para test: usar voluntarios o simulación

### 1.6.3 Viabilidad Económica

**✓ Presupuesto estimado**:
- Infraestructura (GPU cloud, APIs LLM): $500-1000 USD
- Licencias/herramientas: $0 (stack open-source)
- Incentivos participantes test: $200-300 USD
- **Total aprox.**: $800-1300 USD

**✓ Financiamiento disponible**:
- Becas de investigación universitaria
- Recursos propios del investigador
- Posible apoyo de institución financiera colaboradora

**Eficiencia costo-beneficio**:
- Bajo costo relativo comparado con impacto potencial (aplicación en producción)

## 1.7 Justificación e Importancia de la Investigación

### 1.7.1 Justificación Teórica

**Aporte a la literatura académica**:

Existe una brecha identificada en la literatura: no hay trabajos que unifiquen en una sola arquitectura verificada:
1. Predicción tabular (GBDT) + detección anomalías (ensemble) + explicabilidad (SHAP) + generación reportes (LLM+RAG)
2. Con énfasis en trazabilidad regulatoria (NIST AI RMF)
3. Con evaluación empírica de usabilidad en usuarios reales (auditores)

Esta tesis aporta:
- **Modelo conceptual** integrado documentado y evaluado
- **Validación empírica** de que integración > silos en contexto financiero
- **Guía de implementación** para instituciones financieras

### 1.7.2 Justificación Económica

**Potencial de mercado**:

Instituciones financieras enfrentan:
- Costo de auditoría manual: >$1M USD/año en grandes bancos (5000+ transacciones/día)
- Riesgo regulatorio: multas por incumplimiento (e.g., SBS Perú: hasta 3% ingresos)
- Oportunidad: automatización + explicabilidad reduce ambos

Sistema integrado podría:
- Reducir costo auditoría 40-50% mediante automatización
- Reducir riesgo regulatorio mediante trazabilidad
- ROI estimado: 18-24 meses en implementación

### 1.7.3 Justificación Social

**Impacto regulatorio y confianza**:

- Reguladores (SBS, Basilea III) demandan IA explicable en finanzas
- Confianza ciudadana en sistemas automáticos requiere transparencia
- Sistema integrado demuestra viabilidad de IA responsable en decisiones críticas

**Inclusión financiera**:

- Mejor detección fraude protege a usuarios vulnerables
- Reportería automatizada permite atender casos más rápidamente

### 1.7.4 Importancia

**Nivel académico**:
- Contribución a campos: ML interpretable, auditoría computarizada, gobernanza IA
- Potencial publicación en congresos (ICML, AAAI, FAccT) y revistas (IEEE TKDE, ACM TIST)

**Nivel profesional**:
- Guía de referencia para instituciones financieras adoptando IA
- Buenas prácticas documentadas en diseño modular, explicabilidad, gobernanza

**Nivel institucional**:
- Fortalece posicionamiento de universidad en IA responsable
- Establece colaboraciones con sector financiero

## 1.8 Alcance

**Alcance temático**:
- Predicción con GBDT, detección anomalías ensemble, explicabilidad SHAP, generación reportes LLM
- Marco de gobernanza NIST AI RMF
- **Excluye**: Deep learning puro, modelos de series temporales avanzados (fuera del scope), regulación detallada SBS

**Alcance geográfico**:
- Contexto de banco/institución financiera típica en América Latina (Perú, formato SBS)
- Datos sintéticos (BAF Benchmark) + posiblemente data anónima local

**Alcance temporal**:
- Evaluación en dataset static (no live monitoring en producción)
- Tiempo de estudio: 5 meses

**Alcance de usuarios**:
- Auditores de instituciones financieras (n=10-20 en test de usabilidad)
- Reguladores (audiencia secundaria para recomendaciones)

---

# CAPÍTULO II: MARCO TEÓRICO

## 2.1 Antecedentes de la Investigación

El desarrollo de sistemas de predicción, detección de anomalías y generación de reportes en entornos empresariales ha evolucionado significativamente en los últimos años, impulsado por avances en aprendizaje automático, modelado de series temporales y el uso emergente de modelos de lenguaje.

### Avances en modelos para datos tabulares

En el ámbito de los datos tabulares, diversos estudios han demostrado que los métodos basados en Gradient Boosting Decision Trees (GBDT) continúan siendo altamente competitivos. El modelo XGBoost [1] introdujo mejoras significativas en escalabilidad y rendimiento para grandes volúmenes de datos estructurados, mientras que LightGBM [2] optimizó el proceso de entrenamiento mediante técnicas como histogram-based learning y reducción de dimensionalidad. Por su parte, CatBoost [3] resolvió de manera eficiente el tratamiento de variables categóricas mediante codificación ordenada, evitando problemas de target leakage. Investigaciones más recientes han evaluado modelos profundos para datos tabulares, concluyendo que arquitecturas como FT-Transformer [4] pueden ser competitivas, aunque no superan consistentemente a los métodos basados en árboles en todos los escenarios [11].

### Series temporales y forecasting

En el campo del modelado de series temporales, los enfoques tradicionales continúan siendo relevantes. El método AutoARIMA [6] permite la selección automática de modelos estadísticos adecuados para forecasting, mientras que Prophet [7] facilita la modelación de estacionalidades y tendencias en entornos empresariales. Sin embargo, modelos más recientes como N-BEATS [8], N-HiTS [9] y Temporal Fusion Transformers [10] han demostrado mejoras en la predicción multi-horizonte y la incorporación de variables exógenas, lo cual resulta relevante para sistemas que requieren proyecciones complejas.

### Detección de anomalías

En cuanto a la detección de anomalías, el algoritmo Isolation Forest [11] ha sido ampliamente adoptado debido a su eficiencia y capacidad para detectar valores atípicos sin supervisión. Métodos clásicos como Local Outlier Factor (LOF) [12] permiten identificar anomalías basadas en densidad local, mientras que enfoques más recientes como Deep SVDD [13] extienden el problema a representaciones profundas. No obstante, estudios comparativos como ADBench [14] evidencian que no existe un algoritmo universalmente superior, y que el rendimiento depende del tipo de anomalía, la calidad de los datos y el nivel de supervisión disponible.

### Fraude y auditoría continua

En el contexto específico de fraude y auditoría, la literatura reciente destaca desafíos recurrentes como el desbalance extremo de clases, el concept drift y la necesidad de interpretabilidad en los modelos. Asimismo, se ha identificado una transición hacia sistemas de auditoría continua apoyados en inteligencia artificial, capaces de monitorear operaciones en tiempo real y detectar irregularidades de manera proactiva. En este sentido, el uso de datasets sintéticos como el Bank Account Fraud Benchmark [15] ha permitido simular condiciones reales de fraude, incluyendo sesgos y dinámica temporal.

### Modelos de lenguaje en auditoría

De manera complementaria, el uso de modelos de lenguaje (LLMs) ha comenzado a integrarse en tareas de análisis y detección de anomalías. Investigaciones recientes exploran su aplicación en datos tabulares [18] y en auditoría contable mediante sistemas como AuditCopilot [19], los cuales combinan detección automatizada con generación de explicaciones en lenguaje natural. Sin embargo, estos enfoques aún se consideran complementarios a los modelos tradicionales, especialmente en tareas críticas donde la trazabilidad y la precisión son fundamentales.

### Gobernanza y calidad en sistemas IA

Finalmente, el desarrollo de estos sistemas requiere considerar aspectos de gobernanza y calidad, alineados con marcos como el AI Risk Management Framework del NIST [20], así como prácticas de documentación como Datasheets for Datasets [22] y Model Cards [23], que permiten garantizar transparencia, reproducibilidad y control del sesgo en los modelos.

### Síntesis de antecedentes

En conjunto, estos antecedentes evidencian que la tendencia actual no se orienta hacia el uso de un único modelo, sino hacia arquitecturas híbridas que integran predicción, detección de anomalías y explicabilidad, soportadas por prácticas de MLOps y evaluación rigurosa. Este enfoque resulta particularmente relevante en entornos empresariales donde la toma de decisiones depende de la confiabilidad y trazabilidad de los resultados.

## 2.2 Estado del Arte

| # | Autor(es) | Año | Tema | Aporte |
|---|-----------|-----|------|--------|
| [1] | T. Chen y C. Guestrin | 2016 | Modelos Tabulares | XGBoost: modelo de boosting optimizado para datos tabulares, destacando por escalabilidad y rendimiento en problemas estructurados. |
| [2] | G. Ke et al. | 2017 | Modelos Tabulares | LightGBM: mejora en eficiencia de entrenamiento mediante histogramas y reducción de complejidad computacional. |
| [3] | L. Prokhorenkova et al. | 2018 | Modelos Tabulares | CatBoost: optimizado para variables categóricas, evitando fuga de información (target leakage). |
| [4] | Y. Gorishniy et al. | 2021 | Modelos Tabulares | FT-Transformer: arquitectura deep learning para datos tabulares, competitiva con GBDT en ciertos escenarios. |
| [6] | R. J. Hyndman y Y. Khandakar | 2008 | Series Temporales | AutoARIMA: método automático para selección de modelos de series temporales. |
| [7] | S. J. Taylor y B. Letham | 2017 | Series Temporales | Prophet: modelo robusto para forecasting con estacionalidad y tendencia en entornos empresariales. |
| [8] | B. N. Oreshkin et al. | 2020 | Series Temporales | N-BEATS: modelo profundo para series temporales con alta precisión en predicción multi-horizonte. |
| [9] | C. Challu et al. | 2023 | Series Temporales | N-HiTS: arquitectura optimizada para forecasting en horizontes largos. |
| [10] | B. Lim et al. | 2021 | Series Temporales | Temporal Fusion Transformer (TFT): modelo interpretable para predicción multi-horizonte. |
| [11] | F. T. Liu et al. | 2008 | Anomalías | Isolation Forest: algoritmo eficiente para detección de anomalías sin supervisión. |
| [12] | M. M. Breunig et al. | 2000 | Anomalías | LOF: método basado en densidad para detección de outliers locales. |
| [13] | L. Ruff et al. | 2018 | Anomalías | Deep SVDD: enfoque profundo para detección de anomalías en espacios complejos. |
| [14] | S. Han et al. | 2022 | Anomalías | ADBench: benchmark para evaluar algoritmos de detección de anomalías bajo distintos escenarios. |
| [15] | S. Jesus et al. | 2022 | Fraude Bancario | BAF Benchmark: dataset realista para evaluación de fraude financiero con drift temporal. |
| [16] | R. E. Machado et al. | 2024 | Fraude Detectión | Revisión sistemática sobre detección de fraude, identificando desafíos como desbalance y drift. |
| [17] | D. Leocádio et al. | 2024 | Auditoría IA | Marco conceptual de auditoría con IA, enfocándose en monitoreo continuo y soporte a decisiones. |
| [18] | C.-P. Tsai et al. | 2025 | LLMs Tabulares | Exploración de LLMs en detección de anomalías tabulares, ampliando enfoques tradicionales. |
| [19] | M. A. Kadir et al. | 2025 | Auditoría LLM | AuditCopilot: integración de LLMs en auditoría contable con generación de explicaciones. |
| [20] | NIST | 2023 | Gobernanza IA | AI Risk Management Framework: lineamientos de gobernanza, confiabilidad y riesgo en sistemas IA. |
| [21] | D. Sculley et al. | 2015 | MLOps | Hidden Technical Debt in ML Systems: análisis de complejidad operativa de sistemas ML. |
| [22] | T. Gebru et al. | 2021 | Documentación | Datasheets for Datasets: enfoque para documentar datasets y mejorar transparencia. |
| [23] | M. Mitchell et al. | 2019 | Documentación | Model Cards: documentación estructurada para modelos de ML. |

## 2.3 Marco Conceptual

El marco conceptual del presente estudio se sustenta en los principios del aprendizaje automático, análisis de datos y sistemas inteligentes aplicados a entornos empresariales. Se abordan los conceptos clave necesarios para comprender el diseño de un sistema híbrido orientado a la predicción, detección de anomalías y generación de reportes.

### 2.3.1 Reconocimiento de patrones

El reconocimiento de patrones es un campo fundamental dentro de la inteligencia artificial que se encarga de identificar regularidades, estructuras o relaciones en los datos. Este proceso permite transformar datos crudos en información útil mediante la identificación de tendencias y comportamientos recurrentes.

En el contexto del aprendizaje automático, el reconocimiento de patrones se realiza a través de modelos que aprenden funciones a partir de datos históricos, permitiendo generalizar hacia nuevos datos no observados. Este proceso es la base para tareas como clasificación, regresión y detección de anomalías [16].

### 2.3.2 Aprendizaje automático (Machine Learning)

El aprendizaje automático es una disciplina que permite a los sistemas mejorar su desempeño mediante la experiencia, es decir, a través del análisis de datos. Se clasifica en tres tipos principales:

- **Aprendizaje supervisado**: Utiliza datos etiquetados para entrenar modelos predictivos.
- **Aprendizaje no supervisado**: Identifica patrones sin necesidad de etiquetas.
- **Aprendizaje semi-supervisado**: Combina ambos enfoques cuando las etiquetas son limitadas.

Estos enfoques son ampliamente utilizados en aplicaciones empresariales como análisis de clientes, predicción de demanda y detección de fraude [16].

### 2.3.3 Modelos basados en árboles y Gradient Boosting

Los modelos basados en árboles de decisión son ampliamente utilizados en datos tabulares debido a su interpretabilidad y capacidad para manejar relaciones no lineales. El enfoque de Gradient Boosting combina múltiples árboles débiles para construir un modelo robusto mediante optimización iterativa.

Algoritmos como XGBoost [1], LightGBM [2] y CatBoost [3] han demostrado alto rendimiento en problemas de predicción estructurada, mejorando aspectos como eficiencia computacional, manejo de datos categóricos y escalabilidad.

### 2.3.4 Datos tabulares en sistemas empresariales

Los datos tabulares representan la forma más común de almacenamiento en sistemas empresariales, donde cada fila corresponde a una instancia y cada columna a una variable. Este tipo de datos se encuentra en sistemas como ERP, CRM y bases de datos financieras.

Estudios recientes indican que los modelos basados en árboles siguen siendo una referencia sólida para este tipo de datos, incluso frente a modelos profundos más complejos [4].

### 2.3.5 Series temporales y predicción

Las series temporales son secuencias de datos ordenados en el tiempo, utilizadas para analizar tendencias, estacionalidad y comportamiento dinámico. El objetivo principal es predecir valores futuros a partir de datos históricos.

Modelos clásicos como ARIMA permiten capturar relaciones lineales [6], mientras que modelos modernos como Prophet [7] facilitan el modelado de tendencias y estacionalidad. En paralelo, arquitecturas profundas como N-BEATS [8], N-HiTS [9] y TFT [10] han demostrado mejoras en predicción multi-horizonte y manejo de variables externas.

### 2.3.6 Detección de anomalías

La detección de anomalías consiste en identificar observaciones que se desvían significativamente del comportamiento esperado. Este proceso es clave en aplicaciones como fraude, monitoreo y auditoría.

El algoritmo Isolation Forest [11] permite detectar anomalías mediante la partición aleatoria del espacio de datos, mientras que LOF [12] se basa en la densidad local. En escenarios más complejos, se emplean enfoques profundos como Deep SVDD [13]. Sin embargo, la literatura evidencia que la efectividad depende del contexto y tipo de datos [14].

### 2.3.7 Detección de fraude y auditoría inteligente

Los sistemas modernos de detección de fraude combinan modelos predictivos, detección de anomalías y reglas de negocio. Estos sistemas enfrentan desafíos como el desbalance de clases y la variabilidad temporal de los datos.

Investigaciones recientes destacan la necesidad de arquitecturas híbridas que integren múltiples enfoques para mejorar la precisión y robustez del sistema [16], [17]. Además, el uso de datasets sintéticos permite simular escenarios reales y evaluar el desempeño de los modelos [15].

### 2.3.8 Modelos de lenguaje (LLMs) y generación de reportes

Los modelos de lenguaje de gran escala (LLMs) permiten generar texto en lenguaje natural a partir de datos estructurados. En sistemas empresariales, se utilizan para transformar resultados analíticos en reportes comprensibles para usuarios no técnicos.

Sin embargo, su uso debe ser complementario a modelos determinísticos, debido a limitaciones en precisión y trazabilidad [18], [19].

### 2.3.9 Gobernanza y calidad en sistemas de IA

El desarrollo de sistemas de inteligencia artificial requiere garantizar confiabilidad, transparencia y control del riesgo. El marco de gestión de riesgos del NIST [20] proporciona lineamientos para asegurar estos aspectos.

Asimismo, prácticas como Datasheets for Datasets [22] y Model Cards [23] permiten documentar datasets y modelos, mejorando la reproducibilidad y reduciendo sesgos en sistemas productivos.

---

(Continúa en siguiente sección: Capítulo III Propuesta Metodológica)
