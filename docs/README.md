# 📚 Sistema Integrado de Auditoría Continua con IA - Proyecto de Tesis

## Descripción General

Este proyecto contiene la estructura completa de una tesis de investigación sobre un **sistema integrado de auditoría continua** que combina:

- 🤖 **Predicción** con GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) (XGBoost, LightGBM)
- 🎯 **Detección de anomalías** con ensemble (IF (Isolation Forest - Bosque de Aislamiento), LOF (Local Outlier Factor - Factor de Anomalía Local), Deep SVDD)
- 📊 **Explicabilidad** con SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)
- 📝 **Generación de reportes** con LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)

---

## 📁 Estructura de Archivos

```
d:/tesis_yoset/
├── entregable1.md              # Cap. I & II (Plan + Marco Teórico)
├── plan_detallado.md           # Plan maestro Cap. I-V + estructura completa
├── mejora-continua-plan.md     # Plan PDCA de mejora continua
├── .agent.md                   # Agente de revisión y validación
├── entregable/                 # Artefactos de revisión y datasets
├── refs.bib                    # Bibliografía BibTeX (28-35 referencias)
├── apa.csl                     # Estilo de citación APA
│
├── 🐳 Docker (Visor Web)
├── Dockerfile                  # Imagen contenedor
├── docker-compose.yml          # Orquestación servicios
├── app.py                      # Flask server (visor web)
├── convert_md_to_html.py       # Conversor Markdown → HTML
├── entrypoint.sh              # Script inicio servicios
├── requirements-docker.txt     # Dependencias Python
│
├── 📊 Documentación
├── README.md                   # Este archivo
└── README-DOCKER.md           # Instrucciones Docker

```

---

## 🚀 Inicio Rápido

### Opción 1: Visor Web con Docker (Recomendado)

**Requisitos**: Docker, Docker Compose

```bash
# 1. Navegar al directorio del proyecto
cd d:/tesis_yoset

# 2. Construir e iniciar contenedores
docker-compose up --build

# 3. Abrir en navegador
# http://localhost:8000
```

**Características del visor web**:
- ✅ Visualización interactiva de Markdown
- ✅ Índice dinámico con búsqueda
- ✅ Tabla de contenidos automática
- ✅ Diseño responsivo
- ✅ Soporte para tablas y código
- ✅ Conversión en tiempo real

---

### Opción 2: Lectura Local (Sin Docker)

```bash
# 1. Abrir directamente los archivos .md
# - entregable1.md (Capítulos I & II)
# - mejora-continua-plan.md (Plan PDCA)
# - .agent.md (Checklist revisión)

# Usar editor compatible: VS Code, Typora, Obsidian, etc.

# 2. O convertir a HTML manualmente
python3 convert_md_to_html.py
# Genera: /html/entregable1.html, mejora-continua.html, etc.
```

---

## 📄 Contenido de Archivos Principales

### 1. **entregable1.md** (Principal)

**Propósito**: Plan completo de investigación (Capítulos I & II)

**Contenido**:
```
├─ CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA
│  ├─ 1.1 Descripción realidad problemática (6 problemas)
│  ├─ 1.2 Problema principal + sub-problemas
│  ├─ 1.3 Objetivos (1 general + 5 específicos)
│  ├─ 1.4 Hipótesis (H1 + H0 + 4 sub-hipótesis)
│  ├─ 1.5 Variables e indicadores (VI + 5 VD)
│  ├─ 1.6 Viabilidad (técnica, operativa, económica)
│  ├─ 1.7 Justificación (teórica, económica, social)
│  └─ 1.8-1.9 Alcance, Línea, Tipo, Nivel
│
└─ CAPÍTULO II: MARCO TEÓRICO
   ├─ 2.1 Antecedentes (6 dominios de investigación)
   ├─ 2.2 Estado del Arte (tabla 23 referencias)
   └─ 2.3 Marco Conceptual (9 subsecciones)
```

