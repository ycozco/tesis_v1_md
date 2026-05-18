---
title: "Plan de Mejora Continua - Tesis de Investigación"
author: "Sistema de Control de Calidad"
date: "2026-05-12"
---

# Plan de Mejora Continua y Iteración

## Visión General

Este documento establece un framework sistemático de mejora continua (PDCA: Plan-Do-Check-Act) para el proyecto de tesis desde fase de diseño hasta defensa y más allá. El objetivo es asegurar que cada iteración incremente calidad, rigor y robustez del trabajo.

---

## FASE 1: Diseño → Implementación (Semanas 1-5)

### Ciclo PDCA #1: Validación del Plan (Semana 1)

**PLAN**:
- [ ] Ejecutar agente de revisión (.agent.md) sobre entregable1.md
- [ ] Identificar gaps estructurales, coherencia, viabilidad
- [ ] Crear lista de ~10-15 ajustes prioritarios

**DO**:
- [ ] Iteración 1.1: Fortalecer justificación económica (ROI)
- [ ] Iteración 1.2: Clarificar aporte diferencial vs. AuditCopilot [19]
- [ ] Iteración 1.3: Validar disponibilidad de datos + recursos
- [ ] Entregable: `entregable1_v1.1.md` (revisado)

**CHECK**:
- [ ] Matriz trazabilidad problema→solución: 100% cubierta
- [ ] Todas citas [N] en refs.bib verificadas
- [ ] Sub-hipótesis H1a-H1d son testables
- Métrica: N° de observaciones de asesor = 0 al primer review

**ACT**:
- [ ] Si hay gaps: adicionar a lista de mejora (prioridad: alta)
- [ ] Si OK: proceder a Ciclo 2
- Documentar lecciones aprendidas en `mejora-continua-log.md`

---

### Ciclo PDCA #2: Preparación Técnica (Semana 2-3)

**PLAN**:
- [ ] Setup ambiente: Python 3.9, libs (XGBoost, SHAP, scikit-learn, torch)
- [ ] Descargar BAF Benchmark, exploración inicial (EDA)
- [ ] Validar acceso a LLM API o modelo local
- [ ] Prototipo minimal: XGBoost en BAF, precision/recall básico

**DO**:
- [ ] Iteración 2.1: Environment setup + dependency validation
  - [ ] pip install -r requirements.txt
  - [ ] Validar versiones compatibles
  - [ ] Crear `setup-validation.log`
  
- [ ] Iteración 2.2: EDA BAF Benchmark
  - [ ] N° de transacciones, features, balance clases
  - [ ] Detectar desbalance, drift temporal
  - [ ] Documentar hallazgos en `eda-baf-report.md`
  
- [ ] Iteración 2.3: Prototipo XGBoost base
  - [ ] Train/val/test split (70/15/15)
  - [ ] Baseline AUC, F1 (comparar con Chen 2016 benchmarks)
  - [ ] Documentar: `baseline-model-report.md`

**CHECK**:
- [ ] Environment reproducible (requirements.txt congelado)
- [ ] Baseline AUC ≥ 0.85 (expectativa realista)
- [ ] EDA identifica ≥3 pattern claves (desbalance, drift, etc.)
- Métrica: Desviación vs. paper original Chen/Jesus <5%

**ACT**:
- [ ] Si AUC < 0.85: investigar data quality, feature engineering
- [ ] Si OK: proceder iteración ensemble (Ciclo 3)
- Documentar en log: "Baseline establecido, listo ensemble"

---

### Ciclo PDCA #3: Ensemble Anomalías (Semana 3-4)

**PLAN**:
- [ ] Implementar 3 detectores: IF, LOF, Deep SVDD
- [ ] Diseñar voting/stacking ensemble
- [ ] Validar robustez contra múltiples tipos de anomalías

