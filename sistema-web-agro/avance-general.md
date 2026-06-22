# AVANCE GENERAL DEL SISTEMA — Agro-Intelligence Oversight
## Análisis de Valor FOB en Exportaciones Agroalimentarias con IA Explicable

> **Tesis:** Sistema de Auditoría Aduanera con Inteligencia Artificial Explicable  
> **Autor:** Yoset Cozco Mauri | **Director:** Dr. Víctor Cornejo Aparicio  
> **UNSA — Junio 2026** | **Repo:** https://github.com/ycozco/tesis_v1_md

---

## ⚠️ ENFOQUE DEL SISTEMA — Solo Análisis FOB

> El sistema realiza **únicamente análisis de valor FOB declarado** en Declaraciones Aduaneras de Mercancías (DAM) de exportaciones agroalimentarias peruanas. El objetivo es detectar posibles subvaloraciones del precio FOB que puedan constituir evasión arancelaria o triangulación de precios en el comercio exterior.

El análisis FOB es el eje central de las 4 capas:
- **Capa 1:** Predicción del FOB esperado (XGBoost) → compara con FOB declarado
- **Capa 2:** Score de anomalía FOB (PyOD Ensemble) → detecta si la desviación es estadísticamente atípica
- **Capa 3:** SHAP → explica qué variable contribuye más a la desviación FOB
- **Capa 4:** RAG → recupera normativas que regulan el control del valor FOB en aduanas

---

## 1. TAREAS REALIZADAS — Registro Completo

### 1.1 Infraestructura y DevOps

| Tarea | Estado | Detalle |
|---|---|---|
| Configurar `docker-compose.yml` con 3 servicios | ✅ Completo | frontend (Nginx:8050), backend (Flask:5000), db (pgvector:pg15:5432) |
| Imagen PostgreSQL con pgvector | ✅ Completo | `pgvector/pgvector:pg15` — habilita búsqueda vectorial |
| Health check de BD antes de iniciar backend | ✅ Completo | `depends_on: db: condition: service_healthy` |
| Dockerfile multi-stage frontend | ✅ Completo | Node build → Nginx prod |
| Dockerfile backend con dependencias ML | ✅ Completo | ~2GB de dependencias Python ML/NLP |
| Reverse proxy Nginx → Flask | ✅ Completo | `/api/*` → `backend:5000`, todo lo demás → SPA |
| Auto-entrenamiento de modelos en startup | ✅ Completo | `init_db.py` entrena y serializa en `models_weights/` |
| `.gitignore` excluye `models_weights/`, `node_modules/` | ✅ Completo | Pesos se regeneran automáticamente |
| Git init + push a `tesis_v1_md` en GitHub | ✅ Completo | `sistema-web-agro/` como subcarpeta del repo |

### 1.2 Base de Datos (PostgreSQL + pgvector)

| Tarea | Estado | Detalle |
|---|---|---|
| Habilitar extensión `pgvector` | ✅ Completo | `CREATE EXTENSION IF NOT EXISTS vector` |
| Modelo `Usuario` | ✅ Completo | Autenticación, rol (ADMIN/AUDITOR), condición experimental A/B |
| Modelo `OperacionAlerta` | ✅ Completo | DAM completa: FOB declarado, FOB esperado, score anomalía, estado |
| Modelo `DecisionAuditoria` | ✅ Completo | Telemetría: tiempo decisión, Likert comprensión, condición |
| Modelo `ExplicacionSHAP` | ✅ Completo | Valores SHAP por variable, Numeric(16,6) para precisión FOB |
| Modelo `DocumentoNormativo` | ✅ Completo | Normativas con `embedding VECTOR(384)` para búsqueda semántica |
| Modelo `SecurityLog` | ✅ Completo | Log de accesos y eventos del sistema |
| Seed de datos de prueba (11 alertas FOB) | ✅ Completo | Alertas reales con FOB declarado vs esperado, scores |

### 1.3 Backend — Pipeline de IA (Flask + Gunicorn)

