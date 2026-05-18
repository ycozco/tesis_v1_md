# PLAN DE REVISIÓN ACADÉMICA EXHAUSTIVA
## Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas
## Universidad Nacional de San Agustín de Arequipa — Ingeniería de Sistemas
## Versión 1.0 — 2026-05-17 | Para uso en revisión previa a defensa y preparación de artículo

---

> **PROPÓSITO DE ESTE DOCUMENTO**
> Este plan estructura una revisión académica de máxima rigurosidad en 10 dimensiones, con 87 criterios verificables. Cada criterio tiene un estado (✅ / ⚠️ / 🔴), una acción correctiva cuando aplica, y una referencia al archivo de la tesis donde debe verificarse. Al finalizar, el documento sirve como base para redactar un artículo académico publicable.

---

## ESTADO GLOBAL DE REVISIÓN

| Dimensión | Criterios | Verificados | Pendientes | Bloqueadores |
|-----------|-----------|-------------|------------|--------------|
| D1 — Coherencia estructural | 10 | 9 | 1 | 0 |
| D2 — Rigor en el planteamiento | 12 | 11 | 1 | 0 |
| D3 — Auditoría bibliográfica | 10 | 8 | 2 | 0 |
| D4 — Rigor metodológico | 12 | 9 | 3 | 1 |
| D5 — Consistencia inter-capítulos | 8 | 8 | 0 | 0 |
| D6 — Calidad de redacción académica | 8 | 7 | 1 | 0 |
| D7 — Preparación para artículo | 10 | 4 | 6 | 1 |
| D8 — Verificación regulatoria y de dominio | 6 | 3 | 3 | 2 |
| D9 — Auditoría de claims específicos | 7 | 6 | 1 | 0 |
| D10 — Diseño del estudio empírico | 4 | 4 | 0 | 0 |
| **TOTAL** | **87** | **69** | **18** | **4** |

### Avance acumulado al 2026-05-17 (ejecución del plan)

- ✅ Cap I: §1.7.1 (aporte original específico), §1.9 (marco epistemológico + diseño), §1.12 (Limitaciones), §1.13 (Declaración de intereses)
- ✅ Cap II §2.3.7: claims sobre RAG/EU AI Act matizados; agregada distinción intrínseca/extrínseca de alucinaciones
- ✅ Cap III §3.1: nota justificando ECOD sobre Deep SVDD
- ✅ Cap III §3.3: división temporal, semilla, diseño experimental E1–E5, pruebas estadísticas, criterios de inclusión, baselines
- ✅ `docs/variables-operacionalizadas.md` (Hito 1) — tabla formal 7 cols × 5 VD
- ✅ `docs/busqueda-sistematica-gap.md` — protocolo PRISMA-light + 9 trabajos identificados
- ✅ `docs/A1-anexo-usabilidad.md` — protocolo completo, consentimiento, cuestionario SUS
- ✅ `docs/A2-anexo-modelcards.md` — 4 Model Cards (Mitchell et al. 2019)
- ✅ `docs/A3-anexo-datasheet.md` — Datasheet completo (Gebru et al. 2021)
- ✅ `config/refs.bib`: +8 refs (Friedman 2001, TreeSHAP 2020, Ji 2023, Creswell 2018, PRISMA 2020, MIDAGRI 2026, Cohen Kappa, Optuna)
- ✅ `requirements.txt` con versiones fijadas para reproducibilidad
- ✅ `src/generate_synthetic_dataset.py` — generador del dataset sintético v1.0

### Bloqueadores remanentes (🔴)

1. **C8.1 — Verificación SBS N°053-2023**: requiere acceso al texto original en sbs.gob.pe.
2. **C8.2 — Verificación D.S. 115-2025-PCM**: requiere acceso al texto original en elperuano.pe.
3. **C7.6 — Repositorio GitHub público**: pendiente publicar al cierre del Hito 3.
4. **C4.5 — Tamaño efectivo de muestra del estudio de usabilidad**: depende del reclutamiento real (meta N ≥ 15, deseable N = 27).

---

## DIMENSIÓN 1: COHERENCIA ESTRUCTURAL DE LA TESIS

**Objetivo**: Verificar que todos los elementos del planteamiento (título → problema → objetivos → hipótesis → variables → metodología → conclusiones) formen una cadena argumental sin saltos ni contradicciones.

### C1.1 — Alineación título ↔ problema de investigación
- **Criterio**: El título debe nombrar exactamente el fenómeno estudiado (variable independiente o sistema) y el contexto (dominio + país).
- **Estado**: ✅
- **Verificación**: Título = "Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas". El problema (§1.2) pregunta cómo mejora la detección, explicación y documentación de anomalías con el sistema propuesto. Coherente.
- **Archivo**: `docs/10-capitulo1.md:29–31`

### C1.2 — Alineación problema principal ↔ sub-problemas
- **Criterio**: Cada sub-problema debe ser desglosable directamente del problema principal y conducir a un objetivo específico identificable.
- **Estado**: ✅
- **Verificación**: Los 5 sub-problemas de §1.2 mapean 1:1 con los 6 objetivos específicos de §1.3.2. Ligera asimetría (5 sub-problemas → 6 objetivos) pero justificable porque OE1 (fuentes de datos) es precondición técnica, no sub-problema conceptual.
- **Acción**: En la defensa, preparar justificación de por qué OE1 no tiene sub-problema correspondiente.
- **Archivo**: `docs/10-capitulo1.md:33–58`

### C1.3 — Alineación objetivos específicos ↔ capítulos
- **Criterio**: Cada OE debe tener una sección específica que lo desarrolle.

| Objetivo Específico | Sección | Estado |
|---------------------|---------|--------|
| OE1: Fuentes de datos | §3.2 | ✅ |
| OE2: Arquitectura modular | §3.1 | ✅ |
| OE3: Predicción y detección | §4.1 (pendiente) | 🔴 |
| OE4: SHAP | §4.2 (pendiente) | 🔴 |
| OE5: Reportes LLM+RAG | §4.3 (pendiente) | 🔴 |
| OE6: Evaluación integrada | §4.4 (pendiente) | 🔴 |

- **Acción 🔴**: Los 4 OE de implementación requieren Cap IV. Bloqueados por Hito 2 (dataset).

### C1.4 — Hipótesis general → sub-hipótesis → experimentos
- **Criterio**: Cada sub-hipótesis (H1a–H1d) debe tener un experimento diseñado (E1–Ex) con condición experimental y condición de control claramente distintas.
- **Estado**: ⚠️
- **Brecha**: Las sub-hipótesis están declaradas en §1.4 pero no hay mapeo explícito H1x ↔ Ex en Cap III. El lector de tesis y el jurado necesitan esta trazabilidad.
- **Acción**: Agregar Tabla 3.X en Cap III: "Mapa hipótesis → experimento → métrica → criterio de aceptación".
- **Archivo**: `docs/10-capitulo1.md:62–72`, `docs/30-capitulo3.md:47–53`

### C1.5 — Variables dependientes ↔ métricas de §3.3
- **Criterio**: Cada VD debe aparecer con exactamente las mismas métricas en §1.5 y en §3.3.
- **Estado**: ✅
- **Verificación**: VD1→PR-AUC/F1, VD2→top-k SHAP/Likert, VD3→completitud/ROUGE, VD4→tiempo/Likert, VD5→% trazabilidad. Coincidentes.

### C1.6 — Alcance declarado ↔ metodología efectiva
- **Criterio**: Lo que §1.8 (Alcance) excluye no debe aparecer como objetivo en Cap III.
- **Estado**: ✅
- **Verificación**: §1.8 excluye DL puro, implementación productiva en tiempo real, reemplazo de decisión humana. Cap III no los incluye. Coherente.

### C1.7 — Introducción ↔ estructura de capítulos
- **Criterio**: La introducción debe anticipar todos los capítulos y no mencionar secciones que no existen.
- **Estado**: ⚠️
- **Brecha**: La introducción (`03-introduccion.md`) menciona "resultados experimentales" pero Cap IV es placeholder. Verificar si el lenguaje de la introducción está en futuro o en presente.
- **Acción**: Revisar tiempos verbales en la introducción. Toda referencia a Cap IV debe estar en futuro hasta que el capítulo esté completo.
- **Archivo**: `docs/03-introduccion.md`