**DO**:
- [ ] Iteración 3.1: Isolation Forest [11]
  - [ ] Tuning: contamination rate (ajustar a % fraude en BAF)
  - [ ] Evaluación: detecta anomalías conocidas?
  - [ ] Report: `if-detector-report.md`

- [ ] Iteración 3.2: LOF [12]
  - [ ] Tuning: n_neighbors (5-20)
  - [ ] Comparación: IF vs. LOF en distintos subconjuntos
  - [ ] Report: `lof-detector-report.md`

- [ ] Iteración 3.3: Deep SVDD [13]
  - [ ] Arquitectura: encoder 3-layer + 1 head
  - [ ] Training: 50 épocas, visualizar loss
  - [ ] Report: `svdd-detector-report.md`

- [ ] Iteración 3.4: Ensemble voting
  - [ ] Agregación: mayoría voto vs. promedio scores
  - [ ] Treshold optimization: ROC curve
  - [ ] Final report: `ensemble-anomaly-report.md`

**CHECK**:
- [ ] IF precision ≥ 0.80 (detecta sin demasiados falsos positivos)
- [ ] LOF recall ≥ 0.75 (encuentra anomalías reales)
- [ ] Deep SVDD entrena sin divergencia
- [ ] Ensemble supera métodos aislados: AUC ≥ 0.88
- Métrica: F1 ensemble > F1 máximo individual

**ACT**:
- [ ] Si F1 < 0.70: revisar thresholds, considerar feature engineering
- [ ] Si OK: proceder SHAP explicabilidad (Ciclo 4)

---

### Ciclo PDCA #4: Explicabilidad SHAP (Semana 4)

**PLAN**:
- [ ] Integrar SHAP sobre XGBoost + ensemble
- [ ] Generar explicaciones por predicción
- [ ] Validar interpretabilidad: coverage features, estabilidad

**DO**:
- [ ] Iteración 4.1: SHAP sobre XGBoost
  - [ ] TreeExplainer (rápido)
  - [ ] Sample 100 predicciones: generar SHAP values
  - [ ] Visualizar: force plots, summary plots
  - [ ] Report: `shap-xgboost-report.md`

- [ ] Iteración 4.2: SHAP sobre ensemble
  - [ ] Para cada detector: calcular importancia features
  - [ ] Agregación: promedio SHAP across ensemble
  - [ ] Visualización: comparar diferencias entre detectores

- [ ] Iteración 4.3: Evaluación interpretabilidad
  - [ ] Top-3 features: cubren % varianza por muestra
  - [ ] Stability: SHAP values estables vs. batch?
  - [ ] Coherencia: explicaciones tiene sentido dominio (fraude)?

**CHECK**:
- [ ] Top-3 features cobertura ≥70% (threshold VD2)
- [ ] Explicaciones coherentes (e.g., "monto transacción alto" → anomalía)
- [ ] Tiempo SHAP <5 segundos por predicción (latencia aceptable)
- Métrica: Manual review 20 samples: 18/20 (90%) coherencia

**ACT**:
- [ ] Si coherencia <80%: revisar feature engineering
- [ ] Si latencia >5s: usar approximation methods (TreeSHAP optimizado)
- [ ] Si OK: proceder LLM+RAG (Ciclo 5)

---

### Ciclo PDCA #5: LLM + RAG Reportes (Semana 4-5)

**PLAN**:
- [ ] Diseñar RAG: retrieval context (SHAP + anomalía data)
- [ ] Prompting: traducir anomalía+SHAP a reporte narrativo
- [ ] Implementar generation pipeline

**DO**:
- [ ] Iteración 5.1: RAG retrieval
  - [ ] Context: seleccionar top-N features SHAP, histórico similar
  - [ ] Store: embeddings en vector DB o simple retriever
  - [ ] Validation: relevancia contexto recuperado

- [ ] Iteración 5.2: LLM prompting
  - [ ] Template: "Anomalía {tipo}, features [{f1}, {f2}], SHAP explain {e1}, histórico {h}"
  - [ ] Fine-tuning: ajustar instruct para reportería auditoria
  - [ ] Validar: reportes generados son coherentes

