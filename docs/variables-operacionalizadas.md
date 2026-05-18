# OPERACIONALIZACIÓN FORMAL DE VARIABLES
## Hito 1 — Plan de Revisión Académica Exhaustiva
## Fecha de cierre: 2026-05-27 | Estado: ✅ Documento base completo

> Este documento traduce las variables del Capítulo I §1.5 a una tabla operacional formal con definición conceptual, definición operacional, fórmula o protocolo de medición, instrumento, rango, criterio de aceptación, nivel de medición y prueba estadística asociada.
>
> **Uso**: referencia obligatoria al ejecutar los experimentos E1–E5 (Capítulo III §3.3) y al reportar resultados en el Capítulo IV.

---

## 1. Variable Independiente (VI)

### VI: Tipo de sistema de supervisión operativa

| Atributo | Especificación |
|---|---|
| **Definición conceptual** | Configuración arquitectónica del sistema que combina o aísla los cuatro módulos (predicción tabular, detección de anomalías, explicabilidad SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley), reporte LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)). |
| **Definición operacional** | Variable categórica binaria que distingue dos condiciones experimentales: sistema integrado (todas las capas activas y comunicadas) vs. sistema con componentes aislados (cada módulo opera de manera independiente, sin paso de evidencia entre capas). |
| **Operacionalización (valores)** | VI1 = "integrado" (pipeline de 4 capas con paso de evidencias); VI2 = "aislado" (módulos independientes con salidas técnicas separadas). |
| **Instrumento de manipulación** | Configuración del archivo `src/pipeline.py` mediante el parámetro `mode ∈ {"integrated", "isolated"}`. |
| **Nivel de medición** | Nominal dicotómica. |
| **Control de confusores** | Mismo dataset, misma división temporal, mismas semillas, mismos modelos por capa, mismo entorno computacional. |

---

## 2. Variables Dependientes (VD)

### VD1: Rendimiento de detección

| Atributo | Especificación |
|---|---|
| **Definición conceptual** | Capacidad del sistema de identificar correctamente registros anómalos minimizando falsos positivos y falsos negativos. |
| **Definición operacional** | Conjunto de métricas estándar de clasificación binaria aplicadas sobre el conjunto de test cronológicamente posterior al training. |
| **Indicadores y fórmulas** | (a) PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad) = área bajo la curva precisión-recall; (b) ROC-AUC (Receiver Operating Characteristic Area Under the Curve - Área Bajo la Curva de Característica Operativa del Receptor) = área bajo la curva ROC; (c) F1 = 2·(P·R)/(P+R) en el umbral óptimo; (d) Precision = TP/(TP+FP); (e) Recall = TP/(TP+FN). |
| **Métrica principal** | **PR-AUC**, por ser robusta ante desbalance de clases (~12% de anomalías). |
| **Instrumento** | `sklearn.metrics.precision_recall_curve`, `average_precision_score`, `roc_auc_score`, `f1_score`. |
| **Rango** | [0.0, 1.0] para todas las métricas. |
| **Criterio de aceptación** | El sistema integrado debe superar al baseline B1 (Isolation Forest individual) en PR-AUC con diferencia estadísticamente significativa (p < 0.05) y tamaño de efecto Hedges' g ≥ 0.5, o justificar rendimiento equivalente con mayor trazabilidad. |
| **Nivel de medición** | Razón. |
| **Prueba estadística** | Wilcoxon signed-rank (apareada, no paramétrica) sobre 6 semillas. |
| **Sub-hipótesis vinculada** | H1a |
| **Experimento vinculado** | E1 |

### VD2: Calidad de explicabilidad

| Atributo | Especificación |
|---|---|
| **Definición conceptual** | Grado en que las explicaciones SHAP asociadas a una alerta permiten a un supervisor identificar las variables operativas determinantes y su dirección de impacto. |
| **Definición operacional** | Tres indicadores combinados: (a) cobertura top-k, (b) consistencia entre alertas similares, (c) claridad percibida por evaluador. |
| **Indicador (a) Cobertura top-k SHAP** | Porcentaje de la magnitud total absoluta del score explicada por las k variables con |SHAP| más alto. **Fórmula**: cobertura_k = Σ_{i ∈ top-k} \|φᵢ\| / Σ_j \|φⱼ\|. Se reporta con k=3 y k=5. |
| **Indicador (b) Consistencia** | Coeficiente de similitud (Spearman ρ) entre los rankings de variables SHAP de alertas con etiqueta y tipo de anomalía idéntico (≥10 pares por tipo). |
| **Indicador (c) Claridad operativa** | Escala Likert 1 (muy poco claro) – 5 (muy claro) respondida por evaluadores tras leer la alerta + vector SHAP top-5. |
| **Instrumento** | Librería `shap` (TreeSHAP), cuestionario post-alerta en formulario web propio. |
| **Rango** | Cobertura: [0, 100%]; Consistencia: [-1, 1]; Likert: {1, 2, 3, 4, 5}. |
| **Criterio de aceptación** | Cobertura top-5 ≥ 80% en al menos 70% de alertas; consistencia ρ ≥ 0.6 para alertas del mismo tipo; Likert claridad ≥ 4.0 promedio. |
| **Nivel de medición** | (a) razón, (b) intervalo, (c) ordinal. |
| **Prueba estadística** | Mann-Whitney U sobre Likert claridad (SHAP vs. sin SHAP); estadística descriptiva con IC95% para cobertura y consistencia. |
| **Sub-hipótesis vinculada** | H1b |
| **Experimento vinculado** | E2 |

