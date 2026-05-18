---
title: "Sistema Integrado de Supervisión Operativa con Inteligencia Artificial Explicable para Empresas Agroexportadoras Peruanas"
author: "Yoset Cozco Mauri"
date: "2026"
bibliography: refs.bib
csl: apa.csl
---

---

**UNIVERSIDAD NACIONAL DE SAN AGUSTÍN DE AREQUIPA**

Facultad de Ingeniería de Producción y Servicios

Escuela Profesional de Ingeniería de Sistemas

---

**SISTEMA INTEGRADO DE SUPERVISIÓN OPERATIVA CON INTELIGENCIA ARTIFICIAL EXPLICABLE PARA LA DETECCIÓN DE ANOMALÍAS Y GENERACIÓN DE REPORTES TRAZABLES EN EMPRESAS AGROEXPORTADORAS PERUANAS**

---

Tesis presentada por el Bachiller:

**Cozco Mauri, Yoset**

Para optar el Título Profesional de Ingeniero de Sistemas

Asesor:

**Dr. Víctor Manuel Cornejo Aparicio**

---

**Arequipa – Perú**

**2026**

---

# DEDICATORIA

*(Por completar — dedicatoria personal del autor)*

---

# AGRADECIMIENTOS

*(Por completar — agradecimientos al asesor, jurado, institución colaboradora y familiares)*

---

# PRESENTACIÓN

La presente investigación tiene como propósito el diseño, implementación y evaluación de un sistema integrado de supervisión operativa para empresas agroexportadoras peruanas, que combina técnicas de aprendizaje automático, detección de anomalías, explicabilidad algorítmica y generación automática de reportes trazables mediante modelos de lenguaje con recuperación de contexto. El estudio responde a la necesidad de contar con herramientas de inteligencia artificial capaces de detectar desviaciones operativas, explicar sus causas probables y documentar alertas de manera comprensible para supervisores, responsables de calidad, gestores logísticos y auditores internos.

El trabajo se organiza en cinco capítulos: el Capítulo I establece el planteamiento del problema, objetivos e hipótesis; el Capítulo II desarrolla el marco teórico con antecedentes y estado del arte; el Capítulo III describe la propuesta metodológica; el Capítulo IV presenta los resultados y discusión; y el Capítulo V contiene las conclusiones y trabajos futuros.

**El Autor**

---

# RESUMEN

Esta tesis propone un sistema integrado de supervisión operativa para empresas agroexportadoras peruanas, que combina predicción tabular mediante modelos Gradient Boosting Decision Trees (GBDT), detección de anomalías operativas mediante ensemble de algoritmos, explicabilidad mediante SHAP (SHapley Additive exPlanations), y generación automática de reportes trazables con Modelos de Lenguaje de Gran Tamaño (LLMs) en arquitectura RAG (Retrieval-Augmented Generation).

El sistema aborda una brecha identificada en el contexto agroexportador: los procesos de producción, acopio, almacenamiento, control de calidad, logística, cumplimiento fitosanitario y comercialización internacional suelen analizarse mediante fuentes fragmentadas, reportes manuales o tableros aislados. Esta fragmentación dificulta la detección temprana de anomalías y reduce la trazabilidad de las decisiones. La propuesta se evalúa con métricas técnicas (PR-AUC, F1-Score, cobertura de trazabilidad), evaluación de comprensión operativa y datos públicos/sintéticos documentados del dominio agroexportador.

Las contribuciones principales son: (1) arquitectura modular de cuatro capas que separa predicción, detección, explicación y reporte; (2) integración de fuentes públicas oficiales y dataset sintético agroexportador documentado mediante criterios de Datasheets for Datasets [@gebru2021datasheets]; (3) uso de SHAP para explicar alertas operativas a nivel de variable; (4) generación de reportes mediante RAG restringido a evidencias estructuradas, reduciendo el riesgo de alucinación; (5) evaluación comparativa del sistema integrado frente a componentes aislados en rendimiento, trazabilidad y tiempo de interpretación. La Resolución SBS N° 053-2023 se considera como referencia nacional de buenas prácticas para gestión de riesgo de modelos, mientras que el D.S. N° 115-2025-PCM se adopta como marco peruano general de gobernanza y supervisión humana en IA.

**Palabras clave**: supervisión operativa, detección de anomalías, agroexportación, explicabilidad IA, modelos de lenguaje, gobernanza, GBDT, reportes automáticos, trazabilidad, inteligencia artificial.

---

# ABSTRACT

This thesis proposes an integrated operational supervision system for Peruvian agro-export companies, combining tabular prediction using Gradient Boosting Decision Trees (GBDT), operational anomaly detection through an ensemble of algorithms, explainability through SHAP (SHapley Additive exPlanations), and traceable automatic report generation with Large Language Models (LLMs) in a Retrieval-Augmented Generation (RAG) architecture.

The system addresses an identified gap in agro-export operational supervision: production, storage, quality control, logistics, phytosanitary compliance, and international commercialization are commonly analyzed through fragmented sources, manual reports, or isolated dashboards. This fragmentation limits early anomaly detection and weakens decision traceability. The proposal is evaluated using technical metrics (PR-AUC, F1-Score, traceability coverage), operational comprehension assessment, and documented public/synthetic agro-export data.

The main contributions are: (1) a modular four-layer architecture separating prediction, detection, explanation, and reporting; (2) integration of official public sources and a documented synthetic agro-export dataset; (3) SHAP-based explanation of operational alerts; (4) evidence-restricted RAG reporting to reduce hallucination risk; and (5) comparative evaluation of the integrated system against isolated components in terms of detection performance, traceability, and interpretation time. Peruvian Resolution SBS N° 053-2023 is used only as a national reference for model risk management practices, while D.S. N° 115-2025-PCM is adopted as the general Peruvian AI governance framework.

**Keywords**: operational supervision, anomaly detection, agro-export, AI explainability, language models, governance, GBDT, automatic reports, traceability, artificial intelligence.

---

# ÍNDICE DE CONTENIDOS

- DEDICATORIA
- AGRADECIMIENTOS
- PRESENTACIÓN
- RESUMEN
- ABSTRACT
- ÍNDICE DE CONTENIDOS
- ÍNDICE DE FIGURAS
- ÍNDICE DE TABLAS
- ÍNDICE DE FÓRMULAS
- INTRODUCCIÓN
- **CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA**
  - 1.1 Descripción de la Realidad Problemática
  - 1.2 Problema Principal
  - 1.3 Objetivos
  - 1.4 Hipótesis de la Investigación
  - 1.5 Variables e Indicadores
  - 1.6 Viabilidad de la Investigación
  - 1.7 Justificación e Importancia
  - 1.8 Alcance
  - 1.9 Línea, Tipo y Nivel de la Investigación
  - 1.10 Técnicas e Instrumentos de Recolección de Información
- **CAPÍTULO II: MARCO TEÓRICO**
  - 2.1 Antecedentes de la Investigación
  - 2.2 Estado del Arte
  - 2.3 Marco Conceptual
- **CAPÍTULO III: PROPUESTA METODOLÓGICA**
  - 3.1 Arquitectura del Sistema Integrado
  - 3.2 Datasets de Validación y Benchmarks
  - 3.3 Configuración Experimental y Métricas
- **CAPÍTULO IV: RESULTADOS Y DISCUSIÓN**
  - 4.1 Resultados Cuantitativos
  - 4.2 Resultados Cualitativos
  - 4.3 Discusión de Resultados
- **CAPÍTULO V: CONCLUSIONES Y TRABAJOS FUTUROS**
  - 5.1 Conclusiones
  - 5.2 Limitaciones
  - 5.3 Trabajos Futuros
- CRONOGRAMA DE ACTIVIDADES
- CONCLUSIONES (English)
- RECOMENDACIONES
- GLOSARIO DE TÉRMINOS
- REFERENCIAS BIBLIOGRÁFICAS
- ANEXOS

---

# ÍNDICE DE FIGURAS

*(Por completar — se insertarán las figuras del diagrama de arquitectura del sistema, flujo del pipeline y resultados experimentales)*

---

# ÍNDICE DE TABLAS

- Tabla 2.1 — Comparativa de Sistemas de Supervisión con IA
- Tabla 2.2 — Resumen del Estado del Arte por Bloques Temáticos
- Tabla 1.1 — Variables e Indicadores
- Tabla 1.2 — Cronograma de Actividades
- Tabla 1.3 — Técnicas e Instrumentos de Recolección

---

# ÍNDICE DE FÓRMULAS

- Fórmula 1 — Función objetivo GBDT: $F^*(x) = \arg\min_F \mathbb{E}[L(y, F(x))]$
- Fórmula 2 — Iteración GBDT: $F_m(x) = F_{m-1}(x) + \nu \cdot h_m(x)$
- Fórmula 3 — Local Outlier Factor: $\text{LOF}_k(p)$
- Fórmula 4 — Deep SVDD: $\min_{W,R,c} R^2 + \frac{1}{\nu n}\sum \max(0, \|f(x_i;W)-c\|^2 - R^2)$
- Fórmula 5 — Valor SHAP: $\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!}[f(S\cup\{i\})-f(S)]$

---

# INTRODUCCIÓN

La agroexportación peruana constituye un sector estratégico para la economía nacional debido a su crecimiento sostenido, diversificación de productos y participación en mercados internacionales exigentes. De acuerdo con información oficial del Ministerio de Desarrollo Agrario y Riego, al cierre de 2025 las agroexportaciones peruanas alcanzaron ventas por USD 15 013 millones, con un crecimiento de 17.3% respecto al año anterior [@midagri2026boletin]. Entre los principales productos exportados destacaron arándanos, uvas, paltas, cacao y espárragos, lo que evidencia la importancia económica y operativa de las cadenas agroexportadoras peruanas.

En este contexto, las empresas agroexportadoras articulan procesos de producción agrícola, acopio, almacenamiento, control de calidad, cumplimiento fitosanitario, logística y comercialización internacional. Cada uno de estos procesos genera datos que pueden revelar desviaciones relevantes para la gestión operativa: cambios inusuales en precios, variaciones de volumen, condiciones climáticas adversas, incumplimientos de calidad, retrasos logísticos o patrones atípicos en el comportamiento exportador. No obstante, la supervisión de estos procesos suele depender de reportes manuales, hojas de cálculo, sistemas no integrados o análisis posteriores a la ocurrencia del problema.

La inteligencia artificial ofrece herramientas adecuadas para abordar esta brecha. Los modelos Gradient Boosting Decision Trees (GBDT) han demostrado buen desempeño en datos tabulares estructurados [@grinsztajn2022trees]; los ensembles de detectores de anomalías permiten identificar comportamientos atípicos de manera más robusta que un detector individual [@han2022adbench]; la explicabilidad mediante valores de Shapley (SHAP) convierte predicciones opacas en justificaciones comprensibles [@lundberg2017shap]; y los modelos de lenguaje con arquitectura RAG pueden transformar resultados cuantitativos en reportes comprensibles siempre que se restrinja su función a la generación narrativa basada en evidencias [@schneider2025rag].

La presente investigación propone un sistema integrado de cuatro capas que une predicción tabular, detección de anomalías, explicabilidad y generación de reportes trazables en un flujo coherente de supervisión operativa. El sistema se orienta al contexto agroexportador peruano y busca mejorar la capacidad de detectar desviaciones operativas, explicar sus posibles causas y documentar cada alerta de manera comprensible para supervisores, responsables de calidad, gestores logísticos y auditores internos. La Resolución SBS N° 053-2023 [@sbs2023riesgos] se toma como referencia nacional de buenas prácticas para gestión de riesgo de modelos, sin asumirla como obligación directa para agroexportadoras; el D.S. N° 115-2025-PCM [@pcm2025leyia] se emplea como marco peruano general sobre gobernanza, transparencia y supervisión humana en inteligencia artificial.

El documento se estructura de la siguiente manera: el Capítulo I plantea el problema de investigación, define los objetivos, hipótesis, variables e indicadores, y evalúa la viabilidad del proyecto. El Capítulo II desarrolla el marco teórico, incluyendo antecedentes nacionales e internacionales, estado del arte organizado en cinco debates argumentativos, y el marco conceptual que fundamenta cada componente técnico de la propuesta. El Capítulo III describe la arquitectura del sistema propuesto, los datasets de validación y la configuración experimental. El Capítulo IV presenta los resultados obtenidos y la discusión de los hallazgos. Finalmente, el Capítulo V sintetiza las conclusiones, limitaciones de la investigación y propuestas de trabajos futuros.

---

# CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA

## 1.1 Descripción de la Realidad Problemática