| Tarea | Estado | Detalle |
|---|---|---|
| **Capa 1: XGBoost para predicción FOB** | ✅ Completo | Predice FOB esperado, calcula desviación % |
| **Capa 2: Ensemble PyOD (FOB anomaly score)** | ✅ Completo | IForest 45% + LOF 30% + ECOD 25% → score ∈ [0,1] |
| **Capa 3: TreeSHAP (explicabilidad local FOB)** | ✅ Completo | Atribuciones por variable, persistidas en BD |
| **Capa 4: RAG + pgvector (normativas FOB)** | ✅ Completo | Búsqueda semántica de normativas, reporte con citas |
| Auto-vectorización normativas en startup | ✅ Completo | FDA CFR21, SENASA, Ley IA del Perú |
| Indexación de nuevas normativas vía API | ✅ Completo | `POST /api/config/documents` |
| Pesos del ensemble configurables | ✅ Completo | `GET/PUT /api/config` desde UI |
| Motor heurístico RAG offline | ✅ Completo | Funciona sin Gemini API Key |
| Telemetría automática al adjudicar alerta | ✅ Completo | `POST /api/alerts/<id>/adjudicate` |
| Estadísticas de usabilidad A/B | ✅ Completo | `GET /api/telemetry/stats` |
| Estadísticas de integridad/fairness | ✅ Completo | `GET /api/integrity/stats` |
| Estadísticas del dashboard FOB | ✅ Completo | `GET /api/dashboard/stats` |
| Autenticación con asignación condición A/B | ✅ Completo | `POST /api/auth/login` |

### 1.4 Frontend React — Vistas Implementadas

| Vista | Ruta | Estado | Descripción |
|---|---|---|---|
| Login | `/login` | ✅ Completo | Autenticación + asignación condición experimental |
| Dashboard | `/dashboard` | ✅ Completo | KPIs FOB, alertas prioritarias por score |
| Gestión de Alertas | `/alerts` | ✅ Completo | Listado filtrable por estado, score, producto |
| **Detalle de Alerta FOB** | `/alerts/:id` | ✅ Completo | **Vista central del análisis FOB — 4 capas IA** |
| Historial | `/history` | ✅ Completo | Decisiones pasadas y estados |
| Telemetría | `/telemetry` | ✅ Completo | Boxplots A/B tiempos y comprensión |
| Integridad / Fairness | `/integrity` | ✅ Completo | FPR por producto, Recall, DPR |
| Explorador de Datos | `/data` | ✅ Completo | Datos + Biblioteca RAG + indexador |
| Configuración | `/config` | ✅ Completo | Pesos ensemble, umbral FOB global |
| Usuarios | `/users` | ✅ Completo | Gestión de auditores |

### 1.5 Documentación

| Documento | Ubicación | Estado |
|---|---|---|
| Guía de despliegue local | `sistema-web-agro/GUIA_DESPLIEGUE_LOCAL.md` | ✅ Completo |
| Avance detallado para tesis | `sistema-web-agro/AVANCE_DETALLADO_TESIS.md` | ✅ Completo |
| Datos y credenciales de prueba | `sistema-web-agro/backend/DATOS_PRUEBA.txt` | ✅ Completo |
| Capítulo 4 completo | `docs/02-40-capitulo4.md` | ✅ Actualizado |
| Resultados cuantitativos | `docs/02-41-capitulo4-resultados-cuantitativos.md` | ✅ Actualizado |
| Explicabilidad SHAP y RAG | `docs/02-42-capitulo4-explicabilidad-reportes.md` | ✅ Actualizado |
| Usabilidad y Trazabilidad | `docs/02-43-capitulo4-usabilidad-trazabilidad.md` | ✅ Actualizado |
| GitHub Pages compilado | `github_pages/` → `ycozco.github.io/tesis_v1_md` | ✅ Actualizado |

---

## 2. VISTAS QUE NECESITAN MÁS ANÁLISIS FOB

