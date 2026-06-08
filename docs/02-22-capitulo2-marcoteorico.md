## 2.3 Marco Conceptual

### 2.3.1 Reconocimiento de Patrones y Aprendizaje Automático

El reconocimiento de patrones es la disciplina de la inteligencia artificial que busca identificar regularidades, estructuras o relaciones en datos a partir de ejemplos históricos. En el aprendizaje automático, este proceso se formaliza mediante modelos que aprenden una función $f: X \rightarrow Y$ a partir de un conjunto de entrenamiento $\{(x_i, y_i)\}_{i=1}^n$, con el objetivo de generalizar hacia instancias no observadas.

Se distinguen tres paradigmas principales: **aprendizaje supervisado**, donde el modelo aprende de etiquetas explícitas (e.g., operación normal / operación anómala); **aprendizaje no supervisado**, que identifica patrones sin etiquetas y es fundamental en la detección de anomalías; y **aprendizaje semi-supervisado**, que combina ambos cuando el etiquetado es costoso o escaso, escenario habitual en procesos agroexportadores donde no todas las desviaciones quedan registradas formalmente.

En el contexto de esta investigación, el reconocimiento de patrones opera en dos dimensiones complementarias: la detección de registros operativos anómalos (patrones puntuales) y la identificación de secuencias temporales de comportamiento irregular (patrones colectivos), requiriendo tanto modelos de clasificación supervisada como detectores de anomalías no supervisados.

### 2.3.2 Datos Tabulares en Sistemas Agroexportadores Empresariales

Los datos tabulares son la forma predominante de almacenamiento en los sistemas de información empresarial: cada fila representa una instancia operativa y cada columna una variable. En agroexportación, una instancia puede describir un lote, día, producto, zona, envío o registro de mercado; las columnas pueden incluir precio, volumen, temperatura, precipitación, humedad, destino, cumplimiento fitosanitario, días logísticos, merma y etiqueta de anomalía.

Estas propiedades estructurales explican por qué los GBDT son adecuados para este dominio (Grinsztajn et al., 2022): manejan variables numéricas y categóricas heterogéneas, toleran valores faltantes, capturan relaciones no lineales y requieren menor ingeniería de features que arquitecturas neuronales complejas. Cuando las etiquetas de anomalía son escasas o desbalanceadas, el rendimiento debe evaluarse con métricas orientadas a precisión-recall (PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad)), F1-Score (Medida Armónica de Precisión y Exhaustividad) y análisis de falsos positivos.

### 2.3.3 GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente)

Los Gradient Boosting Decision Trees (GBDT) son una familia de algoritmos de aprendizaje supervisado que construyen modelos predictivos mediante la combinación secuencial de múltiples árboles de decisión débiles. El enfoque fue formalizado por Friedman (2001) como "Greedy Function Approximation", donde cada árbol nuevo se ajusta para corregir los errores residuales del conjunto de árboles previos mediante descenso de gradiente en el espacio funcional de la función de pérdida.

La formulación matemática central de GBDT busca encontrar una función $F(x)$ que minimice la pérdida esperada:

$$F^*(x) = \arg\min_{F} \mathbb{E}_{y,x}[L(y, F(x))]$$

donde $L$ es la función de pérdida (e.g., entropía cruzada para clasificación, MSE para regresión) y la minimización se realiza iterativamente añadiendo árboles de regresión $h_m(x)$ con pesos de aprendizaje $\nu$:

$$F_m(x) = F_{m-1}(x) + \nu \cdot h_m(x)$$

**XGBoost** (Chen & Guestrin, 2016) introduce mejoras clave sobre el GBDT estándar: regularización L1 y L2 en la función objetivo para controlar la complejidad del modelo, manejo nativo de valores faltantes mediante aprendizaje automático de la dirección de ramificación, y paralelización por columnas en lugar de por filas, lo que habilita el procesamiento en datasets de alta dimensión.

**LightGBM** (Ke et al., 2017) acelera el entrenamiento mediante dos innovaciones: Gradient-based One-Side Sampling (GOSS), que retiene las muestras con mayor gradiente y descarta aleatoriamente las de menor gradiente, preservando la distribución sin pérdida estadística significativa; y Exclusive Feature Bundling (EFB), que agrupa features mutuamente excluyentes para reducir dimensionalidad efectiva. El resultado es una aceleración de hasta 20× sobre XGBoost con precisión comparable.

