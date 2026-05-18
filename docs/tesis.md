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

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# RESUMEN

Esta tesis propone un sistema integrado de supervisión operativa para empresas agroexportadoras peruanas, que combina predicción tabular mediante modelos Gradient Boosting Decision Trees (GBDT), detección de anomalías operativas mediante ensemble de algoritmos, explicabilidad mediante SHAP (SHapley Additive exPlanations), y generación automática de reportes trazables con Modelos de Lenguaje de Gran Tamaño (LLMs) en arquitectura RAG (Retrieval-Augmented Generation).

El sistema aborda una brecha identificada en el contexto agroexportador: los procesos de producción, acopio, almacenamiento, control de calidad, logística, cumplimiento fitosanitario y comercialización internacional suelen analizarse mediante fuentes fragmentadas, reportes manuales o tableros aislados. Esta fragmentación dificulta la detección temprana de anomalías y reduce la trazabilidad de las decisiones. La propuesta se evalúa con métricas técnicas (PR-AUC, F1-Score, cobertura de trazabilidad), evaluación de comprensión operativa y datos públicos/sintéticos documentados del dominio agroexportador.

Las contribuciones principales son: (1) arquitectura modular de cuatro capas que separa predicción, detección, explicación y reporte; (2) integración de fuentes públicas oficiales y dataset sintético agroexportador documentado mediante criterios de Datasheets for Datasets (Gebru et al., 2021); (3) uso de SHAP para explicar alertas operativas a nivel de variable; (4) generación de reportes mediante RAG restringido a evidencias estructuradas, reduciendo el riesgo de alucinación; (5) evaluación comparativa del sistema integrado frente a componentes aislados en rendimiento, trazabilidad y tiempo de interpretación. La Resolución SBS N° 053-2023 se considera como referencia nacional de buenas prácticas para gestión de riesgo de modelos, mientras que el D.S. N° 115-2025-PCM se adopta como marco peruano general de gobernanza y supervisión humana en IA.

**Palabras clave**: supervisión operativa, detección de anomalías, agroexportación, explicabilidad IA, modelos de lenguaje, gobernanza, GBDT, reportes automáticos, trazabilidad, inteligencia artificial.

---

# ABSTRACT

This thesis proposes an integrated operational supervision system for Peruvian agro-export companies, combining tabular prediction using Gradient Boosting Decision Trees (GBDT), operational anomaly detection through an ensemble of algorithms, explainability through SHAP (SHapley Additive exPlanations), and traceable automatic report generation with Large Language Models (LLMs) in a Retrieval-Augmented Generation (RAG) architecture.

The system addresses an identified gap in agro-export operational supervision: production, storage, quality control, logistics, phytosanitary compliance, and international commercialization are commonly analyzed through fragmented sources, manual reports, or isolated dashboards. This fragmentation limits early anomaly detection and weakens decision traceability. The proposal is evaluated using technical metrics (PR-AUC, F1-Score, traceability coverage), operational comprehension assessment, and documented public/synthetic agro-export data.

The main contributions are: (1) a modular four-layer architecture separating prediction, detection, explanation, and reporting; (2) integration of official public sources and a documented synthetic agro-export dataset; (3) SHAP-based explanation of operational alerts; (4) evidence-restricted RAG reporting to reduce hallucination risk; and (5) comparative evaluation of the integrated system against isolated components in terms of detection performance, traceability, and interpretation time. Peruvian Resolution SBS N° 053-2023 is used only as a national reference for model risk management practices, while D.S. N° 115-2025-PCM is adopted as the general Peruvian AI governance framework.

**Keywords**: operational supervision, anomaly detection, agro-export, AI explainability, language models, governance, GBDT, automatic reports, traceability, artificial intelligence.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

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

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# INTRODUCCIÓN

La agroexportación peruana constituye un sector estratégico para la economía nacional debido a su crecimiento sostenido, diversificación de productos y participación en mercados internacionales exigentes. De acuerdo con información oficial del Ministerio de Desarrollo Agrario y Riego, al cierre de 2025 las agroexportaciones peruanas alcanzaron ventas por USD 15 013 millones, con un crecimiento de 17.3% respecto al año anterior (MIDAGRI, 2026). Entre los principales productos exportados destacaron arándanos, uvas, paltas, cacao y espárragos, lo que evidencia la importancia económica y operativa de las cadenas agroexportadoras peruanas.

En este contexto, las empresas agroexportadoras articulan procesos de producción agrícola, acopio, almacenamiento, control de calidad, cumplimiento fitosanitario, logística y comercialización internacional. Cada uno de estos procesos genera datos que pueden revelar desviaciones relevantes para la gestión operativa: cambios inusuales en precios, variaciones de volumen, condiciones climáticas adversas, incumplimientos de calidad, retrasos logísticos o patrones atípicos en el comportamiento exportador. No obstante, la supervisión de estos procesos suele depender de reportes manuales, hojas de cálculo, sistemas no integrados o análisis posteriores a la ocurrencia del problema.

La inteligencia artificial ofrece herramientas adecuadas para abordar esta brecha. Los modelos Gradient Boosting Decision Trees (GBDT) han demostrado buen desempeño en datos tabulares estructurados (Grinsztajn et al., 2022); los ensembles de detectores de anomalías permiten identificar comportamientos atípicos de manera más robusta que un detector individual (Han et al., 2022); la explicabilidad mediante valores de Shapley (SHAP) convierte predicciones opacas en justificaciones comprensibles (Lundberg & Lee, 2017); y los modelos de lenguaje con arquitectura RAG pueden transformar resultados cuantitativos en reportes comprensibles siempre que se restrinja su función a la generación narrativa basada en evidencias (Schneider et al., 2025).

La presente investigación propone un sistema integrado de cuatro capas que une predicción tabular, detección de anomalías, explicabilidad y generación de reportes trazables en un flujo coherente de supervisión operativa. El sistema se orienta al contexto agroexportador peruano y busca mejorar la capacidad de detectar desviaciones operativas, explicar sus posibles causas y documentar cada alerta de manera comprensible para supervisores, responsables de calidad, gestores logísticos y auditores internos. La Resolución SBS N° 053-2023 (SBS, 2023) se toma como referencia nacional de buenas prácticas para gestión de riesgo de modelos, sin asumirla como obligación directa para agroexportadoras; el D.S. N° 115-2025-PCM (PCM, 2025) se emplea como marco peruano general sobre gobernanza, transparencia y supervisión humana en inteligencia artificial.

El documento se estructura de la siguiente manera: el Capítulo I plantea el problema de investigación, define los objetivos, hipótesis, variables e indicadores, y evalúa la viabilidad del proyecto. El Capítulo II desarrolla el marco teórico, incluyendo antecedentes nacionales e internacionales, estado del arte organizado en cinco debates argumentativos, y el marco conceptual que fundamenta cada componente técnico de la propuesta. El Capítulo III describe la arquitectura del sistema propuesto, los datasets de validación y la configuración experimental. El Capítulo IV presenta los resultados obtenidos y la discusión de los hallazgos. Finalmente, el Capítulo V sintetiza las conclusiones, limitaciones de la investigación y propuestas de trabajos futuros.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

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

4. **Explicabilidad verificable**: Integrar SHAP (Lundberg & Lee, 2017) para identificar las variables que más contribuyen a cada alerta generada por el sistema.

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

**Disponibilidad de tecnologías**: El stack tecnológico es completamente open-source y maduro: XGBoost (Chen & Guestrin, 2016), LightGBM (Ke et al., 2017) y CatBoost (Prokhorenkova et al., 2018) para predicción tabular; PyOD (Zhao et al., 2019) para ensemble de anomalías con acceso a Isolation Forest (Liu et al., 2008), LOF (Breunig et al., 2000) y Deep SVDD (Ruff et al., 2018); SHAP (Lundberg & Lee, 2017) para explicabilidad; APIs de LLM (Anthropic Claude, OpenAI GPT-4) o modelos locales (Llama 3) para generación de reportes.

**Datos disponibles**: Se contemplan tres niveles de datos. El primer nivel corresponde a fuentes públicas oficiales: MIDAGRI para agroexportaciones, precios y boletines sectoriales; SENAMHI para variables climáticas; SENASA para requisitos fitosanitarios; SUNAT para exportaciones; INEI para indicadores económicos; FAOSTAT y UN Comtrade para validación internacional. El segundo nivel corresponde a un dataset sintético agroexportador documentado, construido con variables operativas plausibles y etiquetas de anomalía controladas. El tercer nivel, opcional, corresponde a datos privados de una empresa agroexportadora bajo acuerdo de confidencialidad. Como referencia metodológica complementaria puede utilizarse el BAF Benchmark (Jesus et al., 2022), no como evidencia directa del dominio agroexportador, sino como benchmark tabular desbalanceado con drift temporal.

**Riesgos técnicos identificados**: La latencia de SHAP en datasets grandes (>1M filas) puede mitigarse con los métodos de aproximación TreeSHAP. La variabilidad en salidas de LLMs requiere prompt engineering robusto y restricción mediante RAG. La mitigación incluye pruebas piloto en subconjuntos de datos y benchmarking iterativo.

### 1.6.2 Viabilidad Operativa

**Timeline**: Fase 1 (meses 1–2): preparación de datos, implementación de arquitectura base. Fase 2 (meses 2–3): entrenamiento de modelos, validación experimental. Fase 3 (mes 4): test de usabilidad con auditores voluntarios. Fase 4 (mes 5): análisis de resultados, escritura y defensa.

**Presupuesto estimado**: Infraestructura GPU cloud y APIs LLM: USD 500–1,000. Stack open-source: USD 0. Incentivos para participantes del test de usabilidad: USD 200–300. Total aproximado: USD 800–1,300.

### 1.6.3 Viabilidad Económica

La viabilidad económica se justifica por la relevancia del sector agroexportador peruano y por el costo operativo asociado a decisiones tardías ante desviaciones de precio, volumen, calidad, clima o logística. MIDAGRI reportó agroexportaciones por USD 15 013 millones al cierre de 2025 (MIDAGRI, 2026), por lo que incluso mejoras marginales en detección temprana, trazabilidad y tiempo de respuesta pueden representar beneficios operativos relevantes. En esta fase, los beneficios económicos se tratarán como escenarios exploratorios y no como resultados finales hasta contar con evaluación experimental y supuestos documentados.

## 1.7 Justificación e Importancia de la Investigación

### 1.7.1 Justificación Teórica

La revisión sistemática de la literatura revela avances importantes en modelos tabulares, detección de anomalías, explicabilidad y generación de reportes mediante LLMs. Sin embargo, estos componentes suelen estudiarse de forma aislada y en dominios distintos al agroexportador. Trabajos de auditoría financiera o fraude contable, como AuditCopilot (Kadir et al., 2025), se utilizan solo como antecedentes metodológicos sobre automatización de reportes y detección de anomalías, no como eje del dominio de aplicación. La brecha central de esta tesis es la ausencia de una arquitectura integrada y trazable para supervisión operativa agroexportadora peruana que combine fuentes públicas oficiales, datos sintéticos documentados, predicción tabular, detección de anomalías por ensemble, explicabilidad SHAP y reportes basados en evidencia bajo restricción anti-alucinación.

**Aporte original específico**: Esta tesis constituye, en el conocimiento del autor (verificado mediante búsqueda sistemática documentada en `docs/busqueda-sistematica-gap.md`), la primera arquitectura integrada de cuatro capas (GBDT + ensemble Isolation Forest/LOF/ECOD + TreeSHAP + LLM-RAG con restricción anti-alucinación) evaluada sobre datos agroexportadores peruanos públicos y sintéticos, con trazabilidad documental diseñada conforme al D.S. N° 115-2025-PCM y los principios del NIST AI RMF (NIST, 2023).

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

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

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

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 2.2 Estado del Arte

El estado del arte se organiza en torno a cinco debates fundamentales de la literatura que la presente propuesta debe resolver o posicionarse explícitamente. Cada sub-sección presenta el debate, los trabajos relevantes y la posición de esta tesis. La Tabla 2.1 sintetiza todas las referencias relevantes al final de la sección.

### 2.2.1 GBDT versus Deep Learning para Datos Tabulares Empresariales y Agroexportadores

