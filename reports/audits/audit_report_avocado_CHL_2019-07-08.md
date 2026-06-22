# REPORTE DE AUDITORÍA OPERATIVA: DETECCIÓN DE ANOMALÍA MULTIVARIABLE
**Código Único del Reporte (UUID):** 1f1fa46a-fbc2-4c00-8708-0178cd43dcd5
**Fecha de Generación:** 2026-06-19 (Lima Timezone)

---

## 1. RESUMEN DE LA ALERTA
*   **Producto:** avocado (Código Arancelario)
*   **Mercado de Destino:** CHL (Agregado)
*   **Semana de Análisis (semana t+1):** 2019-07-08
*   **Puntuación del Ensemble PyOD:** 0.9516
*   **Nivel de Severidad:** Baja
*   **Votos de los Detectores:** 2/3 (Isolation Forest, LOF, ECOD)

---

## 2. EVIDENCIA NUMÉRICA Y DESVÍOS (CAPA 1)
Se observa una desviación en las variables principales respecto al comportamiento esperado estimado por los modelos globales supervisados:

### A. Valor Unitario FOB (USD/kg)
*   **Valor Observado:** 1.2000 USD/kg
*   **Valor Predicho por Ensemble GBDT:** 1.1744 USD/kg
*   **Residuo de Predicción:** +0.0256 USD/kg
*   **Desviación Normalizada Robust-z (13 semanas):** +0.0000

### B. Volumen de Exportación Neto (kg)
*   **Volumen Observado:** 14,950.00 kg
*   **Volumen Predicho por Ensemble GBDT:** nan kg
*   **Residuo de Predicción:** +nan kg
*   **Desviación Normalizada Robust-z (13 semanas):** +nan

---

## 3. EXPLICABILIDAD DE LA ALERTA MEDIANTE TREESHAP (CAPA 3)
La atribución matemática del modelo (valores Shapley de contribución) identifica los siguientes factores influyentes:

### A. Atribución sobre el Valor Unitario FOB
*   **Factores que incrementan la predicción:** price_rolling_std_8 (+0.025), price_rolling_std_4 (+0.022), month_sin (+0.019), volume_rolling_mad_4 (+0.013), volume_rolling_std_13 (+0.013)
*   **Factores que reducen la predicción:** volume_rolling_max_8 (-0.233), price_rolling_mean_4 (-0.207), price_rolling_max_4 (-0.148), price_lag_1 (-0.129), price_rolling_min_4 (-0.111)

### B. Atribución sobre el Volumen de Exportación
*   **Factores que incrementan la predicción:** price_age_weeks (+9.396), volume_pct_change_52 (+0.431), volume_lag_2 (+0.096), volume_rolling_std_4 (+0.035), price_lag_4 (+0.033)
*   **Factores que reducen la predicción:** fob_lag_1 (-0.089), price_rolling_std_8 (-0.046), price_rolling_std_13 (-0.028), volume_lag_1 (-0.023), price_rolling_median_4 (-0.020)

*Nota Metodológica: Los valores SHAP representan la atribución interna del modelo a partir del espacio de características y no implican causalidad física directa en la operación agroexportadora.*

---

## 4. CONTEXTO NORMATIVO Y LIMITACIONES DE LA BASE DE CONOCIMIENTOS (RAG)
Los siguientes fragmentos fueron recuperados de la base de conocimientos documental mediante búsqueda híbrida para contextualizar la alerta:



---

## 5. TRAZABILIDAD DE DATOS Y FIRMA DE INTEGRIDAD (CAPA 6)
*   **ID de Alerta de Origen:** 9f268951de818d5a
*   **Modelo Regresor Precio Hash:** de840e781b7e640b805138c47684d329
*   **Modelo Regresor Volumen Hash:** e3a8c4a3e7bcee3c15b05df1bdfa67f4
*   **Modelo Detección Ensemble Hash:** bc42fbf7ac378adb3934f6f49b0675fd
*   **Firmas de Trazabilidad:** El presente reporte ha sido generado bajo conformidad del Decreto Supremo N.° 115-2025-PCM (IA responsable) y los lineamientos del NIST AI Risk Management Framework 1.0, quedando guardado para propósitos de auditoría operativa humana.
