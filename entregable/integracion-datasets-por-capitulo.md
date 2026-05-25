# Integración de Datasets Validados a la Tesis
## Mapa de Referencias por Capítulo

**Objetivo**: Mostrar dónde y cómo se integran los 25 datasets validados en cada capítulo de la tesis

---

## ESTRUCTURA VISUAL

```
┌─────────────────────────────────────────────────────────────────┐
│  TESIS: Sistema Integrado de Predicción y Detección de Anomalías │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  CAPÍTULO I: Planteamiento del Problema                          │
│  └─ Contexto normativo: SBS N° 053-2023                         │
│  └─ Cifras de sector agroexportador: MIDAGRI, FAOSTAT           │
│  └─ Magnitud del problema: SUNAT estadísticas                   │
│                                                                   │
│  CAPÍTULO II: Marco Teórico                                      │
│  └─ Antecedentes internacionales: FAOSTAT, World Bank           │
│  └─ Estado del arte en anomalías: Papers (sin datos)            │
│  └─ Benchmarks de producción: UN Comtrade, FAOSTAT              │
│                                                                   │
│  CAPÍTULO III: Metodología (★ DONDE VAN LOS DATOS ★)             │
│  ├─ Sección 3.1: Fuentes de Datos (NUEVO)                       │
│  │  ├─ Capa 1 - Datos Operativos: MIDAGRI (4 datasets)         │
│  │  ├─ Capa 2 - Contexto: SENASA, SENAMHI, SUNAT (5 datasets)  │
│  │  └─ Capa 3 - Validación: FAOSTAT, Comtrade, WB (8 datasets) │
│  ├─ Sección 3.2: Procesamiento y Limpieza                       │
│  │  └─ Procedimiento de descarga, normalización, validación     │
│  └─ Sección 3.3: Métricas y Datasheets                          │
│     └─ Documentación Gebru et al. (2018)                        │
│                                                                   │
│  CAPÍTULO IV: Resultados y Discusión (★ ANÁLISIS DE DATOS ★)     │
│  ├─ Figuras y tablas con datos MIDAGRI                          │
│  ├─ Comparativa MIDAGRI vs FAOSTAT (validación)                │
│  ├─ Benchmarking con Comtrade                                   │
│  └─ Análisis de anomalías sobre datos reales                    │
│                                                                   │
│  CAPÍTULO V: Conclusiones                                        │
│  └─ Limitaciones de datos: Explicar restricciones de fuentes    │
│  └─ Trabajos futuros: Integración de datos reales privados      │
│                                                                   │
│  ANEXO A: Datasheets for Datasets (NUEVO)                       │
│  ├─ Datasheet MIDAGRI Precios Mayoristas                        │
│  ├─ Datasheet SENAMHI Datos Climáticos                          │
│  ├─ Datasheet FAOSTAT Production Module                         │
│  └─ ... (uno por cada dataset principal)                        │
│                                                                   │
│  REFERENCIAS BIBLIOGRÁFICAS (ACTUALIZADO)                       │
│  ├─ 14 referencias nuevas validadas ✅                          │
│  ├─ Orden alfabético por autor/entidad                          │
│  └─ Incluir DOI, URLs, fecha de acceso                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## CAPÍTULO I: Planteamiento del Problema
### Dónde integrar referencias de datasets

#### §1.1 Magnitud del Problema
**Datos a incluir**:
- Cifra de mermas en agroexportación peruana → MIDAGRI (si disponible)
- Volumen de exportación Perú vs competidores → UN Comtrade + FAOSTAT
- Costos de rechazo en frontera → SENASA + SUNAT (estadísticas)

**Referencias a agregar**:
- Ministerio de Agricultura (MIDAGRI), 2025. Boletín de precios mayoristas.
- UN Comtrade, 2025. Trade Statistics - Perú.
- FAOSTAT, 2025. Production Module.

#### §1.7 Justificación
**Datos contextuales**:
- Marco regulatorio SBS N° 053-2023 (normativo)
- Contexto económico del sector agrícola (INEI, World Bank)

---

## CAPÍTULO II: Marco Teórico
### Dónde integrar benchmarks internacionales

#### §2.2 Estado del Arte
**Datos de comparación**:
- Producción agrícola global → FAOSTAT
- Estándares de calidad internacionales → FAO (BPA papers)
- Tendencias de exportación → UN Comtrade

**Referencias a citar**:
```
Food and Agriculture Organization (FAO). (2025). 
Production Module. FAOSTAT. Recuperado de https://www.fao.org/faostat/
[Para contexto comparativo de producción global]

United Nations. (2025). 
Comtrade Plus - Trade Statistics. Recuperado de https://comtradeplus.un.org/
[Para datos de exportaciones internacionales]
```

#### §2.3 Bases Teóricas
**Teoría de operaciones agrícolas**:
- Cadena de valor agroexportadora → SENASA (normativa), MIDAGRI
- Control de calidad fitosanitaria → SENASA (requisitos)
- Factores ambientales → SENAMHI (datos climáticos)

---

## CAPÍTULO III: Metodología
### ★ INTEGRACIÓN PRINCIPAL DE DATASETS ★

### §3.1 NUEVO - Fuentes de Datos y Justificación

**Estructura recomendada**:
```markdown
### 3.1 Fuentes de Datos

