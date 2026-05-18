# CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA

## 1.1 Descripción de la Realidad Problemática

### Contexto agroexportador y empresarial

En empresas agroexportadoras —dedicadas a la producción, acopio, procesamiento, empaque, control de calidad y comercialización internacional de productos agrícolas— la supervisión operativa constituye una actividad crítica para detectar desviaciones productivas, mermas, variaciones de precios, condiciones climáticas adversas, retrasos logísticos e incumplimientos de estándares fitosanitarios. Estas desviaciones afectan directamente la rentabilidad, continuidad operativa y competitividad internacional de la empresa.

La magnitud económica del sector refuerza la necesidad de sistemas de supervisión más oportunos y trazables. Según MIDAGRI, las agroexportaciones peruanas superaron los USD 15 013 millones al cierre de 2025, con crecimiento de 17.3% respecto al año anterior (MIDAGRI, 2026). Este dinamismo incrementa la complejidad de las cadenas agroexportadoras, que deben coordinar producción, calidad, sanidad, logística y comercio exterior bajo condiciones cambiantes de clima, demanda internacional y requisitos de destino.

En el contexto peruano, la transformación digital y la adopción de sistemas inteligentes exigen mayores niveles de gobernanza tecnológica y trazabilidad operativa. La Ley N.° 31814 y su reglamento aprobado mediante D.S. N.° 115-2025-PCM (PCM, 2025) establecen un marco general para promover el uso responsable de la inteligencia artificial, con énfasis en transparencia, supervisión humana y gestión de riesgos. Asimismo, la Resolución SBS N.° 053-2023 (SBS, 2023) se considera en esta tesis como referencia nacional de buenas prácticas para gestión de riesgo de modelos, validación y monitoreo, sin asumirla como obligación directa para empresas agroexportadoras.

En escenarios donde una empresa agroexportadora integra datos de producción, precios, clima, inventario, calidad, logística y exportación, la supervisión manual resulta operativamente limitada. Sin embargo, sistemas automatizados sin mecanismos de explicabilidad reducen la confianza organizacional y dificultan la revisión interna de decisiones. En consecuencia, surge la necesidad de sistemas integrados capaces de detectar anomalías operativas en tiempo oportuno, explicar sus causas probables y generar reportes trazables que permitan justificar cada alerta dentro de la cadena agroexportadora.

### Problemas identificados

1. **Falta de integración entre módulos operativos**: Los componentes de predicción, detección de anomalías y generación de reportes funcionan de forma independiente. Los hallazgos de un módulo no se comunican al siguiente con contexto semántico, lo que impide obtener una visión coherente del estado operativo de la empresa.

2. **Baja explicabilidad de las alertas automáticas**: Los modelos predictivos generan puntuaciones de riesgo sin justificar qué variables operativas (mermas, retrasos, desvíos de calidad) determinaron el resultado. Los gestores y auditores internos requieren explicaciones comprensibles para tomar decisiones correctivas.

3. **Reportería manual e ineficiente**: La detección de anomalías operativas —en producción, inventario, logística o calidad— exige la redacción manual de informes por parte de analistas, con riesgo de inconsistencia, errores de interpretación y demoras que comprometen la capacidad de respuesta empresarial.

4. **Falta de trazabilidad en la cadena de decisiones**: La gobernanza tecnológica y la auditoría interna requieren poder rastrear el fundamento de cada alerta desde el dato de origen (sensor, ERP, reporte de campo) hasta el informe ejecutivo. Los sistemas en silos no permiten esta trazabilidad end-to-end.

5. **Ausencia de validación cruzada entre dimensiones operativas**: Una anomalía detectada en producción no se correlaciona automáticamente con posibles irregularidades en inventario, logística o calidad. Esta falta de perspectiva multidimensional genera falsos positivos que saturan a los analistas y falsos negativos que pasan desapercibidos.

6. **Incapacidad de anticipar riesgos operativos**: Los sistemas reactivos detectan anomalías ya ocurridas, pero no predicen tendencias de riesgo emergentes. La ausencia de módulos predictivos integrados impide anticipar desviaciones estacionales, cuellos de botella logísticos o deterioro progresivo de indicadores de calidad.

