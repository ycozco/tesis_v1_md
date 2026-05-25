# 📊 HITOS Y CRONOGRAMA — Rigor Académico y Datasets
## Agroexportación — Sistema Integrado de Predicción y Anomalías

**Creado**: 2026-05-15  
**Versión**: 1.0  
**Estado**: Plan operativo — LISTO PARA EJECUCIÓN

---

## 📅 CRONOGRAMA VISUAL

```
2026 MAYO                                           JUNIO                    JULIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

15  20  22  27│ 30  01  05  10  12  15  20  22│ 01
 ▲   │   │   │       │   │   │   │   │   │   │       │
 │   │   │   │       │   │   │   │   │   │   │       │
 │   └H1-Tareas 1.1   │   │   │   │   │   │   │       │
 │       └─H2-Tarea 2.1│   │   │   │   │   │   │       │
 │          └─H2-01    └HITO 2   │   │   │   │       │
 │                     └H3-01    │   └HITO 3│   │       │
 │                               └H4-01    │ HITO 4    │
 │                                         └─────────HITO 5
 ▼
 HOY
```

---

## 🎯 LOS 5 HITOS

### HITO 1: VARIABLES OPERACIONALIZADAS ✓ En progreso
**Fecha límite**: 📍 **2026-05-27**  
**Responsable**: Yoset Cozco Mauri  
**Duración**: 2 semanas (15-27 mayo)

#### Tareas incluidas
- [x] **Tarea 1.1** (Fecha: 2026-05-20): Revisar Capítulo I → Listar variables
  - **Entregable**: `variables-listado.md`
  - **Criterio**: Mínimo 5 variables identificadas

- [ ] **Tarea 1.2** (Fecha: 2026-05-27): Operacionalizar variables
  - **Entregable**: Tabla con 5 variables + fórmulas
  - **Criterio**: Cada variable tiene definición conceptual + operacional + rango + instrumento

- [ ] **Tarea 1.3** (Fecha: 2026-05-30): Validar con asesor
  - **Entregable**: Documento signado por Dr. Cornejo
  - **Criterio**: Asesor aprueba operacionalizaciones

#### Progreso estimado
```
Semana 1 (15-20 mayo): Tarea 1.1 ███░░░░░░░ 30%
Semana 2 (21-27 mayo): Tarea 1.2 y 1.3 ░░░░░░░░░░ 0% (EN PROGRESO)
```

#### Impacto si se retrasa
⚠️ **Crítico**: Retraso en Tarea 1.2 impide Hito 2 y 3. **Prioridad máxima**.

---

### HITO 2: DATASETS IDENTIFICADOS Y DATASHEETS INICIADOS ⏳ Pendiente
**Fecha límite**: 📍 **2026-06-01**  
**Responsable**: Yoset Cozco Mauri + Dr. Víctor Manuel Cornejo Aparicio  
**Duración**: 1.5 semanas (22 mayo - 1 junio)

#### Tareas incluidas
- [ ] **Tarea 2.1.1** (Fecha: 2026-05-22): Contactar MIDAGRI, SENASA, SENAMHI
  - **Entregable**: `sources-log.md` con emails, contactos, respuestas
  - **Criterio**: 3 instituciones contactadas, 2 responden

- [ ] **Tarea 2.1.2** (Fecha: 2026-05-25): Descargar muestras de fuentes públicas
  - **Entregable**: 3 archivos CSV (primeras 1,000 filas)
  - **Criterio**: 100% de fuentes descargables

- [ ] **Tarea 2.2.1** (Fecha: 2026-05-25): Descargar datos SENAMHI
  - **Entregable**: 3 CSV con datos climáticos de estaciones
  - **Criterio**: Datos disponibles y descargables

- [ ] **Tarea 3.1** (Fecha: 2026-05-30): Crear plantilla Datasheet
  - **Entregable**: Google Doc compartido con estructura estándar
  - **Criterio**: Plantilla completa con 7 secciones

#### Progreso estimado
```
Semana 1 (22-27 mayo): Contactos + descargas ███░░░░░░░ 40%
Semana 2 (28-01 jun): Plantilla + validación ░░░░░░░░░░ 0% (PRÓXIMA)
```

#### Criterio de éxito
✅ Mínimo 3 datasets identificados  
✅ 2 de 3 con acceso confirmado  
✅ Plantilla Datasheet lista

---

### HITO 3: DATOS DESCARGADOS, LIMPIEZA Y VALIDACIÓN ⏳ Pendiente
**Fecha límite**: 📍 **2026-06-10**  
**Responsable**: Yoset Cozco Mauri  
**Duración**: 2 semanas (1-10 junio)

