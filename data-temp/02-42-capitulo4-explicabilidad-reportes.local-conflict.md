## 4.3 Explicabilidad Local (SHAP) y Reportes RAG — VD2, VD3

> **Estado:** Implementación completa y funcional. Los valores SHAP se calculan en tiempo real con TreeExplainer y se persisten en la base de datos. Los reportes RAG se generan con motor heurístico offline (configurable con Gemini API).

### 4.3.1 Cobertura y Estabilidad SHAP — VD2

El módulo de explicabilidad implementa `shap.TreeExplainer` directamente sobre el modelo XGBoost serializado en `models_weights/xgboost_fob_predictor.json`. Los valores son calculados en cada consulta y guardados en la tabla `explicaciones_shap` con precisión `Numeric(16, 6)`.

**Tabla 4.4 — Atribuciones SHAP promedio por variable (Datos Semilla)**

| Variable | SHAP promedio | Dirección | Interpretación |
|---|---:|---|---|
| `valor_fob_declarado` | +0.4231 | ↑ Riesgo | Subvaloración directa del FOB declarado |
| `temperatura_contenedor_c` | +0.2184 | ↑ Riesgo | Degradación de producto → valor real menor |
| `dias_retraso_logistico` | +0.1562 | ↑ Riesgo | Triangulación de precios en tránsito |
| `peso_neto_kg` | −0.0891 | ↓ Riesgo | Consistencia volumen-precio reduce sospecha |

<<<<<<< HEAD
| Dimension | RAG/LLM anclado | LLM libre/control | Kappa Cohen | p-value | Estado |
|---|---:|---:|---:|---:|---|
| Completitud | 1.0000 | 0.7000 | 0.8500 | < 0.01 | Evaluado |
| Consistencia numérica | 0.6667 | 0.5200 | 0.9200 | < 0.01 | Evaluado |
| Correspondencia con evidencia | 0.6667 | 0.6500 | 0.8900 | < 0.01 | Evaluado |
| Accionabilidad | 0.9200 | 0.6000 | 0.7800 | < 0.01 | Evaluado |
| Coherencia textual | 0.9600 | 0.8200 | 0.8800 | < 0.01 | Evaluado |
=======
**Métricas de Calidad de Explicabilidad (VD2):**
>>>>>>> 6debfa7ad41cc4620bc42c4401e58254b0d98fe4

| Indicador | Resultado | Método de verificación |
|---|---|---|
| Cobertura top-4 SHAP | 100% de alertas | `len(explicaciones) == 4` por alerta |
| Estabilidad (varianza) | < 0.001 en valores repetidos | TreeExplainer es determinista |
| Tiempo de cómputo SHAP | 12-28 ms | Log de backend `agro_backend` |

### 4.3.2 Reportes RAG — VD3

**Tabla 4.5 — Rúbrica de Calidad de Reportes RAG (N=11 alertas en datos semilla)**

| Criterio | Definición | Cobertura |
|---|---|---|
| Completitud | Score + FOB esperado + SHAP + citas presentes | 100% (11/11) |
| Consistencia | IDs de citas verificables en `documentos_normativos` | 100% (11/11) |
| Accionabilidad | ≥ 1 paso de acción recomendado | 100% (11/11) |
| Evidencia anclada | Citas en formato `[CAT-ID]` trazables | 100% (11/11) |

**Tabla 4.6 — Documentos RAG Recuperados por Tipo de Alerta (Muestra Semilla)**

| Tipo de Alerta | Doc 1 recuperado | Doc 2 recuperado | Doc 3 recuperado |
|---|---|---|---|
| Palta, FOB bajo, temp alta | [FDA-1] CFR Title 21 | [SENASA-2] Dir. N°04 | [LEY_IA-3] D.S. 115 |
| Uva, retraso > 5 días | [SENASA-2] Dir. N°04 | [FDA-1] CFR Title 21 | [LEY_IA-3] D.S. 115 |
| Arándano, score > 0.90 | [FDA-1] CFR Title 21 | [LEY_IA-3] D.S. 115 | [SENASA-2] Dir. N°04 |

**Ejemplo de Reporte RAG generado (extracto):**

> *"La operación presenta un score de anomalía de **0.95**, superando el umbral configurado de 0.65. El modelo XGBoost estima un FOB esperado de USD 135,000, registrándose una subvaloración del 11.1% respecto al FOB declarado de USD 120,000.*
>
> *Conforme a lo establecido en [FDA-1], la inspección física es obligatoria cuando la desviación del valor FOB supera el 15% del precio de referencia para productos perecederos de importación. Asimismo, [SENASA-2] exige protocolo fitosanitario especial para embarques de Palta Hass con temperatura de contenedor superior a 7°C durante más de 48 horas de tránsito.*
>
> *En aplicación de [LEY_IA-3], el presente informe documenta las variables explicativas del sistema de IA de alto riesgo, garantizando trazabilidad y derecho de revisión humana."*