### VD3: Calidad de reportes generados

| Atributo | Especificación |
|---|---|
| **Definición conceptual** | Grado en que los reportes generados por el módulo LLM+RAG son completos, consistentes con la evidencia, accionables y trazables. |
| **Definición operacional** | Rúbrica operativa de cinco dimensiones evaluada por dos revisores independientes; complementada con ROUGE cuando exista referencia humana. |
| **Indicador (a) Completitud** | Presencia de los siete campos requeridos en el reporte: dato de origen, modelo, score, umbral, explicación SHAP, fuente recuperada por RAG, recomendación. Escala 1 (falta ≥3) – 5 (todos presentes). |
| **Indicador (b) Consistencia numérica** | Coincidencia entre los valores numéricos del reporte y los outputs del sistema. Escala 1 (≥1 error numérico) – 5 (sin errores). |
| **Indicador (c) Accionabilidad** | Presencia de una recomendación operativa específica y verificable. Escala 1 (ninguna) – 5 (acción clara y operativa). |
| **Indicador (d) Coherencia textual** | Calidad gramatical y lógica del texto. Escala 1 (≥3 errores graves) – 5 (sin errores). |
| **Indicador (e) Correspondencia con evidencias** | Cada afirmación del reporte tiene soporte en SHAP/score/fuente. Escala 1 (afirmaciones sin soporte) – 5 (toda afirmación con soporte). |
| **Instrumento** | Formulario de evaluación con 5 ítems × 5 puntos; protocolo de doble revisor independiente; cálculo de Kappa de Cohen para acuerdo inter-evaluador. |
| **Adicional** | ROUGE-1, ROUGE-L cuando se disponga de un reporte de referencia escrito por el asesor o un experto agroexportador (≥10 reportes de referencia). |
| **Rango** | Cada dimensión: {1, 2, 3, 4, 5}; Promedio total: [1.0, 5.0]; ROUGE: [0, 1]. |
| **Criterio de aceptación** | Promedio total ≥ 4.0/5 sobre ≥20 reportes; Kappa de Cohen κ ≥ 0.60 entre revisores; ROUGE-L ≥ 0.40 cuando se calcule. |
| **Nivel de medición** | Ordinal (escalas Likert tratadas como intervalo para análisis paramétrico). |
| **Prueba estadística** | t de Student apareado (o Wilcoxon signed-rank si Shapiro-Wilk rechaza normalidad) comparando RAG vs. sin RAG. |
| **Sub-hipótesis vinculada** | H1c |
| **Experimento vinculado** | E3 |

### VD4: Comprensión y tiempo de decisión del supervisor

| Atributo | Especificación |
|---|---|
| **Definición conceptual** | Eficiencia y calidad cognitiva con que un supervisor operativo interpreta una alerta y emite una decisión, comparando el sistema integrado con componentes aislados. |
| **Definición operacional** | Tres indicadores medidos durante el estudio de usabilidad con N ≥ 15 participantes en diseño within-subject contrabalanceado. |
| **Indicador (a) Tiempo-a-decisión** | Segundos transcurridos desde la apertura de la alerta en la interfaz hasta el envío del veredicto del evaluador. Registro automático en log de la aplicación (`timestamp_decision - timestamp_open`). |
| **Indicador (b) Comprensión de alerta** | Escala Likert 1 (no la comprendí) – 5 (la comprendí completamente) en cuestionario post-tarea. |
| **Indicador (c) Decisión correcta** | Variable binaria: 1 si la clasificación del evaluador coincide con la etiqueta del dataset; 0 en caso contrario. |
| **Instrumento** | Plataforma web propia con tres pantallas: (1) instrucciones, (2) alerta + información disponible según condición, (3) decisión + cuestionario Likert. Cronómetro JavaScript con resolución de milisegundos. |
| **Rango** | (a) ≥ 0 segundos; (b) {1, 2, 3, 4, 5}; (c) {0, 1}. |
| **Criterio de aceptación** | Reducción de tiempo-a-decisión ≥ 20% en condición integrada vs. aislada; comprensión Likert ≥ 4.0; tasa de decisión correcta ≥ 0.80 en condición integrada. |
| **Nivel de medición** | (a) razón, (b) ordinal, (c) nominal. |
| **Prueba estadística** | t de Student apareado (within-subject) sobre tiempo-a-decisión; Wilcoxon signed-rank si rechaza normalidad; McNemar para tasa de decisión correcta. |
| **Sub-hipótesis vinculada** | H1d |
| **Experimento vinculado** | E4 |

