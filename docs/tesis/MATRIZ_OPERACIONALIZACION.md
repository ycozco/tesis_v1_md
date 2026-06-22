# Matriz de Operacionalización de Variables

Esta matriz detalla las variables independiente, dependientes y explicativas que estructuran la investigación, alineadas con el dataset agroexportador integrado y la arquitectura analítica propuesta.

---

## 1. Variable Independiente

| Variable | Definición Conceptual | Definición Operacional | Dimensiones / Niveles | Indicador / Unidad | Escala | Técnica / Instrumento |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tipo de sistema de supervisión operativa** (VI) | Configuración arquitectónica del sistema informático de soporte analítico para la supervisión de exportaciones. | Variable categórica manipulada en la fase experimental comparando el pipeline integrado frente a herramientas analíticas independientes. | - **Sistema Integrado:** Pipeline secuencial de 4 capas con datos unificados, SHAP y reportes RAG con validador.<br>- **Componentes Aislados:** Salidas tabulares e interfaces técnicas inconexas sin flujo estructurado de evidencia. | - Presencia de integración funcional del pipeline.<br>- Valores: `integrado` / `aislado`. | Nominal | - **Técnica:** Experimentación tecnológica.<br>- **Instrumento:** Configuración lógica del pipeline en el código del sistema y logs. |

---

## 2. Variables Dependientes

| Variable | Definición Conceptual | Definición Operacional | Dimensiones | Indicadores y Fórmulas | Escala | Técnica / Instrumento |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Rendimiento predictivo** (VD1) | Capacidad de los modelos supervisados para estimar los valores esperados de precio y volumen. | Magnitud del error residual acumulado por los algoritmos XGBoost y LightGBM sobre el conjunto de prueba temporal fuera de muestra. | - Precisión de predicción de valor unitario FOB.<br>- Precisión de predicción de volumen. | - **MAE (FOB):** Mean Absolute Error en USD/kg.<br>- **RMSLE (Volumen):** Root Mean Squared Logarithmic Error. | De razón | - **Técnica:** Experimentación computacional.<br>- **Instrumento:** Consola de entrenamiento, librería `sklearn.metrics` y archivos JSON de registro de métricas. |
| **Rendimiento de detección de anomalías** (VD2) | Efectividad del ensemble no supervisado para discriminar desviaciones respecto del patrón normal histórico. | Medición de la capacidad de clasificación binaria (anómalo/normal) del ensemble sobre datos reales enriquecidos con inyección sintética controlada de anomalías (5%). | - Sensibilidad ante desviaciones.<br>- Tasa de falsas alarmas. | - **PR-AUC** (Área bajo la curva Precisión-Recall).<br>- **F1-Score** (Media armónica de Precisión y Recall).<br>- **ROC-AUC**.<br>- **Recall por tipo de anomalía** (A, B, C, D, E). | De razón | - **Técnica:** Experimentación computacional.<br>- **Instrumento:** Scripts de evaluación sintética controlada en `src/module2_anomaly.py`. |
| **Comprensión operativa de alertas** (VD3) | Grado de claridad percibida por un analista humano respecto de los motivos y factores que gatillaron una alarma de anomalía. | Nivel de entendimiento del usuario sobre qué variables influyeron en el score de anomalía y en qué sentido lo hicieron, evaluado mediante cuestionario. | - Identificación de factores explicativos.<br>- Comprensión de la magnitud y sentido. | - Puntuación media en escala Likert de 5 puntos (1: Total desacuerdo/Confuso, 5: Total acuerdo/Claro) en preguntas de comprensión de variables SHAP y contexto. | Ordinal | - **Técnica:** Encuesta (Prueba de usabilidad con usuarios).<br>- **Instrumento:** Cuestionario estructurado tipo Likert en la interfaz de supervisión. |
| **Tiempo de decisión** (VD4) | Eficiencia temporal de la supervisión analítica asistida para clasificar y justificar la revisión de una anomalía. | Cantidad de segundos transcurridos desde que se presenta la alerta en pantalla hasta que el evaluador registra su decisión fundamentada. | - Latencia de diagnóstico. | - Tiempo de respuesta en segundos (s) por alerta evaluada en la interfaz experimental. | De razón | - **Técnica:** Registro computacional indirecto.<br>- **Instrumento:** Módulos de cronómetro de la interfaz Flask/Streamlit y logs de bases de datos. |
| **Calidad y consistencia del reporte** (VD5) | Grado de coherencia textual e integridad factual de los informes narrativos autogenerados a partir de la alerta. | Porcentaje de coincidencia numérica exacta de las variables y métricas mencionadas en el texto del reporte contra el registro de evidencia estructurada. | - Fidelidad factual.<br>- Consistencia numérica. | - **Fidelidad numérica:** Porcentaje de cifras numéricas correctas citadas en el reporte (tolerancia error por redondeo $\le 0.5\%$). | De razón | - **Técnica:** Auditoría automatizada (análisis documental del texto).<br>- **Instrumento:** Script validador factual en `src/module5_validation.py`. |
| **Trazabilidad documental y linaje** (VD6) | Capacidad de auditar y reconstruir de extremo a extremo la procedencia y procesamiento de una alerta. | Proporción de alertas de anomalía en las que es posible verificar sus hashes SHA-256 históricos y el identificador único de cada recurso interviniente. | - Integridad del linaje de datos.<br>- Auditabilidad experimental. | - **Tasa de trazabilidad:** Porcentaje de registros de alertas con UUIDs y hashes SHA-256 completos para base de datos, características, modelo, predicción, SHAP y reporte. | De razón | - **Técnica:** Auditoría digital.<br>- **Instrumento:** Registro de auditoría (trazabilidad log) en `src/module6_traceability.py`. |

