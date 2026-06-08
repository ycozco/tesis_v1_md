# PLAN DETALLADO: RIGOR ACADÉMICO Y BÚSQUEDA DE DATASETS
## Con hitos, checkups y integración con plan general

**Versión**: 2.0  
**Fecha de creación**: 2026-05-15  
**Responsable**: Yoset Cozco Mauri  
**Asesor**: Dr. Víctor Manuel Cornejo Aparicio

---

## 📋 ÍNDICE DEL PLAN

1. [Objetivo general](#objetivo-general)
2. [Rigor académico: 5 pilares](#rigor-académico-5-pilares)
3. [Búsqueda y evaluación de datasets](#búsqueda-y-evaluación-de-datasets)
4. [Cronograma y hitos](#cronograma-y-hitos)
5. [Checkups y validación](#checkups-y-validación)
6. [Integración con plan-detallado.md](#integración-con-plan-detalladomd)

---

## OBJETIVO GENERAL

Establecer un **marco académico riguroso** para la tesis mediante:

✅ **Operacionalización clara** de todas las variables (5 variables principales)  
✅ **Búsqueda y validación** de datasets agroexportadores (mínimo 3 datasets)  
✅ **Documentación de metodología** según Datasheets for Datasets (Gebru et al., 2021)  
✅ **Matriz de conformidad regulatoria** (SBS N° 053-2023, DS-115-2025-PCM, EU AI Act)  
✅ **Validación de fairness y sesgo** por subgrupos (región, tamaño empresa)  

**Resultado esperado**: Tesis completamente documentada y lista para defensa con trazabilidad probada.

---

## RIGOR ACADÉMICO: 5 PILARES

### PILAR 1: OPERACIONALIZACIÓN DE VARIABLES

**Objetivo**: Cada concepto abstracto de la tesis → fórmula matemática o escala medible

#### Variables principales a operacionalizar

| # | Variable | Definición Conceptual | Definición Operacional | Tipo | Estado |
|---|----------|----------------------|------------------------|------|--------|
| 1 | **Precisión de Predicción Tabular** | Capacidad del modelo GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) de predecir correctamente rendimiento operativo | F1-Score (Medida Armónica de Precisión y Exhaustividad) = 2 × (Precisión × Recall) / (Precisión + Recall) | Métrica | ⏳ Pendiente |
| 2 | **Tasa de Detección de Anomalías** | Proporción de anomalías reales correctamente identificadas por ensemble | PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad) (Precision-Recall Area Under Curve) | Métrica | ⏳ Pendiente |
| 3 | **Explicabilidad de Decisiones** | Comprensión por supervisor sin IA de por qué modelo flagea riesgo | % de supervisores que entienden explicación SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley) (meta: 80%+) | Cualitativa | ⏳ Pendiente |
| 4 | **Equidad del Modelo (Fairness)** | Desempeño similar del modelo en PYME vs grandes exportadores | Diferencia máxima de F1-Score entre subgrupos ≤ 5% | Métrica | ⏳ Pendiente |
| 5 | **Conformidad Regulatoria** | Trazabilidad y documentación según SBS N° 053 y DS-115 | Matriz de cumplimiento: % de requisitos satisfechos | Documental | ⏳ Pendiente |

#### Tareas por variable

**Tarea 1.1**: Revisar Capítulo I de tesis → Listar todas las variables mencionadas  
**Responsable**: Yoset | **Fecha límite**: 2026-05-20 | **Entregable**: Documento "variables-listado.md"

**Tarea 1.2**: Para cada variable, completar la tabla anterior  
**Responsable**: Yoset | **Fecha límite**: 2026-05-27 | **Entregable**: Tabla completada + ejemplos de cálculo

**Tarea 1.3**: Validar con asesor que operacionalizaciones son medibles  
**Responsable**: Yoset + Dr. Cornejo | **Fecha límite**: 2026-05-30 | **Entregable**: Documento signado

---

### PILAR 2: BÚSQUEDA SISTEMÁTICA DE DATASETS

**Objetivo**: Localizar y documentar mínimo 3 datasets reales de agroexportación peruana

#### 2.1 DATASET PRIMARIO (Datos operativos internos)

**Descripción**: Logs operativos de empresa agroexportadora (si aplica) o datos sintéticos representativos

**Fuentes candidatas**:
- Empresa colaboradora con Ingeniería de Sistemas UNSA (contactar)
- MIDAGRI — datos de producción y comercialización
- SENASA — certificaciones y calidad
- SENAMHI — contexto climático

**Características esperadas**:
- Registros: 5,000 — 50,000 transacciones/registros
- Período: 2020-2026 (al menos 2 años)
- Variables: Producción, calidad, logística, precios, anomalías marcadas manualmente
- Formato: CSV, Excel, o JSON

**Tareas**:

**Tarea 2.1.1**: Contactar MIDAGRI y SENASA solicitando acceso a datos  
**Responsable**: Yoset + Dr. Cornejo | **Fecha límite**: 2026-05-22 | **Entregable**: Email de solicitud + respuestas

**Tarea 2.1.2**: Si no hay datos públicos, generar dataset sintético realista  
**Responsable**: Yoset | **Fecha límite**: 2026-06-05 | **Entregable**: Script Python + 10,000 registros sintéticos

**Tarea 2.1.3**: Crear Datasheet para Dataset Primario (según Gebru et al.)  
**Responsable**: Yoset | **Fecha límite**: 2026-06-10 | **Entregable**: `datasheets/dataset-primario-datasheet.md`

---

#### 2.2 DATASET SECUNDARIO (Contexto climático)

**Descripción**: Series de temperatura, precipitación, humedad de zonas agroexportadoras peruanas

**Fuentes principales**:
- **SENAMHI**: Descargar datos históricos de estaciones meteorológicas
  - Arequipa (zona principal de agroexportación)
  - Lima/Ica (segundo nivel)
  - Junín/Amazonía (complementario)
- Período: 2020-2026

**Características**:
- Variables: T°max, T°min, precipitación, humedad relativa, radiación solar
- Granularidad: Diaria
- Registros: ~2,000 por estación

**Tareas**:

**Tarea 2.2.1**: Descargar datos SENAMHI para 3 estaciones  
**Responsable**: Yoset | **Fecha límite**: 2026-05-25 | **Entregable**: 3 archivos CSV

**Tarea 2.2.2**: Validar calidad de datos (valores faltantes, outliers)  
**Responsable**: Yoset | **Fecha límite**: 2026-05-28 | **Entregable**: Reporte de calidad (datos-senamhi-calidad.md)

**Tarea 2.2.3**: Crear Datasheet para Dataset Climático  
**Responsable**: Yoset | **Fecha límite**: 2026-06-10 | **Entregable**: `datasheets/dataset-climatico-datasheet.md`

---

#### 2.3 DATASET TERCIARIO (Contexto macroeconómico)

**Descripción**: Precios internacionales, tipo de cambio, índices de actividad

**Fuentes principales**:
- **UN Comtrade**: Exportaciones/importaciones por producto
- **World Bank**: Índices de precios, actividad económica
- **INEI**: Índices sectoriales peruanos
- **SUNAT**: Estadísticas aduaneras

**Características**:
- Variables: Precios internacionales, tipo de cambio, índices sectoriales
- Granularidad: Semanal/mensual
- Registros: ~300 (si es mensual, 25 años)

**Tareas**:

**Tarea 2.3.1**: Descargar 3 series macroeconómicas (Comtrade, INEI, SUNAT)  
**Responsable**: Yoset | **Fecha límite**: 2026-05-25 | **Entregable**: 3 archivos CSV

**Tarea 2.3.2**: Validar consistencia y correlación con datos primarios  
**Responsable**: Yoset | **Fecha límite**: 2026-05-28 | **Entregable**: Análisis de correlación (notebook.ipynb)

**Tarea 2.3.3**: Crear Datasheet para Dataset Macroeconómico  
**Responsable**: Yoset | **Fecha límite**: 2026-06-10 | **Entregable**: `datasheets/dataset-macro-datasheet.md`

---

### PILAR 3: DOCUMENTACIÓN DE DATASETS (Datasheets Framework)

**Objetivo**: Aplicar el estándar Gebru et al. (2018) a cada dataset

**Estructura de Datasheet** (para cada dataset):

```markdown
# Datasheet for Dataset: [NOMBRE]

## 1. MOTIVATION
- ¿Por qué se creó este dataset?
- ¿Qué necesidad resuelve?
- ¿Cuál fue el contexto histórico o de proyecto?

## 2. COMPOSITION
- Número de registros: ______
- Número de características: ______
- Período temporal: ______
- Granularidad (diaria, semanal, mensual): ______
- Geografía cubierta: ______
- Valores faltantes: ___% (por característica)
- Outliers identificados: ______
- Sesgos conocidos: ______
  - Sesgo temporal: ¿Hay períodos con menos datos?
  - Sesgo geográfico: ¿Faltan regiones?
  - Sesgo de cobertura: ¿Qué tipos de casos NO están representados?

## 3. COLLECTION PROCESS
- Método de recolección: Manual / Automático / Hybrid
- Anonimización: Sí / No / Parcial
- Instrumentos utilizados: ______
- Frecuencia de recolección: ______
- Supervisión de calidad: ¿Quién validaba?

## 4. PREPROCESSING & CLEANING
- Transformaciones aplicadas: ______
- Valores removidos: ______
- Métodos de imputación (si aplica): ______
- Normalización/escalado: Sí / No / Método

## 5. USES
- Usos RECOMENDADOS: ______
- Usos NO RECOMENDADOS: ______
- Contexto de aplicación: ______

## 6. DISTRIBUTION & ACCESS
- ¿Disponible públicamente? Sí / No / Bajo solicitud
- Licencia (CC-BY, CC-BY-SA, Propietaria, etc.): ______
- Formato: CSV / JSON / Excel / SQL
- Contacto para acceso: ______

## 7. MAINTENANCE & UPDATES
- ¿Se actualiza regularmente? Sí / No / Frecuencia
- Soporte técnico disponible: ______
- Fecha de última actualización: ______
```

**Tareas**:

**Tarea 3.1**: Crear plantilla Datasheet en Google Docs  
**Responsable**: Yoset | **Fecha límite**: 2026-05-30 | **Entregable**: Documento compartido

**Tarea 3.2**: Completar Datasheets para 3 datasets (antes de 2026-06-10)  
**Responsable**: Yoset | **Fecha límite**: 2026-06-10 | **Entregable**: 3 Datasheets en formato .md

**Tarea 3.3**: Validar Datasheets con asesor + guardar en repositorio  
**Responsable**: Yoset + Dr. Cornejo | **Fecha límite**: 2026-06-12 | **Entregable**: Datasheets en `/entregable/datasheets/`

---

### PILAR 4: VALIDACIÓN DE CALIDAD DE DATOS

**Objetivo**: Garantizar que los datos sean reproducibles, completos y confiables

**Métricas de calidad**:

| Criterio | Métrica | Umbral | Método |
|----------|---------|--------|--------|
| **Completitud** | % registros con datos completos | ≥ 95% | Contar nulos por fila |
| **Consistencia** | % valores dentro de rango esperado | ≥ 98% | Domain validation |
| **Outliers** | % valores anómalos detectados | ≤ 5% | IQR o Z-score |
| **Duplicados** | % registros únicos | ≥ 99% | Hash de fila |
| **Temporalidad** | % registros en período esperado | ≥ 99% | Validar fecha |

**Tareas**:

**Tarea 4.1**: Crear script de validación (Python: pandas + numpy)  
**Responsable**: Yoset | **Fecha límite**: 2026-06-05 | **Entregable**: `scripts/data_quality_check.py`

**Tarea 4.2**: Ejecutar validación en 3 datasets  
**Responsable**: Yoset | **Fecha límite**: 2026-06-10 | **Entregable**: 3 reportes de calidad (CSV)

**Tarea 4.3**: Documentar issues de calidad y decisiones de limpieza  
**Responsable**: Yoset | **Fecha límite**: 2026-06-12 | **Entregable**: `data-quality-decisions.md`

---

### PILAR 5: ANÁLISIS DE FAIRNESS Y SESGO

**Objetivo**: Evaluar que el modelo no discrimine en subgrupos de interés

**Subgrupos a evaluar**:

| Subgrupo | Valores | Justificación |
|----------|--------|---|
| **Tamaño empresa** | PYME (1-50 emp.) vs Grande (>50 emp.) | Impacto regulatorio diferente |
| **Región geográfica** | Arequipa, Lima-Ica, Junín | Condiciones climáticas distintas |
| **Tipo de producto** | Fruta, verdura, procesado | Cadenas de valor diferentes |
| **Período temporal** | Verano vs Invierno | Estacionalidad de agroexportación |

**Métricas de fairness**:

```
Para cada subgrupo:
- F1-Score (métrica principal)
- Precision (evitar falsos positivos)
- Recall (evitar falsos negativos)
- Diferencia máxima respecto a población general ≤ 5%
```

**Tareas**:

**Tarea 5.1**: Crear matriz de subgrupos en dataset primario  
**Responsable**: Yoset | **Fecha límite**: 2026-06-15 | **Entregable**: `fairness-subgroups.csv`

**Tarea 5.2**: Implementar cálculo de fairness (Python: scikit-learn)  
**Responsable**: Yoset | **Fecha límite**: 2026-06-20 | **Entregable**: `scripts/fairness_analysis.py`

**Tarea 5.3**: Generar reporte de fairness por subgrupo  
**Responsable**: Yoset | **Fecha límite**: 2026-06-22 | **Entregable**: `fairness-report.md` + gráficos

**Tarea 5.4**: Documentar trade-offs (si mejorar fairness degrada precisión)  
**Responsable**: Yoset | **Fecha límite**: 2026-06-22 | **Entregable**: `fairness-tradeoffs.md`

---

## BÚSQUEDA Y EVALUACIÓN DE DATASETS

### Mapa de fuentes de datos (Referencia: fuentes-datos-agroexport.txt)

```
CATEGORÍA 1: DATOS INTERNOS PRIMARIOS
├─ Producción por lote/campaña
├─ Inventario, mermas y rechazos
├─ Logística (tiempos, transporte, cadena de frío)
├─ Calidad (inspecciones, no conformidades)
└─ Mantenimiento/paradas operativas
   → Responsable: Contactar empresas colaboradoras

CATEGORÍA 2: FUENTES PÚBLICAS PERUANAS
├─ MIDAGRI: Precios, volumen, boletines comerciales
├─ SENASA: Plagas, alertas, certificaciones, BPA
├─ SENAMHI: Temperatura, lluvia, avisos meteorológicos
├─ INEI: Índices sectoriales, precios mayoristas
├─ SUNAT: Estadísticas aduaneras
└─ datosabiertos.gob.pe: Catálogo estatal
   → Responsable: Yoset (descargas directas)

CATEGORÍA 3: FUENTES INTERNACIONALES
├─ FAOSTAT: Producción agrícola, área, rendimiento
├─ UN Comtrade: Exportaciones/importaciones por producto
└─ World Bank: Contexto macroeconómico
   → Responsable: Yoset (APIs + web scraping)

CATEGORÍA 4: FUENTES COMPLEMENTARIAS
├─ Tipo de cambio y precios
├─ Imágenes satelitales y vegetación
└─ Datos climáticos reanalizados
   → Responsable: Yoset (según disponibilidad)
```

### Búsqueda iterativa

**Iteración 1 (Semana 1-2)**:
- [ ] Contactar MIDAGRI, SENASA, SENAMHI por datos
- [ ] Descargar de datosabiertos.gob.pe
- [ ] Recopilar enlaces de UN Comtrade y World Bank
- **Entregable**: Archivo `sources-log.md` con URLs y contactos

**Iteración 2 (Semana 2-3)**:
- [ ] Verificar accesibilidad de fuentes
- [ ] Descargar muestras (primeras 1000 filas)
- [ ] Evaluar calidad inicial
- **Entregable**: Reporte de viabilidad `feasibility-datasets.md`

**Iteración 3 (Semana 3-4)**:
- [ ] Descargar datasets completos
- [ ] Ejecutar limpieza y validación
- [ ] Generar Datasheets
- **Entregable**: 3 Datasheets + datos limpios

---

## CRONOGRAMA Y HITOS

### HITO 1: Variables operacionalizadas
**Fecha**: 2026-05-27  
**Responsable**: Yoset  
**Entregables**:
- [ ] Tabla de 5 variables con definiciones conceptual y operacional
- [ ] Ejemplos de cálculo para cada métrica
- [ ] Documento signado por asesor

**Criterio de éxito**: Cada variable tiene fórmula matemática o escala medible clara.

---

### HITO 2: Datasets identificados y Datasheets iniciados
**Fecha**: 2026-06-01  
**Responsable**: Yoset + Dr. Cornejo  
**Entregables**:
- [ ] Lista de 3 datasets candidatos con fuente
- [ ] Primeros contactos realizados (MIDAGRI, SENASA)
- [ ] Plantilla de Datasheet compartida

**Criterio de éxito**: Mínimo 2 de 3 datasets con acceso confirmado.

---

### HITO 3: Datos descargados y limpieza iniciada
**Fecha**: 2026-06-10  
**Responsable**: Yoset  
**Entregables**:
- [ ] 3 datasets crudos descargados (CSV)
- [ ] Script de validación de calidad ejecutado
- [ ] Reportes de calidad generados (datos-quality-*.csv)
- [ ] Datasheets completados para 3 datasets

**Criterio de éxito**: 100% de registros descargados, calidad ≥ 95% en completitud.

---

### HITO 4: Análisis de fairness completado
**Fecha**: 2026-06-22  
**Responsable**: Yoset  
**Entregables**:
- [ ] Matriz de fairness por subgrupos generada
- [ ] Reporte de fairness (F1-score por subgrupo)
- [ ] Gráficos de comparación (matplotib/seaborn)
- [ ] Documento de trade-offs (precisión vs fairness)

**Criterio de éxito**: Diferencia de F1-Score entre subgrupos ≤ 5% o documentado porqué no es posible.

---

### HITO 5: Documentación integrada en tesis
**Fecha**: 2026-07-01  
**Responsable**: Yoset + Dr. Cornejo  
**Entregables**:
- [ ] Capítulo III actualizado con metodología de datasets
- [ ] Datasheets integrados en Anexos
- [ ] Script de reproducibilidad en repositorio
- [ ] Tesis lista para primeras conclusiones de Cap. IV

**Criterio de éxito**: Cualquier investigador puede reproducir análisis con datos y scripts.

---

## CHECKUPS Y VALIDACIÓN

### CHECKUP SEMANAL (Cada lunes)

**Qué revisar**:
1. ¿Avancé en operacionalización de variables? (Pilar 1)
2. ¿Obtuve respuestas de MIDAGRI/SENASA? (Pilar 2)
3. ¿Descargué datos nuevos? (Búsqueda y evaluación)
4. ¿Ejecuté validación de calidad? (Pilar 4)
5. ¿Actualicé Datasheets? (Pilar 3)

**Herramienta**: Actualizar `matriz-seguimiento-49indicadores.csv` cada lunes

**Responsable**: Yoset  
**Registro**: Archivo `checkups-semanal.md` en repositorio

---

### CHECKUP DE HITO (Al cumplir cada hito)

**Antes de declarar "completado" un hito**:

1. **Verificación de entregables**: ¿Existen los archivos listados?
2. **Validación de criterio de éxito**: ¿Se cumple el umbral (ej. 95% completitud)?
3. **Revisión con asesor**: ¿Aprobación de Dr. Cornejo?
4. **Documentación**: ¿Todo está en el repositorio?

**Responsable**: Yoset + Dr. Cornejo (firma)

**Documento**: Crear `hito-N-completado.md` con evidencia

---

### CHECKUP INTEGRACIÓN CON PLAN GENERAL

**Periodicidad**: Cada 2 semanas  
**Qué revisar**:
1. ¿Se alineó el avance con el plan-detallado.md?
2. ¿Los indicadores de las 8 categorías de revisión están siendo completados?
3. ¿Hay bloqueadores o riesgos?

**Responsable**: Yoset + Dr. Cornejo  
**Documento**: Actualizar sección "Checkup del avance" en plan-detallado.md

---

## INTEGRACIÓN CON PLAN-DETALLADO.MD

### Cómo se integra este plan

Este documento **NO reemplaza** `plan-detallado.md`, pero se **anexa** como nueva sección.

**Ubicación propuesta en plan-detallado.md**:

```
[Índice actual del plan-detallado.md]
├─ ESTRUCTURA COMPLETA Y AVANCE ACTUAL
├─ PLAN DE REVISIONES AMPLIADO (8 CATEGORÍAS)
├─ ÍNDICE DEL PLAN
└─ [NUEVA SECCIÓN] ➜ PLAN DETALLADO DE RIGOR ACADÉMICO Y DATASETS
    ├─ Objetivo general
    ├─ Rigor académico: 5 pilares
    ├─ Búsqueda y evaluación de datasets
    ├─ Cronograma y hitos
    └─ Checkups y validación
```

### Actualización de "Checkup del avance"

**Agregar a la sección "Checkup del avance" del plan-detallado.md**:

```markdown
### Checkup del avance (ACTUALIZADO)

- [x] Portada, presentación, resumen y abstract definidos
- [x] Índice general y estructura de navegación definidos
- [x] Capítulo I avanzado y alineado al enfoque agroexportador
- [x] Capítulo II muy avanzado en antecedentes, estado del arte
- [x] Mapa inicial de fuentes de datos agroexportadores definido
- [x] Plan de revisiones expandido a 8 categorías
- [x] Búsqueda amplia de estándares internacionales (NIST, etc.)
- **[NEW]** [ ] Operacionalización de 5 variables completada
- **[NEW]** [ ] Búsqueda de 3 datasets agroexportadores completada
- **[NEW]** [ ] Datasheets para datasets generados
- **[NEW]** [ ] Análisis de fairness y sesgo completado
- [ ] Capítulo III migrado completamente al dominio agroexportador
- [ ] Capítulo IV consolidado con resultados reales
- [ ] Capítulo V cerrado con conclusiones y limitaciones finales
- [ ] Anexos y bibliografía depurados por completo
```

### Tracking integrado

**En `matriz-seguimiento-49indicadores.csv`**, agregar nuevas filas:

```
Rigor Científico, Operacionalización, "Variables operacionalizadas", "Cada variable con fórmula medible", ⏳ Pendiente, Yoset, Crítica, 2026-05-20, 2026-05-27
Datos y Referencias, Búsqueda, "Datasets agroexportadores identificados", "Mínimo 3 datasets de fuentes públicas", ⏳ Pendiente, Yoset, Crítica, 2026-05-22, 2026-06-01
Datos y Referencias, Documentación, "Datasheets para datasets", "Formato Gebru et al. para 3 datasets", ⏳ Pendiente, Yoset, Crítica, 2026-06-01, 2026-06-10
Ética y Sesgo, Sesgo, "Fairness por subgrupos evaluado", "F1-Score por región, tamaño empresa", ⏳ Pendiente, Yoset, Crítica, 2026-06-15, 2026-06-22
```

---

## RECURSOS Y REFERENCIAS

### Software requerido
- Python 3.10+ (pandas, numpy, scikit-learn)
- Git + GitHub (versionado de datos y scripts)
- Jupyter Notebook (documentación ejecutable)
- Google Docs/Sheets (colaboración con asesor)

### Documentación de referencia
- Gebru et al. (2018) — Datasheets for Datasets
- Mitchell et al. (2018) — Model Cards for Model Reporting
- NIST AI RMF (2023) — Risk Management Framework
- Normativas: SBS N° 053-2023, DS-115-2025-PCM, EU AI Act 2024

### Sitios de datos
- MIDAGRI: www.midagri.gob.pe
- SENASA: www.senasa.gob.pe
- SENAMHI: www.senamhi.gob.pe
- INEI: www.inei.gob.pe
- SUNAT: www.sunat.gob.pe
- UN Comtrade: https://comtrade.un.org
- FAOSTAT: https://www.fao.org/faostat
- datosabiertos.gob.pe: https://datosabiertos.gob.pe

---

## CONCLUSIÓN

Este plan establece un **marco riguroso de 5 pilares** para garantizar que la tesis es:

✅ **Académicamente sólida** (variables operacionalizadas)  
✅ **Empíricamente validada** (datos reales de agroexportación)  
✅ **Reproducible** (Datasheets + scripts)  
✅ **Equitativa** (análisis de fairness)  
✅ **Regulatoriamente conforme** (SBS, DS-115, EU AI Act)

**Próximo paso**: Yoset comienza Hito 1 (variables operacionalizadas) antes del 2026-05-27.

---

**Responsable**: Yoset Cozco Mauri  
**Aprobado por**: Dr. Víctor Manuel Cornejo Aparicio  
**Fecha de aprobación**: [Pendiente firma]  
**Última actualización**: 2026-05-15
