# PLAN DE MIGRACIÓN: INGESTA DE MICRODATOS REALES (8 FUENTES OFICIALES)
## Alternativa de Máximo Rigor Académico sobre el Dataset Sintético
**Última actualización:** 2026-06-07  
**Responsable:** Yoset Cozco Mauri  

---

## 📌 1. Justificación del Cambio de Estrategia

El enfoque inicial del proyecto utilizaba un "generador estadístico" (`build_real_dataset.py`) que simulaba registros transaccionales diarios basándose en promedios agregados de PROMPERÚ y BCRP. Para una tesis de ingeniería de sistemas de alto rigor y con potencial de publicación indexada, **el jurado académico exige el uso de microdatos reales (datos transaccionales crudos)**.

Este plan detalla cómo migrar de la generación sintética a un pipeline de **ETL Real** utilizando microdatos descargados directamente de las 8 fuentes oficiales de la tesis:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              ECOSISTEMA DE FUENTES DE MICRODATOS REALES                │
├──────────────────┬──────────────────┬──────────────────┬──────────────────┬────────────┤
│ SUNAT (Aduanas)  │ SENAMHI (Clima)  │ SENASA (Sanidad) │ MIDAGRI (SISAP)  │ INEI (PBI) │
├──────────────────┴────────┬─────────┴────────┬─────────┴────────┬─────────┴──────┬─────┘
                            │ BCRP (T. Cambio) │ FAOSTAT (Cosecha)│ UN Comtrade    │
                            └──────────────────┴──────────────────┴────────────────┘
                                                    │
                                                    ▼
                                   ┌───────────────────────────────────┐
                                   │     ETL UNIFICADOR (DuckDB)       │ ➔ Filtra por partida, une por RUC,
                                   │     (src/etl_real_data.py)        │   zona y fecha de exportación
                                   └─────────────────┬─────────────────┘
                                                     ▼
                                   ┌───────────────────────────────────┐
                                   │     DATASET TRANSACCIONAL REAL    │ ➔ 100% transacciones reales con
                                   │     (data/dataset_real_v1.csv)    │   contexto climático y macro
                                   └───────────────────────────────────┘