### Contexto agroexportador y empresarial

En empresas agroexportadoras —dedicadas a la producción, acopio, procesamiento, empaque, control de calidad y comercialización internacional de productos agrícolas— la supervisión operativa constituye una actividad crítica para detectar desviaciones productivas, mermas, variaciones de precios, condiciones climáticas adversas, retrasos logísticos e incumplimientos de estándares fitosanitarios. Estas desviaciones afectan directamente la rentabilidad, continuidad operativa y competitividad internacional de la empresa.

La magnitud económica del sector refuerza la necesidad de sistemas de supervisión más oportunos y trazables. Según MIDAGRI, las agroexportaciones peruanas superaron los USD 15 013 millones al cierre de 2025, con crecimiento de 17.3% respecto al año anterior [@midagri2026boletin]. Este dinamismo incrementa la complejidad de las cadenas agroexportadoras, que deben coordinar producción, calidad, sanidad, logística y comercio exterior bajo condiciones cambiantes de clima, demanda internacional y requisitos de destino.

En el contexto peruano, la transformación digital y la adopción de sistemas inteligentes exigen mayores niveles de gobernanza tecnológica y trazabilidad operativa. La Ley N.° 31814 y su reglamento aprobado mediante D.S. N.° 115-2025-PCM [@pcm2025leyia] establecen un marco general para promover el uso responsable de la inteligencia artificial, con énfasis en transparencia, supervisión humana y gestión de riesgos. Asimismo, la Resolución SBS N.° 053-2023 [@sbs2023riesgos] se considera en esta tesis como referencia nacional de buenas prácticas para gestión de riesgo de modelos, validación y monitoreo, sin asumirla como obligación directa para empresas agroexportadoras.

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
- ¿De qué manera la explicabilidad mediante SHAP contribuye a que supervisores operativos comprendan las causas probables de una alerta?
- ¿Cómo generar reportes automáticos que sean comprensibles, accionables y trazables sin permitir que el modelo de lenguaje tome decisiones o invente información?
- ¿Cómo evaluar si el sistema integrado mejora la trazabilidad, comprensión de alertas y tiempo de decisión frente al uso de componentes aislados?

## 1.3 Objetivos

### 1.3.1 Objetivo Principal

Diseñar, implementar y evaluar un sistema integrado de supervisión operativa basado en inteligencia artificial explicable para detectar anomalías en datos agroexportadores, explicar los factores asociados mediante SHAP y generar reportes trazables que apoyen la toma de decisiones en empresas agroexportadoras peruanas.

### 1.3.2 Objetivos Específicos

1. **Fuentes de datos y dominio**: Identificar y documentar fuentes de datos públicas y sintéticas aplicables a la supervisión operativa agroexportadora, considerando variables de precios, volúmenes, clima, comercio exterior y cumplimiento fitosanitario.

2. **Arquitectura y modularidad**: Diseñar una arquitectura modular de cuatro capas (predicción → detección → explicación → reporte) que integre modelos tabulares, detectores de anomalías, explicabilidad y generación de reportes trazables.

3. **Predicción y detección robusta**: Implementar modelos de predicción y detección de anomalías sobre datos agroexportadores públicos y sintéticos, utilizando algoritmos adecuados para datos tabulares y series temporales.

4. **Explicabilidad verificable**: Integrar SHAP [@lundberg2017shap] para identificar las variables que más contribuyen a cada alerta generada por el sistema.

5. **Generación de reportes trazables**: Diseñar un componente LLM+RAG que redacte explicaciones operativas basadas exclusivamente en evidencias estructuradas del sistema.

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
- Indicadores: ROC-AUC, Precisión, Recall, F1-Score, PR-AUC
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

**Disponibilidad de tecnologías**: El stack tecnológico es completamente open-source y maduro: XGBoost [@chen2016xgboost], LightGBM [@ke2017lightgbm] y CatBoost [@prokhorenkova2018catboost] para predicción tabular; PyOD [@zhao2019pyod] para ensemble de anomalías con acceso a Isolation Forest [@liu2008iforest], LOF [@breunig2000lof] y Deep SVDD [@ruff2018deepsvdd]; SHAP [@lundberg2017shap] para explicabilidad; APIs de LLM (Anthropic Claude, OpenAI GPT-4) o modelos locales (Llama 3) para generación de reportes.

**Datos disponibles**: Se contemplan tres niveles de datos. El primer nivel corresponde a fuentes públicas oficiales: MIDAGRI para agroexportaciones, precios y boletines sectoriales; SENAMHI para variables climáticas; SENASA para requisitos fitosanitarios; SUNAT para exportaciones; INEI para indicadores económicos; FAOSTAT y UN Comtrade para validación internacional. El segundo nivel corresponde a un dataset sintético agroexportador documentado, construido con variables operativas plausibles y etiquetas de anomalía controladas. El tercer nivel, opcional, corresponde a datos privados de una empresa agroexportadora bajo acuerdo de confidencialidad. Como referencia metodológica complementaria puede utilizarse el BAF Benchmark [@jesus2022baf], no como evidencia directa del dominio agroexportador, sino como benchmark tabular desbalanceado con drift temporal.

**Riesgos técnicos identificados**: La latencia de SHAP en datasets grandes (>1M filas) puede mitigarse con los métodos de aproximación TreeSHAP. La variabilidad en salidas de LLMs requiere prompt engineering robusto y restricción mediante RAG. La mitigación incluye pruebas piloto en subconjuntos de datos y benchmarking iterativo.

### 1.6.2 Viabilidad Operativa

**Timeline**: Fase 1 (meses 1–2): preparación de datos, implementación de arquitectura base. Fase 2 (meses 2–3): entrenamiento de modelos, validación experimental. Fase 3 (mes 4): test de usabilidad con auditores voluntarios. Fase 4 (mes 5): análisis de resultados, escritura y defensa.

**Presupuesto estimado**: Infraestructura GPU cloud y APIs LLM: USD 500–1,000. Stack open-source: USD 0. Incentivos para participantes del test de usabilidad: USD 200–300. Total aproximado: USD 800–1,300.

### 1.6.3 Viabilidad Económica

La viabilidad económica se justifica por la relevancia del sector agroexportador peruano y por el costo operativo asociado a decisiones tardías ante desviaciones de precio, volumen, calidad, clima o logística. MIDAGRI reportó agroexportaciones por USD 15 013 millones al cierre de 2025 [@midagri2026boletin], por lo que incluso mejoras marginales en detección temprana, trazabilidad y tiempo de respuesta pueden representar beneficios operativos relevantes. En esta fase, los beneficios económicos se tratarán como escenarios exploratorios y no como resultados finales hasta contar con evaluación experimental y supuestos documentados.

## 1.7 Justificación e Importancia de la Investigación

### 1.7.1 Justificación Teórica

La revisión sistemática de la literatura revela avances importantes en modelos tabulares, detección de anomalías, explicabilidad y generación de reportes mediante LLMs. Sin embargo, estos componentes suelen estudiarse de forma aislada y en dominios distintos al agroexportador. Trabajos de auditoría financiera o fraude contable, como AuditCopilot [@kadir2025auditcopilot], se utilizarán solo como antecedentes metodológicos sobre automatización de reportes y detección de anomalías, no como eje del dominio de aplicación. La brecha central de esta tesis es la ausencia de una arquitectura integrada y trazable para supervisión operativa agroexportadora que combine datos públicos/sintéticos, predicción tabular, detección de anomalías, explicabilidad y reportes basados en evidencia.

Esta tesis aporta a la literatura y a la práctica profesional: (a) un modelo conceptual integrado para supervisión operativa agroexportadora; (b) un protocolo de construcción y documentación de datos públicos/sintéticos mediante criterios de Datasheets for Datasets [@gebru2021datasheets]; (c) una arquitectura que restringe el LLM a la generación de reportes basados en evidencias; y (d) una evaluación comparativa del sistema integrado frente a componentes aislados en rendimiento, trazabilidad y comprensión operativa.

### 1.7.2 Justificación Económica

La automatización inteligente de la supervisión operativa tiene impacto económico potencial al reducir el tiempo de análisis, mejorar la detección temprana de desviaciones y facilitar la documentación de decisiones. En empresas agroexportadoras, las alertas oportunas sobre precios, volúmenes, clima, mermas, calidad o logística pueden apoyar decisiones correctivas antes de que la desviación se convierta en pérdida operativa o incumplimiento comercial. La escalabilidad del sistema permite adaptarlo a empresas de distintos tamaños mediante fuentes públicas, datos internos o datos sintéticos documentados.

### 1.7.3 Justificación Social

El Decreto Supremo N° 115-2025-PCM, reglamento de la Ley N° 31814 de Inteligencia Artificial del Perú, proporciona un marco nacional para promover el uso responsable de la IA, incluyendo transparencia, supervisión humana y gestión de riesgos [@pcm2025leyia]. A nivel internacional, el Reglamento (UE) 2024/1689 —EU AI Act— refuerza la importancia de documentar sistemas de IA, especialmente cuando sus resultados afectan decisiones relevantes [@eu2024aiact]. El sistema propuesto incorpora estos principios mediante explicabilidad, trazabilidad documental y revisión humana de reportes.

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

### 1.9.2 Tipo de Investigación

La investigación es de tipo **aplicada**, dado que utiliza conocimiento teórico y metodológico existente en machine learning, detección de anomalías, explicabilidad algorítmica y modelos de lenguaje para diseñar, implementar y evaluar un sistema concreto que resuelve un problema identificado en el contexto empresarial agroexportador peruano. No se busca generar nuevos algoritmos de base, sino integrar y validar una arquitectura que produce valor operativo y regulatorio verificable.

### 1.9.3 Nivel de Investigación

El nivel de la investigación es **explicativo-evaluativo**. Se parte de un diagnóstico descriptivo del problema (sistemas de supervisión fragmentados y sin trazabilidad), se propone una solución arquitectónica basada en literatura existente, y se diseñan experimentos controlados que permiten evaluar la relación entre integración de componentes y mejoras en trazabilidad, comprensión operativa y tiempo de decisión. La evaluación combina métricas cuantitativas (PR-AUC, F1-Score, cobertura de trazabilidad, tiempo-a-decisión) y cualitativas (escala Likert con supervisores o evaluadores).

## 1.10 Técnicas e Instrumentos de Recolección de Información

### 1.10.1 Técnicas

Las técnicas de recolección de información utilizadas en esta investigación son:

1. **Revisión sistemática de literatura**: Búsqueda estructurada en bases de datos académicas (IEEE Xplore, ACM Digital Library, arXiv, Google Scholar, Scopus) utilizando términos de búsqueda como "anomaly detection ensemble", "GBDT tabular data", "SHAP explainability", "RAG generated reports", "AI governance Peru" y "agricultural anomaly detection". Se aplican criterios de inclusión: publicaciones entre 2017 y 2026, en inglés o español, con evaluación empírica o propuesta metodológica verificable.

2. **Análisis documental**: Revisión de fuentes oficiales nacionales (MIDAGRI, SENASA, SENAMHI, SUNAT, INEI), regulaciones nacionales sobre IA (Ley N° 31814 y D.S. N° 115-2025-PCM) y marcos internacionales de gobernanza (EU AI Act 2024, NIST AI RMF 1.0). La Resolución SBS N° 053-2023 se considera solo como referencia metodológica de gestión de riesgo de modelos.

3. **Experimentación controlada**: Diseño de experimentos comparativos con el sistema integrado versus componentes aislados, evaluados sobre datos públicos/sintéticos agroexportadores. El BAF Benchmark [@jesus2022baf] puede emplearse solo como benchmark metodológico complementario para datos tabulares desbalanceados.

4. **Evaluación con usuarios o evaluadores simulados**: Prueba de comprensión y tiempo de decisión con supervisores, auditores internos, estudiantes avanzados o evaluadores simulados mediante protocolo de tareas cronometradas y cuestionario post-tarea.

### 1.10.2 Instrumentos

| Instrumento | Propósito | Variable que mide |
|---|---|---|
| Fuentes públicas oficiales | Construir contexto, variables y rangos plausibles del dominio agroexportador | VD1, VD5 |
| Dataset sintético agroexportador | Evaluación controlada de predicción, anomalías y reportes | VD1, VD2, VD3 |
| BAF Benchmark [@jesus2022baf] | Benchmark metodológico complementario para datos tabulares desbalanceados | VD1 |
| Cuestionario de comprensión (Likert 1–5) | Evaluar claridad de explicaciones y reportes para supervisores | VD2, VD3, VD4 |
| Registro de tiempo-a-decisión | Medir segundos requeridos para interpretar y decidir sobre una alerta | VD4 |
| Checklist de trazabilidad | Verificar dato, modelo, score, umbral, explicación, fuente y reporte por alerta | VD5 |

