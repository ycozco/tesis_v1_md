# Informe detallado de datasets

Este informe clasifica los datasets conocidos del proyecto segun su uso metodologico final: entra al pipeline, entra condicionado, contexto, proxy, sintetico auxiliar o exclusion.

## 1. Datasets que entran al nucleo

| Dataset | Ruta | Estado | Uso |
|---|---|---|---|
| Dataset real local | `data/dataset_real_v1.csv` | Disponible | Base inicial auditada. |
| SUNAT/ADUANET | `data/sunat/`, `codex-revision/data_raw/aduanet_bases` | Descargado/parcialmente procesado | Fuente primaria de exportaciones. |
| Trade Map exportaciones | `data-trademap/export_*` | Descargado manualmente | Benchmark externo. |
| BCRP tipo de cambio | `data/bcrp/`, `codex-revision/data_raw/bcrp/` | Disponible | Control macro mensual. |

## 2. Datasets condicionados o contextuales

| Dataset | Ruta | Decision |
|---|---|---|
| SISAP/MIDAGRI | `codex-revision/data_processed/sisap_midagri/` | Usar como mercado interno para palta, uva y esparrago. |
| MIDAGRI compendios | `data/midagri/`, `codex-revision/data_raw/midagri_compendio` | Contexto sectorial y validacion agregada. |
| FAOSTAT | `codex-revision/data_raw/faostat`, `data/faostat` | Benchmark macro internacional. |
| NASA/SENAMHI/NDVI | Varias rutas locales | Proxy climatico. |
| APN/OSITRAN | `codex-revision/data_raw/apn_*`, `ositran_*` | Proxy logistico. |
| SENASA/FDA/RASFF | `codex-revision/data_raw/senasa`, `fda`, `rasff` | Proxy sanitario/contexto. |

## 3. Datasets auxiliares o excluidos

| Dataset | Ruta | Decision |
|---|---|---|
| Dataset sintetico | `data/dataset_agro_sintetico_v1.csv` | Auxiliar para escenarios, balanceo o etiquetas experimentales. |
| Procesados sinteticos | `data/synthetic_processed/` | No usar como evidencia principal. |
| Trade Map importaciones coladas | `data-trademap/import_colado_*` | Excluir del pipeline. |
| Cacao en dataset real | Registros dentro de `data/dataset_real_v1.csv` | Excluir por baja representatividad. |

## 4. Productos y decision

| Producto | Filas locales conocidas | Decision |
|---|---:|---|
| Palta | 17,360 | Nucleo. |
| Uva | 15,701 | Nucleo. |
| Arandano | 4,633 | Nucleo. |
| Esparrago | 2,599 | Secundario condicionado. |
| Cacao | 379 | Excluido. |

## 5. Riesgos metodologicos

- No confundir precio interno SISAP con precio FOB de exportacion.
- No presentar alertas sanitarias agregadas como cumplimiento por embarque.
- No usar variables sinteticas sin etiqueta `sintetica`.
- No editar conclusiones de resultados sin ejecucion final verificable.

---
