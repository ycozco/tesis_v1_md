# Contexto y Planificación de Tesis: Sistema Integrado de Supervisión Operativa con IA Explicable

Este documento compila el contexto de la investigación, el diseño arquitectónico de la solución propuesta, el plan de desarrollo de vistas y el protocolo experimental para el tratamiento de datos y pruebas de usabilidad. Está estructurado para servir como fuente de contexto de alta fidelidad para NotebookLM.

---

## 1. Contexto General de la Tesis

### 1.1 Título de la Tesis
**Sistema Integrado de Supervisión Operativa con Inteligencia Artificial Explicable en Empresas Agroexportadoras Peruanas: Validación de la Eficiencia (Tiempo-a-Decisión), Comprensión (SHAP) y Calidad de Reportes (RAG).**

### 1.2 Resumen Ejecutivo
La investigación propone el diseño, implementación y evaluación de un sistema integrado de supervisión operativa de cuatro capas dirigido al sector agroexportador peruano (abarcando productos como arándanos, uvas, paltas, cacao y espárragos). El sistema unifica la predicción de series temporales tabulares, la detección no supervisada de anomalías por ensemble, la explicabilidad local con SHAP y la redacción automática de reportes ejecutivos mediante LLM+RAG con anclaje técnico y regulatorio. 

El objetivo es superar la brecha de los sistemas de auditoría en silos y de "caja negra" que causan desconfianza y demoras en la toma de decisiones críticas de calidad, logística o sanidad. La Resolución SBS N° 053-2023 se toma como referencia de buenas prácticas de gestión de riesgo de modelos y el D.S. N° 115-2025-PCM como marco de gobernanza, transparencia y supervisión humana en inteligencia artificial.

### 1.3 Objetivos de la Investigación
*   **Objetivo Principal**: Diseñar, implementar y evaluar un sistema integrado de supervisión operativa basado en inteligencia artificial explicable para detectar anomalías en datos agroexportadores, explicar los factores asociados mediante SHAP y generar reportes trazables que apoyen la toma de decisiones operativas.
*   **Objetivos Específicos**:
    1.  Identificar y documentar variables agroexportadoras (precios, volúmenes, clima, sanidad, logística) para entrenar modelos.
    2.  Diseñar la arquitectura modular de cuatro capas (predicción → detección → explicación → reporte).
    3.  Implementar los modelos predictivos tabulares GBDT y detectores de anomalías por ensemble.
    4.  Integrar el motor de explicabilidad local TreeSHAP.
    5.  Implementar el módulo LLM+RAG restrictivo anti-alucinaciones para redactar los reportes técnicos basados en evidencias.
    6.  Evaluar la utilidad del sistema integrado mediante pruebas estadísticas apareadas de tiempo de decisión y comprensión con testers especializados.

### 1.4 Hipótesis
*   **Hipótesis General (H1)**: Un sistema integrado de predicción, detección de anomalías, explicabilidad y generación de reportes trazables mejora la trazabilidad de decisiones, la comprensión de alertas y el tiempo de decisión de supervisores operativos frente al uso de componentes aislados.
*   **Hipótesis Nula (H0)**: No existe diferencia significativa entre el sistema integrado y los componentes aislados en trazabilidad de decisiones, comprensión de alertas o tiempo de decisión de supervisores operativos.
*   **Sub-hipótesis**:
    *   **H1a**: El ensemble detector (IF + LOF + ECOD) identifica desviaciones con mayor rendimiento técnico ($\text{PR-AUC} \ge 0.85$ y $\text{F1-Score} \ge 0.80$) que detectores individuales aislados.
    *   **H1b**: Las explicaciones SHAP incrementan la comprensión subjetiva de las alertas por parte de los supervisores al aislar el top-5 de variables incidentes.
    *   **H1c**: Los reportes generados con RAG a partir de evidencias SHAP presentan mayor consistencia y menor alucinación que reportes de LLM libre sin contexto.
    *   **H1d**: El sistema integrado reduce en al menos un 20% el tiempo promedio de decisión frente a componentes aislados en silos, con significancia estadística bajo la prueba de Wilcoxon ($\alpha = 0.05$).