## 1.11 Cronograma de Actividades

| Actividad | Mes 1 | Mes 2 | Mes 3 | Mes 4 | Mes 5 |
|---|:---:|:---:|:---:|:---:|:---:|
| Revisión bibliográfica y marco teórico | ✓ | | | | |
| Obtención y preprocesamiento de datos | ✓ | ✓ | | | |
| Implementación Capa 1 (GBDT + TFT) | | ✓ | | | |
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

---

# CAPÍTULO II: MARCO TEÓRICO

## 2.1 Antecedentes de la Investigación

Los antecedentes de esta investigación se organizan desde dos perspectivas. La primera corresponde a trabajos técnicos sobre datos tabulares, detección de anomalías, explicabilidad y generación de reportes, incluso cuando fueron desarrollados en dominios financieros o contables. Estos trabajos se utilizan como soporte metodológico. La segunda corresponde al dominio de aplicación de esta tesis: supervisión operativa agroexportadora, donde la contribución principal consiste en adaptar e integrar dichas técnicas para detectar, explicar y documentar desviaciones en procesos agroexportadores peruanos.

El desarrollo de sistemas de predicción, detección de anomalías y generación de reportes en datos empresariales ha seguido una trayectoria de especialización creciente, marcada por tres tendencias paralelas: el auge de los modelos basados en árboles para datos tabulares, la proliferación de benchmarks sistemáticos y la emergencia de los modelos de lenguaje como capa de interpretación. Los siguientes antecedentes fueron seleccionados por su proximidad metodológica con la propuesta de esta investigación, aunque varios provienen de dominios financieros o contables y se emplean aquí solo como soporte técnico transferible.

### 2.1.1 Kadir et al. (2025) — AuditCopilot: LLMs para Reportes de Anomalías

Kadir et al. (2025) desarrollaron AuditCopilot [@kadir2025auditcopilot], un sistema de auditoría contable que integra LLMs con detección de anomalías en asientos de doble entrada para generar explicaciones automáticas en lenguaje natural. El sistema implementa un pipeline de tres etapas —detección de irregularidades, interpretación contextual con LLM ajustado y generación de narrativas— evaluado sobre un corpus de asientos contables sintéticos y reales. Los resultados reportan mejoras en la tasa de detección y reducción del tiempo de revisión, con valoración positiva de auditores en pruebas de aceptabilidad.

La relevancia de este antecedente para la presente tesis es metodológica: confirma la viabilidad de combinar detección de anomalías con generación de reportes LLM. No obstante, su dominio es contable, por lo que no se adopta como evidencia agroexportadora. Esta tesis traslada el principio de generación narrativa a un contexto operativo, separando estrictamente la detección de la redacción mediante RAG sobre scores y vectores SHAP.

### 2.1.2 Park (2024) — Framework Multi-Agente LLM para Anomalías Financieras

Park (2024) propuso un framework de múltiples agentes LLM especializados para validar alertas de anomalías en el mercado bursátil (S&P 500) [@park2024llm]. La arquitectura organiza cuatro agentes —conversión de datos, análisis estadístico, verificación cruzada y consolidación— que se comunican mediante prompts estructurados y alcanzan mejores tasas de verdaderos positivos que un LLM único. La especialización de agentes demuestra ser superior a la generalización en la validación de señales financieras.

Este trabajo aporta a la literatura evidencia de que los LLMs en arquitecturas especializadas pueden mejorar la calidad del análisis automatizado. Sin embargo, opera en mercados de alta frecuencia, un dominio alejado del contexto agroexportador. Esta tesis aplica únicamente el principio de especialización de roles —LLM como intérprete, no como detector— en un sistema de supervisión operativa con trazabilidad y generación restringida a datos verificados [@schneider2025rag].

### 2.1.3 Autores varios (2025) — Ensemble GBDT+SHAP en Datos Tabulares Críticos

En el trabajo publicado en el *Journal of Risk and Financial Management* (2025), los autores diseñaron un framework integrado de detección de fraude en estados financieros combinando Stacking Ensemble de XGBoost, LightGBM y CatBoost con explicabilidad SHAP [@mongolia2025fraud]. El ensemble alcanza PR-AUC = 0.93 y F1-Score = 0.83, superando a TabNet y FT-Transformer, con un SHAP Stability Index = 0.87 que certifica la coherencia forense de las explicaciones —requisito indispensable en auditoría.

Este antecedente respalda la decisión arquitectónica de combinar GBDT y SHAP en datos tabulares críticos. La diferencia clave es que dicho trabajo se limita a detección de fraude en estados financieros; la presente investigación adapta la lógica de modelos tabulares explicables al contexto agroexportador, incorporando fuentes públicas, dataset sintético documentado y generación de reportes LLM+RAG para supervisión operativa.

### 2.1.4 Han et al. (2022) — ADBench: Benchmark para Detección de Anomalías

Han et al. (2022) publicaron ADBench [@han2022adbench], un benchmark sistemático que evalúa 30 algoritmos de detección de anomalías en 57 datasets reales y sintéticos bajo tres niveles de supervisión —no supervisado, semisupervisado y supervisado. El hallazgo central es que no existe un algoritmo universalmente superior: el rendimiento depende del tipo de anomalía, la distribución de datos y el nivel de etiquetado. Isolation Forest y ECOD muestran consistencia en escenarios no supervisados, y los ensembles de múltiples detectores superan sistemáticamente a los detectores individuales en escenarios de alta variabilidad distribucional.

ADBench justifica formalmente la estrategia de ensemble adoptada en esta tesis y proporciona la metodología experimental de referencia para el Capítulo III. La librería PyOD [@zhao2019pyod], compatible con todos los algoritmos evaluados en ADBench, asegura la reproducibilidad directa de los resultados.

### 2.1.5 Grinsztajn et al. (2022) — GBDT vs. Deep Learning en Datos Tabulares

Grinsztajn et al. (2022) realizaron un benchmark sistemático en 45 datasets tabulares comparando GBDT contra FT-Transformer, TabNet y MLP [@grinsztajn2022trees]. El resultado es contundente: en datasets con menos de 50,000 muestras, los GBDT superan a cualquier modelo de Deep Learning en el 95% de los casos. Los autores identifican tres propiedades estructurales de los datos tabulares que favorecen a los árboles: robustez ante features no informativas, orientación no invariante a rotaciones e irregularidades en la función objetivo.

Este trabajo cierra el debate GBDT versus Deep Learning para el tamaño de dataset típico en entornos empresariales medianos y justifica de manera irrefutable la elección de XGBoost y LightGBM como backbone del módulo de predicción de esta tesis. Es el argumento bibliográfico central de la primera batalla del estado del arte (§2.2.1).

### 2.1.6 Lim et al. (2021) — Temporal Fusion Transformer para Forecasting Interpretable

Lim et al. (2021) propusieron el Temporal Fusion Transformer (TFT) [@lim2020tft], una arquitectura que combina codificación LSTM, selección de variables mediante mecanismo de gating, atención multi-cabezal interpretable y predicción por cuantiles para forecasting multi-horizonte con covariables exógenas. TFT supera a LSTMs, N-BEATS y Transformers vanilla en cuatro de seis datasets de referencia, con mapas de atención legibles por analistas de negocio.

TFT es seleccionado como arquitectura del módulo de forecasting por su doble ventaja: rendimiento predictivo e interpretabilidad incorporada. En el contexto de supervisión operativa, la capacidad de justificar qué períodos temporales y qué covariables (indicadores de producción, calendarios logísticos) fundamentan la predicción es un requisito funcional equivalente en importancia a la precisión numérica.

### 2.1.7 Zhao et al. (2019) — PyOD: Librería Estándar para Detección de Outliers

Zhao et al. (2019) desarrollaron PyOD [@zhao2019pyod], una librería unificada en Python que implementa más de 40 algoritmos de detección de outliers con una API compatible con scikit-learn. Cubre métodos basados en proximidad (LOF), proyección (PCA), ensembles (Isolation Forest) y redes neuronales (Deep SVDD, AutoEncoder). Con más de 7,000 estrellas en GitHub y adopción en publicaciones de NeurIPS, ICDM e ICML, PyOD es la infraestructura técnica de referencia para implementar el ensemble de detección de anomalías de esta tesis, garantizando reproducibilidad directa con los 30 algoritmos de ADBench [@han2022adbench].

---

## 2.2 Estado del Arte

El estado del arte se organiza en torno a cinco debates fundamentales de la literatura que la presente propuesta debe resolver o posicionarse explícitamente. Cada sub-sección presenta el debate, los trabajos relevantes y la posición de esta tesis. La Tabla 2.1 sintetiza todas las referencias relevantes al final de la sección.

### 2.2.1 GBDT versus Deep Learning para Datos Tabulares Empresariales y Agroexportadores

El desarrollo de modelos para datos tabulares ha seguido una trayectoria diferente a la de visión computacional y procesamiento de lenguaje natural: el Deep Learning no ha conseguido desplazar a los modelos basados en árboles como estándar de facto en datos estructurados. Chen y Guestrin (2016) [@chen2016xgboost] introdujeron XGBoost como sistema escalable de gradient boosting con regularización L1/L2, manejo nativo de valores faltantes y paralelización por columnas, estableciéndolo como el baseline universal con más de 45,000 citas en la literatura científica. Ke et al. (2017) [@ke2017lightgbm] lo extendieron con LightGBM, que incorpora Gradient-based One-Side Sampling (GOSS) e histogramas para lograr velocidades de entrenamiento hasta 20 veces superiores con rendimiento comparable. Prokhorenkova et al. (2018) [@prokhorenkova2018catboost] resolvieron el problema de target leakage en variables categóricas con Ordered Boosting, siendo especialmente relevante en datos contables con alta cardinalidad (cuentas, departamentos, centros de costo).

El auge del Deep Learning motivó intentos de adaptar estas arquitecturas a datos tabulares. Gorishniy et al. (2021) [@gorishniy2021ft] propusieron FT-Transformer, el primer Transformer robusto para tablas mediante feature embeddings, que en algunos benchmarks iguala pero raramente supera a los GBDT. Arik y Pfister (2021) [@arik2021tabnet] desarrollaron TabNet, que combina selección secuencial de features con atención interpretable, argumentando que puede ofrecer tanto rendimiento como interpretabilidad en un solo modelo. Sin embargo, el estudio seminal de Grinsztajn et al. (2022) [@grinsztajn2022trees], con un benchmark en 45 datasets y hasta 50,000 muestras, zanjó empíricamente este debate: los GBDT superan a todo modelo de Deep Learning en el 95% de los casos para datasets de tamaño empresarial mediano. Los autores identifican tres propiedades estructurales de los datos tabulares que favorecen a los árboles: robustez ante features no informativas, orientación no invariante a rotaciones y presencia de irregularidades en la función objetivo —todas características presentes en los registros transaccionales de auditoría.

En dominios empresariales con datos tabulares heterogéneos, esta evidencia respalda el uso de GBDT como primera opción antes de recurrir a arquitecturas neuronales complejas. En el caso agroexportador, los registros combinan variables numéricas, categóricas, temporales y contextuales —producto, zona, volumen, precio, clima, destino, cumplimiento y logística—, por lo que los modelos basados en árboles son una base técnica adecuada para capturar relaciones no lineales y manejar variables de distinta naturaleza.

**Posición de esta tesis**: XGBoost y LightGBM constituyen el backbone del módulo de predicción tabular. TabNet y FT-Transformer se evalúan como baselines comparativos, no como propuesta principal, dado que la evidencia empírica no justifica su adopción en el contexto de tamaño del dataset empresarial analizado.

### 2.2.2 Detector Único versus Ensemble para Detección de Anomalías

El campo de la detección de anomalías cuenta con una historia de más de dos décadas de métodos en competencia. Breunig et al. (2000) [@breunig2000lof] establecieron el Local Outlier Factor (LOF) como referencia para detectar anomalías locales mediante densidad relativa al vecindario k-NN, un enfoque sensible a variaciones locales que permite identificar transacciones con patrones de comportamiento heterogéneos. Liu et al. (2008) [@liu2008iforest] revolucionaron el campo con Isolation Forest, que aísla anomalías por particionamiento aleatorio sin necesidad de definir perfiles de normalidad, con complejidad O(n) que lo hace viable en millones de transacciones diarias. Ruff et al. (2018) [@ruff2018deepsvdd] extendieron la detección a espacios de representación profundos con Deep SVDD, capturando patrones no lineales en los datos mediante redes neuronales. Li et al. (2022) [@li2022ecod] propusieron ECOD, un detector moderno libre de parámetros basado en distribución empírica acumulada que supera a 11 baselines en datasets no supervisados, eliminando el riesgo de sobreajuste al proceso de calibración.

