# ESTADO DEL ARTE

## 2.2 Estado del Arte

El estado del arte de la investigación se estructura a partir de los siguientes debates científicos de la disciplina:

### 2.2.1 Modelos GBDT frente a Aprendizaje Profundo Tabular
El modelado de datos estructurados empresariales se caracteriza por un debate continuo entre el uso de algoritmos basados en árboles (GBDT) y la adaptación de arquitecturas de aprendizaje profundo, como Transformers tabulares o TabNet. Trabajos como FT-Transformer (Gorishniy et al., 2021) y TabNet (Arik & Pfister, 2021) muestran que los mecanismos de atención pueden capturar relaciones complejas. Sin embargo, la evidencia experimental de Grinsztajn et al. (2022) indica que los GBDT suelen mantener un rendimiento competitivo o superior en numerosos conjuntos tabulares de tamaño intermedio. Por ello, la tesis evalúa XGBoost y LightGBM como modelos principales, sin asumir su superioridad antes de ejecutar la comparación experimental.

### 2.2.2 Detector Único frente a Ensemble de Anomalías
En la detección de valores atípicos, el debate gira en torno a si un único detector optimizado, como Isolation Forest o LOF, resulta suficiente frente a un ensemble multialgoritmo. ADBench (Han et al., 2022) muestra que el desempeño depende del conjunto de datos y del tipo de anomalía, por lo que ningún detector debe considerarse universalmente superior. En esta tesis se comparan Isolation Forest, LOF y ECOD individualmente y como ensemble calibrado por percentiles; la conveniencia del ensemble deberá sustentarse con las métricas obtenidas en el experimento agroexportador.

### 2.2.3 Predicción Esperada y Residuos
La detección tradicional de anomalías suele aplicarse directamente sobre los datos observados. En esta investigación también se evaluarán desviaciones respecto de valores esperados mediante residuos predictivos. El uso de una mediana y una desviación absoluta mediana móvil de 13 semanas constituye una decisión metodológica del estudio y deberá validarse frente a otras ventanas o procedimientos robustos, evitando presentarla como una regla universal.

### 2.2.4 SHAP y Explicabilidad
La interpretabilidad algorítmica incluye métodos locales agnósticos, como LIME (Ribeiro et al., 2016), y métodos de atribución aditiva, como SHAP (Lundberg & Lee, 2017). LIME aproxima localmente el comportamiento del modelo, mientras que SHAP proporciona una formulación basada en valores de Shapley con propiedades formales de atribución. Para modelos de árboles, TreeSHAP permite calcular explicaciones de manera eficiente. La tesis adopta SHAP y evaluará la estabilidad y utilidad de sus explicaciones en el contexto agroexportador.

### 2.2.5 LLM como Detector frente a LLM como Redactor
Los modelos de lenguaje pueden emplearse para analizar datos serializados o apoyar la interpretación de alertas; sin embargo, presentan riesgos de alucinación factual y numérica. Por ello, en esta propuesta el modelo de lenguaje no sustituye a los detectores matemáticos. Su función se limita a redactar reportes a partir de evidencia estructurada, documentos recuperados y resultados previamente calculados.

### 2.2.6 RAG y Control Factual
La generación aumentada por recuperación (RAG) combina un modelo generativo con evidencia documental recuperada (Lewis et al., 2020). Esta arquitectura puede mejorar el acceso a información externa, pero no garantiza por sí sola la exactitud factual. Por ello, el sistema incorpora validación determinista de cifras, trazabilidad de evidencias y plantillas de contingencia cuando el reporte no supera los controles definidos.

### 2.2.7 Arquitecturas Aisladas frente a Integradas
La literatura revisada presenta soluciones separadas para pronóstico, detección de anomalías, explicabilidad y generación de reportes. La brecha de la investigación se define como la falta de integración y trazabilidad entre estos componentes en el dominio agroexportador peruano. Esta afirmación se limita al corpus bibliográfico revisado y deberá actualizarse si se incorporan nuevos antecedentes verificables.

### 2.2.8 Gobernanza de IA y Trazabilidad
El despliegue de sistemas inteligentes requiere gobernanza, supervisión humana y mecanismos de rendición de cuentas. La propuesta considera el NIST AI Risk Management Framework y las normas peruanas citadas como referencias de diseño. Cada alerta deberá poder reconstruirse mediante identificadores, marcas de tiempo, versiones y hashes de los artefactos relevantes.

---

### 2.2.9 Brecha específica que aborda la tesis

La revisión anterior permite delimitar una brecha: las herramientas existentes suelen resolver de forma separada el pronóstico, la detección de anomalías, la explicabilidad, la generación de reportes o la trazabilidad. En cambio, la supervisión agroexportadora requiere un flujo unido y auditable, porque una alerta solo resulta útil si puede reconstruirse desde el dato de origen hasta la decisión humana.

| Bloque del estado del arte | Solución dominante | Brecha persistente | Decisión de esta tesis |
|---|---|---|---|
| Predicción tabular | GBDT, modelos estadísticos y redes tabulares | Bajo acoplamiento con anomalías y reportes | Comparar XGBoost y LightGBM con modelos base para valor unitario FOB y volumen |
| Anomalías | Detectores individuales o benchmarks generales | Sensibilidad al tipo de anomalía y al umbral | Evaluar IF, LOF y ECOD individualmente y como ensemble calibrado |
| Explicabilidad | SHAP y LIME como análisis posterior al modelo | Explicaciones no siempre evaluadas con usuarios | Incorporar atribuciones SHAP en alertas y reportes y evaluar su utilidad |
| Reportes con LLM | Generación flexible de texto | Riesgo de errores numéricos y factuales | RAG restringido, validación determinista y plantilla de contingencia |
| Gobernanza | Model cards, datasheets y auditoría | Trazabilidad fragmentada entre artefactos | Hashes SHA-256, UUID, versiones y registro de linaje por alerta |
| Agroexportación peruana | Reportes sectoriales y fuentes públicas | Granularidades heterogéneas y uso de proxies | Dataset semanal producto-mercado-semana con marcas de origen |

### 2.2.10 Implicancia para el diseño metodológico

El diseño del Capítulo III adopta tres principios derivados del estado del arte:

1. **Modelo antes que alerta:** la anomalía se interpreta como desviación respecto de un valor esperado y no únicamente como un valor extremo observado.
2. **Explicación antes que automatización:** el sistema apoya la decisión humana y no ejecuta bloqueos automáticos ni sanciones.
3. **Evidencia antes que narrativa:** el reporte automático solo se acepta cuando sus cifras y afirmaciones pueden rastrearse a datos estructurados, documentos recuperados o registros de ejecución.

Cuando una fuente no tiene granularidad de embarque, se incorpora como contexto agregado o proxy y no se interpreta como causa directa de una falla operativa. Esta regla mantiene la consistencia entre el alcance de los datos disponibles y las afirmaciones de la tesis.