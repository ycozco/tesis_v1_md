# BÚSQUEDA SISTEMÁTICA — Verificación del Gap de Investigación
## Sustento del claim: "Primera arquitectura integrada de 4 capas para supervisión operativa agroexportadora peruana"
## Fecha de cierre prevista: 2026-05-27 | Estado: 🔄 En ejecución

> **Propósito**: Documentar la búsqueda bibliográfica sistemática que respalda la afirmación de brecha (gap claim) del Capítulo II §2.2 Batalla 4 y Capítulo I §1.7.1. Este documento es un requisito de revisión por pares para cualquier afirmación de "primer trabajo" o "no existe en la literatura".
>
> **Método**: Inspirado en PRISMA 2020 (Page et al., 2021), adaptado a una tesis individual de pregrado.

---

## 1. Pregunta de revisión

¿Existe en la literatura académica algún trabajo previo que integre, en un mismo pipeline operativo y con evaluación empírica reproducible, los cuatro módulos siguientes aplicados a supervisión operativa agroexportadora o a un dominio análogo de monitoreo de cadenas productivas?

1. Predicción tabular con GBDT validada en benchmark.
2. Detección de anomalías mediante ensemble de detectores.
3. Explicabilidad mediante SHAP (TreeSHAP).
4. Generación de reportes con LLM bajo restricción anti-alucinación (RAG o equivalente).

---

## 2. Estrategia de búsqueda

### 2.1 Bases de datos consultadas

| Base de datos | Cobertura | Estado |
|---|---|---|
| IEEE Xplore | Conferencias y revistas IEEE | 🔄 Por consultar |
| ACM Digital Library | Conferencias ACM (KDD, FAccT, SIGMOD) | 🔄 Por consultar |
| Scopus | Indexador multidisciplinario | 🔄 Por consultar |
| Google Scholar | Cobertura amplia, peer y no-peer | ✅ Consultado parcialmente |
| arXiv (cs.AI, cs.LG, cs.CL) | Preprints | ✅ Consultado parcialmente |
| ALICIA — CONCYTEC | Tesis peruanas | 🔄 Por consultar |
| Renati — SUNEDU | Tesis peruanas | 🔄 Por consultar |

### 2.2 Cadenas de búsqueda (Inglés)

| ID | Cadena | Bases | N resultados | N revisados |
|---|---|---|---|---|
| Q1 | `("anomaly detection" OR "outlier detection") AND ("SHAP" OR "Shapley") AND ("LLM" OR "language model") AND ("report" OR "narrative")` | Scopus | — | — |
| Q2 | `"explainable AI" AND "audit" AND ("GBDT" OR "XGBoost" OR "LightGBM") AND "ensemble"` | Scopus | — | — |
| Q3 | `"continuous auditing" AND ("artificial intelligence" OR "machine learning") AND "explainability"` | IEEE Xplore | — | — |
| Q4 | `("agro-export" OR "agriculture" OR "supply chain") AND "anomaly detection" AND ("Peru" OR "Latin America")` | Scopus | — | — |
| Q5 | `"RAG" AND "anomaly" AND "audit" AND "tabular"` | Google Scholar | — | — |
| Q6 | `"integrated pipeline" AND "explainable" AND "machine learning" AND "report generation"` | ACM DL | — | — |

### 2.3 Cadenas de búsqueda (Español)

| ID | Cadena | Bases | N resultados | N revisados |
|---|---|---|---|---|
| Q7 | `"detección de anomalías" AND "inteligencia artificial explicable" AND "Perú"` | ALICIA | — | — |
| Q8 | `"sistema integrado" AND "auditoría" AND "aprendizaje automático" AND "agroexportador"` | Renati | — | — |
| Q9 | `"IA responsable" AND "explicabilidad" AND ("MIDAGRI" OR "SENASA")` | Google Scholar | — | — |
| Q10 | `"supervisión operativa" AND "anomalías" AND "machine learning" AND "Perú"` | ALICIA | — | — |

---

## 3. Criterios de inclusión y exclusión

### 3.1 Inclusión

- Publicaciones entre 2017 y 2026 (10 años, alineado con el surgimiento de SHAP y GBDT moderno).
- Idiomas: inglés o español.
- Tipo: artículo en revista revisada por pares, paper de conferencia, tesis doctoral/maestría, preprint con ≥10 citas o de autor reconocido.
- Aborda al menos dos de los cuatro módulos relevantes (predicción + anomalías; anomalías + SHAP; SHAP + LLM; anomalías + reporte automático).

### 3.2 Exclusión

- Sistemas que se centran exclusivamente en mercados financieros de alta frecuencia (no comparable con el dominio agroexportador empresarial).
- Trabajos sin evaluación empírica (puramente conceptuales o tutoriales).
- Sistemas que usan LLMs como detectores principales (no como narradores), por no ser comparables arquitectónicamente.
- Trabajos cuyo dominio sea exclusivamente médico, vehicular o de ciberseguridad sin transferibilidad mostrada.