```

---

## 📂 2. Especificación de Datasets e Instrucciones de Navegación

> [!NOTE]
> Dado que los servidores del Estado peruano (SUNAT, SENAMHI, INEI) reestructuran periódicamente sus rutas internas causando errores 404 en enlaces profundos, se proporcionan los **portales de acceso general estables** y las **instrucciones de navegación paso a paso** para ubicar cada conjunto de datos.

### 1. SUNAT (Superintendencia Nacional de Aduanas y de Administración Tributaria)
*   **Nombre del Dataset:** *Descarga de Base de Datos de Regímenes Definitivos - Exportación Definitiva*.
*   **Portal de Acceso Estable:** [https://www.sunat.gob.pe/operatividadaduanera/](https://www.sunat.gob.pe/operatividadaduanera/)
*   **Ruta de Navegación:**
    1. Ingresar al portal de **Operatividad Aduanera de SUNAT**.
    2. En el menú lateral o central de servicios de información, ubicar la sección **Descarga de Información**.
    3. Seleccionar la opción **Bases Regímenes Definitivos** (o *Descarga de datos de Importación, Exportación*).
    4. Descargar el archivo de estructura `estructura_bases.xls` y el archivo comprimido `.zip` del año de interés (por ejemplo, `x2024.zip` para exportaciones de 2024).
    5. Para catálogos de códigos (aduanas, países), navegar en el menú de Operatividad a **Catálogos de Códigos** > **Bajar información tablas**.
*   **Datos extraídos:** Fecha de numeración, aduana de despacho, RUC del exportador, nombre del exportador, partida arancelaria (10 dígitos), valor FOB USD y peso neto (kg).

### 2. SENAMHI (Servicio Nacional de Meteorología e Hidrología del Perú)
*   **Nombre del Dataset:** *Descarga de datos históricos de estaciones meteorológicas*.
*   **Portal de Acceso Estable:** [https://www.senamhi.gob.pe](https://www.senamhi.gob.pe)
*   **Ruta de Navegación:**
    1. Ingresar al portal principal de **SENAMHI**.
    2. En la barra de navegación superior, seleccionar **Datos** ➔ **Descarga de datos meteorológicos** (o ir directamente a [senamhi.gob.pe/servicios/?p=descarga-datos-meteorologicos](https://www.senamhi.gob.pe/servicios/?p=descarga-datos-meteorologicos)).
    3. Registrarse de forma gratuita para obtener las credenciales de descarga.
    4. En el mapa interactivo, seleccionar la estación de la zona de interés (ej. Estación *San Camilo* en Ica o *San Pedro* en Piura).
    5. Ir a la pestaña **Descarga**, ingresar el rango de fechas e ingresar el código de verificación para bajar la serie diaria en formato de texto.
*   **Datos extraídos:** Lecturas diarias de temperatura máxima (°C), temperatura mínima (°C) y precipitación acumulada (mm).

### 3. SENASA (Servicio Nacional de Sanidad Agraria)
*   **Nombre del Dataset:** *Certificados Fitosanitarios de Exportación Emitidos* e *Inscripción de Plantas de Empaque Habilitadas*.
*   **Portales de Acceso Estables:**
    *   *Plataforma de Datos Abiertos:* [https://datosabiertos.gob.pe](https://datosabiertos.gob.pe)
    *   *Portal del SENASA:* [https://www.gob.pe/senasa](https://www.gob.pe/senasa)
*   **Ruta de Navegación:**
    1. En **datosabiertos.gob.pe**, utilizar el buscador principal e ingresar `"Servicio Nacional de Sanidad Agraria"` para filtrar la organización, y buscar los datasets de certificados fitosanitarios.
    2. Alternativamente, en el portal de **SENASA**, dirigirse a **Informes y Publicaciones** y buscar *"Lista de empacadoras habilitadas"* o el nombre del cultivo de interés (arándano, palta, uva, etc.) para descargar el archivo de control en formato `.xlsx`.
*   **Datos extraídos:** RUC de la agroexportadora habilitada, cultivo certificado, número de certificado, fecha de emisión y estado (Aprobado/Rechazado).

### 4. MIDAGRI (Ministerio de Desarrollo Agrario y Riego)
*   **Nombre del Dataset 1 (SISAP):** *Volumen e Ingreso de Productos en el Gran Mercado Mayorista de Lima y Mercado de Frutas N° 2*.
*   **Nombre del Dataset 2 (SIEA):** *Boletín Estadístico de la Producción Agrícola Regional*.
*   **Portales de Acceso Estables:**
    *   *Portal SISAP:* [http://sistemas.minag.gob.pe/sisap/portal/](http://sistemas.minag.gob.pe/sisap/portal/)
    *   *Portal SIEA:* [http://siea.midagri.gob.pe/siea/](http://siea.midagri.gob.pe/siea/)
*   **Ruta de Navegación:**
    *   En el **SISAP**, seleccionar el módulo **SISAP Lima** o **Precios de Ciudades** para consultar el histórico de precios mayoristas por producto.
    *   En el **SIEA**, seleccionar **Estadísticas Agrícolas** ➔ **Producción Agrícola** para descargar las planillas mensuales de rendimiento agrícola regional.
*   **Datos extraídos:** Precios nacionales diarios por cultivo y rendimiento agrícola mensual por departamento de origen.

### 5. INEI (Instituto Nacional de Estadística e Informática)
*   **Nombre del Dataset 1 (Microdatos):** *Encuesta Nacional Agropecuaria (ENA)*.
*   **Nombre del Dataset 2 (Variaciones):** *Índice de Precios al por Mayor (IPM)*.
*   **Portales de Acceso Estables:**
    *   *Portal de Microdatos:* [http://iinei.inei.gob.pe/microdatos/](http://iinei.inei.gob.pe/microdatos/)
    *   *Portal INEI Principal:* [https://www.inei.gob.pe](https://www.inei.gob.pe)
*   **Ruta de Navegación:**
    *   En el **Portal de Microdatos**, seleccionar **Consulta por encuestas**, elegir la **Encuesta Nacional Agropecuaria (ENA)**, seleccionar el año correspondiente y descargar los módulos de interés en formato SPSS/CSV.
    *   En el **Portal del INEI**, ir a **Estadísticas** ➔ **Índice Temático** ➔ **Precios** ➔ **Índice de Precios al por Mayor** para descargar las series históricas mensuales en XLS.
*   **Datos extraídos:** Encuestas de caracterización de la unidad productora agrícola (ENA), e índice de inflación mayorista mensual (IPM).

### 6. BCRP (Banco Central de Reserva del Perú)
*   **Nombre del Dataset:** *Series Estadísticas Mensuales y Diarias (BCRPData)*.
*   **Portal de Acceso Estable:** [https://estadisticas.bcrp.gob.pe/estadisticas/series/](https://estadisticas.bcrp.gob.pe/estadisticas/series/)
*   **Ruta de Navegación / Programática:**
    *   *Consulta Programática:* Utilizar la API RESTful oficial para consultar series sin intermediarios:
        *   JSON: `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json/2024-01/2026-12` (Serie `PN01207PM` para Tipo de Cambio).
        *   CSV: `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/csv/2024-01/2026-12`.
    *   *Portal Web:* Buscar el código de la serie (ej. `PN01207PM`) en el buscador del portal BCRPData y descargar los datos consolidados en Excel.
*   **Datos extraídos:** Tasa cambiaria oficial aplicable a la fecha exacta de numeración de la exportación aduanera.

### 7. FAOSTAT (Organización de las Naciones Unidas para la Alimentación y la Agricultura)
*   **Nombre del Dataset:** *Production - Crops and livestock products (Perú)*.
*   **Portal de Acceso Estable:** [https://www.fao.org/faostat/en/](https://www.fao.org/faostat/en/)
*   **Ruta de Navegación:**
    *   Ingresar al portal de **FAOSTAT** y seleccionar el menú **Data**.
    *   Hacer clic en **Production** ➔ **Crops and livestock products** (o ir directamente a [fao.org/faostat/en/#data/QCL](https://www.fao.org/faostat/en/#data/QCL)).
    *   Seleccionar el país ("Peru"), los productos (arándano, palta, uva, cacao, espárrago), las variables (área cosechada, rendimiento, cantidad producida) y descargar el archivo CSV.
*   **Datos extraídos:** Rendimientos históricos del cultivo (toneladas por hectárea), área cosechada y volumen global de producción del Perú para validación de frontera productiva.

### 8. UN Comtrade (Organización de las Naciones Unidas)
*   **Nombre del Dataset:** *International Trade Statistics (Goods, HS)*.
*   **Portal de Acceso Estable:** [https://comtradeplus.un.org](https://comtradeplus.un.org)
*   **Ruta de Navegación:**
    *   Ingresar a la plataforma **Comtrade Plus**.
    *   Configurar los filtros de búsqueda rápida: Type: *Goods*, Frequency: *Monthly*, Commodity Code: subpartidas a 6 dígitos (Blueberry: `081040`, Uva: `080610`, Palta: `080440`, Espárrago: `070920`, Cacao: `180100`), Reporter: *Peru*.
    *   Descargar la base de datos resultante en formato CSV.
*   **Datos extraídos:** Volúmenes e importaciones globales en USD de los países de destino para entrenar las variables exógenas del modelo de forecasting de demanda (Capa 1).

---

## 🛠️ 3. El Pipeline ETL: Integración y Unificación

Para procesar estas 8 fuentes de microdatos crudos, se estructurará un script de procesamiento en Python: **`src/etl_real_data.py`** que utilizará **DuckDB** para realizar consultas SQL analíticas de alto rendimiento sobre los archivos locales.

### Algoritmo del ETL Real
1.  **Ingesta de Aduanas (SUNAT):**
    *   Cargar las tablas de cabecera y detalle de los archivos unificados de SUNAT.
    *   Filtrar las transacciones correspondientes únicamente a las 5 subpartidas nacionales de interés.
2.  **Integración Climatológica (SENAMHI):**
    *   Mapear las aduanas de despacho de SUNAT (`CODI_ADUA`) a las zonas geográficas.
    *   Hacer un `JOIN` temporal utilizando el par `(fecha, zona)` para inyectar la temperatura máxima, mínima y precipitación registrada ese día en la zona productora.
3.  **Integración de Cumplimiento (SENASA):**
    *   Hacer un `LEFT JOIN` utilizando el RUC del exportador (`RUCP_EXPO`) y la `fecha` para verificar si la transacción cuenta con la habilitación fitosanitaria del SENASA y asociar el estado de cumplimiento (1 si cuenta con certificado; 0 si no cuenta o fue rechazado).
4.  **Integración Macroeconómica y Comercial (MIDAGRI + INEI + BCRP + UN Comtrade):**
    *   Hacer un `LEFT JOIN` por `fecha` y `producto` para inyectar el precio de mercado local diario (SISAP) y el índice de precios al por mayor (IPM).
    *   Asociar la cotización del Tipo de Cambio (BCRP) y la demanda agregada internacional (UN Comtrade).
5.  **Cálculo de Mermas Estimadas:**
    *   Asociar mermas promedio por tipo de cultivo usando la correlación entre el tiempo de tránsito logística de la SUNAT (diferencia entre fecha de embarque y numeración) y la temperatura promedio del trayecto.

---

## 🎯 4. Impacto en la Detección de Anomalías

Al migrar a microdatos 100% reales, **ya no será necesario inyectar anomalías artificialmente**. El pipeline de la Capa 2 (Ensemble PyOD: Isolation Forest + LOF + ECOD) actuará directamente sobre las transacciones del mundo real:

*   Detectará **anomalías de precios:** subvaluación o sobrevaluación de precios FOB declarados en aduanas frente a precios de mercados locales e internacionales.
*   Detectará **anomalías de volumen:** despachos inusualmente grandes para mermas reportadas.
*   Detectará **stress climático:** correlación de picos de calor (SENAMHI) con aumentos en la tasa de merma del cultivo.

Esto le da a la tesis un enfoque **100% empírico y no-simulado**, elevando radicalmente su valor metodológico para los jurados de la UNSA.
