# CAPÍTULO IV: RESULTADOS Y DISCUSIÓN

> **Estado:** Estructura completa lista — las tablas y gráficos numéricos se completarán tras ejecutar los experimentos E1–E5 (Hito 4 — 2026-06-22).

## 4.1 Resultados Cuantitativos (Predicción y Detección — VD1)

Esta sección presenta las métricas obtenidas por el módulo de predicción tabular y el ensemble de detección de anomalías sobre el conjunto de test del dataset sintético agroexportador (v1.0, 400 registros del período 2025-05-01 a 2025-12-31).

### 4.1.1 Tabla 4.1 — Rendimiento de detección (Experimento E1)

| Método | PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad) | ROC-AUC (Receiver Operating Characteristic Area Under the Curve - Área Bajo la Curva de Característica Operativa del Receptor) | F1 | Precision | Recall | Tiempo inferencia |
|---|---|---|---|---|---|---|
| Isolation Forest individual (baseline B1) | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| LOF (Local Outlier Factor - Factor de Anomalía Local) individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica) individual | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| Ensemble IF (Isolation Forest - Bosque de Aislamiento) + LOF (B2) | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
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

| Métrica | Sistema con SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley) | Sistema sin SHAP | p-value (Mann-Whitney U) |
|---|---|---|---|
| Cobertura top-3 (mediana) | _pendiente_ | N/A | — |
| Cobertura top-5 (mediana) | _pendiente_ | N/A | — |
| Consistencia ρ (Spearman) | _pendiente_ | N/A | — |
| Claridad operativa (Likert 1–5, promedio) | _pendiente_ | _pendiente_ | _pendiente_ |

### 4.2.2 Tabla 4.4 — Calidad de reportes generados (Experimento E3)

| Dimensión | LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño) + RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación) (propuesto) | LLM libre (control) | Kappa Cohen | p-value |
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

| Atributo | Esta tesis | AuditCopilot (Kadir et al., 2025) | Park (2024) | AuditMAI (Waltersdorfer et al., 2024) | Almalki & Masud (2025) / JRFM (2025) |
|---|---|---|---|---|---|
| Predicción tabular GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) | XGBoost + LightGBM | No reportada | No (solo LLMs (Large Language Models - Modelos de Lenguaje de Gran Tamaño)) | No | Stacking GBDT |
| Ensemble de detección | IF + LOF + ECOD | Parcial | No | No | No |
| Explicabilidad SHAP estructurada | TreeSHAP top-k | No | No | No | SHAP |
| Generación LLM bajo RAG | RAG anclado en SHAP | LLM libre | Multi-agente | No | No |
| Restricción anti-alucinación | Sí (validación numérica posterior) | No documentada | No | N/A | N/A |
| PR-AUC reportado | _pendiente_ | No reporta | No reporta | No | > 0.90 |
| Dominio | Agroexportador peruano | Asientos contables | S&P 500 | Auditoría de IA | Fraude financiero |
| Contexto regulatorio | D.S. 115-2025-PCM + NIST AI RMF | No especificado | No | No | No |
| Evaluación con usuarios | Sí (N ≥ 15) | No | No | No | No |
| Dataset abierto disponible | Sí (CC BY 4.0) | No | No | N/A | Parcial / No |

**Lectura del cruce 1**:
- La cobertura modular del sistema propuesto (cuatro capas con restricción anti-alucinación) es estrictamente mayor que cualquier trabajo individual de la literatura revisada.
- Los trabajos más cercanos en cobertura metodológica (Almalki & Masud, 2025; JRFM, 2025) combinan GBDT y SHAP en fraude financiero, pero carecen de detección no supervisada, módulo LLM y contexto regulatorio.
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
| clima | _pendiente_ | La caída del recall en clima puede explicarse por sparsity y baja densidad local, consistente con limitaciones de LOF reportadas por Breunig et al. (2000). | Agregar densidad estacional regional |
| logistica | _pendiente_ | Anomalía compuesta (dos condiciones) — IF puede subestimar | Reforzar con regla determinista complementaria |
| calidad | _pendiente_ | Pocas instancias inyectadas (10%) | Subir a 15% en v1.1 si recall < 0.6 |

### 4.4.7 Interpretación conjunta teórica: ¿Por qué el sistema propuesto es superior?

La superioridad del sistema integrado no se justifica únicamente por la ganancia empírica en métricas como el PR-AUC, sino por fundamentos teóricos subyacentes a cada componente de su arquitectura:

1. **¿Por qué IF + LOF + ECOD mejora la detección (PR-AUC)?**
   La combinación mediante ensemble mitiga los puntos ciegos de cada algoritmo individual. *Isolation Forest* (IF) es altamente eficiente para aislar anomalías globales en espacios de alta dimensión, pero falla al identificar anomalías contextuales en vecindarios densos. *Local Outlier Factor* (LOF) captura estas variaciones de densidad local (como fluctuaciones sutiles de precios por zona), aunque es sensible a la escasez de datos (sparsity) en ciertas regiones. Al incorporar *ECOD*, que estima de manera no paramétrica la función de distribución acumulada empírica, el ensemble adquiere la capacidad de detectar anomalías en las colas de distribución (ej. eventos climáticos extremos) sin depender de hiperparámetros complejos de vecindad. Esta triangulación algorítmica crea una frontera de decisión mucho más robusta frente al desbalance extremo característico del sector agroexportador.

2. **¿Por qué SHAP mejora la comprensión operativa?**
   A diferencia de las explicaciones heurísticas, *SHAP* (SHapley Additive exPlanations) se fundamenta teóricamente en la teoría de juegos cooperativos (Lundberg & Lee, 2017). SHAP asigna a cada característica (feature) un valor de contribución marginal exacta hacia la predicción final, garantizando consistencia y aditividad local. Para un supervisor agroexportador, esto transforma una alerta de "caja negra" ("Anomalía detectada con score 0.85") en un diagnóstico estructurado y trazable ("Anomalía impulsada en un 40% por la temperatura atípica y en un 25% por el retraso logístico"). Al cuantificar el "por qué", se reduce la carga cognitiva del usuario, elevando significativamente los puntajes de claridad empírica.

3. **¿Por qué RAG reduce la ambigüedad y alucinaciones del LLM?**
   Los Grandes Modelos de Lenguaje (LLMs) propenden a la alucinación cuando se basan exclusivamente en su memoria paramétrica, especialmente en dominios técnicos estrictos. La arquitectura *Retrieval-Augmented Generation* (RAG) resuelve este problema inyectando un contexto determinista (los valores numéricos de SHAP y los metadatos exactos de la transacción) directamente en el prompt del LLM (Lewis et al., 2020). Al restringir semánticamente el espacio de generación del modelo para que actúe únicamente como un "sintetizador de evidencias inyectadas" y no como un "creador de respuestas libres", se elimina la ambigüedad. Esto asegura que el reporte generado mantenga total fidelidad (consistencia numérica) con el evento disparador, cumpliendo con las exigencias de trazabilidad documental regulatoria.

> **Lectura integrada (a completar con resultados reales)**: Si los cinco cruces (Tabla 4.8–4.12) muestran consistencia direccional con las predicciones del Capítulo I, esta tesis sostiene que la arquitectura propuesta no solo es novedosa por su integración modular, sino también teórica y empíricamente superior bajo las condiciones evaluadas. En caso de inconsistencias, se documentan en §4.5 (Limitaciones de los resultados) y se proponen líneas de mejora en §5.3 (Trabajo futuro).

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
