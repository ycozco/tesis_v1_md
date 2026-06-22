# PLAN DE DESARROLLO DETALLADO — Sistema Agro-Intelligence Oversight
## Análisis FOB con IA Explicable | Tesis UNSA 2026

> **Fecha de elaboración:** 21 de Junio de 2026 — 23:31 (UTC-5, Arequipa, Perú)  
> **Autor:** Yoset Cozco Mauri  
> **Estado del sistema:** Servicios activos en Docker (`localhost:8050`)  
> **Repositorio:** https://github.com/ycozco/tesis_v1_md  
> **Rama activa:** `main`

---

## CONTEXTO ACTUAL DEL SISTEMA

El prototipo **Agro-Intelligence Oversight** está **operativo y funcional** con:
- ✅ Pipeline completo de 4 capas IA (XGBoost + PyOD + TreeSHAP + RAG pgvector)
- ✅ 10 vistas React implementadas
- ✅ 11 alertas FOB sembradas en PostgreSQL
- ✅ Telemetría A/B capturando decisiones de auditores
- ✅ Normativas RAG indexadas (FDA, SENASA, Ley IA)

**Enfoque único del sistema:** Análisis del valor FOB declarado en exportaciones agroalimentarias peruanas para detectar posibles subvaloraciones mediante modelos de IA explicable.

---

## PLAN DE DESARROLLO — SPRINT 1
### Semana: 22 Junio — 28 Junio 2026 · Prioridad: ALTA

**Meta:** Completar los gráficos de análisis FOB en el Dashboard y la vista de Integridad.

---

### TAREA 1.1 — Dashboard FOB: Scatter Plot Declarado vs Esperado
**Fecha objetivo:** 23 Junio 2026  
**Archivo afectado:** `frontend/src/pages/Dashboard.jsx`  
**Backend:** Nuevo endpoint `GET /api/dashboard/fob-scatter`  
**Archivo backend:** `backend/app.py`

**Descripción:**
Agregar al Dashboard un gráfico de dispersión (scatter plot) que muestre, para cada alerta, el valor FOB declarado en el eje X y el valor FOB esperado (XGBoost) en el eje Y. La línea diagonal a 45° representa la "declaración perfecta". Puntos sobre la línea = subvaloración (riesgo). Los puntos se colorean por score de anomalía (verde < 0.65, naranja 0.65–0.85, rojo > 0.85).

**Implementación backend (`app.py`):**
```python
@app.route('/api/dashboard/fob-scatter', methods=['GET'])
def fob_scatter():
    alerts = OperacionAlerta.query.filter(
        OperacionAlerta.valor_fob_esperado.isnot(None)
    ).all()
    return jsonify([{
        'id_alerta': a.id_alerta,
        'producto': a.producto,
        'empresa': a.empresa_exportadora[:20],
        'fob_declarado': float(a.valor_fob_declarado),
        'fob_esperado': float(a.valor_fob_esperado),
        'desviacion_pct': round(
            (float(a.valor_fob_declarado) - float(a.valor_fob_esperado))
            / float(a.valor_fob_esperado) * 100, 2
        ),
        'score': float(a.score_anomalia or 0)
    } for a in alerts])
```

**Implementación frontend (Dashboard.jsx):**
- Usar librería `recharts` (ya en package.json) o implementar con SVG puro
- Gráfico: `<ScatterChart>` con eje X = FOB declarado, eje Y = FOB esperado
- Línea de referencia diagonal (FOB dec = FOB esp)
- Tooltip con: ID alerta, empresa, producto, desviación %, score
- Leyenda de colores por nivel de riesgo

**Criterio de aceptación:**
- [ ] Scatter plot visible en `/dashboard` sección "Análisis FOB"
- [ ] Línea diagonal de referencia trazada
- [ ] Colores por score: verde/naranja/rojo
- [ ] Tooltip funcional al pasar el mouse sobre cada punto
- [ ] Endpoint devuelve JSON con los campos requeridos

---

### TAREA 1.2 — Dashboard FOB: Distribución de Desviación por Rangos
**Fecha objetivo:** 23 Junio 2026  
**Archivo afectado:** `frontend/src/pages/Dashboard.jsx` + `backend/app.py`  
**Endpoint:** `GET /api/dashboard/fob-distribution`

