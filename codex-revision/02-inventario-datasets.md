# Inventario de datasets locales

## Resumen de archivos de datos

Conteo por extensión dentro de `data/`:

| Extensión | Cantidad |
|---|---:|
| `.zip` | 50 |
| `.xlsx` | 32 |
| `.csv` | 28 |
| `.pdf` | 6 |
| `.xls` | 4 |
| `.json` | 4 |
| `.png` | 1 |
| `.DBF` | 1 |
| `.txt` | 1 |
| `.html` | 1 |

## Datasets principales auditados

| Archivo | Filas | Columnas | Observación |
|---|---:|---:|---|
| `data/dataset_real_v1.csv` | 40,672 | 21 | Dataset consolidado con microdato SUNAT y variables enriquecidas/simuladas. |
| `data/dataset_agro_sintetico_v1.csv` | 2,689 | 21 | Dataset sintético/calibrado v1; incluye cacao. |
| `data/real_processed/palta/dataset_palta_raw.csv` | 17,360 | 21 | Segmento real de palta. |
| `data/real_processed/uva/dataset_uva_raw.csv` | 15,701 | 21 | Segmento real de uva. |
| `data/real_processed/arandano/dataset_arandano_raw.csv` | 4,633 | 21 | Segmento real de arándano. |
| `data/real_processed/esparrago/dataset_esparrago_raw.csv` | No existe | - | Debe generarse si espárrago queda en alcance. |
| `data/bcrp/bcrp-tipo-cambio-mensual.csv` | 26 | 12 | Series mensuales BCRP; contiene PN01207PM. |
| `data/faostat/faostat-produccion-peru-2024.csv` | 97 | 15 | Producción FAOSTAT local descargada. |
| `data/global_benchmarks/world_bank_pink_sheet.csv` | 4 | 4 | Archivo mínimo/fallback de commodities. |

## Distribución de productos en `data/dataset_real_v1.csv`

| Producto | Registros | Decisión recomendada |
|---|---:|---|
| palta | 17,360 | Mantener como producto principal. |
| uva | 15,701 | Mantener como producto principal. |
| arándano | 4,633 | Mantener como producto principal. |
| espárrago | 2,599 | Mantener como secundario si pasa auditoría. |
| cacao | 379 | Excluir del modelamiento experimental. |

Rango de fechas del dataset real: 2018-06-15 a 2026-05-27.

## Distribución de productos en `data/dataset_agro_sintetico_v1.csv`

| Producto | Registros |
|---|---:|
| palta | 526 |
| uva | 552 |
| arándano | 517 |
| espárrago | 540 |
| cacao | 554 |

Rango de fechas del dataset sintético: 2024-01-01 a 2026-12-28.

Observación: el dataset sintético tiene fechas futuras respecto a 2026-06-07. Si se usa como escenario prospectivo/simulado, debe indicarse explícitamente. Si se usa para evaluación histórica, debe recortarse.

## Segmentos reales existentes

### Palta

- Archivo: `data/real_processed/palta/dataset_palta_raw.csv`
- Filas: 17,360
- Rango de fechas: 2018-06-15 a 2026-05-27

### Uva

- Archivo: `data/real_processed/uva/dataset_uva_raw.csv`
- Filas: 15,701
- Rango de fechas: 2021-01-07 a 2026-05-24

### Arándano

- Archivo: `data/real_processed/arandano/dataset_arandano_raw.csv`
- Filas: 4,633
- Rango de fechas: 2022-08-19 a 2026-05-23

### Espárrago

- Registros existen en el maestro: 2,599.
- Segmento crudo no encontrado.
- Acción requerida: modificar `src/segment_datasets.py` para incluir `"esparrago"` o justificar su exclusión operativa.

## ZIP SUNAT/Aduanet

Se encontraron 50 archivos `.zip` bajo `data/sunat/` y `data/sunat/raw_downloads/`. Tipos observados:

- `x*.zip`: exportaciones definitivas, contiene DBF `x*.DBF`.
- `ma*.zip`, `mam*.zip`, `mb*.zip`: otros regímenes/bases descargadas.
- `idv*.zip`: archivos muy pequeños con DBF, probablemente informes/verificación o base auxiliar.

Ejemplos:

| Archivo | Tamaño | Contenido |
|---|---:|---|
| `data/sunat/raw_downloads/x23290326.zip` | 2,035,604 bytes | `x23290326.DBF` |
| `data/sunat/raw_downloads/x30050426.zip` | 1,525,565 bytes | `x30050426.DBF` |
| `data/sunat/raw_downloads/ma25310526.zip` | 19,149,284 bytes | `ma25310526.DBF` |
| `data/sunat/raw_downloads/mam18240526.zip` | 38,480,718 bytes | `mam18240526.DBF` |

## Columnas del dataset real

`data/dataset_real_v1.csv` contiene:

```text
id, fecha, producto, partida_arancelaria, empresa_exportadora, zona,
volumen_kg, precio_kg_usd, destino_mercado, dias_logisticos,
costo_logistico_usd_kg, cumplimiento_fitosanitario, merma_pct,
tipo_cambio_pen_usd, temperatura_max_c, temperatura_min_c,
precipitacion_mm, humedad_pct, etiqueta_anomalia, tipo_anomalia,
regla_inyeccion
```

Clasificación metodológica recomendada:

| Variable | Tipo recomendado |
|---|---|
| `fecha` | Real observado si proviene de SUNAT. |
| `producto` | Real observado derivado de partida. |
| `partida_arancelaria` | Real observado. |
| `empresa_exportadora` | Real observado si proviene de DBF; verificar anonimización si aplica. |
| `volumen_kg` | Real observado. |
| `precio_kg_usd` | Real observado/calculado desde FOB y peso. |
| `destino_mercado` | Real observado o agrupación derivada. |
| `tipo_cambio_pen_usd` | Real observado BCRP. |
| `zona` | Proxy derivado de aduana/CADU, no finca real. |
| `temperatura_*`, `precipitacion_mm`, `humedad_pct` | Proxy climático/simulado si no proviene de SENAMHI/NASA por fecha y coordenada. |
| `dias_logisticos` | Proxy/sintético si no existe fecha logística pública confiable. |
| `costo_logistico_usd_kg` | Sintético/calibrado. |
| `cumplimiento_fitosanitario` | Sintético/calibrado salvo prueba pública SENASA por DUA. |
| `merma_pct` | Sintético/calibrado. |
| `etiqueta_anomalia`, `tipo_anomalia`, `regla_inyeccion` | Etiqueta experimental/sintética o regla heurística, no etiqueta oficial. |

## Auditoría de integridad ejecutada

Comando funcional:

```powershell
& 'd:\tesis_yoset\.venv\Scripts\python.exe' src\verify_integrity.py
```

Resultado consolidado:

| Dataset | Estado | Nulos iniciales | Duplicados |
|---|---|---:|---:|
| `dataset_agro_sintetico_v1.csv` | Aprobado | 2,472 | 0 |
| `dataset_real_v1.csv` | Aprobado con advertencia | 42,847 | 4,684 |

Acción recomendada: crear `data/real/dataset_real_v1_1_no_cacao.csv` sin cacao, con deduplicación documentada y reporte de calidad por producto.

