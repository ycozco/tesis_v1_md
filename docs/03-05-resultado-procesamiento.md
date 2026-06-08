# Informe tecnico: resultados de procesamiento

Este informe resume el estado actual de procesamiento segun el panorama de datasets reales e integrados.

## 1. Dataset real auditado

Archivo: `data/dataset_real_v1.csv`  
Filas: 40,672  
Columnas: 21

| Producto | Filas | Decision |
|---|---:|---|
| Palta | 17,360 | Nucleo. |
| Uva | 15,701 | Nucleo. |
| Arandano | 4,633 | Nucleo. |
| Esparrago | 2,599 | Secundario condicionado. |
| Cacao | 379 | Excluido. |

## 2. Decision de procesamiento

- El dataset real es la base inicial, pero debe validarse contra SUNAT/ADUANET.
- Las variables climaticas, logisticas y sanitarias deben etiquetarse como reales, proxies o sinteticas segun origen.
- Cacao no debe entrar al dataset modelable final.
- Esparrago solo entra si se crea y valida su segmento.

## 3. Datasets complementarios procesados

| Fuente | Archivo/Ruta | Estado |
|---|---|---|
| SISAP | `codex-revision/data_processed/sisap_midagri/sisap_midagri_mensual_2018_2026_2026-06-07.csv` | Procesado. |
| Trade Map | `data-trademap/export_*` | Pendiente conversion a CSV limpio. |
| BCRP | `codex-revision/data_raw/bcrp/PN01207PM_2018-01_2026-06.csv` | Disponible. |
| SUNAT/ADUANET | `data/sunat/`, `codex-revision/data_raw/aduanet_bases` | Pendiente normalizacion final. |

## 4. Resultados numericos

Los resultados de entrenamiento basados exclusivamente en dataset sintetico o corridas anteriores deben reportarse como preliminares hasta ejecutar el pipeline final sobre el dataset agroexportador integrado.

---
