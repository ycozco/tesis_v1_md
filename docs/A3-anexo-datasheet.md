## Anexo C — Datasheet del Dataset Sintético Agroexportador

> **Estándar aplicado**: Gebru et al. (2021) — Datasheets for Datasets (Gebru et al., 2021).
> **Versión del dataset**: v1.0
> **Fecha de creación prevista**: 2026-06-01 (Hito 2 del plan general)
> **Estado actual**: 📐 Especificación completa lista para generación.

---

### C.1 Motivación

**¿Para qué se creó el dataset?**
Para entrenar y evaluar de forma reproducible el sistema integrado de supervisión operativa con IA explicable propuesto en esta tesis, sin depender de datos privados de empresas agroexportadoras. La opción sintética permite (a) controlar la distribución de anomalías, (b) garantizar reproducibilidad mediante semilla fija, y (c) publicar el dataset junto al paper.

**¿Quién lo creó?**
Yoset Cozco Mauri, Escuela Profesional de Ingeniería de Sistemas, Universidad Nacional de San Agustín de Arequipa (UNSA). Bajo asesoría del Dr. Víctor Manuel Cornejo Aparicio.

**¿Quién financió la creación?**
Sin financiamiento externo. Desarrollo en el marco de una tesis de pregrado.

---

### C.2 Composición

**¿Qué instancias representa?**
Cada fila representa un evento operativo agroexportador diario por combinación de producto, zona y destino. Una instancia agrupa indicadores de producción, comercialización, clima, sanidad, logística y calidad para un día específico.

**¿Cuántas instancias?**
Mínimo 2,000 — Recomendado 5,000 — Tope 10,000. La versión inicial v1.0 generará 2,000 instancias.

**¿Es muestra o universo?**
Es una muestra sintética generada para cubrir las distribuciones plausibles del sector durante el período 2022-01-01 a 2025-12-31.

**¿Qué datos contiene cada instancia?**

| Variable | Tipo | Descripción | Rango plausible | Fuente para rangos | Distribución |
|---|---|---|---|---|---|
| `id` | int | Identificador único | 1..N | — | Secuencial |
| `fecha` | datetime | Día del evento | 2022-01-01 a 2025-12-31 | — | Uniforme |
| `producto` | category | Producto agroexportador | {arándano, uva, palta, cacao, espárrago} | MIDAGRI | Ponderada por participación |
| `zona` | category | Departamento productor | {Ica, La Libertad, Piura, Arequipa, Lima} | MIDAGRI | Ponderada por área cultivada |
| `volumen_kg` | float | Volumen del día (kg) | 500–50,000 | MIDAGRI | LogNormal(μ=8, σ=1.2) |
| `precio_kg_usd` | float | Precio FOB por kg | 0.5–12.0 | MIDAGRI / SUNAT | Normal por producto |
| `temperatura_max_c` | float | Temperatura máxima del día (°C) | 15–38 | SENAMHI | Normal por zona/mes |
| `temperatura_min_c` | float | Temperatura mínima del día (°C) | 5–22 | SENAMHI | Normal por zona/mes |
| `precipitacion_mm` | float | Precipitación diaria (mm) | 0–200 | SENAMHI | Gamma(α=0.5, β=10) |
| `humedad_pct` | float | Humedad relativa (%) | 40–95 | SENAMHI | Beta(α=8, β=3) |
| `destino_mercado` | category | Mercado destino | {EEUU, UE, Asia, Otro} | SUNAT | Ponderada por exportaciones |
| `cumplimiento_fitosanitario` | binary | Lote cumple SENASA | {0, 1} | SENASA | Bernoulli(p=0.92) |
| `dias_logisticos` | int | Días desde cosecha a embarque | 3–45 | Estimado | LogNormal(μ=2.3, σ=0.5) |
| `merma_pct` | float | Pérdida del lote (%) | 0–30 | Estimado | Beta(α=2, β=10) |
| `costo_logistico_usd_kg` | float | Costo logístico unitario | 0.05–1.2 | Estimado | LogNormal |
| `tipo_cambio_pen_usd` | float | Tipo de cambio del día | 3.5–4.2 | BCRP | Random walk con tendencia |
| `etiqueta_anomalia` | binary | Es anomalía operativa | {0, 1} | Inyección controlada | Bernoulli(p=0.12) |
| `tipo_anomalia` | category | Tipo de anomalía | {precio, volumen, clima, logistica, calidad, none} | Inyección controlada | Definida por reglas |

