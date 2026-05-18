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