El desarrollo de modelos para datos tabulares ha seguido una trayectoria diferente a la de visión computacional y procesamiento de lenguaje natural: el Deep Learning no ha conseguido desplazar a los modelos basados en árboles como estándar de facto en datos estructurados. Chen y Guestrin (2016) introdujeron XGBoost como sistema escalable de gradient boosting con regularización L1/L2, manejo nativo de valores faltantes y paralelización por columnas, estableciéndolo como el baseline universal con más de 45,000 citas en la literatura científica. Ke et al. (2017) lo extendieron con LightGBM, que incorpora Gradient-based One-Side Sampling (GOSS) e histogramas para lograr velocidades de entrenamiento hasta 20 veces superiores con rendimiento comparable. Prokhorenkova et al. (2018) resolvieron el problema de target leakage en variables categóricas con Ordered Boosting, siendo especialmente relevante en datos contables con alta cardinalidad (cuentas, departamentos, centros de costo).

El auge del Deep Learning motivó intentos de adaptar estas arquitecturas a datos tabulares. Gorishniy et al. (2021) propusieron FT-Transformer, el primer Transformer robusto para tablas mediante feature embeddings, que en algunos benchmarks iguala pero raramente supera a los GBDT. Arik y Pfister (2021) desarrollaron TabNet, que combina selección secuencial de features con atención interpretable, argumentando que puede ofrecer tanto rendimiento como interpretabilidad en un solo modelo. Sin embargo, el estudio seminal de Grinsztajn et al. (2022) zanjó empíricamente este debate: en datasets tabulares de hasta 50,000 muestras, los GBDT superan a los modelos de Deep Learning en la inmensa mayoría de los escenarios empíricos. Esta robusta evidencia respalda la decisión arquitectónica de la presente tesis, cuyo conjunto de datos transaccionales se sitúa en un volumen óptimo (hasta 10,000 registros sintéticos) para maximizar el rendimiento de los árboles de decisión. Los autores identifican tres propiedades estructurales de los datos tabulares que favorecen a los árboles: robustez ante features no informativas, orientación no invariante a rotaciones y presencia de irregularidades en la función objetivo —todas características presentes en los registros transaccionales de auditoría.

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

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 2.3 Marco Conceptual

### 2.3.1 Reconocimiento de Patrones y Aprendizaje Automático

El reconocimiento de patrones es la disciplina de la inteligencia artificial que busca identificar regularidades, estructuras o relaciones en datos a partir de ejemplos históricos. En el aprendizaje automático, este proceso se formaliza mediante modelos que aprenden una función $f: X \rightarrow Y$ a partir de un conjunto de entrenamiento $\{(x_i, y_i)\}_{i=1}^n$, con el objetivo de generalizar hacia instancias no observadas.

Se distinguen tres paradigmas principales: **aprendizaje supervisado**, donde el modelo aprende de etiquetas explícitas (e.g., operación normal / operación anómala); **aprendizaje no supervisado**, que identifica patrones sin etiquetas y es fundamental en la detección de anomalías; y **aprendizaje semi-supervisado**, que combina ambos cuando el etiquetado es costoso o escaso, escenario habitual en procesos agroexportadores donde no todas las desviaciones quedan registradas formalmente.

En el contexto de esta investigación, el reconocimiento de patrones opera en dos dimensiones complementarias: la detección de registros operativos anómalos (patrones puntuales) y la identificación de secuencias temporales de comportamiento irregular (patrones colectivos), requiriendo tanto modelos de clasificación supervisada como detectores de anomalías no supervisados.

### 2.3.2 Datos Tabulares en Sistemas Agroexportadores Empresariales

Los datos tabulares son la forma predominante de almacenamiento en los sistemas de información empresarial: cada fila representa una instancia operativa y cada columna una variable. En agroexportación, una instancia puede describir un lote, día, producto, zona, envío o registro de mercado; las columnas pueden incluir precio, volumen, temperatura, precipitación, humedad, destino, cumplimiento fitosanitario, días logísticos, merma y etiqueta de anomalía.

Estas propiedades estructurales explican por qué los GBDT son adecuados para este dominio (Grinsztajn et al., 2022): manejan variables numéricas y categóricas heterogéneas, toleran valores faltantes, capturan relaciones no lineales y requieren menor ingeniería de features que arquitecturas neuronales complejas. Cuando las etiquetas de anomalía son escasas o desbalanceadas, el rendimiento debe evaluarse con métricas orientadas a precisión-recall (PR-AUC), F1-Score y análisis de falsos positivos.

### 2.3.3 Gradient Boosting Decision Trees (GBDT)

Los Gradient Boosting Decision Trees (GBDT) son una familia de algoritmos de aprendizaje supervisado que construyen modelos predictivos mediante la combinación secuencial de múltiples árboles de decisión débiles. El enfoque fue formalizado por Friedman (2001) como "Greedy Function Approximation", donde cada árbol nuevo se ajusta para corregir los errores residuales del conjunto de árboles previos mediante descenso de gradiente en el espacio funcional de la función de pérdida.

La formulación matemática central de GBDT busca encontrar una función $F(x)$ que minimice la pérdida esperada:

$$F^*(x) = \arg\min_{F} \mathbb{E}_{y,x}[L(y, F(x))]$$

donde $L$ es la función de pérdida (e.g., entropía cruzada para clasificación, MSE para regresión) y la minimización se realiza iterativamente añadiendo árboles de regresión $h_m(x)$ con pesos de aprendizaje $\nu$:

$$F_m(x) = F_{m-1}(x) + \nu \cdot h_m(x)$$

**XGBoost** (Chen & Guestrin, 2016) introduce mejoras clave sobre el GBDT estándar: regularización L1 y L2 en la función objetivo para controlar la complejidad del modelo, manejo nativo de valores faltantes mediante aprendizaje automático de la dirección de ramificación, y paralelización por columnas en lugar de por filas, lo que habilita el procesamiento en datasets de alta dimensión.

**LightGBM** (Ke et al., 2017) acelera el entrenamiento mediante dos innovaciones: Gradient-based One-Side Sampling (GOSS), que retiene las muestras con mayor gradiente y descarta aleatoriamente las de menor gradiente, preservando la distribución sin pérdida estadística significativa; y Exclusive Feature Bundling (EFB), que agrupa features mutuamente excluyentes para reducir dimensionalidad efectiva. El resultado es una aceleración de hasta 20× sobre XGBoost con precisión comparable.

**CatBoost** (Prokhorenkova et al., 2018) resuelve el problema del target leakage en variables categóricas mediante Ordered Boosting: calcula las estadísticas de objetivo para cada categoría usando únicamente las observaciones previas en un orden aleatorio permutado, evitando que la información del objetivo filtre hacia las features de entrada durante el entrenamiento. Esta propiedad es especialmente relevante en datos contables, donde variables como "código de cuenta" o "centro de costo" tienen alta cardinalidad.

La justificación empírica para elegir GBDT sobre Deep Learning en datos tabulares empresariales está sólidamente documentada por (Grinsztajn et al., 2022): en 45 datasets con hasta 50,000 muestras, los GBDT superan a arquitecturas neuronales complejas (como FT-Transformer o TabNet) en la inmensa mayoría de los casos. Dado que el dataset operativo de esta tesis comprende un volumen controlado de hasta 10,000 registros transaccionales sintéticos (Anexo C), se sitúa exactamente en el rango donde los modelos basados en árboles maximizan su ventaja comparativa. Esta superioridad es atribuible a tres propiedades estructurales de los datos tabulares que los árboles aprovechan mejor que las redes neuronales.

### 2.3.4 Detección de Anomalías y Estrategia de Ensemble

La detección de anomalías es el problema de identificar observaciones que se desvían significativamente del comportamiento esperado del conjunto de datos. La literatura distingue tres tipos fundamentales de anomalías (Han et al., 2022): (a) **puntuales** — instancias individuales anómalas (e.g., una transacción de monto atípico); (b) **contextuales** — instancias que son anómalas en un contexto particular pero no en general (e.g., un cargo nocturno inusual para un perfil de usuario); y (c) **colectivas** — secuencias de instancias que son anómalas en conjunto aunque cada una individualmente no lo sea (e.g., un patrón de micro-transacciones).

**Isolation Forest** (Liu et al., 2008) se basa en el principio de que las anomalías son "pocas y diferentes": son más fáciles de aislar que los puntos normales mediante particionamiento aleatorio del espacio. Un árbol de aislamiento selecciona aleatoriamente una feature y un valor de corte; la anomalía será aislada en pocas particiones (camino corto), mientras que los puntos normales requieren muchas particiones (camino largo). El score de anomalía es el inverso de la longitud promedio del camino de aislamiento, normalizada según la longitud esperada para un punto normal en un conjunto de tamaño $n$. La complejidad es O(n log n) en entrenamiento y O(n) en inferencia.

**Local Outlier Factor (LOF)** (Breunig et al., 2000) cuantifica el grado de anomalía de cada punto en función de la densidad de su vecindario local respecto a la densidad de sus vecinos. El score LOF para el punto $p$ se define como:

$$\text{LOF}_k(p) = \frac{\sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}}{|N_k(p)|}$$

donde $\text{lrd}_k$ es la densidad de alcanzabilidad local. Un valor LOF >> 1 indica que $p$ tiene densidad local mucho menor que sus vecinos, lo que lo caracteriza como anomalía. LOF es sensible a variaciones locales de densidad, lo que lo hace complementario a Isolation Forest en datasets heterogéneos.

**Deep SVDD** (Ruff et al., 2018) extiende el Support Vector Data Description al espacio de representación de redes neuronales: entrena una red para mapear los datos normales hacia el interior de una hipersfera mínima en el espacio latente. Las anomalías se detectan como puntos que caen fuera o lejos de esta hipersfera. La función objetivo minimiza el volumen de la hipersfera:

$$\min_{W, R, c} R^2 + \frac{1}{\nu n} \sum_{i=1}^{n} \max(0, \|f(x_i; W) - c\|^2 - R^2)$$

donde $f(x_i; W)$ es la representación de la red neuronal, $c$ es el centro de la hipersfera y $R$ es su radio.

**ECOD** (Li et al., 2022) calcula el score de anomalía como la probabilidad acumulada de observar un punto tan extremo como $x$ bajo la distribución empírica del dataset, estimada mediante funciones de distribución acumulada (ECDF) multivariadas. Su ventaja principal es que no tiene hiperparámetros que calibrar, eliminando el riesgo de sobreajuste y simplificando el despliegue en producción.

La estrategia de **ensemble** consolida las puntuaciones de múltiples detectores mediante aggregation functions (promedio de scores, votación por mayoría o meta-clasificación). El fundamento teórico lo proporciona ADBench (Han et al., 2022): no existe un algoritmo universal, y el ensemble reduce la varianza del estimador de anomalía agregando perspectivas complementarias. PyOD (Zhao et al., 2019) implementa esta estrategia con la clase `LSCP` (Locally Selective Combination in Parallel Outlier Ensembles) y otras técnicas de combinación estándar.

### 2.3.5 Forecasting de Series Temporales con Transformers

Las series temporales agroexportadoras presentan tres desafíos que los modelos de forecasting deben resolver: tendencia no estacionaria, estacionalidad múltiple (diaria, semanal, mensual, anual) y dependencia de covariables exógenas (clima, calendario agrícola, demanda internacional, precios y condiciones logísticas). Los modelos estadísticos clásicos como ARIMA capturan relaciones lineales con eficacia, pero presentan limitaciones en la modelización de no-linealidades y horizontes largos.

**Temporal Fusion Transformer (TFT)** (Lim et al., 2021) propone una arquitectura especializada que combina cuatro mecanismos: (1) codificación LSTM para dependencias secuenciales locales; (2) selección de variables con mecanismo de gating (GLU — Gated Linear Unit) que identifica automáticamente las covariables más informativas; (3) atención multi-cabezal interpretable que pondera los pasos temporales según su relevancia predictiva; y (4) red de cuantiles para cuantificar la incertidumbre de la predicción. TFT acepta tres tipos de entradas: features estáticas conocidas (e.g., producto, zona, destino), covariables futuras conocidas (e.g., calendario agrícola, campañas, feriados) y covariables históricas observadas (e.g., precio, volumen, clima o merma pasada).