**CatBoost** (Prokhorenkova et al., 2018) resuelve el problema del target leakage en variables categóricas mediante Ordered Boosting: calcula las estadísticas de objetivo para cada categoría usando únicamente las observaciones previas en un orden aleatorio permutado, evitando que la información del objetivo filtre hacia las features de entrada durante el entrenamiento. Esta propiedad es especialmente relevante en datos contables, donde variables como "código de cuenta" o "centro de costo" tienen alta cardinalidad.

La justificación empírica para elegir GBDT sobre Deep Learning en datos tabulares empresariales está sólidamente documentada por (Grinsztajn et al., 2022): en 45 datasets con hasta 50,000 muestras, los GBDT superan a arquitecturas neuronales complejas (como FT-Transformer o TabNet) en la inmensa mayoría de los casos. Dado que el dataset operativo de esta tesis se define como un dataset agroexportador integrado de escala tabular, con datos reales observados, datos agregados, proxies y datos sintéticos controlados, se sitúa en el rango donde los modelos basados en árboles maximizan su ventaja comparativa. Esta superioridad es atribuible a tres propiedades estructurales de los datos tabulares que los árboles aprovechan mejor que las redes neuronales.

### 2.3.4 Detección de Anomalías y Estrategia de Ensemble

La detección de anomalías es el problema de identificar observaciones que se desvían significativamente del comportamiento esperado del conjunto de datos. La literatura distingue tres tipos fundamentales de anomalías (Han et al., 2022): (a) **puntuales** — instancias individuales anómalas (e.g., una transacción de monto atípico); (b) **contextuales** — instancias que son anómalas en un contexto particular pero no en general (e.g., un cargo nocturno inusual para un perfil de usuario); y (c) **colectivas** — secuencias de instancias que son anómalas en conjunto aunque cada una individualmente no lo sea (e.g., un patrón de micro-transacciones).

**Isolation Forest** (Liu et al., 2008) se basa en el principio de que las anomalías son "pocas y diferentes": son más fáciles de aislar que los puntos normales mediante particionamiento aleatorio del espacio. Un árbol de aislamiento selecciona aleatoriamente una feature y un valor de corte; la anomalía será aislada en pocas particiones (camino corto), mientras que los puntos normales requieren muchas particiones (camino largo). El score de anomalía es el inverso de la longitud promedio del camino de aislamiento, normalizada según la longitud esperada para un punto normal en un conjunto de tamaño $n$. La complejidad es O(n log n) en entrenamiento y O(n) en inferencia.

**Local Outlier Factor (LOF (Local Outlier Factor - Factor de Anomalía Local))** (Breunig et al., 2000) cuantifica el grado de anomalía de cada punto en función de la densidad de su vecindario local respecto a la densidad de sus vecinos. El score LOF para el punto $p$ se define como:

$$\text{LOF}_k(p) = \frac{\sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}}{|N_k(p)|}$$

donde $\text{lrd}_k$ es la densidad de alcanzabilidad local. Un valor LOF >> 1 indica que $p$ tiene densidad local mucho menor que sus vecinos, lo que lo caracteriza como anomalía. LOF es sensible a variaciones locales de densidad, lo que lo hace complementario a Isolation Forest en datasets heterogéneos.

**Deep SVDD** (Ruff et al., 2018) extiende el Support Vector Data Description al espacio de representación de redes neuronales: entrena una red para mapear los datos normales hacia el interior de una hipersfera mínima en el espacio latente. Las anomalías se detectan como puntos que caen fuera o lejos de esta hipersfera. La función objetivo minimiza el volumen de la hipersfera:

$$\min_{W, R, c} R^2 + \frac{1}{\nu n} \sum_{i=1}^{n} \max(0, \|f(x_i; W) - c\|^2 - R^2)$$

donde $f(x_i; W)$ es la representación de la red neuronal, $c$ es el centro de la hipersfera y $R$ es su radio.

**ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica)** (Li et al., 2022) calcula el score de anomalía como la probabilidad acumulada de observar un punto tan extremo como $x$ bajo la distribución empírica del dataset, estimada mediante funciones de distribución acumulada (ECDF) multivariadas. Su ventaja principal es que no tiene hiperparámetros que calibrar, eliminando el riesgo de sobreajuste y simplificando el despliegue en producción.

