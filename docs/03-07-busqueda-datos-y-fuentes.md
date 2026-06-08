# GUÍA DETALLADA DE BÚSQUEDA DE DATOS Y MAPEO DE FUENTES
## Sistema Integrado de Supervisión Operativa con IA Explicable — Tesis UNSA
**Última actualización:** 2026-06-07  
**Responsable:** Yoset Cozco Mauri  

Este documento detalla la metodología de búsqueda, extracción, integración y estructuración de los datos del sector agroexportador peruano para el entrenamiento y evaluación de los modelos de la tesis.

---

## 🗺️ 1. Arquitectura de Búsqueda y Mapeo de Fuentes

La tesis combina datos empíricos reales obtenidos mediante APIs y raspado web (*scraping*) de portales oficiales, con simulaciones basadas en distribuciones estadísticas de variables climáticas, logísticas y regulatorias. 

El ecosistema de fuentes está organizado de la siguiente manera:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           FUENTES EXTERNAS REALES                        │
├───────────────────┬──────────────────────┬───────────────────────────────┤
│ API REST BCRP     │ Portal PROMPERÚ      │ Repositorios Locales          │
│ Tipo de cambio    │ Precios FOB, RUC,    │ FAOSTAT, SUNAT, INEI          │
│ PEN/USD mensual   │ destinos, empresas   │ PBI, volúmenes históricos     │
└─────────┬─────────┴──────────┬───────────┴──────────────┬────────────────┘
          │                    │                          │
          ▼                    ▼                          ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   EXTRACTOR INTEGRADO (build_real_dataset.py)             │
├──────────────────────────────────────────────────────────────────────────┤
│ - Descarga y parsea la API de BCRP.                                      │
│ - Extrae __NEXT_DATA__ (JSON estructurado) de las fichas de PROMPERÚ.     │
│ - Modula variables exógenas (clima por zonas, mermas por producto).      │
│ - Inyecta un 12% de anomalías operativas (precio, volumen, mermas...).   │
│ - Inyecta un 3% de datos faltantes para simular ruido del SENAMHI/sensores│
└──────────────────────────────────┬───────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                  DATASET OPERATIVO (dataset_agro_sintetico_v1.csv)       │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 2. Catálogo de Variables y Fuentes de Origen

Cada variable del dataset de trabajo está mapeada a una entidad regulatoria o estadística real en el Perú:

| Variable | Tipo de Dato | Unidad / Rango | Origen de los Datos / Criterio |
| :--- | :--- | :--- | :--- |
| `fecha` | Temporal | AAAA-MM-DD | Uniforme (2024-01-01 a 2026-12-31). |
| `producto` | Categórico | Arándano, Uva, Palta, Cacao, Espárrago | **PROMPERÚ**: Mapeados a las 5 partidas arancelarias de mayor exportación. |
| `partida_arancelaria` | Categórico | Código HS (10 dígitos) | **SUNAT**: Clasificación aduanera oficial de exportación. |
| `empresa_exportadora` | Categórico | Razón social real (ej. Camposol) | **PROMPERÚ**: Extraído del Top-10 de exportadores reales de cada ficha. |
| `zona` | Categórico | Ica, La Libertad, Piura, Arequipa, Lima | **MIDAGRI**: Regiones líderes en agroexportación. |
| `volumen_kg` | Continuo | 500 a 50,000 kg | **PROMPERÚ / SUNAT**: Muestreo Log-Normal calibrado con cargas de contenedores standard (FCL). |
| `precio_kg_usd` | Continuo | 0.50 a 12.00 USD/kg | **PROMPERÚ**: Calibrado dinámicamente según el precio FOB referencial mensual real de 2024-2026. |
| `destino_mercado` | Categórico | EEUU, UE, Asia, Otro | **PROMPERÚ**: Probabilidades de destino extraídas de la participación de mercados cerrados. |
| `dias_logisticos` | Entero | 3 a 80 días | **SUNAT / Operadores Logísticos**: Simulado por destino (ej. Asia: 25-45 días; EEUU: 8-18 días). |
| `costo_logistico_usd_kg`| Continuo | 0.12 a 2.50 USD/kg | **Operadores Logísticos**: Tarifa base + factor de días transcurridos. |
| `cumplimiento_fitosanitario`| Binario | 0 (Rechazo), 1 (Aprobado) | **SENASA**: Tasa base de aprobación fitosanitaria del 94%. |
| `merma_pct` | Continuo | 0% a 30% | **Control de Calidad**: Muestreo Beta calibrado por tipo de cultivo (perecibilidad). |
| `tipo_cambio_pen_usd` | Continuo | 3.50 a 4.20 PEN/USD | **BCRP API**: Serie de tipo de cambio promedio mensual real. |
| `temperatura_max_c` | Continuo | 15.0 a 38.0 °C | **SENAMHI**: Estaciones climatológicas por zona (Piura: 30°C; Ica: 26°C; Arequipa: 22°C). |
| `temperatura_min_c` | Continuo | 5.0 a 22.0 °C | **SENAMHI**: Delta de temperaturas diarias registradas por región. |
| `precipitacion_mm` | Continuo | 0.0 a 200.0 mm | **SENAMHI**: Simulación Gamma climatológica (Piura con mayor estacionalidad). |
| `humedad_pct` | Continuo | 40% a 95% | **SENAMHI**: Humedad promedio de valles costeros. |

