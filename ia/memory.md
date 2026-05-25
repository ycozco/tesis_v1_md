# MEMORY.md — Contexto del Proyecto
## Tesis UNSA: Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas
## Última actualización: 2026-05-17

> **Propósito**: Documento de contexto persistente para agentes de IA que retomen el trabajo. Léelo SIEMPRE primero antes de actuar. Si algo aquí contradice lo que ves en el código o los documentos, confía en lo que está en el código y actualiza este documento.

---

## 1. Identidad del proyecto

| Campo | Valor |
|---|---|
| Título | Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas |
| Autor | Yoset Cozco Mauri |
| Email | yodetcozco@gmail.com |
| Institución | Escuela Profesional de Ingeniería de Sistemas — Universidad Nacional de San Agustín de Arequipa (UNSA) |
| Asesor | Dr. Víctor Manuel Cornejo Aparicio |
| Tipo | Tesis de pregrado (Ingeniería de Sistemas) |
| Defensa estimada | Julio 2026 |
| Publicación derivada | Paper para CLEI 2026 (primera opción) o IEEE LATAM/Applied Intelligence (extensión) |
| Working dir | `d:\tesis_yoset` |
| Plataforma | Windows 11 Pro · PowerShell + Bash · Python 3.11–3.14 vía `py` launcher |

---

## 2. Sistema propuesto (qué construye la tesis)

Arquitectura de **4 capas** para supervisión operativa agroexportadora con IA explicable:

```
┌──────────────────────────────────────────────────────┐
│ Capa 4 — Reportes LLM + RAG                          │  ← anclado en SHAP + RAG estructurado
│ Anthropic Claude (o Llama 3) + BM25 retrieval       │     genera reporte narrativo trazable
└──────────────────────────────────────────────────────┘
                         ↑
┌──────────────────────────────────────────────────────┐
│ Capa 3 — Explicabilidad SHAP                         │  ← TreeSHAP top-5 por alerta
└──────────────────────────────────────────────────────┘
                         ↑
┌──────────────────────────────────────────────────────┐
│ Capa 2 — Detección de anomalías ENSEMBLE             │  ← IF + LOF + ECOD vía PyOD
└──────────────────────────────────────────────────────┘
                         ↑
┌──────────────────────────────────────────────────────┐
│ Capa 1 — Predicción tabular GBDT                     │  ← XGBoost + LightGBM
└──────────────────────────────────────────────────────┘
                         ↑
                  Dataset agroexportador
                  (sintético v1.0 + fuentes públicas)
```

**Variables del dominio** (17 columnas en el dataset): fecha, producto (arándano, uva, palta, cacao, espárrago), zona (Ica, La Libertad, Piura, Arequipa, Lima), volumen_kg, precio_kg_usd, temperatura_max_c, temperatura_min_c, precipitacion_mm, humedad_pct, destino_mercado, cumplimiento_fitosanitario, dias_logisticos, merma_pct, costo_logistico_usd_kg, tipo_cambio_pen_usd, etiqueta_anomalia, tipo_anomalia.

**Tipos de anomalía inyectados**: precio, volumen, clima, logística, calidad.

---

## 3. Decisiones arquitectónicas clave (no cambiar sin justificar)

1. **GBDT sobre Deep Learning** para datos tabulares — justificado en Grinsztajn et al. (2022).
2. **Ensemble de detectores** (IF + LOF + ECOD) sobre detector único — justificado en ADBench (Han et al., 2022).
3. **ECOD reemplaza Deep SVDD** en el ensemble — no requiere tuning de hiperparámetros, fundamento estadístico interpretable, complejidad lineal.
4. **LLM restringido a generación, NO decisión** — el LLM NUNCA decide si es anomalía; solo narra evidencias SHAP + RAG. Patrón anti-alucinación.
5. **RAG anclado en vectores SHAP estructurados** — la "base de conocimiento" del RAG son los vectores SHAP de la alerta + fuentes recuperadas, no texto libre.
6. **Dataset sintético documentado** (no datos privados de empresa) — permite reproducibilidad y publicación con licencia CC BY 4.0.
7. **División temporal del dataset** (no aleatoria) — evita data leakage en series con estacionalidad.
8. **Semilla aleatoria fija = 42** (con semillas 43–47 para reportar media ± DE).
9. **Stack open-source completo** — XGBoost, LightGBM, PyOD, SHAP, scikit-learn, Optuna.