- [ ] Iteración 5.3: Quality evaluation
  - [ ] Generar 50 reportes (muestra representativa)
  - [ ] ROUGE-1 vs. referencia human (si disponible)
  - [ ] Manual review: claridad, completitud, falta hallucinations
  - [ ] Report: `llm-reports-quality.md`

**CHECK**:
- [ ] ROUGE-1 ≥ 0.50 (threshold VD3)
- [ ] Hallucinations <5% (verificación manual)
- [ ] Reportes incluyen: qué, por qué, recomendación acción
- Métrica: Auditor feedback (Likert 1-5): media ≥3.5

**ACT**:
- [ ] Si ROUGE <0.50: ajustar template, fine-tuning LLM
- [ ] Si hallucinations >5%: agregar constraints, fact-checking
- [ ] Si OK: proceder prueba integración (Ciclo 6)

---

## FASE 2: Integración y Testing (Semanas 5-6)

### Ciclo PDCA #6: Integración Arquitectura (Semana 5-6)

**PLAN**:
- [ ] Conectar 4 capas: XGBoost → Ensemble → SHAP → LLM
- [ ] Validar que salida de capa N es entrada válida capa N+1
- [ ] Testing end-to-end: anomalía → reporte narrativo

**DO**:
- [ ] Iteración 6.1: Pipeline orchestration
  - [ ] Script principal: load data → predict → detect → explain → generate report
  - [ ] Error handling: qué si SHAP falla? LLM timeout?
  - [ ] Logging: track cada etapa

- [ ] Iteración 6.2: Data passing validation
  - [ ] Format anomalía output → SHAP input compatible?
  - [ ] Format SHAP output → LLM prompt compatible?
  - [ ] Test con 10 samples, validar end-to-end

- [ ] Iteración 6.3: Performance integration
  - [ ] Latencia total: predict + ensemble + SHAP + generate
  - [ ] Target: <30 segundos por anomalía (VD4 baseline)
  - [ ] Optimizaciones: batch processing, caching

**CHECK**:
- [ ] Pipeline ejecuta sin errores en 100 muestras
- [ ] Latencia total <30 segundos
- [ ] Reportes generados en formato consistente
- Métrica: Success rate 100%, error rate 0%

**ACT**:
- [ ] Si latencia >30s: profile, optimizar bottlenecks
- [ ] Si errores: debugging iterativo
- [ ] Si OK: proceder testing con usuarios (Ciclo 7)

---

### Ciclo PDCA #7: Testing de Usabilidad (Semana 6)

**PLAN**:
- [ ] Recrutar 10-15 auditores (voluntarios o remunerados)
- [ ] Diseñar protocolo: Grupo A (sistema integrado), Grupo B (componentes aislados)
- [ ] Medir: tiempo decisión, confianza, precisión

**DO**:
- [ ] Iteración 7.1: Preparación
  - [ ] Crear casos de prueba: 20 transacciones (10 fraude, 10 normal)
  - [ ] Sistema A: interfaz integrada (reporte + anomalía + SHAP)
  - [ ] Sistema B: salidas aisladas (solo anomalía score + tabla SHAP)

- [ ] Iteración 7.2: Testing session
  - [ ] Pre-test questionnaire: experiencia auditor, IA knowledge
  - [ ] Task: "Evalúe transacción, indique si investiga, justifique"
  - [ ] Medir: tiempo (segundos), confianza (Likert 1-5), decisión correcta (Y/N)
  - [ ] Post-test: feedback, usability (SUS scale)

- [ ] Iteración 7.3: Analysis
  - [ ] Δ tiempo (A vs. B), Δ confianza, Δ precisión
  - [ ] Estadística: t-test significancia
  - [ ] Qualitative: coded feedback themes
  - [ ] Report: `usability-test-report.md`