## 1.2 Problema Principal

**¿Cómo mejorar la detección, explicación y documentación de anomalías operativas en empresas agroexportadoras peruanas mediante un sistema integrado de inteligencia artificial explicable que combine predicción tabular, detección de anomalías, explicabilidad y generación de reportes trazables?**

### Sub-problemas

- ¿Qué variables operativas, climáticas, comerciales y fitosanitarias pueden utilizarse para caracterizar el comportamiento normal y anómalo de procesos agroexportadores peruanos?
- ¿Qué arquitectura de inteligencia artificial permite integrar predicción tabular, detección de anomalías, explicabilidad y generación de reportes en un flujo operativo trazable?
- ¿De qué manera la explicabilidad mediante SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley) contribuye a que supervisores operativos comprendan las causas probables de una alerta?
- ¿Cómo generar reportes automáticos que sean comprensibles, accionables y trazables sin permitir que el modelo de lenguaje tome decisiones o invente información?
- ¿Cómo evaluar si el sistema integrado mejora la trazabilidad, comprensión de alertas y tiempo de decisión frente al uso de componentes aislados?

## 1.3 Objetivos

### 1.3.1 Objetivo Principal

Diseñar, implementar y evaluar un sistema integrado de supervisión operativa basado en inteligencia artificial explicable para detectar anomalías en datos agroexportadores, explicar los factores asociados mediante SHAP y generar reportes trazables que apoyen la toma de decisiones en empresas agroexportadoras peruanas.

### 1.3.2 Objetivos Específicos

1. **Fuentes de datos y dominio**: Identificar y documentar fuentes de datos públicas y sintéticas aplicables a la supervisión operativa agroexportadora, considerando variables de precios, volúmenes, clima, comercio exterior y cumplimiento fitosanitario.

2. **Arquitectura y modularidad**: Diseñar una arquitectura modular de cuatro capas (predicción → detección → explicación → reporte) que integre modelos tabulares, detectores de anomalías, explicabilidad y generación de reportes trazables.

3. **Predicción y detección robusta**: Implementar modelos de predicción y detección de anomalías sobre datos agroexportadores públicos y sintéticos, utilizando algoritmos adecuados para datos tabulares y series temporales.

4. **Explicabilidad verificable**: Integrar SHAP (Lundberg & Lee, 2017) para identificar las variables que más contribuyen a cada alerta generada por el sistema.

5. **Generación de reportes trazables**: Diseñar un componente LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación) que redacte explicaciones operativas basadas exclusivamente en evidencias estructuradas del sistema.

6. **Evaluación integrada**: Evaluar el sistema integrado mediante métricas técnicas, trazabilidad documental y prueba de comprensión/tiempo de decisión con usuarios o evaluadores simulados.

## 1.4 Hipótesis de la Investigación

**Hipótesis General (H1)**: Un sistema integrado de predicción, detección de anomalías, explicabilidad y generación de reportes trazables mejora la trazabilidad de decisiones, la comprensión de alertas y el tiempo de decisión de supervisores operativos frente al uso de componentes aislados.

**Hipótesis Nula (H0)**: No existe diferencia significativa entre el sistema integrado y los componentes aislados en trazabilidad de decisiones, comprensión de alertas o tiempo de decisión de supervisores operativos.

**Sub-hipótesis**:

- **H1a**: El uso combinado de modelos tabulares y detectores de anomalías permite identificar desviaciones operativas con mejor rendimiento que detectores individuales aplicados de forma aislada.
- **H1b**: Las explicaciones SHAP incrementan la comprensión de las alertas por parte de supervisores operativos, al identificar variables relevantes y dirección de impacto.
- **H1c**: Los reportes generados mediante RAG a partir de evidencias estructuradas presentan mayor trazabilidad y consistencia que reportes generados sin recuperación de contexto.
- **H1d**: El sistema integrado reduce el tiempo requerido para interpretar una alerta operativa frente a un flujo basado en tablas, gráficos o salidas técnicas aisladas.

## 1.5 Variables e Indicadores