### 1.1 **plan_detallado.md** (Evolución maestra)

**Propósito**: Mapa completo de estructura, avance, brechas y plan de datos.

**Contenido**:
- Estructura completa de la tesis (Cap. I-V + anexos)
- Checkup del avance por capítulo
- Checklist de datos faltantes y revisiones
- Planificación integrada de fuentes y datasets

### 1.2 **entregable/** (Artefactos)

**Propósito**: Centralizar soportes operativos del proyecto.

**Incluye**:
- `dataset-matrix.csv`
- `dataset-decision.txt`
- `fuentes-datos-agroexport.txt`

**Métricas clave**:
- 8 secciones Cap. I
- 3 secciones Cap. II
- 25+ referencias verificadas
- ~4000 palabras

---

### 2. **mejora-continua-plan.md**

**Propósito**: Framework PDCA para desarrollo iterativo

**Ciclos incluidos**:
- ✅ Ciclo 1-2: Validación plan + preparación técnica
- ✅ Ciclo 3-5: Implementación componentes (ensemble, SHAP, LLM)
- ✅ Ciclo 6-7: Integración + testing usabilidad
- ✅ Ciclo 8-10: Análisis, documentación, defensa
- 🔮 Ciclo 11-12: Post-defensa (producción, publicación)

**Características**:
- Matriz PDCA detallada (Plan-Do-Check-Act)
- Métricas de aceptación por ciclo
- Sistema de alertas (Rojo/Amarillo/Verde)
- Registro de lecciones aprendidas
- Timeline 5 meses (300 horas)

---

### 3. **.agent.md**

**Propósito**: Agente de revisión automático

**Secciones**:
1. **Validación Estructural**: Checklist Cap. I & II
2. **Validación Coherencia**: Matriz trazabilidad problema→solución
3. **Validación Referencias**: Verificación BibTeX, citas críticas
4. **Viabilidad Técnica**: Recursos, timeline, testing
5. **Originalidad y Aporte**: Diferencial vs. literatura
6. **Pre-defensa**: Documento DOCX listo
7. **Recomendaciones**: Fortalecimiento puntos débiles
8. **Instrucciones**: Modo automático vs. manual

**Criterios aprobación**:
- ✅ APROBADO: ≥80% estructura + 100% trazabilidad + ≥25 citas
- ⚠️ REVISIÓN: <5% gaps + validación posible
- ❌ NO APROBADO: problemas fundamentales

---

### 4. **refs.bib** (Bibliografía)

**Cantidad**: 28-35 referencias BibTeX verificadas

**Cobertura**:
- 📊 GBDT: Chen 2016, Ke 2017, Prokhorenkova 2018 (XGBoost, LightGBM, CatBoost)
- 📈 Series temporales: Hyndman 2008, Taylor 2017, Oreshkin 2020 (AutoARIMA, Prophet, N-BEATS)
- 🎯 Anomalías: Liu 2008, Breunig 2000, Ruff 2018, Han 2022 (IF, LOF, Deep SVDD, ADBench)
- 💳 Fraude: Jesus 2022, Machado 2024, Leocádio 2024 (BAF Benchmark, revisión, auditoría IA)
- 🤖 LLMs (Large Language Models - Modelos de Lenguaje de Gran Tamaño): Tsai 2025, Kadir 2025 (LLMs tabulares, AuditCopilot)
- 🛡️ Gobernanza: NIST 2023, Gebru 2021, Mitchell 2019 (NIST RMF, Datasheets, Model Cards)

**Validación**:
- ✅ DOIs presentes para journals/conferences
- ✅ Preprints marcados con {arXiv}
- ✅ Formato APA consistente
- ✅ ≥50% referencias últimos 5 años

---

## 🎯 Objetivos de la Tesis

**Hipótesis Principal**: 
> Un sistema integrado (predicción GBDT + ensemble anomalías + SHAP + LLM+RAG) es **superior en trazabilidad, usabilidad y confianza** que componentes aislados.