El hallazgo central de Han et al. (2022) [@han2022adbench] en ADBench —57 datasets, 30 algoritmos, tres niveles de supervisión— establece que no existe un algoritmo universalmente superior: el rendimiento depende fuertemente del tipo de anomalía, la distribución de los datos y el nivel de etiquetado disponible. Esta conclusión teórica valida la estrategia de ensemble como la opción más robusta para entornos de producción donde la distribución de anomalías es desconocida a priori. La librería PyOD [@zhao2019pyod] proporciona la infraestructura técnica para implementar este ensemble de manera estandarizada y reproducible.

**Posición de esta tesis**: El ensemble Isolation Forest + LOF + Deep SVDD (coordinado mediante PyOD) es más robusto que cualquier detector individual. Esta decisión está respaldada por ADBench [@han2022adbench] como fundamento teórico.

### 2.2.3 LLM como Detector versus LLM como Generador de Reportes

El surgimiento de los LLMs ha generado propuestas de integración en sistemas empresariales con distintos roles. Hegselmann et al. (2023) [@tabllm2023] demostraron con TabLLM que los LLMs pueden clasificar datos tabulares en configuración zero/few-shot mediante serialización a texto, con rendimiento no trivial incluso sin ajuste fino. Park (2024) [@park2024llm] llevó esta lógica más lejos con un framework multi-agente donde LLMs especializados validan alertas de anomalías. Estos antecedentes muestran potencial metodológico, aunque no resuelven por sí mismos el problema de trazabilidad operativa agroexportadora.

Sin embargo, existe evidencia sustancial de que usar LLMs como detectores o tomadores de decisiones introduce riesgos inaceptables. El survey sobre alucinaciones en LLMs [@survey2026hallucination] documenta que los modelos pueden generar razonamiento coherente en forma pero incorrecto en contenido, con alta confianza aparente. Este riesgo es especialmente importante en reportes operativos, donde una cifra o causa inventada puede inducir decisiones equivocadas.

La arquitectura RAG (Schneider et al., 2025 [@schneider2025rag]) ofrece una solución al anclar las respuestas del LLM a bases de conocimiento verificadas —en este caso, scores, umbrales, vectores SHAP y fuentes agroexportadoras recuperadas— reduciendo el espacio de alucinación al forzar al modelo a narrar únicamente lo que los datos cuantitativos establecen. El LLM no infiere anomalías; las narra con evidencias como fundamento.

**Posición de esta tesis**: El LLM se restringe estrictamente a la capa de generación de reportes mediante RAG. La detección, cuantificación y explicación son realizadas por modelos y evidencias estructuradas (GBDT + ensemble + SHAP). Esta separación se alinea con principios de transparencia, supervisión humana y trazabilidad promovidos por marcos como el D.S. N° 115-2025-PCM [@pcm2025leyia], el EU AI Act [@eu2024aiact] y el NIST AI RMF [@nist2023aia].

### 2.2.4 Sistemas Aislados versus Sistema Integrado de Supervisión Operativa Continua

La revisión de la literatura evidencia una fragmentación sistemática en los sistemas de supervisión asistida por IA. Los trabajos pueden agruparse en cuatro categorías según el módulo que abordan: (1) sistemas de predicción tabular [@chen2016xgboost; @ke2017lightgbm; @prokhorenkova2018catboost]; (2) sistemas de forecasting y series temporales [@lim2020tft; @nhts2022]; (3) sistemas de detección de anomalías [@liu2008iforest; @han2022adbench]; y (4) sistemas de generación de reportes con LLMs [@kadir2025auditcopilot; @park2024llm].

Trabajos como AuditCopilot [@kadir2025auditcopilot] logran una integración parcial al combinar detección de anomalías con generación de reportes LLM, pero operan en dominio contable y no abordan supervisión agroexportadora. El framework de Park (2024) [@park2024llm] integra múltiples LLMs pero opera en mercados financieros de alta frecuencia. AuditMAI [@auditmai2024] propone una infraestructura conceptual para auditoría continua de sistemas de IA. La Tabla 2.2 resume comparativamente los sistemas más cercanos a la propuesta de esta tesis desde una perspectiva metodológica.

**Posición de esta tesis**: Esta investigación cierra la brecha de integración al proponer y evaluar una arquitectura modular de cuatro capas que combina predicción tabular, detección de anomalías, explicabilidad SHAP y generación de reportes LLM-RAG con restricción anti-alucinación, aplicada a supervisión operativa agroexportadora. BAF [@jesus2022baf] se utiliza solo como benchmark metodológico complementario; la validación principal se orienta a datos agroexportadores públicos y sintéticos.

### 2.2.5 Contexto Regulatorio Internacional versus Perú

La mayoría de marcos de gobernanza de IA de la literatura operan en contextos regulatorios de EE.UU. (NIST AI RMF [@nist2023aia]), Europa (EU AI Act [@eu2024aiact], GDPR) o Asia. Estos marcos coinciden en principios relevantes para esta tesis: documentación, transparencia, supervisión humana, gestión de riesgos y trazabilidad.

En el contexto peruano, el marco regulatorio ha madurado significativamente en 2023–2025. La Resolución SBS N° 053-2023 establece lineamientos de gobernanza, trazabilidad y explicabilidad para modelos de riesgo en entidades supervisadas por la SBS [@sbs2023riesgos], por lo que se adopta aquí solo como referencia de buenas prácticas. El Decreto Supremo N° 115-2025-PCM, reglamento de la Ley N° 31814, proporciona un marco nacional general para promover el uso responsable de la inteligencia artificial [@pcm2025leyia]. A nivel internacional, el EU AI Act [@eu2024aiact] refuerza obligaciones de transparencia y documentación para sistemas de IA.

**Posición de esta tesis**: Esta investigación diseña un sistema de supervisión operativa agroexportadora que incorpora principios de gobernanza, trazabilidad, documentación y supervisión humana. El D.S. N° 115-2025-PCM se adopta como marco peruano general de IA responsable, mientras que la Resolución SBS N° 053-2023 se utiliza solo como referencia nacional de gestión de riesgo de modelos.

### 2.2.6 Síntesis y Tabla del Estado del Arte

La revisión sistemática de los bloques temáticos permite identificar la brecha de investigación central: **no existe en la literatura revisada un sistema orientado al contexto agroexportador peruano que integre de manera modular, con evaluación reproducible y trazabilidad explícita, los cuatro componentes**: predicción tabular, detección de anomalías, explicabilidad SHAP y generación de reportes LLM-RAG basada en evidencias. Esta tesis propone y evalúa dicha integración para supervisión operativa agroexportadora.

**Tabla 2.1 — Comparativa de Sistemas de Supervisión con IA**

| Característica | **Esta tesis** | AuditCopilot [@kadir2025auditcopilot] | Park 2024 [@park2024llm] | AuditMAI [@auditmai2024] | [@mongolia2025fraud] |
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
| 1 | Chen & Guestrin [@chen2016xgboost] | 2016 | XGBoost: gradient boosting escalable con regularización L1/L2, benchmark universal para datos tabulares |
| 2 | Ke et al. [@ke2017lightgbm] | 2017 | LightGBM: GOSS + histogramas, 20× más rápido que XGBoost con precisión comparable |
| 3 | Prokhorenkova et al. [@prokhorenkova2018catboost] | 2018 | CatBoost: Ordered Boosting elimina target leakage en variables categóricas de alta cardinalidad |
| 4 | Gorishniy et al. [@gorishniy2021ft] | 2021 | FT-Transformer: primer Transformer robusto para datos tabulares mediante feature embeddings |
| 5 | Arik & Pfister [@arik2021tabnet] | 2021 | TabNet: atención secuencial interpretable para tablas, combina rendimiento e interpretabilidad |
| 6 | Grinsztajn et al. [@grinsztajn2022trees] | 2022 | GBDT supera a DL en el 95% de datasets ≤50K muestras; cierra el debate en contexto empresarial |
| 7 | Lim et al. [@lim2020tft] | 2021 | TFT: forecasting multi-horizonte con gating de covariables e interpretabilidad incorporada |
| 8 | Liu et al. [@liu2008iforest] | 2008 | Isolation Forest: aislamiento aleatorio O(n), sin perfil de normalidad, escalable a millones de registros |
| 9 | Breunig et al. [@breunig2000lof] | 2000 | LOF: densidad local relativa k-NN, detecta anomalías locales heterogéneas |
| 10 | Ruff et al. [@ruff2018deepsvdd] | 2018 | Deep SVDD: detección one-class en espacio latente profundo para patrones no lineales |
| 11 | Han et al. [@han2022adbench] | 2022 | ADBench: benchmark de 30 algoritmos en 57 datasets; ensembles son más robustos que detectores únicos |
| 12 | Lundberg & Lee [@lundberg2017shap] | 2017 | SHAP: valores Shapley con consistencia axiomática; TreeSHAP exacto para GBDT |
| 13 | Kadir et al. [@kadir2025auditcopilot] | 2025 | AuditCopilot: LLM+detección en asientos contables; antecedente metodológico para reportes automáticos |
| 14 | Park [@park2024llm] | 2024 | Framework multi-agente LLM para validar anomalías en mercados bursátiles |
| 15 | Schneider et al. [@schneider2025rag] | 2025 | RAG avanzado para BI organizacional; arquitectura anti-alucinación base de esta tesis |
| 16 | SBS Perú [@sbs2023riesgos] | 2023 | Resolución N° 053-2023: referencia nacional de buenas prácticas para gestión de riesgo de modelos |

---

## 2.3 Marco Conceptual

### 2.3.1 Reconocimiento de Patrones y Aprendizaje Automático

El reconocimiento de patrones es la disciplina de la inteligencia artificial que busca identificar regularidades, estructuras o relaciones en datos a partir de ejemplos históricos. En el aprendizaje automático, este proceso se formaliza mediante modelos que aprenden una función $f: X \rightarrow Y$ a partir de un conjunto de entrenamiento $\{(x_i, y_i)\}_{i=1}^n$, con el objetivo de generalizar hacia instancias no observadas.

Se distinguen tres paradigmas principales: **aprendizaje supervisado**, donde el modelo aprende de etiquetas explícitas (e.g., operación normal / operación anómala); **aprendizaje no supervisado**, que identifica patrones sin etiquetas y es fundamental en la detección de anomalías; y **aprendizaje semi-supervisado**, que combina ambos cuando el etiquetado es costoso o escaso, escenario habitual en procesos agroexportadores donde no todas las desviaciones quedan registradas formalmente.

En el contexto de esta investigación, el reconocimiento de patrones opera en dos dimensiones complementarias: la detección de registros operativos anómalos (patrones puntuales) y la identificación de secuencias temporales de comportamiento irregular (patrones colectivos), requiriendo tanto modelos de clasificación supervisada como detectores de anomalías no supervisados.

### 2.3.2 Datos Tabulares en Sistemas Agroexportadores Empresariales

Los datos tabulares son la forma predominante de almacenamiento en los sistemas de información empresarial: cada fila representa una instancia operativa y cada columna una variable. En agroexportación, una instancia puede describir un lote, día, producto, zona, envío o registro de mercado; las columnas pueden incluir precio, volumen, temperatura, precipitación, humedad, destino, cumplimiento fitosanitario, días logísticos, merma y etiqueta de anomalía.

Estas propiedades estructurales explican por qué los GBDT son adecuados para este dominio [@grinsztajn2022trees]: manejan variables numéricas y categóricas heterogéneas, toleran valores faltantes, capturan relaciones no lineales y requieren menor ingeniería de features que arquitecturas neuronales complejas. Cuando las etiquetas de anomalía son escasas o desbalanceadas, el rendimiento debe evaluarse con métricas orientadas a precisión-recall (PR-AUC), F1-Score y análisis de falsos positivos.

### 2.3.3 Gradient Boosting Decision Trees (GBDT)

Los Gradient Boosting Decision Trees (GBDT) son una familia de algoritmos de aprendizaje supervisado que construyen modelos predictivos mediante la combinación secuencial de múltiples árboles de decisión débiles. El enfoque fue formalizado por Friedman (2001) como "Greedy Function Approximation", donde cada árbol nuevo se ajusta para corregir los errores residuales del conjunto de árboles previos mediante descenso de gradiente en el espacio funcional de la función de pérdida.