La estrategia de **ensemble** consolida las puntuaciones de múltiples detectores para reducir la varianza del estimador agregando perspectivas de densidad local (LOF), aislamiento espacial (IF) y probabilidad empírica acumulada (ECOD). Sin embargo, un desafío matemático fundamental radica en que los algoritmos marginales producen puntuaciones en escalas y naturalezas numéricas completamente incompatibles:
1. **Isolation Forest** genera puntuaciones acotadas $S_{IF}(x) \in [0, 1]$.
2. **Local Outlier Factor** genera puntuaciones $S_{LOF}(x) \in [1, \infty)$, donde valores cercanos a 1 indican normalidad y valores superiores representan el grado local de desviación.
3. **ECOD** genera puntuaciones acumuladas inversas $S_{ECOD}(x) \in [0, \infty)$ en escalas de log-probabilidad.

Sumar o promediar estos valores en bruto anularía la influencia de IF y ECOD debido a que LOF dominaría la agregación por magnitud. Para resolver esta incompatibilidad, esta tesis implementa la unificación probabilística de puntuaciones basada en el escalamiento Min-Max lineal calibrado sobre el conjunto de entrenamiento (Kriegel et al., 2011). Las puntuaciones brutas de cada detector se transforman en puntuaciones probabilísticas de anomalía acotadas $P_m(a|x) \in [0, 1]$ mediante la función de mapeo:

$$P_m(a|x) = \max\left(0, \min\left(1, \frac{S_m(x) - \min_{x' \in D_{train}}(S_m(x'))}{\max_{x' \in D_{train}}(S_m(x')) - \min_{x' \in D_{train}}(S_m(x'))}\right)\right)$$

donde $\min_{D_{train}}$ y $\max_{D_{train}}$ son los valores extremos de score observados en el conjunto de calibración histórica del detector $m$. La puntuación consolidada de anomalía del ensemble $S_{Ensemble}(x) \in [0, 1]$ se calcula entonces como el promedio simple de estas probabilidades unificadas:

$$S_{Ensemble}(x) = \frac{P_{IF}(a|x) + P_{LOF}(a|x) + P_{ECOD}(a|x)}{3}$$

Una instancia operativa $x$ se clasifica finalmente como alerta anómala si y solo si $S_{Ensemble}(x) \ge \tau$, donde $\tau \in [0, 1]$ es el umbral de decisión operativo global calibrado empíricamente en la fase de validación cruzada. El fundamento teórico de este enfoque de agregación lo proporciona ADBench (Han et al., 2022) y su implementación robusta se realiza mediante la API modular de PyOD (Zhao et al., 2019).

### 2.3.5 Forecasting de Series Temporales con Transformers

Las series temporales agroexportadoras presentan tres desafíos que los modelos de forecasting deben resolver: tendencia no estacionaria, estacionalidad múltiple (diaria, semanal, mensual, anual) y dependencia de covariables exógenas (clima, calendario agrícola, demanda internacional, precios y condiciones logísticas). Los modelos estadísticos clásicos como ARIMA capturan relaciones lineales con eficacia, pero presentan limitaciones en la modelización de no-linealidades y horizontes largos.

**Temporal Fusion Transformer (TFT)** (Lim et al., 2021) propone una arquitectura especializada que combina cuatro mecanismos: (1) codificación LSTM para dependencias secuenciales locales; (2) selección de variables con mecanismo de gating (GLU — Gated Linear Unit) que identifica automáticamente las covariables más informativas; (3) atención multi-cabezal interpretable que pondera los pasos temporales según su relevancia predictiva; y (4) red de cuantiles para cuantificar la incertidumbre de la predicción. TFT acepta tres tipos de entradas: features estáticas conocidas (e.g., producto, zona, destino), covariables futuras conocidas (e.g., calendario agrícola, campañas, feriados) y covariables históricas observadas (e.g., precio, volumen, clima o merma pasada).

