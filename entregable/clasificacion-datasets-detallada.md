# Clasificación Detallada de Datasets
## Sistema Integrado de Supervisión Operativa con IA para Agroexportación Peruana

Este documento presenta la clasificación y sistematización de los **25 datasets identificados** y de los **archivos de datos reales** descargados y almacenados en la carpeta `data/`. Esta clasificación estructurada sirve como sustento de rigor metodológico para el Capítulo III (Metodología) y el Anexo A (Datasheets for Datasets) de la tesis.

---

## 1. Clasificación por Capas Funcionales de Integración

Para estructurar la ingesta del pipeline de predicción y detección de anomalías (y posterior justificación mediante SHAP y reportes RAG), los datasets se clasifican en tres capas funcionales:

```
                      ┌────────────────────────────────────────┐
                      │   CAPA 3: Validación Macroeconómica    │
                      │   (FAOSTAT, UN Comtrade, World Bank)   │
                      └───────────────────┬────────────────────┘
                                          │
                      ┌───────────────────▼────────────────────┐
                      │    CAPA 2: Contexto Sanitario y Clima  │
                      │      (SENASA, SENAMHI, SUNAT, INEI)    │
                      └───────────────────┬────────────────────┘
                                          │
                      ┌───────────────────▼────────────────────┐
                      │    CAPA 1: Datos Operativos Primarios  │
                      │           (MIDAGRI, BCRP)              │
                      └────────────────────────────────────────┘
```

### Capa 1: Datos Operativos Primarios
Representan las transacciones reales de comercio interno, ingresos a mercados y precios mayoristas que configuran el núcleo del modelado de series de tiempo.
*   **Boletines de Precios Mayoristas (MIDAGRI)**: Precios mensuales de productos hortofrutícolas.
*   **Reporte de Ingreso Diario a Mercados (MIDAGRI)**: Volúmenes e ingresos diarios de camiones con carga agrícola.
*   **Boletín de Abastecimiento GMML (MIDAGRI)**: Registro de stocks en el Gran Mercado Mayorista de Lima.
*   **Tipo de Cambio Mensual (BCRP)**: Serie temporal del tipo de cambio interbancario y bancario (crucial para conversión de precios FOB y costo operativo).

### Capa 2: Datos de Contexto Sanitario, Climático y de Aduanas
Variables exógenas que influyen directamente en la oferta, la calidad física y el cumplimiento de los despachos agroexportadores.
*   **Sanidad Agraria (SENASA)**: Requisitos fitosanitarios por producto, base de datos de establecimientos habilitados (packings/plantas de procesamiento) y manuales de Buenas Prácticas Agrícolas (BPA) enfocados en límites de contaminantes.
*   **Monitoreo Climático (SENAMHI)**: Pronósticos diarios y series históricas de lluvias acumuladas y temperaturas extremas en las zonas agroexportadoras (Ica, Piura, Arequipa, La Libertad, Lima).
*   **Estadísticas Aduaneras (SUNAT)**: Datos de flujos sectoriales por mes para cuantificar la dinámica agregada del comercio exterior.

### Capa 3: Datos de Validación Macroeconómica y Benchmarks
Series temporales consolidadas y agregadas a nivel internacional que sirven para realizar validación cruzada y análisis de consistencia de los modelos.
*   **Production & Trade Modules (FAOSTAT)**: Históricos anuales de rendimiento por hectárea, producción y comercio global de cultivos agrícolas peruanos desde 1961.
*   **Trade Statistics (UN Comtrade Plus)**: Base de datos de aduanas de la ONU para comprobar volúmenes de exportación declarados por Perú frente a los reportados por socios de destino (EE.UU., Unión Europea, Asia).
*   **Agricultural & Trade Data (World Bank)**: Indicadores de desarrollo y precios internacionales de commodities.

---

## 2. Clasificación por Formato y Estructura Técnica

La infraestructura de datos requiere procesar tres formatos distintos de almacenamiento:

| Formato | Tipo de Archivo | Características y Procesamiento | Ejemplos en el Proyecto |
| :--- | :--- | :--- | :--- |
| **Estructurado Plano** | `.csv` | Carga directa en DataFrames de Pandas. Formato limpio con delimitadores por comas. | Tipo de cambio (BCRP), Producción agrícola (FAOSTAT), Exportaciones (SUNAT) |
| **Tablas Complejas** | `.xlsx` / `.xls` | Tablas multipestaña con celdas combinadas y formatos visuales. Requieren parser especializado (`openpyxl` / `xlrd`) para extracción de series. | Boletines e insumos de comercialización mensuales de MIDAGRI (Julio-Diciembre 2025) |
| **Documental** | `.pdf` | Informes y normas redactadas. Requieren extracción de texto o procesamiento por modelos de visión/RAG para análisis cualitativo. | Manuales de BPA de SENASA, reportes mensuales "Agro en Cifras", y reportes del INEI |