El debate sobre la efectividad de los Transformers en series temporales es relevante para esta tesis. Zeng et al. (2023) argumentan que DLinear —un modelo lineal simple— supera a los Transformers en múltiples benchmarks, atribuyendo la limitación de los Transformers al hecho de que el mecanismo de self-attention es permutation-invariant y destruye el orden temporal de las secuencias. Sin embargo, este argumento ha sido rebatido sucesivamente: Nie et al. (2023) demuestran que la tokenización por patches —agrupando segmentos temporales antes de aplicar atención— preserva el orden local y supera a DLinear en la mayoría de benchmarks de horizonte largo. Liu et al. (2024) proponen invertir la tokenización: en lugar de tokenizar por timestamp, tokenizan por variable, aplicando self-attention entre variables en lugar de entre tiempos, obteniendo SOTA en 7 datasets multivariados.

**Posición de esta tesis respecto al debate**: TFT se considera por su interpretabilidad incorporada —el mecanismo de gating y los mapas de atención son legibles por analistas— más que exclusivamente por su rendimiento predictivo. En el contexto agroexportador, la capacidad de justificar qué períodos temporales y qué covariables fundamentan la predicción es un requerimiento funcional comparable en importancia a la precisión numérica.

N-HiTS (Challu et al., 2022) ofrece una alternativa no-Transformer para forecasting de horizonte largo, con interpolación jerárquica multi-tasa que reduce la complejidad computacional respecto a N-BEATS. Chronos (Ansari et al., 2024) representa el paradigma emergente de los foundation models para series temporales, basado en T5, que logra performance zero-shot competitivo en múltiples datasets; sin embargo, su opacidad y dependencia de infraestructura de gran escala limitan su aplicación directa cuando se requiere trazabilidad operativa.

### 2.3.6 Explicabilidad mediante Valores de Shapley (SHAP)

La explicabilidad en sistemas de IA se clasifica en dos grandes categorías: **inherente** —modelos cuya estructura es intrínsecamente interpretable, como los árboles de decisión— y **post-hoc** —métodos aplicados a cualquier modelo después del entrenamiento para interpretar sus predicciones. SHAP y LIME son los dos métodos post-hoc agnósticos más adoptados en la literatura.

**LIME** (Local Interpretable Model-agnostic Explanations) (Ribeiro et al., 2016) genera explicaciones locales construyendo un modelo lineal sustituto en el vecindario de la instancia a explicar, ponderando las muestras según su proximidad al punto de interés. LIME es rápido y flexible, pero produce explicaciones inestables: pequeñas perturbaciones de la instancia pueden cambiar significativamente la explicación, un problema crítico en contextos forenses.

**SHAP** (Lundberg & Lee, 2017) fundamenta las explicaciones en los valores de Shapley de la teoría de juegos cooperativos. El valor SHAP de la feature $i$ para la predicción $f(x)$ cuantifica la contribución marginal media de $i$ a la predicción, promediando sobre todas las coaliciones posibles de features:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!} [f(S \cup \{i\}) - f(S)]$$

donde $F$ es el conjunto de todas las features y $S$ es una coalición de features sin $i$. Esta formulación garantiza cuatro propiedades axiomáticas: (a) **eficiencia** — la suma de todos los valores SHAP iguala la diferencia entre la predicción y el valor esperado; (b) **simetría** — features con contribución idéntica reciben el mismo valor; (c) **dummy** — features sin efecto tienen valor cero; y (d) **aditividad** — los valores SHAP son consistentes al combinar modelos.

SHAP resuelve las limitaciones de LIME al garantizar consistencia: si un modelo cambia la predicción al aumentar la contribución de una feature, el valor SHAP de esa feature nunca disminuye (Lundberg & Lee, 2017). **TreeSHAP** extiende este cálculo con un algoritmo exacto en O(TLD²) para modelos basados en árboles —donde T es el número de árboles, L es el número de hojas por árbol y D es la profundidad máxima— haciendo el cálculo computacionalmente viable para GBDT en producción.

En el contexto de supervisión operativa, la estabilidad de las explicaciones permite verificar que el modelo asigna importancias consistentes a variables semejantes. Un índice alto de estabilidad fortalece la confianza en el sistema, porque evita que alertas similares reciban justificaciones contradictorias.

La integración SHAP+LLM de esta tesis opera como sigue: los vectores SHAP de una alerta operativa (una lista de pares variable→contribución cuantitativa) se incorporan como contexto verificado en el RAG, y el LLM genera la narración del informe sin posibilidad de inventar cifras que no estén en esos vectores o en las fuentes recuperadas.

### 2.3.7 Modelos de Lenguaje y Arquitectura RAG para Generación de Reportes

Los Modelos de Lenguaje de Gran Tamaño (LLMs) son sistemas entrenados mediante autoregresión en corpus masivos de texto para aprender distribuciones probabilísticas sobre secuencias de tokens. Su capacidad de generalización les permite realizar tareas de reasoning, traducción, resumen y generación de texto con calidad próxima a la humana en configuraciones zero-shot y few-shot.

**In-context learning** permite guiar el comportamiento del LLM mediante ejemplos incluidos directamente en el prompt, sin necesidad de ajuste fino (fine-tuning). TabLLM (Hegselmann et al., 2023) demostró que mediante serialización de datos tabulares a texto descriptivo, los LLMs pueden realizar clasificación sobre datos estructurados con rendimiento no trivial en zero-shot, ampliando el espectro de aplicación de estos modelos más allá del texto no estructurado.

Sin embargo, el uso de LLMs como agentes de decisión autónoma introduce el riesgo de **alucinaciones**: el modelo puede generar afirmaciones coherentes en forma pero incorrectas en contenido (Ji et al., 2023; Maynez et al., 2026). La literatura distingue al menos dos tipos: (a) alucinaciones intrínsecas, en las que el texto generado contradice la información del contexto recuperado; y (b) alucinaciones extrínsecas, en las que el modelo inventa información no presente en el contexto. En particular, las "alucinaciones numéricas" —valores específicos de métricas, porcentajes o fechas que no corresponden a los datos reales (Barclays Research, 2025)— son especialmente peligrosas en reportes operativos, porque pueden inducir decisiones equivocadas pese a la apariencia de precisión cuantitativa.

**Retrieval-Augmented Generation (RAG)** (Lewis et al., 2020; Schneider et al., 2025) reduce este riesgo al separar el conocimiento factual del modelo generativo: en lugar de que el LLM "recuerde" información de su entrenamiento, el sistema recupera documentos o datos relevantes de una base de conocimiento externa verificada y los incluye en el contexto del prompt. El LLM entonces genera texto fundamentado en esos datos recuperados, no en su memoria paramétrica. Es importante señalar que RAG **reduce significativamente pero no elimina** el riesgo de alucinación; persisten casos de alucinación intrínseca (faithful hallucination) en los que el modelo genera afirmaciones que se desvían del contexto recuperado. Técnicas avanzadas como GraphRAG incorporan grafos de conocimiento para recuperación semántica más rica, mientras que Self-RAG permite al modelo verificar la pertinencia de los documentos recuperados antes de usarlos.

En la arquitectura de esta tesis, la "base de conocimiento" del RAG son los vectores SHAP de la alerta analizada, las métricas del ensemble de detección, las fuentes agroexportadoras recuperadas y las reglas de reporte definidas. El LLM recibe ese contexto verificado y genera el informe narrativo sin acceso a conocimiento adicional no validado. Adicionalmente se aplican dos controles complementarios: (a) plantillas de prompt estructurado con campos obligatorios (dato, modelo, score, umbral, explicación SHAP, fuente recuperada), y (b) validación posterior del reporte contra los vectores SHAP de entrada para detectar discrepancias numéricas. Este diseño permite que cada afirmación del reporte pueda trazarse hasta una fuente, score, umbral o variable explicativa.

La evaluación de calidad de los reportes generados puede utilizar **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) cuando exista un texto de referencia. Sin embargo, para esta tesis se prioriza una rúbrica operativa de completitud, consistencia, accionabilidad y correspondencia con evidencias, porque la calidad de un reporte de supervisión depende no solo de similitud textual, sino de su utilidad para la toma de decisiones.

### 2.3.8 Gobernanza de IA y MLOps

El despliegue de sistemas de IA en entornos empresariales críticos requiere un marco de gobernanza que trascienda el rendimiento técnico. Sculley et al. (2015) documentaron la "deuda técnica oculta" en sistemas de ML: más del 95% del código de un sistema ML de producción no es el modelo en sí, sino la infraestructura de ingesta, validación, features, servicio y monitoreo. Los pipelines con alto acoplamiento entre componentes generan "entanglement" que dificulta el mantenimiento y aumenta el riesgo de regresiones silenciosas.

**MLOps** (Kreuzberger et al., 2022) establece el conjunto de prácticas para gestionar el ciclo de vida completo de los modelos ML en producción: integración y entrega continua (CI/CD) para modelos, monitoreo de data drift y model drift, automatización del reentrenamiento, y trazabilidad de versiones de datos, código y modelos. En el contexto de supervisión operativa agroexportadora, MLOps permite reproducir qué modelo generó una alerta, con qué datos de entrada, bajo qué versión y con qué umbral.

El **NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0)** (NIST, 2023) proporciona cuatro funciones de gestión de riesgo para sistemas de IA: (1) **Govern** — establecer políticas y roles de responsabilidad; (2) **Map** — identificar el contexto de despliegue y los riesgos asociados; (3) **Measure** — evaluar los riesgos con métricas verificables; y (4) **Manage** — implementar controles y mitigaciones. La arquitectura modular de esta tesis es diseñada para que cada capa corresponda a responsabilidades verificables bajo este framework.

**Datasheets for Datasets** (Gebru et al., 2021) propone una plantilla de documentación estandarizada para datasets que detalla: motivación de recolección, proceso de recolección, composición, preprocesamiento aplicado, distribución permitida y consideraciones éticas. Esta práctica se aplicará al dataset sintético agroexportador y a las fuentes públicas utilizadas, garantizando que los resultados reportados en esta tesis sean reproducibles y que las limitaciones de cada fuente estén identificadas antes de evaluar el sistema.

**Model Cards** (Mitchell et al., 2019) extiende la documentación al nivel del modelo, especificando para quién fue entrenado, en qué condiciones, cuáles son sus limitaciones conocidas y cómo debe usarse de manera responsable. En esta tesis, se elaboran Model Cards para los modelos XGBoost/LightGBM, detectores de anomalías y el componente LLM+RAG, en conformidad con los principios de documentación del NIST AI RMF (NIST, 2023).

El contexto peruano e internacional consolida la necesidad de este framework de gobernanza. El D.S. N° 115-2025-PCM (PCM, 2025), el NIST AI RMF (NIST, 2023) y el EU AI Act (Parlamento Europeo y Consejo, 2024) refuerzan principios comunes: transparencia, documentación, supervisión humana y gestión de riesgos. Estos principios son adoptados como referencia de diseño para esta tesis. No se afirma cumplimiento formal con ninguno de estos marcos —tal afirmación requeriría auditoría regulatoria externa— sino conformidad de diseño con sus principios, en particular: (a) transparencia mediante SHAP y Model Cards, (b) supervisión humana mediante revisión obligatoria de cada reporte antes de su uso operativo, (c) gestión de riesgos mediante umbrales calibrados y validación cruzada, y (d) trazabilidad documental mediante logs completos por alerta. La aplicabilidad regulatoria efectiva del sistema a una empresa específica depende de su clasificación de riesgo bajo el reglamento correspondiente y queda fuera del alcance de esta tesis.

### 2.3.9 Supervisión Operativa, Trazabilidad e Inteligencia Artificial

La supervisión operativa en agroexportación exige monitorear procesos que combinan producción, acopio, calidad, sanidad, logística y comercio exterior. Las anomalías en este dominio no necesariamente corresponden a fraude; pueden representar variaciones atípicas de precio, caídas de volumen, condiciones climáticas adversas, mermas elevadas, incumplimientos fitosanitarios o retrasos logísticos. Por ello, el sistema propuesto se orienta a detectar desviaciones relevantes para la toma de decisiones, no a sustituir procesos de investigación legal o auditoría financiera.

La **supervisión operativa continua** busca reemplazar ciclos de revisión tardíos por monitoreo frecuente y documentado de indicadores. En este enfoque, cada alerta debe registrar el dato de origen, el modelo aplicado, el score calculado, el umbral utilizado, las variables explicativas y el reporte generado. Esta trazabilidad permite que un supervisor operativo comprenda por qué el sistema marcó un evento como anómalo y qué evidencia respalda la recomendación.