Las siguientes vistas actualmente tienen datos de prueba o análisis genérico y deben ampliarse para mostrar **análisis FOB específico** que aporte valor directo a la tesis:

### 2.1 Dashboard — `/dashboard` 🔴 PRIORITARIO

**Qué tiene ahora:** Conteo de alertas activas, tiempo promedio de decisión, logs recientes.

**Qué necesita para análisis FOB:**
- 📊 **Gráfico de dispersión FOB Declarado vs FOB Esperado** por alerta (visual de desviación)
- 📈 **Tendencia histórica** del valor FOB promedio declarado vs esperado por semana/mes
- 🗂️ **Distribución de desviación FOB** por rango (0-5%, 5-10%, 10-15%, >15%)
- 🏆 **Top 5 operaciones con mayor desviación FOB** (ordenadas por `fob_declarado - fob_esperado`)
- 📦 **Desviación FOB por producto** (Palta, Uva, Arándano, Mango) — gráfico de barras

### 2.2 Vista Detalle de Alerta — `/alerts/:id` 🟡 MEJORAR

**Qué tiene ahora:** 4 capas de IA completas, SHAP, narrativa RAG.

**Qué necesita para análisis FOB:**
- 💹 **Medidor gauge visual** de desviación FOB (declarado vs esperado con escala coloreada)
- 📊 **Historial de FOB** de la misma empresa exportadora (contexto de comportamiento)
- 🌍 **Comparativo con precio FOB de mercado internacional** (Trade Map benchmark)
- 📉 **Serie de tiempo** del precio FOB de ese producto en el mercado destino

### 2.3 Integridad/Fairness — `/integrity` 🟡 MEJORAR

**Qué tiene ahora:** FPR por producto, Recall por segmento, DPR.

**Qué necesita para análisis FOB:**
- 📐 **Histograma de desviaciones FOB** — distribución de `(FOB_declarado - FOB_esperado) / FOB_esperado`
- 📏 **Boxplot de desviación FOB por producto** — comparar si Palta tiene mayor sesgo que Arándano
- 🎯 **Curva ROC del ensemble** sobre el umbral de desviación FOB
- 📊 **Error de predicción XGBoost por rango de FOB** — ¿es igual de preciso para embarques pequeños que grandes?

### 2.4 Explorador de Datos — `/data` 🟢 AMPLIAR

**Qué tiene ahora:** Tabla de alertas, biblioteca RAG, formulario de indexación.

**Qué necesita para análisis FOB:**
- 🔍 **Filtro por rango de desviación FOB** (`< 10%`, `10-20%`, `> 20%`)
- 📥 **Exportar alertas FOB a CSV** con columnas: DAM, empresa, producto, FOB_dec, FOB_esp, desviacion%, score, decision
- 📊 **Mini-gráfico de barras** de desviación FOB inline en la tabla

### 2.5 Telemetría — `/telemetry` 🟢 AMPLIAR

**Qué tiene ahora:** Boxplots de tiempo de decisión y comprensión A/B.

**Qué necesita para análisis FOB:**
- 🎯 **Tasa de acierto en la decisión** — ¿cuántos auditores identificaron correctamente alertas con alta desviación FOB?
- 📊 **Correlación entre desviación FOB y tiempo de decisión** — ¿a mayor desviación, más tiempo?
- 🧮 **Tabla de decisiones por nivel de desviación FOB** — ¿las condiciones A/B afectan diferente según el % de desviación?

---

## 3. ARQUITECTURA FOB — Cómo Fluye el Análisis

