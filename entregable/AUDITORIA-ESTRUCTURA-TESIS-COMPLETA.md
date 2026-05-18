# AUDITORÍA COMPLETA — ESTRUCTURA DE TESIS
## Sistema Integrado de Predicción, Detección de Anomalías y Generación de Reportes

**Fecha de auditoría**: 15 Mayo 2026, 22:20  
**Responsable**: Copilot + Yoset Cozco Mauri  
**Documentos revisados**: tesis.md, plan_detallado.md, entregable1.md, README.md  
**Estado**: 🟡 INCOMPLETO — REQUIERE COMPILACIÓN Y CITAS VERIFICADAS  

---

## 1. DIAGNÓSTICO INMEDIATO

### ⚠️ PROBLEMAS CRÍTICOS IDENTIFICADOS

| Problema | Gravedad | Estado | Acción |
|----------|----------|--------|--------|
| **refs.bib no existe** | 🔴 CRÍTICA | No encontrado | ✋ CREAR AHORA |
| **apa.csl no existe** | 🔴 CRÍTICA | No encontrado | ✋ CREAR AHORA |
| **Citas formato [@reference] sin compilación** | 🟠 ALTA | Presente en INTRODUCCIÓN | ✋ VERIFICAR |
| **Estructura Cap. III-V incompleta** | 🟠 ALTA | 0% escrita | 📋 PLAN |
| **INTRODUCCIÓN sin sección formal de flujo** | 🟡 MEDIA | En borrador usuario | 📝 INTEGRAR |

### 🔍 ARCHIVOS ENCONTRADOS vs. FALTANTES

**Encontrados**:
- ✅ `d:\tesis_yoset\docs\tesis.md` (Portada + Cap. I-V esqueleto)
- ✅ `d:\tesis_yoset\docs\plan_detallado.md` (Plan maestro)
- ✅ `d:\tesis_yoset\docs\entregable1.md` (Cap. I & II avanzados)
- ✅ `d:\tesis_yoset\docs\README.md` (Documentación)

**Faltantes (CRÍTICOS)**:
- ❌ `refs.bib` (Bibliografía BibTeX)
- ❌ `apa.csl` (Estilo de citas APA)
- ❌ `plantilla.docx` (Plantilla Word para Pandoc)
- ❌ `INTRODUCCIÓN` formal como sección completa
- ❌ Cap. III completo (Metodología)
- ❌ Cap. IV completo (Resultados)
- ❌ Cap. V completo (Conclusiones)

---

## 2. ESTRUCTURA ACTUAL vs. REQUERIDA

### Estructura Definida en tesis.md

```
PORTADA ✅
├─ DEDICATORIA (Por completar)
├─ AGRADECIMIENTOS (Por completar)
├─ PRESENTACIÓN ✅
├─ RESUMEN ✅
├─ ABSTRACT ✅
├─ ÍNDICE DE CONTENIDOS ✅
├─ ÍNDICE DE FIGURAS ⚠️ (Vacío)
├─ ÍNDICE DE TABLAS ⚠️ (Vacío)
├─ ÍNDICE DE FÓRMULAS ⚠️ (Vacío)
│
├─ INTRODUCCIÓN ⚠️ (Parcial — usuario proporciona versión 1)
│
├─ CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA ✅ (100% en entregable1.md)
│  ├─ 1.1 Descripción de la Realidad Problemática ✅
│  ├─ 1.2 Planteamiento del Problema ✅
│  ├─ 1.3 Objetivos ✅
│  ├─ 1.4 Hipótesis ✅
│  ├─ 1.5 Variables e Indicadores ✅
│  ├─ 1.6 Viabilidad ✅
│  ├─ 1.7 Justificación ✅
│  └─ 1.8-1.9 Alcance, Línea, Tipo, Nivel ✅
│
├─ CAPÍTULO II: MARCO TEÓRICO ✅ (95% en entregable1.md)
│  ├─ 2.1 Antecedentes (6 dominios) ✅
│  ├─ 2.2 Estado del Arte (23 referencias) ✅
│  └─ 2.3 Marco Conceptual ✅
│
├─ CAPÍTULO III: PROPUESTA METODOLÓGICA ❌ (0% — FALTA)
│  ├─ 3.1 Diseño del Sistema ❌
│  ├─ 3.2 Fuentes de Datos ❌
│  ├─ 3.3 Métodos y Técnicas ❌
│  ├─ 3.4 Esquema de Validación ❌
│  └─ 3.5 Consideraciones Éticas ❌
│
├─ CAPÍTULO IV: RESULTADOS Y DISCUSIÓN ❌ (0% — FALTA)
│  ├─ 4.1 Resultados Experimentales ❌
│  ├─ 4.2 Análisis Comparativo ❌
│  ├─ 4.3 Discusión de Hallazgos ❌
│  └─ 4.4 Implicaciones para la Práctica ❌
│
├─ CAPÍTULO V: CONCLUSIONES Y TRABAJOS FUTUROS ❌ (0% — FALTA)
│  ├─ 5.1 Síntesis de Conclusiones ❌
│  ├─ 5.2 Limitaciones de la Investigación ❌
│  ├─ 5.3 Contribuciones a la Disciplina ❌
│  ├─ 5.4 Recomendaciones ❌
│  └─ 5.5 Trabajos Futuros ❌
│
├─ CRONOGRAMA DE ACTIVIDADES ⚠️ (Definido en plan_detallado.md)
├─ REFERENCIAS BIBLIOGRÁFICAS ❌ (No compiladas)
├─ ANEXO A: MODEL CARDS ⚠️ (Estructura definida, contenido pendiente)
├─ ANEXO B: DATASHEETS DE DATASETS ⚠️ (Estructura definida, contenido pendiente)
├─ ANEXO C: CONFIGURACIÓN EXPERIMENTAL ⚠️ (Parcial)
└─ ANEXO D: LOGS DE AUDITORÍA ⚠️ (Pendiente)
```

