# PLAN DE SIGUIENTES PASOS
## Sistema Integrado de Supervisión Operativa con IA Explicable — Tesis UNSA
## Documento de roadmap operativo · Fecha de creación: 2026-05-17

> **Estado de avance al 2026-05-17**:
> - ✅ Hito 1 (Variables operacionalizadas) cerrado anticipadamente
> - 🟢 Hito 2 (Dataset sintético) — especificación y script listos, pendiente ejecución
> - ⏳ Hitos 3–5 según calendario
>
> **Próxima revisión de este plan**: 2026-05-24 (lunes) — checkup semanal

---

## CALENDARIO MAESTRO HASTA DEFENSA

| Semana | Fechas | Hito principal | Entregable verificable | Estado |
|---|---|---|---|---|
| S1 | 2026-05-17 a 2026-05-23 | Verificación regulatoria + ejecución dataset | (a) Textos SBS/PCM verificados, (b) `data/dataset_agro_sintetico_v1.csv` generado | ⏳ En curso |
| S2 | 2026-05-24 a 2026-05-30 | Búsqueda sistemática gap claim + módulo 1 | (a) `busqueda-sistematica-gap.md` cerrado, (b) `src/module1_prediction.py` funcional | ⏳ |
| S3 | 2026-05-31 a 2026-06-06 | Módulo 2 + Optuna tuning | (a) `src/module2_anomaly.py`, (b) hiperparámetros documentados | ⏳ |
| S4 | 2026-06-07 a 2026-06-13 | Módulo 3 (SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)) + Módulo 4 (LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)) | (a) `src/module3_shap.py`, (b) `src/module4_rag.py` | ⏳ |
| S5 | 2026-06-14 a 2026-06-20 | Pipeline integrado + experimentos E1–E5 | (a) `src/pipeline.py` + `src/evaluate.py`, (b) resultados E1–E3 | ⏳ |
| S6 | 2026-06-21 a 2026-06-27 | Estudio de usabilidad + Cap IV completo | (a) ≥15 sesiones ejecutadas, (b) Cap IV con tablas 4.1–4.12 reales | ⏳ |
| S7 | 2026-06-28 a 2026-07-04 | Cap V + Conclusiones + Anexos B/C cerrados | (a) `50-capitulo5.md` completo, (b) Model Cards llenadas | ⏳ |
| S8 | 2026-07-05 a 2026-07-11 | Revisión asesor + correcciones | (a) Revisión integral, (b) errata corregida | ⏳ |
| S9 | 2026-07-12 a 2026-07-18 | Defensa | Sustentación pública | ⏳ |
| S10+ | Post-defensa | Paper de conferencia | Sometimiento a CLEI 2026 o IEEE LATAM | ⏳ |

---

## DETALLE POR HITO

### Hito 2 — Dataset Sintético Agroexportador (cierre: 2026-06-01)

**Estado**: 🟢 Adelantado — especificación y script listos.

| # | Tarea | Comando / Acción | Responsable | Fecha límite |
|---|---|---|---|---|
| 2.1 | Instalar dependencias | `pip install -r requirements.txt` | Yoset | 2026-05-19 |
| 2.2 | Generar v1.0 del dataset | `py src/generate_synthetic_dataset.py --n 2000 --seed 42 --out data/dataset_agro_sintetico_v1.csv` | Yoset | 2026-05-20 |
| 2.3 | Validar distribuciones | Notebook: histograma por variable + comparación con rangos del Datasheet | Yoset | 2026-05-22 |
| 2.4 | Verificar inyección de anomalías | Notebook: porcentaje real por tipo vs. esperado | Yoset | 2026-05-22 |
| 2.5 | Versionar en Git (LFS) | `git lfs track "*.csv"; git add data/...` | Yoset | 2026-05-23 |
| 2.6 | Publicar metadata en Anexo C | Actualizar tabla §C.2 con conteos reales | Yoset | 2026-05-24 |

### Hito 3 — Implementación de los 4 módulos (cierre: 2026-06-15)

| # | Módulo | Archivo | Bibliotecas clave | Test mínimo |
|---|---|---|---|---|
| 3.1 | Predicción | `src/module1_prediction.py` | xgboost, lightgbm, optuna | Acepta CSV → produce score 0–1 por fila |
| 3.2 | Detección anomalías | `src/module2_anomaly.py` | pyod (IF (Isolation Forest - Bosque de Aislamiento), LOF (Local Outlier Factor - Factor de Anomalía Local), ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica)) | Devuelve score ensemble y flag binario |
| 3.3 | Explicabilidad | `src/module3_shap.py` | shap (TreeExplainer) | Devuelve vector SHAP top-5 por alerta |
| 3.4 | Reportes LLM+RAG | `src/module4_rag.py` | anthropic, rank-bm25, sentence-transformers | Devuelve reporte markdown anclado en SHAP |
| 3.5 | Pipeline integrado | `src/pipeline.py` | orquesta 3.1–3.4 con paso de evidencias | end-to-end sobre dataset v1.0 |
| 3.6 | Evaluación | `src/evaluate.py` | sklearn.metrics, statsmodels, pingouin | Calcula E1–E5 y exporta tablas Cap IV |

