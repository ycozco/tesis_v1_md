# Decisiones Metodológicas de la Investigación

Este documento detalla las decisiones metodológicas definitivas que rigen la investigación y el desarrollo técnico del sistema. Estas decisiones están cerradas y no deben ser modificadas.

---

## 1. Identificación General

*   **Título Principal Propuesto:** Sistema integrado de inteligencia artificial explicable para la predicción del valor unitario FOB y volumen exportado, detección de anomalías y generación de reportes trazables en operaciones agroexportadoras peruanas.
*   **Título Alternativo (Corto):** Sistema integrado de inteligencia artificial explicable para la supervisión de operaciones agroexportadoras peruanas.
*   **Dominio del Estudio:** Operaciones agroexportadoras registradas en el Perú.
*   **Unidad de Análisis Principal:** producto × mercado de destino × semana (representada por la combinación `product_code`, `destination_market`, `week_start`).

---

## 2. Cobertura del Sistema

### 2.1 Productos Incluidos
El alcance de la investigación se restringe estrictamente a los siguientes tres productos núcleo (códigos arancelarios correspondientes):
1.  **Palta (*avocado*):** `0804400000`
2.  **Uva fresca (*grape*):** `0806100000`
3.  **Arándano (*blueberry*):** `0810400000`

> [!IMPORTANT]
> Se excluye por completo el cultivo de **cacao** de todas las fases del modelamiento predictivo principal y detección de anomalías por su baja representatividad transaccional en el dataset real. El cultivo de **espárrago** se excluye de los modelos principales y aparecerá únicamente en las limitaciones y trabajos futuros.

### 2.2 Periodo y Ventana Temporal
*   **Rango de Fechas Objetivo:** Desde el `2018-06-01` hasta el `2026-05-31` inclusive.
*   **Zona Horaria de Referencia:** `America/Lima` (PET).
*   **Frecuencia Analítica:** Semanal (definido mediante semanas ISO, de lunes a domingo).

---

## 3. Variables y Horizonte de Predicción

### 3.1 Variable Objetivo Principal (FOB)
*   **Nombre Académico:** Valor unitario FOB de exportación de la siguiente semana.
*   **Nombre Técnico:** `target_fob_unit_value_usd_kg_t1`
*   **Fórmula de Cálculo:** 
    $$\text{fob\_unit\_value\_usd\_kg} = \frac{\text{total\_fob\_usd}}{\text{total\_net\_weight\_kg}}$$
*   **Unidad de Medida:** USD por kilogramo (USD/kg).
*   **Interpretación:** Representa el valor unitario FOB promedio ponderado obtenido por kilogramo de exportación. No equivale a un precio internacional puro ya que puede reflejar variaciones por calidad, presentación, tamaño y contratos preestablecidos.

### 3.2 Variable Objetivo Secundaria (Volumen)
*   **Nombre Académico:** Volumen exportado durante la siguiente semana.
*   **Nombre Técnico:** `target_export_volume_kg_t1`
*   **Fórmula de Cálculo:** 
    $$\text{export\_volume\_kg} = \sum \text{net\_weight\_kg}$$
*   **Unidad de Medida:** Kilogramos (kg).
*   **Transformación:** Aplicación de $\log(1p)$ para estabilizar la asimetría en el modelamiento experimental, evaluando las métricas en su escala original.

### 3.3 Horizonte Predictivo
*   **Horizonte:** Una semana hacia adelante ($t+1$).
*   **Regla Temporal:** La información acumulada y calculada al cierre de la semana $t$ se utiliza para estimar los comportamientos en la semana $t+1$.
*   **Modelos Excluidos:** Se excluyen modelos de pronóstico multi-horizonte (como TFT, Chronos, N-BEATS, N-HiTS, LSTM o iTransformer) en el núcleo del sistema, enfocando la propuesta en algoritmos de aprendizaje de gradiente tabular sobre características diseñadas.

---

## 4. Cadena Analítica y Datos

