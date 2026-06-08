# Plan de Ingesta, Descarga Iterada y Segmentación Multiproducto (Capa 0)

Este documento detalla el plan de ingeniería de datos para la recopilación, descarga programática iterada, integración relacional y segmentación por producto de los conjuntos de datos de la tesis.

---

## 🗺️ 1. Arquitectura de Datos: Homogéneos vs. Segmentados

El pipeline de la **Capa 0** procesa los datos en dos dimensiones: datos **específicos** de la transacción (heterogéneos) y datos de **contexto** (homogéneos). Estos se unifican mediante cruces relacionales de fecha y región, para luego ser exportados en archivos de entrenamiento independientes por cada cultivo.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FUENTES DE DATOS COMPARTIDAS (HOMOGÉNEAS)           │
├───────────────────┬──────────────────────┬──────────────────────────────┤
│ BCRP API          │ SENAMHI Estaciones   │ World Bank Pink Sheet        │
│ Dólar mensual     │ Temp/Lluvia diaria   │ Precios Spot globales        │
└─────────┬─────────┴──────────┬───────────┴──────────────┬───────────────┘
          │                    │                          │
          └────────────────────┼──────────────────────────┘
                               │ (Cruces relacionales por Fecha y Zona)
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     FUENTES ESPECÍFICAS DE EXPORTACIÓN (HETEROGÉNEAS)    │
├─────────────────────────────────────────────────────────────────────────┤
│ SUNAT (Aduanet DBF)  ➔ Partidas, precios FOB, pesos netos, RUCs         │
│ PROMPERÚ Scraper     ➔ Top exportadores, mercados objetivos             │
│ NDVI Satelital (FAO) ➔ Vigor de vegetación local por cultivo            │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     DATASET MAESTRO UNIFICADO                           │
│                     (data/dataset_real_v1.csv)                          │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ (Particionado automático)
                               ▼
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
     [Segmento Palta]   [Segmento Uva]   [Segmento Arándano]
```

---

## 📂 2. Estructura de Directorios de Datos

Para evitar colisiones y mantener el orden metodológico, la carpeta `data/` se organizará de la siguiente manera:

```text
data/
|-- bcrp/                   # Respuestas JSON del tipo de cambio BCRP.
|-- sunat/
|   |-- raw_downloads/      # Archivos ZIP semanales descargados de Aduanet.
|   |-- extracted_dbfs/     # Bases de datos DBF temporales extraídas.
|-- weather/                # Series históricas diarias de SENAMHI por zona.
|-- global_benchmarks/      # Precios mundiales de commodities (World Bank).
|-- vegetation/             # Índices NDVI mensuales regionales (FAO/Copernicus).
|-- real_processed/         # Datasets finales filtrados y listos para modelar.
|   |-- palta/              # Train/Test y Modelos específicos de Palta.
|   |-- uva/                # Train/Test y Modelos específicos de Uva.
|   |-- arandano/           # Train/Test y Modelos específicos de Arándano.
```

---

## 🔄 3. Estrategia de Descarga Iterada y ETL Relacional

La recolección se realiza de forma programática y robusta, manejando excepciones de red y reintentos automáticos.

### A. Extracción Dinámica de Aduanas (SUNAT)
El script navega por la página de Aduanet de SUNAT, extrae los enlaces que apuntan a bases de datos de exportación definitiva (`x*.zip`), descarga iteradamente los últimos 10 archivos publicados y los almacena en `data/sunat/raw_downloads/`.

### B. Consumo Homogéneo de APIs y Benchmarks (BCRP, World Bank y SENAMHI)
*   **Tipo de Cambio BCRP**: Petición a la serie `PN01207PM` en formato JSON. Se almacena localmente en caché para evitar llamadas repetidas a la red durante el re-entrenamiento.
*   **Clima SENAMHI**: Descarga de series temporales de estaciones clave (Paita para Piura, San Camilo para Ica, Salaverry para La Libertad, La Joya para Arequipa).
*   **Precios World Bank**: Descarga del reporte CSV de commodities mensuales de la *Pink Sheet* del Banco Mundial, filtrando las series internacionales del sector agrícola.

### C. Joining Relacional de Datos en ETL
El unificador de datos (`etl_real_data.py`) mapea las aduanas de la DUA (`CADU`) a departamentos productores (`Zona`), y realiza la combinación relacional mediante:
1.  `fecha_numeracion` ➔ Cruce con Tipo de Cambio BCRP y Precios World Bank.
2.  `(fecha_numeracion, zona)` ➔ Cruce con Climatología SENAMHI y Vigor Vegetativo NDVI local.

---

## 🛠️ 4. Código de Segmentación y Particionado por Producto

El pipeline de preprocesamiento aplicará la división lógica por cultivo de forma determinista para que cada modelo aprenda las características únicas de su dominio.

```python
# src/segment_datasets.py
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("Segmenter")

