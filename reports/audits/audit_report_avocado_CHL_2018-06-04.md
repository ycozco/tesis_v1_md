# REPORTE DE AUDITORÍA OPERATIVA: DETECCIÓN DE ANOMALÍA MULTIVARIABLE
**Código Único del Reporte (UUID):** e4440321-0457-4f21-9b84-94366df05e24
**Fecha de Generación:** 2026-06-19 (Lima Timezone)

---

## 1. RESUMEN DE LA ALERTA
*   **Producto:** avocado (Código Arancelario)
*   **Mercado de Destino:** CHL (Agregado)
*   **Semana de Análisis (semana t+1):** 2018-06-04
*   **Puntuación del Ensemble PyOD:** 0.8826
*   **Nivel de Severidad:** Baja
*   **Votos de los Detectores:** 2/3 (Isolation Forest, LOF, ECOD)

---

## 2. EVIDENCIA NUMÉRICA Y DESVÍOS (CAPA 1)
Se observa una desviación en las variables principales respecto al comportamiento esperado estimado por los modelos globales supervisados:

### A. Valor Unitario FOB (USD/kg)
*   **Valor Observado:** nan USD/kg
*   **Valor Predicho por Ensemble GBDT:** nan USD/kg
*   **Residuo de Predicción:** +0.0000 USD/kg
*   **Desviación Normalizada Robust-z (13 semanas):** +0.0000

### B. Volumen de Exportación Neto (kg)
*   **Volumen Observado:** 0.00 kg
*   **Volumen Predicho por Ensemble GBDT:** 0.48 kg
*   **Residuo de Predicción:** -0.48 kg
*   **Desviación Normalizada Robust-z (13 semanas):** +0.0000

---

## 3. EXPLICABILIDAD DE LA ALERTA MEDIANTE TREESHAP (CAPA 3)
La atribución matemática del modelo (valores Shapley de contribución) identifica los siguientes factores influyentes:

### A. Atribución sobre el Valor Unitario FOB
*   **Factores que incrementan la predicción:** price_rolling_min_4 (+0.070), price_rolling_max_4 (+0.017), volume_rolling_mean_52 (+0.013), volume_rolling_max_8 (+0.012), volume_pct_change_4 (+0.012)
*   **Factores que reducen la predicción:** month_sin (-0.134), month_cos (-0.062), price_rolling_std_8 (-0.052), volume_rolling_std_8 (-0.051), product_code_avocado (-0.050)

### B. Atribución sobre el Volumen de Exportación
*   **Factores que incrementan la predicción:** fob_lag_1 (+0.003), shipment_count_lag_1 (+0.003), volume_rolling_std_8 (+0.002), volume_rolling_mean_8 (+0.002), volume_rolling_mean_4 (+0.002)
*   **Factores que reducen la predicción:** price_age_weeks (-0.196), volume_pct_change_52 (-0.011), volume_lag_1 (-0.005), week_cos (-0.003), price_lag_1 (-0.001)

*Nota Metodológica: Los valores SHAP representan la atribución interna del modelo a partir del espacio de características y no implican causalidad física directa en la operación agroexportadora.*

---

## 4. CONTEXTO NORMATIVO Y LIMITACIONES DE LA BASE DE CONOCIMIENTOS (RAG)
Los siguientes fragmentos fueron recuperados de la base de conocimientos documental mediante búsqueda híbrida para contextualizar la alerta:



---

## 5. TRAZABILIDAD DE DATOS Y FIRMA DE INTEGRIDAD (CAPA 6)
*   **ID de Alerta de Origen:** 840f836cf3370a2d
*   **Modelo Regresor Precio Hash:** de840e781b7e640b805138c47684d329
*   **Modelo Regresor Volumen Hash:** e3a8c4a3e7bcee3c15b05df1bdfa67f4
*   **Modelo Detección Ensemble Hash:** bc42fbf7ac378adb3934f6f49b0675fd
*   **Firmas de Trazabilidad:** El presente reporte ha sido generado bajo conformidad del Decreto Supremo N.° 115-2025-PCM (IA responsable) y los lineamientos del NIST AI Risk Management Framework 1.0, quedando guardado para propósitos de auditoría operativa humana.