La integración de IA en supervisión operativa plantea el problema de la confianza en decisiones automáticas. Esta exigencia convierte a la explicabilidad (SHAP), la documentación de datasets (Datasheets), la documentación de modelos (Model Cards) y los logs de decisión en componentes funcionales del sistema. En el marco peruano, el D.S. N° 115-2025-PCM (PCM, 2025) proporciona una base general para el uso responsable de IA; la Resolución SBS N° 053-2023 (SBS, 2023) se conserva solo como referencia nacional de buenas prácticas para gestión de riesgo de modelos.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CAPÍTULO III: PROPUESTA METODOLÓGICA

## 3.1 Arquitectura del Sistema Integrado

La arquitectura propuesta se divide en cuatro módulos secuenciales, diseñados para maximizar trazabilidad, interpretabilidad y utilidad operativa en procesos agroexportadores:

- **Módulo de Predicción Tabular (Capa 1):** Utiliza algoritmos GBDT como núcleo predictivo, priorizando XGBoost (Chen & Guestrin, 2016) y LightGBM (Ke et al., 2017) por su robustez ante datos tabulares con variables heterogéneas (Grinsztajn et al., 2022). El módulo puede estimar valores esperados de precio, volumen, merma o riesgo operativo.
- **Módulo de Detección de Anomalías (Capa 2):** Emplea detectores como Isolation Forest (Liu et al., 2008), LOF (Breunig et al., 2000) y ECOD (Li et al., 2022), orquestados mediante PyOD (Zhao et al., 2019), para identificar comportamientos atípicos en variables agroexportadoras. Se selecciona ECOD sobre Deep SVDD (Ruff et al., 2018) —considerado en la revisión bibliográfica del Capítulo II— por tres razones: (a) ECOD no requiere ajuste de hiperparámetros, lo cual elimina el riesgo de sobreajuste en la calibración; (b) su fundamento basado en funciones de distribución empírica acumulada es interpretable estadísticamente para auditores, mientras que Deep SVDD opera sobre representaciones latentes opacas; y (c) su complejidad computacional es lineal, apropiada para el tamaño medio del dataset experimental (2,000–5,000 registros). Deep SVDD se mantiene como referencia conceptual del Capítulo II por su valor histórico, pero no entra al ensemble final.
- **Módulo de Explicabilidad (Capa 3):** SHAP (Lundberg & Lee, 2017) genera explicaciones locales por alerta, identificando qué variables —precio, volumen, clima, destino, cumplimiento o merma— contribuyen al score del sistema.
- **Módulo de Reportes LLM+RAG (Capa 4):** Un LLM restringido a evidencias estructuradas mediante RAG (Schneider et al., 2025) redacta reportes operativos trazables. El LLM no decide si existe una anomalía; solo traduce scores, umbrales y explicaciones SHAP a lenguaje comprensible.

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
2. **Dataset sintético agroexportador documentado**: conjunto de registros simulados con variables como fecha, producto, zona, volumen, precio, temperatura, precipitación, humedad, destino, cumplimiento fitosanitario, días logísticos, merma, etiqueta de anomalía y tipo de anomalía. Este dataset se documentará con criterios de Datasheets for Datasets (Gebru et al., 2021).
3. **Benchmark metodológico complementario**: BAF Benchmark (Jesus et al., 2022) podrá utilizarse solo para contrastar comportamiento de modelos en datos tabulares desbalanceados con drift temporal, sin presentarlo como validación directa del dominio agroexportador.

## 3.3 Configuración Experimental y Métricas

### 3.3.1 Métricas por variable dependiente

- **Métricas de predicción y detección (VD1)**: PR-AUC (métrica principal para datasets desbalanceados), ROC-AUC, F1-Score, Precision y Recall con umbral óptimo determinado por el punto de máxima F1 sobre el conjunto de validación.
- **Métricas de explicabilidad (VD2)**: cobertura top-k SHAP (porcentaje de alertas en las que las k=5 variables principales explican ≥80% de la magnitud absoluta del score), consistencia cualitativa de variables explicativas y claridad operativa (Likert 1–5 evaluada por revisores con perfil agroexportador).
- **Métricas de calidad de reportes (VD3)**: rúbrica operativa de cinco dimensiones (completitud, consistencia numérica, accionabilidad, coherencia textual, correspondencia con evidencias) evaluada por dos revisores independientes con cálculo de Kappa de Cohen para confiabilidad inter-evaluador. Adicionalmente ROUGE-1/ROUGE-L cuando exista referencia humana.
- **Métricas de comprensión y decisión (VD4)**: tiempo-a-decisión (segundos, medido automáticamente desde la apertura de la alerta hasta el envío del veredicto del evaluador), comprensión de alerta (Likert 1–5) y decisión final correcta (sí/no respecto a la etiqueta del dataset).
- **Métricas de trazabilidad (VD5)**: porcentaje de alertas con todos los campos completos (dato de origen, versión de dataset, modelo, score, umbral, explicación SHAP, fuente recuperada por RAG y reporte generado).

### 3.3.2 División del dataset y semilla

Para evitar fuga de información temporal en variables agroexportadoras con estacionalidad, se aplica una **división cronológica** y no aleatoria:
- **Train**: primeros 70% de registros ordenados por fecha.
- **Validation**: 10% siguiente, para selección de hiperparámetros.
- **Test**: 20% final, evaluado solo al cierre del entrenamiento.

Todas las ejecuciones experimentales fijan `np.random.seed(42)` y `random.seed(42)`. Cada experimento se repite con cinco semillas adicionales (43, 44, 45, 46, 47) para reportar media ± desviación estándar de cada métrica.

### 3.3.3 Diseño experimental: condiciones y experimentos E1–E5

La evaluación se organiza en cinco experimentos cuya condición experimental aísla un componente arquitectónico distinto:

| Exp. | Nombre | Condición experimental | Condición de control | Variable observada | Hipótesis |
|---|---|---|---|---|---|
| E1 | Rendimiento de detección | Ensemble IF + LOF + ECOD | Isolation Forest individual | VD1: PR-AUC, F1 | H1a |
| E2 | Aporte de SHAP | Sistema con vectores SHAP | Sistema sin SHAP (solo scores) | VD2: cobertura top-k, Likert | H1b |
| E3 | Aporte de RAG | LLM + RAG (anclado en SHAP) | LLM libre (sin RAG) | VD3: rúbrica 5D, ROUGE-L | H1c |
| E4 | Sistema integrado vs. aislado | Pipeline completo de 4 capas | Salidas técnicas aisladas por módulo | VD4: tiempo, Likert; VD5: trazabilidad | H1, H1d |
| E5 | Ablation study | Configuraciones parciales (E5a, E5b, E5c, E5d) | — | VD1 + VD5 por configuración | Contribución por capa |

Variantes del ablation study (E5):
- **E5a**: Solo Capa 2 (sin predicción, sin SHAP, sin RAG) — baseline mínimo.
- **E5b**: Capas 1 + 2 + 4 (sin SHAP) — evalúa el aporte de SHAP al pipeline.
- **E5c**: Capas 1 + 2 + 3 + LLM libre (sin RAG) — evalúa el aporte del anclaje RAG.
- **E5d**: Pipeline completo de 4 capas — referencia experimental.

### 3.3.4 Pruebas estadísticas y mapa hipótesis → experimento

Cada sub-hipótesis se contrasta con una prueba estadística específica, seleccionada según el tipo de variable y el diseño:

| Sub-hipótesis | Comparación | Variable | Prueba estadística | α | Tamaño de efecto |
|---|---|---|---|---|---|
| H1a | Ensemble vs. detector único | PR-AUC sobre 6 semillas | Wilcoxon signed-rank (no paramétrica, apareada) | 0.05 | Hedges' g |
| H1b | SHAP vs. sin SHAP | Likert comprensión (1–5) | Mann-Whitney U (escala ordinal, muestras independientes) | 0.05 | r de rangos |
| H1c | RAG vs. sin RAG | Rúbrica de reportes (1–5) | t de Student apareado o Wilcoxon según Shapiro-Wilk | 0.05 | Cohen's d |
| H1d | Sistema integrado vs. aislado | Tiempo-a-decisión (s) | t de Student apareado (within-subjects) | 0.05 | Cohen's dz |

Para todas las pruebas se verifica previamente el supuesto de normalidad con Shapiro-Wilk; ante violación, se aplica la prueba no paramétrica equivalente. Se reporta intervalo de confianza al 95% para cada métrica y se calcula el tamaño de efecto como medida complementaria a la significancia estadística.

### 3.3.5 Estudio de usabilidad: tamaño y selección de muestra

El estudio de usabilidad para VD4 adopta un **diseño within-subjects con N ≥ 15 participantes**, contrabalanceado en orden de presentación (mitad evalúa primero el sistema integrado, mitad evalúa primero el aislado). Con este tamaño se reportan resultados como exploratorios, con cálculo de tamaño de efecto Cohen's dz y intervalo de confianza al 95%, sin afirmar significancia estadística con potencia plena. Para detectar un efecto medio (dz = 0.5) con potencia 0.80 y α = 0.05 se requieren N = 27 participantes; este tamaño se considera meta deseable y, en caso de no alcanzarse, se reporta el limitante en §5.2 (Limitaciones).

**Criterios de inclusión de participantes**:
- Estudiantes avanzados de Ingeniería de Sistemas, Industrial o Agronomía (≥ séptimo semestre), o
- Profesionales con ≥ 1 año de experiencia en supervisión operativa, control de calidad o auditoría interna.

**Criterios de exclusión**:
- Participación previa en el diseño del sistema o de cualquiera de sus capas.
- Conflicto de interés directo con empresas agroexportadoras evaluadas.

El protocolo detallado, formulario de consentimiento informado y cuestionario post-tarea figuran en el Anexo A.

### 3.3.6 Tuning de hiperparámetros y reproducibilidad

La selección de hiperparámetros se realiza con **Optuna** (TPE sampler, 50 trials por modelo), optimizando PR-AUC sobre el validation set. Los rangos de búsqueda se documentan en el Anexo B (Model Cards). El código fuente, requirements.txt con versiones exactas, semillas y notebooks de reproducción se publican en repositorio GitHub público con licencia MIT al cierre del Hito 3.

### 3.3.7 Comparación con baselines

Para cada experimento, los resultados del sistema propuesto se comparan con baselines documentados:

| # | Baseline | Justificación |
|---|---|---|
| B1 | Isolation Forest individual | Detector más simple y ampliamente adoptado |
| B2 | Ensemble IF + LOF (sin ECOD) | Aislar el aporte de ECOD al ensemble |
| B3 | XGBoost supervisado con etiqueta de anomalía | Upper bound supervisado |
| B4 | LLM sin RAG y sin SHAP | Línea base de reporte automático |

Los baselines se ejecutan sobre el mismo dataset, misma división y mismas semillas para garantizar comparación justa.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CAPÍTULO IV: RESULTADOS Y DISCUSIÓN

> **Estado:** Estructura completa lista — las tablas y gráficos numéricos se completarán tras ejecutar los experimentos E1–E5 (Hito 4 — 2026-06-22).

## 4.1 Resultados Cuantitativos (Predicción y Detección — VD1)

Esta sección presenta las métricas obtenidas por el módulo de predicción tabular y el ensemble de detección de anomalías sobre el conjunto de test del dataset sintético agroexportador (v1.0, 400 registros del período 2025-05-01 a 2025-12-31).

### 4.1.1 Tabla 4.1 — Rendimiento de detección (Experimento E1)

| Método | PR-AUC | ROC-AUC | F1 | Precision | Recall | Tiempo inferencia |
|---|---|---|---|---|---|---|
| Isolation Forest individual (baseline B1) | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| LOF individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| ECOD individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| Ensemble IF + LOF (B2) | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| **Ensemble IF + LOF + ECOD (propuesto)** | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| XGBoost supervisado (B3 — upper bound) | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |

> Valores reportados como media ± desviación estándar sobre 6 semillas (42–47).

### 4.1.2 Tabla 4.2 — Recall por tipo de anomalía

| Tipo de anomalía | Recall ensemble | Recall IF solo | Δ (puntos porcentuales) |
|---|---|---|---|
| precio | _pendiente_ | _pendiente_ | _pendiente_ |
| volumen | _pendiente_ | _pendiente_ | _pendiente_ |
| clima | _pendiente_ | _pendiente_ | _pendiente_ |
| logistica | _pendiente_ | _pendiente_ | _pendiente_ |
| calidad | _pendiente_ | _pendiente_ | _pendiente_ |