**Descripción:**
Gráfico de barras mostrando cuántas alertas caen en cada rango de desviación FOB:
- `0% – 5%`: Riesgo bajo (verde)
- `5% – 10%`: Riesgo moderado (amarillo)
- `10% – 15%`: Riesgo alto (naranja)
- `> 15%`: Riesgo crítico (rojo)

**Implementación backend:**
```python
@app.route('/api/dashboard/fob-distribution', methods=['GET'])
def fob_distribution():
    alerts = OperacionAlerta.query.filter(
        OperacionAlerta.valor_fob_esperado.isnot(None)
    ).all()
    rangos = {'0-5%': 0, '5-10%': 0, '10-15%': 0, '>15%': 0}
    for a in alerts:
        desv = abs((float(a.valor_fob_declarado) - float(a.valor_fob_esperado))
                   / float(a.valor_fob_esperado) * 100)
        if desv < 5:
            rangos['0-5%'] += 1
        elif desv < 10:
            rangos['5-10%'] += 1
        elif desv < 15:
            rangos['10-15%'] += 1
        else:
            rangos['>15%'] += 1
    return jsonify([{'rango': k, 'count': v} for k, v in rangos.items()])
```

**Criterio de aceptación:**
- [ ] Gráfico de barras por rango de desviación visible en Dashboard
- [ ] Colores diferenciados por nivel de riesgo
- [ ] Cada barra muestra el conteo de alertas

---

### TAREA 1.3 — Dashboard FOB: Top 5 Desviaciones y KPI de Desviación Media
**Fecha objetivo:** 24 Junio 2026  
**Archivos afectados:** `frontend/src/pages/Dashboard.jsx`, `backend/app.py`

**Descripción:**
- KPI card: "Desviación FOB Media" (% promedio de todas las alertas)
- KPI card: "Alertas con Desv. > 10%" (conteo)
- Tabla compacta: Top 5 alertas con mayor desviación FOB (empresa, producto, FOB dec, FOB esp, % desviación, score)

**Implementación backend (agregar a `/api/dashboard/stats`):**
```python
fob_deviations = []
for a in all_alerts:
    if a.valor_fob_esperado:
        desv = abs((float(a.valor_fob_declarado) - float(a.valor_fob_esperado))
                   / float(a.valor_fob_esperado) * 100)
        fob_deviations.append({
            'id': a.id_alerta,
            'empresa': a.empresa_exportadora,
            'producto': a.producto,
            'fob_declarado': float(a.valor_fob_declarado),
            'fob_esperado': float(a.valor_fob_esperado),
            'desviacion_pct': round(desv, 2),
            'score': float(a.score_anomalia or 0)
        })

stats['avg_fob_deviation_pct'] = round(
    sum(d['desviacion_pct'] for d in fob_deviations) / len(fob_deviations), 2
) if fob_deviations else 0
stats['alerts_high_deviation'] = sum(1 for d in fob_deviations if d['desviacion_pct'] > 10)
stats['top5_deviations'] = sorted(fob_deviations, key=lambda x: -x['desviacion_pct'])[:5]
```

**Criterio de aceptación:**
- [ ] KPI "Desviación FOB Media" visible como card numérico
- [ ] KPI "Alertas con Desv. > 10%" visible como card numérico
- [ ] Tabla Top 5 desviaciones ordenada correctamente

---

### TAREA 1.4 — Integridad: Boxplot de Desviación FOB por Producto
**Fecha objetivo:** 25 Junio 2026  
**Archivo afectado:** `frontend/src/pages/Integrity.jsx` + `backend/app.py`  
**Endpoint:** `GET /api/integrity/fob-by-product`

**Descripción:**
Boxplot (o violin chart simplificado con barras de error) que muestre la distribución de la desviación FOB por producto (Palta, Uva, Arándano, Mango). Responde a la pregunta de investigación: **¿El modelo XGBoost es igualmente preciso para todos los productos?**