---

## 4. Marco regulatorio (posición de la tesis)

| Norma | País | Aplicabilidad declarada |
|---|---|---|
| D.S. N° 115-2025-PCM (Reglamento de la Ley N° 31814) | Perú | Referencia general de IA responsable; principios de transparencia, supervisión humana, gestión de riesgos. |
| Resolución SBS N° 053-2023 | Perú | **NO obligatoria** para agroexportadoras (la SBS regula al sistema financiero). Se usa como **referencia de buenas prácticas** de gestión de riesgo de modelos. |
| Reglamento (UE) 2024/1689 EU AI Act | UE | Referencia internacional para principios del Art. 13 (transparencia). Se diseña "conformidad de principios", NO se afirma cumplimiento formal. |
| NIST AI RMF 1.0 | EE.UU. | Marco de gestión de riesgos: Govern, Map, Measure, Manage. Adoptado como referencia de diseño. |

**Importante**: el lenguaje correcto es "el sistema se diseña siguiendo los principios de..."; NUNCA "el sistema cumple con...".

---

## 5. Hipótesis de la tesis

**H1 (general)**: Un sistema integrado de predicción + detección + explicabilidad + reporte trazable mejora la trazabilidad de decisiones, la comprensión de alertas y el tiempo de decisión de supervisores operativos frente a componentes aislados.

**Sub-hipótesis** (cada una con experimento E_x asignado):

| Sub-hip | Experimento | Métrica | Prueba estadística | α |
|---|---|---|---|---|
| H1a — Ensemble > Detector único | E1 | PR-AUC | Wilcoxon signed-rank | 0.05 |
| H1b — SHAP mejora comprensión | E2 | Likert + cobertura top-k | Mann-Whitney U | 0.05 |
| H1c — RAG mejora reporte | E3 | Rúbrica 5D + ROUGE-L | t apareado / Wilcoxon | 0.05 |
| H1d — Sistema integrado reduce tiempo | E4 | Tiempo-a-decisión | t apareado | 0.05 |

---

## 6. Variables dependientes operacionalizadas