El debate sobre la efectividad de los Transformers en series temporales es relevante para esta tesis. Zeng et al. (2023) argumentan que DLinear —un modelo lineal simple— supera a los Transformers en múltiples benchmarks, atribuyendo la limitación de los Transformers al hecho de que el mecanismo de self-attention es permutation-invariant y destruye el orden temporal de las secuencias. Sin embargo, este argumento ha sido rebatido sucesivamente: Nie et al. (2023) demuestran que la tokenización por patches —agrupando segmentos temporales antes de aplicar atención— preserva el orden local y supera a DLinear en la mayoría de benchmarks de horizonte largo. Liu et al. (2024) proponen invertir la tokenización: en lugar de tokenizar por timestamp, tokenizan por variable, aplicando self-attention entre variables en lugar de entre tiempos, obteniendo SOTA en 7 datasets multivariados.

**Posición de esta tesis respecto al debate**: TFT se considera por su interpretabilidad incorporada —el mecanismo de gating y los mapas de atención son legibles por analistas— más que exclusivamente por su rendimiento predictivo. En el contexto agroexportador, la capacidad de justificar qué períodos temporales y qué covariables fundamentan la predicción es un requerimiento funcional comparable en importancia a la precisión numérica.

N-HiTS (Challu et al., 2022) ofrece una alternativa no-Transformer para forecasting de horizonte largo, con interpolación jerárquica multi-tasa que reduce la complejidad computacional respecto a N-BEATS. Chronos (Ansari et al., 2024) representa el paradigma emergente de los foundation models para series temporales, basado en T5, que logra performance zero-shot competitivo en múltiples datasets; sin embargo, su opacidad y dependencia de infraestructura de gran escala limitan su aplicación directa cuando se requiere trazabilidad operativa.

### 2.3.6 Explicabilidad mediante SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)

La explicabilidad en sistemas de IA se clasifica en dos grandes categorías: **inherente** —modelos cuya estructura es intrínsecamente interpretable, como los árboles de decisión— y **post-hoc** —métodos aplicados a cualquier modelo después del entrenamiento para interpretar sus predicciones. SHAP y LIME son los dos métodos post-hoc agnósticos más adoptados en la literatura.

**LIME** (Local Interpretable Model-agnostic Explanations) (Ribeiro et al., 2016) genera explicaciones locales construyendo un modelo lineal sustituto en el vecindario de la instancia a explicar, ponderando las muestras según su proximidad al punto de interés. LIME es rápido y flexible, pero produce explicaciones inestables: pequeñas perturbaciones de la instancia pueden cambiar significativamente la explicación, un problema crítico en contextos forenses.

**SHAP** (Lundberg & Lee, 2017) fundamenta las explicaciones en los valores de Shapley de la teoría de juegos cooperativos. El valor SHAP de la feature $i$ para la predicción $f(x)$ cuantifica la contribución marginal media de $i$ a la predicción, promediando sobre todas las coaliciones posibles de features:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!} [f(S \cup \{i\}) - f(S)]$$

donde $F$ es el conjunto de todas las features y $S$ es una coalición de features sin $i$. Esta formulación garantiza cuatro propiedades axiomáticas: (a) **eficiencia** — la suma de todos los valores SHAP iguala la diferencia entre la predicción y el valor esperado; (b) **simetría** — features con contribución idéntica reciben el mismo valor; (c) **dummy** — features sin efecto tienen valor cero; y (d) **aditividad** — los valores SHAP son consistentes al combinar modelos.

SHAP resuelve las limitaciones de LIME al garantizar consistencia: si un modelo cambia la predicción al aumentar la contribución de una feature, el valor SHAP de esa feature nunca disminuye (Lundberg & Lee, 2017). **TreeSHAP** extiende este cálculo con un algoritmo exacto en O(TLD²) para modelos basados en árboles —donde T es el número de árboles, L es el número de hojas por árbol y D es la profundidad máxima— haciendo el cálculo computacionalmente viable para GBDT en producción.

En el contexto de supervisión operativa, la estabilidad de las explicaciones permite verificar que el modelo asigna importancias consistentes a variables semejantes. Un índice alto de estabilidad fortalece la confianza en el sistema, porque evita que alertas similares reciban justificaciones contradictorias.

La integración SHAP+LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño) de esta tesis opera como sigue: los vectores SHAP de una alerta operativa (una lista de pares variable→contribución cuantitativa) se incorporan como contexto verificado en el RAG, y el LLM genera la narración del informe sin posibilidad de inventar cifras que no estén en esos vectores o en las fuentes recuperadas.

### 2.3.7 Modelos de Lenguaje y Arquitectura RAG para Generación de Reportes

