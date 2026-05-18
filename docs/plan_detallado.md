# PLAN DETALLADO — TESIS COMPLETA (CAP. I-V + ANEXOS)
## Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas
## Universidad Nacional de San Agustín de Arequipa — Ingeniería de Sistemas
## Estado: Actualizado 2026-05-17 (Hito 1 cerrado, ejecutado plan-revision-academica-exhaustiva.md)

---

> **CÓMO USAR ESTE PLAN**
> Cada sección indica: (a) texto borrador listo para insertar o adaptar, (b) dónde van las citas, (c) qué datos faltan marcados con `⚠️ DATO FALTANTE`, (d) qué diferencia a esta tesis de los competidores marcados con `🎯 DIFERENCIADOR`.
>
> **NOVEDAD 2026-05-17:** La tesis fue segmentada en 19 archivos numerados en `docs/`. El servidor Flask sirve cada sección en `/seccion/<slug>` con hot-reload. Ver `docs/plan-segmentacion-docker.md`.

---

## ACTUALIZACIÓN 2026-05-17 — ESTADO REAL

### Lo que cambió respecto al plan del 2026-05-15

| Componente | Estado en 2026-05-15 | Estado real 2026-05-17 |
|------------|----------------------|------------------------|
| Título y enfoque | Mixto (financiero + agro) | ✅ 100% agroexportador |
| Capítulo I | Avanzado | ✅ Completo — `docs/10-capitulo1.md` |
| Capítulo II §2.1 | Superficial | ✅ 7 antecedentes completos — `docs/20-*.md` |
| Capítulo II §2.2 | Parcial | ✅ 5 batallas + 2 tablas — `docs/21-*.md` |
| Capítulo II §2.3 | No iniciado | ✅ §2.3.1–§2.3.9 completos — `docs/22-*.md` |
| Capítulo III | Pendiente de migrar | ✅ Completo y agroexportador — `docs/30-capitulo3.md` |
| Capítulo IV | Placeholder | 🔴 Placeholder — requiere experimentos |
| Capítulo V | Placeholder | 🔴 Placeholder — depende de Cap IV |
| Monolito `tesis.md` | Activo (1018 líneas) | ✅ Segmentado en 19 archivos numerados |
| Servidor Docker | Compilación estática | ✅ Hot-reload por sección activado |
| `refs.bib` | 65 entradas, 37 usadas | ✅ Verificado — sin citas huérfanas |

### El cuello de botella real (no es redacción, es implementación)

El plan de 2026-05-15 se enfocó en redacción. La tesis **ya está escrita** en todos los capítulos donde se puede escribir sin datos experimentales. El bloqueo ahora es:

1. **No existe el dataset sintético agroexportador** → bloquea Cap IV §4.1 y §4.2
2. **No existe el código de los 4 módulos** (`src/module1_prediction.py`, etc.) → bloquea todos los experimentos
3. **Sin resultados experimentales, Cap IV, V, Conclusiones y Anexos B/C** no se pueden completar

### Diagnóstico de los 5 hitos del plan anterior

| Hito | Fecha | Estado | Diagnóstico |
|------|-------|--------|-------------|
| Hito 1: Variables operacionalizadas | 2026-05-27 | ✅ Cerrado 2026-05-17 | `docs/variables-operacionalizadas.md` con tabla formal 7×5 + pruebas estadísticas asignadas. |
| Hito 2: Datasets identificados | 2026-06-01 | 🟢 Adelantado | Especificación cerrada (`docs/A3-anexo-datasheet.md`) + script generador (`src/generate_synthetic_dataset.py`). Falta ejecutar `pip install -r requirements.txt && py src/generate_synthetic_dataset.py`. |
| Hito 3: Datos descargados y Datasheets | 2026-06-10 | ⏳ Pendiente | Datasheet ya está. Falta ejecutar el generador y validar muestra. |
| Hito 4: Fairness completado | 2026-06-22 | ⏳ Pendiente | Plantillas de análisis por subgrupo agregadas a Model Cards (Anexo B). |
| Hito 5: Cap III actualizado | 2026-07-01 | ✅ Completado | Cap III ya está agroexportador, con diseño experimental E1–E5 detallado. |

---

## ESTRUCTURA COMPLETA Y ARCHIVOS ACTIVOS (2026-05-17)

### Archivos de sección (esquema segmentado)

| Archivo | Sección | Estado | Tamaño |
|---------|---------|--------|--------|
| `docs/00-portada.md` | Portada, dedicatoria, agradecimientos, presentación | ✅ | 2 KB |
| `docs/01-resumen.md` | Resumen + Abstract | ✅ | 4 KB |
| `docs/02-indices.md` | Índices de contenidos, figuras, tablas, fórmulas | ✅ | 2 KB |
| `docs/03-introduccion.md` | Introducción | ✅ | 4 KB |
| `docs/10-capitulo1.md` | Cap I §1.1–§1.11 | ✅ | 23 KB |
| `docs/20-capitulo2-antecedentes.md` | §2.1 — 7 antecedentes | ✅ | 8 KB |
| `docs/21-capitulo2-estadoarte.md` | §2.2 — 5 batallas + tablas | ✅ | 15 KB |
| `docs/22-capitulo2-marcoteorico.md` | §2.3 — §2.3.1–§2.3.9 | ✅ | 23 KB |
| `docs/30-capitulo3.md` | Cap III §3.1–§3.3 | ✅ | 6 KB |
| `docs/40-capitulo4.md` | Cap IV §4.1–§4.3 | 🔴 Placeholder | 2 KB |
| `docs/50-capitulo5.md` | Cap V §5.1–§5.3 | 🔴 Placeholder | 1 KB |
| `docs/60-conclusiones.md` | Conclusiones ES + EN | 🔴 Placeholder | 2 KB |
| `docs/70-recomendaciones.md` | Recomendaciones | ✅ | 2 KB |
| `docs/80-glosario.md` | Glosario | ✅ | 6 KB |
| `docs/90-referencias.md` | Referencias bibliográficas APA | ✅ | 11 KB |
| `docs/A1-anexo-usabilidad.md` | Anexo A — Protocolo usabilidad | 🔴 Skeleton | 1 KB |
| `docs/A2-anexo-modelcards.md` | Anexo B — Model Cards | 🔴 Skeleton | <1 KB |
| `docs/A3-anexo-datasheet.md` | Anexo C — Datasheet dataset | 🔴 Skeleton | <1 KB |
| `docs/A4-anexo-ia.md` | Anexo D — Registro uso IA | ✅ | <1 KB |

**Resumen**: 13/19 secciones completas · 6/19 requieren datos experimentales

### Checkup del avance

**PROGRESO REDACCIÓN**: 13/19 secciones escritas (68%)
**PROGRESO IMPLEMENTACIÓN**: 0/5 hitos de datos/código completados (0%)

#### Componentes de redacción
- [x] Portada, presentación, resumen y abstract — `00-portada.md`, `01-resumen.md`
- [x] Índice general y estructura de navegación — `02-indices.md`
- [x] Introducción completa — `03-introduccion.md`
- [x] Capítulo I §1.1–§1.11 completo y alineado al enfoque agroexportador
- [x] Capítulo II §2.1 — 7 antecedentes con formato UNSA
- [x] Capítulo II §2.2 — 5 batallas argumentativas + Tablas 2.1 y 2.2
- [x] Capítulo II §2.3 — 9 sub-secciones del marco conceptual
- [x] Capítulo III §3.1–§3.3 — arquitectura, datasets, métricas
- [x] Recomendaciones, Glosario, Referencias
- [ ] **Hito 1: Tabla formal de variables operacionalizadas (2026-05-27)**
- [ ] **Hito 2: Dataset sintético agroexportador construido (2026-06-01)**
- [ ] **Hito 3: Código 4 módulos + experimentos E1–E5 (2026-06-15)**
- [ ] **Hito 4: Cap IV escrito con resultados reales (2026-06-22)**
- [ ] **Hito 5: Cap V + Conclusiones + Anexos B/C cerrados (2026-07-07)**

#### Componentes de implementación (nueva categoría — bloqueo principal)
- [ ] Dataset sintético `data/dataset_agro_sintetico.csv` (800–2000 registros)
- [ ] `src/module1_prediction.py` — XGBoost + LightGBM
- [ ] `src/module2_anomaly.py` — IF + LOF + ECOD vía PyOD
- [ ] `src/module3_shap.py` — TreeSHAP + top-k
- [ ] `src/module4_rag.py` — LLM + RAG + prompt
- [ ] `src/pipeline.py` — integración de las 4 capas
- [ ] `src/evaluate.py` — métricas E1–E5

#### Infraestructura Docker (completado hoy 2026-05-17)
- [x] `docs/` segmentada en 19 archivos numerados
- [x] `src/app.py` — rutas `/secciones` y `/seccion/<slug>` con navegación prev/next
- [x] Hot-reload: editar cualquier `docs/XX-*.md` → Flask recarga automáticamente
- [x] MathJax integrado para fórmulas LaTeX en el visor web
- [x] `convert_md_to_html.py` actualizado con `SECTION_ORDER` dinámico
- [x] `docker-compose.yml` en modo `development` con `FLASK_DEBUG=1`