**Total**: 17 columnas; 2,000 filas en v1.0.

**¿Las etiquetas son confiables?**
Sí, porque el dataset es sintético y las etiquetas se asignan según las reglas de inyección documentadas (§C.4). No hay ambigüedad por error humano de etiquetado.

**¿Falta algún dato?**
Sí, se inyectan valores faltantes en el 3% de las filas para simular registros parciales (campos: humedad_pct, dias_logisticos, costo_logistico_usd_kg). Esto evalúa robustez del modelo ante datos incompletos típicos de fuentes operativas.

**¿Las relaciones entre instancias son explícitas?**
Las instancias están temporalmente ordenadas. No hay relación de identidad (no es panel longitudinal con seguimiento individual). Una misma combinación (producto, zona, fecha) puede aparecer solo una vez.

**¿División train/test recomendada?**
División cronológica:
- Train: 2022-01-01 a 2024-12-31 (70%)
- Validation: 2025-01-01 a 2025-04-30 (10%)
- Test: 2025-05-01 a 2025-12-31 (20%)

Esta división evita data leakage temporal y simula el caso realista de aplicar el modelo a períodos futuros.

**¿Hay datos sensibles?**
No. No hay datos personales, no se identifican empresas reales, no se referencian transacciones específicas. Es completamente sintético.

---

### C.3 Proceso de recolección

**¿Cómo se generaron los datos?**
Mediante un script Python (`src/generate_synthetic_dataset.py`) que muestrea cada columna según las distribuciones de la tabla §C.2 condicionadas a (producto, zona, mes). La generación se realiza en cuatro pasos:
1. Muestreo de variables base (fecha, producto, zona).
2. Muestreo condicional de variables dependientes (clima por zona+mes; precio por producto+mes).
3. Inyección de correlaciones plausibles (volumen ↑ → merma ↓ por economías de escala; precipitacion ↑ → merma ↑ por daño post-cosecha).
4. Inyección controlada de anomalías según reglas §C.4.

**¿Quién recopiló los datos?**
N/A — Datos sintéticos generados por el autor con `numpy.random.default_rng(seed=42)`.

**¿En qué período se generaron?**
Generación prevista: 2026-05-31 a 2026-06-01.

---

### C.4 Inyección de anomalías

**Distribución de tipos de anomalía** (sobre 12% de filas marcadas como anómalas):

| Tipo | Proporción | Mecanismo de inyección | Variables afectadas |
|---|---|---|---|
| `precio` | 30% | `precio_kg_usd` > percentil 99 o < percentil 1 del producto | precio_kg_usd |
| `volumen` | 25% | `volumen_kg` > media + 3·DE para producto/zona | volumen_kg |
| `clima` | 20% | `temperatura_max_c` > 38°C ∧ `precipitacion_mm` < 1 mm (sequía con calor extremo) | temperatura_max_c, precipitacion_mm |
| `logistica` | 15% | `dias_logisticos` > percentil 95 ∧ `cumplimiento_fitosanitario` = 1 (demora a pesar de cumplir) | dias_logisticos |
| `calidad` | 10% | `merma_pct` > 25% ∧ `precio_kg_usd` > mediana (pérdida con precio alto) | merma_pct |

**Verificabilidad**: Para cada anomalía inyectada se registra `tipo_anomalia` y el campo `regla_inyeccion` que documenta los valores exactos que activaron la regla. Esto permite auditoría posterior del proceso de generación.

---

### C.5 Preprocesamiento, limpieza y etiquetado

**¿Se aplicó preprocesamiento?**
El dataset v1.0 se publica sin preprocesamiento adicional. El script de pipeline (`src/pipeline.py`) aplica:
1. Imputación de valores faltantes (mediana para numéricas, moda para categóricas).
2. Codificación one-hot de variables categóricas.
3. Escalamiento StandardScaler para variables numéricas (solo para LOF; XGBoost no lo requiere).
4. Construcción de features derivadas: `temperatura_rango = temperatura_max_c - temperatura_min_c`, `precio_unitario_zscore` por producto.