### 1.5.1 Variable Independiente

**Tipo de sistema de supervisión operativa (variable categórica)**:
- VI1: Sistema integrado (predicción tabular + detección de anomalías + SHAP + LLM+RAG)
- VI2: Componentes aislados (salidas técnicas independientes por módulo)

### 1.5.2 Variables Dependientes

**VD1: Rendimiento de detección**
- Indicadores: ROC-AUC (Receiver Operating Characteristic Area Under the Curve - Área Bajo la Curva de Característica Operativa del Receptor), Precisión, Recall, F1-Score (Medida Armónica de Precisión y Exhaustividad), PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad)
- Criterio de aceptación: superar el baseline individual o justificar rendimiento equivalente con mayor trazabilidad

**VD2: Calidad de explicabilidad**
- Indicadores: cobertura top-k SHAP, consistencia cualitativa, claridad de variables explicativas
- Criterio de aceptación: las variables principales deben permitir explicar operativamente la alerta

**VD3: Calidad de reportes generados**
- Indicadores: completitud, consistencia, accionabilidad, coherencia textual y correspondencia con evidencias
- Criterio de aceptación: evaluación manual ≥ 4/5 en rúbrica de reporte trazable

**VD4: Comprensión y tiempo de decisión del supervisor**
- Indicadores: tiempo-a-decisión (segundos), comprensión de alerta (Likert 1–5), decisión final correcta
- Criterio de aceptación: reducción de tiempo y mejora de comprensión respecto a componentes aislados

**VD5: Trazabilidad documental**
- Indicadores: porcentaje de alertas con dato, modelo, score, umbral, explicación, fuente recuperada y reporte generado
- Criterio de aceptación: ≥ 95% de alertas con campos de trazabilidad completos

## 1.6 Viabilidad de la Investigación

### 1.6.1 Viabilidad Técnica

**Disponibilidad de tecnologías**: El stack tecnológico es completamente open-source y maduro: XGBoost (Chen & Guestrin, 2016) y LightGBM (Ke et al., 2017) para predicción tabular; PyOD (Zhao et al., 2019) para ensemble de anomalías con acceso a Isolation Forest (Liu et al., 2008), LOF (Local Outlier Factor - Factor de Anomalía Local) (Breunig et al., 2000) y Deep SVDD (Ruff et al., 2018); SHAP (Lundberg & Lee, 2017) para explicabilidad; APIs de LLM (Anthropic Claude, OpenAI GPT-4) o modelos locales (Llama 3) para generación de reportes.

**Datos disponibles**: Se contemplan tres niveles de datos. El primer nivel corresponde a fuentes públicas oficiales: MIDAGRI para agroexportaciones, precios y boletines sectoriales; SENAMHI para variables climáticas; SENASA para requisitos fitosanitarios; SUNAT para exportaciones; INEI para indicadores económicos; FAOSTAT y UN Comtrade para validación internacional. El segundo nivel corresponde a un dataset sintético agroexportador documentado, construido con variables operativas plausibles y etiquetas de anomalía controladas. El tercer nivel, opcional, corresponde a datos privados de una empresa agroexportadora bajo acuerdo de confidencialidad. Como referencia metodológica complementaria puede utilizarse el BAF Benchmark (Jesus et al., 2022), no como evidencia directa del dominio agroexportador, sino como benchmark tabular desbalanceado con drift temporal.

**Riesgos técnicos identificados**: La latencia de SHAP en datasets grandes (>1M filas) puede mitigarse con los métodos de aproximación TreeSHAP. La variabilidad en salidas de LLMs (Large Language Models - Modelos de Lenguaje de Gran Tamaño) requiere prompt engineering robusto y restricción mediante RAG. La mitigación incluye pruebas piloto en subconjuntos de datos y benchmarking iterativo.

### 1.6.2 Viabilidad Operativa

**Timeline**: Fase 1 (meses 1–2): preparación de datos, implementación de arquitectura base. Fase 2 (meses 2–3): entrenamiento de modelos, validación experimental. Fase 3 (mes 4): test de usabilidad con auditores voluntarios. Fase 4 (mes 5): análisis de resultados, escritura y defensa.