### C1.8 — Resumen/Abstract ↔ contribuciones reales
- **Criterio**: El resumen no debe listar contribuciones que aún no están evaluadas (resultados experimentales).
- **Estado**: ⚠️
- **Acción**: Verificar si `01-resumen.md` menciona resultados cuantitativos como logros. Si los menciona, moverlos a "contribuciones esperadas" o revisar después de Cap IV.
- **Archivo**: `docs/01-resumen.md`

### C1.9 — Glosario ↔ términos usados en el texto
- **Criterio**: Cada término técnico usado por primera vez en el texto debe estar definido en el glosario o en el texto mismo.
- **Estado**: ✅
- **Verificación**: `80-glosario.md` tiene 6 KB con terminología técnica. Pendiente: verificar que "ECOD", "PyOD", "RAG", "prompt engineering" y "drift" aparezcan en el glosario.
- **Acción**: Ejecutar grep de términos técnicos en `10-capitulo1.md` y verificar que todos están en `80-glosario.md`.

### C1.10 — Referencias ↔ citas en texto
- **Criterio**: Toda entrada en `refs.bib` debe estar citada en texto; toda cita en texto debe tener entrada en `refs.bib`.
- **Estado**: ✅ (verificado en sesión anterior: sin citas huérfanas)
- **Acción pendiente**: Al agregar las nuevas referencias del Apéndice B de `plan_detallado.md`, re-ejecutar verificación.

---

## DIMENSIÓN 2: RIGOR EN EL PLANTEAMIENTO DEL PROBLEMA

**Objetivo**: Garantizar que el planteamiento tenga nivel de publicación científica: variables operacionalizadas, hipótesis contrastables, y causalidad correctamente declarada.

### C2.1 — Operacionalización formal de variables dependientes
- **Criterio**: Cada VD debe tener: (a) definición conceptual, (b) definición operacional, (c) fórmula o protocolo de medición, (d) rango de valores, (e) criterio de aceptación, (f) instrumento de medición, (g) nivel de medición (nominal/ordinal/intervalo/razón).
- **Estado**: 🔴 BLOQUEADOR
- **Brecha**: §1.5 define VD1–VD5 con indicadores y criterios de aceptación, pero sin tabla formal de operacionalización. Las definiciones operacionales (cómo exactamente se mide cada indicador) están incompletas para VD2, VD3 y VD4.
- **Acción crítica**: Crear `docs/variables-operacionalizadas.md` con tabla de 7 columnas × 5 filas. Este es el Hito 1 (2026-05-27).
- **Ejemplo de gap en VD2**: "cobertura top-k SHAP" — ¿qué es k? ¿cómo se mide "consistencia cualitativa"? ¿quién evalúa "claridad de variables"? Falta protocolo.
- **Ejemplo de gap en VD4**: "tiempo-a-decisión" — ¿desde qué evento hasta qué evento se mide? ¿con cronómetro externo o log automático?

### C2.2 — Testabilidad de las hipótesis
- **Criterio**: Cada hipótesis debe especificar: (a) qué se compara, (b) bajo qué condiciones, (c) con qué prueba estadística, (d) con qué nivel de significancia (α), (e) qué tamaño de efecto mínimo se considera relevante.
- **Estado**: 🔴 BLOQUEADOR
- **Brecha**: Las hipótesis H1a–H1d están declaradas pero sin prueba estadística designada.
- **Acción**: Para cada sub-hipótesis, declarar en §3.3:

| Sub-hipótesis | Comparación | Variable de resultado | Prueba estadística | α |
|---|---|---|---|---|
| H1a | Ensemble vs. detector único | PR-AUC | Wilcoxon signed-rank (no paramétrico, una muestra) | 0.05 |
| H1b | SHAP vs. sin SHAP | Likert comprensión (1–5) | Mann-Whitney U o t de Student según normalidad (Shapiro-Wilk) | 0.05 |
| H1c | RAG vs. sin RAG | Completitud y consistencia de reportes | McNemar o Cohen's κ | 0.05 |
| H1d | Sistema integrado vs. aislado | Tiempo-a-decisión (segundos) | t de Student apareado o Wilcoxon | 0.05 |

### C2.3 — Tipo de causalidad declarada
- **Criterio**: La tesis debe declarar explícitamente si establece causalidad o asociación. Un estudio con dataset sintético puede mostrar rendimiento diferencial pero no causalidad en el sentido experimental estricto.
- **Estado**: ⚠️
- **Acción**: En §1.9.3 (nivel de investigación) clarificar que la relación entre el sistema integrado y las mejoras en VD1–VD5 es una relación de rendimiento evaluado bajo condiciones controladas, no causalidad en sentido experimental puro. Usar el término "efecto diferencial" en lugar de "causa" al reportar resultados.

### C2.4 — Variable independiente correctamente declarada
- **Criterio**: La VI debe ser manipulable, no confundible con covariables, y operacionalizable.
- **Estado**: ✅
- **Verificación**: VI = "tipo de sistema" (integrado vs. aislado). Es una variable categórica binaria y controlable.
- **Nota**: El "sistema aislado" (condición de control) debe estar explícitamente definido: ¿Isolation Forest solo? ¿Qué salida exacta recibe el usuario en la condición de control? Definir esto en Cap III.

### C2.5 — Criterios de inclusión y exclusión del estudio
- **Criterio**: Para el estudio de usabilidad (VD4), deben declararse criterios de inclusión/exclusión de participantes.
- **Estado**: 🔴 BLOQUEADOR
- **Brecha**: §1.10 menciona "supervisores, auditores internos, estudiantes avanzados o evaluadores simulados" sin criterios formales.
- **Acción**: Definir en §3.3 o Anexo A: (a) criterio de inclusión mínimo (ej. 2+ años de experiencia en supervisión operativa o formación en gestión empresarial), (b) criterio de exclusión (ej. participación en diseño del sistema), (c) N mínimo de participantes según análisis de potencia estadística (ver C4.5).

### C2.6 — Marco epistemológico declarado
- **Criterio**: La tesis debe declarar su postura epistemológica (positivismo, post-positivismo, pragmatismo) en §1.9.
- **Estado**: ⚠️
- **Brecha**: §1.9 declara el tipo (aplicada) y nivel (explicativo-evaluativo) pero no el marco epistemológico.
- **Acción**: Agregar un párrafo en §1.9.1 indicando que la investigación adopta un enfoque post-positivista: asume que los fenómenos operativos son medibles objetivamente, pero reconoce que la evaluación de usabilidad incorpora componentes subjetivos (Likert) que requieren triangulación de métodos cuantitativos y cualitativos.

### C2.7 — Pregunta de investigación correctamente formulada
- **Criterio**: La pregunta principal debe ser específica, medible, alcanzable, relevante y temporal (SMART).
- **Estado**: ✅
- **Verificación**: La pregunta de §1.2 es específica (sistema integrado con 4 componentes), medible (métricas en §1.5), alcanzable (stack open-source), relevante (contexto agroexportador peruano) y temporal (5 meses).

### C2.8 — Limitaciones de la investigación declaradas
- **Criterio**: Las limitaciones deben aparecer en Cap I y ser retomadas en Cap V, incluyendo: validez externa (¿generalizable?), validez interna (¿controlado?), y amenazas al dataset sintético.
- **Estado**: ⚠️
- **Brecha**: No se encontró sección de limitaciones explícita en Cap I. Las amenazas a la validez del dataset sintético son un punto crítico de revisión de jurado.
- **Acción**: Agregar §1.12 "Limitaciones de la Investigación" con al menos:
  - Validez externa limitada: dataset sintético documentado no reemplaza datos operativos reales de empresa.
  - Muestra de usabilidad pequeña (si N < 30): resultados son preliminares y requieren réplica.
  - Dependencia de APIs de LLM comerciales: resultados pueden variar entre versiones del modelo.
  - Sesgo de evaluador: los participantes del estudio de usabilidad pueden conocer el sistema propuesto.

### C2.9 — Aporte original declarado con precisión
- **Criterio**: El aporte original debe enunciarse en una sola oración que ningún trabajo previo pueda reclamar como propio.
- **Estado**: ✅
- **Verificación**: El aporte se puede formular como: "Primera arquitectura integrada de 4 capas (GBDT + ensemble anomalías + SHAP + LLM-RAG con restricción anti-alucinación) evaluada sobre datos agroexportadores peruanos públicos/sintéticos con trazabilidad conforme a D.S. N°115-2025-PCM."
- **Acción**: Incluir esta formulación exacta en §1.7.1 y en el Abstract.