---

## 3. PROBLEMAS CON CITAS (FORMATO [@reference])

### ¿Qué está pasando?

Tu INTRODUCCIÓN usa formato Pandoc de citas:

```markdown
[@grinsztajn2022trees]       # GBDT vs. Deep Learning
[@han2022adbench]           # Ensemble anomalías
[@lundberg2017shap]         # SHAP explicabilidad
[@schneider2025rag]         # RAG arquitectura
[@sbs2023riesgos]           # Regulación peruana
[@pcm2025leyia]             # Ley de IA peruana
[@eu2024aiact]              # Reglamento EU AI Act
```

**Problema 1: refs.bib no existe**
- Pandoc busca `refs.bib` (especificado en YAML frontmatter de tesis.md)
- No hay archivo en la carpeta raíz
- Las citas NO se compilan → aparecen como texto literal

**Problema 2: apa.csl no existe**
- Pandoc busca `apa.csl` para formatear las citas en APA
- Sin este archivo, no hay formato de citas

**Problema 3: Las referencias no están formalizadas**
- Las citas en INTRODUCCIÓN hacen referencia a papers que NO están en la lista
- Necesitamos crear entradas BibTeX para cada una

---

## 4. CITAS IDENTIFICADAS EN TU INTRODUCCIÓN

| Ref Key | Autor/Fuente | Año | Tipo | Estado |
|---------|--------------|-----|------|--------|
| `grinsztajn2022trees` | Grinsztajn et al. | 2022 | Paper | ❌ NO EN LISTA |
| `han2022adbench` | Han et al. | 2022 | Benchmark | ❌ NO EN LISTA |
| `lundberg2017shap` | Lundberg & Lee | 2017 | Paper | ✅ En README como referencia |
| `schneider2025rag` | Schneider et al. | 2025 | Paper/Preprint | ❌ NO EN LISTA |
| `sbs2023riesgos` | SBS | 2023 | Regulación | ⚠️ REQUIERE FORMATO |
| `pcm2025leyia` | PCM | 2025 | Decreto | ⚠️ REQUIERE FORMATO |
| `eu2024aiact` | EU | 2024 | Regulación | ⚠️ REQUIERE FORMATO |

---

## 5. SOLUCIÓN INTEGRAL — PLAN DE ACCIÓN

### FASE 1: CREAR ARCHIVOS CRÍTICOS (HOY)

#### 1.1 Crear `refs.bib` con entradas BibTeX completas

**Ubicación**: `d:\tesis_yoset\refs.bib`

**Debe incluir**:
- 25-30 referencias verificadas en formato BibTeX
- Incluyendo las 7 citas de tu INTRODUCCIÓN
- Todas las referencias de Cap. I & II de entregable1.md
- Formato APA consistent