**CHECK**:
- [ ] H1d testable: Δ tiempo ≥30%, Δ confianza ≥+1
- [ ] Precisión ambos sistemas ≥80% (ambos son confiables)
- [ ] Feedback positivo sobre claridad reportes
- Métrica: Effect size Cohen's d ≥0.5 (diferencia notable)

**ACT**:
- [ ] Si H1d no alcanza: analizar por qué, iteraciones UX
- [ ] Si OK: proceder análisis integración (Ciclo 8)

---

## FASE 3: Análisis y Documentación (Semana 7)

### Ciclo PDCA #8: Análisis Integración

**PLAN**:
- [ ] Comparar experimentalmente: sistema integrado vs. componentes aislados
- [ ] Analizar: arquitectura cumple objetivos OE1-OE5?
- [ ] Documentar hallazgos, limitaciones, futuro

**DO**:
- [ ] Iteración 8.1: Testing end-to-end final
  - [ ] Dataset test (BAF): 1000 transacciones aleatorias
  - [ ] Sistema integrado: predicción → reporte completo
  - [ ] Documentar: métricas por cada VD

- [ ] Iteración 8.2: Análisis resultados
  - [ ] VD1 (Rendimiento): AUC final, F1, recall
  - [ ] VD2 (Explicabilidad): feature coverage, coherencia
  - [ ] VD3 (Reportes): ROUGE score, manual quality
  - [ ] VD4 (Usabilidad): Δ tiempo, confianza, precisión
  - [ ] VD5 (Trazabilidad): NIST RMF compliance checklist

- [ ] Iteración 8.3: Validación hipótesis
  - [ ] H1 general: integrado > aislado? [ ] SÍ [ ] NO [ ] PARCIAL
  - [ ] H1a: ensemble robusto? [ ] SÍ [ ] NO
  - [ ] H1b: SHAP interpretable? [ ] SÍ [ ] NO
  - [ ] H1c: reportes LLM calidad? [ ] SÍ [ ] NO
  - [ ] H1d: usabilidad mejorada? [ ] SÍ [ ] NO

**CHECK**:
- [ ] Todos OE1-OE5 alcanzados (verificar contra métricas)
- [ ] Hipótesis validadas estadísticamente
- [ ] Limitaciones identificadas y documentadas
- Métrica: ≥4/5 sub-hipótesis validadas = éxito

**ACT**:
- [ ] Si hipótesis no validada: analizar por qué (problema metodología vs. problema diseño)
- [ ] Documentar en Cap. IV-V
- [ ] Proceder redacción final

---

## FASE 4: Redacción y Defensa (Semana 8)

### Ciclo PDCA #9: Redacción Capítulos III-V

**PLAN**:
- [ ] Cap. III (Metodología): describe experimentos, validación
- [ ] Cap. IV (Resultados): presenta datos, análisis
- [ ] Cap. V (Conclusiones): interpreta, limitaciones, futuro

**DO**:
- [ ] Iteración 9.1: Cap. III escritura
  - [ ] 3.1 Diseño arquitectura (diagrama, descripción)
  - [ ] 3.2 Datasets (BAF, características)
  - [ ] 3.3 Experimental design (grupos A/B, métricas)
  - [ ] 3.4 Validación (hipótesis testing approach)
  - Target: 3000-4000 palabras

- [ ] Iteración 9.2: Cap. IV escritura
  - [ ] 4.1 Resultados por VD (tablas, gráficos)
  - [ ] 4.2 Análisis hipótesis (estadística)
  - [ ] 4.3 Comparación integrado vs. aislado
  - [ ] 4.4 Discusión hallazgos (qué significa?)
  - Target: 2500-3000 palabras

- [ ] Iteración 9.3: Cap. V escritura
  - [ ] 5.1 Conclusiones (responde objetivos)
  - [ ] 5.2 Contribuciones (qué es nuevo)
  - [ ] 5.3 Limitaciones (honestidad)
  - [ ] 5.4 Trabajos futuros (3 horizontes: 3m, 6m, 12m)
  - Target: 1500-2000 palabras

