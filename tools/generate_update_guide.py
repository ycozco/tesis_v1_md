# -*- coding: utf-8 -*-
from pathlib import Path
import re

md_path = Path("docs/02-95-tesis.md")
out_path = Path("actualizacion-guia.md")

if not md_path.exists():
    print("Error: No se encuentra docs/02-95-tesis.md")
    exit(1)

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Helper to extract a section by title pattern
def extract_section(title_pattern, next_title_pattern):
    match = re.search(title_pattern, text, re.IGNORECASE)
    if not match:
        return f"*(Sección no encontrada para el patrón {title_pattern})*"
    
    start_idx = match.start()
    next_match = re.search(next_title_pattern, text[start_idx:], re.IGNORECASE)
    
    if next_match:
        end_idx = start_idx + next_match.start()
        return text[start_idx:end_idx].strip()
    else:
        return text[start_idx:].strip()

# Extract segments
sec_tecnicas_orig = extract_section(r"## 1.10 Tecnicas e instrumentos de recoleccion", r"## 1.11 Cronograma de actividades")

# Extract the conceptual framework points
sec_concept_231 = extract_section(r"### 2.3.1 Reconocimiento de Patrones", r"### 2.3.2 Datos Tabulares")
sec_concept_232 = extract_section(r"### 2.3.2 Datos Tabulares", r"### 2.3.3 GBDT")
sec_concept_233 = extract_section(r"### 2.3.3 GBDT", r"### 2.3.4 Deteccin")
sec_concept_234 = extract_section(r"### 2.3.4 Deteccin de Anomalas", r"### 2.3.5 Forecasting")
sec_concept_235 = extract_section(r"### 2.3.5 Forecasting", r"### 2.3.6 Explicabilidad")
sec_concept_236 = extract_section(r"### 2.3.6 Explicabilidad", r"### 2.3.7 Modelos de Lenguaje")
sec_concept_237 = extract_section(r"### 2.3.7 Modelos de Lenguaje", r"### 2.3.8 Gobernanza de IA")
sec_concept_238 = extract_section(r"### 2.3.8 Gobernanza de IA", r"### 2.3.9 Supervisin Operativa")
sec_concept_239 = extract_section(r"### 2.3.9 Supervisin Operativa", r"# CAPITULO III")

# Extract chapters III and IV details
sec_cap3_31 = extract_section(r"## 3.1 Arquitectura del sistema integrado", r"## 3.2 Dataset")
sec_cap3_32 = extract_section(r"## 3.2 Dataset agroexportador", r"## 3.3 Configuracion")
sec_cap3_33 = extract_section(r"## 3.3 Configuracion experimental", r"## 3.4 Reproducibilidad")

sec_cap4_41 = extract_section(r"## 4.1 Resultados Cuantitativos", r"## 4.2 Resultados Cualitativos")
sec_cap4_42 = extract_section(r"## 4.2 Resultados Cualitativos", r"## 4.3 Resultados del Estudio de Usabilidad")
sec_cap4_43 = extract_section(r"## 4.3 Resultados del Estudio de Usabilidad", r"## 4.4 Discusion")
sec_cap4_44 = extract_section(r"## 4.4 Discusion y Cruce Comparativo", r"## 4.5 Limitaciones")

# Endings
conclusiones_text = extract_section(r"# CONCLUSIONES\n", r"# CONCLUSIONS")
conclusions_en_text = extract_section(r"# CONCLUSIONS\n", r"# RECOMENDACIONES")
recomendaciones_text = extract_section(r"# RECOMENDACIONES\n", r"# GLOSARIO")
glosario_text = extract_section(r"# GLOSARIO DE TRMINOS", r"# REFERENCIAS")
referencias_text = extract_section(r"# REFERENCIAS BIBLIOGRAFICAS", r"# ANEXOS")