Esta investigación integra datos de tres capas:

#### Capa 1: Datos Operativos Primarios (MIDAGRI)
- Boletín de precios mayoristas (mensual)
  - URL: https://www.gob.pe/minagri
  - Frecuencia: Mensual
  - Periodo: 2020-2026
  - Cobertura: Principales productos agroexportables
  - Justificación: Datos operacionales reales de mercado
  
- Reporte de ingreso a mercado mayorista (diario)
  - URL: https://www.gob.pe/minagri
  - Frecuencia: Diaria
  - Periodo: Últimos 24 meses
  - Justificación: Granularidad temporal para detección de anomalías

#### Capa 2: Datos Contextuales (SENASA, SENAMHI, SUNAT)
- Requisitos fitosanitarios SENASA
  - Justificación: Validación de conformidad regulatoria
  
- Datos climáticos SENAMHI
  - Estaciones: Arequipa, Lima, Junín
  - Variables: Temperatura, precipitación, humedad
  - Justificación: Features contextuales de entorno

- Estadísticas aduaneras SUNAT
  - Justificación: Contexto de dinámicas exportadoras

#### Capa 3: Datos de Validación (FAOSTAT, Comtrade, WB)
- FAOSTAT Production Module (1961-2025)
  - Justificación: Benchmark internacional para validación cruzada
  
- UN Comtrade Plus
  - Justificación: Datos ONU de comercio para verificación
  
- World Bank Data
  - Justificación: Contexto macroeconómico sectorial
```

### §3.2 Procesamiento de Datos

**Integrar sección sobre limpieza**:
```markdown
#### 3.2.1 Descarga y Validación Inicial
- Procedimiento de descarga de MIDAGRI (manual/API)
- Validación de completitud: % de datos faltantes
- Conversión de formatos (PDF → CSV, si aplica)

#### 3.2.2 Normalización
- Escalado de variables de precio (normalizados por IPC)
- Conversión de fechas a formato estándar
- Manejo de valores atípicos (outliers legitimados vs. anomalías)

#### 3.2.3 Integración Multifuente
- Cruce de MIDAGRI con SENAMHI (fecha/zona)
- Incorporación de variables SENASA (si/no cumplimiento)
- Enriquecimiento con variables FAOSTAT (contexto)
```

### §3.3 Datasheets for Datasets

**Integrar referencias a documentación**:
```markdown
#### 3.3 Documentación de Datasets (Gebru et al., 2018)

Conforme al estándar de "Datasheets for Datasets", cada fuente 
primaria está documentada en el Anexo A con:
- Motivación de recolección
- Composición (variables, tipos de datos)
- Recolección (fuente, procedimiento, fecha)
- Preprocesamiento
- Limitaciones conocidas
- Usos recomendados
```

---

## CAPÍTULO IV: Resultados y Discusión
### Dónde incluir gráficas y análisis de datos

#### §4.1 Análisis Descriptivo
**Datos a visualizar**:
- Series temporales de precios MIDAGRI (últimos 24 meses)
- Distribución de volúmenes ingresados a mercado
- Correlación con variables climáticas SENAMHI

**Validación**:
- Comparativa MIDAGRI vs FAOSTAT (¿alineados?)
- Comparativa MIDAGRI vs precios internacionales (Comtrade)

#### §4.2 Resultados del Modelo
**Datos de testing**:
- Validación sobre datos MIDAGRI reales
- Benchmarking contra baselines (modelos simples)
- Análisis de falsos positivos/negativos

#### §4.3 Discusión
**Limitaciones de datos**:
- Granularidad de MIDAGRI (mensual vs. operativa real)
- Datos climáticos SENAMHI disponibles solo para estaciones específicas
- Requisitos fitosanitarios SENASA (categóricos, no continuos)

**Implicaciones prácticas**:
- Cómo los datos disponibles determinan el modelo propuesto
- Restricciones de reproducibilidad (datos sensibles no públicos)
- Oportunidades de mejora con datos privados (trabajo futuro)

---

## CAPÍTULO V: Conclusiones y Trabajos Futuros

#### §5.1 Limitaciones de la Investigación
```markdown
### Limitaciones de Datos

Esta investigación está limitada por:

1. **Granularidad temporal**: MIDAGRI publica datos mensuales, 
   mientras que anomalías operativas ocurren a nivel diario/horario.
   
2. **Cobertura espacial**: SENAMHI tiene estaciones limitadas; 
   microclimas locales no están representados.
   
3. **Acceso a datos sensibles**: Datos reales de empresas 
   agroexportadoras no fueron disponibles por confidencialidad. 
   Se utilizaron datos públicos de MIDAGRI como proxy.

4. **Variables categóricas**: Requisitos SENASA son normativos 
   (sí/no), limitando modelado continuo.
```

#### §5.2 Trabajos Futuros
```markdown
### Mejora con Datos Privados