**Objetivos Específicos**:
1. OE1: Diseñar arquitectura modular con separación responsabilidades
2. OE2: Implementar predicción ensemble con AUC ≥0.92
3. OE3: Integrar SHAP con coverage features ≥70%
4. OE4: Generar reportes LLM con ROUGE-1 ≥0.50
5. OE5: Validar usabilidad: Δ tiempo ≥30%, Δ confianza ≥+1

**Variables Dependientes**:
- VD1: Rendimiento detección (ROC-AUC (Receiver Operating Characteristic Area Under the Curve - Área Bajo la Curva de Característica Operativa del Receptor), F1)
- VD2: Explicabilidad (coverage, coherencia)
- VD3: Calidad reportes (ROUGE, hallucinations)
- VD4: Usabilidad (tiempo, confianza, precisión)
- VD5: Trazabilidad regulatoria (NIST RMF compliance)

---

## 🔬 Metodología

### Diseño Experimental

**Grupos**:
- **Grupo A**: Sistema integrado (predicción → ensemble → SHAP → reporte)
- **Grupo B**: Componentes aislados (baseline sin integración)

**Dataset**: Bank Account Fraud Benchmark (Jesus et al. 2022)
- 1M transacciones
- 30 features
- ~0.8% fraude
- Drift temporal incluido

**Evaluación**:
- Métricas automáticas (AUC, ROUGE, latencia)
- Testing con 10-15 auditores (usabilidad)
- Análisis estadístico (t-test, effect size)

### Timeline (5 meses)

```
Semana 1-2: Diseño plan + preparación técnica
Semana 2-3: Baseline model + EDA
Semana 3-4: Ensemble anomalías
Semana 4  : SHAP explicabilidad + LLM+RAG
Semana 5-6: Integración + testing usabilidad
Semana 6-7: Análisis resultados
Semana 7-8: Redacción + defensa
```

---

## ✅ Control de Calidad

### Agente de Revisión (.agent.md)

Usar para validar plan completo:

```bash
# Modo manual (recomendado)
1. Abrir .agent.md
2. Por cada sección, verificar checklist contra entregable1.md
3. Registrar observaciones
4. Ejecutar mejoras iterativamente

# Modo automático (futuro)
# python3 scripts/validate_thesis.py entregable1.md
```

### Ciclos PDCA (mejora-continua-plan.md)

Ejecutar iterativamente durante desarrollo:
- 📋 PLAN: Definir qué hacer
- ⚡ DO: Implementar
- ✓ CHECK: Validar contra métricas
- 🔄 ACT: Ajustar según resultados

---

## 🌐 Visor Web Interactivo

### Características

```
┌─────────────────────────────────────┐
│  NAVBAR: Navegación + Links         │
├─────────────────────────────────────┤
│ SIDEBAR        │      MAIN          │
│ - Búsqueda     │  - Título          │
│ - Índice       │  - Contenido HTML  │
│ - TOC auto     │  - Tablas          │
│                │  - Código coloreado│
└─────────────────────────────────────┘
```

### URLs Disponibles

- `http://localhost:8000/` → Página inicio
- `http://localhost:8000/admin` → Panel admin centralizado
- `http://localhost:8000/docs/entregable1` → Cap. I & II
- `http://localhost:8000/docs/mejora-continua-plan` → PDCA
- `http://localhost:8000/docs/.agent` → Agente revisión
- `http://localhost:8000/api/docs` → JSON lista documentos
- `http://localhost:8000/health` → Health check

---

## 📦 Conversión DOCX (Pandoc)

### Método 1: Dentro del contenedor Docker

```bash
# Abrir terminal en contenedor
docker exec -it tesis-pandoc-service bash

# Convertir Markdown a DOCX
pandoc entregable1.md \
  -o entregable1.docx \
  --reference-doc=plantilla.docx \
  --citeproc \
  --bibliography=refs.bib \
  --csl=apa.csl \
  --toc \
  --toc-depth=3
```