**Presupuesto estimado**: Infraestructura GPU cloud y APIs LLM: USD 500–1,000. Stack open-source: USD 0. Incentivos para participantes del test de usabilidad: USD 200–300. Total aproximado: USD 800–1,300.

### 1.6.3 Viabilidad Económica

La viabilidad económica se justifica por la relevancia del sector agroexportador peruano y por el costo operativo asociado a decisiones tardías ante desviaciones de precio, volumen, calidad, clima o logística. MIDAGRI reportó agroexportaciones por USD 15 013 millones al cierre de 2025 (MIDAGRI, 2026), por lo que incluso mejoras marginales en detección temprana, trazabilidad y tiempo de respuesta pueden representar beneficios operativos relevantes. En esta fase, los beneficios económicos se tratarán como escenarios exploratorios y no como resultados finales hasta contar con evaluación experimental y supuestos documentados.

## 1.7 Justificación e Importancia de la Investigación

### 1.7.1 Justificación Teórica

La revisión sistemática de la literatura revela avances importantes en modelos tabulares, detección de anomalías, explicabilidad y generación de reportes mediante LLMs. Sin embargo, estos componentes suelen estudiarse de forma aislada y en dominios distintos al agroexportador. Trabajos de auditoría financiera o fraude contable, como AuditCopilot (Kadir et al., 2025), se utilizan solo como antecedentes metodológicos sobre automatización de reportes y detección de anomalías, no como eje del dominio de aplicación. La brecha central de esta tesis es la ausencia de una arquitectura integrada y trazable para supervisión operativa agroexportadora peruana que combine fuentes públicas oficiales, datos sintéticos documentados, predicción tabular, detección de anomalías por ensemble, explicabilidad SHAP y reportes basados en evidencia bajo restricción anti-alucinación.

**Aporte original específico**: Esta tesis constituye, en el conocimiento del autor (verificado mediante búsqueda sistemática documentada en `docs/busqueda-sistematica-gap.md`), la primera arquitectura integrada de cuatro capas (GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) + ensemble Isolation Forest/LOF/ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica) + TreeSHAP + LLM-RAG con restricción anti-alucinación) evaluada sobre datos agroexportadores peruanos públicos y sintéticos, con trazabilidad documental diseñada conforme al D.S. N° 115-2025-PCM y los principios del NIST AI RMF (NIST, 2023).

Esta tesis aporta a la literatura y a la práctica profesional cuatro elementos diferenciados y verificables:

1. **Aporte arquitectónico**: Un modelo conceptual integrado de cuatro capas para supervisión operativa agroexportadora, donde la separación estricta de responsabilidades entre detección determinista (GBDT + ensemble) y narración asistida (LLM-RAG anclado en vectores SHAP) constituye un patrón de diseño anti-alucinación replicable en otros dominios regulados.

2. **Aporte de datos abiertos**: Un protocolo público y reproducible de construcción y documentación de un dataset sintético agroexportador, calibrado con rangos plausibles de MIDAGRI/SENAMHI/SENASA y descrito según Datasheets for Datasets (Gebru et al., 2021), disponible para la comunidad como referencia metodológica.

3. **Aporte de evaluación**: Una metodología de evaluación dual que combina métricas técnicas (PR-AUC, F1, ROC-AUC) con métricas de utilidad operativa (tiempo-a-decisión, comprensión Likert, trazabilidad documental) y aplica pruebas estadísticas formales (Wilcoxon signed-rank, t-Student apareado) para contrastar las sub-hipótesis H1a–H1d.

4. **Aporte regulatorio**: Una primera traducción operativa de los principios del D.S. N° 115-2025-PCM al diseño de un sistema de IA empresarial peruano, mostrando cómo cada capa de la arquitectura puede mapear con requisitos de explicabilidad, supervisión humana y trazabilidad documental.

### 1.7.2 Justificación Económica

