# Reporte consolidado completo - Codex Revision

Fecha: 2026-06-07  
Proyecto: `d:\tesis_yoset`  
Tema: supervisión de implementación, búsqueda de datasets y trazabilidad metodológica.

## Resumen ejecutivo

La tesis cuenta con una implementación avanzada: scraper SUNAT/Aduanet, ETL de DBF, integración BCRP, datasets reales y sintéticos, preprocesamiento, modelos de anomalías, SHAP, reportes y compilación DOCX/PDF. El punto crítico no es la ausencia de implementación, sino la necesidad de alinear el pipeline con el alcance metodológico actualizado.

La decisión recomendada es:

```text
Núcleo modelable: palta, uva y arándano.
Producto secundario: espárrago, si pasa auditoría.
Producto excluido: cacao, por baja representatividad muestral.
```

## Evidencia cuantitativa local

`data/dataset_real_v1.csv` contiene 40,672 registros y 21 columnas, con fechas desde 2018-06-15 hasta 2026-05-27.

Distribución:

| Producto | Registros | Decisión |
|---|---:|---|
| palta | 17,360 | Principal |
| uva | 15,701 | Principal |
| arándano | 4,633 | Principal |
| espárrago | 2,599 | Secundario |
| cacao | 379 | Excluir |

`data/dataset_agro_sintetico_v1.csv` contiene 2,689 registros y todavía incluye cacao con 554 registros, lo que produce una discrepancia metodológica: cacao tiene baja representación real, pero alta representación sintética.

## Estado de integridad

Se ejecutó:

```powershell
& 'd:\tesis_yoset\.venv\Scripts\python.exe' src\verify_integrity.py
```

Resultado:

| Dataset | Estado | Nulos | Duplicados |
|---|---|---:|---:|
| Sintético v1 | Aprobado | 2,472 | 0 |
| Real v1 | Aprobado con advertencia | 42,847 | 4,684 |

Interpretación: la estructura y plausibilidad pasan, pero el dataset real requiere deduplicación documentada y separación más clara de variables reales, proxy y sintéticas.

## Hallazgos técnicos principales

1. Cacao sigue presente en scripts y datasets.
2. Espárrago existe en el maestro, pero no tiene segmento `real_processed`.
3. Variables privadas no públicas aparecen en el dataset real como si fueran columnas operativas observadas.
4. El script `build_real_dataset.py` tiene nombre ambiguo porque genera un dataset sintético/calibrado.
5. La verificación formal requiere usar el Python del `.venv`, no el lanzador `py` genérico.

## Fuentes externas verificadas

Fuentes base para sostener la tesis:

| Bloque | Fuente principal |
|---|---|
| Microdato de exportación | SUNAT/Aduanet |
| Tipo de cambio | BCRP API PN01207PM |
| Contexto comercial | PROMPERÚ Exportemos |
| Comercio agrario agregado | MIDAGRI |
| Precios internos | MIDAGRI SISAP |
| Clima observado | SENAMHI |
| Clima proxy | NASA POWER |
| Vegetación | MODIS MOD13Q1 |
| Logística portuaria | APN/OSITRAN |
| Fitosanidad normativa | SENASA |
| Validación externa sanitaria | FDA Import Refusals / RASFF |
| Benchmark internacional | FAOSTAT / UN Comtrade / ITC Trade Map |

El detalle completo está en `03-fuentes-web-y-datasets.md`.

## Clasificación metodológica obligatoria

| Grupo | Variables |
|---|---|
| Real observado | fecha, partida, producto, FOB/peso/precio, destino, aduana, tipo de cambio. |
| Proxy real | zona por aduana, presión portuaria, clima regional, NDVI/EVI. |
| Validación externa | rechazos FDA, alertas RASFF, requisitos SENASA. |
| Sintético calibrado | merma, calidad lote, temperatura contenedor, costo logístico, cumplimiento fitosanitario por embarque, etiqueta de anomalía. |

## Acciones prioritarias

1. Crear dataset real sin cacao:

```text
data/real/dataset_real_v1_1_no_cacao.csv
```

2. Crear segmento espárrago o excluirlo operacionalmente:

```text
data/real_processed/esparrago/dataset_esparrago_raw.csv
```

3. Deduplicar dataset real y documentar criterio:

```text
reports/data_audit/deduplication_report.md
```

4. Regenerar dataset sintético sin cacao:

```text
data/synthetic/synthetic_agroexport_v2_calibrated_no_cacao.csv
```

5. Actualizar Capítulo III y Anexo Datasheet con matriz real/proxy/sintético.

6. Regenerar Capítulo IV y métricas sin cacao.

## Documentos de esta revisión

- `00-indice.md`: índice del paquete.
- `01-auditoria-implementacion.md`: auditoría de implementación.
- `02-inventario-datasets.md`: inventario y conteos locales.
- `03-fuentes-web-y-datasets.md`: consolidado de fuentes externas.
- `04-plan-supervision-scraping-etl.md`: plan operativo.
- `05-riesgos-correcciones-prioritarias.md`: riesgos y checklist.

## Conclusión

El proyecto es recuperable y defendible con una corrección clara: no vender todo como dato real y no entrenar cacao. La tesis debe presentarse como un sistema híbrido de supervisión agroexportadora basado en microdatos reales SUNAT, enriquecimiento externo oficial/proxy y datos sintéticos calibrados para dimensiones privadas no disponibles públicamente.