La formulación matemática central de GBDT busca encontrar una función $F(x)$ que minimice la pérdida esperada:

$$F^*(x) = \arg\min_{F} \mathbb{E}_{y,x}[L(y, F(x))]$$

donde $L$ es la función de pérdida (e.g., entropía cruzada para clasificación, MSE para regresión) y la minimización se realiza iterativamente añadiendo árboles de regresión $h_m(x)$ con pesos de aprendizaje $\nu$:

$$F_m(x) = F_{m-1}(x) + \nu \cdot h_m(x)$$

**XGBoost** [@chen2016xgboost] introduce mejoras clave sobre el GBDT estándar: regularización L1 y L2 en la función objetivo para controlar la complejidad del modelo, manejo nativo de valores faltantes mediante aprendizaje automático de la dirección de ramificación, y paralelización por columnas en lugar de por filas, lo que habilita el procesamiento en datasets de alta dimensión.

**LightGBM** [@ke2017lightgbm] acelera el entrenamiento mediante dos innovaciones: Gradient-based One-Side Sampling (GOSS), que retiene las muestras con mayor gradiente y descarta aleatoriamente las de menor gradiente, preservando la distribución sin pérdida estadística significativa; y Exclusive Feature Bundling (EFB), que agrupa features mutuamente excluyentes para reducir dimensionalidad efectiva. El resultado es una aceleración de hasta 20× sobre XGBoost con precisión comparable.

**CatBoost** [@prokhorenkova2018catboost] resuelve el problema del target leakage en variables categóricas mediante Ordered Boosting: calcula las estadísticas de objetivo para cada categoría usando únicamente las observaciones previas en un orden aleatorio permutado, evitando que la información del objetivo filtre hacia las features de entrada durante el entrenamiento. Esta propiedad es especialmente relevante en datos contables, donde variables como "código de cuenta" o "centro de costo" tienen alta cardinalidad.

La justificación empírica para elegir GBDT sobre Deep Learning en datos tabulares empresariales está sólidamente documentada por [@grinsztajn2022trees]: en 45 datasets con hasta 50,000 muestras, los GBDT superan a FT-Transformer, TabNet y MLP en el 95% de los casos, atribuible a tres propiedades estructurales de los datos tabulares que los árboles aprovechan mejor que las redes neuronales.

### 2.3.4 Detección de Anomalías y Estrategia de Ensemble

La detección de anomalías es el problema de identificar observaciones que se desvían significativamente del comportamiento esperado del conjunto de datos. La literatura distingue tres tipos fundamentales de anomalías [@han2022adbench]: (a) **puntuales** — instancias individuales anómalas (e.g., una transacción de monto atípico); (b) **contextuales** — instancias que son anómalas en un contexto particular pero no en general (e.g., un cargo nocturno inusual para un perfil de usuario); y (c) **colectivas** — secuencias de instancias que son anómalas en conjunto aunque cada una individualmente no lo sea (e.g., un patrón de micro-transacciones).

**Isolation Forest** [@liu2008iforest] se basa en el principio de que las anomalías son "pocas y diferentes": son más fáciles de aislar que los puntos normales mediante particionamiento aleatorio del espacio. Un árbol de aislamiento selecciona aleatoriamente una feature y un valor de corte; la anomalía será aislada en pocas particiones (camino corto), mientras que los puntos normales requieren muchas particiones (camino largo). El score de anomalía es el inverso de la longitud promedio del camino de aislamiento, normalizada según la longitud esperada para un punto normal en un conjunto de tamaño $n$. La complejidad es O(n log n) en entrenamiento y O(n) en inferencia.

**Local Outlier Factor (LOF)** [@breunig2000lof] cuantifica el grado de anomalía de cada punto en función de la densidad de su vecindario local respecto a la densidad de sus vecinos. El score LOF para el punto $p$ se define como:

$$\text{LOF}_k(p) = \frac{\sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}}{|N_k(p)|}$$

donde $\text{lrd}_k$ es la densidad de alcanzabilidad local. Un valor LOF >> 1 indica que $p$ tiene densidad local mucho menor que sus vecinos, lo que lo caracteriza como anomalía. LOF es sensible a variaciones locales de densidad, lo que lo hace complementario a Isolation Forest en datasets heterogéneos.

**Deep SVDD** [@ruff2018deepsvdd] extiende el Support Vector Data Description al espacio de representación de redes neuronales: entrena una red para mapear los datos normales hacia el interior de una hipersfera mínima en el espacio latente. Las anomalías se detectan como puntos que caen fuera o lejos de esta hipersfera. La función objetivo minimiza el volumen de la hipersfera:

$$\min_{W, R, c} R^2 + \frac{1}{\nu n} \sum_{i=1}^{n} \max(0, \|f(x_i; W) - c\|^2 - R^2)$$

donde $f(x_i; W)$ es la representación de la red neuronal, $c$ es el centro de la hipersfera y $R$ es su radio.

**ECOD** [@li2022ecod] calcula el score de anomalía como la probabilidad acumulada de observar un punto tan extremo como $x$ bajo la distribución empírica del dataset, estimada mediante funciones de distribución acumulada (ECDF) multivariadas. Su ventaja principal es que no tiene hiperparámetros que calibrar, eliminando el riesgo de sobreajuste y simplificando el despliegue en producción.

La estrategia de **ensemble** consolida las puntuaciones de múltiples detectores mediante aggregation functions (promedio de scores, votación por mayoría o meta-clasificación). El fundamento teórico lo proporciona ADBench [@han2022adbench]: no existe un algoritmo universal, y el ensemble reduce la varianza del estimador de anomalía agregando perspectivas complementarias. PyOD [@zhao2019pyod] implementa esta estrategia con la clase `LSCP` (Locally Selective Combination in Parallel Outlier Ensembles) y otras técnicas de combinación estándar.

### 2.3.5 Forecasting de Series Temporales con Transformers

Las series temporales agroexportadoras presentan tres desafíos que los modelos de forecasting deben resolver: tendencia no estacionaria, estacionalidad múltiple (diaria, semanal, mensual, anual) y dependencia de covariables exógenas (clima, calendario agrícola, demanda internacional, precios y condiciones logísticas). Los modelos estadísticos clásicos como ARIMA capturan relaciones lineales con eficacia, pero presentan limitaciones en la modelización de no-linealidades y horizontes largos.

**Temporal Fusion Transformer (TFT)** [@lim2020tft] propone una arquitectura especializada que combina cuatro mecanismos: (1) codificación LSTM para dependencias secuenciales locales; (2) selección de variables con mecanismo de gating (GLU — Gated Linear Unit) que identifica automáticamente las covariables más informativas; (3) atención multi-cabezal interpretable que pondera los pasos temporales según su relevancia predictiva; y (4) red de cuantiles para cuantificar la incertidumbre de la predicción. TFT acepta tres tipos de entradas: features estáticas conocidas (e.g., producto, zona, destino), covariables futuras conocidas (e.g., calendario agrícola, campañas, feriados) y covariables históricas observadas (e.g., precio, volumen, clima o merma pasada).

El debate sobre la efectividad de los Transformers en series temporales es relevante para esta tesis. Zeng et al. (2023) [@zeng2023dlinear] argumentan que DLinear —un modelo lineal simple— supera a los Transformers en múltiples benchmarks, atribuyendo la limitación de los Transformers al hecho de que el mecanismo de self-attention es permutation-invariant y destruye el orden temporal de las secuencias. Sin embargo, este argumento ha sido rebatido sucesivamente: Nie et al. (2023) [@nie2023patchtst] demuestran que la tokenización por patches —agrupando segmentos temporales antes de aplicar atención— preserva el orden local y supera a DLinear en la mayoría de benchmarks de horizonte largo. Liu et al. (2024) [@liu2024itransformer] proponen invertir la tokenización: en lugar de tokenizar por timestamp, tokenizan por variable, aplicando self-attention entre variables en lugar de entre tiempos, obteniendo SOTA en 7 datasets multivariados.

**Posición de esta tesis respecto al debate**: TFT se considera por su interpretabilidad incorporada —el mecanismo de gating y los mapas de atención son legibles por analistas— más que exclusivamente por su rendimiento predictivo. En el contexto agroexportador, la capacidad de justificar qué períodos temporales y qué covariables fundamentan la predicción es un requerimiento funcional comparable en importancia a la precisión numérica.

N-HiTS [@nhts2022] ofrece una alternativa no-Transformer para forecasting de horizonte largo, con interpolación jerárquica multi-tasa que reduce la complejidad computacional respecto a N-BEATS. Chronos [@chronos2024] representa el paradigma emergente de los foundation models para series temporales, basado en T5, que logra performance zero-shot competitivo en múltiples datasets; sin embargo, su opacidad y dependencia de infraestructura de gran escala limitan su aplicación directa cuando se requiere trazabilidad operativa.

### 2.3.6 Explicabilidad mediante Valores de Shapley (SHAP)

La explicabilidad en sistemas de IA se clasifica en dos grandes categorías: **inherente** —modelos cuya estructura es intrínsecamente interpretable, como los árboles de decisión— y **post-hoc** —métodos aplicados a cualquier modelo después del entrenamiento para interpretar sus predicciones. SHAP y LIME son los dos métodos post-hoc agnósticos más adoptados en la literatura.

**LIME** (Local Interpretable Model-agnostic Explanations) [@ribeiro2016lime] genera explicaciones locales construyendo un modelo lineal sustituto en el vecindario de la instancia a explicar, ponderando las muestras según su proximidad al punto de interés. LIME es rápido y flexible, pero produce explicaciones inestables: pequeñas perturbaciones de la instancia pueden cambiar significativamente la explicación, un problema crítico en contextos forenses.

**SHAP** [@lundberg2017shap] fundamenta las explicaciones en los valores de Shapley de la teoría de juegos cooperativos. El valor SHAP de la feature $i$ para la predicción $f(x)$ cuantifica la contribución marginal media de $i$ a la predicción, promediando sobre todas las coaliciones posibles de features:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!} [f(S \cup \{i\}) - f(S)]$$

donde $F$ es el conjunto de todas las features y $S$ es una coalición de features sin $i$. Esta formulación garantiza cuatro propiedades axiomáticas: (a) **eficiencia** — la suma de todos los valores SHAP iguala la diferencia entre la predicción y el valor esperado; (b) **simetría** — features con contribución idéntica reciben el mismo valor; (c) **dummy** — features sin efecto tienen valor cero; y (d) **aditividad** — los valores SHAP son consistentes al combinar modelos.

SHAP resuelve las limitaciones de LIME al garantizar consistencia: si un modelo cambia la predicción al aumentar la contribución de una feature, el valor SHAP de esa feature nunca disminuye [@lundberg2017shap]. **TreeSHAP** extiende este cálculo con un algoritmo exacto en O(TLD²) para modelos basados en árboles —donde T es el número de árboles, L es el número de hojas por árbol y D es la profundidad máxima— haciendo el cálculo computacionalmente viable para GBDT en producción.

En el contexto de supervisión operativa, la estabilidad de las explicaciones permite verificar que el modelo asigna importancias consistentes a variables semejantes. Un índice alto de estabilidad fortalece la confianza en el sistema, porque evita que alertas similares reciban justificaciones contradictorias.

La integración SHAP+LLM de esta tesis opera como sigue: los vectores SHAP de una alerta operativa (una lista de pares variable→contribución cuantitativa) se incorporan como contexto verificado en el RAG, y el LLM genera la narración del informe sin posibilidad de inventar cifras que no estén en esos vectores o en las fuentes recuperadas.

### 2.3.7 Modelos de Lenguaje y Arquitectura RAG para Generación de Reportes

Los Modelos de Lenguaje de Gran Tamaño (LLMs) son sistemas entrenados mediante autoregresión en corpus masivos de texto para aprender distribuciones probabilísticas sobre secuencias de tokens. Su capacidad de generalización les permite realizar tareas de reasoning, traducción, resumen y generación de texto con calidad próxima a la humana en configuraciones zero-shot y few-shot.

**In-context learning** permite guiar el comportamiento del LLM mediante ejemplos incluidos directamente en el prompt, sin necesidad de ajuste fino (fine-tuning). TabLLM [@tabllm2023] demostró que mediante serialización de datos tabulares a texto descriptivo, los LLMs pueden realizar clasificación sobre datos estructurados con rendimiento no trivial en zero-shot, ampliando el espectro de aplicación de estos modelos más allá del texto no estructurado.