#### Tareas incluidas
- [ ] **Tarea 2.1.2** (Fecha: 2026-06-05): Generar dataset sintético si falta datos internos
  - **Entregable**: Script Python + 10,000 registros CSV
  - **Criterio**: Datos realistas y documentados

- [ ] **Tarea 2.2.2** (Fecha: 2026-05-28): Validar calidad SENAMHI
  - **Entregable**: `data-quality-senamhi.md`
  - **Criterio**: <5% valores faltantes

- [ ] **Tarea 4.1** (Fecha: 2026-06-05): Crear script de validación
  - **Entregable**: `scripts/data_quality_check.py`
  - **Criterio**: Verifica completitud, outliers, duplicados

- [ ] **Tarea 4.2** (Fecha: 2026-06-10): Ejecutar validación en 3 datasets
  - **Entregable**: 3 reportes CSV con métricas de calidad
  - **Criterio**: 95%+ completitud en cada dataset

- [ ] **Tarea 3.2 y 3.3** (Fecha: 2026-06-10): Completar Datasheets para 3 datasets
  - **Entregable**: 3 Markdown files en `entregable/datasheets/`
  - **Criterio**: 7/7 secciones completadas por dataset

#### Progreso estimado
```
Semana 1 (01-05 junio): Sintéticos + validación ██░░░░░░░░ 25%
Semana 2 (06-10 junio): Datasheets + finalización ░░░░░░░░░░ 0% (PRÓXIMA)
```

#### Criterio de éxito
✅ 3 datasets crudos descargados  
✅ Calidad validada ≥95% en completitud  
✅ 3 Datasheets completados  
✅ Scripts de reproducibilidad en repositorio

---

### HITO 4: ANÁLISIS DE FAIRNESS COMPLETADO ⏳ Pendiente
**Fecha límite**: 📍 **2026-06-22**  
**Responsable**: Yoset Cozco Mauri  
**Duración**: 2 semanas (10-22 junio)

#### Tareas incluidas
- [ ] **Tarea 5.1** (Fecha: 2026-06-15): Crear matriz de subgrupos
  - **Entregable**: `fairness-subgroups.csv` (región, tamaño empresa, producto, período)
  - **Criterio**: 4+ subgrupos definidos

- [ ] **Tarea 5.2** (Fecha: 2026-06-20): Implementar cálculo de fairness
  - **Entregable**: `scripts/fairness_analysis.py` (scikit-learn + numpy)
  - **Criterio**: Calcula F1-Score, Precision, Recall por subgrupo

- [ ] **Tarea 5.3** (Fecha: 2026-06-22): Generar reporte de fairness
  - **Entregable**: `fairness-report.md` + gráficos (matplotlib/seaborn)
  - **Criterio**: Tabla comparativa + 3+ visualizaciones

- [ ] **Tarea 5.4** (Fecha: 2026-06-22): Documentar trade-offs
  - **Entregable**: `fairness-tradeoffs.md`
  - **Criterio**: Si no es posible equidad perfecta, explicado porqué

#### Progreso estimado
```
Semana 1 (10-15 junio): Matriz de subgrupos ███░░░░░░░ 30%
Semana 2 (16-22 junio): Análisis + reportes ░░░░░░░░░░ 0% (PRÓXIMA)
```

#### Criterio de éxito
✅ Fairness calculado en 4+ subgrupos  
✅ Diferencia de F1-Score ≤5% entre subgrupos (o documentado porqué es > 5%)  
✅ Gráficos de comparación  
✅ Trade-offs explícitos

---

### HITO 5: DOCUMENTACIÓN INTEGRADA EN TESIS ⏳ Pendiente
**Fecha límite**: 📍 **2026-07-01**  
**Responsable**: Yoset Cozco Mauri + Dr. Víctor Manuel Cornejo Aparicio  
**Duración**: 1 semana (22 junio - 1 julio)

#### Tareas incluidas
- [ ] **Integración Cap. III**: Actualizar Metodología con datasets y scripts
  - **Entregable**: Capítulo III redactado con referencias a datasheets
  - **Criterio**: Describe cómo se obtuvieron, limpiaron y validaron datos

- [ ] **Integración Anexos**: Insertar Datasheets y fairness report
  - **Entregable**: Anexo A (Datasheets), Anexo B (Fairness Report)
  - **Criterio**: Navegables y cruzadas con Cap. III

- [ ] **Reproducibilidad**: Scripts en repositorio con README
  - **Entregable**: `/scripts/` con .py ejecutables + `REPRODUCIBILIDAD.md`
  - **Criterio**: Cualquier investigador puede replicar análisis