#### Plan de Revisión Académica Exhaustiva (ejecutado 2026-05-17)
- [x] Documento maestro `docs/plan-revision-academica-exhaustiva.md` con 87 criterios en 10 dimensiones
- [x] Cap I §1.7.1 reescrito con 4 aportes diferenciados y aporte original específico
- [x] Cap I §1.9 ampliado a 5 sub-secciones (línea, marco epistemológico, tipo, nivel, diseño)
- [x] Cap I §1.12 (Limitaciones) con 4 categorías de validez declaradas
- [x] Cap I §1.13 (Declaración de intereses y aspectos éticos) agregada
- [x] Cap II §2.3.7 (RAG) con hedging apropiado, distinción tipos de alucinación y referencias a Lewis 2020 + Ji 2023
- [x] Cap II §2.3.8 con matización sobre cumplimiento regulatorio (no afirmar, sino "conformidad de diseño")
- [x] Cap III §3.1 con justificación de ECOD sobre Deep SVDD
- [x] Cap III §3.3 con división temporal, pruebas estadísticas H1a–H1d, criterios participantes, baselines, ablation E5a–E5d
- [x] `docs/variables-operacionalizadas.md` — Hito 1 cerrado
- [x] `docs/busqueda-sistematica-gap.md` — protocolo PRISMA-light
- [x] `docs/A1-anexo-usabilidad.md` completo (protocolo + SUS + consentimiento)
- [x] `docs/A2-anexo-modelcards.md` con 4 Model Cards (Mitchell 2019)
- [x] `docs/A3-anexo-datasheet.md` completo (Gebru 2021)
- [x] `config/refs.bib` + 8 referencias (Friedman, TreeSHAP, Ji 2023, PRISMA, Creswell, MIDAGRI, Cohen, Optuna)
- [x] `requirements.txt` con versiones fijadas
- [x] `src/generate_synthetic_dataset.py` listo (pendiente de ejecución con dependencias)

### ✅ NUEVA SECCIÓN: PLAN DE REVISIONES AMPLIADO (8 CATEGORÍAS)

**Estado**: Completado — 2025  
**Responsable**: Yoset Cozco Mauri + Copilot  
**Documentación**: Ver carpeta `entregable/`

#### Categorías de revisión (Antes: 6 → Ahora: 8)

| # | Categoría | Descripción | Indicadores | Estado |
|---|-----------|-------------|-------------|--------|
| 1 | **Estructural** | Flujo lógico, coherencia, índices | 5 | ✅ 80% |
| 2 | **Rigor Científico** | Variables operacionalizadas, hipótesis, causalidad | 5 | ✅ 60% |
| 3 | **Metodológica** | Reproducibilidad, métricas, Model Cards | 8 | ✅ 62% |
| 4 | **Documentación de Datos** | Datasheets, sesgos conocidos, licencias | 7 | ✅ 57% |
| 5 | **Gobernanza + Regulación** | SBS N° 053, DS-115-PCM, EU AI Act | 6 | ✅ 17% |
| 6 | **Explicabilidad** | SHAP, incertidumbre, anti-alucinación | 6 | ✅ 0% |
| 7 | **Ética y Sesgo** | 🆕 Fairness, desempeño por subgrupos | 6 | ✅ 0% |
| 8 | **Web/Usabilidad** | Interfaz, documentación, accesibilidad | 6 | ✅ 33% |

**Total**: 49 indicadores de logro | **Avance global**: 38% completado

#### Justificación académica
Las nuevas categorías (Explicabilidad y Ética/Sesgo) están fundamentadas en:
- **Mitchell et al. (2018)** — Model Cards for Model Reporting
- **Gebru et al. (2018)** — Datasheets for Datasets
- **Lipton (2016)** — The Mythos of Model Interpretability
- **NIST AI RMF (2023)** — Framework de gobernanza
- **ACM Code of Ethics** — Fairness, transparency, accountability
- **EU AI Act 2024** — Regulación de IA de alto riesgo
- **Perú DS-115-2025-PCM** — Ley de IA nacional

#### Archivos de referencia en `/entregable/`
1. `sustentacion-revisiones-ampliada.md` — Detalle académico de cada categoría
2. `matriz-revisiones-8categorias.md` — Matriz de 49 indicadores con checklist
3. `matriz-seguimiento-49indicadores.csv` — Tracking automático (importar a Excel/Sheets)
4. `RESUMEN-EJECUTIVO-revisiones.md` — Documento ejecutivo de síntesis

#### Orden de trabajo recomendado
**Fase 1 (Inmediata)**: Operacionalizar variables + crear Datasheets + decisiones metodológicas  
**Fase 2 (Semana 2-3)**: Matriz SBS + análisis fairness + validación SHAP  
**Fase 3 (Semana 4+)**: Dashboard + usabilidad + cierre regulatorio

---

## ✅ NUEVA SECCIÓN: PLAN DETALLADO DE RIGOR ACADÉMICO Y BÚSQUEDA DE DATASETS

**Estado**: Creado — 2026-05-15  
**Responsable**: Yoset Cozco Mauri + Dr. Víctor Manuel Cornejo Aparicio  
**Documentación**: Ver `docs/plan-rigor-academico-datasets.md`

**Objetivo**: Establecer un marco académico riguroso en 5 pilares con 5 hitos y 30+ tareas específicas

### 5 Pilares de Rigor Académico

| # | Pilar | Objetivo | Hitos | Documentos |
|---|-------|----------|-------|-----------|
| 1 | **Operacionalización de Variables** | Cada variable → fórmula medible | Hito 1 (2026-05-27) | `variables-operacionalizadas.md` |
| 2 | **Búsqueda de Datasets** | Localizar 3 datasets agroexportadores | Hito 2 (2026-06-01) | `sources-log.md`, `feasibility-datasets.md` |
| 3 | **Datasheets for Datasets** | Documentar cada dataset (Gebru 2018) | Hito 3 (2026-06-10) | 3 datasheets en `datasheets/` |
| 4 | **Validación de Calidad** | Garantizar reproducibilidad y confiabilidad | Hito 3 (2026-06-10) | `data-quality-decisions.md` |
| 5 | **Análisis de Fairness** | Evaluar equidad en subgrupos | Hito 4 (2026-06-22) | `fairness-report.md` + gráficos |

### 5 Hitos principales

| Hito | Fecha Límite | Responsable | Criterio de éxito | Estado |
|------|--------------|-------------|-------------------|--------|
| **Hito 1** | 2026-05-27 | Yoset | 5 variables operacionalizadas + signadas | ⏳ Pendiente |
| **Hito 2** | 2026-06-01 | Yoset + Dr. Cornejo | 3 datasets identificados, 2 con acceso confirmado | ⏳ Pendiente |
| **Hito 3** | 2026-06-10 | Yoset | Datos descargados, 95%+ completos, Datasheets completados | ⏳ Pendiente |
| **Hito 4** | 2026-06-22 | Yoset | Fairness calculado, diferencia ≤5% entre subgrupos o documentada | ⏳ Pendiente |
| **Hito 5** | 2026-07-01 | Yoset + Dr. Cornejo | Cap. III actualizado, scripts reproducibles, anexos listos | ⏳ Pendiente |

### Tareas inmediatas (Esta semana)

1. **Tarea 1.1**: Revisar Capítulo I → Listar todas las variables mencionadas  
   - **Responsable**: Yoset | **Fecha**: 2026-05-20 | **Entregable**: `variables-listado.md`

2. **Tarea 1.2**: Operacionalizar 5 variables (definición operacional + fórmula)  
   - **Responsable**: Yoset | **Fecha**: 2026-05-27 | **Entregable**: Tabla completada

3. **Tarea 2.1.1**: Contactar MIDAGRI, SENASA solicitando acceso a datos  
   - **Responsable**: Yoset + Dr. Cornejo | **Fecha**: 2026-05-22 | **Entregable**: Emails enviados + log

4. **Tarea 3.1**: Crear plantilla Datasheet en Google Docs  
   - **Responsable**: Yoset | **Fecha**: 2026-05-30 | **Entregable**: Documento compartido

### Fuentes de datos identificadas

**Estado**: Búsqueda iterativa completada — 2026-05-15  
**Documentación**: Ver `entregable/BUSQUEDA-DATASETS-ITERATIVA.md` y `entregable/REFERENCIAS-DATASETS-VALIDADAS.csv`