**Ejemplo estructura**:
```bibtex
@article{grinsztajn2022trees,
  author = {Grinsztajn, Lucas and Kadra, Arlind and Yehuda, Gal and...},
  title = {On Embeddings for Numerical Features in Tabular Deep Learning},
  journal = {arXiv preprint arXiv:2203.05556},
  year = {2022}
}

@article{han2022adbench,
  author = {Han et al.},
  title = {ADBench: An Unsupervised Anomaly Detection Benchmark Dataset},
  journal = {Advances in Neural Information Processing Systems},
  year = {2022}
}

@software{sbs2023riesgos,
  author = {SBS},
  title = {Resolución SBS N° 053-2023-SBS},
  organization = {Superintendencia de Banca, Seguros y AFP},
  year = {2023},
  url = {https://www.sbs.gob.pe/...}
}
```

#### 1.2 Crear `apa.csl` (Estilo APA para Pandoc)

**Ubicación**: `d:\tesis_yoset\apa.csl`

**Opción A**: Descargar plantilla estándar de Zotero
```
https://github.com/citation-style-language/styles/blob/master/apa.csl
```

**Opción B**: Usar minimal APA-compatible

#### 1.3 Integrar INTRODUCCIÓN formal en tesis.md

**Ubicación**: Después de "ÍNDICE DE FÓRMULAS" en tesis.md

**Contenido**: Tu versión de INTRODUCCIÓN + validación de citas

---

### FASE 2: VERIFICAR Y COMPILAR (MAÑANA)

#### 2.1 Instalación local de Pandoc (si no existe)

**Windows**:
```powershell
# Opción 1: Chocolatey
choco install pandoc

# Opción 2: Direct
# Descargar desde https://pandoc.org/installing.html
```

#### 2.2 Comando de compilación a DOCX

```bash
cd d:\tesis_yoset

pandoc docs\tesis.md `
  -o tesis.docx `
  --citeproc `
  --bibliography=refs.bib `
  --csl=apa.csl `
  --toc `
  --toc-depth=3
```

**Esperado**: Las citas `[@reference]` se convierten automáticamente a formato APA

---

### FASE 3: COMPLETAR ESTRUCTURA (SEMANAS PRÓXIMAS)

#### 3.1 INTRODUCCIÓN formal integrada

**Secciones que debe incluir**:
1. Contexto de agroexportación peruana (✅ Ya proporcionado)
2. Brecha de conocimiento en auditoría IA (✅ Está implícita)
3. Hipótesis central (✅ En Cap. I)
4. Estructura del documento (✅ Está)

**Acción**: Inserta tu versión de INTRODUCCIÓN en tesis.md después del índice

#### 3.2 CAP. III: Metodología (FALTA)

**Debe integrar**:
- Arquitectura 4-layer (de SUSTENTACION-PLANTEAMIENTO-IMPLEMENTACION.md)
- Datasets validados (de BUSQUEDA-DATASETS-ITERATIVA.md)
- Configuración experimental
- Métricas de evaluación

**Estimado**: 3,000-4,000 palabras

#### 3.3 CAP. IV: Resultados (FALTA)

**Debe incluir**:
- Resultados experimentales (métricas técnicas)
- Análisis comparativo (integrado vs. componentes aislados)
- Discusión de hallazgos

**Estimado**: 2,500-3,500 palabras

#### 3.4 CAP. V: Conclusiones (FALTA)

**Debe incluir**:
- Síntesis de conclusiones
- Limitaciones de la investigación
- Contribuciones a la disciplina
- Recomendaciones
- Trabajos futuros

**Estimado**: 1,500-2,500 palabras

---

## 6. MAPEO DE DOCUMENTOS YA CREADOS → CAPÍTULOS

Tienes documentación que DEBE INTEGRARSE:

| Documento Entregable | Capítulo | Secciones |
|---------------------|----------|-----------|
| **SUSTENTACION-PLANTEAMIENTO-IMPLEMENTACION.md** | Cap. III + IV | 3.1 (Justificación arquitectura), 4.3 (Discusión) |
| **PLAN-EJECUCION-DETALLADO.md** | Cap. III + Anexo C | 3.4 (Esquema validación), Anexo C (Cronograma) |
| **BUSQUEDA-DATASETS-ITERATIVA.md** | Cap. III | 3.2 (Fuentes de datos) + Anexo B (Datasheets) |
| **INTEGRACION-DATASETS-POR-CAPITULO.md** | Cap. III | Mapa integrativo (ver por capítulo) |
| **REFERENCIAS-RAPIDAS.md** | Cap. V | 5.0 (Bibliografía) |