**Implementación backend:**
```python
@app.route('/api/integrity/fob-by-product', methods=['GET'])
def fob_by_product():
    alerts = OperacionAlerta.query.filter(
        OperacionAlerta.valor_fob_esperado.isnot(None)
    ).all()
    by_product = {}
    for a in alerts:
        p = a.producto
        desv = abs((float(a.valor_fob_declarado) - float(a.valor_fob_esperado))
                   / float(a.valor_fob_esperado) * 100)
        if p not in by_product:
            by_product[p] = []
        by_product[p].append(desv)

    result = []
    import statistics
    for prod, desvs in by_product.items():
        result.append({
            'producto': prod,
            'n': len(desvs),
            'media': round(statistics.mean(desvs), 2),
            'mediana': round(statistics.median(desvs), 2),
            'min': round(min(desvs), 2),
            'max': round(max(desvs), 2),
            'desv_std': round(statistics.stdev(desvs), 2) if len(desvs) > 1 else 0
        })
    return jsonify(result)
```

**Criterio de aceptación:**
- [ ] Gráfico de barras con error bars (media ± std) por producto
- [ ] Tabla con estadísticos: N, media, mediana, min, max, σ por producto
- [ ] Integrado en la vista `/integrity`

---

### TAREA 1.5 — Integridad: Histograma de Distribución de Errores de Predicción FOB
**Fecha objetivo:** 26 Junio 2026  
**Archivo afectado:** `frontend/src/pages/Integrity.jsx` + `backend/app.py`

**Descripción:**
Histograma que muestre la distribución del error de predicción del modelo XGBoost: `error = FOB_declarado - FOB_esperado`. Valores negativos = subvaloración (el sistema detecta bien). Valores positivos = sobrevaloración (raro en aduanas). Forma de campana centrada en 0 = modelo bien calibrado.

**Criterio de aceptación:**
- [ ] Histograma de barras del error absoluto FOB visible en `/integrity`
- [ ] Eje X: rangos de error en USD
- [ ] Eje Y: frecuencia (N alertas)
- [ ] Línea vertical en x=0 como referencia de "sin error"

---

## PLAN DE DESARROLLO — SPRINT 2
### Semana: 29 Junio — 05 Julio 2026 · Prioridad: MEDIA

---

### TAREA 2.1 — Exportar Alertas FOB a CSV
**Fecha objetivo:** 30 Junio 2026  
**Archivo afectado:** `frontend/src/pages/Data.jsx` + `backend/app.py`  
**Endpoint:** `GET /api/alerts/export/csv`

**Descripción:**
Botón "Exportar CSV" en el Explorador de Datos que descarga un archivo con las columnas:
`DAM, empresa, producto, destino, fob_declarado, fob_esperado, desviacion_pct, score_anomalia, decision_auditor, condicion_experimento, tiempo_decision_s, likert_comprension, fecha`

**Implementación backend:**
```python
@app.route('/api/alerts/export/csv', methods=['GET'])
def export_alerts_csv():
    import csv
    import io
    alerts = OperacionAlerta.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'id_alerta', 'num_dam', 'empresa', 'producto', 'destino',
        'fob_declarado_usd', 'fob_esperado_usd', 'desviacion_pct',
        'score_anomalia', 'estado', 'fecha_registro'
    ])
    for a in alerts:
        desv = ''
        if a.valor_fob_esperado:
            desv = round(
                (float(a.valor_fob_declarado) - float(a.valor_fob_esperado))
                / float(a.valor_fob_esperado) * 100, 2
            )
        writer.writerow([
            a.id_alerta, a.num_dam, a.empresa_exportadora, a.producto,
            a.mercado_destino, float(a.valor_fob_declarado),
            float(a.valor_fob_esperado) if a.valor_fob_esperado else '',
            desv, float(a.score_anomalia or 0), a.estado,
            a.creado_en.strftime('%Y-%m-%d') if a.creado_en else ''
        ])
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=alertas_fob.csv'
    return response
```

**Criterio de aceptación:**
- [ ] Botón "⬇ Exportar CSV" visible en `/data`
- [ ] Descarga archivo `alertas_fob.csv` con las columnas especificadas
- [ ] Incluye columna `desviacion_pct` calculada
- [ ] Funciona para todas las alertas de la base de datos

---

### TAREA 2.2 — Filtro por Rango de Desviación FOB en Explorador de Datos
**Fecha objetivo:** 01 Julio 2026  
**Archivo afectado:** `frontend/src/pages/Data.jsx`

**Descripción:**
Agregar selector de filtro en el panel de datos:
```
Filtrar por desviación FOB:
[Todos ▾] [0–5%] [5–10%] [10–15%] [>15%]
```
Al seleccionar un rango, la tabla filtra las alertas que caen dentro de ese rango de desviación.