## 4.2 Resultados Cualitativos (Explicabilidad y Reportes — VD2 y VD3)

### 4.2.1 Tabla 4.3 — Calidad de explicabilidad (Experimento E2)

| Métrica | Sistema con SHAP | Sistema sin SHAP | p-value (Mann-Whitney U) |
|---|---|---|---|
| Cobertura top-3 (mediana) | _pendiente_ | N/A | — |
| Cobertura top-5 (mediana) | _pendiente_ | N/A | — |
| Consistencia ρ (Spearman) | _pendiente_ | N/A | — |
| Claridad operativa (Likert 1–5, promedio) | _pendiente_ | _pendiente_ | _pendiente_ |

### 4.2.2 Tabla 4.4 — Calidad de reportes generados (Experimento E3)

| Dimensión | LLM + RAG (propuesto) | LLM libre (control) | Kappa Cohen | p-value |
|---|---|---|---|---|
| Completitud | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| Consistencia numérica | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| Accionabilidad | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| Coherencia textual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| Correspondencia con evidencias | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| **Promedio total** | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| ROUGE-L (subset con referencia) | _pendiente_ | _pendiente_ | — | _pendiente_ |

### 4.2.3 Ejemplo de reporte generado (alerta tipo "calidad")

> Espacio reservado para insertar un reporte real de muestra que ilustre el patrón anclado: dato → modelo → score → umbral → SHAP top-5 → fuente RAG → recomendación operativa.

## 4.3 Resultados del Estudio de Usabilidad (VD4 y VD5)

### 4.3.1 Tabla 4.5 — Tiempo-a-decisión y comprensión (Experimento E4)

| Métrica | Sistema integrado | Componentes aislados | Δ relativo | p-value | Cohen's dz |
|---|---|---|---|---|---|
| Tiempo-a-decisión (s, mediana) | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| Comprensión (Likert 1–5, media) | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| Decisión correcta (%) | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | — |
| SUS Score (0–100) | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |

> N participantes = _pendiente_ — diseño within-subject contrabalanceado.

### 4.3.2 Tabla 4.6 — Trazabilidad documental (VD5)

| Configuración | % alertas completas | Campos faltantes más frecuentes |
|---|---|---|
| Sistema integrado (E5d) | _pendiente_ (meta ≥95%) | _pendiente_ |
| Ablation sin SHAP (E5b) | _pendiente_ | _pendiente_ |
| Ablation sin RAG (E5c) | _pendiente_ | _pendiente_ |
| Componentes aislados (control) | _pendiente_ (esperado < 30%) | _pendiente_ |

### 4.3.3 Tabla 4.7 — Ablation study (Experimento E5)

| Configuración | Capa 1 | Capa 2 | Capa 3 | Capa 4 | PR-AUC | Trazabilidad % | Likert claridad |
|---|---|---|---|---|---|---|---|
| E5a — solo detección | ✗ | ✓ | ✗ | ✗ | _pendiente_ | _pendiente_ | _pendiente_ |
| E5b — sin SHAP | ✓ | ✓ | ✗ | ✓ | _pendiente_ | _pendiente_ | _pendiente_ |
| E5c — sin RAG | ✓ | ✓ | ✓ | LLM libre | _pendiente_ | _pendiente_ | _pendiente_ |
| **E5d — pipeline completo** | ✓ | ✓ | ✓ | ✓ | _pendiente_ | _pendiente_ | _pendiente_ |

---

## 4.4 Discusión Detallada y Cruce de Datos Comparativo

### 4.4.1 Propósito de la discusión

Esta sección triangula los resultados experimentales propios con tres bloques externos: (a) la literatura comparable revisada en el Capítulo II §2.2, (b) las hipótesis declaradas en el Capítulo I §1.4, y (c) las variables operacionalizadas formalmente en `variables-operacionalizadas.md`. El objetivo es demostrar que cada hallazgo cuantitativo se explica conceptualmente, se contrasta con el estado del arte y se interpreta en el contexto regulatorio peruano.

### 4.4.2 Cruce 1 — Resultados propios versus literatura comparable (Tabla 4.8)

La Tabla 4.8 sitúa el rendimiento del sistema propuesto frente a los cinco trabajos más cercanos identificados en la búsqueda sistemática (`busqueda-sistematica-gap.md`). La comparación se realiza considerando que cada trabajo opera en un dominio y dataset distintos, por lo que los valores absolutos no son directamente comparables; lo que se compara es la cobertura modular y la consistencia direccional de los resultados.

| Atributo | Esta tesis | AuditCopilot (Kadir et al., 2025) | Park (2024) | JRFM (2025) | Almalki & Masud (2025) | AuditMAI (Waltersdorfer et al., 2024) |
|---|---|---|---|---|---|---|
| Predicción tabular GBDT | XGBoost + LightGBM | No reportada | No (solo LLMs) | Stacking GBDT | Stacking GBDT | No |
| Ensemble de detección | IF + LOF + ECOD | Parcial | No | No | No | No |
| Explicabilidad SHAP estructurada | TreeSHAP top-k | No | No | SHAP | SHAP | No |
| Generación LLM bajo RAG | RAG anclado en SHAP | LLM libre | Multi-agente | No | No | No |
| Restricción anti-alucinación | Sí (validación numérica posterior) | No documentada | No | N/A | N/A | N/A |
| PR-AUC reportado | _pendiente_ | No reporta | No reporta | 0.93 | _pendiente_ verificar | No |
| Dominio | Agroexportador peruano | Asientos contables | S&P 500 | Fraude financiero | Fraude financiero | Auditoría de IA |
| Contexto regulatorio | D.S. 115-2025-PCM + NIST AI RMF | No especificado | No | No | No | No |
| Evaluación con usuarios | Sí (N ≥ 15) | No | No | No | No | No |
| Dataset abierto disponible | Sí (CC BY 4.0) | No | No | No | Parcial | N/A |

**Lectura del cruce 1**:
- La cobertura modular del sistema propuesto (cuatro capas con restricción anti-alucinación) es estrictamente mayor que cualquier trabajo individual de la literatura revisada.
- El trabajo más cercano en cobertura es JRFM (2025) que combina GBDT y SHAP en fraude financiero, pero carece de detección no supervisada, módulo LLM y contexto regulatorio.
- AuditCopilot (Kadir et al., 2025) es el único que combina detección con generación LLM, pero opera en asientos contables sin SHAP estructurado ni restricción anti-alucinación.

### 4.4.3 Cruce 2 — Contraste de hipótesis (Tabla 4.9)

| Sub-hipótesis | Predicción del Capítulo I | Evidencia empírica obtenida | Decisión |
|---|---|---|---|
| H1a — Ensemble supera al detector individual | PR-AUC ensemble > PR-AUC IF con tamaño de efecto Hedges' g ≥ 0.5 | _pendiente E1_ | _Aceptar / Rechazar / Inconcluso_ |
| H1b — SHAP mejora la comprensión | Likert claridad ≥ 4.0 con SHAP; < 4.0 sin SHAP | _pendiente E2_ | _pendiente_ |
| H1c — RAG mejora la calidad del reporte | Rúbrica promedio ≥ 4.0 y Kappa Cohen ≥ 0.60 | _pendiente E3_ | _pendiente_ |
| H1d — Sistema integrado reduce tiempo-a-decisión | Reducción ≥ 20% del tiempo, p < 0.05 | _pendiente E4_ | _pendiente_ |
| H1 (general) — Sistema integrado mejora trazabilidad | ≥ 95% alertas completas en integrado vs. < 30% en aislado | _pendiente E4 + E5_ | _pendiente_ |

**Lectura del cruce 2**: Esta tabla materializa la operacionalización del Capítulo I y permite al jurado verificar que cada hipótesis está contrastada empíricamente. La columna "Decisión" se completa con: (a) "Aceptar H1x" si p < 0.05 y dirección esperada, (b) "Rechazar" si p < 0.05 en dirección opuesta, (c) "Inconcluso" si p ≥ 0.05.

### 4.4.4 Cruce 3 — Variables operacionalizadas versus indicadores observados (Tabla 4.10)

| Variable | Criterio de aceptación declarado | Valor observado | Cumple |
|---|---|---|---|
| VD1 — Rendimiento de detección | PR-AUC integrado > PR-AUC B1 (p<0.05, g≥0.5) | _pendiente_ | _pendiente_ |
| VD2 — Calidad de explicabilidad | Cobertura top-5 ≥ 80% en ≥70% de alertas; Likert ≥ 4.0 | _pendiente_ | _pendiente_ |
| VD3 — Calidad de reportes | Promedio rúbrica ≥ 4.0/5; Kappa ≥ 0.60; ROUGE-L ≥ 0.40 | _pendiente_ | _pendiente_ |
| VD4 — Comprensión y tiempo | Reducción ≥ 20% tiempo; Likert ≥ 4.0; tasa correcta ≥ 0.80 | _pendiente_ | _pendiente_ |
| VD5 — Trazabilidad | ≥ 95% alertas con 8 campos completos | _pendiente_ | _pendiente_ |

### 4.4.5 Cruce 4 — Mapa principio regulatorio → componente arquitectónico → métrica observada (Tabla 4.11)

| Principio (D.S. 115-2025-PCM / NIST AI RMF / EU AI Act Art. 13) | Componente arquitectónico responsable | Métrica observada |
|---|---|---|
| Transparencia | Capa 3 SHAP + Anexo B Model Cards | VD2 cobertura top-k + claridad Likert |
| Explicabilidad | TreeSHAP top-5 + reporte LLM+RAG | VD2 + VD3 |
| Supervisión humana | Revisión obligatoria del reporte antes de uso | Cuestionario VD4 SUS pregunta 9 (confianza) |
| Gestión de riesgos | Umbrales calibrados + validación cruzada por semilla | VD1 PR-AUC media ± DE |
| Documentación | Datasheet (Anexo C) + Model Cards (Anexo B) | Logs de versión + Anexo D |
| Trazabilidad | Estructura de 8 campos por alerta | VD5 % alertas completas |
| Anti-alucinación | RAG anclado en SHAP + validación numérica posterior | VD3 dimensión consistencia numérica |

**Lectura del cruce 4**: Esta tabla evidencia que cada principio regulatorio relevante tiene un componente concreto que lo materializa y una métrica empírica que lo verifica. Es la evidencia operativa de la "conformidad de diseño" declarada en §2.3.8.

### 4.4.6 Cruce 5 — Errores por tipo de anomalía y posibles causas (Tabla 4.12)

| Tipo anomalía | Recall obs. | Mecanismo probable de fallos | Recomendación de mejora |
|---|---|---|---|
| precio | _pendiente_ | Outliers de cola gruesa pueden caer dentro del rango plausible si la variación es estacional | Incorporar covariable mes y desviación respecto a la media móvil del producto |
| volumen | _pendiente_ | Posible confusión con eventos extraordinarios reales (campaña pico) | Añadir feature `dia_pico_campania` |
| clima | _pendiente_ | LOF sensible a vecindario; pocas observaciones con sequía + calor extremo | Agregar densidad estacional regional |
| logistica | _pendiente_ | Anomalía compuesta (dos condiciones) — IF puede subestimar | Reforzar con regla determinista complementaria |
| calidad | _pendiente_ | Pocas instancias inyectadas (10%) | Subir a 15% en v1.1 si recall < 0.6 |

### 4.4.7 Interpretación conjunta

> **Lectura integrada (a completar con resultados reales)**: Si los cinco cruces (Tabla 4.8–4.12) muestran consistencia direccional con las predicciones del Capítulo I, esta tesis sostiene que la arquitectura propuesta no solo es novedosa por su integración modular, sino también empíricamente superior bajo las condiciones evaluadas. En caso de inconsistencias, se documentan en §4.5 (Limitaciones de los resultados) y se proponen líneas de mejora en §5.3 (Trabajo futuro).

## 4.5 Limitaciones de los Resultados

Los resultados de este capítulo deben interpretarse considerando:

