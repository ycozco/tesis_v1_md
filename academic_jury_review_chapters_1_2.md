# Dictamen Crítico y Exhaustivo de Tesis (Capítulos I y II)
**Nivel:** Jurado Académico de Tesis UNSA (Ingeniería de Sistemas / IA / Auditoría de Sistemas)  
**Proyecto:** *Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas*  
**Foco de Evaluación:** Capítulo I (Planteamiento del Problema, Hipótesis, Variables) y Capítulo II (Antecedentes, Estado del Arte, Marco Conceptual) hasta el inicio del Capítulo III.

---

## 🔍 Introducción al Dictamen de Capítulos I y II
Como jurado evaluador, se ha realizado una lectura exhaustiva de la tesis monolítica. El manuscrito destaca por una redacción técnica impecable, una estructura capitular sólida y una articulación teórica de primer nivel. Sin embargo, para que los Capítulos I y II cumplan plenamente con el rigor epistemológico y técnico exigido por la Escuela Profesional de Ingeniería de Sistemas de la UNSA para optar por el título profesional, se deben subsanar las observaciones que se detallan a continuación.

---

## 1. CAPÍTULO I: Planteamiento del Problema e Hipótesis

### 1.1 Conexión Operativa y "Anomalías" en el Sector Agroexportador (§1.1)
*   **Crítica del Jurado**: El planteamiento describe con solidez el dinamismo macroeconómico del sector (MIDAGRI, 2026). Sin embargo, se mantiene en un nivel abstracto al definir "anomalías operativas". Un jurado especialista en operaciones o logística observará que no se detallan cuáles son los **cuellos de botella y fallas críticas del mundo real** en la agroexportación peruana.
*   **Vulnerabilidad Faltante**: El texto no menciona ejemplos concretos de la realidad agroexportadora nacional, tales como:
    1.  **Fallas en la Cadena de Frío (*Cold Chain Failure*)**: Pérdida de calibración de temperatura en contenedores refrigerados durante el tránsito terrestre hacia el puerto del Callao o Paita, acelerando la maduración y provocando el rechazo del lote en destino.
    2.  **Alertas Fitosanitarias de SENASA/FDA**: Detección de trazas de pesticidas por encima del límite máximo de residuos (LMR) permitido por regulaciones internacionales o presencia de plagas cuarentenarias.
    3.  **Desviaciones de Calidad en Cosecha**: Sobredimensionamiento o calibre inadecuado de frutas (arándanos, uvas) debido a fluctuaciones atípicas de temperatura registradas por el SENAMHI.
*   **Recomendación de Mejora**: Modificar el §1.1 para inyectar estos tres ejemplos prácticos. Esto demuestra al jurado que el estudiante comprende el negocio real del agro y no solo la teoría del machine learning.

### 1.2 Viabilidad Legal y Aplicabilidad del D.S. N° 115-2025-PCM (§1.1 / §1.7.3)
*   **Crítica del Jurado**: La tesis justifica la solución citando la Ley N.° 31814 y el D.S. N.° 115-2025-PCM. No obstante, un jurado especializado en derecho tecnológico u auditoría regulatoria observará que la Ley N.° 31814 y su reglamento regulan **obligatoriamente al sector público nacional** y promueven la adopción responsable en el sector privado de forma general. El texto actual puede inducir al error de que una empresa agroexportadora privada peruana tiene la *obligación legal imperativa* de someterse a este reglamento de la misma forma que un ministerio.
*   **Recomendación de Mejora**: Clarificar en el texto que las agroexportadoras adoptan los principios de transparencia, explicabilidad y supervisión del D.S. N° 115-2025-PCM y el NIST AI RMF bajo un esquema de **conformidad voluntaria por diseño** (*Voluntary Compliance by Design*), posicionándose de manera competitiva frente a barreras comerciales no arancelarias en mercados de alta regulación como la Unión Europea (EU AI Act).

### 1.3 Formulación Matemática y Operacionalización de las Sub-Hipótesis (§1.4)
*   **Crítica del Jurado**: Las sub-hipótesis H1a, H1b, H1c y H1d están bien redactadas en prosa, pero carecen de rigor operacionalizable directo. Un metodólogo estricto observará que términos como "mejor rendimiento" o "mayor trazabilidad" son subjetivos si no se enlazan con sus indicadores cuantitativos directos definidos en la operacionalización (§1.5).
*   **Recomendación de Mejora**: Refinar la enunciación de las sub-hipótesis de la siguiente manera:
    *   **H1a**: Cambiar *"mejor rendimiento"* por *"mayor rendimiento de detección medido mediante el área bajo la curva de precisión y exhaustividad (PR-AUC $\ge 0.85$ y F1-Score $\ge 0.80$)"*.
    *   **H1d**: Cambiar *"reduce el tiempo"* por *"reduce en al menos un 20% el tiempo promedio requerido para interpretar una alerta operativa, con significancia estadística bajo la prueba de Wilcoxon ($\alpha = 0.05$)"*.

---

## 2. CAPÍTULO II: Antecedentes, Estado del Arte y Marco Conceptual