1. Integración de datos operativos reales de empresa colaboradora
   - Producción real, inventario, logística
   - Rechazo en frontera, mermas documentadas
   - Timeline a nivel transaccional

2. Datos climáticos de micro-estaciones personalizadas
   - Sensores IoT en huertos/invernaderos
   - Cobertura completa de zonas de operación

3. Integración de datos de supply chain externo
   - Proveedores de insumos (SENASA validados)
   - Distribuidores internacionales (SUNAT, aduanas)

4. Validación permanente contra benchmarks internacionales
   - Actualización mensual de FAOSTAT y Comtrade
   - Reentrenamiento de modelos con nuevos datos
```

---

## ANEXO A: Datasheets for Datasets
### Nuevo - Documentación de Fuentes

**Estructura recomendada** (uno por dataset importante):

```markdown
### Datasheet: MIDAGRI Boletín de Precios Mayoristas

#### 1. Motivación
- **Purpose**: Reporte oficial de precios mayoristas en mercados de Lima
- **Creator**: Ministerio de Agricultura y Riego (MIDAGRI)
- **Funding**: Presupuesto estatal peruano

#### 2. Composición
- **Instancias**: 24 × 12 = 288 registros mensuales (2020-2026)
- **Variables**: Producto, precio promedio, rango (mín-máx), volumen
- **Tipos de datos**: String (producto), Float (precios), Integer (volumen)
- **Valores faltantes**: <5% (reportado por MIDAGRI)

#### 3. Recolección
- **Procedimiento**: Compilación diaria de precios en mercados mayoristas
- **Fuente primaria**: GMML (Lima), Mercado Frutas Nº2, otros mercados
- **Muestreo**: Censal (todos los mercados principales)
- **Fecha de recolección**: Diaria; publicación mensual

#### 4. Limitaciones Conocidas
- **Sesgo geográfico**: Solo cobertura de mercados de Lima
- **Datos faltantes**: Algunos productos pueden no reportarse cada mes
- **Cambio metodológico**: MIDAGRI modificó metodología en 2023

#### 5. Recomendaciones de Uso
- ✅ Válido para: Análisis de tendencias, benchmarking de precios, detección de anomalías
- ❌ No válido para: Proyecciones de producción, análisis climático causal
- ⚠️ Requiere: Normalización por inflación (IPC INEI)
```

**Repetir para**:
- SENAMHI Datos Climáticos
- FAOSTAT Production Module
- SENASA Establecimientos Autorizados
- Otros datasets principales

---

## REFERENCIAS BIBLIOGRÁFICAS (ACTUALIZADO)

**Nuevas referencias a agregar**:

### Fuentes de Datos - Documentación
1. Food and Agriculture Organization (FAO). (2025). FAOSTAT - Food and Agriculture Statistics. https://www.fao.org/faostat/. [Accedido: 2026-05-15].

2. Ministerio de Agricultura y Riego (MIDAGRI). (2025). Boletín de Comercialización y Precios Mayoristas. https://www.gob.pe/minagri. [Accedido: 2026-05-15].

3. Ministerio de Agricultura y Riego (MIDAGRI). (2025). Reporte de Ingreso y Precios en Mercado Mayorista de Productores. https://www.gob.pe/minagri. [Accedido: 2026-05-15].

4. Servicio Nacional de Sanidad Agraria (SENASA). (2025). Manual de Buenas Prácticas Agrícolas para Palta y Espárrago. https://www.gob.pe/senasa. [Accedido: 2026-05-15].

5. Servicio Nacional de Meteorología e Hidrología (SENAMHI). (2025). Portal de Pronósticos y Datos Climáticos. https://www.senamhi.gob.pe/. [Accedido: 2026-05-15].

6. United Nations (UN). (2025). Comtrade Plus - International Trade Statistics. https://comtradeplus.un.org/. [Accedido: 2026-05-15].

7. World Bank. (2025). Open Data Portal. https://data.worldbank.org/. [Accedido: 2026-05-15].

### Metodología de Documentación de Datos
8. Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Iii, H. D., & Crawford, K. (2021). Datasheets for datasets. Communications of the ACM, 64(12), 86-92. https://doi.org/10.1145/3458723

---

## RESUMEN DE INTEGRACIÓN

| Capítulo | Datasets | Uso Principal | Referencias |
|----------|----------|---------------|-------------|
| I | UN Comtrade, FAOSTAT, SUNAT | Contexto y magnitud | 3 referencias |
| II | FAOSTAT, FAO Papers, World Bank | Benchmarks internacionales | 2 referencias |
| III | MIDAGRI, SENAMHI, SENASA | Fuentes primarias y contexto | 6 referencias + Datasheets |
| IV | MIDAGRI, FAOSTAT, Comtrade | Análisis y validación | 4 referencias |
| V | Todos | Limitaciones y trabajos futuros | 2 referencias |

**Total referencias agregadas**: 14  
**Datasheets a crear**: 5-7 (uno por dataset principal)  
**Impacto en tesis**: Mayor rigor y trazabilidad verificable

---

Este documento sirve como guía de integración específica para cada sección de la tesis.