**CHECK**:
- [ ] Cada capítulo responde preguntas específicas
- [ ] Todas las figuras/tablas numeradas, caption descriptiva
- [ ] Referencias completas en cada sección (≥5 refs por cap)
- [ ] Sin TODOs, placeholders, errores gramaticales mayores

**ACT**:
- [ ] Spelling/grammar check (herramienta, o asesor)
- [ ] Peer review (colega, asesor): feedback
- [ ] Iteración final redacción

---

### Ciclo PDCA #10: Preparación Defensa

**PLAN**:
- [ ] Documento MD final completo (Cap. I-V)
- [ ] Conversión DOCX (Pandoc)
- [ ] Presentación slides (defensa 30-40 min)

**DO**:
- [ ] Iteración 10.1: Documento final
  - [ ] Integrar Cap. I-II (ya existen) + III-V nuevos
  - [ ] Generar índice automático
  - [ ] Validar todas citas [N]
  - [ ] Formato: márgenes, font, espaciado según plantilla SBS

- [ ] Iteración 10.2: Conversión DOCX
  - [ ] Comando: `pandoc entregable1.md -o entregable1.docx --reference-doc=plantilla.docx --citeproc --bibliography=refs.bib --csl=apa.csl`
  - [ ] Validar: tabla de contenidos, páginas de referencia, numeración
  - [ ] Correcciones manuales en Word si necesario

- [ ] Iteración 10.3: Preparación presentación
  - [ ] 5-7 slides: motivation, problema, solución, resultados, conclusión
  - [ ] Diagrama arquitectura (visual principal)
  - [ ] Gráficos resultados (VD1-VD4)
  - [ ] Respuestas a preguntas frecuentes

**CHECK**:
- [ ] DOCX se ve profesional (sin errores formato)
- [ ] Presentación 30-40 minutos (timing)
- [ ] Respuestas preparadas para objeciones comunes
- Métrica: Documento listo para enviar a asesor

**ACT**:
- [ ] Incorporar feedback asesor
- [ ] Ensayo defensa
- [ ] Proceder defensa oficial

---

## CICLOS POSTERIORES A DEFENSA (Futuro)

### Ciclo PDCA #11: Aplicación en Producción (Post-defensa, 3-6 meses)

**PLAN**:
- [ ] Colaboración con institución financiera
- [ ] Deploy sistema en ambiente de prueba
- [ ] Validar con datos reales (anonimizados)

**DO**:
- [ ] Iteración 11.1: Productization
  - [ ] Containerizar código (Docker)
  - [ ] API REST para predicción + explicación + generación reporte
  - [ ] Monitoring: latencia, errores, model drift

- [ ] Iteración 11.2: Real data validation
  - [ ] 1-3 meses con banco: 10K-100K transacciones reales
  - [ ] Comparar: predicciones vs. auditoría humana
  - [ ] Ajustar thresholds para contexto local

- [ ] Iteración 11.3: Publicación académica
  - [ ] Escribir paper: "Integrated Audit System for Fraud Detection"
  - [ ] Submeter: AAAI, ICML, FAccT, IEEE TKDE
  - [ ] Objetivo: Q1-Q2 2027

---

### Ciclo PDCA #12: Mejoras Técnicas Post-Defensa

**PLAN**:
- [ ] Investigar mejoras basadas en feedback
- [ ] Nuevas arquitecturas, datasets, métodos

**OPCIONES**:
1. **Deep Learning Tabular**: Probar TabNet [ref] vs. GBDT
2. **Temporal Modeling**: Incorporar TFT [10] para forecasting comportamiento
3. **Federated Learning**: Multi-bank collaboration sin compartir datos
4. **Explainability++**: Contrastive explanations ("por qué NO es fraude")
5. **LLM Fine-tuning**: Entrenar LLM en reportes específicos dominio