```
DATASETS PRIMARIOS (Datos operativos agroexportadores):
├─ Boletines MIDAGRI: Precios mayoristas mensuales ✅ Verificado
├─ Reportes MIDAGRI: Ingreso diario a mercados ✅ Verificado
├─ Abastecimiento GMML: Volumen y precios mercado mayorista ✅ Verificado
└─ Fuente: MIDAGRI (https://www.gob.pe/minagri)

DATASETS SECUNDARIOS (Contexto climático y regulatorio):
├─ Pronósticos meteorológicos SENAMHI ✅ Verificado
├─ Lluvia acumulada nacional ✅ Verificado
├─ Requisitos fitosanitarios SENASA ✅ Verificado
├─ Establecimientos habilitados SENASA ✅ Verificado
└─ Fuentes: SENAMHI (https://www.senamhi.gob.pe/), SENASA (https://www.gob.pe/senasa)

DATASETS TERCIARIOS (Contexto macroeconómico):
├─ Índice de Precios Mayor (INEI) ✅ Verificado
├─ PBI por sectores (INEI) ✅ Verificado
├─ Estadísticas aduaneras (SUNAT) ✅ Verificado
├─ FAOSTAT Production Module ✅ Verificado
├─ UN Comtrade Plus ✅ Verificado
├─ World Bank Data ✅ Verificado
└─ Fuentes: INEI, SUNAT, FAO, ONU, World Bank
```

**Total de datasets validados**: 25 fuentes + 17 accesos verificados (✅) + 2 accesos restringidos (🔴)

### Tracking integrado

**Usar `matriz-seguimiento-49indicadores.csv` + agregar nuevas filas para hitos**

Ejemplo:
```
Rigor Científico, Operacionalización, "Variables operacionalizadas", "Cada variable con fórmula medible", ⏳ Pendiente, Yoset, Crítica, 2026-05-20, 2026-05-27
Datos y Referencias, Búsqueda, "Datasets agroexportadores identificados", "Mínimo 3 datasets de fuentes públicas", ⏳ Pendiente, Yoset, Crítica, 2026-05-22, 2026-06-01
```

### Validación y checkups

**Checkup Semanal**: Cada lunes, Yoset actualiza progreso en `checkups-semanal.md`

**Checkup de Hito**: Al cumplir cada hito, generar `hito-N-completado.md` con evidencia

**Checkup Integración**: Cada 2 semanas, revisar alineación con plan general y 8 categorías de revisión

---

---

## ÍNDICE DEL PLAN