**Criterio de aceptación:**
- [ ] Select de filtro por rango de desviación visible en `/data`
- [ ] Filtrado funcional en el cliente (sin nueva llamada al servidor)
- [ ] Badge con conteo de resultados actualizándose al filtrar

---

### TAREA 2.3 — Detalle de Alerta: Gauge de Desviación FOB
**Fecha objetivo:** 02 Julio 2026  
**Archivo afectado:** `frontend/src/pages/Detail.jsx`

**Descripción:**
Agregar un indicador visual tipo medidor (gauge) al inicio de la vista de detalle que muestre de forma inmediata y visual el porcentaje de desviación FOB. El gauge tiene tres zonas: verde (< 5%), naranja (5-15%), rojo (> 15%). El puntero apunta al valor calculado.

**Implementación (SVG puro en React):**
```jsx
// Gauge semicircular SVG
// Min: 0%, Max: 30% desviación
// Colores: 0-5% verde, 5-15% naranja, >15% rojo
// Puntero dinámico según desviacion_pct
const FobGauge = ({ desvPct }) => {
  const angle = Math.min(desvPct / 30 * 180, 180)
  // ... render SVG
}
```

**Criterio de aceptación:**
- [ ] Gauge semicircular visible al inicio de `/alerts/:id`
- [ ] Muestra % de desviación FOB de forma prominente
- [ ] Zonas de color correctas (verde/naranja/rojo)
- [ ] Puntero animado al cargar

---

### TAREA 2.4 — Detalle de Alerta: Historial FOB del Exportador
**Fecha objetivo:** 03 Julio 2026  
**Archivo afectado:** `frontend/src/pages/Detail.jsx` + `backend/app.py`  
**Endpoint:** `GET /api/alerts/<id>/company-history`

**Descripción:**
En la vista de detalle de una alerta FOB, mostrar una mini-tabla con el historial de alertas previas de la misma empresa exportadora. Esto permite al auditor ver si la subvaloración es un patrón recurrente o un hecho aislado.

**Implementación backend:**
```python
@app.route('/api/alerts/<id_alerta>/company-history', methods=['GET'])
def company_history(id_alerta):
    alert = OperacionAlerta.query.get_or_404(id_alerta)
    history = OperacionAlerta.query.filter(
        OperacionAlerta.empresa_exportadora == alert.empresa_exportadora,
        OperacionAlerta.id_alerta != id_alerta
    ).order_by(OperacionAlerta.creado_en.desc()).limit(5).all()
    return jsonify([{
        'id_alerta': h.id_alerta,
        'producto': h.producto,
        'fob_declarado': float(h.valor_fob_declarado),
        'fob_esperado': float(h.valor_fob_esperado) if h.valor_fob_esperado else None,
        'score': float(h.score_anomalia or 0),
        'estado': h.estado
    } for h in history])
```

**Criterio de aceptación:**
- [ ] Sección "Historial del Exportador" visible en `/alerts/:id`
- [ ] Muestra últimas 5 alertas de la misma empresa
- [ ] Incluye: producto, FOB declarado, desviación %, score, estado
- [ ] Si no hay historial, muestra mensaje "Primer registro de esta empresa"

---

### TAREA 2.5 — Telemetría: Correlación Desviación FOB vs Tiempo de Decisión
**Fecha objetivo:** 04 Julio 2026  
**Archivo afectado:** `frontend/src/pages/Telemetry.jsx` + `backend/app.py`  
**Endpoint:** `GET /api/telemetry/fob-correlation`

**Descripción:**
Gráfico de dispersión que muestre la correlación entre el porcentaje de desviación FOB de una alerta y el tiempo que tardó el auditor en tomar la decisión. Hipótesis: a mayor desviación FOB (más obvia la anomalía), menos tiempo debería tardar el auditor con IA explicable (Condición A) vs sin ella (Condición B).

**Criterio de aceptación:**
- [ ] Scatter plot visible en `/telemetry`
- [ ] Eje X: % desviación FOB
- [ ] Eje Y: tiempo de decisión (segundos)
- [ ] Puntos coloreados por condición (azul=INTEGRADO, gris=AISLADO)
- [ ] Línea de tendencia por condición