def partition_master_dataset(master_path: Path, output_dir: Path):
    log.info("Cargando dataset maestro unificado: %s", master_path)
    df = pd.read_csv(master_path)
    
    crops = ["palta", "uva", "arandano"]
    for crop in crops:
        crop_dir = output_dir / crop
        crop_dir.mkdir(parents=True, exist_ok=True)
        
        # Filtrar transacciones del cultivo específico
        df_crop = df[df["producto"] == crop].copy()
        
        # Generar archivos crudos por cultivo
        raw_out = crop_dir / f"dataset_{crop}_raw.csv"
        df_crop.to_csv(raw_out, index=False)
        log.info("Segmento [%s] generado con %d transacciones en %s", 
                 crop.upper(), len(df_crop), raw_out.name)

if __name__ == "__main__":
    partition_master_dataset(
        Path("data/dataset_real_v1.csv"), 
        Path("data/real_processed")
    )
```

---

## 📅 5. Plan de Trabajo Detallado (Sprints y Entregables)

El plan se divide en **3 sprints de desarrollo de 2 semanas** para cubrir desde la ingesta de los nuevos datasets hasta el entrenamiento y reporte final.

### Sprint 1: Automatización de Descargas Multimodal (Clima, Macro y Satelital)
*   **Duración**: Semanas 1 y 2.
*   **Módulos Afectados**: Ingesta (Capa 0).
*   **Archivos Modificados**:
    *   [src/scrape_sunat_all.py](file:///d:/tesis_yoset/src/scrape_sunat_all.py): Añadir lógica de reintentos y descargas por bloques.
*   **Archivos Nuevos**:
    *   `src/download_global_benchmarks.py`: Descarga y procesamiento del CSV del Banco Mundial.
    *   `src/download_ndvi_fao.py`: Extractor del índice NDVI regional desde bases agrícolas.
*   **Entregables**:
    *   **Código**: Scripts de descarga con logs de estado y manejo de excepciones de conexión.
    *   **Documentación**: `docs/etl/guia-descarga-fuentes.md` detallando las URLs estables de BCRP, Banco Mundial y SENAMHI.

---

### Sprint 2: Pipeline ETL Relacional y Exportación Segmentada
*   **Duración**: Semanas 3 y 4.
*   **Módulos Afectados**: ETL y Limpieza.
*   **Archivos Modificados**:
    *   [src/etl_real_data.py](file:///d:/tesis_yoset/src/etl_real_data.py): Reescribir para integrar las llaves relacionales del Banco Mundial, NDVI y APN.
*   **Archivos Nuevos**:
    *   `src/segment_datasets.py`: Script automatizado para el particionado físico de datos por producto en carpetas independientes.
*   **Entregables**:
    *   **Código**: Script `segment_datasets.py` compilado y validado.
    *   **Datos**: Archivos CSV segmentados e independientes por cultivo generados con éxito bajo `data/real_processed/`.
    *   **Documentación**: `docs/etl/diseno-relacional-estrella.md` detallando los cruces lógicos de fecha-zona.

---

### Sprint 3: Entrenamiento Multiproducto y Tablas de Tesis
*   **Duración**: Semanas 5 y 6.
*   **Módulos Afectados**: Modelado IA (Capa 1 y 2), Generador de Tablas del Capítulo IV.
*   **Archivos Modificados**:
    *   [src/module1_prediction.py](file:///d:/tesis_yoset/src/module1_prediction.py): Adaptar para recibir un argumento de entrada `--crop` (palta, uva, arandano) y entrenar modelos específicos.
    *   [src/module2_anomaly.py](file:///d:/tesis_yoset/src/module2_anomaly.py): Ajustar para instanciar el ensemble PyOD de forma segmentada por cultivo.
    *   [scripts/update_capitulo4_tables.py](file:///d:/tesis_yoset/scripts/update_capitulo4_tables.py): Actualizar para inyectar métricas desglosadas por cada uno de los 3 productos en el borrador de la tesis.
*   **Entregables**:
    *   **Código**: Módulos de IA adaptados para entrenamiento en paralelo o secuencial parametrizado por cultivo.
    *   **Resultados**: Reporte JSON de métricas (`results_metrics.json`) actualizado con el rendimiento desglosado por Palta, Uva y Arándano.
    *   **Documentación**: Capítulo IV de la tesis actualizado con las tablas de precisión, recall y F1-score segmentadas y discutidas.