1. [Diagnóstico del estado actual](#1-diagnóstico)
2. [Capítulo I — Refinamiento y completitud](#2-capítulo-i)
3. [Capítulo II §2.1 — Antecedentes (estructura completa)](#3-antecedentes)
4. [Capítulo II §2.2 — Estado del Arte (5 batallas argumentativas)](#4-estado-del-arte)
5. [Capítulo II §2.3 — Bases Teóricas](#5-bases-teóricas)
6. [Análisis comparativo con competidores directos](#6-análisis-competidores)
7. [Matriz de brechas (gap analysis)](#7-gap-analysis)
8. [Checklist de datos faltantes](#8-datos-faltantes)

---

## 1. DIAGNÓSTICO DEL ESTADO ACTUAL

### Lo que ya está desarrollado (no reescribir)
| Archivo | Contenido presente | Calidad |
|---------|-------------------|---------|
| `tesis.md` | Estructura completa Cap. I-V + anexos | ✅ Base activa y más avanzada |
| `entregable1.md` | Cap. I y II base previa | ✅ Útil como antecedente de redacción |
| `tesis_v2.md` | Versión anterior financiera/fraude | ⚠️ Desfasada; conservar solo como referencia histórica |
| `mejora-continua-plan.md` | Plan PDCA por ciclos | ✅ Útil para iteración |

### Lo que FALTA y es el objeto de este plan
1. Ajustar el lenguaje financiero residual en `tesis_v2.md` y partes heredadas.
2. Consolidar Capítulo III con datos agroexportadores y benchmarks públicos de soporte.
3. Completar Capítulo IV con resultados, gráficas y discusión.
4. Cerrar Capítulo V con conclusiones, limitaciones y trabajos futuros.
5. Normalizar bibliografía y citas para que el enfoque quede homogéneo.
6. Mantener coherencia entre título, resumen, hipótesis, variables y fuentes de datos.

---

## 2. CAPÍTULO I — REFINAMIENTO Y COMPLETITUD

### 2.1 Refinamientos necesarios (no reescrituras)

El Capítulo I de `entregable1.md` es sólido. Los únicos refinamientos son:

#### §1.1 — Agregar magnitud del problema con cifras verificables

En el párrafo de "Magnitud del problema", insertar después de la frase actual:

> Según Almalki y Masud (2025), las pérdidas globales por fraude financiero ascendieron de USD 28,400 millones en 2020 a USD 33,500 millones en 2022, lo que evidencia la necesidad urgente de sistemas automatizados de detección (Almalki & Masud, 2025 [G09]). En el contexto peruano, la Superintendencia de Banca, Seguros y AFP emitió la Resolución N° 053-2023, que exige a entidades financieras implementar sistemas de gestión de riesgos de modelo con trazabilidad verificable a partir de enero de 2026 (SBS, 2023 [G01]). Esta normativa eleva la urgencia de soluciones como la propuesta en esta investigación.

**⚠️ DATO FALTANTE**: Cifra de pérdidas por fraude en Perú específicamente. Consultar: ASBANC, SBS Memoria Anual 2024, o Unidad de Inteligencia Financiera UIF-Perú. Alternativa: usar estadística de FELABAN (Federación Latinoamericana de Bancos).

#### §1.7.1 — Justificación Teórica: agregar la brecha exacta

Reemplazar el párrafo actual de "brecha identificada" por:

> La revisión sistemática de la literatura revela que trabajos como AuditCopilot (Kadir et al., 2025 [E03]) integran LLMs con detección de anomalías en asientos contables, y el framework multi-agente de Park (2024 [E04]) extiende este enfoque a mercados financieros. Sin embargo, ninguno de estos sistemas contempla simultáneamente: (a) predicción tabular con GBDT validada frente a benchmarks estándar, (b) forecasting multi-horizonte integrado al pipeline de auditoría, (c) ensemble de detectores de anomalías evaluados con ADBench (Han et al., 2022 [C04]), y (d) generación de reportes con trazabilidad regulatoria según la Resolución SBS N° 053-2023. Esta brecha cuádruple justifica la propuesta de arquitectura modular de esta tesis.

#### §1.7.3 — Justificación Social: agregar marco legal peruano e internacional

> El Decreto Supremo N° 115-2025-PCM, reglamento de la Ley N° 31814 de inteligencia artificial del Perú, clasifica los sistemas de IA aplicados a decisiones financieras como de "alto riesgo", exigiendo explicabilidad, auditabilidad y supervisión humana (PCM, 2025 [G02]). A nivel internacional, el Reglamento (UE) 2024/1689 (EU AI Act) establece en su Artículo 13 obligaciones formales de transparencia para sistemas de IA de alto riesgo, con sanciones de hasta 35 millones de euros por incumplimiento (Parlamento Europeo, 2024 [G03]). El sistema propuesto en esta tesis es diseñado desde sus fundamentos para cumplir con ambos marcos regulatorios, lo que le otorga relevancia social y regulatoria directa.

---

## 3. CAPÍTULO II §2.1 — ANTECEDENTES (ESTRUCTURA COMPLETA)

### Formato UNSA para cada antecedente
Cada antecedente debe contener:
1. **Título y referencia** (APA completo)
2. **Objetivo del estudio**
3. **Metodología** (qué hicieron)
4. **Resultados** (qué encontraron, con métricas)
5. **Relevancia para esta tesis** (por qué es antecedente)

Se proponen **7 antecedentes** distribuidos: 3 internacionales directos, 2 internacionales metodológicos, 2 nacionales/regionales.

---

### ANTECEDENTE 1 — AuditCopilot (Competidor directo)
**Fuente**: E03

**Referencia APA**: Kadir, M. A., et al. (2025). AuditCopilot: Large language models in accounting audit. [Verificar venue — probablemente arXiv preprint].

**Objetivo**: Desarrollar un sistema de auditoría contable que integre modelos de lenguaje de gran tamaño (LLMs) con detección de anomalías en asientos contables de doble entrada.

**Metodología**: El sistema implementa un pipeline de tres etapas: (1) detección de irregularidades en asientos contables mediante clasificadores supervisados, (2) interpretación contextual mediante un LLM fine-tuned en terminología contable, y (3) generación de explicaciones en lenguaje natural para auditores. Se evalúa en un corpus de asientos contables sintéticos y reales (bajo confidencialidad).

**Resultados**: El sistema reporta mejoras en la tasa de detección de irregularidades respecto a enfoques manuales, con reducción del tiempo de revisión. Las explicaciones generadas son valoradas por auditores en pruebas de usabilidad.

**Relevancia para esta tesis**: AuditCopilot es el antecedente más cercano en objetivo, pues combina detección de anomalías con generación de reportes en lenguaje natural. Sin embargo, **presenta tres limitaciones fundamentales que esta investigación supera**:
- No incluye módulo de predicción tabular GBDT evaluado contra benchmarks reproducibles.
- No incorpora forecasting de series temporales integrado al pipeline de auditoría.
- No evalúa conformidad con marcos regulatorios explícitos (SBS N° 053-2023, EU AI Act).

🎯 **DIFERENCIADOR**: Esta tesis añade la capa de predicción GBDT (validada en BAF Benchmark) y el módulo de forecasting TFT, configurando un pipeline de auditoría más completo con trazabilidad regulatoria documentada según NIST AI RMF (NIST, 2023 [F05]).

---

### ANTECEDENTE 2 — Framework Multi-Agente LLM para Detección de Anomalías Financieras
**Fuente**: E04

**Referencia APA**: Park, T. (2024). Enhancing anomaly detection in financial markets with an LLM-based multi-agent framework. *arXiv preprint arXiv:2403.19735*.

**Objetivo**: Proponer un framework de múltiples agentes LLM especializados para validar alertas de anomalías en el índice S&P 500, combinando análisis de datos financieros con razonamiento en lenguaje natural.

**Metodología**: Arquitectura multi-agente compuesta por cuatro agentes especializados: (1) agente de conversión de datos, (2) agente de análisis estadístico, (3) agente de verificación cruzada, y (4) agente de consolidación de reportes. Los agentes se comunican mediante prompts estructurados y validan anomalías detectadas por algoritmos clásicos.

**Resultados**: El framework mejora la tasa de verdaderos positivos en la validación de anomalías en S&P 500, con reducción de falsos positivos mediante el consenso multi-agente. La arquitectura demuestra que múltiples LLMs especializados superan a un único LLM generalista.

**Relevancia para esta tesis**: El trabajo de Park (2024) aporta evidencia de que la arquitectura multi-agente mejora la calidad del análisis financiero. Valida el enfoque de usar LLMs como capa de interpretación sobre resultados de modelos cuantitativos.

🎯 **DIFERENCIADOR**: Park trabaja exclusivamente en **mercados financieros** (datos de precios, índices bursátiles) con variables continuas y alta frecuencia. Esta tesis se aplica a **auditoría empresarial** con datos tabulares de transacciones contables, donde la trazabilidad regulatoria interna (SBS, NIST) prima sobre la velocidad de respuesta. Además, esta investigación evita el riesgo de alucinaciones LLM documentado en este tipo de sistemas (survey de alucinaciones, 2026 [G10]) al restringir el LLM a interpretar vectores SHAP deterministas mediante RAG.

---

### ANTECEDENTE 3 — Detección de Fraude con ML Interpretable y Ensemble GBDT
**Fuente**: G06

**Referencia APA**: [Verificar autores]. (2025). Financial statement fraud detection through an integrated machine learning and explainable AI framework. *Journal of Risk and Financial Management*, *19*(1), 13. https://doi.org/10.3390/jrfm19010013

**Objetivo**: Diseñar un framework integrado de detección de fraude en estados financieros que combine modelos de ensamble (Stacking Ensemble de GBDT) con técnicas de explicabilidad (SHAP).

**Metodología**: Se implementa un Stacking Ensemble de tres capas: XGBoost + LightGBM + CatBoost como modelos base, con un meta-clasificador de regresión logística. La explicabilidad se evalúa mediante SHAP Stability Index para medir coherencia de las explicaciones entre instancias similares. El experimento se realiza sobre datos de estados financieros con etiquetas de fraude.

**Resultados**: El ensemble alcanza PR-AUC = 0.93 y F1-Score = 0.83 en la detección de fraude financiero, superando a TabNet (Arik & Pfister, 2021 [A05]) y FT-Transformer (Gorishniy et al., 2021 [A04]). El SHAP Stability Index = 0.87 confirma la coherencia forense de las explicaciones.

**Relevancia para esta tesis**: Este trabajo valida empíricamente la superioridad del Stacking Ensemble de GBDT con SHAP sobre alternativas de Deep Learning para datos financieros. Sus resultados respaldan directamente la elección arquitectónica de esta tesis.

🎯 **DIFERENCIADOR**: El trabajo citado se limita a la detección de fraude. Esta tesis añade el módulo de forecasting (TFT), el ensemble de detectores de anomalías no supervisado, y la generación automática de reportes con LLM+RAG, configurando un pipeline completo de auditoría continua, no solo detección.

---

### ANTECEDENTE 4 — ADBench: Evaluación Sistemática de Detectores de Anomalías
**Fuente**: C04

**Referencia APA**: Han, S., Hu, X., Huang, F., Jiang, M., & Zhao, Y. (2022). ADBench: Anomaly detection benchmark. *Advances in Neural Information Processing Systems*, *35*.

**Objetivo**: Proporcionar un benchmark estandarizado y reproducible para evaluar algoritmos de detección de anomalías bajo múltiples condiciones de supervisión y distribuciones de datos.

**Metodología**: Evaluación de 30 algoritmos en 57 datasets bajo tres escenarios: (1) completamente no supervisado, (2) semisupervisado con pocas etiquetas, y (3) supervisado completo. Los datasets incluyen dominios financieros, médicos, industriales y de ciberseguridad.

**Resultados**: No existe un algoritmo universalmente superior en todos los escenarios. Isolation Forest (Liu et al., 2008 [C01]) y ECOD (Li et al., 2022 [C05]) muestran consistencia en contextos no supervisados. El ensemble de múltiples detectores supera sistemáticamente a cualquier detector individual en escenarios con alta variabilidad de distribución.

**Relevancia para esta tesis**: ADBench justifica formalmente la decisión de implementar un ensemble de detectores (Isolation Forest + LOF + Deep SVDD) en lugar de un único algoritmo. La metodología de evaluación de ADBench sirve como referencia directa para el diseño experimental del Capítulo III.

🎯 **DIFERENCIADOR**: Esta tesis aplica las conclusiones de ADBench en un contexto empresarial específico (auditoría financiera), evaluando el ensemble no solo en métricas de rendimiento sino también en **interpretabilidad para auditores** y **conformidad regulatoria**, dimensiones no abordadas por ADBench.

---

### ANTECEDENTE 5 — Por qué los Modelos Basados en Árboles Superan al Deep Learning en Datos Tabulares
**Fuente**: A06

**Referencia APA**: Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on tabular data? *Advances in Neural Information Processing Systems*, *35*.

**Objetivo**: Investigar empíricamente las causas por las cuales los modelos basados en árboles de decisión superan a las arquitecturas de Deep Learning en conjuntos de datos tabulares de tamaño mediano.

**Metodología**: Benchmark sistemático en 45 datasets tabulares de dominio público, comparando XGBoost, Random Forest y Gradient Boosting contra FT-Transformer, MLP, TabNet y otros modelos de Deep Learning. El análisis identifica tres propiedades de los datos tabulares que favorecen a los árboles: (1) robustez ante features no informativas, (2) orientación de datos no invariante a rotación, (3) irregularidades en la función objetivo.

**Resultados**: En datasets con menos de 100,000 muestras (típico en entornos empresariales medianos), los GBDT superan a todo modelo de Deep Learning en el 95% de los datasets evaluados. La brecha se reduce solo con datasets masivos (>500K muestras).

**Relevancia para esta tesis**: Este trabajo cierra el debate GBDT vs. Deep Learning para el contexto empresarial típico donde se aplica esta investigación. Justifica de manera irrefutable la elección de XGBoost/LightGBM como backbone del módulo de predicción.

**⚠️ DATO FALTANTE**: Caracterizar el tamaño típico del dataset con el que se trabaja en esta tesis (número de transacciones). Si el dataset supera 100K muestras, el argumento de Grinsztajn et al. (2022) se debilita parcialmente y debe complementarse con Almalki & Masud (2025 [G09]).

---

### ANTECEDENTE 6 — Temporal Fusion Transformers para Forecasting Multi-Horizonte Interpretable
**Fuente**: B01

**Referencia APA**: Lim, B., Arık, S. Ö., Loeff, N., & Pfister, T. (2021). Temporal fusion transformers for interpretable multi-horizon time series forecasting. *International Journal of Forecasting*, *37*(4), 1748–1764. https://doi.org/10.1016/j.ijforecast.2021.03.012

**Objetivo**: Proponer una arquitectura de Transformer adaptada para forecasting interpretable en horizontes temporales múltiples, con capacidad de incorporar variables covariables estáticas y dinámicas.

**Metodología**: La arquitectura TFT combina: (1) LSTM para codificación secuencial, (2) mecanismo de selección de variables mediante gating, (3) atención multi-cabezal interpretable, y (4) cuantificación de incertidumbre mediante predicción de cuantiles. Se evalúa en 6 datasets de dominio real incluyendo series financieras y de retail.

**Resultados**: TFT supera a LSTMs, N-BEATS y Transformers vanilla en rendimiento de forecasting para horizontes medios y largos. El mecanismo de gating identifica automáticamente las covariables más relevantes, proporcionando interpretabilidad inherente sin costo computacional adicional.

**Relevancia para esta tesis**: TFT es seleccionado como arquitectura del módulo de forecasting por su doble ventaja: rendimiento predictivo superior y explicabilidad incorporada, alineada con los requisitos regulatorios de trazabilidad. La incorporación de covariables exógenas (indicadores macroeconómicos, fechas de cierre contable) potencia su aplicación en auditoría financiera.

**Nota sobre debate Zeng (2023)**: La crítica de Zeng et al. (2023 [B02]) sobre la efectividad de Transformers en series temporales es superada por PatchTST (Nie et al., 2023 [B05]) e iTransformer (Liu et al., 2024 [B03]), que demuestran que el diseño correcto (tokenización por patches o inversión de dimensiones) preserva las ventajas del mecanismo de atención. TFT evita las críticas de Zeng al incorporar mecanismos de gating que filtran información irrelevante antes de la atención.

---

### ANTECEDENTE 7 — PyOD: Librería Estándar para Detección de Outliers
**Fuente**: C06

**Referencia APA**: Zhao, Y., Nasrullah, Z., & Li, Z. (2019). PyOD: A Python toolbox for scalable outlier detection. *Journal of Machine Learning Research*, *20*(96), 1–7.

**Objetivo**: Desarrollar y publicar una librería unificada en Python que implemente más de 40 algoritmos de detección de outliers con una API estandarizada compatible con scikit-learn.

**Metodología**: Implementación de algoritmos de detección de anomalías en tres categorías: métodos basados en proximidad (LOF, kNN), métodos basados en proyección (PCA, OCSVM) y métodos basados en ensembles (Isolation Forest, LODA). La API sigue el patrón `fit()/predict()` de scikit-learn, facilitando la integración en pipelines existentes.

**Resultados**: PyOD se consolida como la librería más utilizada en la comunidad académica y de industria para detección de anomalías, con más de 7,000 estrellas en GitHub y adopción en competencias Kaggle y papers académicos. Incluye los 30 algoritmos evaluados por ADBench (Han et al., 2022 [C04]) como referencia.

**Relevancia para esta tesis**: PyOD es la herramienta de implementación del módulo de detección de anomalías. Su uso estandariza el pipeline experimental y garantiza reproducibilidad, un requisito del marco NIST AI RMF (NIST, 2023 [F05]) y de la práctica de Datasheets for Datasets (Gebru et al., 2021 [F06]).

---

## 4. CAPÍTULO II §2.2 — ESTADO DEL ARTE

### Estructura propuesta: 5 Batallas Argumentativas

El Estado del Arte se organiza como una argumentación progresiva que conduce al **gap** que justifica esta tesis. Cada "batalla" es una posición teórica que la tesis debe defender ante el jurado.

---

### BATALLA 1 — GBDT vs. Deep Learning para Datos Tabulares

**Posición de la tesis**: XGBoost, LightGBM y CatBoost son la elección óptima para el módulo de predicción en datos financieros de tamaño empresarial.

**Argumento cronológico a desarrollar en prosa**:

> El desarrollo de modelos para datos tabulares ha experimentado una trayectoria que, contrariamente a lo observado en visión computacional y procesamiento de lenguaje natural, no ha sido dominada por el Deep Learning. Chen y Guestrin (2016 [A01]) introdujeron XGBoost como un sistema escalable de gradient boosting con regularización L1/L2 y manejo nativo de valores faltantes, estableciéndolo como el estándar industrial con más de 45,000 citas y presencia dominante en competencias Kaggle. Ke et al. (2017 [A02]) lo extendieron con LightGBM, incorporando Gradient-based One-Side Sampling (GOSS) que logra aceleraciones de hasta 20× respecto a XGBoost sin pérdida significativa de rendimiento, mientras Prokhorenkova et al. (2018 [A03]) resolvieron el problema del target leakage en variables categóricas con Ordered Boosting en CatBoost.
>
> El auge del Deep Learning motivó múltiples intentos de trasladar estos paradigmas a datos tabulares. Gorishniy et al. (2021 [A04]) propusieron FT-Transformer, el primer Transformer robusto para tablas mediante embeddings de features, estableciendo un baseline de DL serio que en algunos benchmarks iguala pero raramente supera a los GBDT. Arik y Pfister (2021 [A05]) desarrollaron TabNet, que combina selección secuencial de features con atención interpretable. Sin embargo, la investigación de Grinsztajn et al. (2022 [A06]) zanjó empíricamente este debate: en un benchmark de 45 datasets con menos de 50,000 muestras, los GBDT superan a todo modelo de Deep Learning en el 95% de los casos, identificando tres propiedades estructurales de los datos tabulares que favorecen a los árboles: robustez ante features no informativas, invarianza a rotaciones de los datos, e irregularidades en la función objetivo.
>
> En el contexto específico de fraude financiero, [G06] confirma esta superioridad con un Stacking Ensemble XGBoost+LightGBM+CatBoost que alcanza PR-AUC = 0.93, superando a TabNet. La estabilidad forense del ensemble (SHAP Stability Index = 0.87) es un requisito adicional en auditoría contable que los modelos de DL difícilmente alcanzan (Thanathamathee et al., 2024 [G08]; [G07]).

**Citas clave para esta batalla**: A01, A02, A03, A04, A05, A06, G06, G07, G08
**⚠️ DATO FALTANTE**: Tamaño del dataset de esta tesis (número de transacciones). Necesario para anclar el argumento de Grinsztajn en el contexto específico.

---

### BATALLA 2 — Detector Único vs. Ensemble para Anomalías

**Posición de la tesis**: Un ensemble de Isolation Forest + LOF + Deep SVDD, coordinado mediante PyOD, es más robusto que cualquier detector individual.

**Prosa para §2.2**:

> La detección de anomalías en datos financieros ha recorrido tres décadas de evolución desde enfoques estadísticos clásicos hasta métodos de aprendizaje profundo. Breunig et al. (2000 [C02]) establecieron el Local Outlier Factor (LOF) como referencia para detectar anomalías locales mediante densidad relativa al vecindario k-NN, un enfoque sensible a variaciones locales apropiado para transacciones con patrones de comportamiento heterogéneos. Liu et al. (2008 [C01]) introdujeron Isolation Forest, que revolucionó el campo al aislar anomalías por particionamiento aleatorio sin necesidad de definir perfiles de normalidad, con complejidad O(n) que lo hace viable en millones de transacciones. Ruff et al. (2018 [C03]) extendieron la detección a espacios de representación profundos con Deep SVDD, capturando patrones no lineales en los datos.
>
> El hallazgo crítico de Han et al. (2022 [C04]) en ADBench —57 datasets, 30 algoritmos, tres escenarios de supervisión— establece que no existe un algoritmo universalmente superior: el rendimiento depende fuertemente del tipo de anomalía, la distribución de los datos y el nivel de etiquetado disponible. Este resultado teórico valida la estrategia de ensemble como la opción más robusta para entornos de producción donde la distribución de anomalías es desconocida a priori. La librería PyOD (Zhao et al., 2019 [C06]) proporciona la infraestructura técnica para implementar este ensemble de manera reproducible y estandarizada.
>
> Un complemento moderno al ensemble es ECOD (Li et al., 2022 [C05]), un detector libre de parámetros basado en distribución empírica acumulada que supera a 11 baselines en 30 datasets. Su ausencia de hiperparámetros elimina el riesgo de sobreajuste al proceso de calibración, particularmente valioso en entornos financieros donde el acceso a datos etiquetados es limitado.

**Citas clave**: C01, C02, C03, C04, C05, C06
**⚠️ DATO FALTANTE**: Resultado experimental comparando detector único vs. ensemble en el dataset de esta tesis (va en Cap. IV pero debe mencionarse como hipótesis aquí).

---

### BATALLA 3 — LLM como Detector vs. LLM como Generador de Reportes

**Posición de la tesis**: El LLM se restringe a la capa de generación de reportes (RAG), NO actúa como detector de anomalías, para garantizar trazabilidad y evitar alucinaciones.

**Esta es la batalla más crítica para el jurado.**

**Prosa para §2.2**:

> El surgimiento de los modelos de lenguaje de gran tamaño (LLMs) ha generado propuestas de integración en sistemas financieros que van desde la clasificación de datos tabulares hasta la detección de anomalías. Hegselmann et al. (2023 [E01]) demostraron con TabLLM que los LLMs pueden clasificar datos tabulares en configuración zero/few-shot mediante serialización a texto, con rendimiento no trivial incluso sin ajuste fino. Park (2024 [E04]) llevó esta lógica más lejos con un framework multi-agente donde LLMs especializados validan alertas de anomalías en mercados financieros. Tsai et al. (2025 [E02]) exploraron embeddings SBERT para detección de anomalías semánticas en registros contables.
>
> Sin embargo, existe evidencia sustancial de que usar LLMs como detectores o tomadores de decisiones en contextos financieros introduce riesgos inaceptables. La literatura sobre alucinaciones en LLMs ([G10], 2026) documenta una taxonomía de errores en los que el modelo genera razonamiento financiero coherente en forma pero matemáticamente incorrecto en contenido. Barclays Research (2025 [G05]) identifica específicamente que LLMs en finanzas pueden producir "alucinaciones numéricas" —valores específicos de métricas, porcentajes o fechas que no corresponden a los datos reales— con alta confianza aparente. El BIS Financial Stability Institute (Prenio & Yong, 2024 [G04]) señala que los reguladores de referencia (FINMA, OCC, MAS) exigen que los sistemas de IA financiera sean explicables en cada decisión individual, condición que los LLMs de caja negra no cumplen.
>
> La respuesta arquitectónica de esta tesis es la separación estricta de responsabilidades: los modelos deterministas (GBDT, Isolation Forest, SHAP) realizan la detección y cuantificación, mientras el LLM actúa exclusivamente como capa de traducción narrativa mediante Retrieval-Augmented Generation (RAG). Como Schneider et al. (2025 [E05]) documentan, el framework RAG permite anclar las respuestas del LLM a bases de conocimiento verificadas, eliminando el espacio de alucinación al forzar al modelo a citar evidencia. El LLM no infiere anomalías; las narra con los valores SHAP deterministas como fundamento. Esto cumple con los requisitos del Art. 13 del EU AI Act (Parlamento Europeo, 2024 [G03]) y la Resolución SBS N° 053-2023 (SBS, 2023 [G01]).

**Citas clave**: E01, E02, E04, E05, G03, G04, G05, G10, G01
**Diferenciadores**: Esta arquitectura de separación es única en la literatura — ninguno de los competidores (AuditCopilot, Park 2024) la implementa con esta justificación regulatoria.

---

### BATALLA 4 — Sistemas Aislados vs. Sistema Integrado (La Brecha Principal)

**Posición de la tesis**: Ningún trabajo en la literatura combina los 4 módulos (predicción GBDT + forecasting + ensemble anomalías + LLM-RAG reportes) en un pipeline de auditoría continua con trazabilidad regulatoria.

**Esta batalla ES el gap de investigación.**

**Prosa para §2.2**:

> La revisión de la literatura evidencia una fragmentación sistemática en los sistemas de auditoría asistida por inteligencia artificial. Los trabajos pueden agruparse en cuatro categorías según el módulo que abordan: (1) sistemas de predicción tabular (Chen et al., 2016 [A01]; Ke et al., 2017 [A02]; Prokhorenkova et al., 2018 [A03]); (2) sistemas de forecasting financiero (Lim et al., 2021 [B01]; Challu et al., 2023 [B06]); (3) sistemas de detección de anomalías (Liu et al., 2008 [C01]; Han et al., 2022 [C04]); y (4) sistemas de generación de reportes con LLMs (Kadir et al., 2025 [E03]; Park, 2024 [E04]).
>
> Trabajos como AuditCopilot (Kadir et al., 2025 [E03]) logran una integración parcial al combinar detección de anomalías con generación de reportes LLM, pero excluyen módulos de predicción tabular validados y forecasting. El framework de Park (2024 [E04]) integra múltiples LLMs pero opera en el dominio de mercados financieros de alta frecuencia, sin abordaje de trazabilidad regulatoria interna. AuditMAI (Knoblauch & Großmann, 2024 [E06]) propone una infraestructura conceptual para auditoría continua de sistemas IA, pero audita la IA en sí, no usa IA para auditar transacciones.
>
> La Tabla 2.X resume comparativamente los sistemas más cercanos a la propuesta de esta tesis:

**[INSERTAR TABLA COMPARATIVA — ver Sección 6 de este plan]**

> Esta revisión sistemática permite identificar la brecha de investigación central: **no existe en la literatura un sistema que integre de manera modular, con evaluación empírica y trazabilidad regulatoria, los cuatro componentes** (predicción tabular GBDT evaluada en benchmark estándar + forecasting multi-horizonte + ensemble de detectores de anomalías calibrado con ADBench + generación de reportes LLM-RAG con SHAP como fundamento determinista). Esta tesis propone y evalúa dicha integración, alineada con la Resolución SBS N° 053-2023 y el marco NIST AI RMF.

**Citas clave**: A01, A02, A03, B01, B06, C01, C04, E03, E04, E06, F05, G01
**⚠️ DATO FALTANTE**: Confirmar que AuditCopilot (E03) no tiene módulo de forecasting ni predicción GBDT evaluada — verificar el paper completo antes de hacer esta afirmación.

---

### BATALLA 5 — Contexto Internacional vs. Contexto Peruano (Originalidad local)

**Posición de la tesis**: La mayoría de los sistemas de la literatura operan en contextos regulatorios de EE.UU., Europa o Asia. Esta tesis es la primera en aplicar un sistema integrado de estas características en el contexto regulatorio peruano (SBS N° 053-2023, Ley N° 31814).

**Prosa para §2.2**:

> El contexto regulatorio en el que opera un sistema de auditoría con IA define directamente sus requisitos de diseño. La literatura internacional se ha desarrollado principalmente bajo marcos europeos (EU AI Act, 2024 [G03]; GDPR) y norteamericanos (NIST AI RMF, 2023 [F05]; OCC guidance). El BIS (Prenio & Yong, 2024 [G04]) documenta cómo jurisdicciones como FINMA (Suiza), OCC (EE.UU.) y MAS (Singapur) exigen explicabilidad diferenciada según el impacto de la decisión.
>
> En el contexto peruano, el marco regulatorio ha madurado significativamente. La Resolución SBS N° 053-2023 establece por primera vez en el Perú lineamientos obligatorios de gobernanza, trazabilidad y explicabilidad para modelos de riesgo en entidades financieras, con implementación gradual hasta enero de 2026. El Decreto Supremo N° 115-2025-PCM (Presidencia del Consejo de Ministros, 2025 [G02]), reglamento de la Ley N° 31814, clasifica los sistemas de IA financiera como de "alto riesgo" y exige supervisión humana en las decisiones automáticas.
>
> Esta tesis es, en el conocimiento de los autores, la primera propuesta académica en el Perú que diseña explícitamente un sistema de auditoría con IA desde sus fundamentos para cumplir con ambas normativas. La Resolución SBS N° 053-2023 y el D.S. N° 115-2025-PCM no son contexto; son restricciones de diseño verificables que diferencian a esta investigación de sus antecedentes internacionales.

**Citas clave**: G01, G02, G03, G04, F05
**⚠️ DATO FALTANTE**: Verificar texto exacto de la Resolución SBS N° 053-2023 en sbs.gob.pe — confirmar que habla de "gestión de riesgos de modelo" y el cronograma de enero 2026. Igualmente verificar D.S. 115-2025-PCM en elperuano.pe.

---

## 5. CAPÍTULO II §2.3 — BASES TEÓRICAS

### Estructura propuesta

La sección de Bases Teóricas desarrolla los fundamentos conceptuales de cada módulo del sistema. Se proponen 6 sub-secciones.

---

### §2.3.1 Gradient Boosting Decision Trees (GBDT)

**Conceptos a desarrollar** (con citas):
- Definición de boosting y diferencia con bagging (citar: cualquier texto ML estándar + A01)
- Gradient Boosting: minimización de función de pérdida mediante descenso de gradiente en espacio funcional
- XGBoost: regularización L1/L2 + manejo de valores faltantes (Chen & Guestrin, 2016 [A01])
- LightGBM: GOSS + histogram-based learning + leaf-wise growth (Ke et al., 2017 [A02])
- CatBoost: Ordered Target Statistics para categóricas (Prokhorenkova et al., 2018 [A03])
- Justificación de superioridad en tabular: Grinsztajn et al. (2022 [A06])

**⚠️ DATO FALTANTE**: Añadir referencia de texto base de gradient boosting (Friedman, 2001 — "Greedy Function Approximation"). Verificar si está en el repositorio de referencias de la tesis.

---

### §2.3.2 Detección de Anomalías: Fundamentos y Ensemble

**Conceptos a desarrollar**:
- Taxonomía de anomalías: puntuales, contextuales, colectivas
- Métricas de evaluación: AUC-ROC, PR-AUC (precisión-recall), F1 con umbral óptimo
- Isolation Forest: fundamento matemático (longitud esperada de camino de aislamiento) (Liu et al., 2008 [C01])
- LOF: ratio de densidad local respecto a k-vecinos (Breunig et al., 2000 [C02])
- Deep SVDD: hipersfera mínima en espacio latente (Ruff et al., 2018 [C03])
- ECOD: función de distribución empírica acumulada multivariada (Li et al., 2022 [C05])
- Estrategia de ensemble: votación por mayoría vs. promedio de scores vs. meta-clasificador
- ADBench como referencia de evaluación (Han et al., 2022 [C04])
- Infraestructura: PyOD (Zhao et al., 2019 [C06])

---

### §2.3.3 Forecasting con Transformers: TFT y debate contemporáneo

**Conceptos a desarrollar**:
- Mecanismo de atención: self-attention y multi-head attention
- TFT: arquitectura completa (gating, atención, cuantil loss) (Lim et al., 2021 [B01])
- Debate Transformers en TS: crítica de Zeng et al. (2023 [B02]) — DLinear supera a Transformers en benchmarks clásicos
- Respuesta: PatchTST (Nie et al., 2023 [B05]) — tokenización por patches resuelve permutation-invariance
- iTransformer (Liu et al., 2024 [B03]) — tokenización por variable en lugar de por tiempo
- Chronos (Ansari et al., 2024 [B04]) — foundation model para TS, paradigma emergente
- N-HiTS (Challu et al., 2023 [B06]) — alternativa sin Transformer para horizontes largos
- **Posición de la tesis**: TFT se elige por su interpretabilidad incorporada (relevante para auditoría), no solo por rendimiento

**⚠️ DATO FALTANTE**: Justificar por qué se incluye forecasting en el pipeline de auditoría. Ejemplos de uso: predecir volúmenes de transacciones futuras para calibrar umbrales de detección, forecasting de riesgo de cartera, predicción de patrones estacionales en fraude. Este argumento debe estar desarrollado en §3.1 (arquitectura) pero referenciado aquí.

---

### §2.3.4 Explicabilidad (XAI) y Valores de Shapley

**Conceptos a desarrollar**:
- Taxonomía XAI: modelo-agnóstico vs. específico, local vs. global, post-hoc vs. inherente
- LIME: aproximación local con modelo sustituto (Ribeiro et al., 2016 [F02])
- SHAP: valores de Shapley — fundamento en teoría de juegos cooperativos (Lundberg & Lee, 2017 [F01])
  - Propiedades: eficiencia, simetría, dummy, aditividad
  - SHAP vs. LIME: SHAP garantiza consistencia global; LIME puede ser inestable
- TreeSHAP: cálculo exacto en O(TLD²) para árboles (citar: Lundberg et al., 2020 — extensión de F01)
- SHAP Stability Index: coherencia forense (citar: [G06])
- Aplicación regulatoria: SHAP como evidencia auditable (EU AI Act Art. 13 [G03], BIS [G04])

**⚠️ DATO FALTANTE**: Incluir referencia a la extensión TreeSHAP (Lundberg et al., 2020, Nature Machine Intelligence). Verificar si está en el repositorio.

---

### §2.3.5 Modelos de Lenguaje y RAG para Auditoría

**Conceptos a desarrollar**:
- LLMs: arquitectura Transformer, atención, tokenización, preentrenamiento
- In-context learning: zero-shot, few-shot, chain-of-thought
- Hallucination en LLMs: tipos y causas ([G10], 2026)
- RAG: Retrieval-Augmented Generation — recuperación de contexto relevante antes de generación (Schneider et al., 2025 [E05])
  - RAG básico: dense retrieval + generación
  - RAG avanzado: GraphRAG, Self-RAG, RAPTOR (mencionar como trabajo futuro)
- TabLLM: serialización tabular para LLMs (Hegselmann et al., 2023 [E01])
- Integración SHAP + LLM: el LLM como "narrador" de valores deterministas
- Evaluación de texto generado: ROUGE (Lin, 2004), BLEU (Papineni et al., 2002) — referencias de tesis_v2

---

### §2.3.6 Gobernanza de IA y MLOps

**Conceptos a desarrollar**:
- Deuda técnica en ML: Sculley et al. (2015 [F04]) — pipelines entangled, configuration debt, undeclared consumers
- MLOps: definición, ciclo de vida, componentes (Kreuzberger et al., 2023 [F03])
  - CI/CD para modelos, monitoreo de drift, reentrenamiento automatizado
- NIST AI RMF: 4 funciones (Govern, Map, Measure, Manage) (NIST, 2023 [F05])
- Datasheets for Datasets: documentación del dataset BAF Benchmark (Gebru et al., 2021 [F06])
- Model Cards: documentación de modelos XGBoost, TFT (Mitchell et al., 2019 [F07])
- Continuous Auditing Framework: Patel et al. (2024 [D03]) — caso: reducción de 45 a 5 días en ciclo de auditoría
- Marco CAQ: Auditing in the Age of Generative AI (CAQ, 2024 [D04]) — posición oficial de Big 4

---

## 6. ANÁLISIS COMPARATIVO CON COMPETIDORES DIRECTOS

### Tabla 2.X — Comparativa de sistemas de auditoría con IA (para insertar en §2.2 Batalla 4)

| Característica | **Esta tesis** | AuditCopilot [E03] | Park 2024 [E04] | AuditMAI [E06] | G06 (Fraude ML+XAI) |
|----------------|---------------|-------------------|----------------|---------------|---------------------|
| **Predicción tabular GBDT** | ✅ XGB+LGBM+CatBoost | ❌ No especificado | ❌ No (solo LLMs) | ❌ No | ✅ Stacking Ensemble |
| **Benchmark estándar de evaluación** | ✅ BAF [D01] | ❌ Dataset propio | ❌ S&P 500 (mercado) | ❌ Conceptual | ⚠️ Dataset propio |
| **Forecasting de series temporales** | ✅ TFT [B01] | ❌ | ❌ | ❌ | ❌ |
| **Ensemble de detección de anomalías** | ✅ IF+LOF+SVDD (ADBench) | ⚠️ Parcial | ❌ | ❌ | ❌ |
| **Explicabilidad SHAP** | ✅ TreeSHAP | ❌ | ❌ | ❌ | ✅ SHAP+Anchor |
| **Generación LLM de reportes** | ✅ RAG determinista | ✅ LLM narrativo | ✅ Multi-agente LLM | ❌ Conceptual | ❌ |
| **Restricción anti-alucinación** | ✅ RAG+SHAP como fundamento | ❌ | ❌ | — | — |
| **Marco regulatorio explícito** | ✅ SBS+DS115+EU AI Act | ❌ | ❌ | ❌ | ❌ |
| **Contexto peruano** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Evaluación de usabilidad** | ✅ Con auditores | ❌ | ❌ | ❌ | ❌ |
| **Dominio de aplicación** | Auditoría empresarial | Asientos contables | Mercados financieros | Auditoría de IA | Fraude en estados financieros |
| **Venue** | UNSA 2026 | arXiv 2025 | arXiv 2024 | arXiv 2024 | JRFM 2025 |

**Conclusión de la tabla**: Esta tesis es la única propuesta que integra los 4 módulos del pipeline con evaluación empírica reproducible, trazabilidad regulatoria explícita y contexto peruano. El valor añadido respecto al trabajo más cercano (AuditCopilot) son los módulos de forecasting, el ensemble calibrado con ADBench, la restricción anti-alucinación del LLM, y el marco regulatorio peruano.

---

### Nota de diferenciación detallada con AuditCopilot (para incluir en §2.1 o §2.2)

> AuditCopilot (Kadir et al., 2025 [E03]) constituye el trabajo más cercano a esta propuesta en términos de objetivo. Sin embargo, tres diferencias fundamentales distinguen ambos sistemas: **primera**, AuditCopilot opera sobre asientos contables de doble entrada con un LLM que detecta Y explica, mientras esta tesis separa estrictamente la detección (GBDT+ensemble determinista) de la explicación (SHAP) y la narración (LLM-RAG), alineándose con los requisitos de trazabilidad del BIS (Prenio & Yong, 2024 [G04]); **segunda**, AuditCopilot no integra forecasting de series temporales ni módulo de predicción tabular validado en benchmarks reproducibles, limitando su capacidad a la revisión retrospectiva; **tercera**, AuditCopilot no aborda el marco regulatorio explícito ni la evaluación de usabilidad con auditores reales, componentes centrales de esta investigación. Esta tesis no compite con AuditCopilot; lo complementa con una arquitectura más completa y regulatoriamente fundada.

---

## 7. MATRIZ DE BRECHAS (GAP ANALYSIS)

### Tabla de brechas identificadas en la literatura

| Brecha | Descripción | Papers que la confirman | Cómo esta tesis la cierra |
|--------|-------------|------------------------|--------------------------|
| **B1: Fragmentación de módulos** | Los sistemas abordan predicción, detección, o reportes, pero no los cuatro integrados | E03, E04, G06, C04 | Arquitectura de 4 capas modulares evaluada como sistema integrado |
| **B2: Ausencia de evaluación en benchmark estándar** | Muchos sistemas usan datasets propios no reproducibles | D01, C04 | Uso de BAF Benchmark [D01] + metodología ADBench [C04] |
| **B3: LLM sin restricción anti-alucinación** | Sistemas con LLMs como agentes de decisión no controlan alucinaciones numéricas | G05, G10, G03 | LLM restringido a RAG sobre vectores SHAP deterministas |
| **B4: Falta de trazabilidad regulatoria** | Sistemas técnicamente sólidos sin alineación a marcos legales | G01, G02, G03, F05 | Diseño desde NIST AI RMF + SBS N°053-2023 + DS115 |
| **B5: Ausencia de contexto peruano** | Literatura dominada por contextos EE.UU./Europa/Asia | G01, G02 | Primera propuesta alineada con regulación peruana específica |
| **B6: Falta de evaluación de usabilidad** | Sistemas evaluados solo en métricas técnicas (AUC, F1) | D03, D04 | Experimento con auditores reales (tiempo-a-decisión, confianza) |
| **B7: Forecasting no integrado en auditoría** | El forecasting financiero se estudia separado de la detección de anomalías | B01, B02, B05 | Módulo TFT integrado al pipeline de auditoría continua |

---

## 8. CHECKLIST DE DATOS FALTANTES

Los siguientes datos son necesarios antes de defender la tesis. Organizados por urgencia:

### 🔴 URGENTE — Necesarios antes de comenzar experimentos

| # | Dato faltante | Dónde obtenerlo | Para qué sección |
|---|--------------|----------------|-----------------|
| 1 | **Tamaño del dataset principal agroexportador** | Empresa colaboradora / piloto anonimizado | §3.2, §2.2, §4 |
| 2 | **Texto exacto de Resolución SBS N° 053-2023** | sbs.gob.pe (buscar: resoluciones 2023) | §1.7.3, §2.2 Batalla 5, §2.3.6 |
| 3 | **Texto del D.S. N° 115-2025-PCM** | busquedas.elperuano.pe | §1.7.3, §2.2 Batalla 5 |
| 4 | **Definición precisa del contexto agroexportador** | Documentación de la empresa colaboradora | §1.1, §3.1 |
| 5 | **Validación de accesibilidad de fuentes públicas** | MIDAGRI, SENASA, SENAMHI, INEI, SUNAT, FAOSTAT, UN Comtrade | §3.2 |

### 🟡 IMPORTANTE — Necesarios antes de escribir Capítulo II definitivo

| # | Dato faltante | Dónde obtenerlo | Para qué sección |
|---|--------------|----------------|-----------------|
| 6 | **Estadística agroexportadora peruana** | MIDAGRI, INEI, SUNAT, datosabiertos.gob.pe | §1.1 |
| 7 | **Autores completos de G05, G06, G07, G10** | Verificar URLs proporcionadas: mdpi.com, arxiv.org | §2.2, bibliografía APA |
| 8 | **Referencia TreeSHAP** (Lundberg et al., 2020) | Google Scholar: `"from local explanations to global understanding" TreeSHAP 2020` | §2.3.4 |
| 9 | **Referencia Friedman 2001 (Gradient Boosting)** | Google Scholar: `"Greedy function approximation gradient boosting machine" Friedman 2001` | §2.3.1 |
| 10 | **Validación de fuentes sectoriales** | SENASA, SENAMHI y MIDAGRI | §3.2 |

### 🟢 RECOMENDABLE — Fortalecen pero no bloquean

| # | Dato faltante | Para qué sección |
|---|--------------|-----------------|
| 11 | Cifra: impacto económico de pérdidas por mermas/logística | §1.7.2 Justificación Económica |
| 12 | Datos de adopción de IA en agroindustria peruana | §1.1 Realidad problemática |
| 13 | Publicación del benchmark/dataset agrícola que usemos como comparativo | §2.1, §3.2 |
| 14 | Referencias de clima, exportaciones y productividad agrícola | §2.3, §3.2 |
| 15 | N-BEATS o alternativas de forecasting si se conservan comparaciones | §2.3.3, §2.1 |

---

## 10. PLANIFICACIÓN INTEGRADA DE DATOS

### Fuentes y tipo de datos

| Fuente | Tipo de datos | Uso en la tesis | Estado |
|---|---|---|---|
| MIDAGRI | precios mayoristas, volúmenes, boletines | contexto sectorial, estacionalidad, variables macro | identificado |
| SENASA | plagas, alertas fitosanitarias, certificaciones | variables de riesgo, calidad y cumplimiento | identificado |
| SENAMHI | temperatura, lluvia, humedad, avisos | forecasting, variación operativa, anomalías climáticas | identificado |
| INEI | actividad económica, índices de precios | contexto macro y validación externa | identificado |
| SUNAT | exportaciones, aduanas, tributación | contexto comercial y trazabilidad sectorial | identificado |
| FAOSTAT | producción, rendimiento, área cosechada | comparativo internacional y benchmark de producción | identificado |
| UN Comtrade | comercio exterior por producto/país | contexto de exportación y validación complementaria | identificado |
| datosabiertos.gob.pe | datasets públicos del Estado | repositorio de apoyo y alternativa de búsqueda | identificado |
| Datos internos empresa | producción, inventario, calidad, logística | dataset principal para modelado y detección | por confirmar |
| Datos externos complementarios | tipo de cambio, clima, precios internacionales | covariables para explicación y forecasting | por integrar |

### Cómo se integran

- **Predicción**: producción, volumen, rendimiento, inventario, demanda, precios.
- **Detección de anomalías**: mermas, retrasos, desviaciones de calidad, eventos climáticos atípicos.
- **Explicabilidad**: variables que más influyen en desviaciones o riesgo operativo.
- **Reportes**: contexto, causa probable, impacto y recomendación accionable.

### Qué aumentó en la planificación

- [x] Estructura completa de la tesis documentada
- [x] Capítulo I consolidado como base estable
- [x] Capítulo II consolidado y alineado al nuevo enfoque
- [x] Mapa de fuentes de datos agroexportadores definido
- [x] Plan de iteración futura con datos internos + fuentes públicas
- [ ] Capítulo III migrado completamente al dominio agroexportador
- [ ] Capítulo IV con resultados reales
- [ ] Capítulo V con conclusiones finales

---

## APÉNDICE A — ORDEN DE REDACCIÓN RECOMENDADO

Para máxima eficiencia, redactar en este orden:

1. **Primero**: Verificar datos urgentes (items 1-5 del checklist)
2. **Segundo**: Redactar §2.3 Bases Teóricas (no requiere datos empíricos, solo literatura)
3. **Tercero**: Completar §2.1 Antecedentes con los 7 antecedentes del plan
4. **Cuarto**: Redactar §2.2 Estado del Arte con las 5 batallas y la tabla comparativa
5. **Quinto**: Ajustar §1.1 y §1.7 del Capítulo I con citas SBS y estadísticas peruanas
6. **Sexto**: Revisar coherencia de toda la cadena argumental: brecha → hipótesis → metodología

---

## APÉNDICE B — CITAS BiBTeX PENDIENTES DE AGREGAR A refs.bib

Los siguientes papers NO están actualmente en `refs.bib` (según la revisión de los archivos existentes) y deben agregarse:

```
A05: @inproceedings{arik2021tabnet, ...}               # TabNet AAAI 2021
A06: @inproceedings{grinsztajn2022trees, ...}          # Grinsztajn NeurIPS 2022
B02: @inproceedings{zeng2023dlinear, ...}              # Zeng AAAI 2023
B03: @inproceedings{liu2024itransformer, ...}          # iTransformer ICLR 2024
B04: @article{ansari2024chronos, ...}                  # Chronos TMLR 2024
B05: @inproceedings{nie2023patchtst, ...}              # PatchTST ICLR 2023
C05: @article{li2022ecod, ...}                         # ECOD TKDE 2022
C06: @article{zhao2019pyod, ...}                       # PyOD JMLR 2019
D03: @article{patel2024auditing, ...}                  # Patel IRJMETS 2024
D04: @techreport{caq2024genai, ...}                    # CAQ 2024
E01: @inproceedings{hegselmann2023tabllm, ...}         # TabLLM AISTATS 2023
E04: @misc{park2024llm, ...}                           # Park arXiv 2024
E05: @article{schneider2025rag, ...}                   # RAG BISE 2025
E06: @misc{auditmai2024, ...}                          # AuditMAI arXiv 2024
F01: @inproceedings{lundberg2017shap, ...}             # SHAP NeurIPS 2017
F02: @inproceedings{ribeiro2016lime, ...}              # LIME KDD 2016
F03: @article{kreuzberger2023mlops, ...}               # MLOps IEEE Access 2023
F04: @inproceedings{sculley2015hidden, ...}            # Hidden Debt NeurIPS 2015
F05: @techreport{nist2023aimf, ...}                    # NIST AI RMF 2023
F06: @article{gebru2021datasheets, ...}                # Datasheets CACM 2021
F07: @inproceedings{mitchell2019modelcards, ...}       # Model Cards FAccT 2019
G01: @techreport{sbs2023resolucion, ...}               # SBS N°053-2023
G02: @techreport{pcm2025ds115, ...}                    # DS 115-2025-PCM
G03: @legislation{eu2024aiact, ...}                    # EU AI Act 2024
G04: @techreport{prenio2024managing, ...}              # BIS FSI 2024
G05: @misc{barclays2025beyond, ...}                    # Barclays arXiv 2025
G06: @article{mongolia2025fraud, ...}                  # JRFM 2025
G07: @article{forensic2025intrusion, ...}              # Applied Sciences 2025
G08: @article{thanathamathee2024shap, ...}             # ESJ 2024
G09: @misc{almalki2025fraud, ...}                      # Almalki arXiv 2025
G10: @misc{survey2026hallucination, ...}               # arXiv 2026
```

**⚠️ IMPORTANTE**: Antes de agregar a refs.bib, verificar DOIs y venues exactos según las notas del documento de referencias. Los marcados con "Solo arXiv" deben citarse como preprints con `howpublished = {arXiv preprint arXiv:XXXX.XXXXX}`.

---

*Plan generado el 2026-05-15. Actualizar este documento cuando se completen los datos faltantes marcados con ⚠️.*