La automatización inteligente de la supervisión operativa tiene impacto económico potencial al reducir el tiempo de análisis, mejorar la detección temprana de desviaciones y facilitar la documentación de decisiones. En empresas agroexportadoras, las alertas oportunas sobre precios, volúmenes, clima, mermas, calidad o logística pueden apoyar decisiones correctivas antes de que la desviación se convierta en pérdida operativa o incumplimiento comercial. La escalabilidad del sistema permite adaptarlo a empresas de distintos tamaños mediante fuentes públicas, datos internos o datos sintéticos documentados.

### 1.7.3 Justificación Social

El Decreto Supremo N° 115-2025-PCM, reglamento de la Ley N° 31814 de Inteligencia Artificial del Perú, proporciona un marco nacional para promover el uso responsable de la IA, incluyendo transparencia, supervisión humana y gestión de riesgos (PCM, 2025). A nivel internacional, el Reglamento (UE) 2024/1689 —EU AI Act— refuerza la importancia de documentar sistemas de IA, especialmente cuando sus resultados afectan decisiones relevantes (Parlamento Europeo y Consejo, 2024). El sistema propuesto incorpora estos principios mediante explicabilidad, trazabilidad documental y revisión humana de reportes.

Adicionalmente, una detección temprana de anomalías operativas protege a las empresas agroexportadoras de tamaño medio —que representan la mayoría del sector exportador peruano— frente a pérdidas acumuladas por mermas, incumplimientos de calidad y fallas logísticas que, sin sistemas de alerta temprana, solo se visibilizan en los estados financieros al cierre del período.

### 1.7.4 Importancia

**Nivel académico**: Contribución a los campos de ML interpretable, detección de anomalías, supervisión operativa y gobernanza de IA aplicada a cadenas agroexportadoras.

**Nivel profesional**: Guía de referencia para empresas agroexportadoras que busquen incorporar IA explicable en procesos de control operativo, calidad, logística y toma de decisiones.

**Nivel institucional**: Fortalece el posicionamiento de la UNSA en investigación aplicada en IA responsable y establece vínculos de colaboración con el sector financiero regional.

## 1.8 Alcance

**Alcance temático**: Predicción con GBDT, detección de anomalías mediante ensemble, explicabilidad SHAP, generación de reportes con LLM+RAG, documentación de datasets y trazabilidad de alertas operativas. **Excluye**: modelos de Deep Learning puro para datos tabulares como propuesta principal, implementación productiva en tiempo real, reemplazo de la decisión humana y análisis legal profundo de regulación sectorial.

**Alcance geográfico**: Empresas agroexportadoras peruanas, con énfasis en productos representativos como arándanos, uvas, paltas, cacao y espárragos. La investigación utiliza fuentes públicas oficiales y dataset sintético documentado; los datos privados de empresa quedan como extensión futura u opcional.

**Alcance temporal**: Evaluación en dataset estático o semiestático, sin monitoreo en producción. Estudio en 5 meses. Evaluación de comprensión y tiempo de decisión con supervisores, auditores internos o evaluadores simulados según disponibilidad.

## 1.9 Línea, Tipo y Nivel de la Investigación

### 1.9.1 Línea de Investigación

La presente investigación se enmarca en la línea de **Inteligencia Artificial e Ingeniería de Software Aplicada** de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Nacional de San Agustín de Arequipa. Específicamente, se inscribe en el área de sistemas inteligentes para la toma de decisiones en organizaciones empresariales, con énfasis en gobernanza tecnológica y conformidad regulatoria.

### 1.9.2 Marco Epistemológico

La investigación adopta un enfoque **post-positivista** (Creswell & Creswell, 2018): asume que los fenómenos operativos del dominio agroexportador (precios, volúmenes, mermas, condiciones climáticas, cumplimiento fitosanitario, tiempos logísticos) son medibles de manera objetiva mediante variables cuantitativas y rangos plausibles documentables. Al mismo tiempo, se reconoce que la evaluación de utilidad operativa de un sistema de supervisión asistida por IA incorpora componentes subjetivos —comprensión, confianza, accionabilidad del reporte— que requieren triangulación entre métricas cuantitativas (PR-AUC, tiempo-a-decisión) y métricas cualitativas (escalas Likert, rúbricas de evaluación). Esta postura justifica la combinación metodológica utilizada y excluye afirmaciones de causalidad en sentido experimental estricto, sustituyéndolas por afirmaciones sobre **efecto diferencial** entre condiciones experimentales controladas (sistema integrado vs. sistema con componentes aislados).

