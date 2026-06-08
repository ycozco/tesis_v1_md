# Diccionario de Fuentes Canonicas

Fecha de creacion: 2026-06-07  
Ultima actualizacion: 2026-06-07  
Mantenido por: agente de codigo (no modificar manualmente campos marcados AUTO)

Este archivo establece la fuente canonica unica para cada campo del dataset final.
Si una fuente difiere de la canonica, la canonica prevalece segun las reglas de la seccion 7.4 del plan.

---

## 1. Fuente canonica por campo critico

| Campo | Fuente canonica | Archivo canonico | Fuentes alternativas (EXCLUIDAS del pipeline) |
|---|---|---|---|
| `volumen_kg` | SUNAT/ADUANET | `codex-revision/data_processed/sunat/sunat_exportaciones_hs_objetivo_YYYY-MM-DD.csv` | dataset_real_v1.csv (referencia), Trade Map (benchmark) |
| `valor_fob_usd` | SUNAT/ADUANET | Idem arriba | Trade Map (benchmark externo) |
| `precio_kg_usd` | Derivado FOB/kg de SUNAT | Calculado en pipeline | dataset_real_v1.csv precio_kg_usd (validacion) |
| `destino_mercado` | SUNAT/ADUANET | Idem arriba | Trade Map (benchmark) |
| `empresa_exportadora` | SUNAT/ADUANET | Idem arriba | dataset_real_v1.csv (referencia) |
| `fecha` | SUNAT/ADUANET | Idem arriba | dataset_real_v1.csv (referencia) |
| `tipo_cambio_pen_usd` | BCRP serie PN01207PM | `codex-revision/data_raw/bcrp/PN01207PM_2018-01_2026-06.csv` | `data/bcrp/bcrp-tipo-cambio-mensual.csv` (EXCLUIDO), `data/downloads/bcrp_tipo_cambio.csv` (EXCLUIDO) |
| `sisap_precio_prom` | SISAP/MIDAGRI | `codex-revision/data_processed/sisap_midagri/sisap_midagri_mensual_2018_2026_2026-06-07.csv` | Ninguna |
| `sisap_volumen` | SISAP/MIDAGRI | Idem arriba | Ninguna |
| `temperatura_max_c` | NASA POWER | `codex-revision/data_processed/proxies/clima_proxy_YYYY-MM-DD.csv` | SENAMHI (si NASA falla) |
| `temperatura_min_c` | NASA POWER | Idem arriba | SENAMHI (si NASA falla) |
| `precipitacion_mm` | NASA POWER | Idem arriba | SENAMHI (si NASA falla) |
| `carga_portuaria_mes` | APN/OSITRAN | `codex-revision/data_raw/apn_2024/`, `apn_2025/` | Ninguna |
| `alertas_sanitarias_mes` | SENASA datos abiertos | `codex-revision/data_raw/senasa/` | FDA/RASFF (contexto adicional) |

---

## 2. Jerarquia de resolucion de conflictos

### Para volumen y valor FOB de exportacion
```
SUNAT/ADUANET > dataset_real_v1.csv > Trade Map > FAOSTAT
```

### Para precio unitario FOB (USD/kg)
```
Derivado de SUNAT (FOB/kg) > dataset_real_v1.csv > Trade Map valor unitario > SISAP (solo referencia interna)
```

### Para tipo de cambio
```
BCRP serie PN01207PM UNICA VERSION CANONICA
Archivos excluidos del pipeline:
  - data/bcrp/bcrp-tipo-cambio-mensual.csv
  - data/downloads/bcrp_tipo_cambio.csv
```

### Para clima
```
NASA POWER (cobertura completa) > SENAMHI estaciones > valor nulo documentado
```

---

## 3. Segmentacion de productos — fija e inmutable

| Producto | HS | Estado | Decision |
|---|---|---|---|
| Palta | 080440 | NUCLEO | Incluir siempre |
| Uva | 080610 | NUCLEO | Incluir siempre |
| Arandano | 081040 | NUCLEO | Incluir siempre |
| Esparrago | 070920 | CONDICIONAL | Incluir solo si pasa validacion de cobertura |
| Cacao | Varios | EXCLUIDO | No incluir en ningun dataset final ni experimento |

---

## 4. Archivos de datos crudos — SOLO LECTURA

Los siguientes directorios y archivos son de SOLO LECTURA.
El agente NO debe modificar, renombrar ni eliminar ninguno de estos archivos.

```
data/sunat/raw_downloads/          <- ZIPs SUNAT originales
data/sunat/x23290326.DBF           <- DBF SUNAT ya extraido
data-trademap/                     <- XLS Trade Map originales
codex-revision/data_raw/           <- Todos los datos raw de fuentes externas
data/dataset_real_v1.csv           <- Dataset real base (referencia)
data/dataset_agro_sintetico_v1.csv <- Dataset sintetico base
```

---

## 5. Directorios de salida autorizados

```
codex-revision/data_processed/trademap/        <- Trade Map limpio
codex-revision/data_processed/sunat/           <- SUNAT filtrado por HS
codex-revision/data_processed/proxies/         <- BCRP, SISAP, clima, logistica, sanidad
codex-revision/data_processed/eda/             <- Tablas y figuras EDA
codex-revision/data_processed/modeling/        <- Splits temporales
codex-revision/data_processed/rejected/        <- Rechazados por violacion de reglas
codex-revision/logs/                           <- Logs de ejecucion
models/                                        <- Modelos serializados
```

---

## 6. Semillas de aleatoriedad — fijadas antes del primer entrenamiento

```python
RANDOM_SEEDS = [42, 123, 456, 789, 2026]
```
Estas semillas NO deben modificarse una vez iniciado el entrenamiento.

---

## 7. Presupuesto de trials Optuna

```
n_trials = 100  # Por modelo y producto
timeout = 3600  # 1 hora maximo por sesion
```

---

## 8. Registro de decisiones criticas tomadas

| Fecha | Decision | Justificacion |
|---|---|---|
| 2026-06-07 | Tipo de cambio canonico: PN01207PM_2018-01_2026-06.csv | Unica serie BCRP con cobertura completa 2018-2026 |
| 2026-06-07 | Cacao excluido del pipeline | Solo 379 filas, sin fuente canonica |
| 2026-06-07 | Split temporal 70/10/20 | Series agroexportadoras con estacionalidad |