---

## PLAN DE DESARROLLO — SPRINT 3
### Semana: 06 Julio — 12 Julio 2026 · Prioridad: INVESTIGACIÓN

---

### TAREA 3.1 — Reentrenamiento con Datos SUNAT/ADUANET
**Fecha objetivo:** 08 Julio 2026  
**Archivos afectados:** `backend/init_db.py`, `backend/app.py`

**Descripción:**
Cuando se consigan los datos reales de SUNAT/ADUANET, reentrenar los modelos con:
- Dataset: DAMs de exportación agroalimentaria 2020-2025
- Productos: Palta (`080440`), Uva (`080610`), Arándano (`081040`)
- Split temporal: 70% train / 10% validation / 20% test
- Semilla fija: `random_state=42`

**Criterio de aceptación:**
- [ ] Dataset real integrado en `backend/data/dataset_real_v1.csv`
- [ ] Script de preprocesamiento documentado
- [ ] Modelos reentrenados y serializados en `models_weights/`
- [ ] Métricas evaluadas: MAE, RMSE, R² para XGBoost; PR-AUC, ROC-AUC, F1 para PyOD
- [ ] Reporte de calidad en `docs/02-41-capitulo4-resultados-cuantitativos.md`

---

### TAREA 3.2 — Experimento A/B con Usuarios Reales
**Fecha objetivo:** 10 Julio 2026  
**Participantes requeridos:** ≥ 10 por condición (20 total)

**Protocolo:**
1. Briefing a participantes (5 min): explicar el contexto aduanero y la interfaz
2. Sesión de práctica con alerta de prueba (5 min)
3. Evaluación de 5 alertas FOB reales por participante (15-20 min)
4. Cuestionario post-sesión SUS (System Usability Scale) (5 min)
5. Descarga de telemetría: `GET /api/telemetry/export/csv`

**Métricas a recolectar:**
- Tiempo de decisión por alerta (ms) — capturado automáticamente
- Likert de comprensión (1-5) — registrado en BD
- Tasa de decisión correcta (vs ground truth auditado)
- Score SUS de usabilidad (calculado post-sesión)