**¿Los datos crudos se conservan?**
Sí. El CSV crudo (`data/dataset_agro_sintetico_v1.csv`) se versiona en Git LFS y queda como referencia de entrada al pipeline.

---

### C.6 Usos previstos y no previstos

**¿Para qué se usará el dataset?**
- Entrenar y evaluar el sistema integrado de supervisión operativa de esta tesis.
- Comparar baselines (Isolation Forest individual, ensembles parciales).
- Publicar como benchmark abierto en el repositorio GitHub asociado al paper.

**¿Para qué NO debe usarse?**
- No representa datos reales de empresas específicas; no debe usarse para toma de decisiones operativas en ninguna empresa real.
- No se diseñó para análisis económico del sector agroexportador peruano (los rangos son plausibles pero no son estadísticas oficiales).
- No es un benchmark estandarizado de la comunidad de detección de anomalías.

**¿Existen tareas para las que el dataset sería inadecuado?**
- Análisis causal: no hay manipulación experimental real, solo inyección de correlaciones plausibles.
- Modelos de pronóstico de mercado: el componente de precio no refleja la volatilidad real de los mercados internacionales.
- Sesgo geográfico/demográfico: solo se modelan 5 productos y 5 departamentos peruanos.

---

### C.7 Distribución y licencia

**¿El dataset se distribuirá?**
Sí, publicación bajo licencia **CC BY 4.0** en el repositorio GitHub asociado a esta tesis. Esto permite uso académico y comercial citando la fuente.

**¿Cómo se citará?**
```
Cozco Mauri, Y. (2026). Dataset Sintético Agroexportador Peruano v1.0 [Data set].
  Universidad Nacional de San Agustín de Arequipa.
  URL: [repositorio GitHub al publicar]
```

**¿Habrá DOI?**
Se solicitará DOI en Zenodo al cierre de la tesis para garantizar persistencia.

---

### C.8 Mantenimiento

**¿Quién mantendrá el dataset?**
Yoset Cozco Mauri hasta diciembre 2027. Después, el repositorio queda como archivo histórico.

**¿Habrá actualizaciones?**
- v1.0 — 2,000 filas — versión base de la tesis.
- v1.1 — posible si se requieren ajustes durante experimentos.
- v2.0 — versión extendida (5,000 filas) para publicación en paper.

**¿Cómo se notificarán los cambios?**
Mediante CHANGELOG.md en el repositorio y release notes versionadas por Git.

---

### C.9 Consideraciones éticas

**¿Hay riesgo de daño a personas o grupos?**
No, dado que el dataset es sintético y no contiene información de individuos ni empresas reales. La elección de 5 productos y 5 departamentos cubre los principales del sector peruano pero no excluye intencionalmente a otros actores.

**¿Hay riesgo de uso indebido?**
Riesgo bajo. El dataset es claramente etiquetado como sintético en cada archivo (header, README, paper). Cualquier uso operativo real sería contrario a la documentación.

---

### C.10 Documentación complementaria — Fuentes públicas utilizadas

El dataset se calibra con rangos plausibles tomados de las siguientes fuentes públicas. Para reproducir o ampliar el dataset, consultar:

| Fuente | URL | Variable calibrada | Acceso |
|---|---|---|---|
| MIDAGRI | https://www.gob.pe/midagri | volumen, precio, producto, zona | Público |
| SENAMHI | https://www.senamhi.gob.pe | temperatura, precipitación, humedad | Público |
| SENASA | https://www.gob.pe/senasa | cumplimiento_fitosanitario | Público |
| SUNAT | https://www.sunat.gob.pe | destino_mercado, valor exportado | Público |
| INEI | https://www.inei.gob.pe | tipo_cambio, indicadores económicos | Público |
| FAOSTAT | https://www.fao.org/faostat | producción nacional comparativa | Público |
| UN Comtrade | https://comtradeplus.un.org | exportaciones por país destino | Público |

---

### C.11 Benchmark complementario

El **BAF Benchmark** (Jesus et al., 2022) se utiliza únicamente como referencia metodológica para validación cruzada de la arquitectura en datos tabulares desbalanceados con drift temporal, NO como evidencia del dominio agroexportador. Se documenta su uso en §3.2 con esa restricción.

---

*Anexo C — versión 1.0 — 2026-05-17. Datasheet completo, listo para generación de v1.0 del dataset.*
