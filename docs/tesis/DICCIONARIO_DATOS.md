# Diccionario de Datos

Este documento describe el diccionario de datos del sistema integrado de supervisión, detallando los campos contenidos en el dataset analítico agregados por `producto × mercado de destino × semana ISO` (`weekly_product_market.parquet`, `prediction_features.parquet` y `anomaly_features.parquet`).

---

## 1. Identificación y Llaves Primarias

| Campo | Tipo | Origen | Descripción |
| :--- | :--- | :--- | :--- |
| `product_code` | Categorical (String) | SUNAT / ADUANET | Código arancelario del cultivo a 10 dígitos. Valores permitidos: `0804400000` (palta), `0806100000` (uva fresca), `0810400000` (arándano). |
| `market_aggregated` | Categorical (String) | SUNAT / ADUANET | Código ISO alfa-3 del país de destino de la exportación (ej. `USA`, `NLD`, `CHN`) o la categoría general `OTHER` para mercados fuera del top-10 de volumen acumulado. |
| `week_start` | DateTime | Derivado de fecha | Fecha correspondiente al lunes de inicio de la semana ISO evaluada (formato `YYYY-MM-DD`). |

---

## 2. Variables de Flujo Comercial (SUNAT)

| Campo | Tipo | Unidad | Descripción |
| :--- | :--- | :--- | :--- |
| `total_fob_usd` | Float | USD | Valor total FOB (Free On Board) declarado acumulado en la semana para la combinación producto-mercado. |
| `total_net_weight_kg` | Float | Kilogramos (kg) | Peso neto total acumulado exportado en la semana. |
| `total_gross_weight_kg`| Float | Kilogramos (kg) | Peso bruto total acumulado en la semana (incluye embalajes y paletas). |
| `shipment_count` | Integer | Unidades | Cantidad total de despachos (declaraciones de exportación individuales) en la semana. |
| `exporter_count` | Integer | Unidades | Cantidad de empresas exportadoras únicas (RUCs anonimizados) con actividad en la semana. |
| `avg_shipment_weight_kg`| Float | Kilogramos (kg) | Peso neto promedio por despacho en la semana. |
| `median_shipment_weight_kg`| Float| Kilogramos (kg)| Mediana del peso neto por despacho en la semana. |
| `fob_unit_value_usd_kg`| Float | USD/kg | Valor unitario FOB de la semana. Calculado como `total_fob_usd / total_net_weight_kg`. Nulo si el peso neto es 0. |
| `destination_volume_share`| Float| Porcentaje (0.0-1.0)| Participación del volumen enviado a este mercado sobre el volumen nacional de ese producto en la semana. |
| `destination_fob_share` | Float | Porcentaje (0.0-1.0)| Participación del valor FOB enviado a este mercado sobre el FOB total de ese producto en la semana. |
| `weeks_since_last_export`| Integer| Semanas | Contador secuencial de semanas transcurridas desde la última exportación de este producto a este mercado. |
| `has_exports` | Boolean | Binario | Indicador de si se registraron exportaciones de la combinación en la semana (`true` o `false`). |

---

## 3. Variables de Variables Exógenas y Proxies

| Campo | Tipo | Unidad | Origen | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `tipo_cambio_pen_usd` | Float | PEN por USD | BCRP | Tipo de cambio promedio interbancario de venta de la semana. |
| `temperatura_max_c` | Float | Grados Celsius | NASA POWER | Temperatura máxima promedio semanal registrada en la zona agroproductora correspondiente. |
| `temperatura_min_c` | Float | Grados Celsius | NASA POWER | Temperatura mínima promedio semanal registrada en la zona agroproductora correspondiente. |
| `precipitacion_mm` | Float | Milímetros (mm) | NASA POWER | Lluvia acumulada semanal registrada en la zona agroproductora. |
| `humedad_pct` | Float | Porcentaje (0-100)| NASA POWER | Humedad relativa promedio semanal de la zona agroproductora. |
| `dias_logisticos` | Float | Días | OSITRAN / APN | Tiempo promedio estimado de tránsito y despacho de aduanas en la semana. (Proxy estimado). |
| `costo_logistico_usd_kg`| Float | USD/kg | OSITRAN | Costo logístico unitario estimado de exportación por contenedor. (Proxy estimado). |
| `cumplimiento_fitosanitario`| Float| Índice (0.0-1.0)| SENASA / FDA | Índice de cumplimiento fitosanitario y ausencia de alertas sanitarias en mercados de destino. (Proxy estimado). |
| `merma_pct` | Float | Porcentaje (0-100)| MIDAGRI | Porcentaje estimado de mermas físicas de transporte. (Proxy estimado). |

---

## 4. Características Temporales y Rezagos (Lags)

*Nota: Todas las variables climáticas, macroeconómicas y proxies se incorporan con el sufijo `_lag1` (desplazadas 1 semana) para prevenir fugas de información. A continuación se listan las principales variables derivadas generadas en `prediction_features.parquet`:*