```
DAM (Declaración Aduanera)
    │
    │  fob_declarado: $120,000
    │  peso_neto: 18,000 kg
    │  temperatura_contenedor: 7.2°C
    │  dias_retraso: 3
    │
    ▼
┌─────────────────────────────────────────────────┐
│  CAPA 1: XGBoost FOB Regressor                  │
│  → fob_esperado = $135,000                      │
│  → desviacion_pct = (120,000−135,000)/135,000   │
│                   = −11.1% (subvalorado)        │
└────────────────────────┬────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│  CAPA 2: PyOD Ensemble (¿es la desviación FOB   │
│          estadísticamente anómala?)             │
│                                                 │
│  IForest → P(anomalía) = 0.95 × 0.45 = 0.4275 │
│  LOF     → P(anomalía) = 0.98 × 0.30 = 0.2940 │
│  ECOD    → P(anomalía) = 0.92 × 0.25 = 0.2300 │
│                                       ────────  │
│                        SCORE TOTAL = 0.9515    │
│  (umbral: 0.65 → ALERTA ACTIVA ✅)             │
└────────────────────────┬────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│  CAPA 3: TreeSHAP (¿qué variable explica la     │
│          desviación FOB?)                       │
│                                                 │
│  fob_declarado:      +0.4231 ← principal        │
│  temperatura:        +0.2184                   │
│  dias_retraso:       +0.1562                   │
│  peso_neto:          −0.0891                   │
└────────────────────────┬────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│  CAPA 4: RAG pgvector (¿qué normativa regula    │
│          la desviación de valor FOB?)           │
│                                                 │
│  Consulta: "Palta Hass Rotterdam FOB −11%       │
│             temperatura 7.2°C retraso 3d"       │
│  → embedding(384-dim)                          │
│  → similitud coseno en pgvector                 │
│  → [FDA-1]: inspección si desv. FOB > 15%      │
│  → [SENASA-2]: protocolo si temp. > 7°C        │
│  → [LEY_IA-3]: explicabilidad obligatoria      │
│                                                 │
│  → Gemini / heurístico genera reporte en español│
└─────────────────────────────────────────────────┘
                         │
                         ▼
           Auditor adjudica decisión FOB:
           [Falsa alarma] [Confirmada] [Inspección]
           + Likert comprensión (1-5)
           + Tiempo de decisión (ms)
```

---

## 4. VARIABLES DEL ANÁLISIS FOB

| Variable | Tipo | Rol en el Pipeline |
|---|---|---|
| `valor_fob_declarado` | Numérica (USD) | Input Capa 1 y 2; target de predicción |
| `valor_fob_esperado` | Numérica (USD) | Output Capa 1 (XGBoost) |
| `desviacion_fob_pct` | Calculada (%) | `(dec - esp) / esp * 100` |
| `score_anomalia` | Numérica [0,1] | Output Capa 2 (PyOD) |
| `peso_neto_kg` | Numérica | Feature Capa 1 (ratio peso/precio) |
| `temperatura_contenedor_c` | Numérica | Feature Capa 1 (calidad deterioro) |
| `dias_retraso_logistico` | Numérica | Feature Capa 1 (triangulación precios) |
| `shap_valor_fob` | Atribución SHAP | Output Capa 3 — contribución del FOB al score |
| `producto` | Categórica | Segmentación de análisis (Palta, Uva, etc.) |
| `empresa_exportadora` | Texto | Trazabilidad y análisis de comportamiento |
| `mercado_destino` | Texto | Contexto normativo (FDA=EEUU, SENASA=general) |

---

## 5. ALERTAS SEMBRADAS — Análisis FOB Real

| ID Alerta | Empresa | Producto | FOB Declarado | FOB Esperado | Desv. % | Score | Estado |
|---|---|---|---:|---:|---:|---:|---|
| AL-2026-0012 | Agroworld S.A.C. | Palta | $120,000 | $135,000 | **−11.1%** | 0.95 | PENDIENTE |
| AL-2026-0009 | Agroworld S.A.C. | Palta | $110,000 | $130,000 | **−15.4%** | 0.88 | CONFIRMADA |
| AL-2026-0014 | Frutas del Pedregal | Mango | $60,000 | $75,000 | **−20.0%** | 0.82 | PENDIENTE |
| AL-2026-0011 | Valles del Norte | Uva | $85,000 | $110,000 | **−22.7%** | 0.72 | PENDIENTE |
| AL-2026-0013 | Campos de Ica | Palta | $95,000 | $112,000 | **−15.2%** | 0.78 | PENDIENTE |
| AL-2026-0008 | Valles del Norte | Uva | $98,000 | $105,000 | −6.7% | 0.58 | EN_REVISION |
| AL-2026-0005 | Frutas del Pedregal | Mango | $55,000 | $68,000 | **−19.1%** | 0.76 | REFIERE |
| AL-2026-0007 | Agroworld S.A.C. | Palta | $130,000 | $133,000 | −2.3% | 0.35 | EN_REVISION |
| AL-2026-0010 | BerryCorp Andina | Arándano | $145,000 | $160,000 | **−9.4%** | 0.65 | PENDIENTE |
| AL-2026-0006 | BerryCorp Andina | Arándano | $150,000 | $152,000 | −1.3% | 0.42 | FALSA_ALARMA |
| AL-2026-0004 | Campos de Ica | Palta | $105,000 | $108,000 | −2.8% | 0.31 | FALSA_ALARMA |