### 1.9.3 Tipo de Investigación

La investigación es de tipo **aplicada**, dado que utiliza conocimiento teórico y metodológico existente en machine learning, detección de anomalías, explicabilidad algorítmica y modelos de lenguaje para diseñar, implementar y evaluar un sistema concreto que resuelve un problema identificado en el contexto empresarial agroexportador peruano. No se busca generar nuevos algoritmos de base, sino integrar y validar una arquitectura que produce valor operativo y regulatorio verificable.

### 1.9.4 Nivel de Investigación

El nivel de la investigación es **explicativo-evaluativo**. Se parte de un diagnóstico descriptivo del problema (sistemas de supervisión fragmentados y sin trazabilidad), se propone una solución arquitectónica basada en literatura existente, y se diseñan experimentos controlados que permiten evaluar la relación entre integración de componentes y mejoras en trazabilidad, comprensión operativa y tiempo de decisión. La evaluación combina métricas cuantitativas (PR-AUC, F1-Score, cobertura de trazabilidad, tiempo-a-decisión) y cualitativas (escala Likert con supervisores o evaluadores). Las conclusiones explicativas se derivan del análisis ablativo (Experimento E5) que aísla la contribución de cada capa al rendimiento global, distinguiendo así qué componente arquitectónico es responsable de cada mejora observada.

### 1.9.5 Diseño de la Investigación

El diseño es **cuasi-experimental con grupos contrabalanceados** para la evaluación de utilidad operativa (VD4): cada participante del estudio de usabilidad evalúa ambas condiciones (sistema integrado y componentes aislados) en orden aleatorizado, controlando por el efecto de aprendizaje mediante diseño within-subjects. Para las variables técnicas (VD1, VD2, VD3, VD5) el diseño es **comparativo en condiciones controladas**: el mismo dataset, mismas particiones train/test temporales (sin solapamiento) y misma semilla aleatoria se aplican a todas las configuraciones experimentales (E1–E5), variando únicamente la condición evaluada (detector individual vs. ensemble, sin SHAP vs. con SHAP, sin RAG vs. con RAG, sin pipeline integrado vs. con pipeline integrado).

## 1.10 Técnicas e Instrumentos de Recolección de Información

### 1.10.1 Técnicas

Las técnicas de recolección de información utilizadas en esta investigación son:

1. **Revisión sistemática de literatura**: Búsqueda estructurada en bases de datos académicas (IEEE Xplore, ACM Digital Library, arXiv, Google Scholar, Scopus) utilizando términos de búsqueda como "anomaly detection ensemble", "GBDT tabular data", "SHAP explainability", "RAG generated reports", "AI governance Peru" y "agricultural anomaly detection". Se aplican criterios de inclusión: publicaciones entre 2017 y 2026, en inglés o español, con evaluación empírica o propuesta metodológica verificable.

2. **Análisis documental**: Revisión de fuentes oficiales nacionales (MIDAGRI, SENASA, SENAMHI, SUNAT, INEI), regulaciones nacionales sobre IA (Ley N° 31814 y D.S. N° 115-2025-PCM) y marcos internacionales de gobernanza (EU AI Act 2024, NIST AI RMF 1.0). La Resolución SBS N° 053-2023 se considera solo como referencia metodológica de gestión de riesgo de modelos.

3. **Experimentación controlada**: Diseño de experimentos comparativos con el sistema integrado versus componentes aislados, evaluados sobre datos públicos/sintéticos agroexportadores. El BAF Benchmark (Jesus et al., 2022) puede emplearse solo como benchmark metodológico complementario para datos tabulares desbalanceados.

4. **Evaluación con usuarios o evaluadores simulados**: Prueba de comprensión y tiempo de decisión con supervisores, auditores internos, estudiantes avanzados o evaluadores simulados mediante protocolo de tareas cronometradas y cuestionario post-tarea.