Los LLMs (Large Language Models - Modelos de Lenguaje de Gran Tamaño) son sistemas entrenados mediante autoregresión en corpus masivos de texto para aprender distribuciones probabilísticas sobre secuencias de tokens. Su capacidad de generalización les permite realizar tareas de reasoning, traducción, resumen y generación de texto con calidad próxima a la humana en configuraciones zero-shot y few-shot.

**In-context learning** permite guiar el comportamiento del LLM mediante ejemplos incluidos directamente en el prompt, sin necesidad de ajuste fino (fine-tuning). TabLLM (Hegselmann et al., 2023) demostró que mediante serialización de datos tabulares a texto descriptivo, los LLMs pueden realizar clasificación sobre datos estructurados con rendimiento no trivial en zero-shot, ampliando el espectro de aplicación de estos modelos más allá del texto no estructurado.

Sin embargo, el uso de LLMs como agentes de decisión autónoma introduce el riesgo de **alucinaciones**: el modelo puede generar afirmaciones coherentes en forma pero incorrectas en contenido (Ji et al., 2023; Maynez et al., 2026). La literatura distingue al menos dos tipos: (a) alucinaciones intrínsecas, en las que el texto generado contradice la información del contexto recuperado; y (b) alucinaciones extrínsecas, en las que el modelo inventa información no presente en el contexto. En particular, las "alucinaciones numéricas" —valores específicos de métricas, porcentajes o fechas que no corresponden a los datos reales (Barclays Research, 2025)— son especialmente peligrosas en reportes operativos, porque pueden inducir decisiones equivocadas pese a la apariencia de precisión cuantitativa.

**RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)** (Lewis et al., 2020; Schneider et al., 2025) reduce este riesgo al separar el conocimiento factual del modelo generativo: en lugar de que el LLM "recuerde" información de su entrenamiento, el sistema recupera documentos o datos relevantes de una base de conocimiento externa verificada y los incluye en el contexto del prompt. El LLM entonces genera texto fundamentado en esos datos recuperados, no en su memoria paramétrica. Es importante señalar que RAG **reduce significativamente pero no elimina** el riesgo de alucinación; persisten casos de alucinación intrínseca (faithful hallucination) en los que el modelo genera afirmaciones que se desvían del contexto recuperado. Técnicas avanzadas como GraphRAG incorporan grafos de conocimiento para recuperación semántica más rica, mientras que Self-RAG permite al modelo verificar la pertinencia de los documentos recuperados antes de usarlos.

En la arquitectura de esta tesis, la "base de conocimiento" del RAG son los vectores SHAP de la alerta analizada, las métricas del ensemble de detección, las fuentes agroexportadoras recuperadas y las reglas de reporte definidas. El LLM recibe ese contexto verificado y genera el informe narrativo sin acceso a conocimiento adicional no validado. Adicionalmente se aplican dos controles complementarios: (a) plantillas de prompt estructurado con campos obligatorios (dato, modelo, score, umbral, explicación SHAP, fuente recuperada), y (b) validación posterior del reporte contra los vectores SHAP de entrada para detectar discrepancias numéricas. Este diseño permite que cada afirmación del reporte pueda trazarse hasta una fuente, score, umbral o variable explicativa.

La evaluación de calidad de los reportes generados puede utilizar **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) cuando exista un texto de referencia. Sin embargo, para esta tesis se prioriza una rúbrica operativa de completitud, consistencia, accionabilidad y correspondencia con evidencias, porque la calidad de un reporte de supervisión depende no solo de similitud textual, sino de su utilidad para la toma de decisiones.

### 2.3.8 Gobernanza de IA y MLOps

El despliegue de sistemas de IA en entornos empresariales críticos requiere un marco de gobernanza que trascienda el rendimiento técnico. Sculley et al. (2015) documentaron la "deuda técnica oculta" en sistemas de ML: más del 95% del código de un sistema ML de producción no es el modelo en sí, sino la infraestructura de ingesta, validación, features, servicio y monitoreo. Los pipelines con alto acoplamiento entre componentes generan "entanglement" que dificulta el mantenimiento y aumenta el riesgo de regresiones silenciosas.

**MLOps** (Kreuzberger et al., 2022) establece el conjunto de prácticas para gestionar el ciclo de vida completo de los modelos ML en producción: integración y entrega continua (CI/CD) para modelos, monitoreo de data drift y model drift, automatización del reentrenamiento, y trazabilidad de versiones de datos, código y modelos. En el contexto de supervisión operativa agroexportadora, MLOps permite reproducir qué modelo generó una alerta, con qué datos de entrada, bajo qué versión y con qué umbral.