- [ ] **Validación con asesor**: Revisión final antes de Cap. IV
  - **Entregable**: Documento signado de aprobación
  - **Criterio**: Dr. Cornejo aprueba metodología y datos

#### Progreso estimado
```
Semana 1 (22-01 julio): Integración + reproducibilidad ░░░░░░░░░░ 0%
```

#### Criterio de éxito
✅ Cap. III completado con 50%+ del contenido metodológico  
✅ Anexos listos  
✅ Scripts reproducibles  
✅ Asesor aprueba

---

## 📊 TABLA RESUMEN DE HITOS

| Hito | Fecha Límite | Responsable | Tareas | Entregables | Criterio de Éxito | Estado |
|------|--------------|-------------|--------|-------------|-------------------|--------|
| **1** | 2026-05-27 | Yoset | 3 | Variables operacionalizadas | Signadas por asesor | ⏳ Semana 1 |
| **2** | 2026-06-01 | Y + Dr. C | 4 | Sources + plantilla datasheet | 2/3 datasets accesibles | ⏳ Semana 2 |
| **3** | 2026-06-10 | Yoset | 5 | 3 datasets + datasheets | 95%+ calidad, scripts | ⏳ Semana 3-4 |
| **4** | 2026-06-22 | Yoset | 4 | Fairness report + gráficos | Diferencia ≤5% o doc. | ⏳ Semana 5-6 |
| **5** | 2026-07-01 | Y + Dr. C | 4 | Cap. III + anexos + scripts | Reproducible + aprobado | ⏳ Semana 7 |

---

## ⚠️ RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| MIDAGRI no responde a tiempo | 🟡 Media | 🔴 Alto | Generar datos sintéticos desde Tarea 2.1.2 |
| Retraso en Hito 1 | 🟡 Media | 🔴 Crítico | Priorizar tareas 1.1 y 1.2 esta semana |
| Datos con >10% valores faltantes | 🟢 Baja | 🟡 Medio | Usar imputación + documentar en datasheet |
| Fairness no se alcanza (<5% diff.) | 🟡 Media | 🟡 Medio | Documentar trade-offs + buscar subgrupos alternativos |
| Retraso general | 🟡 Media | 🔴 Crítico | Revisar checkup semanal + ajustar scope |

---

## 📋 CHECKUPS Y SEGUIMIENTO

### Checkup Semanal (Cada lunes)

**Qué revisar** (5 minutos):
1. ¿Completé tareas de esta semana? ✓/✗
2. ¿Hay bloqueadores? (sí/no)
3. ¿Debo ajustar timeline? (sí/no)

**Registro**: Actualizar `checkups-semanal.md` en repositorio

**Responsable**: Yoset

---

### Checkup de Hito (Al completar cada hito)

**Antes de declarar "Completo"**:
1. Verificar todos los entregables existen
2. Validar criterio de éxito
3. Obtener firma/aprobación de Dr. Cornejo
4. Crear `hito-N-completado.md` con evidencia

**Responsable**: Yoset + Dr. Cornejo

---

### Checkup de Integración (Cada 2 semanas)

**Qué revisar**:
1. ¿Alineado con plan general (plan-detallado.md)?
2. ¿Los 49 indicadores de revisión están siendo completados?
3. ¿Hay conflictos entre hitos?

**Responsable**: Yoset + Dr. Cornejo

---

## 🎯 PRÓXIMAS ACCIONES (HOY)

**HITO 1 - Tarea 1.1 (Fecha: 2026-05-20)**

- [ ] Abrir archivo `docs/tesis.md` Capítulo I
- [ ] Hacer lista de TODAS las variables mencionadas
- [ ] Crear documento `variables-listado.md`
- [ ] Entregar a Dr. Cornejo

**Tiempo estimado**: 2-3 horas

**Entregable**: Archivo con mínimo 5 variables identificadas

---

## 📞 CONTACTOS Y REFERENCIAS

**Asesor Responsable**: Dr. Víctor Manuel Cornejo Aparicio  
**Tesista Responsable**: Yoset Cozco Mauri  
**Fecha de Creación**: 2026-05-15  
**Última Actualización**: 2026-05-15

**Plan Detallado**: `docs/plan-rigor-academico-datasets.md`  
**Matriz de Seguimiento**: `entregable/matriz-seguimiento-49indicadores.csv`

---

**✅ ESTADO**: LISTO PARA EJECUCIÓN

Comienza con **Tarea 1.1 HOY**. Fecha límite: 2026-05-20.

¡Adelante! 🚀