1. **Naturaleza sintética del dataset**: las distribuciones reflejan rangos plausibles documentados, pero no replican la variabilidad operativa real de empresas agroexportadoras (ver §1.12.1).
2. **Tamaño de muestra del estudio de usabilidad**: N ≥ 15 permite reportar resultados exploratorios; para conclusiones con potencia 0.80 se requiere N = 27.
3. **Variabilidad estocástica del LLM**: cada reporte se genera con temperature = 0.2 y se reporta como promedio sobre 3 generaciones; sigue siendo sensible a cambios de versión del modelo base.
4. **Comparación con literatura**: los valores absolutos no son directamente comparables entre trabajos por diferencias de dominio y dataset; se contrasta cobertura modular y direccionalidad.

## 4.6 Síntesis del Capítulo IV

1. El ensemble IF + LOF + ECOD _supera/no supera_ al detector individual con tamaño de efecto _g_=_pendiente_ (H1a).
2. SHAP _mejora/no mejora_ la comprensión de las alertas (H1b).
3. RAG anclado _mejora/no mejora_ la calidad de los reportes (H1c).
4. El sistema integrado _reduce/no reduce_ el tiempo-a-decisión (H1d).
5. La trazabilidad documental alcanza _XX_% de alertas completas en la condición integrada.
6. El cruce con literatura confirma que la integración de los cuatro módulos con restricción anti-alucinación es una contribución original verificable.

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CAPÍTULO V: CONCLUSIONES Y TRABAJOS FUTUROS

> **Pendiente:** Capítulo V — depende de los resultados del Capítulo IV


## 5.1 Conclusiones

*(Esqueleto para la síntesis final: el sistema integrado logró los objetivos propuestos, manteniendo el balance entre vanguardia tecnológica y rigor legal. Incluir: conclusión sobre el gap cerrado, métricas alcanzadas vs. objetivos, validación de hipótesis H1a–H1d, aporte al contexto regulatorio peruano).*

## 5.2 Limitaciones de la Investigación

*(Abordar: limitaciones del dataset sintético agroexportador; granularidad y disponibilidad de fuentes públicas; dependencia de la calidad de datos documentada en Datasheets for Datasets (Gebru et al., 2021); deuda técnica de mantenimiento del pipeline MLOps (Sculley et al., 2015); limitaciones del tamaño de la muestra en la evaluación de comprensión; restricciones de los LLMs actuales en precisión de cálculo aritmético (Maynez et al., 2026)).*

## 5.3 Trabajos Futuros

*(Propuestas: integración de GraphRAG para recuperación semántica más rica sobre conocimiento agroexportador; extensión del ensemble con ECOD (Li et al., 2022) y modelos de concept drift para supervisión en stream; exploración de Chronos (Ansari et al., 2024) para forecasting de horizonte largo; prueba piloto en una empresa agroexportadora peruana; evaluación de sesgos y limitaciones según Datasheets for Datasets (Gebru et al., 2021)).*

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CRONOGRAMA DE ACTIVIDADES

> **Pendiente:** Conclusiones/Conclusions — depende de Cap IV y V


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

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# RECOMENDACIONES

1. **Para implementadores**: Se recomienda iniciar el despliegue del sistema con el módulo de predicción GBDT y el módulo de explicabilidad SHAP antes de integrar el componente LLM+RAG, siguiendo el principio de implementación incremental que reduce la deuda técnica (Sculley et al., 2015) y permite validar cada capa de forma independiente.

2. **Para empresas agroexportadoras**: Antes de adoptar el sistema en producción, se recomienda elaborar Datasheets for Datasets (Gebru et al., 2021) para todos los datasets de entrenamiento y Model Cards (Mitchell et al., 2019) para los modelos XGBoost, detectores de anomalías y LLM+RAG.

3. **Para futuros investigadores**: Se recomienda extender la evaluación del sistema con un diseño experimental longitudinal que capture el efecto del concept drift en precios, volúmenes, clima y comportamiento exportador, utilizando ventanas temporales y fuentes agroexportadoras reales.

4. **Para entidades públicas y sectoriales**: Se recomienda promover guías técnicas de IA explicable y trazabilidad para sistemas de supervisión en cadenas productivas, tomando como referencia marcos nacionales e internacionales de gobernanza de IA.

5. **Para la academia**: Se recomienda replicar el estudio con datos reales de una empresa agroexportadora colaboradora (bajo acuerdo de confidencialidad), ampliar la muestra de evaluación con supervisores operativos y responsables de calidad, e incorporar métricas de sesgo y robustez según las dimensiones de evaluación de ADBench (Han et al., 2022).

---

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

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

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

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

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# ANEXOS

## Anexo A — Protocolo de Evaluación de Usabilidad

> **Versión 1.0 — 2026-05-17.** Aprobar antes de iniciar reclutamiento de participantes.

### A.1 Objetivo del experimento

El experimento de usabilidad mide el impacto del sistema integrado de supervisión operativa en la **eficiencia (VD4 — tiempo-a-decisión)**, **comprensión (VD4 — Likert)** y **trazabilidad documental (VD5)** frente al uso de componentes aislados. Constituye la fuente principal de evidencia para contrastar las sub-hipótesis H1b y H1d (Capítulo I §1.4).

### A.2 Diseño experimental

**Tipo**: Cuasi-experimental con diseño within-subjects (apareado) y orden contrabalanceado.

Cada participante ejecuta las mismas tareas en dos condiciones:
- **Condición A — Sistema integrado**: pipeline de 4 capas con alerta + score + vector SHAP top-5 + reporte LLM+RAG.
- **Condición B — Componentes aislados**: alerta + score crudo del detector, sin SHAP, sin reporte narrativo (solo tabla y visualización técnica).

La mitad de los participantes inicia con A y la otra mitad con B, asignación aleatorizada con `np.random.seed(42)`. Entre ambas condiciones se intercala un descanso de 5 minutos y una tarea distractora (sopa de letras) para reducir efectos de arrastre.

### A.3 Tareas evaluadas

Cada condición presenta el mismo bloque de 10 alertas (5 positivas reales, 3 negativas reales, 2 ambiguas) extraídas del conjunto de test del dataset sintético. Para cada alerta, el participante:

1. **Tarea T1 — Clasificación**: decide si la alerta corresponde a una anomalía operativa real (sí/no/dudoso).
2. **Tarea T2 — Justificación**: en una oración (máx. 200 caracteres) indica la variable que justifica la decisión.
3. **Tarea T3 — Comprensión**: responde Likert 1–5 sobre cuán comprensible resultó la alerta.

Al finalizar el bloque de 10 alertas, completa un cuestionario post-bloque (SUS adaptado + preguntas abiertas).

### A.4 Métricas registradas automáticamente

| Métrica | Fuente | Resolución |
|---|---|---|
| Tiempo apertura alerta → decisión | Log JavaScript de la plataforma | milisegundos |
| Tiempo total bloque | Log JavaScript | segundos |
| Clasificación del participante | Formulario | sí / no / dudoso |
| Justificación textual | Formulario | texto libre |
| Likert comprensión | Formulario | 1–5 |
| Versión del sistema | Variable de configuración | string |
| Identificador de alerta | Variable | string |

### A.5 Criterios de inclusión y exclusión de participantes

**Inclusión**:
- (a) Estudiantes de pregrado ≥ 7° semestre en Ingeniería de Sistemas, Industrial, Agronomía o Administración; o
- (b) Profesionales con ≥ 1 año de experiencia en supervisión operativa, control de calidad, auditoría interna o cargos análogos.
- Mayores de 18 años.
- Aceptación de consentimiento informado.

**Exclusión**:
- Participación previa en el diseño, desarrollo o entrenamiento de cualquier capa del sistema evaluado.
- Conflicto de interés directo declarado.
- Discapacidad visual no corregible que impida la lectura del dashboard.

### A.6 Tamaño de muestra y reclutamiento

**Tamaño meta**: N ≥ 15 participantes (reportar resultados como exploratorios). Tamaño deseable: N = 27 para potencia 0.80 con Cohen's dz = 0.5 (efecto medio). N ≤ 14 obliga a marcar resultados como preliminares y sin pretensión de significancia estadística.

**Reclutamiento**: difusión a través de UNSA (Escuela de Ingeniería de Sistemas, Industrial y Agronomía); contactos directos con empresas agroexportadoras de Arequipa, Ica y La Libertad mediante invitación remitida por el asesor.

### A.7 Procedimiento detallado (sesión por participante, ~45 minutos)

| Paso | Duración | Contenido |
|---|---|---|
| 1 | 5 min | Bienvenida + consentimiento informado firmado |
| 2 | 5 min | Tutorial guiado de la plataforma (alerta de ejemplo) |
| 3 | 12 min | Bloque 1 — Condición A o B (según contrabalanceo) |
| 4 | 5 min | Descanso + tarea distractora |
| 5 | 12 min | Bloque 2 — Condición contraria |
| 6 | 5 min | Cuestionario final SUS + preguntas abiertas |
| 7 | 1 min | Cierre + agradecimiento |

### A.8 Consentimiento informado (texto base)

```
Por la presente confirmo que:
1. He sido informado sobre el propósito del estudio: evaluar la usabilidad de
   un sistema de supervisión operativa con IA explicable.
2. Comprendo que mi participación es voluntaria y puedo retirarme en cualquier
   momento sin justificación ni consecuencia.
3. Comprendo que mis respuestas son anónimas. Solo el investigador principal
   accederá a los datos, que se almacenarán cifrados y se eliminarán al
   finalizar la tesis (julio 2027).
4. Acepto que se registre el tiempo de mis respuestas y las opciones
   seleccionadas para análisis estadístico agregado.
5. Comprendo que no recibiré evaluación individual ni se compartirán mis
   resultados con terceros.
6. Acepto participar en una sesión de aproximadamente 45 minutos.

Nombre: ____________________  Fecha: __________  Firma: __________
```

### A.9 Cuestionario post-bloque

**Bloque I — Comprensión percibida (Likert 1–5)**

| # | Ítem | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 1 | Entendí claramente por qué el sistema marcó cada alerta | | | | | |
| 2 | La información presentada me ayudó a tomar una decisión | | | | | |
| 3 | Las variables explicativas fueron suficientes | | | | | |
| 4 | El reporte generado fue útil para justificar mi decisión | | | | | |
| 5 | Confío en la decisión del sistema | | | | | |

**Bloque II — Tiempo y carga cognitiva (Likert 1–5)**

| # | Ítem | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 6 | Me tomó mucho tiempo entender cada alerta (1) — Fui rápido (5) | | | | | |
| 7 | Tuve que esforzarme mucho mentalmente | | | | | |
| 8 | Me sentí seguro al decidir | | | | | |

**Bloque III — Adaptación SUS (10 ítems Likert 1–5)**

```
1. Creo que me gustaría usar este sistema frecuentemente.
2. Encontré el sistema innecesariamente complejo.
3. Pensé que el sistema fue fácil de usar.
4. Necesitaría el apoyo de un experto técnico para usar este sistema.
5. Las funciones del sistema están bien integradas.
6. Hay demasiada inconsistencia en este sistema.
7. La mayoría aprendería a usar este sistema rápidamente.
8. Encontré el sistema muy engorroso.
9. Me sentí muy confiado al usar el sistema.
10. Necesitaría aprender muchas cosas antes de usar el sistema.
```

**Bloque IV — Preguntas abiertas**

1. ¿Qué fue lo más útil del sistema en esta sesión?
2. ¿Qué información agregaría o quitaría?
3. ¿En qué situación operativa real este sistema sería más valioso?

### A.10 Variables registradas para análisis

| Variable | Tipo | Origen |
|---|---|---|
| `participant_id` | string anónimo | Generado |
| `order` | {AB, BA} | Aleatorización |
| `condition` | {integrated, isolated} | Variable independiente |
| `alert_id` | string | Dataset |
| `gt_label` | {0, 1} | Dataset (oculto al participante) |
| `user_decision` | {yes, no, dunno} | Formulario |
| `time_to_decision_ms` | int | Log JavaScript |
| `likert_comprehension` | 1–5 | Cuestionario |
| `justification_text` | string | Formulario |
| `sus_score` | 0–100 | Cálculo SUS |

### A.11 Plan de análisis estadístico

1. **Tiempo-a-decisión (VD4-a)**: t de Student apareado integrado vs. aislado; Wilcoxon si Shapiro-Wilk rechaza normalidad. Reportar media ± DE, IC95%, Cohen's dz.
2. **Comprensión Likert (VD4-b)**: Wilcoxon signed-rank apareado.
3. **Decisión correcta (VD4-c)**: McNemar sobre pares concordantes/discordantes.
4. **SUS**: comparación de medias con Mann-Whitney U.
5. **Análisis cualitativo de respuestas abiertas**: análisis temático con doble codificación independiente.