### 1.5 Operacionalización de Variables
*   **Variable Independiente (VI)**: Tipo de sistema de supervisión operativa (VI1: Sistema Integrado; VI2: Componentes Técnicos Aislados).
*   **Variables Dependientes (VD)**:
    *   **VD1: Rendimiento de detección**: Medido por ROC-AUC, PR-AUC, F1-Score, Precisión y Recall.
    *   **VD2: Calidad de explicabilidad**: Cobertura Top-K (porcentaje de alertas donde el top-5 explica $\ge 80\%$ del score absoluto) e índice de estabilidad.
    *   **VD3: Calidad de reportes**: Rúbrica 5D (Completitud, Coherencia, Accionabilidad, Consistencia y Evidencias) y ROUGE-L.
    *   **VD4: Comprensión y Eficiencia del Supervisor**: Tiempo-a-decisión (segundos), comprensión percibida (Escala Likert 1-5) y tasa de decisiones correctas.
    *   **VD5: Trazabilidad documental**: Porcentaje de alertas con trazabilidad completa (dato original, modelo, score, explicación SHAP y reporte RAG anclado).

---

## 2. Arquitectura de la Solución (Las 4 Capas)

La arquitectura modular está diseñada para separar estrictamente el procesamiento numérico y de detección de la capa de narración lingüística para evitar alucinaciones operativas.

```
       [Fuentes de Datos] (MIDAGRI, SUNAT, SENAMHI, SENASA)
               │
               ▼
┌──────────────────────────────┐
│ Capa 1: Predicción Tabular    │ ──► XGBoost & LightGBM (Umbrales de normalidad)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Capa 2: Detección Anomalías  │ ──► Ensemble PyOD (IF + LOF + ECOD) -> Score consolidado
└──────────────┬───────────────┘
               │ (Si Score > 0.75)
               ▼
┌──────────────────────────────┐
│ Capa 3: Explicabilidad local │ ──► TreeSHAP (Atribución marginal top-5 variables)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Capa 4: Reportes LLM + RAG   │ ──► Generación de informe trazable e inmutable
└──────────────────────────────┘
```

### 2.1 Detalle Técnico de las Capas

#### Capa 1: Predicción Tabular de Series (GBDT)
*   **Modelos**: XGBoost & LightGBM.
*   **Entradas**: Variables operativas históricas (precios MIDAGRI, volúmenes de envío SUNAT, temperatura/humedad máxima SENAMHI, estado fitosanitario SENASA, días logísticos).
*   **Salidas**: Valores esperados y umbrales de normalidad estadística para cada registro operativo.
*   **Lógica**: Gradient Boosting optimizado para modelar series y dependencias estructuradas en datasets tabulares.
*   **Formulación**: 
    $$F_m(x) = F_{m-1}(x) + \gamma_m h_m(x)$$

#### Capa 2: Detección de Anomalías (Ensemble PyOD)
*   **Modelos**: Isolation Forest (IF) + Local Outlier Factor (LOF) + Empirical Cumulative Distribution Outlier Detection (ECOD).
*   **Entradas**: Desviaciones de los valores observados vs. valores esperados de la Capa 1.
*   **Salidas**: Score de anomalía consolidado (0.0 a 1.0) y bandera de alerta activada si el score es mayor a 0.75.
*   **Lógica**: Ensemble no supervisado que consolida la detección por aislamiento, densidad local y distribución acumulada para reducir falsos positivos.
*   **Formulación**: 
    $$\text{Score}_{\text{cons}} = \frac{1}{3}(\text{Score}_{\text{IF}} + \text{Score}_{\text{LOF}} + \text{Score}_{\text{ECOD}})$$

#### Capa 3: Explicabilidad Algorítmica (TreeSHAP)
*   **Modelos**: TreeSHAP (SHapley Additive exPlanations).
*   **Entradas**: Registros marcados como anomalías críticas en la Capa 2 y la estructura de caminos de los árboles entrenados.
*   **Salidas**: Vectores de contribución marginal (SHAP values) que indican el impacto positivo o negativo de las variables sobre el score de anomalía.
*   **Lógica**: Enfoque cooperativo basado en la Teoría de Juegos para asignar ponderaciones exactas a las variables explicativas locales.
*   **Formulación**: 
    $$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} [f_x(S \cup \{i\}) - f_x(S)]$$