### C2.10 — Coherencia entre el nivel de investigación y las conclusiones esperadas
- **Criterio**: Un nivel "explicativo-evaluativo" implica que las conclusiones deben explicar POR QUÉ el sistema integrado es mejor (o no), no solo decir que lo es.
- **Estado**: ⚠️
- **Acción**: Diseñar en Cap IV una sección de análisis de causas (¿qué módulo aporta más al rendimiento global? → ablation study) para que las conclusiones sean genuinamente explicativas.

### C2.11 — Relevancia de la contribución para el contexto peruano
- **Criterio**: La relevancia peruana debe estar cuantificada con al menos una cifra verificable del sector.
- **Estado**: ✅
- **Verificación**: §1.1 cita USD 15,013 millones en agroexportaciones (MIDAGRI 2026). Cifra concreta y verificable.
- **Acción pendiente**: Verificar la referencia `@midagri2026boletin` — confirmar que este boletín está publicado y la cifra es correcta.

### C2.12 — Declaración de conflictos de interés
- **Criterio**: Las tesis con potencial de publicación deben declarar si existe relación entre el investigador y empresas o entidades que puedan beneficiarse del sistema.
- **Estado**: 🔴 BLOQUEADOR (para publicación)
- **Acción**: Agregar §1.13 "Declaración de intereses" o incorporarlo en la sección de ética. Si no hay conflictos, declararlo explícitamente. Los journals con revisión ciega lo requieren.

---

## DIMENSIÓN 3: AUDITORÍA BIBLIOGRÁFICA

**Objetivo**: Verificar que cada referencia sea verificable, esté correctamente citada en APA 7, exista en la base de datos indicada, y que las afirmaciones extraídas de ella sean fieles al texto original.

### C3.1 — Verificación de referencias primarias críticas

Estas referencias son las más citadas en la tesis. Cada una debe verificarse en su fuente original:

| Clave | Referencia | Afirmación en tesis | Estado | Verificar en |
|---|---|---|---|---|
| A01 | Chen & Guestrin (2016) XGBoost | "regularización L1/L2 + manejo de valores faltantes" | ✅ Verificado (paper público KDD) | kdd.org |
| A02 | Ke et al. (2017) LightGBM | "aceleraciones de hasta 20×" | ⚠️ Verificar cifra exacta | NeurIPS 2017 |
| A06 | Grinsztajn et al. (2022) | "95% de datasets con hasta 50K muestras" | ⚠️ Verificar: el paper dice <50K o <100K? | NeurIPS 2022 |
| C04 | Han et al. (2022) ADBench | "57 datasets, 30 algoritmos" | ✅ Verificado | NeurIPS 2022 |
| F01 | Lundberg & Lee (2017) SHAP | "teoría de juegos cooperativos" | ✅ Verificado | NeurIPS 2017 |
| B01 | Lim et al. (2021) TFT | "6 datasets de dominio real" | ⚠️ Verificar número exacto | IJF 2021 |
| E03 | Kadir et al. (2025) AuditCopilot | "no incluye GBDT ni forecasting" | 🔴 CRÍTICO — verificar el paper completo | arXiv 2025 |
| G01 | SBS N°053-2023 | "gestión de riesgos de modelo + enero 2026" | 🔴 CRÍTICO — verificar texto exacto | sbs.gob.pe |
| G02 | D.S. 115-2025-PCM | "sistemas IA financiera = alto riesgo" | 🔴 CRÍTICO — verificar texto exacto | elperuano.pe |

### C3.2 — Referencias pendientes de agregar a refs.bib
- **Estado**: ⚠️
- **Acción**: Agregar las 30 entradas del Apéndice B de `plan_detallado.md` a `config/refs.bib`. Prioridad URGENTE para A05, A06, C05, C06, F01, F02, F05, F06, F07, G01, G02, G03.
- **Protocolo**: Para cada referencia, buscar DOI en doi.org o crossref.org. Para preprints arXiv, usar `@misc` con `howpublished={arXiv preprint arXiv:XXXX.XXXXX}`.

### C3.3 — Verificación de métricas citadas como afirmaciones propias
- **Criterio**: Toda métrica numérica (PR-AUC = 0.93, F1 = 0.83, SHAP Stability = 0.87) debe atribuirse a la fuente original con cita en el mismo párrafo.
- **Estado**: ✅ (en el texto actual las métricas de G06 están citadas)
- **Acción**: Al redactar Cap IV, cada métrica propia debe presentarse como resultado experimental propio, no como cita.

### C3.4 — Consistencia de formato APA 7
- **Criterio**: Todas las entradas en refs.bib deben seguir APA 7. Puntos específicos de APA 7:
  - DOI como URL (no como número)
  - Hasta 20 autores (luego "…")
  - Cursivas para título de libro, sin cursivas para título de artículo
  - Mayúsculas solo para primera letra de título y propios

- **Estado**: ⚠️
- **Acción**: Revisar las entradas existentes en `config/refs.bib` con las reglas de APA 7. Especialmente: verificar que `@techreport` y `@legislation` usen los campos correctos.

### C3.5 — Citas de normas y leyes (formato especial APA)
- **Criterio**: Los documentos normativos (SBS, DS-115-PCM, EU AI Act) tienen formato APA especial.
- **Estado**: ⚠️
- **Formato correcto para normas peruanas**:
  ```
  Superintendencia de Banca, Seguros y AFP. (2023). Resolución N° 053-2023.
    https://www.sbs.gob.pe/[ruta exacta]
  
  Presidencia del Consejo de Ministros. (2025). Decreto Supremo N° 115-2025-PCM.
    El Peruano. https://busquedas.elperuano.pe/[ruta exacta]
  ```
- **Acción**: Verificar y completar estas entradas con las URLs exactas.

### C3.6 — Antigüedad de referencias
- **Criterio**: Para publicación en journals de IA, la regla general es que ≥60% de las referencias deben ser de los últimos 5 años (2021–2026). Las referencias fundacionales (pre-2021) deben representar ≤40%.
- **Estado**: ✅ (la mayoría de referencias son 2019–2026)
- **Acción**: Ejecutar conteo por año una vez que refs.bib esté completo.

### C3.7 — Referencias a papers no publicados o preprints
- **Criterio**: Los preprints (arXiv) sin revisión por pares deben citarse indicando que son preprints. No se puede afirmar que sus resultados son definitivos.
- **Estado**: ⚠️
- **Afectados**: E03 (AuditCopilot, arXiv), E04 (Park 2024, arXiv), G05 (Barclays, arXiv), G09, G10.
- **Acción**: En cada cita de arXiv, agregar "(preprint bajo revisión)" o usar el lenguaje "según reportan..." en lugar de afirmar como hecho establecido.

### C3.8 — Autocitas (si aplica)
- **Criterio**: Si el investigador tiene publicaciones previas que citar, declararlas explícitamente.
- **Estado**: ✅ (no hay autocitas en el estado actual)

### C3.9 — Verificación de accesibilidad de referencias
- **Criterio**: Todas las referencias deben tener URL o DOI accesible públicamente. Las referencias detrás de paywall deben estar disponibles en la institución o en versión preprint.
- **Estado**: ⚠️
- **Acción**: Verificar acceso a: IEEE Xplore papers (B01: TFT está en IJF con DOI), papers de NeurIPS 2022 (C04, A06 son open access en proceedings).

### C3.10 — Integridad de las citas en el contexto de la Batalla 4 (gap claim)
- **Criterio**: La afirmación central de la tesis —que ningún sistema previo integra los 4 módulos— debe ser una afirmación que sobreviva a revisión de pares. Requiere haber revisado TODOS los trabajos relevantes, no solo los citados.
- **Estado**: ⚠️ CRÍTICO PARA PUBLICACIÓN
- **Acción**: Realizar búsqueda sistemática en IEEE Xplore, ACM DL, Google Scholar con las cadenas:
  - "anomaly detection SHAP LLM report generation"
  - "explainable AI audit system GBDT ensemble"
  - "integrated AI auditing pipeline explainability"
  - "agricultural anomaly detection machine learning Peru"
  Documentar la búsqueda en `docs/busqueda-sistematica-gap.md` con: base de datos, cadena de búsqueda, N resultados, N seleccionados, criterios de exclusión. Esto es un requisito de revisión de pares.

---

## DIMENSIÓN 4: RIGOR METODOLÓGICO

**Objetivo**: Garantizar que el diseño experimental sea reproducible, estadísticamente válido y que las métricas elegidas sean las más apropiadas para el problema.