El **NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0)** (NIST, 2023) proporciona cuatro funciones de gestión de riesgo para sistemas de IA: (1) **Govern** — establecer políticas y roles de responsabilidad; (2) **Map** — identificar el contexto de despliegue y los riesgos asociados; (3) **Measure** — evaluar los riesgos con métricas verificables; y (4) **Manage** — implementar controles y mitigaciones. La arquitectura modular de esta tesis es diseñada para que cada capa corresponda a responsabilidades verificables bajo este framework.

**Datasheets for Datasets** (Gebru et al., 2021) propone una plantilla de documentación estandarizada para datasets que detalla: motivación de recolección, proceso de recolección, composición, preprocesamiento aplicado, distribución permitida y consideraciones éticas. Esta práctica se aplicará al dataset agroexportador integrado y a sus capas de datos reales, agregados, proxies y sintéticos controlados, garantizando que los resultados reportados sean reproducibles y que las limitaciones de cada fuente estén identificadas antes de evaluar el sistema.

**Model Cards** (Mitchell et al., 2019) extiende la documentación al nivel del modelo, especificando para quién fue entrenado, en qué condiciones, cuáles son sus limitaciones conocidas y cómo debe usarse de manera responsable. En esta tesis, se elaboran Model Cards para los modelos XGBoost/LightGBM, detectores de anomalías y el componente LLM+RAG, en conformidad con los principios de documentación del NIST AI RMF (NIST, 2023).

El contexto peruano e internacional consolida la necesidad de este framework de gobernanza. El D.S. N° 115-2025-PCM (PCM, 2025), el NIST AI RMF (NIST, 2023) y el EU AI Act (Parlamento Europeo y Consejo, 2024) refuerzan principios comunes: transparencia, documentación, supervisión humana y gestión de riesgos. Estos principios son adoptados como referencia de diseño para esta tesis. No se afirma cumplimiento formal con ninguno de estos marcos —tal afirmación requeriría auditoría regulatoria externa— sino conformidad de diseño con sus principios, en particular: (a) transparencia mediante SHAP y Model Cards, (b) supervisión humana mediante revisión obligatoria de cada reporte antes de su uso operativo, (c) gestión de riesgos mediante umbrales calibrados y validación cruzada, y (d) trazabilidad documental mediante logs completos por alerta. La aplicabilidad regulatoria efectiva del sistema a una empresa específica depende de su clasificación de riesgo bajo el reglamento correspondiente y queda fuera del alcance de esta tesis.

### 2.3.9 Supervisión Operativa, Trazabilidad e Inteligencia Artificial

La supervisión operativa en agroexportación exige monitorear procesos que combinan producción, acopio, calidad, sanidad, logística y comercio exterior. Las anomalías en este dominio no necesariamente corresponden a fraude; pueden representar variaciones atípicas de precio, caídas de volumen, condiciones climáticas adversas, mermas elevadas, incumplimientos fitosanitarios o retrasos logísticos. Por ello, el sistema propuesto se orienta a detectar desviaciones relevantes para la toma de decisiones, no a sustituir procesos de investigación legal o auditoría financiera.

La **supervisión operativa continua** busca reemplazar ciclos de revisión tardíos por monitoreo frecuente y documentado de indicadores. En este enfoque, cada alerta debe registrar el dato de origen, el modelo aplicado, el score calculado, el umbral utilizado, las variables explicativas y el reporte generado. Esta trazabilidad permite que un supervisor operativo comprenda por qué el sistema marcó un evento como anómalo y qué evidencia respalda la recomendación.

La integración de IA en supervisión operativa plantea el problema de la confianza en decisiones automáticas. Esta exigencia convierte a la explicabilidad (SHAP), la documentación de datasets (Datasheets), la documentación de modelos (Model Cards) y los logs de decisión en componentes funcionales del sistema. En el marco peruano, el D.S. N° 115-2025-PCM (PCM, 2025) proporciona una base general para el uso responsable de IA; la Resolución SBS N° 053-2023 (SBS, 2023) se conserva solo como referencia nacional de buenas prácticas para gestión de riesgo de modelos.

---