---

## 4. Trabajos identificados hasta 2026-05-17 (selección inicial)

| # | Trabajo | Módulos cubiertos | Dominio | Gap respecto a esta tesis |
|---|---|---|---|---|
| T1 | AuditCopilot (Kadir et al., 2025) | Anomalías + LLM narrativo | Asientos contables (doble entrada) | Sin GBDT, sin SHAP estructurado, sin RAG anclado, sin contexto peruano |
| T2 | Park (2024) | LLM multi-agente sobre anomalías | Mercados financieros (S&P 500) | Sin GBDT propio, sin SHAP, dominio no comparable |
| T3 | AuditMAI (Waltersdorfer et al., 2024) | Infraestructura de auditoría de IA | Sistemas IA en general | No usa IA para auditar; audita IA. Conceptual. |
| T4 | Mongolia 2025 (JRFM, 2025) | GBDT + SHAP | Fraude estados financieros | Sin LLM, sin RAG, sin forecasting |
| T5 | Thanathamathee 2024 (Thanathamathee et al., 2024) | XGBoost + SHAP + Anchor | Fraude financiero | Sin LLM, sin ensemble de anomalías |
| T6 | Patel 2024 (Patel et al., 2024) | Auditoría continua con IA | Auditoría financiera | Marco conceptual, sin pipeline implementado |
| T7 | TabLLM (Hegselmann et al., 2023) | LLM para datos tabulares | Tabular genérico | Solo clasificación, no integrado con anomalías ni SHAP |
| T8 | Tsai 2025 (Tsai et al., 2025) | LLM + embeddings para anomalía tabular | Tabular genérico | Sin SHAP, sin RAG anclado, sin reporte estructurado |
| T9 | Almalki & Masud 2025 (Almalki & Masud, 2025) | Stacking GBDT + XAI | Fraude financiero | Sin LLM, sin RAG, sin contexto agroexportador |

---

## 5. Pre-conclusión (sujeto a búsqueda exhaustiva pendiente)

Sobre los 9 trabajos identificados hasta ahora, **ninguno integra simultáneamente los cuatro módulos** (predicción GBDT + ensemble anomalías + SHAP + LLM-RAG anclado) **aplicados al dominio agroexportador** con trazabilidad documental conforme al D.S. N° 115-2025-PCM peruano. La integración parcial más completa es AuditCopilot (T1), que cubre dos módulos en un dominio distinto (asientos contables).

La afirmación de gap se sostiene en cinco dimensiones diferenciadas:

| Dimensión | Trabajo previo más cercano | Distancia respecto a esta tesis |
|---|---|---|
| Integración de 4 módulos | AuditCopilot (2 módulos) | +2 módulos (GBDT y SHAP estructurado) |
| Dominio agroexportador | Ninguno explícito en literatura revisada | Dominio nuevo |
| Contexto regulatorio peruano | Ninguno | Primera aplicación de D.S. 115-2025-PCM |
| RAG anclado en SHAP | Ninguno explícito | Patrón arquitectónico nuevo |
| Evaluación dual técnica + usabilidad | Patel 2024 (solo conceptual) | Primera evaluación empírica integrada |

---

## 6. Acciones pendientes para cerrar el documento

| # | Acción | Responsable | Fecha límite |
|---|---|---|---|
| 1 | Ejecutar Q1–Q10 en cada base de datos y registrar N de resultados | Yoset | 2026-05-22 |
| 2 | Aplicar criterios de inclusión/exclusión sobre N resultados → llegar a corpus final | Yoset | 2026-05-24 |
| 3 | Construir diagrama PRISMA con flujo identificación → cribado → elegibilidad → inclusión | Yoset | 2026-05-26 |
| 4 | Buscar en ALICIA y Renati tesis peruanas similares | Yoset | 2026-05-24 |
| 5 | Documentar trabajos descartados con razón explícita | Yoset | 2026-05-26 |
| 6 | Si aparece un trabajo que cubre los 4 módulos, refinar el gap claim para reflejar la diferenciación específica (contexto, evaluación, etc.) | Yoset + Dr. Cornejo | 2026-05-27 |

---

## 7. Plantilla para registrar cada artículo revisado

```
ID: [T-XX]
Cita: [APA]
Año: [YYYY]
Venue: [Conferencia/Revista]
Módulos cubiertos: [predicción / anomalías / SHAP / LLM]
Dominio: [...]
Dataset: [...]
Métrica reportada: [...]
Limitación principal: [...]
Relevancia para gap claim: [alta/media/baja]
Decisión: [incluido / descartado por criterio X]
```

---

*Documento generado 2026-05-17. Actualizar tras cada ejecución de búsqueda hasta cierre del Hito 1.*