---

## 3. Inventario Físico de Archivos Disponibles en `data/`

En el entorno de desarrollo se encuentran los siguientes archivos físicos listos para ser procesados por los módulos del pipeline:

| Carpeta / Ruta Física | Archivo | Tamaño | Cobertura Temporal | Propósito del Dataset |
| :--- | :--- | :--- | :--- | :--- |
| `data/bcrp/` | [bcrp-tipo-cambio-mensual.csv](file:///d:/tesis_yoset/data/bcrp/bcrp-tipo-cambio-mensual.csv) | 5.0 KB | Mayo 2024 - Abril 2026 | Proporcionar la serie de cotización del dólar para calcular valores en soles constantes e inflación. |
| `data/faostat/` | [faostat-produccion-peru-2024.csv](file:///d:/tesis_yoset/data/faostat/faostat-produccion-peru-2024.csv) | 15.4 KB | Año 2024 (Anual) | Servir de línea base del rendimiento (ha cosechadas) de cultivos de palta, espárrago y uva. |
| `data/inei/` | [inei-pbi-desestacionalizado-nov20.pdf](file:///d:/tesis_yoset/data/inei/inei-pbi-desestacionalizado-nov20.pdf) | 1.1 MB | Noviembre 2020 | Marco de referencia macroeconómica y comportamiento de sectores clave. |
| `data/sunat/` | [sunat-exportacion-sectorial-2026.csv](file:///d:/tesis_yoset/data/sunat/sunat-exportacion-sectorial-2026.csv) | 3.6 KB | Ene - Mar 2026 | Datos agregados de exportaciones FOB del sector agropecuario peruano tradicionales y no tradicionales. |
| `data/midagri/` | `Agro_en_cifras-*.pdf` | ~2.2 MB c/u | Julio - Diciembre 2025 | Reportes mensuales resumidos con el estado de la comercialización agrícola y pecuaria. |
| `data/midagri/` | Archivos Excel `.xlsx` y `.xls` | 150 KB - 1 MB c/u | Julio - Diciembre 2025 | Tablas de datos en bruto de producción agrícola, comercio interno, comercio externo e insumos. |

---

## 4. Alineación de Datos Sintéticos con Rangos Reales

El generador de datos sintéticos [generate_synthetic_dataset.py](file:///d:/tesis_yoset/src/generate_synthetic_dataset.py) utiliza los límites extraídos de los datasets reales listados arriba para asegurar que los datos de entrenamiento de los modelos de ensamble de PyOD (`XGBoost`, `LightGBM`, `Isolation Forest`, etc.) sean realistas:

*   **Ponderación de Productos**: La prevalencia de productos en la simulación se ajusta a la participación real del mercado exportador: arándano (30%), uva (25%), palta (20%), cacao (10%) y espárrago (15%).
*   **Ponderación Regional**: La distribución de zonas productoras simula la realidad geográfica: Ica (30%), La Libertad (25%), Piura (20%), Arequipa (15%) y Lima (10%).
*   **Rango de Precios FOB**: Calibrado según datos históricos de MIDAGRI y SUNAT (rango de 0.5 a 12.0 USD/kg).
*   **Parámetros Climáticos**: Calibrado según SENAMHI para temperaturas máximas/mínimas promedio de cada región, variando desde Arequipa (media de 22°C) hasta Piura (media de 30°C).

---

## 5. Recomendaciones para el Sustento en la Tesis

Para justificar la estrategia de datos ante el jurado revisor:
1.  **Enfoque Epistemológico**: Enfatizar que se utiliza un enfoque cuantitativo-descriptivo donde el dataset sintético permite la experimentación en escenarios controlados de anomalías, pero su distribución está anclada directamente en rangos reales recopilados de fuentes estatales.
2.  **Transparencia de Datos**: Utilizar el Anexo A (**Datasheets for Datasets**) para detallar el origen público de las variables, lo cual otorga validez externa a los experimentos de simulación.
3.  **Reproducibilidad**: Resaltar que el uso de la semilla aleatoria (`seed=42`) en el script generador garantiza que cualquier investigador pueda reproducir exactamente el mismo dataset con las mismas propiedades estadísticas.