### 1.10.2 Instrumentos

| Instrumento | Propósito | Variable que mide |
|---|---|---|
| Fuentes públicas oficiales | Construir contexto, variables y rangos plausibles del dominio agroexportador | VD1, VD5 |
| Dataset sintético agroexportador | Evaluación controlada de predicción, anomalías y reportes | VD1, VD2, VD3 |
| BAF Benchmark (Jesus et al., 2022) | Benchmark metodológico complementario para datos tabulares desbalanceados | VD1 |
| Cuestionario de comprensión (Likert 1–5) | Evaluar claridad de explicaciones y reportes para supervisores | VD2, VD3, VD4 |
| Registro de tiempo-a-decisión | Medir segundos requeridos para interpretar y decidir sobre una alerta | VD4 |
| Checklist de trazabilidad | Verificar dato, modelo, score, umbral, explicación, fuente y reporte por alerta | VD5 |

## 1.11 Cronograma de Actividades

| Actividad | Mes 1 | Mes 2 | Mes 3 | Mes 4 | Mes 5 |
|---|:---:|:---:|:---:|:---:|:---:|
| Revisión bibliográfica y marco teórico | ✓ | | | | |
| Obtención y preprocesamiento de datos | ✓ | ✓ | | | |
| Implementación Capa 1 (Predicción Tabular GBDT) | | ✓ | | | |
| Implementación Capa 2 (Ensemble anomalías) | | ✓ | ✓ | | |
| Implementación Capa 3 (SHAP) | | | ✓ | | |
| Implementación Capa 4 (LLM+RAG) | | | ✓ | | |
| Integración del pipeline completo | | | ✓ | | |
| Experimentos comparativos (baselines) | | | | ✓ | |
| Prueba de usabilidad con auditores | | | | ✓ | |
| Análisis de resultados y discusión | | | | ✓ | |
| Redacción del documento final | | | | | ✓ |
| Revisión del asesor y correcciones | | | | | ✓ |
| Presentación y defensa | | | | | ✓ |

## 1.12 Limitaciones de la Investigación

La presente investigación adopta un enfoque transparente respecto a sus limitaciones, declarando de forma explícita las amenazas a la validez que podrían afectar la interpretación o generalización de los resultados. Esta declaración es un requisito de rigor académico y constituye una práctica estándar en la literatura de IA responsable.

### 1.12.1 Limitaciones de validez externa

**Dataset sintético**: La evaluación principal se realiza sobre un dataset sintético agroexportador documentado con criterios de Datasheets for Datasets (Gebru et al., 2021). Aunque las distribuciones y mecanismos de inyección de anomalías se calibran con rangos plausibles tomados de fuentes oficiales (MIDAGRI, SENAMHI, SENASA, SUNAT), un dataset sintético no reproduce todas las dinámicas operativas, sesgos de medición y patrones de drift presentes en datos reales de una empresa agroexportadora. Por lo tanto, los resultados deben interpretarse como evidencia de viabilidad arquitectónica y comportamiento esperado bajo condiciones controladas, no como predictores directos del rendimiento en producción.

**Generalización a otros sectores**: La arquitectura se diseña y evalúa para el dominio agroexportador peruano. Su extensión a otros sectores (minería, manufactura, retail) requiere recalibración de variables, ajustes en el dataset y nueva validación experimental antes de afirmar transferibilidad.

**Generalización a otros países**: El marco regulatorio que orienta el diseño (D.S. N° 115-2025-PCM, Ley N° 31814) corresponde al contexto peruano. Aunque los principios subyacentes (transparencia, supervisión humana, gestión de riesgos) son compatibles con marcos internacionales como el EU AI Act y el NIST AI RMF, la aplicabilidad directa del sistema en otras jurisdicciones requiere una revisión de conformidad específica.

### 1.12.2 Limitaciones de validez interna

