# Pipeline de Limpieza, Tratamiento y Normalización de Datos

Este directorio contiene el pipeline de preparación de datos diseñado para el **Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas**. 

El script principal [preprocess_data.py](file:///d:/tesis_yoset/limpieza_de_datos_y_normalizacion/preprocess_data.py) procesa el dataset empírico agroexportador crudo, aplica ingeniería de variables, corrige datos faltantes, normaliza las escalas continuas y balancea el conjunto de entrenamiento para garantizar la convergencia óptima y evitar el sesgo en los algoritmos de detección de anomalías y predicción.

---

## 1. Datasets y Rutas de Archivos

El pipeline opera bajo una estructura de directorios estandarizada en la carpeta `data/` del proyecto. Las rutas de entrada y salida utilizadas son:

| Tipo de Dataset | Descripción | Ruta del Archivo |
| :--- | :--- | :--- |
| **Dataset Crudo (Input)** | Contiene los registros agroexportadores históricos crudos (con anomalías inyectadas y un 3% de datos faltantes para simular ruido real). | [`data/dataset_agro_sintetico_v1.csv`](file:///d:/tesis_yoset/data/dataset_agro_sintetico_v1.csv) |
| **Train Raw (Output)** | Conjunto de entrenamiento (2022-2024) preprocesado, escalado e imputado, pero manteniendo la distribución original de anomalías (sin balancear). | [`data/dataset_processed_train_raw.csv`](file:///d:/tesis_yoset/data/dataset_processed_train_raw.csv) |
| **Train Balanced (Output)** | Conjunto de entrenamiento balanceado mediante la técnica de sobremuestreo SMOTE (50% clase normal, 50% clase anómala) para modelos que lo requieran. | [`data/dataset_processed_train_balanced.csv`](file:///d:/tesis_yoset/data/dataset_processed_train_balanced.csv) |
| **Test Set (Output)** | Conjunto de evaluación final (2025) totalmente limpio y escalado, manteniendo la tasa original de anomalías (8.06%) para reportar métricas realistas. | [`data/dataset_processed_test.csv`](file:///d:/tesis_yoset/data/dataset_processed_test.csv) |

---

## 2. Metodología de Tratamiento de Datos

El pipeline se ejecuta de manera secuencial para asegurar la reproducibilidad técnica y prevenir la **fuga de datos (data leakage)** temporal o estadística.

### Paso 1: Ingeniería de Características (Feature Engineering)
Para capturar patrones estacionales y temporales característicos de la agroexportación, se generan las siguientes variables:
* **Codificación Cíclica de Fechas**: Se transforman el mes y el día del año utilizando funciones trigonométricas de seno y coseno (`mes_sin`, `mes_cos`, `dia_ano_sin`, `dia_ano_cos`). Esto permite que el modelo entienda que diciembre (mes 12) y enero (mes 1) son contiguos.
* **Rezago Temporal (Lags)**: Se calculan variables de rezago temporal a 1, 7 y 30 días para el precio (`precio_lag_1`, `precio_lag_7`, `precio_lag_30`) y el volumen (`volumen_lag_1`, `volumen_lag_7`, `volumen_lag_30`), agrupados por producto y departamento de origen (`zona`).
* **Imputación de Lags Iniciales**: Los primeros registros de la serie que carecen de historia temporal para calcular los rezagos se completan mediante interpolación hacia adelante (`ffill`) y hacia atrás (`bfill`) por grupos, y los nulos residuales globales se llenan con la mediana de la columna.

### Paso 2: Particionado Temporal Estricto
Para evitar contaminación en la evaluación debido a tendencias históricas e inflación, se realiza una división cronológica:
* **Conjunto de Entrenamiento**: Transacciones registradas entre **2022 y 2024** (fechas menores a `2025-01-01`).
* **Conjunto de Prueba**: Transacciones del año **2025** (fechas a partir de `2025-01-01`).

### Paso 3: Imputación de Datos Faltantes (KNNImputer)
El dataset de entrada contiene valores nulos aleatorios (3% en variables como `humedad_pct`, `dias_logisticos` y `costo_logistico_usd_kg`) debido a fallas de integración con sensores del SENAMHI o demoras logísticas.
* Se utiliza un imputador de vecinos más cercanos **`KNNImputer` con $K=5$**.
* **Protección contra data leakage**: El imputador se entrena (`fit`) únicamente en el conjunto de entrenamiento (Train) y se aplica (`transform`) tanto en Train como en Test.

### Paso 4: Escalamiento y Normalización Robusta (RobustScaler)
Dado que las anomalías inyectadas (precios excesivos, mermas extremas por daños fitosanitarios) actúan como outliers estadísticos severos, el uso de escaladores tradicionales como `MinMaxScaler` o `StandardScaler` (Z-Score) se ve distorsionado por el promedio y la varianza extrema de estas anomalías.
* Se aplica **`RobustScaler`**, que centra los datos restando la mediana y escala utilizando el rango intercuartílico (IQR, percentiles 25 a 75).
* Esto asegura que las características continuas (volumen, precio, temperatura, precipitaciones, costos y mermas) queden normalizadas sin que los outliers enmascaren la distribución normal.
* Al igual que en la imputación, el escalador se entrena (`fit_transform`) en Train y se aplica (`transform`) en Test.

### Paso 5: Balanceo de Clases por Sobremuestreo (SMOTE)
La tasa de anomalías del dataset crudo es de aproximadamente el 8%, lo que representa un desbalance severo de clases.
* Se aplica la técnica **SMOTE (Synthetic Minority Over-sampling Technique)** sobre el conjunto de entrenamiento.
* SMOTE sintetiza nuevas instancias de la clase minoritaria (anomalías) a lo largo de los segmentos de línea que unen a los vecinos más cercanos, elevando la representación de la clase al 50%.
* El conjunto de pruebas **no se balancea**, manteniendo la distribución real (8.06%) para garantizar una evaluación de performance del mundo real.

---

## 3. Resultados Cuantitativos del Pipeline

Tras ejecutar el pipeline, los resultados de los datasets resultantes son los siguientes:

* **Dataset de Entrenamiento Original (Train Raw)**: 
  * Total de registros: **902**
  * Uso: Detección no supervisada y calibración base.
* **Dataset de Entrenamiento Balanceado (Train Balanced - SMOTE)**: 
  * Total de registros: **1,658** (829 normales, 829 anómalos).
  * Uso: Entrenamiento de clasificadores supervisados (Capa 1: XGBoost / LightGBM) que requieren balanceo para evitar sesgos en el umbral de decisión.
* **Dataset de Prueba (Test)**: 
  * Total de registros: **1,787**
  * Tasa de anomalías: **8.06%**
  * Uso: Simulación de ejecución en producción, evaluación del ensemble PyOD y cálculo del tiempo de decisión en las pruebas de usabilidad.