**Resumen estadístico FOB (datos semilla):**
- Desviación media: **−11.5%**
- Desviación máxima: **−22.7%** (AL-2026-0011, Uva)
- Alertas con desviación > 10%: **7 de 11** (63.6%)
- Score promedio: **0.672**

---

## 6. LO QUE QUEDA PENDIENTE

### 6.1 Análisis FOB Pendiente (Prioridad ALTA)

| Tarea | Detalle | Bloqueo |
|---|---|---|
| **Gráficos FOB en Dashboard** | Dispersión dec vs esp, tendencia, distribución por desviación | Requiere endpoint backend |
| **Histograma de desviaciones** | Distribución de % de error FOB por alerta | Requiere cálculo en backend |
| **Boxplot FOB por producto** | Comparar sesgo de modelo por categoría agroexportadora | Requiere datos reales |
| **Exportar CSV de alertas FOB** | Con columnas: DAM, empresa, FOB_dec, FOB_esp, desv%, score, decisión | Implementación frontend |
| **Correlación desviación FOB vs tiempo decisión** | ¿A mayor desviación FOB más tiempo tarda el auditor? | Requiere N muestral |

### 6.2 Datos Reales Pendientes

| Tarea | Detalle |
|---|---|
| Dataset SUNAT/ADUANET real | Exportaciones reales de Palta, Uva, Arándano, Mango 2020-2025 |
| Reentrenamiento XGBoost | Con datos reales para predicción FOB robusta |
| Reentrenamiento PyOD | Con distribución real de precios FOB para calibración del score |
| Split temporal 70/10/20 | Para evaluación definitiva del modelo |
| Experimento con usuarios reales | ≥ 10 auditores/condición para significancia estadística |

### 6.3 Vistas Pendientes de Mejorar

| Vista | Mejora Pendiente |
|---|---|
| `/dashboard` | Gráficos análisis FOB (dispersión, tendencia, distribución) |
| `/integrity` | Histograma y boxplot de desviación FOB por producto |
| `/data` | Filtro por rango de desviación FOB + exportación CSV |
| `/telemetry` | Correlación desviación FOB vs tiempo de decisión |

---

## 7. USUARIOS Y CREDENCIALES

| Username | Contraseña | Condición | Descripción |
|---|---|---|---|
| `auditor1` | `correct` | INTEGRADO (A) | Ve las 4 capas de IA incluyendo SHAP y RAG |
| `auditor2` | `correct` | AISLADO (B) | Solo ve FOB declarado, esperado y score |
| `admin` | `correct` | ADMIN | Panel completo de administración |

---

## 8. ACCESO AL SISTEMA

```bash
# Levantar el sistema (primera vez ~10 min por descarga de dependencias ML)
cd sistema-web-agro
docker-compose up --build -d

# Verificar servicios
docker ps

# Acceder
# Frontend:  http://localhost:8050
# API REST:  http://localhost:5000/api
# DB:        localhost:5432 | DB: agro_audit | User: postgres | Pass: postgres
```

---

*Última actualización: Junio 2026 | Commit: `5f5c6d8`*