### A.12 Almacenamiento y privacidad de datos

- Datos almacenados en archivo CSV cifrado con clave conocida solo por el investigador.
- Identificadores anónimos, sin nombre, correo ni datos demográficos sensibles.
- Backup en disco duro institucional UNSA.
- Eliminación de datos crudos al cierre del proyecto (julio 2027).
- Resultados agregados publicados en la tesis y en el repositorio GitHub.

### A.13 Aprobación ética

El protocolo se somete a revisión del asesor de tesis (Dr. Víctor Manuel Cornejo Aparicio) y, si la Escuela de Ingeniería de Sistemas dispone de comité de ética, a su aprobación formal antes del reclutamiento.

---

*Anexo A — versión 1.0 — 2026-05-17. Sometido a revisión final antes de ejecutar el estudio.*

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo B — Model Cards del Sistema

> **Estándar aplicado**: Mitchell et al. (2019) — Model Cards for Model Reporting (Mitchell et al., 2019).
> **Estado**: 📐 Plantillas listas, métricas pendientes de completar tras experimentos E1–E5.

> Cada Model Card sigue las 9 secciones de Mitchell et al.: detalles del modelo, uso previsto, factores, métricas, datos de evaluación, datos de entrenamiento, análisis cuantitativos, consideraciones éticas, advertencias y recomendaciones.

---

### B.1 Model Card — Módulo de Predicción Tabular (XGBoost / LightGBM)

**1. Detalles del modelo**
- Nombre: `module1_prediction`
- Tipo: Ensemble de Gradient Boosting Decision Trees (XGBoost + LightGBM)
- Versión: 1.0
- Autor: Yoset Cozco Mauri (UNSA)
- Licencia del modelo entrenado: MIT
- Citación recomendada: Cozco Mauri (2026), *Tesis UNSA*.
- Hiperparámetros: definidos mediante Optuna TPE con 50 trials, optimizando PR-AUC.

**2. Uso previsto**
- Estimar el riesgo operativo (valor esperado de score) de cada registro agroexportador.
- Usuario primario: módulo de detección de anomalías (capa 2) y supervisor operativo a través del dashboard.
- Uso fuera de alcance: clasificación de decisiones legales o financieras automatizadas; no debe usarse en contextos distintos al sector agroexportador peruano sin recalibración.

**3. Factores**
- Producto, zona, mes, destino.
- Variables climáticas (temperatura, precipitación, humedad).
- Cumplimiento fitosanitario y días logísticos.

**4. Métricas**
- PR-AUC, ROC-AUC, F1, Precision, Recall.
- Reportadas como media ± DE sobre 6 semillas en el test set.

**5. Datos de evaluación**
- Dataset sintético agroexportador v1.0 (Anexo C), conjunto de test (20% cronológicamente posterior).

**6. Datos de entrenamiento**
- Dataset sintético v1.0, conjunto de train (70%) + validation (10%).

**7. Análisis cuantitativos**
| Métrica | Valor (mean ± SD) |
|---|---|
| PR-AUC | _pendiente_ |
| ROC-AUC | _pendiente_ |
| F1 | _pendiente_ |
| Precision | _pendiente_ |
| Recall | _pendiente_ |

Análisis por subgrupos (fairness):
| Subgrupo | PR-AUC | F1 |
|---|---|---|
| Producto = arándano | _pendiente_ | _pendiente_ |
| Producto = uva | _pendiente_ | _pendiente_ |
| Producto = palta | _pendiente_ | _pendiente_ |
| Producto = cacao | _pendiente_ | _pendiente_ |
| Producto = espárrago | _pendiente_ | _pendiente_ |
| Zona = Ica | _pendiente_ | _pendiente_ |
| Zona = La Libertad | _pendiente_ | _pendiente_ |

**8. Consideraciones éticas**
- Datos sintéticos: cero riesgo de exposición de información personal o empresarial.
- Posible sesgo geográfico: solo 5 departamentos modelados.
- Mitigación: documentación explícita del alcance y limitaciones de generalización.

**9. Advertencias y recomendaciones**
- Recalibrar antes de uso operativo real con datos de empresa.
- Monitorear data drift mensual (KS test sobre distribuciones de input).
- No usar como única fuente de decisión; siempre con revisión humana.

---

### B.2 Model Card — Módulo de Detección de Anomalías (Ensemble IF + LOF + ECOD)

**1. Detalles del modelo**
- Nombre: `module2_anomaly`
- Tipo: Ensemble no supervisado (Isolation Forest + LOF + ECOD)
- Versión: 1.0
- Infraestructura: PyOD (Zhao et al., 2019)
- Estrategia de combinación: promedio normalizado de scores (alternativa: voto por mayoría con umbral por detector).

**2. Uso previsto**
- Identificar registros operativos atípicos en el dataset agroexportador.
- Salida: score continuo (0–1) y bandera binaria (≥ umbral → anomalía).

**3. Factores**
- Mismas variables que módulo 1, con preprocesamiento StandardScaler para LOF.

**4. Métricas**
- PR-AUC, ROC-AUC, F1 con umbral óptimo, Specificity.
- Tasa de falsos positivos como métrica operativa (cuántas alertas se generan al día).

**5. Datos de evaluación**
- Conjunto de test del dataset sintético v1.0.

**6. Datos de entrenamiento**
- Conjunto de train (no se usan etiquetas durante el fit — entrenamiento no supervisado).

**7. Análisis cuantitativos**
| Detector | PR-AUC | ROC-AUC | F1 | FPR |
|---|---|---|---|---|
| Isolation Forest individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| LOF individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| ECOD individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| Ensemble IF+LOF+ECOD | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |

Por tipo de anomalía inyectada:
| Tipo | Recall ensemble | Recall IF solo |
|---|---|---|
| precio | _pendiente_ | _pendiente_ |
| volumen | _pendiente_ | _pendiente_ |
| clima | _pendiente_ | _pendiente_ |
| logistica | _pendiente_ | _pendiente_ |
| calidad | _pendiente_ | _pendiente_ |

**8. Consideraciones éticas**
- Riesgo de sobre-alerta sobre productos o zonas específicas si la distribución del dataset está sesgada.
- Mitigación: análisis de tasa de alerta por subgrupo y calibración de umbral por categoría.

**9. Advertencias y recomendaciones**
- Ajustar umbral según costo operativo de falsos positivos en cada empresa.
- No usar sin la capa de explicabilidad SHAP (las alertas sin contexto generan ruido).

---

### B.3 Model Card — Módulo de Explicabilidad (TreeSHAP)

**1. Detalles del modelo**
- Nombre: `module3_shap`
- Tipo: TreeSHAP (cálculo exacto de valores de Shapley en árboles)
- Versión: 1.0 (librería `shap`)
- Fundamento: Lundberg & Lee (2017); TreeSHAP — Lundberg et al. (2020)

**2. Uso previsto**
- Generar vectores de contribución por variable para cada alerta.
- Alimentar la capa LLM+RAG con evidencia cuantitativa estructurada.

**3. Factores**
- Las mismas variables del modelo predictor; las contribuciones se reportan en la escala del logit del XGBoost.

**4. Métricas**
- Cobertura top-k (k=3, k=5).
- Consistencia ρ entre alertas del mismo tipo (Spearman).
- Claridad operativa (Likert 1–5 evaluada en estudio de usabilidad).

**5. Datos de evaluación**
- Subconjunto de 100 alertas seleccionadas aleatoriamente del test set.

**6. Datos de entrenamiento**
- N/A — SHAP es un método post-hoc, no se entrena.

**7. Análisis cuantitativos**
| Métrica | Valor |
|---|---|
| Cobertura top-5 (mediana) | _pendiente_ |
| Cobertura top-3 (mediana) | _pendiente_ |
| Consistencia ρ (mediana) | _pendiente_ |
| Likert claridad (mediana) | _pendiente_ |

**8. Consideraciones éticas**
- SHAP puede inducir sobre-confianza si se interpreta como causalidad. Es una atribución, no una causa.
- Mitigación: documentación explícita en el dashboard y en el reporte generado.

**9. Advertencias y recomendaciones**
- TreeSHAP es exacto solo para árboles; no aplicar a modelos no-árbol.
- El orden y magnitud de las contribuciones depende del modelo predictor; cambiar el modelo invalida explicaciones previas.

---

### B.4 Model Card — Módulo de Generación de Reportes (LLM + RAG)

**1. Detalles del modelo**
- Nombre: `module4_rag`
- Componentes:
  - LLM base: Anthropic Claude Sonnet 4.6 (o alternativa local Llama 3.1 8B Instruct).
  - Retriever: BM25 sobre fuentes agroexportadoras + vectores SHAP estructurados.
  - Prompt template: estructurado con campos obligatorios (dato, modelo, score, umbral, SHAP, fuente, recomendación).
- Versión: 1.0
- Parámetros: temperature = 0.2, max_tokens = 800.

**2. Uso previsto**
- Generar reporte narrativo de cada alerta operativa, anclado en evidencias SHAP y fuentes recuperadas.
- Usuario primario: supervisor operativo, auditor interno.

**3. Factores**
- Vector SHAP top-5 de la alerta.
- Score y umbral aplicado.
- Fragmentos recuperados de la base de conocimiento (fuentes MIDAGRI, SENAMHI, etc.).

**4. Métricas**
- Rúbrica de 5 dimensiones (completitud, consistencia numérica, accionabilidad, coherencia textual, correspondencia con evidencias).
- ROUGE-1, ROUGE-L cuando exista referencia humana.
- Kappa de Cohen entre dos revisores.

**5. Datos de evaluación**
- 20 reportes generados a partir de alertas seleccionadas aleatoriamente del test set.
- Evaluación por 2 revisores independientes con la rúbrica del Capítulo III §3.3.

**6. Datos de entrenamiento**
- N/A — LLM no se fine-tunea. El conocimiento operativo se inyecta vía RAG en tiempo de inferencia.

**7. Análisis cuantitativos**
| Dimensión | Valor (media de 2 revisores) | Kappa Cohen |
|---|---|---|
| Completitud | _pendiente_ | _pendiente_ |
| Consistencia numérica | _pendiente_ | _pendiente_ |
| Accionabilidad | _pendiente_ | _pendiente_ |
| Coherencia textual | _pendiente_ | _pendiente_ |
| Correspondencia con evidencias | _pendiente_ | _pendiente_ |
| **Promedio total** | _pendiente_ | _pendiente_ |
| ROUGE-L (subset con referencia humana) | _pendiente_ | — |

**8. Consideraciones éticas**
- Riesgo de alucinación numérica residual (intrinsic hallucination): un porcentaje de reportes puede contener números no presentes en SHAP.
- Mitigación: validación posterior automática (regex extrae números del reporte y compara con vector SHAP).
- Dependencia de API comercial: variabilidad por versión de modelo.

**9. Advertencias y recomendaciones**
- Ningún reporte debe usarse sin revisión humana en contextos operativos críticos.
- Documentar siempre la versión exacta del LLM al generar el reporte.
- Verificar coincidencia numérica entre reporte y SHAP antes de publicar.

---

*Anexo B — versión 1.0 — 2026-05-17. Plantillas completas; métricas se completan tras experimentos E1–E5.*

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo C — Datasheet del Dataset Sintético Agroexportador

> **Estándar aplicado**: Gebru et al. (2021) — Datasheets for Datasets (Gebru et al., 2021).
> **Versión del dataset**: v1.0
> **Fecha de creación prevista**: 2026-06-01 (Hito 2 del plan general)
> **Estado actual**: 📐 Especificación completa lista para generación.

---

### C.1 Motivación

**¿Para qué se creó el dataset?**
Para entrenar y evaluar de forma reproducible el sistema integrado de supervisión operativa con IA explicable propuesto en esta tesis, sin depender de datos privados de empresas agroexportadoras. La opción sintética permite (a) controlar la distribución de anomalías, (b) garantizar reproducibilidad mediante semilla fija, y (c) publicar el dataset junto al paper.