### Método 2: Local (si Pandoc instalado)

```bash
# Windows PowerShell
pandoc .\entregable1.md `
  -o .\entregable1.docx `
  --reference-doc=.\plantilla.docx `
  --citeproc `
  --bibliography=.\refs.bib `
  --csl=.\apa.csl `
  --toc `
  --toc-depth=3
```

---

## 🛠️ Desarrollo Local (Sin Docker)

### Dependencias

```bash
# Python 3.9+
pip install flask markdown pymdown-extensions

# Pandoc (para conversión DOCX)
# Windows: choco install pandoc
# macOS: brew install pandoc
# Linux: sudo apt-get install pandoc
```

### Ejecutar servidor local

```bash
python3 app.py
# Acceso: http://localhost:5000 (Flask por defecto)
```

---

## 📊 Progreso Actual (2026-05-12)

| Componente | Estado | Completitud |
|---|---|---|
| Cap. I Planteamiento | ✅ | 100% |
| Cap. II Marco Teórico | ✅ | 100% |
| Cap. III Metodología | 🟡 | 0% (pendiente) |
| Cap. IV Resultados | 🟡 | 0% (pendiente) |
| Cap. V Conclusiones | 🟡 | 0% (pendiente) |
| Bibliografía (28-35 refs) | ✅ | 100% |
| Agente Revisión | ✅ | 100% |
| Plan Mejora Continua | ✅ | 100% |
| Visor Web Docker | ✅ | 100% |
| Conversión DOCX | 🟡 | 50% (script ready) |

**Siguiente paso**: Iniciar Ciclo PDCA #1 (Validación plan) → Ciclos 2-10 (Desarrollo)

---

## 🤝 Colaboración y Feedback

### Cómo usar el agente de revisión

1. **Asesor**: Abrir `.agent.md`
2. **Asesor**: Marcar [ ] → [X] al validar
3. **Asesor**: Enviar observaciones
4. **Estudiante**: Incorporar feedback en entregable1.md
5. **Repite** iterativamente

### Mejora Continua

- Registrar lecciones en `mejora-continua-plan.md` → Lecciones aprendidas
- Actualizar plan cada ciclo PDCA
- Usar métricas de dashboard

---

## 📚 Referencias Clave

### Documentos Clave (Incluidos)
- [1] Chen & Guestrin (2016) - XGBoost
- [2] Ke et al. (2017) - LightGBM
- [15] Jesus et al. (2022) - BAF Benchmark
- [20] NIST (2023) - AI Risk Management Framework
- [23] Mitchell et al. (2019) - Model Cards

### Lectura Complementaria
- Grinsztajn et al. (2022) - "On Embeddings for Neural Networks" (GBDT vs. DL)
- Lundberg (2017) - "SHAP" (Explicabilidad)
- Kadir et al. (2025) - "AuditCopilot" (LLMs en auditoría)

---

## 📞 Soporte

### Troubleshooting Docker

```bash
# Error: Puerto 8000 en uso
docker-compose down
docker ps -a  # Listar contenedores
docker rm <container_id>

# Error: Permisos en Windows
# → Usar WSL2 para Docker Desktop
# → O instalar Docker Toolbox

# Logs del contenedor
docker-compose logs -f thesis-viewer
```

### Troubleshooting Pandoc

```bash
# Validar instalación
pandoc --version

# Si falta, instalar en contenedor
docker exec thesis-pandoc-service apt-get update && apt-get install pandoc
```

---

## 📄 Licencia y Atribución

Este proyecto es parte de una tesis de investigación de **UNSA** (Universidad Nacional de San Agustín, Perú).

**Referencias académicas**: Todas las citas son verificadas y atribuidas correctamente en `refs.bib`.

---

**Última actualización**: 2026-05-12 | **Versión**: 1.0 | **Estado**: 🚀 En desarrollo