### Hito 4 — Experimentos E1–E5 (cierre: 2026-06-22)

| # | Experimento | Variable contrastada | Salida esperada | Sub-hipótesis |
|---|---|---|---|---|
| E1 | Rendimiento de detección | PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad), F1 ensemble vs. baselines | Tabla 4.1 + Wilcoxon | H1a |
| E2 | Aporte de SHAP | Cobertura top-k + Likert | Tabla 4.3 | H1b |
| E3 | Aporte de RAG | Rúbrica 5D + ROUGE-L | Tabla 4.4 | H1c |
| E4 | Sistema integrado vs. aislado | Tiempo + Likert + trazabilidad | Tablas 4.5 y 4.6 | H1d + H1 |
| E5 | Ablation (E5a–E5d) | Contribución por capa | Tabla 4.7 | Diagnóstico de causas |

### Hito 5 — Cierre del documento de tesis (cierre: 2026-07-07)

| # | Tarea | Archivo afectado |
|---|---|---|
| 5.1 | Cap V con conclusiones derivadas de resultados reales | `docs/50-capitulo5.md` |
| 5.2 | Conclusiones ES/EN actualizadas | `docs/60-conclusiones.md` |
| 5.3 | Anexo B Model Cards con métricas reales | `docs/A2-anexo-modelcards.md` |
| 5.4 | Anexo C Datasheet con conteos reales | `docs/A3-anexo-datasheet.md` |
| 5.5 | Resumen y abstract con números reales | `docs/01-resumen.md` |
| 5.6 | Verificación final integridad refs.bib | `config/refs.bib` + auditoría |
| 5.7 | Búsqueda sistemática cerrada | `docs/busqueda-sistematica-gap.md` |

---

## VERIFICACIÓN REGULATORIA URGENTE (Bloque crítico semana 1)

| # | Acción | Fuente | Fecha |
|---|---|---|---|
| V1 | Descargar texto Resolución SBS N° 053-2023 | https://www.sbs.gob.pe → Regulación → Resoluciones 2023 | 2026-05-19 |
| V2 | Descargar texto D.S. N° 115-2025-PCM | https://busquedas.elperuano.pe | 2026-05-19 |
| V3 | Leer EU AI Act Art. 13 oficial | https://eur-lex.europa.eu/eli/reg/2024/1689 | 2026-05-20 |
| V4 | Verificar Boletín MIDAGRI 2026 con cifras 2025 | https://www.gob.pe/midagri | 2026-05-21 |
| V5 | Anotar artículos exactos citados en Cap I y Cap II | Actualizar cada `[SBS-Art.X]` con número real | 2026-05-22 |

---

## TAREAS DE SEGUIMIENTO Y CALIDAD

### Semanales (cada lunes)
1. Actualizar progreso en `docs/plan-siguientes-pasos.md` con checkmarks.
2. Ejecutar `py scripts/auditar_referencias.py` para verificar integridad de citas.
3. Pull / push del repositorio Git con mensaje semanal.

### Quincenales
1. Reunión con asesor Dr. Cornejo.
2. Revisión cruzada de avance contra plan-revision-academica-exhaustiva.md.

### Al cierre de cada hito
1. Crear `docs/hito-N-completado.md` con evidencia (tablas, capturas, fechas).
2. Actualizar `plan_detallado.md` con el estado real.

---

## RIESGOS IDENTIFICADOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Reclutamiento insuficiente para estudio de usabilidad (N < 15) | Media | Alto | Diseñar protocolo asíncrono que permita autoaplicación; usar estudiantes UNSA |
| Texto regulatorio SBS/PCM no disponible públicamente | Baja | Medio | Solicitar a biblioteca UNSA o consulta institucional directa |
| API LLM excede presupuesto | Media | Medio | Usar modelo local (Llama 3.1) como respaldo |
| Resultados experimentales no confirman hipótesis | Media | Alto | Reportar honestamente; convertir resultado negativo en aporte (qué no funciona y por qué) |
| Demora en código por complejidad RAG | Media | Alto | Usar implementación mínima viable (BM25 + plantilla) antes de optimizar |

---

## SIGUIENTE ACCIÓN INMEDIATA (esta semana)

1. **HOY (2026-05-17)**: terminar el commit con los cambios de plan + purga referencias.
2. **2026-05-18 (lunes)**: ejecutar `pip install -r requirements.txt` en `.venv`.
3. **2026-05-19**: descargar y leer texto oficial SBS N° 053-2023 + D.S. 115-2025-PCM.
4. **2026-05-20**: ejecutar `py src/generate_synthetic_dataset.py` y validar dataset.
5. **2026-05-21**: comenzar `src/module1_prediction.py` con esqueleto + tests unitarios.

---

*Plan creado 2026-05-17. Próxima revisión: 2026-05-24.*