| VD | Indicador principal | Criterio aceptación | Experimento |
|---|---|---|---|
| VD1 — Rendimiento detección | PR-AUC | superar B1 (p<0.05, Hedges' g ≥ 0.5) | E1 |
| VD2 — Calidad explicabilidad | Cobertura top-5 + Likert claridad | ≥80% cobertura; Likert ≥ 4.0 | E2 |
| VD3 — Calidad reportes | Rúbrica 5D + ROUGE-L | promedio ≥ 4.0/5; Kappa ≥ 0.60 | E3 |
| VD4 — Comprensión y tiempo | Tiempo-a-decisión + Likert | -20% tiempo; Likert ≥ 4.0 | E4 |
| VD5 — Trazabilidad documental | % alertas completas (8 campos) | ≥ 95% en integrado | E4, E5 |

Detalle completo en `docs/variables-operacionalizadas.md`.

---

## 7. Hitos del calendario (estado al 2026-05-17)

| Hito | Fecha límite | Estado |
|---|---|---|
| Hito 1 — Variables operacionalizadas | 2026-05-27 | ✅ Cerrado anticipadamente (2026-05-17) |
| Hito 2 — Dataset sintético generado | 2026-06-01 | 🟢 Especificación y script listos; falta ejecutar |
| Hito 3 — 4 módulos de código + experimentos E1–E5 | 2026-06-15 | ⏳ |
| Hito 4 — Cap IV con resultados reales | 2026-06-22 | ⏳ |
| Hito 5 — Cap V + Conclusiones + Anexos cerrados | 2026-07-07 | ⏳ |
| Defensa | 2026-07-18 (estimado) | ⏳ |

Roadmap detallado: `docs/plan-siguientes-pasos.md`.

---

## 8. Estado de los documentos (19 secciones de la tesis)

### Secciones completas (13/19)
- `00-portada.md`, `01-resumen.md`, `02-indices.md`, `03-introduccion.md`
- `10-capitulo1.md` (Cap I: §1.1–§1.13, incluyendo §1.12 Limitaciones y §1.13 Declaración de intereses)
- `20-capitulo2-antecedentes.md`, `21-capitulo2-estadoarte.md`, `22-capitulo2-marcoteorico.md`
- `30-capitulo3.md` (Cap III: §3.1–§3.3 con diseño experimental E1–E5)
- `70-recomendaciones.md`, `80-glosario.md`, `90-referencias.md`
- `a4-anexo-ia.md` (Anexo D — uso de IA en redacción)

### Secciones con estructura lista, pendientes de datos (3/19)
- `40-capitulo4.md` — Cap IV con tablas 4.1–4.12 listas (incluye §4.4 Discusión Detallada con 5 cruces comparativos)
- `a2-anexo-modelcards.md` — 4 Model Cards (Mitchell et al., 2019) con plantillas
- `a3-anexo-datasheet.md` — Datasheet completo (Gebru et al., 2021)

### Secciones placeholder (3/19)
- `50-capitulo5.md` — Cap V (depende de Cap IV)
- `60-conclusiones.md` — Conclusiones ES + EN (depende de Cap IV)
- `a1-anexo-usabilidad.md` — completo en protocolo pero pendiente N real

---

## 9. Documentos auxiliares (planeación, no son secciones de la tesis)

Ubicados en `docs/` pero NO incluidos en `SECTION_ORDER`:

| Archivo | Propósito |
|---|---|
| `plan-detallado.md` | Plan general consolidado con checkup de hitos |
| `plan-segmentacion-docker.md` | Diseño de la segmentación en 19 archivos + hot-reload Flask |
| `plan-revision-academica-exhaustiva.md` | 87 criterios de revisión en 10 dimensiones (69/87 verificados) |
| `plan-rigor-academico-datasets.md` | 5 pilares de rigor, búsqueda de datasets |
| `plan-siguientes-pasos.md` | Roadmap operativo semanal hasta defensa |
| `variables-operacionalizadas.md` | Tabla formal de las 5 VD (Hito 1) |
| `busqueda-sistematica-gap.md` | Protocolo PRISMA-light para sustentar gap claim |
| `guia-uso.md` | Cómo usar el repo (visor, scripts, dataset, Git) |
| `README.md` | Resumen del repositorio |

---

## 10. Stack tecnológico

| Componente | Tecnología | Versión |
|---|---|---|
| Visor de tesis | Flask | 3.0.0 |
| Conversión Markdown→HTML | python-markdown | 3.5.1 |
| Renderizado fórmulas | MathJax 3 (CDN) | latest |
| Predicción GBDT | XGBoost + LightGBM | 2.0.3 + 4.3.0 |
| Detección anomalías | PyOD (IF + LOF + ECOD) | 1.1.3 |
| Explicabilidad | SHAP | 0.45.0 |
| Tuning hiperparámetros | Optuna | 3.6.1 |
| LLM | Anthropic Claude / Llama 3 | claude-sonnet-4-6 |
| Retrieval | rank-bm25 + sentence-transformers | 0.2.2 + 2.7.0 |
| Estadística | statsmodels + pingouin | 0.14.2 + 0.5.4 |
| Métricas texto | rouge-score | 0.1.2 |
| Container | Docker + docker-compose | 24+ |

Dependencias completas: `requirements.txt` (entorno ML) + `config/requirements-docker.txt` (visor).

---

## 11. Estructura del repositorio

```
tesis_yoset/
├── config/
│   ├── refs.bib                  47 entradas, 11 categorías (A–K)
│   ├── apa.csl                   estilo APA para Pandoc
│   ├── entrypoint.sh
│   └── requirements-docker.txt
├── data/                         CSV generados (no commiteado por defecto)
├── docs/                         19 secciones + auxiliares
├── ia/                           ← memory.md y agents.md (este directorio)
├── scripts/
│   ├── purga_referencias.py
│   ├── limpia_duplicados.py
│   ├── auditar_referencias.py
│   ├── rebuild_tesis_monolith.py     sincroniza tesis.md monolítica a partir de capítulos
│   └── compile_thesis.py             compilador integrado PDF y DOCX (Docker + Chrome)
├── src/
│   ├── app.py                    visor Flask con hot-reload
│   ├── convert_md_to_html.py
│   ├── serve_thesis.py
│   └── generate_synthetic_dataset.py
├── output/                       PDF, DOCX y HTML compilados
├── requirements.txt              entorno ML completo
├── docker-compose.yml            visor en localhost:8000
└── Dockerfile
```

---

## 12. Sistema de Compilación y Exportación (PDF y DOCX)

Para garantizar la entrega y presentación académica formal de la tesis, se cuenta con un sistema de compilación integrado que automatiza la exportación de la tesis completa a partir de los documentos actualizados de `docs/`.

### Arquitectura de Compilación
```
              [Capítulos individuales en docs/]
                              │
               (rebuild_tesis_monolith.py)
                              │
                              ▼
                        [tesis.md]
                  ┌───────────┴───────────┐
                  ▼                       ▼
           (PANDOC en Docker)     (Chrome Headless)
           Con plantilla oficial  Vista de servidor Flask
                  │                       │
                  ▼                       ▼
            [tesis.docx]             [tesis.pdf]
```

### Script de Compilación: `scripts/compile_thesis.py`
El script ejecuta un pipeline híbrido robusto:
1. **Compilación a DOCX (Docker + Pandoc):** Invoca a Pandoc dentro del contenedor `tesis-web-viewer` para compilar `docs/tesis.md` en formato Word. Aplica la plantilla oficial `formato/Plantilla - Tesis de Investigación 2026.docx`, el motor de citas `--citeproc` mapeado a `config/refs.bib` y el estilo de citación APA 7 (`config/apa.csl`).
2. **Compilación a PDF (Chrome Headless en Host):** Para evitar fallos por codificación de caracteres o problemas en el motor LaTeX tradicional, el script utiliza Google Chrome o Microsoft Edge en modo *headless* para imprimir la vista web interactiva del servidor (`http://localhost:8000/docs/tesis`) directamente a PDF. Esto mantiene las fuentes tipográficas prémium, las fórmulas matemáticas procesadas por MathJax, y el diseño de tablas e interfaces del visor interactivo.

### Ejecución
Para compilar la tesis en ambos formatos (generando las copias base y versiones fechadas para control de cambios):
```powershell
$env:PYTHONIOENCODING="utf-8"; py scripts/compile_thesis.py
```
**Archivos Generados (en `output/`):**
* `tesis.docx` y `tesis_[AAAA_MM_DD].docx` (Entregable formal en Word con estilo institucional).
* `tesis.pdf` y `tesis_[AAAA_MM_DD].pdf` (Lectura prémium con tipografía moderna, ecuaciones renderizadas y gráficos vectoriales).

---

## 13. Bloqueadores remanentes para la defensa (4 críticos)

1. **C8.1 — Verificación SBS N° 053-2023**: bajar texto oficial de sbs.gob.pe y citar artículos exactos.
2. **C8.2 — Verificación D.S. 115-2025-PCM**: bajar texto oficial de elperuano.pe.
3. **C7.6 — Repositorio GitHub público**: pendiente publicar al cierre del Hito 3.
4. **C4.5 — Tamaño efectivo de muestra**: depende de reclutamiento real (meta N ≥ 15, deseable N = 27).

---

## 14. Eventos y decisiones recientes (log corto)

- **2026-05-12**: creación de `plan-detallado.md`, 46 referencias organizadas por bloques.
- **2026-05-15**: actualización del enfoque de tesis (financiero → agroexportador), Cap II expandido con 7 antecedentes y 5 batallas argumentativas, Cap III migrado.
- **2026-05-17 (sesión 1)**: segmentación del monolito `tesis.md` en 19 archivos numerados, visor Flask con hot-reload, MathJax integrado.
- **2026-05-17 (sesión 2)**: creación de `plan-revision-academica-exhaustiva.md` (87 criterios en 10 dimensiones).
- **2026-05-17 (sesión 3)**: ejecución del plan de revisión — Cap I §1.12+§1.13, refinamiento §1.7.1+§1.9, Cap II §2.3.7 hedging RAG, Cap III diseño experimental E1–E5, anexos A1/A2/A3 completos, requirements.txt, generador del dataset sintético.
- **2026-05-17 (sesión 4)**: purga bibliográfica (refs.bib v2.0, 47 entradas en 11 categorías), reemplazo masivo de citas APA (179 reemplazos), nueva §4.4 Discusión Detallada con 5 cruces comparativos, plan-siguientes-pasos.md, guia-uso.md, commit `7d27efe`.
- **2026-05-17 (sesión 5)**: sincronización total de `docs/tesis.md` monolítica con los cambios de rigor de los Hitos 1-4. Diseño e implementación de `scripts/rebuild_tesis_monolith.py` y `scripts/compile_thesis.py` para generación automática de versiones DOCX (vía Pandoc en Docker) y PDF (vía Chrome Headless en Host). Compilación fechada exitosa.

---

## 15. Cosas que NO hacer (anti-patrones)

- ❌ Usar `[@clave]` en documentos activos de `docs/`. Sí en `tesis.md` o `tesis-v2.md` (reconstruido automáticamente por script).
- ❌ Afirmar "el sistema cumple con el EU AI Act / SBS / etc.". Decir "se diseña siguiendo los principios de...".
- ❌ Decir que RAG "elimina" alucinaciones. RAG "reduce significativamente pero no elimina".
- ❌ Usar Deep SVDD en lugar de ECOD en el ensemble (decisión arquitectónica documentada).
- ❌ Cambiar la semilla aleatoria base (42).
- ❌ Citar el nombre de archivo en el cuerpo de la tesis (`según docs/30-capitulo3.md`). Usar `según §3.3`.
- ❌ Modificar `tesis.md` de forma manual sin propagarlo a los capítulos individuales (los capítulos son la fuente única de verdad, `tesis.md` se regenera vía script).
- ❌ Editar `SECTION_ORDER` para incluir planes auxiliares (no son parte del flujo defensa).
- ❌ Commit con mensajes vagos. Usar prefijos: `tesis:`, `refs:`, `script:`, `plan:`, `anexo:`, `fix:`, `doc:`.
- ❌ Reportar resultados experimentales que aún no están medidos (todo Cap IV debe seguir en futuro hasta E1–E5).

---

## 16. Referencias clave para entender el proyecto

Para comprender la arquitectura: Grinsztajn et al. (2022), Han et al. (2022) ADBench, Lundberg & Lee (2017) SHAP, Lundberg et al. (2020) TreeSHAP, Lewis et al. (2020) RAG.

Para comprender el marco regulatorio: D.S. 115-2025-PCM (PCM, 2025), EU AI Act 2024 (Parlamento Europeo y Consejo, 2024), NIST AI RMF 1.0 (NIST, 2023).

Para comprender la metodología: Creswell & Creswell (2018), Page et al. (2021) PRISMA, Gebru et al. (2021) Datasheets, Mitchell et al. (2019) Model Cards.

Para comprender el dominio: MIDAGRI (2026), SENAMHI, SENASA, SUNAT (todas como referencias institucionales en `refs.bib` categoría K).

---

*Documento generado 2026-05-17. Mantener actualizado al cierre de cada hito.*