### 4.1 Cadena de Procesamiento
Toda la lógica del sistema debe apegarse a la siguiente estructura secuencial:
$$\text{Fuentes Reales} \rightarrow \text{Ingesta y Normalización} \rightarrow \text{Datos Transaccionales} \rightarrow \text{Agregación Semanal} \rightarrow \text{Características Temporales} \rightarrow \text{Predicción FOB} \rightarrow \text{Predicción Volumen} \rightarrow \text{Cálculo de Residuos} \rightarrow \text{Ensemble PyOD} \rightarrow \text{SHAP} \rightarrow \text{RAG} \rightarrow \text{Validador Factual} \rightarrow \text{Log de Trazabilidad}$$

### 4.2 Fuentes de Información
1.  **Fuente Primaria:** Registros de aduanas de SUNAT/ADUANET (microdatos de exportaciones).
2.  **Fuente Macroeconómica:** Tipo de cambio PEN/USD del Banco Central de Reserva del Perú (BCRP).
3.  **Mercado Interno (Proxy):** Precios mayoristas de SISAP (MIDAGRI).
4.  **Clima (Proxy):** Radiación, temperatura y precipitación de NASA POWER o SENAMHI.
5.  **Fitosanitario y Logístico (Proxy):** Alertas sanitarias de SENASA o FDA, y estadísticas agregadas portuarias.
6.  **Trade Map:** Utilizado únicamente como benchmark comercial externo y validación macro, no como sustituto de los registros locales.

### 4.3 Tratamiento de Datos Sintéticos
*   **Uso Permitido:** Exclusivamente para la inyección controlada de anomalías con el fin de evaluar la sensibilidad, recall, precisión y puntuación F1 del ensemble de detección de anomalías y para pruebas del sistema generador de reportes.
*   **Uso Prohibido:** No se permite rellenar vacíos históricos de datos reales, simular tendencias de entrenamiento sin etiquetas de origen, o mezclar registros sintéticos dentro del conjunto de prueba limpio. Todos los datos sintéticos deben incluir `is_synthetic = true`.

---

## 5. Algoritmos e Implementación Analítica

### 5.1 Modelos Predictivos
*   **Baselines Obligatorios:** Última observación, mediana móvil (4 semanas), valor estacional (52 semanas) y regresión regularizada Elastic Net.
*   **Modelos Principales:** Regresores globales de XGBoost y LightGBM (un modelo unificado para todos los productos y mercados que incorpora las variables categóricas codificadas).

### 5.2 Detección de Anomalías
*   **Modelos Integrados:** Isolation Forest, Local Outlier Factor (LOF) y ECOD.
*   **Normalización de Puntuación:** Transformación de puntuaciones crudas a percentiles basados en la distribución de calibración de entrenamiento.
*   **Ensemble Score:** Promedio aritmético de los percentiles individuales de Isolation Forest, LOF y ECOD.
*   **Criterio de Alerta:** Una observación se etiqueta como anómala si el score del ensemble $\ge 0.95$ o si al menos dos detectores individuales marcan un percentil $\ge 0.95$.

### 5.3 Explicabilidad (SHAP)
*   **Formulación:** TreeSHAP aplicado a los regresores globales de GBDT para valor unitario FOB y volumen.
*   **Interpretación:** Mide la contribución local de cada variable en la desviación de la predicción respecto del valor esperado. No indica causalidad física y se asocia como justificación de alerta en el reporte.

### 5.4 Reportes RAG y Validación Factual
*   **Recuperación:** Motor de búsqueda híbrido (BM25 + Sentence Transformers) con Reciprocal Rank Fusion (RRF) sobre un corpus metodológico y operativo.
*   **Generación de Reporte:** Redacción de informes asistida por LLM o `TemplateProvider` a partir de un objeto JSON estructurado que encapsula la alerta.
*   **Validador Factual:** Filtro determinista que compara los valores numéricos citados en el texto contra la evidencia estructurada del JSON (tolerancia de error por redondeo $\le 0.5\%$).

---

## 6. Gobernanza y Trazabilidad

*   **Identificadores Únicos:** Uso de UUIDs en cada etapa del pipeline (`alert_id`, `prediction_id`, `report_id`, etc.).
*   **Integridad de Datos:** Cálculo de hashes SHA-256 de archivos fuente, datasets, configuraciones de modelos y reportes generados.
*   **Marcos Regulatorios:** Alineación conceptual del prototipo con el Decreto Supremo N° 115-2025-PCM (Gobernanza de IA y Supervisión Humana en Perú) y la Resolución SBS N° 053-2023 (Gestión de Riesgo de Modelos).