**Tamaño de muestra del estudio de usabilidad**: La evaluación de VD4 (comprensión y tiempo de decisión) requiere participantes humanos con perfil de supervisor operativo, analista de calidad o auditor interno. La disponibilidad realista en el contexto de una tesis individual es de 15 a 20 participantes mediante un diseño within-subject (cada participante evalúa ambas condiciones en orden aleatorizado). Con este tamaño, los resultados de VD4 deben reportarse como exploratorios, calculando intervalos de confianza y tamaño de efecto (Cohen's d) en lugar de afirmar significancia estadística con potencia plena.

**Sesgo del evaluador**: Los participantes en el estudio de usabilidad pueden conocer la procedencia del sistema integrado, lo cual puede introducir un sesgo de expectativa. Se mitiga mediante: (a) orden contrabalanceado de presentación de las condiciones, (b) cuestionario post-tarea con preguntas no directivas, y (c) registro automático de tiempo-a-decisión (no dependiente de auto-reporte).

**Variabilidad del LLM**: El módulo de generación de reportes utiliza un modelo de lenguaje cuyas respuestas presentan variación estocástica entre ejecuciones, incluso con el mismo prompt. Para mitigar este efecto se fija el parámetro de temperatura (temperature = 0.2), se documenta la versión exacta del modelo utilizado y se reportan los resultados como promedio sobre al menos 3 generaciones por alerta.

### 1.12.3 Limitaciones de validez de constructo

**Definición de "anomalía operativa"**: La etiqueta `etiqueta_anomalia` del dataset sintético se construye mediante un protocolo de inyección controlada, lo que define la anomalía operativamente a partir de reglas predeterminadas. En la práctica empresarial, la categorización de un registro como "anómalo" depende de criterios contextuales no siempre formalizables. El sistema, por tanto, evalúa su capacidad de detectar desviaciones según reglas declaradas, no como reemplazo del juicio experto.

**Métrica de comprensión (VD2)**: La "claridad de variables explicativas" se mide mediante una escala Likert 1–5 que captura percepción subjetiva del evaluador. Esta métrica está expuesta a sesgos de halo y aquiescencia. Se complementa con métricas objetivas (cobertura top-k SHAP) para triangulación.

### 1.12.4 Limitaciones técnicas y de recursos

**Dependencia de APIs comerciales de LLM**: La generación de reportes puede emplear servicios comerciales (Anthropic Claude, OpenAI GPT-4) cuya versión, costo y disponibilidad pueden variar durante el horizonte experimental. Se documenta la versión exacta utilizada en cada experimento y se evalúa la posibilidad de réplica con modelos locales (Llama 3) como verificación cruzada.

**Recursos computacionales**: La investigación se ejecuta en infraestructura GPU cloud limitada por presupuesto académico. Esto restringe la exploración exhaustiva de hiperparámetros y limita el tamaño del dataset experimental a un rango medio (2,000–5,000 registros). La escalabilidad a millones de registros queda como trabajo futuro.

## 1.13 Declaración de Intereses y Aspectos Éticos

Se declara que el autor de esta investigación no mantiene relación contractual, comercial o financiera con empresas agroexportadoras específicas que pudiera condicionar la independencia metodológica de los resultados. La investigación se desarrolla en el marco de la formación de pregrado en la Universidad Nacional de San Agustín de Arequipa y no cuenta con financiamiento externo.

El uso de datos en esta tesis se restringe a fuentes públicas oficiales (MIDAGRI, SENAMHI, SENASA, SUNAT, INEI, FAOSTAT, UN Comtrade) y a un dataset sintético generado por el autor con un protocolo documentado. No se utilizan datos personales, datos de empresas bajo confidencialidad ni datos que pudieran exponer información sensible de actores del sector.

El estudio de usabilidad con participantes humanos (VD4) sigue los principios de consentimiento informado, voluntariedad, anonimato y derecho de retiro establecidos en la Declaración de Helsinki y adaptados al contexto de investigación en ingeniería. El protocolo completo, formulario de consentimiento y cuestionario figuran en el Anexo A.

El uso de herramientas de IA durante la elaboración de la tesis (búsqueda bibliográfica, revisión de redacción, apoyo en codificación) se documenta en el Anexo D, conforme a las prácticas emergentes de transparencia académica sobre el uso de IA generativa en investigación.

---