| Campo | Tipo | Unidad | Fórmula o Ventana |
| :--- | :--- | :--- | :--- |
| `price_lag_k` | Float | USD/kg | `fob_unit_value_usd_kg` desplazado $k$ semanas (donde $k \in \{1, 2, 4, 8, 13, 26, 52\}$). |
| `volume_lag_k` | Float | Kilogramos | `total_net_weight_kg` desplazado $k$ semanas (donde $k \in \{1, 2, 4, 8, 13, 26, 52\}$). |
| `fob_lag_k` | Float | USD | `total_fob_usd` desplazado $k$ semanas ($k \in \{1, 4, 13, 52\}$). |
| `shipment_count_lag_k` | Integer | Unidades | `shipment_count` desplazado $k$ semanas ($k \in \{1, 4, 13\}$). |
| `price_rolling_mean_w` | Float | USD/kg | Media móvil de `fob_unit_value_usd_kg` (con forward fill hasta 4 semanas) en ventana de $w$ semanas ($w \in \{4, 8, 13, 26, 52\}$). |
| `price_rolling_std_w` | Float | USD/kg | Desviación estándar móvil de precio en ventana de $w$ semanas ($w \in \{4, 8, 13, 26, 52\}$). |
| `price_rolling_mad_w` | Float | USD/kg | Desviación absoluta de la mediana (MAD) móvil de precio en ventana de $w$ semanas. |
| `volume_rolling_mean_w` | Float | Kilogramos | Media móvil de volumen exportado en ventana de $w$ semanas ($w \in \{4, 8, 13, 26, 52\}$). |
| `price_pct_change_k` | Float | Variación | Cambio porcentual de precio frente a lag $k$ (ej. $k=1, 4, 52$). Formula: `(lag1 - lagk) / lagk`. |
| `volume_pct_change_k` | Float | Variación | Cambio porcentual de volumen frente a lag $k$ (ej. $k=1, 4, 52$). |
| `log_price_difference_1`| Float| Variación | Diferencia logarítmica de precio: `log(lag1 + eps) - log(lag2 + eps)`. |
| `week_sin` / `week_cos` | Float | Cíclica | Codificación de semana del año mediante $\sin$ y $\cos$ para capturar estacionalidad regular de 52 semanas. |
| `month_sin` / `month_cos`| Float| Cíclica | Codificación del mes del año mediante $\sin$ y $\cos$. |

---

## 5. Variables de Predicción y Residuos (Anomaly Features)

Contenidas en `anomaly_features.parquet` y consumidas por el detector de anomalías:

| Campo | Tipo | Unidad | Descripción |
| :--- | :--- | :--- | :--- |
| `pred_fob_unit_value_usd_kg` | Float | USD/kg | Predicción puntual del valor unitario FOB esperado para la semana $t+1$, obtenida por el modelo global de regresión (XGBoost/LightGBM). |
| `pred_export_volume_kg` | Float | Kilogramos | Predicción puntual del volumen exportado esperado en $t+1$, obtenida por el modelo global. |
| `price_residual` | Float | USD/kg | Residuo simple de precio de la semana. Calculado como: `fob_unit_value_usd_kg - pred_fob_unit_value_usd_kg`. |
| `price_residual_robust_z` | Float | Z-Score | Residuo de precio escalado robustamente según la mediana y MAD de los residuos de las últimas 13 semanas para la serie temporal. |
| `volume_residual` | Float | Kilogramos | Residuo simple de volumen. Calculado como: `total_net_weight_kg - pred_export_volume_kg`. |
| `volume_residual_robust_z` | Float | Z-Score | Residuo de volumen escalado robustamente según la mediana y MAD de los residuos de las últimas 13 semanas. |
| `is_synthetic` | Boolean | Binario | Bandera indicadora de si la fila ha sido modificada por inyección sintética controlada de anomalías en el entorno de pruebas (`true` o `false`). |
| `synthetic_scenario` | String | Categoría | Tipo de anomalía simulada inyectada en la fila. Valores: `A` (multiplicador de precio), `B` (volumen extremo), `C` (clima severo), `D` (bloqueo logístico), `E` (alerta sanitaria masiva), `None` (datos observados). |

---

## 6. Variables y Métricas de Anomalías (Alerts)

Contenidas en `alerts.parquet` y registradas para el supervisor:

| Campo | Tipo | Unidad | Descripción |
| :--- | :--- | :--- | :--- |
| `iforest_score` | Float | Probabilidad (0.0-1.0)| Puntuación calibrada a percentil obtenida por el algoritmo **Isolation Forest**. |
| `lof_score` | Float | Probabilidad (0.0-1.0)| Puntuación calibrada a percentil obtenida por el algoritmo **Local Outlier Factor (LOF)**. |
| `ecod_score` | Float | Probabilidad (0.0-1.0)| Puntuación calibrada a percentil obtenida por el algoritmo **ECOD**. |
| `ensemble_score` | Float | Probabilidad (0.0-1.0)| Score unificado del ensemble. Promedio simple de los tres percentiles anteriores. |
| `is_anomaly` | Boolean | Binario | Bandera de alerta del ensemble. Es `true` si `ensemble_score >= 0.95` o si al menos dos de los detectores marcan un percentil $\ge 0.95$. |
| `severity` | String | Categoría | Nivel de prioridad técnica asignado a la alerta. Categorías: `BAJA` ($\ge 0.95$), `MEDIA` ($\ge 0.975$), `ALTA` ($\ge 0.99$). |
| `alert_id` | String | UUIDv4 | Identificador único global e inmutable asignado a la alerta para linaje y auditoría. |