Sin embargo, el uso de LLMs como agentes de decisión autónoma introduce el riesgo de **alucinaciones**: el modelo puede generar afirmaciones coherentes en forma pero incorrectas en contenido [@survey2026hallucination]. En particular, las "alucinaciones numéricas" —valores específicos de métricas, porcentajes o fechas que no corresponden a los datos reales— son peligrosas en reportes operativos, porque pueden inducir decisiones equivocadas.

**Retrieval-Augmented Generation (RAG)** [@schneider2025rag] mitiga este riesgo al separar el conocimiento factual del modelo generativo: en lugar de que el LLM "recuerde" información de su entrenamiento, el sistema recupera documentos o datos relevantes de una base de conocimiento externa verificada y los incluye en el contexto del prompt. El LLM entonces genera texto fundamentado en esos datos recuperados, no en su memoria paramétrica. Técnicas avanzadas como GraphRAG incorporan grafos de conocimiento para recuperación semántica más rica, mientras que Self-RAG permite al modelo verificar la pertinencia de los documentos recuperados antes de usarlos.

En la arquitectura de esta tesis, la "base de conocimiento" del RAG son los vectores SHAP de la alerta analizada, las métricas del ensemble de detección, las fuentes agroexportadoras recuperadas y las reglas de reporte definidas. El LLM recibe ese contexto verificado y genera el informe narrativo sin acceso a conocimiento adicional no validado. Este diseño permite que cada afirmación del reporte pueda trazarse hasta una fuente, score, umbral o variable explicativa.

La evaluación de calidad de los reportes generados puede utilizar **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) cuando exista un texto de referencia. Sin embargo, para esta tesis se prioriza una rúbrica operativa de completitud, consistencia, accionabilidad y correspondencia con evidencias, porque la calidad de un reporte de supervisión depende no solo de similitud textual, sino de su utilidad para la toma de decisiones.

### 2.3.8 Gobernanza de IA y MLOps

El despliegue de sistemas de IA en entornos empresariales críticos requiere un marco de gobernanza que trascienda el rendimiento técnico. Sculley et al. (2015) [@sculley2015hidden] documentaron la "deuda técnica oculta" en sistemas de ML: más del 95% del código de un sistema ML de producción no es el modelo en sí, sino la infraestructura de ingesta, validación, features, servicio y monitoreo. Los pipelines con alto acoplamiento entre componentes generan "entanglement" que dificulta el mantenimiento y aumenta el riesgo de regresiones silenciosas.

**MLOps** [@kreuzberger2022mlops] establece el conjunto de prácticas para gestionar el ciclo de vida completo de los modelos ML en producción: integración y entrega continua (CI/CD) para modelos, monitoreo de data drift y model drift, automatización del reentrenamiento, y trazabilidad de versiones de datos, código y modelos. En el contexto de supervisión operativa agroexportadora, MLOps permite reproducir qué modelo generó una alerta, con qué datos de entrada, bajo qué versión y con qué umbral.

El **NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0)** [@nist2023aia] proporciona cuatro funciones de gestión de riesgo para sistemas de IA: (1) **Govern** — establecer políticas y roles de responsabilidad; (2) **Map** — identificar el contexto de despliegue y los riesgos asociados; (3) **Measure** — evaluar los riesgos con métricas verificables; y (4) **Manage** — implementar controles y mitigaciones. La arquitectura modular de esta tesis es diseñada para que cada capa corresponda a responsabilidades verificables bajo este framework.

**Datasheets for Datasets** [@gebru2021datasheets] propone una plantilla de documentación estandarizada para datasets que detalla: motivación de recolección, proceso de recolección, composición, preprocesamiento aplicado, distribución permitida y consideraciones éticas. Esta práctica se aplicará al dataset sintético agroexportador y a las fuentes públicas utilizadas, garantizando que los resultados reportados en esta tesis sean reproducibles y que las limitaciones de cada fuente estén identificadas antes de evaluar el sistema.

**Model Cards** [@mitchell2019model] extiende la documentación al nivel del modelo, especificando para quién fue entrenado, en qué condiciones, cuáles son sus limitaciones conocidas y cómo debe usarse de manera responsable. En esta tesis, se elaboran Model Cards para los modelos XGBoost/LightGBM, detectores de anomalías y el componente LLM+RAG, en conformidad con los principios de documentación del NIST AI RMF [@nist2023aia].

El contexto peruano e internacional consolida la necesidad de este framework de gobernanza. El D.S. N° 115-2025-PCM [@pcm2025leyia], el NIST AI RMF [@nist2023aia] y el EU AI Act [@eu2024aiact] refuerzan principios comunes: transparencia, documentación, supervisión humana y gestión de riesgos. Estos principios son adoptados como referencia para diseñar el flujo de revisión humana y trazabilidad de alertas en el sistema propuesto.

### 2.3.9 Supervisión Operativa, Trazabilidad e Inteligencia Artificial

La supervisión operativa en agroexportación exige monitorear procesos que combinan producción, acopio, calidad, sanidad, logística y comercio exterior. Las anomalías en este dominio no necesariamente corresponden a fraude; pueden representar variaciones atípicas de precio, caídas de volumen, condiciones climáticas adversas, mermas elevadas, incumplimientos fitosanitarios o retrasos logísticos. Por ello, el sistema propuesto se orienta a detectar desviaciones relevantes para la toma de decisiones, no a sustituir procesos de investigación legal o auditoría financiera.

La **supervisión operativa continua** busca reemplazar ciclos de revisión tardíos por monitoreo frecuente y documentado de indicadores. En este enfoque, cada alerta debe registrar el dato de origen, el modelo aplicado, el score calculado, el umbral utilizado, las variables explicativas y el reporte generado. Esta trazabilidad permite que un supervisor operativo comprenda por qué el sistema marcó un evento como anómalo y qué evidencia respalda la recomendación.

La integración de IA en supervisión operativa plantea el problema de la confianza en decisiones automáticas. Esta exigencia convierte a la explicabilidad (SHAP), la documentación de datasets (Datasheets), la documentación de modelos (Model Cards) y los logs de decisión en componentes funcionales del sistema. En el marco peruano, el D.S. N° 115-2025-PCM [@pcm2025leyia] proporciona una base general para el uso responsable de IA; la Resolución SBS N° 053-2023 [@sbs2023riesgos] se conserva solo como referencia nacional de buenas prácticas para gestión de riesgo de modelos.

---

# CAPÍTULO III: PROPUESTA METODOLÓGICA

## 3.1 Arquitectura del Sistema Integrado

La arquitectura propuesta se divide en cuatro módulos secuenciales, diseñados para maximizar trazabilidad, interpretabilidad y utilidad operativa en procesos agroexportadores:

- **Módulo de Predicción Tabular (Capa 1):** Utiliza algoritmos GBDT como núcleo predictivo, priorizando XGBoost [@chen2016xgboost] y LightGBM [@ke2017lightgbm] por su robustez ante datos tabulares con variables heterogéneas [@grinsztajn2022trees]. El módulo puede estimar valores esperados de precio, volumen, merma o riesgo operativo.
- **Módulo de Detección de Anomalías (Capa 2):** Emplea detectores como Isolation Forest [@liu2008iforest], LOF [@breunig2000lof] y ECOD [@li2022ecod], orquestados mediante PyOD [@zhao2019pyod], para identificar comportamientos atípicos en variables agroexportadoras.
- **Módulo de Explicabilidad (Capa 3):** SHAP [@lundberg2017shap] genera explicaciones locales por alerta, identificando qué variables —precio, volumen, clima, destino, cumplimiento o merma— contribuyen al score del sistema.
- **Módulo de Reportes LLM+RAG (Capa 4):** Un LLM restringido a evidencias estructuradas mediante RAG [@schneider2025rag] redacta reportes operativos trazables. El LLM no decide si existe una anomalía; solo traduce scores, umbrales y explicaciones SHAP a lenguaje comprensible.

```
┌─────────────────────────────────────────────────────────┐
│ CAPA 4: Reporte Automatizado (LLM + RAG)               │
│ Entrada: anomalías + vectores SHAP                      │
│ Salida: reporte auditado en lenguaje natural (MD/PDF)  │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ CAPA 3: Explicabilidad (SHAP / TreeSHAP)               │
│ Entrada: predicciones + datos originales               │
│ Salida: vectores Shapley + SHAP Stability Index        │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ CAPA 2: Detección de Anomalías (Ensemble)              │
│ Métodos: IF + LOF + ECOD (PyOD)                        │
│ Salida: score anomalía + método que detectó            │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ CAPA 1: Predicción tabular agroexportadora             │
│ Modelo: XGBoost / LightGBM                             │
│ Entrada: precio, volumen, clima, calidad, logística    │
│ Salida: valor esperado + riesgo operativo              │
└─────────────────────────────────────────────────────────┘
```

## 3.2 Fuentes de Datos, Dataset Sintético y Benchmarks

Para validar la robustez del sistema sin depender obligatoriamente de datos privados, se emplearán tres niveles de información:

1. **Fuentes públicas oficiales del dominio agroexportador**: MIDAGRI para agroexportaciones, precios y productos; SENAMHI para variables climáticas; SENASA para requisitos fitosanitarios; SUNAT para exportaciones; INEI para indicadores económicos; FAOSTAT y UN Comtrade para validación internacional.
2. **Dataset sintético agroexportador documentado**: conjunto de registros simulados con variables como fecha, producto, zona, volumen, precio, temperatura, precipitación, humedad, destino, cumplimiento fitosanitario, días logísticos, merma, etiqueta de anomalía y tipo de anomalía. Este dataset se documentará con criterios de Datasheets for Datasets [@gebru2021datasheets].
3. **Benchmark metodológico complementario**: BAF Benchmark [@jesus2022baf] podrá utilizarse solo para contrastar comportamiento de modelos en datos tabulares desbalanceados con drift temporal, sin presentarlo como validación directa del dominio agroexportador.

## 3.3 Configuración Experimental y Métricas

- **Métricas de predicción y detección**: PR-AUC (métrica principal para datasets desbalanceados), ROC-AUC, F1-Score, Precision y Recall con umbral óptimo.
- **Métricas de explicabilidad**: cobertura top-k SHAP, consistencia cualitativa de variables explicativas y claridad operativa (Likert 1–5).
- **Métricas de calidad de reportes**: completitud, consistencia, accionabilidad, correspondencia con evidencias y, cuando exista referencia humana, ROUGE-1/ROUGE-L.
- **Métricas de comprensión y decisión**: tiempo-a-decisión (segundos), comprensión de alerta (Likert 1–5) y decisión final correcta.
- **Métricas de trazabilidad**: porcentaje de alertas con dato de origen, versión de dataset, modelo, score, umbral, explicación SHAP, fuente recuperada por RAG y reporte generado.

---

# CAPÍTULO IV: RESULTADOS Y DISCUSIÓN

## 4.1 Resultados Cuantitativos (Predicción y Detección)

*(Sección reservada para la inserción de métricas resultantes: PR-AUC del ensemble GBDT, comparativa detector único vs. ensemble, velocidad de inferencia de LightGBM respecto a XGBoost, y comparativas de forecasting entre TFT y DLinear [@zeng2023dlinear] como baseline).*

## 4.2 Resultados Cualitativos (Generación de Reportes LLM-RAG)

*(Sección reservada para ilustrar cómo el módulo LLM+RAG transforma los vectores SHAP crudos en explicaciones narrativas auditables, con ejemplos de reportes generados y evaluación ROUGE-1 vs. referencia humana).*

## 4.3 Discusión de Resultados

La arquitectura propuesta se evaluará frente a enfoques basados en componentes aislados, considerando rendimiento técnico, trazabilidad documental y utilidad para la supervisión operativa agroexportadora.

### 4.3.1 Superioridad de GBDT sobre Deep Learning en Datos Tabulares

Los hallazgos se discutirán a la luz del benchmark de Grinsztajn et al. [-@grinsztajn2022trees], que respalda el uso de modelos basados en árboles para datos tabulares. En el contexto agroexportador, esta elección se justifica por la heterogeneidad de variables como precio, volumen, clima, producto, zona, destino y cumplimiento fitosanitario. Los trabajos de fraude financiero y auditoría se conservarán solo como antecedentes metodológicos sobre datos tabulares desbalanceados y explicabilidad, no como evidencia principal del dominio.

### 4.3.2 Restricción Determinista de LLMs frente al Riesgo de Alucinación

En contraste con arquitecturas donde el LLM actúa como agente autónomo de toma de decisiones [@park2024llm], este sistema relega al LLM estrictamente a la capa de traducción narrativa mediante RAG [@schneider2025rag]. Esta decisión reduce el riesgo documentado de alucinaciones [@survey2026hallucination]. Al restringir al LLM a interpretar scores, umbrales, variables SHAP y contexto recuperado, el sistema mantiene fidelidad a las evidencias operativas.