---

## 🔗 3. Mapeo de Enlaces de Consulta y Descarga

Para la sustentación ante el jurado, es crítico mantener la trazabilidad de los enlaces de las fuentes públicas utilizadas. 

### A. Tipo de Cambio (BCRP API)
*   **Endpoint de consulta:** `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{serie}/json/{fecha_inicio}/{fecha_fin}`
*   **Serie utilizada:** `PN01207PM` (Tipo de cambio promedio mensual PEN/USD, venta interbancaria).
*   **Parámetros:** `2024-01` a `2026-12`.
*   **Ubicación local de datos descargados:** [bcrp/](file:///d:/tesis_yoset/data/bcrp)

### B. Estadísticas de Exportación por Producto (PROMPERÚ)
Se realiza raspado de datos (*scraping*) directamente sobre las páginas de comercio de PromPerú para obtener el JSON del frontend (`__NEXT_DATA__`). 

*   **URL de la Ficha General:** `https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/{partida}`
*   **Partidas arancelarias mapeadas:**
    *   **Arándano:** `0810400000` (Ficha: [exportemos.pe/producto/0810400000](https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0810400000))
    *   **Uva fresca:** `0806100000` (Ficha: [exportemos.pe/producto/0806100000](https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0806100000))
    *   **Palta fresca:** `0804400000` (Ficha: [exportemos.pe/producto/0804400000](https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0804400000))
    *   **Cacao en grano:** `1801001900` (Ficha: [exportemos.pe/producto/1801001900](https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/1801001900))
    *   **Espárrago fresco:** `0709200000` (Ficha: [exportemos.pe/producto/0709200000](https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0709200000))

### C. Estadísticas Sectoriales e Históricas (Local Data)
*   **SUNAT Aduanas:** Se recopilaron las estadísticas agregadas de exportaciones de la SUNAT en **[sunat/](file:///d:/tesis_yoset/data/sunat)**.
*   **FAOSTAT:** Datos anuales de rendimientos y áreas cultivadas en el Perú para validación externa en **[faostat/](file:///d:/tesis_yoset/data/faostat)**.
*   **INEI PBI:** Informes técnicos del Producto Bruto Interno mensual para contextualización macroeconómica en **[inei/](file:///d:/tesis_yoset/data/inei)**.

---

## 🛠️ 4. Protocolo de Ejecución y Generación del Dataset

El pipeline de extracción y consolidación de datos ya está programado en **[build_real_dataset.py](file:///d:/tesis_yoset/src/build_real_dataset.py)**. Para ejecutar la descarga de APIs y unificar los datos empíricos con el dataset final, sigue estos pasos:

### Paso 1: Activar el Entorno Virtual e Instalar Dependencias
Asegúrate de tener instaladas las dependencias del entorno de machine learning:
```powershell
# En la raíz del proyecto (D:\tesis_yoset)
.venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 2: Ejecutar el Generador
Ejecuta el script unificador de datos reales:
```powershell
python src/build_real_dataset.py
```
*   **Qué hace el script:** Conecta al API de BCRP para descargar los tipos de cambio, raspa las fichas de PROMPERÚ, parsea el JSON interno, extrae los top exportadores reales y los precios FOB del histórico, y genera el archivo **[dataset_agro_sintetico_v1.csv](file:///d:/tesis_yoset/data/dataset_agro_sintetico_v1.csv)**.

### Paso 3: Ejecutar el Preprocesamiento y Tratamiento Estadístico
Una vez generado el dataset crudo unificado, ejecuta el script de normalización y limpieza:
```powershell
python limpieza_de_datos_y_normalizacion/preprocess_data.py
```
*   **Qué hace el script:** Aplica codificación cíclica a las fechas, calcula rezagos temporales (*lags*), aplica `KNNImputer` para completar nulos operacionales, escala con `RobustScaler` (mantiene intactos los outliers operacionales) y realiza balanceo de clases `SMOTE` en el set de entrenamiento.

### Paso 4: Validar las Salidas Procesadas
Verifica en la carpeta `data/` que existan los archivos limpios listos para modelado:
*   `data/dataset_processed_train_raw.csv` (Entrenamiento con anomalías originales).
*   `data/dataset_processed_train_balanced.csv` (Entrenamiento balanceado SMOTE 50% anomalías).
*   `data/dataset_processed_test.csv` (Test set con tasa natural de anomalías del 8.06% para evaluación).