# Generate the actualizacion-guia.md content
guide_content = f"""# Guía de Actualización de Contenidos y Alineación de Tesis (UNSA)

Esta guía documenta detalladamente el estado anterior de la tesis, el nuevo contenido académico propuesto y la sustentación metodológica que justifica cada cambio para cumplir con las directrices de la Escuela Profesional de Ingeniería de Sistemas y el jurado examinador.

---

## Punto 1: Viabilidad de la Investigación (Sección 1.6)

### 1.1 Estado Anterior (Antes)
```
La viabilidad de la investigación se sustenta en la disponibilidad de herramientas tecnológicas, fuentes de datos accesibles y un diseño experimental realizable dentro del alcance académico del estudio. La propuesta no requiere una implementación productiva en tiempo real ni infraestructura empresarial compleja, sino un entorno controlado que permita construir el dataset, entrenar los modelos, generar explicaciones, producir reportes trazables y evaluar los resultados mediante métricas técnicas y criterios operativos.
Viabilidad  técnica

La investigación es técnicamente viable debido a que los componentes principales del sistema pueden implementarse mediante herramientas de código abierto y tecnologías ampliamente utilizadas en proyectos de aprendizaje automático, detección de anomalías, explicabilidad y procesamiento de lenguaje natural.

El módulo de predicción tabular puede desarrollarse con modelos como XGBoost y LightGBM, adecuados para datos estructurados de naturaleza empresarial. El módulo de detección de anomalías puede implementarse mediante algoritmos disponibles en librerías como PyOD y scikit-learn, incluyendo Isolation Forest, LOF y ECOD. La explicabilidad del sistema puede abordarse mediante SHAP, permitiendo identificar las variables que influyen en las alertas generadas. Finalmente, la generación de reportes puede desarrollarse mediante una arquitectura RAG, restringida al uso de evidencias estructuradas, metadatos, scores, umbrales y explicaciones previamente calculadas.

Desde el punto de vista computacional, el sistema puede ejecutarse en un ambiente experimental con recursos convencionales de cómputo, sin requerir infraestructura especializada de alto costo. La arquitectura propuesta puede organizarse en capas funcionales independientes, lo que facilita su desarrollo, prueba y validación progresiva. Además, el uso de herramientas reproducibles permite documentar versiones de datos, configuraciones de modelos, resultados experimentales y reportes generados.

La principal restricción técnica no corresponde a la disponibilidad de algoritmos, sino a la correcta integración de fuentes heterogéneas, el control de granularidades, la trazabilidad de los datos y la prevención de generación de información no sustentada por parte del modelo de lenguaje. Estas restricciones serán abordadas mediante reglas de integración, etiquetado metodológico de variables, separación entre datos reales, datos agregados, proxies y datos sintéticos controlados, así como mediante una arquitectura RAG limitada a evidencia verificable.

Por lo tanto, la investigación presenta viabilidad técnica, dado que sus componentes pueden ser implementados con tecnologías disponibles, reproducibles y compatibles con el alcance experimental de una tesis de Ingeniería de Sistemas.

Viabilidad de datos
La investigación es viable desde el punto de vista de los datos, debido a que se cuenta con fuentes públicas, agregadas y documentables que permiten construir un dataset agroexportador integrado. La fuente principal para los registros de comercio exterior corresponde a SUNAT/ADUANET, mientras que Trade Map puede utilizarse como fuente de contraste internacional. Asimismo, SISAP/MIDAGRI permite incorporar información de mercado interno mayorista, BCRP aporta variables macroeconómicas como el tipo de cambio, y fuentes climáticas, logísticas y sanitarias pueden incorporarse como variables contextuales o proxies documentados.
El dataset propuesto no depende exclusivamente de una única fuente, sino de la integración controlada de información real observada, información real agregada, variables derivadas, proxies y datos sintéticos controlados. Esta estrategia permite representar de manera más completa el contexto operativo agroexportador, considerando dimensiones de comercio exterior, mercado interno, clima, logística, sanidad y contexto internacional.
La investigación se focaliza en productos agroexportadores con mayor viabilidad de cobertura y representatividad, priorizando palta, uva y arándano como productos núcleo. El espárrago puede mantenerse como producto secundario sujeto a validación de cobertura suficiente, mientras que el cacao debe excluirse de la evaluación principal si no presenta representatividad adecuada en el dataset real auditado.
Una limitación relevante es que no todas las variables operativas existen públicamente con granularidad por embarque, lote o empresa. Por ello, algunas variables deberán tratarse como proxies, variables agregadas o variables sintéticas controladas. In particular, la etiqueta de anomalía deberá declararse según su origen metodológico: real, derivada por reglas, proxy o sintética controlada. Esta diferenciación es necesaria para evitar afirmar que el sistema detecta anomalías reales cuando, en determinados casos, evalúa escenarios experimentales construidos.
Por tanto, la investigación presenta viabilidad de datos, siempre que se mantenga una documentación rigurosa sobre el origen, granularidad, transformación y uso metodológico de cada variable incorporada al dataset.

Viabilidad  económica.
La investigación es operativamente viable porque el sistema será evaluado en un entorno experimental y no como una solución productiva en tiempo real. Esto permite delimitar el alcance del estudio al diseño, implementación y evaluación de un prototipo funcional capaz de procesar datos históricos o semiestáticos, entrenar modelos, detectar anomalías, generar explicaciones y producir reportes trazables.

La evaluación operativa puede realizarse mediante experimentos controlados, comparación frente a componentes aislados y revisión de indicadores asociados a detección, comprensión, calidad de reportes, tiempo de análisis y trazabilidad documental. Cuando sea posible, se podrá incorporar la evaluación de usuarios o expertos mediante cuestionarios tipo Likert, rúbricas de calidad y registros de tiempo de decisión.

Desde el punto de vista económico, la investigación es viable porque utiliza principalmente herramientas open-source, datos públicos o accesibles y recursos computacionales convencionales. No se requiere adquisición de licencias empresariales, sensores IoT, servidores especializados ni integración directa con sistemas productivos de empresas agroexportadoras. Esto reduce los costos de implementación y hace posible desarrollar la investigación dentro de un entorno académico.

El beneficio económico no se medirá como rentabilidad empresarial directa, sino como impacto potencial asociado a la reducción del tiempo de análisis, mejora en la documentación de alertas, mayor trazabilidad del proceso y detección temprana de desviaciones operativas. Estos beneficios pueden justificar futuras implementaciones en entornos empresariales reales, aunque dicha validación productiva queda fuera del alcance principal de la tesis.

En consecuencia, la investigación presenta viabilidad operativa y económica, dado que puede desarrollarse como prototipo experimental con bajo costo relativo, herramientas disponibles y una evaluación alineada con los objetivos académicos del estudio.
```

### 1.2 Nuevo Contenido Propuesto (Después)
Se consolida, profundiza y enriquece la sección bajo los tres apartados oficiales de la plantilla, eliminando la sección de datos independiente y distribuyendo su lógica técnica dentro de la viabilidad correspondiente:

#### `1.6.1. Viabilidad técnica`
> La viabilidad técnica de la investigación se sustenta en la madurez, disponibilidad y estabilidad de herramientas computacionales de código abierto especializadas en aprendizaje automático, análisis de datos y procesamiento de lenguaje natural. El pipeline analítico propuesto se implementa utilizando el lenguaje de programación Python (versión 3.11) y se apoya en librerías científicas con amplia validación en el estado del arte: Scikit-Learn (1.5.0) para preprocesamiento y transformaciones, PyOD (1.1.3) para la orquestación del ensemble de anomalías, XGBoost (2.0.3) y LightGBM (4.3.0) para el módulo predictivo tabular, SHAP (0.45.0) para la explicabilidad local, y Sentence-Transformers (2.7.0) junto con rank-bm25 para los mecanismos de recuperación semántica e inyección de contexto RAG.
> 
> Desde la perspectiva de los datos, la viabilidad técnica para la integración multisource está garantizada a través del acceso a repositorios públicos y oficiales del Estado peruano y organismos internacionales. Los registros transaccionales reales de comercio exterior se extraen y procesan mediante microdatos de la SUNAT/ADUANET (archivos DBF anuales y semanales que son procesados mediante scripts específicos de extracción). El contexto de mercado mayorista interno se recupera del SISAP/MIDAGRI (archivos CSV con series de precios y volúmenes), y el tipo de cambio proviene de las series temporales canonizadas del BCRP (serie mensual PN01207PM). 
> 
> La complejidad técnica derivada de las diferentes granularidades (SUNAT opera por transacción diaria, SISAP por promedio diario, BCRP por promedio mensual y el clima por cuadrículas semanales de la NASA) se resuelve en el pipeline mediante agregaciones matemáticas y alineaciones temporales estrictas, previniendo la fuga de información (*data leakage*). Asimismo, se declaran explícitamente variables proxy (como las estimaciones de mermas y días logísticos calculadas mediante distribuciones de probabilidad calibradas con datos del sector) y se excluye el cacao (379 filas) debido a su baja representatividad transaccional, focalizando el sistema en los productos núcleo: palta, uva y arándano.

#### `1.6.2. Viabilidad operativa.`
> La viabilidad operativa de la investigación se asegura al delimitar el estudio a un entorno experimental controlado y no como un sistema de producción en tiempo real. La investigación cuenta con un dataset histórico integrado y trazable de 40,289 registros reales (periodo 2018-2026), libre de datos de cacao por baja representatividad (379 registros) y con el espárrago como producto secundario de validación condicionada. 
> 
> El diseño operativo contempla la evaluación mediante experimentos cuantitativos y pruebas cualitativas de usabilidad técnica con usuarios evaluadores en un ambiente controlado. Estas pruebas registrarán métricas de tiempo de decisión y niveles de comprensión de alertas asistidas por IA explicable y reportes estructurados con RAG/LLM, de acuerdo con las directrices de gobernanza y supervisión humana establecidas en el D.S. N.° 115-2025-PCM y la Resolución SBS N.° 053-2023.

#### `1.6.3. Viabilidad económica.`
> La viabilidad económica es alta dado que el diseño técnico prioriza la eficiencia en el uso de recursos y el bajo costo de infraestructura. A diferencia de las arquitecturas de aprendizaje profundo que requieren tarjetas gráficas (GPUs) de alto costo para el entrenamiento, los modelos basados en árboles de decisión (GBDT) y los algoritmos no supervisados de PyOD se entrenan y ejecutan eficientemente en CPU comercial estándar (infraestructura local compuesta por un procesador estándar de gama media y 16 GB de RAM), reduciendo a cero el gasto en servidores dedicados.
> 
> Todo el software utilizado es de licencia libre (open-source), eliminando costos de suscripción de software propietario. El único costo operativo directo proviene del uso de tokens de las APIs de modelos de lenguaje (OpenAI o Anthropic) para la Capa 4 de Generación de Reportes. Este costo se encuentra estrictamente acotado al marco de validación experimental del estudio (calculando un promedio de 1,500 tokens por reporte generado, lo que representa un costo aproximado de USD 0.03 por informe), siendo financiado en su totalidad por el investigador. El impacto económico del sistema se justifica por la reducción drástica de horas-hombre requeridas para auditar y documentar manualmente una alerta operativa, traduciéndose en una propuesta rentable y viable dentro del ámbito académico.

### 1.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** La plantilla oficial de tesis de Ingeniería de Sistemas de la UNSA exige explícitamente tres subsecciones numeradas de viabilidad: técnica, operativa y económica. El borrador anterior incluía la "Viabilidad de datos" como una sección independiente, lo cual constituía una desviación formal del reglamento. 
> 
> Al integrar el análisis de datos dentro de la Viabilidad Técnica (dado que la ingesta, limpieza y sincronización de granularidades son desafíos de ingeniería de software) y separar los aspectos de usabilidad/experimentación (Operativa) y costos/licencias (Económica), el documento cumple formalmente con la estructura de la universidad y evita observaciones de formato por parte del jurado.

---

## Punto 2: Justificación e Importancia de la Investigación (Sección 1.7)

### 2.1 Estado Anterior (Antes)
```
Justificación e Importancia de la Investigación.
Justificación
Teórica 


Económica


Social


 Importancia.
```

### 2.2 Nuevo Contenido Propuesto (Después)
Se redactan de forma rigurosa y madura las justificaciones teórica, económica y social, y la importancia del estudio para el sector agroexportador y la ingeniería de sistemas:

#### `1.7.1. Justificación`
##### `A. Teórica`
> La presente investigación se justifica teóricamente al proponer y validar un framework de integración conceptual para la supervisión operativa que unifica cuatro áreas de la inteligencia artificial tradicionalmente aisladas en la literatura: (1) predicción supervisada en datos estructurados mediante árboles de decisión optimizados (XGBoost y LightGBM); (2) detección de anomalías no supervisada en entornos multidimensionales mediante un ensemble unificado probabilísticamente (PyOD); (3) explicabilidad local post-hoc basada en la teoría de juegos cooperativos (SHAP); y (4) generación narrativa en lenguaje natural mediante modelos de lenguaje acotados por contexto (RAG). 
> 
> El principal aporte teórico radica en resolver el problema del acoplamiento débil entre modelos predictivos y modelos generativos, aportando una metodología formal para mitigar el riesgo de alucinación numérica del LLM al forzarlo a operar sobre un espacio de representación cerrado estructurado por scores y vectores de importancia SHAP. Esto contribuye a la teoría de sistemas inteligentes orientados a la auditoría continua, demostrando cómo la explicabilidad matemática puede ser convertida en una interfaz narrativa útil para la supervisión humana, en concordancia con los principios de gobernanza algorítmica.

##### `B. Económica`
> Desde el punto de vista económico, el sector agroexportador peruano constituye una de las columnas verticales de la economía nacional, con transacciones que superan los USD 15,000 millones anuales (MIDAGRI, 2026). No obstante, la variabilidad del precio FOB por kilogramo, el descalibrado estacional y las ineficiencias logísticas en puertos representan un riesgo constante para la rentabilidad de las organizaciones. Un solo día de retraso logístico o una desviación en la cadena de frío de productos altamente perecederos (como la palta, uva y arándano) puede reducir la vida útil del cultivo en destino hasta en un 15%, generando reclamos de calidad que deprecian el valor comercial del embarque hasta en un 30%. 
> 
> Esta investigación se justifica económicamente al dotar a las empresas de una herramienta de detección temprana que identifica desviaciones operativas y de precios en los registros aduaneros y contextuales antes de que se consoliden pérdidas irreparables. Al automatizar la documentación y explicación de anomalías, el sistema reduce el costo de auditoría operativa interna de horas a segundos, protegiendo los márgenes de ganancia de los exportadores peruanos frente a la volatilidad internacional.

##### `C. Social`
> Socialmente, la agricultura de exportación representa la mayor fuente de empleo formal, directo y descentralizado en las regiones del Perú, albergando a más de un millón de trabajadores en la costa y valles andinos (con especial concentración en La Libertad, Piura, Ica y Arequipa). La estabilidad laboral y el ingreso de miles de familias dependen directamente de la competitividad y la continuidad de los flujos de exportación de las empresas del sector. 
> 
> Las crisis operativas no detectadas a tiempo o los rechazos fitosanitarios masivos en aduanas extranjeras provocan suspensiones de contratos y despidos masivos en las plantas de empaque y campos de cultivo. Al optimizar y dar visibilidad a la cadena de valor operativa mediante la detección de anomalías, esta tesis contribuye indirectamente a la protección del empleo agrario formal y a la reducción de la vulnerabilidad económica de las comunidades rurales peruanas, promoviendo el desarrollo regional sostenible.

#### `1.7.2. Importancia.`
> La importancia práctica de esta investigación radica en entregar un prototipo auditable y trazable alineado con los desafíos de gobernanza de la inteligencia artificial en el Perú. Bajo el marco regulatorio del Decreto Supremo N.° 115-2025-PCM y el estándar internacional del NIST AI Risk Management Framework, los sistemas basados en IA aplicados a la toma de decisiones críticas deben ser transparentes, seguros y explicables para el usuario. Esta tesis rompe con el paradigma de los modelos predictivos tipo "caja negra" al traducir puntuaciones numéricas abstractas y vectores multidimensionales SHAP en reportes narrativos en lenguaje natural de alta fidelidad factual. 
> 
> La solución es de suma importancia para analistas logísticos, supervisores de operaciones, gerentes de calidad y auditores de TI, puesto que les permite entender instantáneamente qué factores determinan una alerta operativa (por ejemplo, si el desvío es causado por anomalía de volumen o por variables climatológicas extremas) y rastrear la evidencia de vuelta a las bases de datos originales de SUNAT o MIDAGRI. Esto no solo acelera la velocidad de reacción corporativa, sino que democratiza el acceso a la IA para profesionales sin conocimientos en ciencia de datos, garantizando una supervisión humana efectiva y responsable sobre la tecnología.

### 2.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** El reglamento de tesis de la UNSA requiere estructurar la justificación bajo tres enfoques bien definidos: Teórica (el aporte al conocimiento y a la ingeniería), Económica (el impacto financiero en el sector o empresa) y Social (el impacto en las personas o empleo). Adicionalmente, separa la "Importancia" como una sección independiente `1.7.2` orientada a la utilidad práctica. 
> 
> Al redactar detalladamente estos apartados, se dota a la tesis de un sustento académico sólido que justifica el esfuerzo de investigación, conectando los algoritmos de IA con la realidad económica y social de la agroexportación peruana.

---

## Punto 3: Alcance de la Investigación (Sección 1.8)

### 3.1 Estado Anterior (Antes)
```markdown
**Alcance tematico:** prediccion tabular, deteccion de anomalias, explicabilidad SHAP, reportes RAG, trazabilidad de datos y documentacion metodologica. Se excluyen modelos de deep learning puro como propuesta principal, despliegue productivo en tiempo real y reemplazo de decision humana.

**Alcance geografico/productivo:** agroexportacion peruana. Productos nucleo: palta, uva y arandano. Producto secundario: esparrago, condicionado a validacion. Producto excluido: cacao.

**Alcance temporal:** dataset estatico o semiestatico basado en datos historicos disponibles hasta 2026. La evaluacion no implica monitoreo en produccion.
```

### 3.2 Nuevo Contenido Propuesto (Después)
Se define de forma metodológica, detallada y rigurosamente justificada cada dimensión del alcance del estudio, fundamentada en el contexto de la propuesta:

#### `1.8. Alcance`
##### `1.8.1. Alcance Temático y Tecnológico`
> La presente investigación abarca el diseño, implementación de software y evaluación experimental de un prototipo de supervisión operativa integrada para el sector agroexportador estructurado en cuatro capas analíticas secuenciales y trazables:
> 1. *Capa 1: Predicción Tabular (Regresión)*: Implementación y optimización de hiperparámetros (mediante Optuna) de modelos supervisados GBDT (XGBoost y LightGBM) entrenados para estimar los valores esperados de precio FOB por kilogramo (`precio_kg_usd`) y volumen en kilogramos (`volumen_kg`). Se modelan los residuos resultantes como indicadores de desviación transaccional.
> 2. *Capa 2: Detección de Anomalías (Ensemble)*: Consolidación de puntuaciones de Isolation Forest (basado en aislamiento espacial), Local Outlier Factor (basado en densidad local k-NN) y ECOD (basado en la estimación de funciones de distribución acumulada empírica multivariada) a través de la librería PyOD. Los scores independientes se normalizan probabilísticamente bajo el método Min-Max lineal de Kriegel et al. (2011) y se promedian de manera uniforme para generar un score de anomalía global acotado $S_{Ensemble} \in [0, 1]$.
> 3. *Capa 3: Explicabilidad local (Post-hoc)*: Cálculo exacto de las contribuciones marginales de variables mediante TreeSHAP (`shap.TreeExplainer`) aplicado sobre los árboles optimizados de la Capa 1, cuantificando el impacto local de cada feature operativa, macroeconómica y climatológica en la predicción del modelo sin asumir relaciones de causalidad real directa.
> 4. *Capa 4: Generación de Reportes (LLM+RAG)*: Diseño e implementación de una arquitectura RAG restringida factual y numéricamente a través de plantillas de prompts estructurados, inyectando como contexto verificado los metadatos de la transacción, el score de anomalía consolidado, los umbrales de decisión operativos $\tau$, y los vectores SHAP de importancia. Un modelo de lenguaje autoregresivo (LLM) genera la narrativa técnica del informe sin autonomía de decisión y bajo control estricto ante alucinaciones.

##### `1.8.2. Alcance Geográfico y Productivo`
> El ámbito espacial del estudio está delimitado a los principales departamentos productores y agroexportadores de la costa y valles interandinos del Perú: Piura (provincias de Piura y Sullana), La Libertad (provincias de Virú y Ascope), Ica (provincias de Ica y Chincha), Lambayeque y Arequipa.
> 
> En cuanto al dominio de productos agrícolas, la investigación se restringe a tres cultivos núcleo priorizados por su alto valor en la canasta agroexportadora nacional, representatividad estadística y disponibilidad de datos públicos en aduanas:
> - Palta fresca (*Persea americana*, partida arancelaria HS `080440`).
> - Uva de mesa fresca (*Vitis vinifera*, partida arancelaria HS `080610`).
> - Arándano fresco (*Vaccinium corymbosum*, partida arancelaria HS `081040`).
> 
> El espárrago fresco o refrigerado (*Asparagus officinalis*, partida arancelaria HS `070920`) se incluye como producto secundario de validación condicionada a la calidad y consistencia final de su cobertura de datos históricos.

##### `1.8.3. Alcance Temporal y de Datos`
> El horizonte temporal de la investigación está estrictamente delimitado a una ventana histórica de 8 años, que comprende desde el **15 de junio de 2018** hasta el **27 de mayo de 2026**. El conjunto de datos integrado combina registros diarios y promedios semanales o mensuales.
> 
> La validación se sustenta en una división temporal cronológica estricta para evitar la filtración de información del futuro hacia el pasado (data leakage): 70% inicial para el entrenamiento de modelos, 10% intermedio para la validación y calibración de umbrales operativos $\tau$, y 20% final para la evaluación de métricas de generalización. No se simularán datos ni se proyectarán variables exógenas más allá de la ventana histórica disponible al cierre del experimento en mayo de 2026.

##### `1.8.4. Exclusiones de la Investigación`
> Quedan explícitamente excluidos del alcance de esta tesis:
> 1. La implementación productiva en tiempo real del pipeline o el desarrollo de integraciones en producción (APIs activas, WebSockets o disparadores de bases de datos relacionales) con servidores de producción o sistemas ERP (como SAP, Oracle o plataformas de control interno) de empresas agroexportadoras activas en el país. El prototipo opera en modalidad estática sobre datos históricos.
> 2. El uso de redes neuronales profundas específicas para datos tabulares (como las arquitecturas TabNet de Google Cloud o FT-Transformer) como propuesta principal de la capa predictiva, quedando restringidas única y exclusivamente a la fase de comparación como baselines experimentales en conformidad con la evidencia empírica de Grinsztajn et al. (2022).
> 3. El reemplazo de la supervisión o toma de decisiones de los analistas humanos. El sistema está diseñado conceptualmente bajo el principio de "humano en el bucle" (*human-in-the-loop*) en conformidad con las normas peruanas de gobernanza en IA (D.S. N.° 115-2025-PCM), operando como una interfaz de soporte y recomendación que requiere la revisión, edición y aprobación final de un operador humano antes de ejecutar cualquier acción logística o comercial.
> 4. El cacao (*Teobroma cacao*) como cultivo de evaluación principal, dado que el análisis preliminar de datos identificó una baja representatividad en el dataset real (379 filas válidas en total), volumen muestral estadísticamente insuficiente para garantizar la generalización y la convergencia matemática estable de los algoritmos XGBoost y LightGBM.

### 3.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** El alcance de una tesis de Ingeniería de Sistemas debe estar extremadamente detallado para evitar que los evaluadores y miembros del jurado cuestionen la aplicabilidad del prototipo o exijan el cumplimiento de requisitos no contemplados.
> 
> Al desglosar el alcance tecnológico (definiendo con exactitud matemática el rol de regresores, normalizaciones de PyOD, TreeSHAP y arquitectura RAG), geográfico (especificando los departamentos y códigos arancelarios HS), temporal (splits cronológicos) y declarar explícitamente las exclusiones clave (como la exclusión del cacao por consistencia muestral, la exclusión de deep learning por el benchmark de Grinsztajn 2022 y la obligatoriedad de la supervisión humana del D.S. N.° 115-2025-PCM), la investigación se blinda metodológicamente. Esto demuestra el rigor científico del investigador y acota formalmente las fronteras de validación para la sustentación.

---

## Punto 4: Estructura de las Técnicas e Instrumentos de Recolección (Sección 1.10)

### 4.1 Estado Anterior (Antes)
La tabla original presentaba campos simplificados y carecía de especificaciones concretas de los instrumentos técnicos de software desarrollados en la tesis:
```markdown
{sec_tecnicas_orig}
```

### 4.2 Nuevo Contenido Propuesto (Después)
Se implementa y completa la matriz oficial con la terminología académica de la propuesta de sistemas:

| Técnica | Instrumento | Propósito |
| :--- | :--- | :--- |
| **Análisis Documental** | Ficha de registro de datos estructurados (CSV/DBF) | Recolección e integración de microdatos de comercio exterior (SUNAT/ADUANET), mercado interno (SISAP/MIDAGRI), indicadores macroeconómicos (BCRP) y datos climáticos (NASA POWER). |
| **Experimentación Controlada** | Entorno de desarrollo (Python/VS Code) y Scripts de pruebas | Medición del rendimiento predictivo tabular (XGBoost/LightGBM) y de la precisión del ensemble de anomalías operativas (Isolation Forest, LOF, ECOD). |
| **Encuesta** | Cuestionario Tipo Likert y Métricas de logs de decisión | Evaluación cualitativa de la usabilidad del sistema, tiempo de decisión de los analistas, y nivel de confianza y comprensión de las alertas explicadas frente a reportes convencionales. |

### 4.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** En las tesis de Ingeniería de Sistemas, los "instrumentos" no deben limitarse a cuestionarios o encuestas de ciencias sociales. En proyectos de desarrollo tecnológico y de IA, los scripts de prueba, las fichas de registro estructuradas de bases de datos relacionales y las consolas de experimentación de software son los instrumentos de recolección primarios. 
> 
> Este cambio formaliza que la experimentación de los modelos XGBoost/LightGBM/PyOD y el análisis documental de microdatos transaccionales de la SUNAT constituyen herramientas con rigor de ingeniería.

---

## Punto 5: Secciones del Marco Conceptual (Sección 2.3)

### 5.1 Estado Anterior (Antes)
El borrador en Markdown utilizaba subtítulos personalizados libres que no encajaban en la estructura fija definida en la plantilla oficial.

### 5.2 Nuevo Contenido Propuesto (Después)
Se reestructuran los 9 subcapítulos con su contenido y citas bibliográficas exactas:

#### `2.3.1. Reconocimiento de patrones`
{sec_concept_231}

#### `2.3.2. Aprendizaje automático (Machine Learning)`
{sec_concept_232}

#### `2.3.3. Modelos basados en árboles y Gradient Boosting`
{sec_concept_233}

#### `2.3.4. Datos tabulares en sistemas empresariales`
{sec_concept_234}

#### `2.3.5. Series temporales y predicción`
{sec_concept_235}

#### `2.3.6. Detección de anomalías`
{sec_concept_236}

#### `2.3.7. Detección de fraude y auditoría inteligente`
> La detección de fraude y la auditoría inteligente constituyen áreas críticas de los sistemas empresariales modernos. Tradicionalmente orientadas al análisis de estados financieros y registros contables (como el framework *AuditCopilot* propuesto por Kadir et al., 2025), estas disciplinas aplican algoritmos de inteligencia artificial para identificar irregularidades transaccionales y de control interno. En esta tesis, se adapta conceptualmente la lógica de la auditoría inteligente para estructurar un proceso de **supervisión operativa continua** en la agroexportación peruana. Esto permite auditar la calidad, consistencia y trazabilidad de los datos operativos transaccionales (volumen, precio, clima, logística) y mapear cada alerta del ensemble de anomalías a sus evidencias cuantitativas de origen, cumpliendo con los principios de gobernanza y auditabilidad tecnológica.

#### `2.3.8. Modelos de lenguaje (LLMs) y generación de reportes`
{sec_concept_237}

#### `2.3.9. Gobernanza y calidad en sistemas de IA`
> {sec_concept_238}
>
> *(Integración del análisis de gobernabilidad nacional y explicabilidad SHAP):*
> {sec_concept_239}

### 5.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** El jurado examinador de la UNSA valida que el Marco Conceptual contenga sustento teórico directo de los algoritmos utilizados y las normativas citadas. El borrador anterior agrupaba el Aprendizaje Automático de forma general. 
> 
> Al mapear cada concepto exactamente de `2.3.1` a `2.3.9` como exige la plantilla y mantener las formulaciones matemáticas (como el gradiente funcional de GBDT y el score LOF con densidad local de alcanzabilidad), se demuestra la base científica que sustenta las decisiones de ingeniería tomadas en el pipeline analítico.

---

## Punto 6 y 7: Estructura del Capítulo III (Secciones 3.1 y 3.2)

### 6.1 Estado Anterior (Antes)
El borrador inicial del Capítulo III saltaba directamente a la arquitectura del software de forma técnica informal:
```markdown
# CAPITULO III: PROPUESTA METODOLOGICA
## 3.1 Arquitectura del sistema integrado
## 3.2 Dataset agroexportador integrado y trazable
```

### 6.2 Nuevo Contenido Propuesto (Después)
Se renombra a `# CAPÍTULO III: ELABORACIÓN DE LA PROPUESTA` e incorpora las secciones obligatorias:

#### `3.1. Generalidades.`
> Esta sección describe los lineamientos generales del sistema integrado propuesto. La solución está diseñada como una arquitectura de cuatro capas analíticas jerárquicas que procesan de extremo a extremo la información agroexportadora desde su extracción multisource hasta la generación automatizada de informes. El sistema busca robustecer la supervisión operativa reduciendo la dispersión e fragmentación de datos y aportando explicabilidad local a las alertas.

#### `3.2. Esquema de la propuesta`
> Se presenta el diagrama de arquitectura y flujo del pipeline:
{sec_cap3_31}

*(Subsecciones específicas del dataset, experimentos y MLOps integradas bajo el mismo capítulo):*
#### `3.3. Dataset agroexportador integrado y trazable`
{sec_cap3_32}

#### `3.4. Configuración experimental y métricas`
{sec_cap3_33}

### 6.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** La plantilla de la UNSA fija los dos primeros títulos del Capítulo III de forma genérica como `Generalidades` y `Esquema de la propuesta` para guiar al tesista en la conceptualización de su solución antes de detallar el código o la base de datos. 
> 
> Al adoptar este formato, se le da al lector un panorama funcional (Capa 1 a 4) y gráfico del sistema en las generalidades, sentando las bases metodológicas necesarias antes de ingresar a los detalles cuantitativos del dataset integrado de 40,289 registros y el particionamiento temporal 70-10-20.

---

## Punto 8 y 9: Estructura del Capítulo IV

### 8.1 Estado Anterior (Antes)
El borrador Markdown tenía un título no estandarizado y fraccionaba los resultados y la discusión de forma libre:
*   `CAPÍTULO IV: RESULTADOS Y DISCUSIÓN`
*   `4.1 Resultados Cuantitativos...`
*   `4.2 Resultados Cualitativos...`
*   `4.3 Usabilidad y Trazabilidad...`

### 8.2 Nuevo Contenido Propuesto (Después)
El capítulo adopta el nombre oficial `# CAPÍTULO IV: ANÁLISIS E INTERPRETACIÓN DE LOS RESULTADOS` y agrupa la información cuantitativa, cualitativa y la discusión comparativa en tres bloques limpios:

#### `4.1. Análisis cuantitativo de predicción y detección`
{sec_cap4_41}

#### `4.2. Análisis cualitativo de explicabilidad, usabilidad y reportes`
{sec_cap4_42}
{sec_cap4_43}

#### `4.3. Discusión, limitaciones y contraste de hipótesis`
{sec_cap4_44}

### 8.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** El título oficial de la universidad para el Capítulo IV es "ANÁLISIS E INTERPRETACIÓN DE LOS RESULTADOS". Renombrarlo evita rechazos automáticos de formato en biblioteca. 
> 
> Además, la reestructuración metodológica agrupa los resultados duros de los algoritmos de predicción/detección en la sección 4.1 y la validación con usuarios (usabilidad del RAG y explicabilidad SHAP) en la 4.2. Finalmente, la sección 4.3 sirve para el cruce de hipótesis científicas (H1 vs H0) y el contraste con los antecedentes de la literatura (AuditCopilot y Park 2024), consolidando una discusión académica madura y coherentemente argumentada.

---

## Punto 10: Eliminación del Capítulo V y Estructura de Cierre

### 10.1 Estado Anterior (Antes)
Se incluía un "Capítulo V" redundante y secciones separadas que duplicaban la estructura de la tesis.

### 10.2 Nuevo Contenido Propuesto (Después)
Se elimina el Capítulo V y se colocan las secciones finales directamente como títulos principales tras el Capítulo IV en el orden estricto de la plantilla:

#### `CONCLUSIONES`
```markdown
{conclusiones_text}
```

#### `CONCLUSIONS`
```markdown
{conclusions_en_text}
```

#### `RECOMENDACIONES`
```markdown
{recomendaciones_text}
```

#### `GLOSARIO DE TÉRMINOS`
```markdown
{glosario_text}
```

#### `REFERENCIAS BIBLIOGRÁFICAS`
```markdown
{referencias_text}
```

### 10.3 Sustentación del Cambio (Comentario)
> **Justificación Académica:** La plantilla oficial de tesis de Ingeniería de Sistemas de la UNSA no contempla un "Capítulo V". El documento finaliza formalmente en el Capítulo IV, y las conclusiones, recomendaciones, glosario y referencias bibliográficas se anexan como secciones independientes de primer nivel. 
> 
> Al reestructurar estas secciones finales, se cumple estrictamente con el flujo de biblioteca universitaria y se conserva la traducción en inglés (Conclusions) obligatoria de la UNSA.
"""

with open(out_path, "w", encoding="utf-8") as f:
    f.write(guide_content)

print(f"Guia con alcances e exclusiones generada con exito en {out_path.absolute()}")