### 4.3.3 Cumplimiento Regulatorio y Gobernanza

La interpretabilidad post-hoc (SHAP) implementada en el sistema responde a principios modernos de gobernanza de IA: transparencia, documentación, supervisión humana y trazabilidad. En el contexto nacional, el D.S. N° 115-2025-PCM [@pcm2025leyia] proporciona el marco general de IA responsable. La Resolución SBS N° 053-2023 [@sbs2023riesgos] se utiliza como referencia nacional de buenas prácticas para gestión de riesgo de modelos, sin asumir obligación directa para empresas agroexportadoras. A nivel internacional, el EU AI Act [@eu2024aiact] y NIST AI RMF [@nist2023aia] refuerzan la necesidad de documentar decisiones y riesgos de sistemas de IA.

---

# CAPÍTULO V: CONCLUSIONES Y TRABAJOS FUTUROS

## 5.1 Conclusiones

*(Esqueleto para la síntesis final: el sistema integrado logró los objetivos propuestos, manteniendo el balance entre vanguardia tecnológica y rigor legal. Incluir: conclusión sobre el gap cerrado, métricas alcanzadas vs. objetivos, validación de hipótesis H1a–H1d, aporte al contexto regulatorio peruano).*

## 5.2 Limitaciones de la Investigación

*(Abordar: limitaciones del dataset sintético agroexportador; granularidad y disponibilidad de fuentes públicas; dependencia de la calidad de datos documentada en Datasheets for Datasets [@gebru2021datasheets]; deuda técnica de mantenimiento del pipeline MLOps [@sculley2015hidden]; limitaciones del tamaño de la muestra en la evaluación de comprensión; restricciones de los LLMs actuales en precisión de cálculo aritmético [@survey2026hallucination]).*

## 5.3 Trabajos Futuros

*(Propuestas: integración de GraphRAG para recuperación semántica más rica sobre conocimiento agroexportador; extensión del ensemble con ECOD [@li2022ecod] y modelos de concept drift para supervisión en stream; exploración de Chronos [@chronos2024] para forecasting de horizonte largo; prueba piloto en una empresa agroexportadora peruana; evaluación de sesgos y limitaciones según Datasheets for Datasets [@gebru2021datasheets]).*

---

# CRONOGRAMA DE ACTIVIDADES

*(Ver Tabla 1.2 en el Capítulo I, §1.11)*

---

# CONCLUSIONES

*(Por completar con los resultados finales de la investigación. Estructura sugerida:)*

1. *(Conclusión sobre el gap cerrado: el sistema integrado de cuatro capas constituye la primera propuesta académica en el Perú que unifica predicción GBDT, detección de anomalías ensemble, explicabilidad SHAP y generación de reportes LLM+RAG con trazabilidad regulatoria verificable para el contexto agroexportador.)*

2. *(Conclusión sobre métricas alcanzadas: los objetivos específicos OE1–OE5 fueron alcanzados según las métricas definidas — PR-AUC ≥ 0.92, SHAP Coverage ≥ 70%, ROUGE-1 ≥ 0.50, reducción tiempo-a-decisión ≥ 30%...)*

3. *(Conclusión sobre validación de hipótesis H1a–H1d.)*

4. *(Conclusión sobre gobernanza: el diseño incorpora principios de trazabilidad, documentación y supervisión humana alineados con el D.S. N° 115-2025-PCM, NIST AI RMF y buenas prácticas de gestión de riesgo de modelos.)*

5. *(Conclusión sobre aporte al campo: el sistema integrado proporciona mayor trazabilidad y usabilidad que los sistemas con componentes aislados, validado mediante experimentos comparativos controlados.)*

---

# CONCLUSIONS

*(Por completar — versión en inglés de las conclusiones principales)*

1. *(The integrated four-layer system constitutes the first academic proposal in Peru that unifies GBDT prediction, ensemble anomaly detection, SHAP explainability, and LLM+RAG report generation with verifiable regulatory traceability.)*

2. *(Technical objectives OE1–OE5 were achieved according to defined metrics — PR-AUC ≥ 0.92, SHAP Coverage ≥ 70%, ROUGE-1 ≥ 0.50, decision-time reduction ≥ 30%.)*

3. *(The integrated system produces superior traceability and usability compared to isolated-component systems, as validated through controlled comparative experiments.)*

4. *(The design incorporates traceability, documentation, and human oversight principles aligned with D.S. N° 115-2025-PCM, NIST AI RMF, and model risk management good practices.)*

---

# RECOMENDACIONES

1. **Para implementadores**: Se recomienda iniciar el despliegue del sistema con el módulo de predicción GBDT y el módulo de explicabilidad SHAP antes de integrar el componente LLM+RAG, siguiendo el principio de implementación incremental que reduce la deuda técnica [@sculley2015hidden] y permite validar cada capa de forma independiente.

2. **Para empresas agroexportadoras**: Antes de adoptar el sistema en producción, se recomienda elaborar Datasheets for Datasets [@gebru2021datasheets] para todos los datasets de entrenamiento y Model Cards [@mitchell2019model] para los modelos XGBoost, detectores de anomalías y LLM+RAG.

3. **Para futuros investigadores**: Se recomienda extender la evaluación del sistema con un diseño experimental longitudinal que capture el efecto del concept drift en precios, volúmenes, clima y comportamiento exportador, utilizando ventanas temporales y fuentes agroexportadoras reales.

4. **Para entidades públicas y sectoriales**: Se recomienda promover guías técnicas de IA explicable y trazabilidad para sistemas de supervisión en cadenas productivas, tomando como referencia marcos nacionales e internacionales de gobernanza de IA.

5. **Para la academia**: Se recomienda replicar el estudio con datos reales de una empresa agroexportadora colaboradora (bajo acuerdo de confidencialidad), ampliar la muestra de evaluación con supervisores operativos y responsables de calidad, e incorporar métricas de sesgo y robustez según las dimensiones de evaluación de ADBench [@han2022adbench].

---

# GLOSARIO DE TÉRMINOS

**ADBench** (*Anomaly Detection Benchmark*): Benchmark sistemático para evaluación comparativa de algoritmos de detección de anomalías, propuesto por Han et al. (2022), que cubre 57 datasets y 30 algoritmos bajo tres niveles de supervisión.

**Alucinación (LLM)**: Fenómeno en el que un modelo de lenguaje genera texto coherente en forma pero incorrecto en contenido, incluyendo afirmaciones factuales erróneas, citas inexistentes o cifras fabricadas.

**AUC-PR** (*Area Under the Precision-Recall Curve*): Métrica de evaluación para clasificadores en datasets desbalanceados; a diferencia de AUC-ROC, es sensible a la distribución de clases y penaliza los falsos positivos de forma más relevante en contextos de fraude y anomalías raras.

**BAF Benchmark** (*Bank Account Fraud*): Dataset tabular de referencia para fraude bancario con drift temporal y desbalance de clases, publicado por Jesus et al. (2022). En esta tesis se considera únicamente como benchmark metodológico complementario para evaluar robustez tabular, no como validación directa del dominio agroexportador.

**CatBoost**: Algoritmo GBDT desarrollado por Yandex (Prokhorenkova et al., 2018) que resuelve el problema de target leakage en variables categóricas mediante Ordered Boosting.

**Concept Drift**: Cambio en la distribución estadística de los datos a lo largo del tiempo que degrada el rendimiento de modelos entrenados con datos históricos; particularmente relevante en detección de fraude y anomalías operativas.

**Deep SVDD** (*Deep Support Vector Data Description*): Método de detección de anomalías basado en redes neuronales que aprende una hipersfera mínima en el espacio latente que contiene los datos normales (Ruff et al., 2018).

**ECOD** (*Empirical Cumulative distribution functions Outlier Detection*): Detector de anomalías sin parámetros basado en distribuciones empíricas acumuladas (Li et al., 2022), notable por su ausencia de hiperparámetros a calibrar.

**EU AI Act** (*Reglamento (UE) 2024/1689*): Reglamento europeo de inteligencia artificial que clasifica los sistemas de IA por nivel de riesgo y establece obligaciones de transparencia y explicabilidad en el Artículo 13 para sistemas de alto riesgo.

**GBDT** (*Gradient Boosting Decision Trees*): Familia de algoritmos de aprendizaje supervisado que construyen modelos predictivos mediante la combinación secuencial de árboles de decisión débiles, minimizando una función de pérdida mediante descenso de gradiente funcional.

**Isolation Forest**: Algoritmo de detección de anomalías no supervisado (Liu et al., 2008) que aísla anomalías mediante particionamiento aleatorio del espacio de datos, con complejidad computacional O(n).

**LightGBM**: Algoritmo GBDT de Microsoft (Ke et al., 2017) que acelera el entrenamiento hasta 20× mediante Gradient-based One-Side Sampling y estructuras de datos basadas en histogramas.

**LLM** (*Large Language Model*): Modelo de lenguaje de gran tamaño entrenado en corpus masivos de texto para aprender distribuciones probabilísticas sobre secuencias de tokens, capaz de realizar tareas de generación, resumen y razonamiento en lenguaje natural.

**LOF** (*Local Outlier Factor*): Detector de anomalías basado en densidad local relativa (Breunig et al., 2000) que cuantifica el grado de anomalía de un punto comparando su densidad con la de sus vecinos k-NN.

**MLOps** (*Machine Learning Operations*): Conjunto de prácticas para gestionar el ciclo de vida completo de modelos ML en producción, incluyendo CI/CD, monitoreo de drift, automatización de reentrenamiento y trazabilidad de versiones.

**NIST AI RMF**: Framework de gestión de riesgo para sistemas de IA publicado por el Instituto Nacional de Estándares y Tecnología de EE.UU. (2023), organizado en cuatro funciones: Govern, Map, Measure y Manage.

**PR-AUC**: Ver AUC-PR.

**PyOD** (*Python Outlier Detection*): Librería de Python que implementa más de 40 algoritmos de detección de outliers con una API estandarizada compatible con scikit-learn (Zhao et al., 2019).

**RAG** (*Retrieval-Augmented Generation*): Arquitectura para modelos de lenguaje que separa el conocimiento factual del modelo generativo, recuperando documentos relevantes de una base de conocimiento externa para anclar las respuestas y mitigar alucinaciones.

**Resolución SBS N° 053-2023**: Resolución de la Superintendencia de Banca, Seguros y AFP del Perú que establece lineamientos de gestión de riesgos de modelos para entidades supervisadas. En esta tesis se utiliza como referencia nacional de buenas prácticas para trazabilidad, validación y monitoreo, no como obligación directa para empresas agroexportadoras.

**ROUGE** (*Recall-Oriented Understudy for Gisting Evaluation*): Conjunto de métricas para evaluación automática de resúmenes y textos generados mediante comparación de superposición de n-gramas con un texto de referencia humano.

**SHAP** (*SHapley Additive exPlanations*): Marco de explicabilidad post-hoc que asigna a cada feature una contribución marginal promediada sobre todas las coaliciones posibles, garantizando consistencia axiomática (Lundberg & Lee, 2017).

**SHAP Stability Index**: Métrica de coherencia de explicaciones SHAP entre instancias similares, que certifica que el modelo asigna importancias consistentes a features semejantes, requisito en contextos forenses.

**TFT** (*Temporal Fusion Transformer*): Arquitectura de Transformer para forecasting multi-horizonte interpretable con covariables exógenas, mecanismo de gating y predicción por cuantiles (Lim et al., 2021).

**TreeSHAP**: Algoritmo exacto para el cálculo de valores SHAP en modelos basados en árboles, con complejidad O(TLD²), que hace viable la explicabilidad en GBDT de producción con millones de transacciones.

**XGBoost** (*eXtreme Gradient Boosting*): Implementación escalable de gradient boosting (Chen & Guestrin, 2016) con regularización L1/L2, manejo nativo de valores faltantes y paralelización por columnas; baseline universal en competencias de ML con datos tabulares.

---

# REFERENCIAS BIBLIOGRÁFICAS

Almalki, F., & Masud, M. (2025). *Financial fraud detection using explainable AI and stacking ensemble methods*. arXiv preprint arXiv:2505.10050.

Ansari, A. F., Stella, L., Turkmen, C., Zhang, X., Mercado, P., Sinha, R., & Bergmeir, C. (2024). *Chronos: Learning the language of time series*. arXiv preprint arXiv:2403.07815.

Arik, S. O., & Pfister, T. (2021). TabNet: Attentive interpretable tabular learning. *Proceedings of the AAAI Conference on Artificial Intelligence*, *35*(8), 6679–6687. https://doi.org/10.1609/aaai.v35i8.16842