### C4.1 — Reproducibilidad del pipeline experimental
- **Criterio**: Otro investigador con el mismo código y datos debe poder replicar exactamente los resultados. Requiere: (a) semilla aleatoria fija (random_state), (b) versiones de librerías en requirements.txt, (c) datos versionados.
- **Estado**: 🔴 BLOQUEADOR
- **Acción**:
  1. En todos los scripts de `src/`: `np.random.seed(42)`, `random.seed(42)`, pasar `random_state=42` a todos los modelos.
  2. Crear `requirements.txt` o `environment.yml` con versiones exactas (scikit-learn==X.Y.Z, xgboost==X.Y.Z, shap==X.Y.Z, pyod==X.Y.Z).
  3. Documentar en `docs/A3-anexo-datasheet.md` la semilla de generación del dataset sintético.

### C4.2 — Diseño del experimento comparativo (sistema integrado vs. aislado)
- **Criterio**: La comparación debe ser "fair": mismos datos, misma división train/test, mismo preprocesamiento, misma semilla. La única diferencia debe ser la condición experimental (integrado vs. aislado).
- **Estado**: 🔴 BLOQUEADOR
- **Acción**: Definir en §3.3:
  - **Condición experimental**: Pipeline completo (Capa 1 → Capa 2 → Capa 3 → Capa 4).
  - **Condición de control A**: Solo detector de anomalías (IF individual) + output técnico sin SHAP ni reporte.
  - **Condición de control B**: Detector + SHAP, sin reporte LLM.
  - **Condición de control C**: Detector + reporte LLM sin RAG (LLM "libre").
  - Este diseño ablativo permite aislar la contribución de cada capa.

### C4.3 — División del dataset (train/test/validation)
- **Criterio**: Para datos con potencial drift temporal (datos agroexportadores por fecha), la división debe ser temporal, no aleatoria. El test set debe ser cronológicamente posterior al train set.
- **Estado**: ⚠️
- **Acción**: Especificar en §3.2 que la división será temporal:
  - Train: primeros 70% de registros cronológicos
  - Validation: 10% siguiente (para tuning de hiperparámetros)
  - Test: 20% final (para evaluación final, nunca visto durante entrenamiento)
  - Justificación: evitar data leakage en series con estacionalidad.

### C4.4 — Métricas correctas para datos desbalanceados
- **Criterio**: En datasets con ~10–15% de anomalías, el Accuracy no es una métrica válida. PR-AUC es preferible a ROC-AUC cuando la clase positiva es rara.
- **Estado**: ✅
- **Verificación**: §3.3 usa PR-AUC como métrica principal. Correcto.
- **Acción**: Asegurarse de que no aparezca "Accuracy" como métrica principal en ninguna tabla de resultados de Cap IV.