---

## 3. Variables Explicativas (Características del Modelo)

| Grupo | Variable Técnica | Definición y Unidad | Fuente Preferida | Tipo Metodológico | Uso en el Sistema |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Comercio Exterior** | `fob_unit_value_usd_kg` | Valor unitario FOB en USD/kg (FOB USD / Peso Neto kg). | SUNAT/ADUANET | Real observada / Derivada | Entrada de modelos predictivos y anomalías. Variable predictiva principal en $t$. |
| | `total_net_weight_kg` | Volumen neto exportado en kilogramos por semana. | SUNAT/ADUANET | Real observada | Entrada predictiva y de anomalías. Variable predictiva secundaria en $t$. |
| | `shipment_count` | Número total de despachos (declaraciones) semanales. | SUNAT/ADUANET | Real observada | Característica de escala y actividad. |
| | `exporter_count` | Cantidad de empresas exportadoras únicas activas en la semana. | SUNAT/ADUANET | Real observada | Característica de concentración empresarial. |
| | `destination_volume_share` | Participación de volumen del mercado de destino en las exportaciones totales del producto. | SUNAT/ADUANET | Derivada | Característica de peso de mercado. |
| **Mercado Interno** | `sisap_precio_prom` | Precio promedio mayorista del producto en mercados de Lima (PEN/kg). | SISAP/MIDAGRI | Real agregada (Proxy) | Variable exógena de oferta nacional. |
| **Macroeconomía** | `tipo_cambio_pen_usd` | Tipo de cambio promedio de venta interbancario de la semana. | BCRP | Real agregada | Factor macro de competitividad cambiaria. |
| **Clima** | `temperatura_media_c` | Temperatura media semanal en la zona productora (°C). | NASA POWER / SENAMHI | Proxy regional | Variable exógena física de impacto en producción. |
| | `precipitacion_mm` | Lluvia acumulada semanal en la zona productora (mm). | NASA POWER / SENAMHI | Proxy regional | Variable exógena física de impacto en producción. |
| **Logística** | `dias_logisticos` | Tiempo promedio de tránsito terrestre y aduanero estimado por semana (días). | OSITRAN / APN | Proxy logística | Variable de costos e ineficiencias de despacho. |
| **Sanidad** | `cumplimiento_fitosanitario` | Índice semanal agregado de rechazos y alertas sanitarias (SENASA/FDA). | SENASA / FDA | Proxy sanitaria | Variable de riesgo de mercado y rechazo. |
| **Contexto Internacional** | `trade_participacion_pct` | Participación porcentual de Perú en las importaciones del mercado de destino. | Trade Map | Real agregada | Factor estructural de posicionamiento competitivo. |