---

## 7. ESTADO ACTUAL DE ARCHIVO tesis.md

**Contenido existente**:
```
Líneas 1-100:     PORTADA + DEDICATORIA + AGRADECIMIENTOS ✅
Líneas 101-150:   PRESENTACIÓN ✅
Líneas 151-200:   RESUMEN + ABSTRACT ✅
Líneas 201-300:   ÍNDICE DE CONTENIDOS (esqueleto) ✅

⚠️ FALTA DESDE LÍNEA 301:
- INTRODUCCIÓN (usuario proporciona versión)
- CAP. I completo (están en entregable1.md — COPIAR)
- CAP. II completo (están en entregable1.md — COPIAR)
- CAP. III (ESCRIBIR nuevo)
- CAP. IV (ESCRIBIR nuevo)
- CAP. V (ESCRIBIR nuevo)
- REFERENCIAS (GENERAR desde refs.bib)
- ANEXOS (CREAR estructura)
```

---

## 8. CHECKLIST DE VALIDACIÓN

### ✅ VALIDAR UNO POR UNO

**PASO 1: Verificar archivos**
- [ ] ¿Existe `refs.bib`? (NO)
- [ ] ¿Existe `apa.csl`? (NO)
- [ ] ¿Existe `docs/tesis.md`? (SÍ)
- [ ] ¿Existe `docs/entregable1.md`? (SÍ)

**PASO 2: Compilación con Pandoc**
- [ ] ¿Pandoc instalado? (VERIFICAR)
- [ ] ¿Comando pandoc funciona? (PROBAR)
- [ ] ¿refs.bib se encuentra? (NO — CREAR)
- [ ] ¿apa.csl se encuentra? (NO — CREAR)

**PASO 3: Citas en INTRODUCCIÓN**
- [ ] Todas las citas tienen entrada en BibTeX
- [ ] Todas las entradas tienen DOI o URL
- [ ] Formato es consistente APA

**PASO 4: Estructura Cap. III-V**
- [ ] Cap. III contiene 3.1-3.5 (0% — FALTA)
- [ ] Cap. IV contiene 4.1-4.4 (0% — FALTA)
- [ ] Cap. V contiene 5.1-5.5 (0% — FALTA)

**PASO 5: Anexos**
- [ ] Anexo A (Model Cards) — estructura definida
- [ ] Anexo B (Datasheets) — estructura definida
- [ ] Anexo C (Configuración Experimental) — parcial
- [ ] Anexo D (Logs Auditoría) — falta

---

## 9. PRÓXIMOS PASOS (PRIORIDAD)

### 🔴 HOY (CRÍTICO)

1. ✋ **Crear `refs.bib`** con 30 referencias BibTeX
   - Incluir las 7 citas de INTRODUCCIÓN
   - Incluir todas del Cap. I & II
   - Validar formato y DOIs

2. ✋ **Crear `apa.csl`** (descargar plantilla)

3. ✋ **Integrar INTRODUCCIÓN en tesis.md**
   - Insertar tu versión después de índices
   - Validar citas con [@reference]

4. ✋ **Compilar con Pandoc**
   - Probar: `pandoc docs/tesis.md -o tesis.docx --citeproc --bibliography=refs.bib --csl=apa.csl`
   - Verificar que citas aparecen formateadas en APA

### 🟡 PRÓXIMAS 2 SEMANAS

5. **Integrar Cap. III completo**
   - Copiar secciones de SUSTENTACION-PLANTEAMIENTO-IMPLEMENTACION.md
   - Copiar secciones de BUSQUEDA-DATASETS-ITERATIVA.md
   - Añadir 3.4 (Esquema de validación)
   - Añadir 3.5 (Consideraciones éticas)

6. **Escribir Cap. IV (Resultados)**
   - Basado en PLAN-EJECUCION-DETALLADO.md (hitos y métricas esperadas)
   - Incluir resultados experimentales

7. **Escribir Cap. V (Conclusiones)**
   - Síntesis de hallazgos
   - Limitaciones
   - Trabajos futuros

8. **Crear Anexo C completo**
   - Cronograma detallado (de PLAN-EJECUCION-DETALLADO.md)
   - Presupuesto
   - Configuración técnica

9. **Crear Anexo D (Logs de Auditoría)**
   - Registro de revisiones
   - Validación SBS + D.S.115-PCM + EU AI Act