**Criterio de aceptación:**
- [ ] N ≥ 10 participantes por condición con datos limpios
- [ ] Exportar dataset de telemetría para análisis estadístico
- [ ] Aplicar prueba Mann-Whitney U sobre tiempos de decisión
- [ ] Reportar efecto tamaño (Cohen's d o rank-biserial correlation)

---

### TAREA 3.3 — Análisis Estadístico y Redacción Capítulo 5
**Fecha objetivo:** 12 Julio 2026  
**Documento objetivo:** `docs/02-50-capitulo5.md`

**Descripción:**
Con los datos reales del experimento, completar el Capítulo 5 de resultados:

- Tabla de resultados cuantitativos del modelo (MAE, RMSE, F1, AUC-ROC)
- Boxplots comparativos A/B de tiempo de decisión y comprensión
- Pruebas de hipótesis H1, H2, H3
- Análisis de fairness (FPR por producto, DPR)
- Discusión y contraste con literatura

**Criterio de aceptación:**
- [ ] Capítulo 5 completo con todos los resultados del experimento
- [ ] Tablas con IC al 95%
- [ ] Gráficos exportados en alta resolución para la tesis
- [ ] Hipótesis aceptadas o rechazadas con justificación estadística

---

## CRONOGRAMA RESUMEN

```
JUNIO 2026
──────────────────────────────────────────────────
22 Jun ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
23 Jun ▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  [1.1] Scatter FOB + [1.2] Distribución
24 Jun ░░░░▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  [1.3] KPIs Dashboard FOB
25 Jun ░░░░░░░▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  [1.4] Boxplot Integridad
26 Jun ░░░░░░░░░░▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░  [1.5] Histograma errores FOB
27-28 Jun ──── Buffer / Pruebas / Push a GitHub ────

JULIO 2026
──────────────────────────────────────────────────
30 Jun ░░░░░░░░░░░░░▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░  [2.1] Exportar CSV
01 Jul ░░░░░░░░░░░░░░░░▓▓▓░░░░░░░░░░░░░░░░░░░░░░  [2.2] Filtro desviación
02 Jul ░░░░░░░░░░░░░░░░░░░▓▓▓░░░░░░░░░░░░░░░░░░░  [2.3] Gauge FOB Detalle
03 Jul ░░░░░░░░░░░░░░░░░░░░░░▓▓▓░░░░░░░░░░░░░░░░  [2.4] Historial exportador
04 Jul ░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓░░░░░░░░░░░░░  [2.5] Correlación telemetría
05 Jul ──── Buffer / Pruebas / Documentación ────

08 Jul ░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓░░░░░░░░░░  [3.1] Datos reales SUNAT
10 Jul ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓░░░░░░░  [3.2] Experimento usuarios
12 Jul ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓░░░░  [3.3] Análisis estadístico
```

---

## CHECKLIST DE PROGRESO (actualizar con cada tarea completada)

### Sprint 1 — Gráficos FOB
- [ ] **1.1** Scatter FOB declarado vs esperado en Dashboard
- [ ] **1.2** Distribución de alertas por rango de desviación FOB
- [ ] **1.3** KPIs: desviación media y alertas críticas en Dashboard
- [ ] **1.4** Boxplot de desviación FOB por producto en Integridad
- [ ] **1.5** Histograma de errores de predicción XGBoost en Integridad

### Sprint 2 — Funcionalidades Operativas
- [ ] **2.1** Exportación de alertas FOB a CSV
- [ ] **2.2** Filtro por rango de desviación FOB en Explorador de Datos
- [ ] **2.3** Gauge visual de desviación FOB en vista Detalle
- [ ] **2.4** Historial de alertas FOB por empresa exportadora
- [ ] **2.5** Correlación desviación FOB vs tiempo de decisión en Telemetría

### Sprint 3 — Investigación y Resultados
- [ ] **3.1** Integración de dataset real SUNAT/ADUANET y reentrenamiento
- [ ] **3.2** Experimento A/B con ≥ 20 participantes reales
- [ ] **3.3** Análisis estadístico y redacción Capítulo 5 definitivo

---

## NOTAS TÉCNICAS IMPORTANTES

### Librerías disponibles para gráficos
El proyecto usa React + Vite. Para implementar los gráficos FOB se puede usar:

```bash
# Opción A: recharts (recomendado, simple, React-native)
npm install recharts

# Opción B: SVG puro (sin dependencia extra)
# Usar <svg>, <path>, <circle> directamente en JSX

# Opción C: chart.js con react-chartjs-2
npm install chart.js react-chartjs-2
```

### Convención de colores del sistema
```
Riesgo CRÍTICO (score > 0.85): #ef4444  (rojo)
Riesgo ALTO    (score 0.65-0.85): #f97316  (naranja)
Riesgo BAJO    (score < 0.65): #22c55e  (verde)
Condición A (INTEGRADO): #6366f1   (violeta)
Condición B (AISLADO): #94a3b8    (gris)
FOB declarado: #f59e0b             (ámbar)
FOB esperado:  #3b82f6             (azul)
```

### Endpoints activos confirmados (22 Junio 2026)
```
GET  /api/dashboard/stats       ✅ Activo
GET  /api/alerts                ✅ Activo
GET  /api/alerts/<id>           ✅ Activo (pipeline 4 capas)
POST /api/alerts/<id>/adjudicate ✅ Activo (telemetría)
GET  /api/telemetry/stats       ✅ Activo
GET  /api/integrity/stats       ✅ Activo
GET  /api/config                ✅ Activo
GET  /api/config/documents      ✅ Activo
POST /api/config/documents      ✅ Activo (indexar normativas)
GET  /api/history               ✅ Activo

PENDIENTES DE IMPLEMENTAR:
GET  /api/dashboard/fob-scatter      🔲 Sprint 1.1
GET  /api/dashboard/fob-distribution 🔲 Sprint 1.2
GET  /api/integrity/fob-by-product   🔲 Sprint 1.4
GET  /api/alerts/<id>/company-history 🔲 Sprint 2.4
GET  /api/telemetry/fob-correlation  🔲 Sprint 2.5
GET  /api/alerts/export/csv          🔲 Sprint 2.1
```

---

*Documento generado: 21 de Junio de 2026, 23:31 hrs (Arequipa, Perú)*  
*Sistema activo en: `http://localhost:8050` — Commit base: `77a3ee0`*