#### Capa 4: Reportes Narrativos Generativos (LLM + RAG)
*   **Modelos**: LLM (Llama 3 / Claude) + motor RAG.
*   **Entradas**: Vectores de contribución SHAP (Capa 3), metadatos del lote y Base de Conocimientos regulatorios (Resolución SBS N° 053-2023, manual fitosanitario SENASA, regulaciones FDA).
*   **Salidas**: Borrador de reporte técnico automatizado en Markdown/PDF con anclaje fitosanitario y normativo.
*   **Lógica**: Restricción semántica por prompt para anclar las inferencias a datos numéricos SHAP y directivas regulatorias recuperadas vectorialmente, impidiendo alucinaciones libres.
*   **Formulación**: 
    $$\text{Reporte} = \text{LLM}(\text{Query}, \text{SHAP}, \text{Contexto}_{\text{RAG}})$$

---

## 3. Plan de Desarrollo de Vistas y Módulos (Planificación)

El desarrollo del frontend y backend de soporte está estructurado de manera descendente en cuatro fases planificadas a lo largo de un ciclo de 8 semanas:

### 3.1 Fase 1: Configuración del Pipeline de Datos y Modelos (Semanas 1-2)
*   **Estado**: Planificado.
*   **Entregables**:
    *   Generación del conjunto de datos sintético transaccional agroexportador (10,000 registros).
    *   Implementación de los estimadores GBDT (LightGBM y XGBoost) en Python para predicción de series.
    *   Configuración de algoritmos no supervisados de PyOD (IF, LOF, ECOD) para detección.

### 3.2 Fase 2: Motor de Explicabilidad y Generación de Reportes (Semanas 3-4)
*   **Estado**: Planificado.
*   **Entregables**:
    *   Integración del motor TreeSHAP para explicabilidad local del modelo de anomalías.
    *   Implementación del índice de estabilidad de SHAP y jerarquía de relevancia local.
    *   Creación de la base de conocimiento vectorial RAG para regulaciones de exportación y manuales fitosanitarios.
    *   Orquestador LLM restrictivo para la redacción de informes técnicos basados en evidencias numéricas.

### 3.3 Fase 3: Frontend y Dashboard Jerárquico del Supervisor (Semanas 5-6)
*   **Estado**: Planificado.
*   **Entregables**:
    *   Dashboard principal con KPIs consolidados de control operativo (Lotes, alertas, tasa de FP y tiempos).
    *   Cola de priorización de alertas ordenadas por criticidad del score consolidado.
    *   Vista detallada interactiva de explicabilidad local (gráficos SHAP integrados en HTML5).
    *   Implementación de la interfaz del Sandbox de usabilidad comparativa (Condición A vs. Condición B).
    *   Panel de generación y exportación de informes técnicos en PDF y Word.

### 3.4 Fase 4: Protocolo de Usabilidad y Cierre Experimental (Semanas 7-8)
*   **Estado**: Planificado.
*   **Entregables**:
    *   Despliegue de la versión experimental en contenedor Docker institucional.
    *   Convocatoria y selección del grupo cerrado de testers especializados ($N=15$ a $N=27$).
    *   Registro automático de telemetría de interacción (segundos transcurridos hasta la toma de decisión).
    *   Cálculo y validación de contrastes estadísticos (Wilcoxon Signed-Rank, t-test y análisis SUS).

---

## 4. Diseño Experimental y Protocolo de Usabilidad

### 4.1 Tratamiento de Datos y División Temporal
Para prevenir la fuga de información (data leakage) provocada por la estacionalidad climática y logística en agroexportación, se descarta la división aleatoria de datos. En su lugar, se implementa una **partición temporal cronológica**:
*   **Entrenamiento (Train) — 70%**: Datos cronológicamente iniciales para el modelado de normalidad.
*   **Validación (Validation) — 10%**: Empleada para el ajuste de hiperparámetros (Optuna, 50 trials).
*   **Pruebas (Test) — 20%**: Evaluación final del ensemble y fuente para la simulación de usabilidad.
*   *Reproducibilidad*: Fijación de la semilla principal en 42 y repetición con 5 semillas adicionales (43, 44, 45, 46, 47) para mitigar variabilidad estocástica en los algoritmos.