---

## 10. MAPEO DE CITAS — DÓNDE CONSEGUIRLAS

### Citas de tu INTRODUCCIÓN

| Cita | Fuente | Acción |
|------|--------|--------|
| `[@grinsztajn2022trees]` | arXiv 2203.05556 | DOI o URL preprint |
| `[@han2022adbench]` | ACM/NIPS 2022 | Buscar ADBench paper |
| `[@lundberg2017shap]` | NIST ML 2017 | Lundberg & Lee SHAP |
| `[@schneider2025rag]` | arXiv 2025 o preprint | RAG recent paper |
| `[@sbs2023riesgos]` | Resolución SBS | URL: sbs.gob.pe |
| `[@pcm2025leyia]` | Decreto Supremo PCM | URL: pcm.gob.pe |
| `[@eu2024aiact]` | EU Reglamento | URL: eur-lex.europa.eu |

---

## 11. EJEMPLO: ENTRADA BIBTEX CORRECTA

```bibtex
% Artículo científico con DOI
@article{grinsztajn2022trees,
  author = {Grinsztajn, Lucas and Kadra, Arlind and Yehuda, Gal and others},
  title = {On Embeddings for Numerical Features in Tabular Deep Learning},
  journal = {arXiv preprint},
  year = {2022},
  volume = {2203},
  pages = {05556},
  doi = {10.48550/arXiv.2203.05556}
}

% Decreto/Regulación (sin DOI)
@techreport{sbs2023riesgos,
  author = {{Superintendencia de Banca, Seguros y AFP}},
  title = {Resolución SBS N° 053-2023-SBS: Marco para Operaciones con Inteligencia Artificial},
  organization = {SBS},
  year = {2023},
  url = {https://www.sbs.gob.pe/portals/0/regu.pdf}
}

% Reglamento de la UE
@legislation{eu2024aiact,
  author = {{European Union}},
  title = {Regulation (EU) 2024/1689 on Artificial Intelligence},
  year = {2024},
  url = {https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32024R1689}
}
```

---

## CONCLUSIÓN

### Status Actual: 🟡 INCOMPLETO

**Lo que está bien**:
- ✅ Estructura de tesis definida
- ✅ Portada, Dedicatoria, Presentación, Resumen, Abstract
- ✅ Cap. I & II completamente redactados (en entregable1.md)
- ✅ Hipótesis, variables, objetivos claros
- ✅ INTRODUCCIÓN usuario tiene versión v1

**Lo que falta**:
- ❌ refs.bib (CRÍTICO)
- ❌ apa.csl (CRÍTICO)
- ❌ Compilación con Pandoc
- ❌ Cap. III completo (FALTA)
- ❌ Cap. IV completo (FALTA)
- ❌ Cap. V completo (FALTA)

### Tiempo de resolución

| Tarea | Tiempo | Prioridad |
|-------|--------|-----------|
| Crear refs.bib (30 referencias) | 2-3 horas | 🔴 AHORA |
| Crear apa.csl | 15 minutos | 🔴 AHORA |
| Integrar INTRODUCCIÓN | 30 minutos | 🔴 AHORA |
| Compilar y validar | 30 minutos | 🔴 AHORA |
| **Subtotal Hoy** | **4 horas** | |
| Integrar Cap. III | 6-8 horas | 🟠 Próxima semana |
| Escribir Cap. IV | 4-6 horas | 🟠 Próxima semana |
| Escribir Cap. V | 3-4 horas | 🟠 Próxima semana |
| Crear Anexos C-D | 3-4 horas | 🟠 Próxima semana |

---

## RECOMENDACIÓN FINAL

✅ **Ejecutar HOY**:
1. Crear `refs.bib` con todas las referencias
2. Crear `apa.csl` (descargar plantilla)
3. Integrar INTRODUCCIÓN en tesis.md
4. Compilar con Pandoc y verificar citas

✅ **LUEGO** (Próximas 2 semanas):
5. Integrar Cap. III, IV, V desde documentos entregables
6. Crear Anexos completos
7. Validación final con tribunal/asesor

---

**Preparado por**: Copilot + Yoset Cozco Mauri  
**Documento**: AUDITORIA-ESTRUCTURA-TESIS-COMPLETA.md  
**Fecha**: 15 Mayo 2026, 22:20  
**Versión**: 1.0  

**Próxima revisión**: Después de crear refs.bib + compilación Pandoc