### VD5: Trazabilidad documental

| Atributo | Especificación |
|---|---|
| **Definición conceptual** | Grado en que cada alerta producida por el sistema queda documentada con todos los elementos necesarios para reconstruir su origen y justificación. |
| **Definición operacional** | Porcentaje de alertas que contienen los ocho campos obligatorios de trazabilidad en el log estructurado. |
| **Indicador único** | Trazabilidad = (alertas_completas / alertas_totales) × 100. Una alerta se considera completa si presenta los ocho campos: (1) identificador de dato de origen, (2) versión del dataset, (3) modelo aplicado y versión, (4) score numérico, (5) umbral aplicado, (6) vector SHAP top-k, (7) fuente recuperada por RAG (al menos un fragmento), (8) reporte generado en formato Markdown. |
| **Instrumento** | Validador automático `src/evaluate.py::check_traceability(alert)` que retorna 1 si los ocho campos están presentes y no vacíos. |
| **Rango** | [0, 100%]. |
| **Criterio de aceptación** | ≥ 95% de alertas con trazabilidad completa en el sistema integrado. La condición de control (aislado) servirá como referencia: típicamente < 30%. |
| **Nivel de medición** | Razón. |
| **Prueba estadística** | Prueba binomial exacta sobre la proporción; o chi-cuadrado comparando proporciones entre integrado y aislado. |
| **Sub-hipótesis vinculada** | H1 (general — trazabilidad documental como uno de los tres ejes principales). |
| **Experimento vinculado** | E4 (sistema integrado vs. aislado) y E5 (ablation para detectar qué capa aporta más a la trazabilidad). |

---

## 3. Tabla síntesis (visión global)

| VD | Indicador principal | Instrumento | Rango | Criterio aceptación | Prueba | Exp. |
|---|---|---|---|---|---|---|
| VD1 | PR-AUC | sklearn | [0,1] | Superar B1 (p<0.05, g≥0.5) | Wilcoxon signed-rank | E1 |
| VD2 | Cobertura top-5 + Likert claridad | shap + cuestionario | [0,100%] + {1–5} | ≥80% cobertura; ≥4.0 Likert | Mann-Whitney U | E2 |
| VD3 | Rúbrica 5D + ROUGE-L | Doble revisor + rouge | {1–5} promedio | ≥4.0/5; κ≥0.60 | t apareado / Wilcoxon | E3 |
| VD4 | Tiempo-a-decisión + Likert | Plataforma web | ≥0 s; {1–5} | -20% tiempo; ≥4.0 Likert | t apareado | E4 |
| VD5 | % alertas completas | check_traceability | [0,100%] | ≥95% | Binomial exacta | E4, E5 |

---

## 4. Consideraciones de validez

- **Validez de constructo**: cada VD captura la dimensión conceptual declarada en el Capítulo I §1.5. Para mitigar amenazas, VD2 y VD4 usan triangulación (medida objetiva + Likert).
- **Validez interna**: el diseño contrabalanceado y la fijación de semillas controlan los principales confusores. La división temporal de datos previene fuga de información.
- **Validez externa**: limitada por el uso de dataset sintético. Se mitiga documentando rangos plausibles tomados de MIDAGRI/SENAMHI/SENASA.
- **Confiabilidad**: cada experimento se ejecuta con 6 semillas; reportes con doble revisor y Kappa de Cohen.

---

## 5. Trazabilidad inversa: cada indicador apunta a su decisión metodológica

| Decisión | Variable afectada | Justificación |
|---|---|---|
| Usar PR-AUC como métrica principal | VD1 | Robustez ante desbalance (~12% anomalías) |
| Reportar 6 semillas | VD1 | Cuantificar incertidumbre del estimador |
| Doble revisor con Kappa | VD3 | Confiabilidad inter-evaluador exigida en publicación |
| Diseño within-subject | VD4 | Controlar variabilidad inter-participante con N pequeño |
| Validador automático de trazabilidad | VD5 | Reproducibilidad y eliminación de juicio humano |

---

*Documento generado 2026-05-17. Revisar antes de cerrar Hito 2 (dataset).*