**¿Quién lo creó?**
Yoset Cozco Mauri, Escuela Profesional de Ingeniería de Sistemas, Universidad Nacional de San Agustín de Arequipa (UNSA). Bajo asesoría del Dr. Víctor Manuel Cornejo Aparicio.

**¿Quién financió la creación?**
Sin financiamiento externo. Desarrollo en el marco de una tesis de pregrado.

---

### C.2 Composición

**¿Qué instancias representa?**
Cada fila representa un evento operativo agroexportador diario por combinación de producto, zona y destino. Una instancia agrupa indicadores de producción, comercialización, clima, sanidad, logística y calidad para un día específico.

**¿Cuántas instancias?**
Mínimo 2,000 — Recomendado 5,000 — Tope 10,000. La versión inicial v1.0 generará 2,000 instancias.

**¿Es muestra o universo?**
Es una muestra sintética generada para cubrir las distribuciones plausibles del sector durante el período 2022-01-01 a 2025-12-31.

**¿Qué datos contiene cada instancia?**

| Variable | Tipo | Descripción | Rango plausible | Fuente para rangos | Distribución |
|---|---|---|---|---|---|
| `id` | int | Identificador único | 1..N | — | Secuencial |
| `fecha` | datetime | Día del evento | 2022-01-01 a 2025-12-31 | — | Uniforme |
| `producto` | category | Producto agroexportador | {arándano, uva, palta, cacao, espárrago} | MIDAGRI | Ponderada por participación |
| `zona` | category | Departamento productor | {Ica, La Libertad, Piura, Arequipa, Lima} | MIDAGRI | Ponderada por área cultivada |
| `volumen_kg` | float | Volumen del día (kg) | 500–50,000 | MIDAGRI | LogNormal(μ=8, σ=1.2) |
| `precio_kg_usd` | float | Precio FOB por kg | 0.5–12.0 | MIDAGRI / SUNAT | Normal por producto |
| `temperatura_max_c` | float | Temperatura máxima del día (°C) | 15–38 | SENAMHI | Normal por zona/mes |
| `temperatura_min_c` | float | Temperatura mínima del día (°C) | 5–22 | SENAMHI | Normal por zona/mes |
| `precipitacion_mm` | float | Precipitación diaria (mm) | 0–200 | SENAMHI | Gamma(α=0.5, β=10) |
| `humedad_pct` | float | Humedad relativa (%) | 40–95 | SENAMHI | Beta(α=8, β=3) |
| `destino_mercado` | category | Mercado destino | {EEUU, UE, Asia, Otro} | SUNAT | Ponderada por exportaciones |
| `cumplimiento_fitosanitario` | binary | Lote cumple SENASA | {0, 1} | SENASA | Bernoulli(p=0.92) |
| `dias_logisticos` | int | Días desde cosecha a embarque | 3–45 | Estimado | LogNormal(μ=2.3, σ=0.5) |
| `merma_pct` | float | Pérdida del lote (%) | 0–30 | Estimado | Beta(α=2, β=10) |
| `costo_logistico_usd_kg` | float | Costo logístico unitario | 0.05–1.2 | Estimado | LogNormal |
| `tipo_cambio_pen_usd` | float | Tipo de cambio del día | 3.5–4.2 | BCRP | Random walk con tendencia |
| `etiqueta_anomalia` | binary | Es anomalía operativa | {0, 1} | Inyección controlada | Bernoulli(p=0.12) |
| `tipo_anomalia` | category | Tipo de anomalía | {precio, volumen, clima, logistica, calidad, none} | Inyección controlada | Definida por reglas |

**Total**: 17 columnas; 2,000 filas en v1.0.

**¿Las etiquetas son confiables?**
Sí, porque el dataset es sintético y las etiquetas se asignan según las reglas de inyección documentadas (§C.4). No hay ambigüedad por error humano de etiquetado.

**¿Falta algún dato?**
Sí, se inyectan valores faltantes en el 3% de las filas para simular registros parciales (campos: humedad_pct, dias_logisticos, costo_logistico_usd_kg). Esto evalúa robustez del modelo ante datos incompletos típicos de fuentes operativas.

**¿Las relaciones entre instancias son explícitas?**
Las instancias están temporalmente ordenadas. No hay relación de identidad (no es panel longitudinal con seguimiento individual). Una misma combinación (producto, zona, fecha) puede aparecer solo una vez.

**¿División train/test recomendada?**
División cronológica:
- Train: 2022-01-01 a 2024-12-31 (70%)
- Validation: 2025-01-01 a 2025-04-30 (10%)
- Test: 2025-05-01 a 2025-12-31 (20%)

Esta división evita data leakage temporal y simula el caso realista de aplicar el modelo a períodos futuros.

**¿Hay datos sensibles?**
No. No hay datos personales, no se identifican empresas reales, no se referencian transacciones específicas. Es completamente sintético.

---

### C.3 Proceso de recolección

**¿Cómo se generaron los datos?**
Mediante un script Python (`src/generate_synthetic_dataset.py`) que muestrea cada columna según las distribuciones de la tabla §C.2 condicionadas a (producto, zona, mes). La generación se realiza en cuatro pasos:
1. Muestreo de variables base (fecha, producto, zona).
2. Muestreo condicional de variables dependientes (clima por zona+mes; precio por producto+mes).
3. Inyección de correlaciones plausibles (volumen ↑ → merma ↓ por economías de escala; precipitacion ↑ → merma ↑ por daño post-cosecha).
4. Inyección controlada de anomalías según reglas §C.4.

**¿Quién recopiló los datos?**
N/A — Datos sintéticos generados por el autor con `numpy.random.default_rng(seed=42)`.

**¿En qué período se generaron?**
Generación prevista: 2026-05-31 a 2026-06-01.

---

### C.4 Inyección de anomalías

**Distribución de tipos de anomalía** (sobre 12% de filas marcadas como anómalas):

| Tipo | Proporción | Mecanismo de inyección | Variables afectadas |
|---|---|---|---|
| `precio` | 30% | `precio_kg_usd` > percentil 99 o < percentil 1 del producto | precio_kg_usd |
| `volumen` | 25% | `volumen_kg` > media + 3·DE para producto/zona | volumen_kg |
| `clima` | 20% | `temperatura_max_c` > 38°C ∧ `precipitacion_mm` < 1 mm (sequía con calor extremo) | temperatura_max_c, precipitacion_mm |
| `logistica` | 15% | `dias_logisticos` > percentil 95 ∧ `cumplimiento_fitosanitario` = 1 (demora a pesar de cumplir) | dias_logisticos |
| `calidad` | 10% | `merma_pct` > 25% ∧ `precio_kg_usd` > mediana (pérdida con precio alto) | merma_pct |

**Verificabilidad**: Para cada anomalía inyectada se registra `tipo_anomalia` y el campo `regla_inyeccion` que documenta los valores exactos que activaron la regla. Esto permite auditoría posterior del proceso de generación.

---

### C.5 Preprocesamiento, limpieza y etiquetado

**¿Se aplicó preprocesamiento?**
El dataset v1.0 se publica sin preprocesamiento adicional. El script de pipeline (`src/pipeline.py`) aplica:
1. Imputación de valores faltantes (mediana para numéricas, moda para categóricas).
2. Codificación one-hot de variables categóricas.
3. Escalamiento StandardScaler para variables numéricas (solo para LOF; XGBoost no lo requiere).
4. Construcción de features derivadas: `temperatura_rango = temperatura_max_c - temperatura_min_c`, `precio_unitario_zscore` por producto.

**¿Los datos crudos se conservan?**
Sí. El CSV crudo (`data/dataset_agro_sintetico_v1.csv`) se versiona en Git LFS y queda como referencia de entrada al pipeline.

---

### C.6 Usos previstos y no previstos

**¿Para qué se usará el dataset?**
- Entrenar y evaluar el sistema integrado de supervisión operativa de esta tesis.
- Comparar baselines (Isolation Forest individual, ensembles parciales).
- Publicar como benchmark abierto en el repositorio GitHub asociado al paper.

**¿Para qué NO debe usarse?**
- No representa datos reales de empresas específicas; no debe usarse para toma de decisiones operativas en ninguna empresa real.
- No se diseñó para análisis económico del sector agroexportador peruano (los rangos son plausibles pero no son estadísticas oficiales).
- No es un benchmark estandarizado de la comunidad de detección de anomalías.

**¿Existen tareas para las que el dataset sería inadecuado?**
- Análisis causal: no hay manipulación experimental real, solo inyección de correlaciones plausibles.
- Modelos de pronóstico de mercado: el componente de precio no refleja la volatilidad real de los mercados internacionales.
- Sesgo geográfico/demográfico: solo se modelan 5 productos y 5 departamentos peruanos.

---

### C.7 Distribución y licencia

**¿El dataset se distribuirá?**
Sí, publicación bajo licencia **CC BY 4.0** en el repositorio GitHub asociado a esta tesis. Esto permite uso académico y comercial citando la fuente.

**¿Cómo se citará?**
```
Cozco Mauri, Y. (2026). Dataset Sintético Agroexportador Peruano v1.0 [Data set].
  Universidad Nacional de San Agustín de Arequipa.
  URL: [repositorio GitHub al publicar]
```

**¿Habrá DOI?**
Se solicitará DOI en Zenodo al cierre de la tesis para garantizar persistencia.

---

### C.8 Mantenimiento

**¿Quién mantendrá el dataset?**
Yoset Cozco Mauri hasta diciembre 2027. Después, el repositorio queda como archivo histórico.

**¿Habrá actualizaciones?**
- v1.0 — 2,000 filas — versión base de la tesis.
- v1.1 — posible si se requieren ajustes durante experimentos.
- v2.0 — versión extendida (5,000 filas) para publicación en paper.

**¿Cómo se notificarán los cambios?**
Mediante CHANGELOG.md en el repositorio y release notes versionadas por Git.

---

### C.9 Consideraciones éticas

**¿Hay riesgo de daño a personas o grupos?**
No, dado que el dataset es sintético y no contiene información de individuos ni empresas reales. La elección de 5 productos y 5 departamentos cubre los principales del sector peruano pero no excluye intencionalmente a otros actores.

**¿Hay riesgo de uso indebido?**
Riesgo bajo. El dataset es claramente etiquetado como sintético en cada archivo (header, README, paper). Cualquier uso operativo real sería contrario a la documentación.

---

### C.10 Documentación complementaria — Fuentes públicas utilizadas

El dataset se calibra con rangos plausibles tomados de las siguientes fuentes públicas. Para reproducir o ampliar el dataset, consultar:

| Fuente | URL | Variable calibrada | Acceso |
|---|---|---|---|
| MIDAGRI | https://www.gob.pe/midagri | volumen, precio, producto, zona | Público |
| SENAMHI | https://www.senamhi.gob.pe | temperatura, precipitación, humedad | Público |
| SENASA | https://www.gob.pe/senasa | cumplimiento_fitosanitario | Público |
| SUNAT | https://www.sunat.gob.pe | destino_mercado, valor exportado | Público |
| INEI | https://www.inei.gob.pe | tipo_cambio, indicadores económicos | Público |
| FAOSTAT | https://www.fao.org/faostat | producción nacional comparativa | Público |
| UN Comtrade | https://comtradeplus.un.org | exportaciones por país destino | Público |

---

### C.11 Benchmark complementario

El **BAF Benchmark** (Jesus et al., 2022) se utiliza únicamente como referencia metodológica para validación cruzada de la arquitectura en datos tabulares desbalanceados con drift temporal, NO como evidencia del dominio agroexportador. Se documenta su uso en §3.2 con esa restricción.

---

*Anexo C — versión 1.0 — 2026-05-17. Datasheet completo, listo para generación de v1.0 del dataset.*

<div style="page-break-before: always;"></div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Anexo D — Registro de Uso de Herramientas de IA

La presente investigación utilizó herramientas de inteligencia artificial generativa como apoyo en las siguientes actividades: revisión bibliográfica exploratoria, verificación de coherencia de argumentos, corrección de estilo académico y generación de borradores de secciones específicas. Todas las referencias bibliográficas fueron verificadas manualmente en las fuentes originales. Las decisiones de diseño, la interpretación de resultados y las conclusiones son responsabilidad exclusiva del investigador.

*(Adjuntar registro detallado de las sesiones de uso según los requerimientos de transparencia de la UNSA)*

---

*(Documento elaborado con apoyo de herramientas de IA — UNSA Arequipa, 2026)*