### 4.2 Experimentos Controlados (E1 a E5)

| Exp. | Nombre del Experimento | Condición Experimental | Grupo de Control | Variable Observada (VD) | Hipótesis |
|---|---|---|---|---|---|
| **E1** | Rendimiento de Detección | Ensemble IF + LOF + ECOD (PyOD) | Isolation Forest Individual | VD1: PR-AUC, F1-Score | H1a |
| **E2** | Aporte de Explicabilidad | Sistema con vectores SHAP | Sistema sin SHAP (solo scores) | VD2: Cobertura Top-K, Likert | H1b |
| **E3** | Aporte de Anclaje RAG | LLM + RAG (anclado en SHAP) | LLM libre (sin RAG) | VD3: Rúbrica 5D, ROUGE-L | H1c |
| **E4** | Evaluación del Sistema Integrado | Pipeline completo de 4 capas | Salidas técnicas aisladas en silos | VD4: Tiempo de decisión, Likert | H1d |
| **E5** | Ablation Study | Configuraciones parciales (E5a a E5d) | — | VD1 y VD5: Trazabilidad | Aporte Capa |

*   *Notas de Ablación*: E5a (Solo Capa 2), E5b (Capas 1+2+4 sin SHAP), E5c (Capas 1+2+3 sin RAG), E5d (Pipeline completo).

### 4.3 Pruebas de Contraste Estadístico

*   **H1a**: Wilcoxon Signed-Rank sobre métricas técnicas en las 6 semillas.
*   **H1b**: Mann-Whitney U para evaluar las puntuaciones Likert 1-5 de comprensión.
*   **H1c**: t-Student apareada / Wilcoxon sobre la consistencia de reportes mediante la Rúbrica 5D.
*   **H1d**: t-Student apareada (within-subjects) sobre los tiempos de interpretación de las alertas.

### 4.4 Baselines Comparativos

*   **B1: Isolation Forest Individual**: Representa el detector univariado/multivariado estándar de la industria.
*   **B2: Ensemble sin ECOD**: Aísla y cuantifica la ganancia en reducción de falsos positivos que aporta ECOD.
*   **B3: XGBoost Supervisado**: Actúa como límite superior teórico para evaluar el castigo en rendimiento al pasar a un entorno no supervisado.
*   **B4: LLM directo sin RAG y sin SHAP**: Evalúa la tasa de alucinación semántica y numérica en reportes libres.

### 4.5 Protocolo de Usabilidad con Grupos Cerrados

#### Perfil de Testers Seleccionados
La muestra se limita estrictamente a un **grupo cerrado de testers con conocimiento especializado en el área** (N = 15 a N = 27):
1.  **Estudiantes avanzados o egresados**: Noveno ciclo en adelante de Ingeniería de Sistemas, Ingeniería Industrial o Agronomía, con formación académica aprobada en gestión de calidad, auditoría o administración logística.
2.  **Profesionales activos**: Auditores internos de sistemas, supervisores de operaciones, inspectores de calidad fitosanitaria o analistas de TI en agroexportadoras peruanas.

#### Procedimiento de la Sesión (~45 Minutos)
1.  **Firma del Consentimiento Informado** (5 min): Registro del acuerdo de confidencialidad y autorización de telemetría de interacción.
2.  **Tutorial Guiado** (5 min): Inducción interactiva con una alerta de prueba.
3.  **Bloque 1 - Condición A o B** (12 min): Evaluación de 10 alertas bajo una de las dos condiciones operativas. El sistema registra silenciosamente el tiempo en milisegundos desde que abre la alerta hasta que el tester envía su veredicto.
4.  **Descanso y Tarea Distractora** (5 min): Rompe el efecto de aprendizaje de la primera condición.
5.  **Bloque 2 - Condición Contrapuesta** (12 min): Evaluación de las alertas bajo la condición restante.
6.  **Cuestionario SUS + Preguntas Abiertas** (6 min): El tester evalúa la escala Likert de usabilidad SUS (10 ítems standard) y responde preguntas sobre la utilidad cualitativa de las explicaciones SHAP y narrativas RAG.
7.  **Agradecimiento y Cierre** (1 min).
