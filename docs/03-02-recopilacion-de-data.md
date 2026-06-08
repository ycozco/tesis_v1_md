# Informe tecnico: recopilacion de datos e ingesta multisource

Este informe documenta la Capa 0 de datos para la tesis. La recopilacion ya no se plantea como una simple generacion de datos sinteticos, sino como un proceso de construccion de un **dataset agroexportador integrado**.

## 1. Relacion metodologica con la tesis

El sistema propuesto requiere datos para cuatro funciones: prediccion, deteccion de anomalias, explicabilidad SHAP y reportes RAG. Por tanto, cada fuente debe indicar que variable aporta, con que granularidad y que limitacion tiene.

| Variable | Tipo en tesis | Fuente preferida | Etiqueta metodologica |
|---|---|---|---|
| `volumen_kg` | Explicativa/objetivo de prediccion | SUNAT/ADUANET | real_observada |
| `valor_fob_usd` | Explicativa comercial | SUNAT/ADUANET | real_observada |
| `precio_kg_usd` | Derivada comercial | FOB/kg o dataset real | derivada |
| `destino_mercado` | Contexto comercial | SUNAT/Trade Map | real_observada |
| `sisap_precio_prom` | Contexto interno | SISAP/MIDAGRI | real_agregada |
| `tipo_cambio_pen_usd` | Control macro | BCRP | real_agregada |
| `temperatura_max_c` | Exogena | NASA/SENAMHI | proxy |
| `carga_portuaria_mes` | Logistica | APN/OSITRAN | proxy |
| `alertas_sanitarias_mes` | Sanidad | SENASA/FDA/RASFF | proxy |
| `etiqueta_anomalia` | Objetivo experimental | reglas/modelo/dataset | derivada o sintetica |

## 2. Productos de estudio

| Producto | HS | Estado |
|---|---|---|
| Palta | `080440` | Nucleo. |
| Uva | `080610` | Nucleo. |
| Arandano | `081040` | Nucleo. |
| Esparrago | `070920` | Secundario condicionado. |
| Cacao | No aplica al nucleo final | Excluido por baja representatividad. |

Aunque cacao fue detectado en exploraciones previas, no debe presentarse como producto de evaluacion principal.

## 3. Fuentes integradas

| Fuente | Ruta local | Uso |
|---|---|---|
| SUNAT/ADUANET | `data/sunat/`, `codex-revision/data_raw/aduanet_bases` | Fuente primaria de exportaciones. |
| Dataset real local | `data/dataset_real_v1.csv` | Base auditada inicial de 40,672 filas. |
| Trade Map | `data-trademap/export_*` | Benchmark internacional por producto/destino. |
| SISAP/MIDAGRI | `codex-revision/data_processed/sisap_midagri/` | Mercado interno para palta, uva y esparrago. |
| BCRP | `data/bcrp/`, `codex-revision/data_raw/bcrp/` | Tipo de cambio mensual. |
| NASA/SENAMHI/NDVI | `codex-revision/data_raw/nasa_power`, `codex-revision/data_raw/senamhi`, `data/vegetation/` | Clima proxy. |
| APN/OSITRAN | `codex-revision/data_raw/apn_*`, `codex-revision/data_raw/ositran_*` | Logistica portuaria proxy. |
| SENASA/FDA/RASFF | `codex-revision/data_raw/senasa`, `fda`, `rasff` | Riesgo sanitario contextual. |
| MIDAGRI/FAOSTAT/World Bank | `data/midagri/`, `codex-revision/data_raw/faostat`, `world_bank` | Contexto sectorial. |

## 4. Evidencia local relevante

- `codex-revision/informe-final-data.md`: inventario y relacion con tesis.
- `codex-revision/10-descarga-masiva-sisap-midagri.md`: descarga SISAP.
- `data-trademap/README_renombrado.md`: clasificacion de archivos Trade Map.
- `plan-implementacion-datasets-tesis.md`: plan rector de integracion.

## 5. Decision metodologica

La recopilacion se considera suficiente para avanzar si:

- SUNAT/ADUANET queda normalizado para HS objetivo.
- Trade Map se convierte a CSV limpio.
- SISAP se usa solo como contexto interno.
- BCRP se integra como control mensual.
- Clima, logistica y sanidad se integran como proxies documentados.
- Sinteticos se mantienen separados y marcados.

---