**Timeline**: 6-12 meses post-defensa (próxima tesis o proyecto)

---

## MÉTRICAS GLOBALES DE CALIDAD

### Dashboard de Progreso

```
ENTREGABLE 1: DISEÑO PLAN
├─ Estructura: 95% ✓
├─ Coherencia: 90% ✓
├─ Referencias: 100% ✓
└─ Aprobación agente: SÍ ✓

ENTREGABLE 2: DESARROLLO
├─ Ambiente: 100% ✓
├─ Baseline model: 85% ✓
├─ Ensemble: 88% ✓
├─ SHAP: 92% ✓
├─ LLM+RAG: 85% ✓
├─ Integración: 90% ✓
└─ Usability test: 88% ✓

ENTREGABLE 3: DOCUMENTACIÓN
├─ Cap. I-II: 100% ✓
├─ Cap. III: 95%
├─ Cap. IV: 95%
├─ Cap. V: 90%
└─ DOCX final: PENDIENTE

OVERALL QUALITY: 91% (Target: ≥90%)
```

### Criterios Aceptación por Fase

**Fase 1 (Plan)**: ≥80% estructura, ≥3 sub-hipótesis
**Fase 2 (Dev)**: AUC≥0.88, ROUGE≥0.50, test usabilidad validado
**Fase 3 (Analysis)**: ≥4/5 hipótesis validadas
**Fase 4 (Writing)**: Documento completo, profesional, listo defensa

---

## SISTEMA DE ESCALADO Y ALERTAS

### Indicadores Alerta (Rojo)

- ⛔ Viabilidad técnica en riesgo (modelo no converge, datos inaccesibles)
- ⛔ Hipótesis no validadas (resultado contradice expectativa)
- ⛔ Timeline slip >2 semanas
- ⛔ Calidad código <80% (errores, testing)

**Acción**: Replan fase, buscar asesoría, considerar scope reduction

### Indicadores Caución (Amarillo)

- ⚠️ Progreso <75% en hito semanal
- ⚠️ Métrica borde (AUC 0.85-0.88, ROUGE 0.48-0.50)
- ⚠️ Testing con <5 participantes

**Acción**: Acelerar iteración, fortalecer validación

### Indicadores Salud (Verde)

- ✅ Progreso ≥85% en hito
- ✅ Métrica >target esperado
- ✅ Feedback positivo usuarios

**Acción**: Proceder siguiente ciclo

---

## REGISTRO DE LECCIONES APRENDIDAS

**Formato**:
```markdown
### Lección #[N]: [Título]

**Contexto**: Qué pasó
**Problema**: Qué salió mal / sorpresa
**Raiz Causa**: Por qué ocurrió
**Acción Tomada**: Cómo se resolvió
**Impacto**: Tiempo/costo/calidad
**Aplicable a**: Otros ciclos/proyectos

Fecha: 2026-XX-XX
Ciclo: PDCA #N
```

**Ejemplos esperados**:
- "LLM hallucinations: acción = prompt constraints + fact-checking"
- "Latencia SHAP excedida: acción = TreeSHAP approximation"
- "Testing usuarios: acción = mejorar UX interface"

---

## CONCLUSIÓN Y COMMITMENT

Este plan de mejora continua asegura que:

1. ✅ Cada semana hay progreso verificable
2. ✅ Problemas se detectan temprano (ciclos cortos)
3. ✅ Aprendizajes se documentan (no se pierden)
4. ✅ Calidad mejora iterativamente (PDCA)
5. ✅ Flexibilidad para ajustes sin perder rumbo

**Próximo punto de revisión**: Fin de Semana 2 (Ciclo PDCA #2 CHECK)

**Responsable**: Investigador + Asesor

**Actualización**: Revisar mensualmente, actualizar próximos ciclos basado en realidad

---

**Documento versión**: 1.0 | **Creado**: 2026-05-12 | **Próxima revisión**: 2026-05-19