Barclays Research. (2025). *Beyond the black box: Interpretability of LLMs in finance*. arXiv preprint arXiv:2505.24650.

Breunig, M. M., Kriegel, H.-P., Ng, R. T., & Sander, J. (2000). LOF: Identifying density-based local outliers. *ACM SIGMOD Record*, *29*(2), 93–104. https://doi.org/10.1145/342009.335388

Center for Audit Quality. (2024). *Auditing in the age of generative AI*. CAQ. https://thecaq.org/wp-content/uploads/2024/04/caq_auditing-in-the-age-of-generative-ai__2024-04.pdf

Challu, C., Olivares, K. G., Oreshkin, B., Garza, F., Mergenthaler-Canseco, M., & Dubrawski, A. (2022). N-HiTS: Neural hierarchical interpolation for time series forecasting. *Advances in Neural Information Processing Systems*, *35*. (arXiv:2201.12886)

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794. https://doi.org/10.1145/2939672.2939785

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM*, *64*(12), 86–92. https://doi.org/10.1145/3458723

Gorishniy, Y., Rubashevskiy, I., Khrulkov, V., & Babenko, A. (2021). Revisiting deep learning models for tabular data. *Advances in Neural Information Processing Systems 34 (NeurIPS)*, 8946–8959.

Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on tabular data? *Advances in Neural Information Processing Systems 35 (NeurIPS)*, 507–520.

Han, X., Hu, Y., Venevdev, L., Liu, M., Wen, Q., & Zhang, Y. (2022). ADBench: Anomaly detection benchmark. *Advances in Neural Information Processing Systems*, *35*.

Hegselmann, S., Buendia, A., Lang, H., Agrawal, M., Jiang, X., & Sontag, D. (2022). TabLLM: Few-shot classification of tabular data with large language models. arXiv preprint arXiv:2210.10723.

Hyndman, R. J., & Khandakar, Y. (2008). Automatic time series forecasting: The forecast package for R. *Journal of Statistical Software*, *27*(3), 1–22. https://doi.org/10.18637/jss.v027.i03

Jesus, S., Pombal, J., Alves, D., Cruz, A., Saleiro, P., Ribeiro, R. P., Gama, J., & Bizarro, P. (2022). *Turning the tables: Biased, imbalanced, dynamic tabular datasets for ML evaluation*. arXiv preprint arXiv:2211.13358. [NeurIPS 2022]

Kadir, M. A., Macharla Vasu, S. S., Nair, S. S., & Sonntag, D. (2025). AuditCopilot: Leveraging LLMs for fraud detection in double-entry bookkeeping. arXiv preprint arXiv:2512.02726. https://doi.org/10.48550/arXiv.2512.02726

Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems 30 (NeurIPS)*, 3146–3154.

Kreuzberger, D., Kühl, N., & Hirschl, G. (2022). MLOps: Overview, definition, and architecture. *IEEE Access*, *10*, 86995–87010. https://doi.org/10.1109/ACCESS.2022.3197550

Leocádio, D., et al. (2024). *Continuous auditing artificial intelligence framework*. [Pending venue publication]

Lewis, P., Perez, E., Piktus, A., Schwenk, H., Schwab, C., Yeh, C., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 9457–9474. https://doi.org/10.18653/v1/2020.emnlp-main.727

Li, Z., Zhao, Y., Hu, X., Botta, N., Ionescu, C., & Chen, G. H. (2022). ECOD: Unsupervised outlier detection using empirical cumulative distribution functions. *IEEE Transactions on Knowledge and Data Engineering*, *35*(12), 12181–12193. https://doi.org/10.1109/TKDE.2022.3159580

Lim, B., Arik, S. O., Loeff, N., & Pfister, T. (2021). Temporal fusion transformers for interpretable multi-horizon time series forecasting. *International Conference on Learning Representations (ICLR)*. (arXiv:1912.09300)

Lin, C.-Y. (2004). ROUGE: A package for automatic evaluation of summaries. *Proceedings of the Workshop on Text Summarization Branches Out (ACL 2004)*, 74–81.

Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation forest. *Proceedings of the 8th IEEE International Conference on Data Mining (ICDM)*, 413–422. https://doi.org/10.1109/ICDM.2008.17

Liu, Y., Hu, T., Zhang, H., Wu, H., Wang, S., Ma, L., & Long, M. (2024). iTransformer: Inverted transformers are effective for time series forecasting. *International Conference on Learning Representations (ICLR)*.

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems 30 (NeurIPS)*, 4765–4774.

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model cards for model reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency (FAccT)*, 220–229. https://doi.org/10.1145/3287560.3287596

National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)*. NIST. https://doi.org/10.6028/NIST.AI.600-1

Nie, Y., Nguyen, N. H., Sinthong, P., & Kalagnanam, J. (2023). A time series is worth 64 words: Long-term forecasting with transformers. *International Conference on Learning Representations (ICLR)*.

Oreshkin, B. N., Carpov, D., Chapados, N., & Bengio, Y. (2020). N-BEATS: Neural basis expansion analysis for interpretable time series forecasting. *Proceedings of the 37th International Conference on Machine Learning (ICML)*, 4799–4808. https://doi.org/10.5555/3524938.3525255

Papineni, K., Roukos, S., Ward, T., & Zhu, W.-J. (2002). BLEU: A method for automatic evaluation of machine translation. *Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics (ACL)*, 311–318. https://doi.org/10.3115/1073083.1073135

Park, S. (2024). *LLMs for anomaly validation and report generation in financial systems*. arXiv preprint arXiv:2403.19735.

Patel, R., Khan, F., Silva, B., & Shaturaev, J. (2024). AI-driven continuous auditing and real-time financial monitoring. *International Research Journal of Modernization in Engineering Technology and Science*.

Parlamento Europeo y Consejo de la Unión Europea. (2024). *Reglamento (UE) 2024/1689 por el que se establecen normas armonizadas en materia de inteligencia artificial (Ley de Inteligencia Artificial)*. Diario Oficial de la Unión Europea. https://eur-lex.europa.eu/eli/reg/2024/1689

Prenio, J., & Yong, J. (2024). *Managing explanations: How regulators can address AI explainability*. Bank for International Settlements, Financial Stability Institute. https://www.bis.org/fsi/fsipapers24.pdf

Presidencia del Consejo de Ministros. (2025, septiembre). *Decreto Supremo N° 115-2025-PCM: Reglamento de la Ley N° 31814*. Lima, Perú. https://busquedas.elperuano.pe

Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: Unbiased boosting with categorical features. *Advances in Neural Information Processing Systems 31 (NeurIPS)*, 6638–6648. https://doi.org/10.5555/3327757.3327790

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 1135–1144. https://doi.org/10.1145/2939672.2939778

Ruff, L., Kauffmann, J. R., Vandermeulen, R. A., Montavon, G., Samek, W., Kloft, M., Dickhaus, T., & Müller, K.-R. (2018). Deep one-class classification. *Proceedings of the 35th International Conference on Machine Learning (ICML)*, 4393–4402.

Schneider, J., et al. (2025). Retrieval-augmented generation (RAG). *Business & Information Systems Engineering*. https://doi.org/10.1007/s12599-025-00945-3

Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., & Young, M. (2015). Hidden technical debt in machine learning systems. *Proceedings of the 28th International Conference on Neural Information Processing Systems (NIPS) Workshop*.

Superintendencia de Banca, Seguros y AFP. (2023). *Resolución SBS N° 053-2023: Reglamento de gestión de riesgos de modelo*. Lima, Perú. https://www.sbs.gob.pe

Taylor, S. J., & Letham, B. (2017). *Forecasting at scale*. PeerJ Preprints. https://doi.org/10.7287/peerj.preprints.3190v2

Thanathamathee, P., et al. (2024). SHAP-instance weighting and anchor explainable AI: Enhancing XGBoost for financial fraud detection. *Emerging Science Journal*, *8*(6). https://doi.org/10.28991/ESJ-2024-08-06-024

Tsai, C.-P., et al. (2025). *LLM-based anomaly detection in tabular data*. [Pending venue publication]

Varios autores. (2025). *Hallucination detection and mitigation in large language models*. arXiv preprint arXiv:2601.09929.

Varios autores. (2025). Financial statement fraud detection through an integrated machine learning and explainable AI framework. *Journal of Risk and Financial Management*, *19*(1), 13. https://doi.org/10.3390/jrfm19010013

Varios autores. (2025). Explainable AI for forensic analysis: A comparative study of SHAP and LIME in intrusion detection models. *Applied Sciences*, *15*(13), 7329. https://doi.org/10.3390/app15137329

Waltersdorfer, L., Ekaputra, F. J., Miksa, T., & Sabou, M. (2024). AuditMAI: Towards an infrastructure for continuous AI auditing. arXiv preprint arXiv:2406.14243. https://doi.org/10.48550/arXiv.2406.14243

Zeng, A., Chen, M., Zhang, L., & Xu, Q. (2023). Are transformers effective for time series forecasting? *Proceedings of the AAAI Conference on Artificial Intelligence*, *37*(9), 11121–11128. https://doi.org/10.1609/aaai.v37i9.26317

Zhao, Y., Nasrullah, Z., & Li, Z. (2019). PyOD: A Python toolbox for scalable outlier detection. *Journal of Machine Learning Research*, *20*(96), 1–7.

---

# ANEXOS

## Anexo A — Protocolo de Evaluación de Usabilidad

*(Por completar — incluirá: instrucciones para el evaluador, descripción de las tareas cronometradas, cuestionario post-tarea, escala de confianza Likert, y formulario de consentimiento informado para los auditores participantes)*

### A.1 Descripción del Experimento

El experimento de usabilidad tiene como objetivo medir el impacto del sistema integrado en la eficiencia, comprensión y confianza de supervisores operativos o evaluadores al revisar reportes de anomalías agroexportadoras. Se utiliza un diseño within-subject: cada participante completa las mismas tareas primero con el sistema de componentes aislados (condición de control) y luego con el sistema integrado (condición experimental), o viceversa en orden contrabalanceado.

**Tareas evaluadas**:
1. Identificar las tres alertas operativas más relevantes de un lote de 50 registros agroexportadores
2. Justificar la decisión de marcar un registro como anomalía usando la información disponible
3. Redactar una conclusión operativa de dos párrafos basada en los hallazgos

**Métricas registradas**: tiempo de completación por tarea (segundos), tasa de acierto en clasificación, confianza post-tarea (Likert 1–5), satisfacción general con el sistema (SUS adaptado).

### A.2 Cuestionario Post-Tarea

*(Incluir el cuestionario completo de evaluación de confianza y usabilidad en la versión final)*

---

## Anexo B — Model Cards del Sistema

*(Por completar — se elaborarán Model Cards [@mitchell2019model] para los siguientes componentes del sistema:)*

- **Model Card: XGBoost/LightGBM (Módulo de Predicción)**: especificaciones de entrenamiento, métricas de rendimiento por segmento poblacional, limitaciones conocidas, usos apropiados e inapropiados.
- **Model Card: Ensemble IF+LOF+DeepSVDD (Módulo de Detección)**: umbrales de decisión, sensibilidad a concept drift, comparativa con detectores individuales.
- **Model Card: LLM+RAG (Módulo de Reportes)**: modelo base utilizado, restricciones de la arquitectura RAG, evaluación ROUGE, limitaciones de alucinación residual.

---

## Anexo C — Datasheet del Dataset de Evaluación

*(Por completar — Datasheet for Datasets [@gebru2021datasheets] para el dataset sintético agroexportador y las fuentes públicas utilizadas, cubriendo: motivación de selección, proceso de generación o recolección, composición, distribución de clases, preprocesamiento aplicado, sesgos identificados, limitaciones y condiciones de uso. BAF Benchmark [@jesus2022baf] quedará documentado solo si se utiliza como benchmark metodológico complementario.)*

---

## Anexo D — Registro de Uso de Herramientas de IA

La presente investigación utilizó herramientas de inteligencia artificial generativa como apoyo en las siguientes actividades: revisión bibliográfica exploratoria, verificación de coherencia de argumentos, corrección de estilo académico y generación de borradores de secciones específicas. Todas las referencias bibliográficas fueron verificadas manualmente en las fuentes originales. Las decisiones de diseño, la interpretación de resultados y las conclusiones son responsabilidad exclusiva del investigador.

*(Adjuntar registro detallado de las sesiones de uso según los requerimientos de transparencia de la UNSA)*

---

*(Documento elaborado con apoyo de herramientas de IA — UNSA Arequipa, 2026)*