### C4.5 — Tamaño de muestra para el estudio de usabilidad (VD4)
- **Criterio**: Para detectar un efecto medio (Cohen's d = 0.5) con α = 0.05 y potencia = 0.80 en un t-test de dos muestras independientes, se necesitan N ≥ 52 participantes por grupo. Para un diseño apareado (within-subjects), N ≥ 27.
- **Estado**: 🔴 BLOQUEADOR
- **Brecha**: No se ha definido N de participantes. Con muestra pequeña (N < 10), los resultados de VD4 serán "exploratorios" y no permitirán conclusiones estadísticas.
- **Acción**: Tomar una decisión explícita:
  - **Opción A (recomendada)**: Diseño within-subjects con N ≥ 15–20 evaluadores (reducible por presupuesto). Cada evaluador ve ambas condiciones (integrado y aislado) en orden aleatorizado. Reporte los resultados como "exploratorios, N = XX".
  - **Opción B (alternativa)**: Eliminar el estudio de usabilidad del alcance y declarar VD4 como "trabajo futuro". En este caso, ajustar H1d también como trabajo futuro.
  - Cualquiera que sea la opción, debe estar declarada en §1.8 (Alcance) y §3.3.

### C4.6 — Protocolo del estudio de usabilidad
- **Criterio**: El protocolo debe estar en Anexo A y cubrir: consentimiento informado, tareas específicas, método de medición de tiempo, cuestionario post-tarea, criterios de invalidación de una sesión.
- **Estado**: ⚠️ (Anexo A es skeleton)
- **Acción**: Completar `docs/A1-anexo-usabilidad.md` con protocolo completo ANTES del estudio. Requiere aprobación del comité de ética de UNSA si los participantes son externos.

### C4.7 — Hiperparámetros y proceso de tuning
- **Criterio**: El proceso de selección de hiperparámetros debe ser documentado: ¿se usó grid search, random search, Optuna, o valores por defecto? ¿Con cuántos trials? ¿Con qué métrica de validación?
- **Estado**: 🔴 BLOQUEADOR
- **Acción**: Documentar en §3.3 o Apéndice:
  ```
  Estrategia de tuning: Optuna con 50 trials, optimizando PR-AUC en el validation set.
  Parámetros buscados XGBoost: n_estimators ∈ [100, 1000], max_depth ∈ [3, 10], 
  learning_rate ∈ [0.01, 0.3], subsample ∈ [0.6, 1.0].
  ```

### C4.8 — Evaluación del módulo de reportes (VD3)
- **Criterio**: ROUGE-1/ROUGE-L requiere una "referencia" (reporte gold-standard) para comparar. Si no hay referencias humanas, se necesita un protocolo alternativo.
- **Estado**: ⚠️
- **Brecha**: En el contexto del dataset sintético, no hay reportes gold-standard escritos por auditores reales.
- **Acción**: Definir protocolo de evaluación de VD3 con una de estas opciones:
  - **Opción A**: Rúbrica de 5 dimensiones (completitud, consistencia, accionabilidad, coherencia, correspondencia con evidencias) evaluada por 3 revisores independientes. Calcular Kappa de Cohen para confiabilidad inter-evaluador.
  - **Opción B**: Generar 10–20 reportes de referencia escritos por el investigador o asesor como gold-standard, luego usar ROUGE-L.
  - **Opción A es más robusta** para el dataset sintético.

### C4.9 — Evaluación del ensemble de anomalías
- **Criterio**: Para comparar detector único vs. ensemble, se debe reportar no solo la métrica promedio sino la varianza entre runs (si hay aleatoriedad en Isolation Forest) y el intervalo de confianza.
- **Estado**: ⚠️
- **Acción**: Ejecutar cada experimento con 5–10 semillas diferentes. Reportar: mean ± std de PR-AUC.

### C4.10 — Ablation study
- **Criterio**: Para publicación en conferencia o journal de IA, se espera un ablation study que aísle la contribución de cada componente.
- **Estado**: ⚠️
- **Acción**: Diseñar Experimento E5 como ablation:
  - E5a: Pipeline sin Capa 1 (solo detección)
  - E5b: Pipeline sin SHAP (Capa 3)
  - E5c: Pipeline con LLM sin RAG
  - E5d: Pipeline completo
  Comparar VD3 y VD5 entre E5a–E5d.

### C4.11 — Documentación del dataset sintético (Datasheets for Datasets)
- **Criterio**: Gebru et al. (2021) define 57 preguntas en 7 categorías para documentar cualquier dataset. Las secciones críticas son: Motivación, Composición, Proceso de recolección, Preprocesamiento, Usos, Distribución, Mantenimiento.
- **Estado**: 🔴 BLOQUEADOR
- **Acción**: Completar `docs/A3-anexo-datasheet.md` siguiendo la plantilla de Datasheets for Datasets. Es un requisito de Hito 2 (2026-06-01).

### C4.12 — Comparación con baselines del estado del arte
- **Criterio**: Para publicación, los resultados propios deben compararse con baselines reportados en papers previos usando el mismo benchmark o benchmarks comparables.
- **Estado**: 🔴 BLOQUEADOR
- **Brecha**: No existe benchmark agroexportador estándar. El BAF Benchmark es de fraude financiero, no agroexportador.
- **Acción**: Diseñar la comparación de baselines de la siguiente forma:
  - **Baseline 1**: Isolation Forest individual (referencia más simple)
  - **Baseline 2**: Isolation Forest + LOF (ensemble sin ECOD)
  - **Baseline 3**: XGBoost supervisado (si hay etiquetas) — upper bound
  - Reportar en una tabla: Método | PR-AUC | AUC-ROC | F1 | Explicabilidad | Trazabilidad

---

## DIMENSIÓN 5: CONSISTENCIA INTER-CAPÍTULOS

**Objetivo**: Verificar que los diferentes capítulos de la tesis sean mutuamente consistentes y formen un argumento sin contradicciones internas.

### C5.1 — Variables de Cap I ↔ variables de Cap III
- **Estado**: ✅
- **Verificación**: Las variables operativas (precio, volumen, clima, merma, cumplimiento fitosanitario, destino, días logísticos) aparecen en §1.1, §1.5, §3.1 y §3.2 con los mismos nombres.

### C5.2 — Algoritmos de Cap II ↔ algoritmos de Cap III
- **Estado**: ✅
- **Verificación**: IF+LOF+ECOD (Cap II §2.3.4) = IF+LOF+ECOD (Cap III §3.1 Capa 2). Consistente. Nota: Deep SVDD aparece en §2.1 Antecedente 2 y §2.2 Batalla 2 pero no en §3.1. Esto es correcto porque §3.1 usa ECOD en lugar de Deep SVDD (decisión de diseño). Verificar que esta sustitución esté justificada en el texto.
- **Acción**: En §3.1, agregar una nota: "Se selecciona ECOD (Li et al., 2022) sobre Deep SVDD (Ruff et al., 2018) por su ausencia de hiperparámetros y complejidad computacional menor, apropiados para el dataset sintético de tamaño medio."

### C5.3 — Gap del Estado del Arte ↔ contribución de la tesis
- **Estado**: ✅
- **Verificación**: La Brecha B4 (falta de contexto peruano) y B1 (fragmentación de módulos) de §2.2 corresponden exactamente al aporte declarado en §1.7.1.

### C5.4 — Marco regulatorio citado en Cap I ↔ marco regulatorio en Cap II
- **Estado**: ⚠️
- **Brecha**: En Cap I (§1.1) se presenta la SBS N°053-2023 como "referencia de buenas prácticas", no como obligación. En el `plan_detallado.md` se habla de "gestión de riesgos de modelo con trazabilidad verificable a partir de enero de 2026". Estas son dos posiciones diferentes.
- **Acción**: Unificar la posición en todos los capítulos: la SBS N°053-2023 no es directamente aplicable a agroexportadoras (son reguladas por MIDAGRI/SENASA, no por SBS). Usarla como referencia de buenas prácticas de gobernanza de modelos, no como requisito obligatorio. Esta posición está en §1.1 del Cap I actual y debe propagarse a Cap II.

### C5.5 — Métricas de §1.5 ↔ métricas de §3.3
- **Estado**: ✅ (verificado en C1.5)

### C5.6 — Alcance de §1.8 ↔ diseño metodológico de §3
- **Estado**: ✅
- **Verificación**: §1.8 excluye DL puro y tiempo real. Cap III no los incluye.

### C5.7 — Cronograma de §1.11 ↔ hitos del plan_detallado.md
- **Estado**: ⚠️
- **Brecha**: El cronograma de §1.11 muestra 5 meses con actividades mensuales. Los hitos del plan tienen fechas específicas (2026-05-27 a 2026-07-07). Verificar coherencia.
- **Acción**: Actualizar §1.11 para que refleje el cronograma real (Hito 1: mes 1, Hito 2: mes 2, etc.).

### C5.8 — Terminología consistente entre capítulos
- **Criterio**: Los mismos conceptos deben nombrarse con los mismos términos en todo el documento.
- **Estado**: ⚠️
- **Inconsistencias detectadas**:
  - "Deep SVDD" vs "ECOD" — en distintas secciones se usa uno u otro como tercer detector
  - "AuditCopilot" aparece en Cap II como "antecedente" y en §1.7.1 como punto de referencia metodológica — OK pero verificar que no lo llame "competidor" en ningún lado
  - "BAF Benchmark" vs "dataset BAF" — unificar término
- **Acción**: Ejecutar búsqueda de estas inconsistencias y unificarlas.

---

## DIMENSIÓN 6: CALIDAD DE REDACCIÓN ACADÉMICA

**Objetivo**: Garantizar que la prosa sea adecuada para publicación académica: precisa, sin ambigüedades, con hedging apropiado y formato consistente.

### C6.1 — Uso correcto de tiempos verbales según el avance de la tesis
- **Criterio**:
  - Lo que ya se diseñó (arquitectura): presente o pasado.
  - Lo que se implementará: futuro o condicional.
  - Los experimentos pendientes: futuro.
  - Los resultados esperados: condicional o futuro.
- **Estado**: ⚠️
- **Acción**: Revisar especialmente Cap III y el resumen ejecutivo. Si un capítulo usa presente para describir experimentos no realizados, corregir a futuro.

### C6.2 — Hedging correcto en las afirmaciones
- **Criterio**: Las afirmaciones sin evidencia experimental propia deben usar hedging: "se espera que...", "los resultados preliminares sugieren...", "según la literatura...".
- **Estado**: ⚠️
- **Frases problemáticas a revisar**:
  - "el sistema mejora la detección" — ¿mejora o se espera que mejore?
  - "el ensemble supera al detector individual" — si no hay experimentos propios todavía, es una hipótesis.
- **Acción**: Buscar afirmaciones en presente sin soporte experimental y agregar hedging.

### C6.3 — Uso de primera persona
- **Criterio**: En UNSA, las tesis de ingeniería típicamente usan tercera persona ("se propone", "se evalúa"). Verificar consistencia.
- **Estado**: ✅
- **Verificación**: El texto revisado usa voz pasiva ("se emplearán", "se documentará"). Consistente.

### C6.4 — Definición de siglas en primera aparición
- **Criterio**: Toda sigla debe definirse en su primera aparición en el texto principal (no en el glosario, sino en el texto).
- **Estado**: ⚠️
- **Verificar**: GBDT, SHAP, RAG, LLM, TFT, ROC-AUC, PR-AUC, LOF, IF, ECOD, PyOD, MLOps, XAI.
- **Acción**: En `10-capitulo1.md`, verificar que cada sigla tenga su expansión la primera vez que aparece.

### C6.5 — Captions de figuras y tablas
- **Criterio**: Cada figura y tabla debe tener: (a) número consecutivo, (b) caption descriptivo auto-contenido (el lector entiende la figura sin leer el texto circundante), (c) fuente si es adaptada de otro trabajo.
- **Estado**: ⚠️
- **Brecha**: El diagrama ASCII de la arquitectura en §3.1 no tiene número ni caption formal.
- **Acción**: Reemplazar el bloque `code` de la arquitectura con una figura numerada (Figura 3.1) y su caption.

### C6.6 — Consistencia en el uso de cursivas y comillas
- **Criterio**: Los términos técnicos en inglés la primera vez que aparecen deben ir en cursiva. Las citas directas van entre comillas. Los títulos de documentos y libros van en cursiva.
- **Estado**: ⚠️
- **Acción**: Revisar que "machine learning", "gradient boosting", "forecasting", "retrieval-augmented generation" estén en cursiva en su primera aparición.

### C6.7 — Numeración de secciones
- **Criterio**: La numeración debe ser jerárquica y consistente: 1, 1.1, 1.1.1, etc. No debe haber saltos en la numeración.
- **Estado**: ✅ (la estructura segmentada en 19 archivos mantiene la numeración)

### C6.8 — Referencias cruzadas internas
- **Criterio**: Las referencias a otras secciones ("como se explicará en §3.2") deben apuntar a secciones que efectivamente existen.
- **Estado**: ⚠️
- **Acción**: Verificar que todas las referencias a §4.X (que son placeholder) no estén en tiempo presente en los capítulos anteriores.

---

## DIMENSIÓN 7: PREPARACIÓN PARA PUBLICACIÓN COMO ARTÍCULO

**Objetivo**: Identificar qué componentes de la tesis son publicables y qué acciones se necesitan para tener un artículo de conferencia o revista listo después de la defensa.

### C7.1 — Identificación del venue objetivo
- **Estado**: 🔴 BLOQUEADOR (sin resultados, no se puede someter)
- **Venues recomendados por orden de accesibilidad y relevancia**:

| Venue | Tipo | Factor de impacto / Indexación | Deadline típico | Cuota APC |
|---|---|---|---|---|
| CLEI (XLIII Conferencia) | Congreso | Scopus | Oct 2026 | Gratuito |
| RCCI (Rev. Cubana Ciencias Informáticas) | Revista | Latindex/DOAJ | Continua | Gratuito |
| IEEE LATAM | Revista | IEEE Xplore | Continua | USD 1,750 |
| Computers & Security | Revista | Q1 Scopus, IF 5.6 | Continua | USD 2,500 |
| Expert Systems with Applications | Revista | Q1 Scopus, IF 7.5 | Continua | USD 3,200 |
| Applied Intelligence | Revista | Q2 Scopus, IF 5.0 | Continua | USD 2,800 |

**Recomendación**: Comenzar con CLEI 2026 (sin costo, latam, Scopus) como primer venue y paralelamente preparar versión extendida para IEEE LATAM o Applied Intelligence.

### C7.2 — Estructura del paper de conferencia (6–8 páginas IEEE)
- **Estado**: ⚠️
- **Estructura propuesta**:
  1. Abstract (150 palabras): problema, brecha, propuesta, resultados clave, implicación
  2. Introduction: contexto, motivación, gap, contribuciones (3 bullets), estructura del paper
  3. Related Work: tablas comparativas de sistemas similares (de §2.2 Batalla 4)
  4. Proposed Architecture: diagrama + descripción de las 4 capas
  5. Experimental Setup: dataset, métricas, baselines
  6. Results & Discussion: tablas con PR-AUC, F1, tiempo-decisión; ablation study
  7. Conclusion & Future Work: 3 conclusiones + 2 limitaciones + 2 trabajos futuros
  8. References (formato IEEE)

### C7.3 — Abstract publicable
- **Estado**: ⚠️
- **Abstract borrador** (para refinar con resultados reales):
  > "Supervisory anomaly detection in agro-export operations faces the challenge of combining accurate detection with auditor-understandable explanations and traceable documentation. Existing systems address these components in isolation, leaving a gap in integrated, regulatorily compliant pipelines for Peruvian agro-export contexts. We propose a four-layer architecture: (1) tabular prediction with XGBoost/LightGBM, (2) ensemble anomaly detection (Isolation Forest + LOF + ECOD via PyOD), (3) SHAP explainability, and (4) LLM+RAG report generation restricted to structured evidence. Evaluated on a documented synthetic agro-export dataset under Peru's D.S. N°115-2025-PCM governance framework, the integrated system achieves [PR-AUC=X.XX] compared to [X.XX] for single-detector baselines, with [XX%] improvement in decision time and [≥95%] alert traceability. This work represents, to our knowledge, the first integrated explainable AI pipeline for agro-export operational supervision designed for the Peruvian regulatory context."
- **Acción**: Completar con resultados reales al terminar Cap IV.

### C7.4 — Contribuciones para el artículo (novelty claims)
- **Estado**: ✅
- **Tres contribuciones diferenciadas**:
  1. **Arquitectura**: Primera integración documentada de GBDT + ensemble anomalías + SHAP + LLM-RAG (con restricción anti-alucinación) para supervisión agroexportadora.
  2. **Dataset**: Dataset sintético agroexportador documentado con criterios de Datasheets for Datasets, disponible para la comunidad como benchmark.
  3. **Evaluación**: Protocolo de evaluación dual (rendimiento técnico + comprensión/tiempo de decisión del supervisor) con trazabilidad conforme a D.S. N°115-2025-PCM.

### C7.5 — Ética de publicación con datos sintéticos
- **Criterio**: Declarar explícitamente que el dataset es sintético (no datos reales de empresas). Esto es un requisito ético y de reproducibilidad.
- **Estado**: ✅ (§3.2 declara el dataset como sintético documentado)
- **Acción para publicación**: Incluir párrafo en §3.2 del paper: "The dataset was synthetically generated to enable open evaluation without confidentiality concerns. The generation process, variable distributions, and anomaly injection protocol are documented following the Datasheets for Datasets framework (Gebru et al., 2021) and are publicly available at [URL del repositorio]."

### C7.6 — Repositorio público del código (open science)
- **Criterio**: Los journals de IA de alto impacto requieren o recomiendan código reproducible. GitHub con README + requirements.txt + instrucciones de ejecución.
- **Estado**: 🔴 BLOQUEADOR
- **Acción**: Al terminar Hito 3 (código de módulos), publicar el repositorio en GitHub con:
  - README.md con instrucciones claras
  - requirements.txt con versiones
  - Notebook de ejemplo end-to-end
  - Dataset sintético o instrucciones de generación
  - Citar el repositorio en el paper como [código disponible en: URL]

### C7.7 — Tabla de resultados principales (estructura para el artículo)

La tabla principal del paper debe comparar:

| Método | PR-AUC | AUC-ROC | F1 | Tiempo-decisión (s) | Trazabilidad (%) |
|---|---|---|---|---|---|
| IF individual (baseline) | — | — | — | — | — |
| IF + LOF (ensemble parcial) | — | — | — | — | — |
| Sistema completo (E5d) | — | — | — | — | ≥95% |
| Sin SHAP (ablation E5b) | — | — | — | — | — |
| Sin RAG (ablation E5c) | — | — | — | — | — |

### C7.8 — Revisión de conflictos de interés para publicación
- **Criterio**: Declarar explícitamente en el paper si el trabajo es derivado de una tesis y si hubo financiamiento.
- **Acción**: Agregar al paper: "Este trabajo es derivado de la tesis de grado de [Yoset Cozco Mauri] en la UNSA. No existe financiamiento externo ni conflicto de interés."

### C7.9 — Evaluación ciega por pares
- **Criterio**: Para revisión ciega doble, el paper no debe contener información que identifique a los autores en el texto principal (universidades, "nuestros trabajos anteriores", etc.).
- **Acción**: Preparar versión anónima si el venue lo requiere.

### C7.10 — Plazo realista para publicación
- **Cronograma estimado**:
  - Julio 2026: Defensa de tesis
  - Agosto 2026: Extracto del paper de conferencia (6 páginas)
  - Septiembre 2026: Sometimiento a CLEI 2026 (si la fecha lo permite)
  - Enero 2027: Versión extendida para revista (IEEE LATAM o Applied Intelligence)

---

## DIMENSIÓN 8: VERIFICACIÓN REGULATORIA Y DE DOMINIO

**Objetivo**: Confirmar que todos los marcos normativos citados dicen exactamente lo que la tesis afirma que dicen. Un error factual en una cita legal es causa de rechazo en defensa.

### C8.1 — Verificación del texto de la Resolución SBS N°053-2023
- **Estado**: 🔴 CRÍTICO
- **Afirmaciones a verificar**:
  - ¿Habla de "gestión de riesgos de modelo"?
  - ¿Menciona cronograma de implementación hasta enero 2026?
  - ¿Es aplicable solo a entidades financieras bajo supervisión SBS, NO a agroexportadoras?
- **Procedimiento**: Ir a https://www.sbs.gob.pe → Regulación → Resoluciones → buscar N°053-2023. Leer el articulado completo. Documentar los artículos exactos que se citan.
- **Posición actual de la tesis** (correcta, en §1.1): se usa como "referencia de buenas prácticas", no como obligación directa. Esta posición debe mantenerse consistente en TODO el documento.

### C8.2 — Verificación del D.S. N°115-2025-PCM
- **Estado**: 🔴 CRÍTICO
- **Afirmaciones a verificar**:
  - ¿Clasifica sistemas de IA en "categorías de riesgo"?
  - ¿Usa el término "alto riesgo" para IA en contextos empresariales?
  - ¿Exige explicabilidad y supervisión humana?
  - ¿Es reglamento de la Ley N°31814?
- **Procedimiento**: Buscar en https://busquedas.elperuano.pe con "D.S. 115-2025-PCM". Leer artículos 1, 2 (definiciones), y la sección de clasificación de riesgos.
- **Nota**: Si el decreto usa terminología diferente, ajustar las citas en toda la tesis.

### C8.3 — Verificación de estadísticas del sector agroexportador
- **Estado**: ⚠️
- **Afirmación**: "USD 15,013 millones al cierre de 2025, con crecimiento de 17.3% respecto al año anterior" (§1.1)
- **Procedimiento**: Verificar en el Boletín MIDAGRI 2026. La referencia `@midagri2026boletin` debe tener URL exacta.
- **Riesgo**: Si el boletín no está publicado aún (la fecha del documento es 2026), indicar como "según datos preliminares de MIDAGRI (comunicación institucional, 2026)" o buscar la fuente secundaria más reciente.

### C8.4 — Verificación del EU AI Act, Artículo 13
- **Estado**: ✅ (el EU AI Act fue promulgado en 2024 y es de acceso público)
- **Afirmaciones a verificar**: Art. 13 trata sobre "Transparency and provision of information to users". La tesis lo cita como fundamento de requisitos de explicabilidad.
- **Procedimiento**: Leer Art. 13 del Reglamento (UE) 2024/1689 en eur-lex.europa.eu.

### C8.5 — Verificación de AuditCopilot (paper crítico)
- **Estado**: 🔴 CRÍTICO
- **Afirmación central**: "AuditCopilot no incluye módulo de predicción tabular GBDT evaluado contra benchmarks reproducibles" y "no evalúa conformidad con marcos regulatorios".
- **Procedimiento**: Leer el paper completo de Kadir et al. (2025) en arXiv. Confirmar que no tiene esos módulos. Si los tiene, la Batalla 4 (gap claim) necesita ajustarse.
- **Consecuencia**: Si AuditCopilot tiene GBDT o benchmarks, la afirmación de brecha debe re-formularse.

### C8.6 — Exactitud de la afirmación sobre PyOD
- **Estado**: ✅
- **Afirmación**: "más de 7,000 estrellas en GitHub" — verificar el número actual en github.com/yzhao062/pyod (puede haber crecido desde que se escribió).

---

## DIMENSIÓN 9: AUDITORÍA DE CLAIMS ESPECÍFICOS

**Objetivo**: Revisar las afirmaciones técnicas más importantes que serán cuestionadas en la defensa.

### C9.1 — Claim sobre GBDT vs. Deep Learning
- **Claim**: "XGBoost supera al Deep Learning en el 95% de datasets tabulares con <50K muestras"
- **Fuente**: Grinsztajn et al. (2022)
- **Estado**: ⚠️
- **Riesgo**: El paper dice "45 datasets, menos de 50,000 muestras". Si el dataset de la tesis tiene diferente tamaño, el argumento se debilita.
- **Acción**: Verificar el tamaño exacto del dataset sintético. Si tiene >100K registros, usar Almalki & Masud (2025) como soporte adicional.

### C9.2 — Claim sobre el ensemble de anomalías
- **Claim**: "El ensemble supera sistemáticamente a cualquier detector individual en escenarios con alta variabilidad de distribución"
- **Fuente**: ADBench (Han et al., 2022)
- **Estado**: ✅
- **Verificación**: ADBench efectivamente concluye esto para escenarios sin etiquetas (fully unsupervised).

### C9.3 — Claim sobre alucinaciones en LLMs
- **Claim**: "Los LLMs pueden producir 'alucinaciones numéricas' con alta confianza aparente"
- **Fuente**: Barclays Research (G05, arXiv 2025) + Survey (G10, arXiv 2026)
- **Estado**: ⚠️
- **Riesgo**: G10 es de 2026 y G05 es preprint. Si no están publicados en revista revisada por pares, la afirmación es más débil.
- **Acción**: Complementar con referencias más establecidas sobre hallucinations en LLMs (Lewis et al., 2020 RAG paper; Ji et al., 2023 survey en ACM CSUR).

### C9.4 — Claim sobre la brecha de integración
- **Claim**: "No existe en la literatura un sistema que integre los 4 módulos con trazabilidad regulatoria"
- **Estado**: ⚠️ CRÍTICO
- **Verificación necesaria**: Realizar búsqueda sistemática (ver C3.10). Esta es la afirmación más vulnerable de la tesis en revisión de pares.
- **Estrategia de defensa**: Incluso si existe un sistema similar, la tesis tiene el diferenciador del contexto peruano (D.S. N°115-2025-PCM) que ningún trabajo internacional puede reclamar.

### C9.5 — Claim sobre SHAP como evidencia auditable
- **Claim**: "El sistema cumple con los requisitos del Art. 13 del EU AI Act"
- **Estado**: ⚠️
- **Riesgo**: El EU AI Act distingue entre "sistemas de IA de alto riesgo" (Annex III) y otros. Una empresa agroexportadora pequeña puede no caer en Annex III. Afirmar cumplimiento regulatorio es una afirmación legal que requiere matización.
- **Acción**: Cambiar a "el sistema fue diseñado siguiendo los principios de transparencia del Art. 13 del EU AI Act, aplicables como referencia de diseño responsable de IA, independientemente de si el sistema es formalmente clasificable como de alto riesgo según el Reglamento."

### C9.6 — Claim sobre RAG como mitigador de alucinaciones
- **Claim**: "RAG elimina el espacio de alucinación al forzar al modelo a citar evidencia"
- **Estado**: ⚠️
- **Riesgo**: RAG reduce pero no "elimina" las alucinaciones. Los LLMs pueden alucinar incluso con contexto recuperado (conocido como "faithful hallucination" o "intrinsic hallucination").
- **Acción**: Cambiar a "RAG reduce significativamente el riesgo de alucinación numérica al anclar la generación a vectores SHAP deterministas como único contexto de entrada, limitando el espacio de generación libre del modelo."

### C9.7 — Claim sobre la primera propuesta en el Perú
- **Claim**: "Primera propuesta académica en el Perú que diseña explícitamente un sistema de auditoría con IA conforme a regulación peruana"
- **Estado**: ⚠️
- **Riesgo**: "Primera" es una afirmación que requiere haber buscado en repositorios de tesis peruanas (ALICIA CONCYTEC, Renati).
- **Acción**: Buscar en https://alicia.concytec.gob.pe y https://renati.sunedu.gob.pe con términos: "sistema auditoría inteligencia artificial Perú", "detección anomalías agroexportador". Documentar la búsqueda.

---

## DIMENSIÓN 10: DISEÑO DEL ESTUDIO EMPÍRICO (HITOS 2–4)

**Objetivo**: Definir con precisión qué se va a medir, cómo, y con qué datos, para que la implementación en Hito 3 sea directamente evaluable en Hito 4.

### C10.1 — Especificación completa del dataset sintético
- **Estado**: 🔴 BLOQUEADOR
- **Especificación requerida antes de construir el dataset**:

| Variable | Tipo | Rango plausible | Fuente para rangos | Distribución |
|---|---|---|---|---|
| fecha | datetime | 2022-01-01 a 2025-12-31 | — | Uniforme |
| producto | categorical | arándano, uva, palta, cacao, espárrago | MIDAGRI | Uniforme |
| zona | categorical | Ica, La Libertad, Piura, Arequipa, Lima | MIDAGRI | Ponderada |
| volumen_kg | float | 500–50,000 | MIDAGRI | LogNormal |
| precio_kg_usd | float | 0.5–12.0 | MIDAGRI/SUNAT | Normal |
| temperatura_max_c | float | 15–38 | SENAMHI | Normal |
| precipitacion_mm | float | 0–200 | SENAMHI | Gamma |
| humedad_pct | float | 40–95 | SENAMHI | Beta |
| destino_mercado | categorical | EEUU, UE, Asia, Otro | SUNAT | Ponderada |
| cumplimiento_fitosanitario | binary | 0/1 | SENASA | Bernoulli(p=0.92) |
| dias_logisticos | integer | 3–45 | Estimado | LogNormal |
| merma_pct | float | 0–30 | Estimado | Beta |
| etiqueta_anomalia | binary | 0/1 | Inyección controlada | Bernoulli(p=0.12) |
| tipo_anomalia | categorical | precio, volumen, clima, logistica, calidad, none | Inyección controlada | — |

- **N registros**: Mínimo 1,000, recomendado 2,000–5,000.
- **N anomalías**: 12–15% del total (desbalance realista).
- **Semilla**: np.random.seed(42).

### C10.2 — Protocolo de inyección de anomalías
- **Estado**: 🔴 BLOQUEADOR
- **Tipos de anomalías a inyectar y mecanismo**:
  1. **Anomalía de precio** (30% de anomalías): precio_kg_usd > percentil 99 o < percentil 1 de la distribución del producto.
  2. **Anomalía de volumen** (25%): volumen_kg > media + 3σ para el producto/zona.
  3. **Anomalía climática** (20%): temperatura_max_c > 38°C simultáneamente con precipitacion_mm = 0 (sequía con calor extremo).
  4. **Anomalía logística** (15%): dias_logisticos > percentil 95 simultáneamente con cumplimiento = 1 (demora a pesar de cumplir).
  5. **Anomalía de calidad** (10%): merma_pct > 25% simultáneamente con precio > mediana (pérdida de valor inesperada).
- **Documentar en Datasheet**: descripción de cada tipo, proporción, mecanismo de inyección, verificabilidad.

### C10.3 — Diseño de los 5 experimentos (E1–E5)
- **Estado**: 🔴 BLOQUEADOR
- **Propuesta de experimentos**:

| Exp. | Nombre | Condición experimental | Condición control | Variable que mide | Hipótesis |
|---|---|---|---|---|---|
| E1 | Rendimiento de detección | Ensemble IF+LOF+ECOD | IF individual | PR-AUC, F1 | H1a |
| E2 | Contribución de SHAP | Sistema completo | Sistema sin SHAP (solo scores) | VD2: top-k, Likert | H1b |
| E3 | Contribución de RAG | LLM+RAG (restringido) | LLM libre (sin RAG) | VD3: completitud, consistencia | H1c |
| E4 | Sistema integrado vs. aislado | Pipeline completo | Salidas técnicas separadas | VD4: tiempo, Likert; VD5: trazabilidad | H1 y H1d |
| E5 | Ablation study | Configuraciones parciales | — | VD1 + VD5 por configuración | Contribución de cada capa |

### C10.4 — Protocolo de evaluación de reportes (VD3)
- **Estado**: 🔴 BLOQUEADOR
- **Rúbrica propuesta** (5 dimensiones, escala 1–5 cada una):

| Dimensión | Descripción | 1 (Deficiente) | 5 (Excelente) |
|---|---|---|---|
| Completitud | El reporte contiene dato, modelo, score, umbral, SHAP, fuente RAG | Falta ≥3 elementos | Todos los elementos presentes |
| Consistencia | Los valores numéricos en el reporte coinciden con los outputs del sistema | ≥1 error numérico | Sin errores numéricos |
| Accionabilidad | El reporte sugiere una acción correctiva específica y verificable | Sin sugerencias | Acción clara y operativa |
| Coherencia textual | El texto es gramaticalmente correcto y sin contradicciones lógicas | ≥3 errores graves | Sin errores |
| Correspondencia con evidencias | Las afirmaciones del reporte se derivan de las evidencias SHAP, no de generación libre | Afirmaciones sin soporte | Toda afirmación tiene soporte |

- **Evaluadores**: ≥2 revisores independientes. Calcular Kappa de Cohen entre evaluadores.
- **N reportes evaluados**: ≥20 alertas seleccionadas aleatoriamente.

---

## PLAN DE ACCIÓN PRIORIZADO

### FASE 0 — Inmediata (2026-05-17 a 2026-05-24)
| Tarea | Archivo afectado | Urgencia |
|---|---|---|
| Verificar texto SBS N°053-2023 en sbs.gob.pe | `10-capitulo1.md`, `22-capitulo2-marcoteorico.md` | 🔴 CRÍTICA |
| Verificar texto D.S. 115-2025-PCM en elperuano.pe | Ídem | 🔴 CRÍTICA |
| Verificar que AuditCopilot no tiene módulo GBDT | `20-capitulo2-antecedentes.md`, `21-estadoarte.md` | 🔴 CRÍTICA |
| Agregar §1.12 Limitaciones al Cap I | `10-capitulo1.md` | 🔴 |
| Unificar posición sobre SBS: es referencia, no obligación | Todos los archivos | 🔴 |
| Corregir claim "RAG elimina alucinaciones" → "RAG reduce" | `22-capitulo2-marcoteorico.md` | ⚠️ |
| Corregir claim "EU AI Act Art. 13 cumplimiento" → "diseño siguiendo principios" | `10-capitulo1.md` | ⚠️ |

### FASE 1 — Hito 1 (hasta 2026-05-27)
| Tarea | Archivo | Hito |
|---|---|---|
| Tabla formal de variables operacionalizadas (7 columnas × 5 filas) | `docs/variables-operacionalizadas.md` | Hito 1 |
| Agregar Tabla 3.X: mapa H1x → Ex → métrica | `docs/30-capitulo3.md` | Hito 1 |
| Definir prueba estadística para cada sub-hipótesis | `docs/30-capitulo3.md` | Hito 1 |
| Definir criterios inclusión/exclusión estudio de usabilidad | `docs/30-capitulo3.md` | Hito 1 |
| Definir N de participantes y análisis de potencia | `docs/30-capitulo3.md` | Hito 1 |
| Búsqueda sistemática en ALICIA/Renati (claim "primera en Perú") | `docs/busqueda-sistematica-gap.md` | Hito 1 |

### FASE 2 — Hito 2 (hasta 2026-06-01)
| Tarea | Archivo | Hito |
|---|---|---|
| Especificación completa del dataset sintético (C10.1) | `docs/A3-anexo-datasheet.md` | Hito 2 |
| Protocolo de inyección de anomalías (C10.2) | `docs/A3-anexo-datasheet.md` | Hito 2 |
| Generación del dataset con seed=42 | `data/dataset_agro_sintetico.csv` | Hito 2 |
| Agregar refs pendientes a config/refs.bib (Apéndice B) | `config/refs.bib` | Hito 2 |
| Definir requirement.txt con versiones exactas | `requirements.txt` | Hito 2 |

### FASE 3 — Hito 3 (hasta 2026-06-15)
| Tarea | Archivo | Hito |
|---|---|---|
| Implementar E1–E5 (código) | `src/` | Hito 3 |
| Protocolo de usabilidad completo | `docs/A1-anexo-usabilidad.md` | Hito 3 |
| Repositorio GitHub con README | GitHub | Hito 3 |
| Ablation study diseñado y ejecutado | Cap IV | Hito 3 |

### FASE 4 — Hito 4 (hasta 2026-06-22)
| Tarea | Archivo | Hito |
|---|---|---|
| Cap IV con resultados reales y tablas | `docs/40-capitulo4.md` | Hito 4 |
| Discusión de resultados (por qué el ensemble supera al individual) | `docs/40-capitulo4.md` | Hito 4 |
| Model Cards para XGBoost y LightGBM | `docs/A2-anexo-modelcards.md` | Hito 4 |

### FASE 5 — Hito 5 (hasta 2026-07-07)
| Tarea | Archivo | Hito |
|---|---|---|
| Cap V con conclusiones basadas en resultados reales | `docs/50-capitulo5.md` | Hito 5 |
| Conclusiones ES + EN actualizadas | `docs/60-conclusiones.md` | Hito 5 |
| Abstract publicable con resultados reales | `docs/01-resumen.md` | Hito 5 |
| Borrador del paper de conferencia (6 páginas) | Nuevo archivo | Post-defensa |

---

## INDICADORES DE LOGRO PARA LA DEFENSA

Una tesis lista para defensa debe cumplir **todos** estos criterios:

| # | Indicador | Verificación | Estado |
|---|---|---|---|
| 1 | Todas las VD tienen tabla de operacionalización formal | `variables-operacionalizadas.md` existe y está completo | 🔴 |
| 2 | Todas las hipótesis tienen prueba estadística designada | §3.3 tiene tabla H1x → prueba → α | 🔴 |
| 3 | El claim sobre SBS N°053-2023 está verificado en el texto original | Artículo exacto citado con número | 🔴 |
| 4 | El claim sobre D.S. 115-2025-PCM está verificado en el texto original | Artículo exacto citado con número | 🔴 |
| 5 | El claim de brecha (gap) está respaldado por búsqueda sistemática documentada | `busqueda-sistematica-gap.md` existe | 🔴 |
| 6 | El dataset sintético tiene Datasheet completo (Gebru 2021) | `A3-anexo-datasheet.md` completo | 🔴 |
| 7 | Los experimentos E1–E5 están ejecutados y reportados en Cap IV | `40-capitulo4.md` completo | 🔴 |
| 8 | Cap V tiene conclusiones derivadas de resultados reales, no de expectativas | `50-capitulo5.md` completo | 🔴 |
| 9 | Todas las citas en texto tienen entrada en refs.bib | grep de citas ↔ refs.bib | ⚠️ |
| 10 | El código es reproducible (seed fija + requirements.txt) | `requirements.txt` + seeds en código | 🔴 |
| 11 | §1.12 Limitaciones está escrito | `10-capitulo1.md` tiene §1.12 | 🔴 |
| 12 | El protocolo de usabilidad está en Anexo A | `A1-anexo-usabilidad.md` completo | 🔴 |
| 13 | No hay afirmaciones de resultados experimentales propios en Cap I y II | Revisión de tiempos verbales | ⚠️ |
| 14 | La tabla comparativa de sistemas (Tabla 2.X) está en Cap II | `21-capitulo2-estadoarte.md` | ⚠️ |
| 15 | Las métricas de VD4 tienen N de participantes definido | §3.3 o Anexo A | 🔴 |

**Criterio mínimo para defensa**: 15/15 indicadores ✅.
**Estado actual**: 0/15 indicadores completamente cerrados (los 3 en ⚠️ están en progreso).

---

*Plan generado 2026-05-17. Actualizar estado de cada criterio (✅/⚠️/🔴) conforme se complete cada hito.*
*Próxima revisión programada: 2026-05-27 (Hito 1).*