### 2.1 Carencia de Antecedentes del Dominio Sectorial (§2.1)
*   **Crítica del Jurado**: Los antecedentes metodológicos son impecables (Kadir et al., 2025; Grinsztajn et al., 2022; Han et al., 2022). Sin embargo, casi todos los antecedentes se sitúan en el ámbito del fraude financiero, asientos contables o benchmarks generales de datos tabulares. Un jurado revisor criticará que **no existan antecedentes de machine learning aplicado al agro o agroexportación peruana**, lo cual debilita el estado del arte y la contextualización de la brecha.
*   **Recomendación de Mejora**: Incorporar al menos dos antecedentes de aplicación sectorial. Ejemplos sugeridos:
    1.  Modelos predictivos de rendimiento de cultivos en el norte y sur peruano utilizando GBDT y variables de clima (SENAMHI).
    2.  Detección de anomalías en cadenas logísticas de perecederos mediante sensores de temperatura y algoritmos de aislamiento espacial.

### 2.2 Defensa de la Capa de Detección (Ensemble vs. Deep Learning para Series Temporales) (§2.2.2)
*   **Crítica del Jurado**: En la segunda batalla del Estado del Arte (§2.2.2), se defiende el uso del ensemble IF+LOF+ECOD sobre detectores profundos basados en redes neuronales. Un jurado especialista en Inteligencia Artificial preguntará: *"Dado que los datos agroexportadores tienen un alto componente temporal (estacionalidad de cosechas, variaciones climáticas semanales), ¿por qué no se utilizó un detector de anomalías basado en aprendizaje profundo para series de tiempo, como LSTM-Autoencoders o Temporal Fusion Transformers aplicados a anomalías?"*
*   **Recomendación de Mejora**: Introducir en la justificación de la posición de la tesis en §2.2.2 el factor de **factibilidad de infraestructura y costo computacional en entornos productivos medianos**. Explicar que los modelos profundos de series de tiempo requieren infraestructura GPU dedicada para el reentrenamiento frecuente ante el *concept drift* temporal (estacionalidad de campañas agrícolas), lo que resulta inviable económicamente para agroexportadoras medianas peruanas. En contraste, el ensemble tabular propuesto se entrena en CPU estándar en pocos segundos con mínima latencia y alta interpretabilidad, garantizando viabilidad operativa real.

### 2.3 El Vacío Matemático de la Capa 2 en el Marco Conceptual (§2.3.4)
*   **Crítica del Jurado**: Esta es una de las observaciones técnicas más severas. Se define en el marco conceptual que el sistema propone un "Stacking Ensemble" combinando Isolation Forest, Local Outlier Factor y ECOD. Sin embargo, no se presenta la formulación matemática de cómo se unifican y combinan los puntajes marginales de anomalía.
    *   *El problema matemático*: El score bruto de IF está en $[0, 1]$; el score bruto de LOF va de $1$ a $\infty$; y el score de ECOD representa densidades marginales acumuladas. Sumarlos o promediarlos directamente es un grave error de diseño.
*   **Recomendación de Mejora**: Agregar en la sección 2.3.4 la formulación matemática exacta de la unificación probabilística de los scores marginales. Por ejemplo, definir que los scores brutos $S_m(x)$ para cada modelo $m \in \{IF, LOF, ECOD\}$ se transforman en probabilidades unificadas $P_m(a|x) \in [0, 1]$ mediante el escalamiento probabilístico de Kriegel et al. (2011), y que la puntuación consolidada del ensemble se calcula como:
    $$S_{Ensemble}(x) = \frac{1}{3} \sum_{m \in \{IF, LOF, ECOD\}} P_m(a|x)$$
    Esto proporciona la rigurosidad matemática que exige una tesis de Ingeniería de Sistemas de la UNSA.

---

## 3. CAPÍTULO III: Metodología (Comienzo)

### 3.1 Consistencia de Instrumentos y Escalas Likert (§3.3.1)
*   **Crítica del Jurado**: Al inicio del Capítulo III, se define que la variable VD4 (Comprensión) se medirá mediante una Escala Likert de 1 a 5. El jurado metodológico observará si no se justifica la fiabilidad de este instrumento. ¿Cómo sabemos que la escala Likert mide la "comprensión real" y no simplemente la "sensación de claridad"?
*   **Recomendación de Mejora**: Explicar en la metodología que el cuestionario Likert se complementa con una **evaluación objetiva post-tarea** (preguntar al usuario qué decisión operativa específica tomaría ante la alerta y contrastarla contra la decisión óptima esperada, midiendo la tasa de decisión correcta como indicador binomial de control).

---

## ⚖️ Dictamen Final de Capítulos I y II
Los Capítulos I y II son **sobresalientes en su planteamiento general**. Para alcanzar el nivel de excelencia académica y garantizar una aprobación rápida sin observaciones por parte de los dictaminadores, se deben implementar las modificaciones sugeridas para: (a) concretar los ejemplos de anomalías agrícolas reales, (b) aclarar la conformidad voluntaria del D.S. N° 115-2025-PCM, (c) justificar la exclusión de deep learning temporal por coste y (d) detallar la unificación matemática del ensemble.
