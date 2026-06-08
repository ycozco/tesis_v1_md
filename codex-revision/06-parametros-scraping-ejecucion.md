# Parámetros de scraping y ejecución

Fecha: 2026-06-07  
Ruta de trabajo: `d:\tesis_yoset`  
Modo aplicado: scraping/API probe controlado, sin descarga masiva de binarios.

## Parámetros globales

```yaml
workspace: "d:/tesis_yoset"
python: "d:/tesis_yoset/.venv/Scripts/python.exe"
encoding: "utf-8"
user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
timeout_seconds: 25
allow_redirects: true
productos_incluidos:
  palta: "0804400000"
  uva: "0806100000"
  arandano: "0810400000"
  esparrago: "0709200000"
producto_excluido:
  cacao: "1801001900"
periodo_objetivo: "2018-01 a 2026-06"
```

## SUNAT/Aduanet - bases definitivas

### URL

```text
http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm
```

### Método

```text
GET HTML -> extraer enlaces .zip/.xls -> normalizar barras invertidas -> descargar ZIP -> extraer DBF
```

### Patrones detectados

```text
x*.zip   = exportaciones definitivas
ma*.zip
mb*.zip
mam*.zip
idv*.zip
estructura_bases.xls
totales_2011.xls
```

### Parámetros operativos

```yaml
download_dir: "data/sunat/raw_downloads"
extract_dir: "data/sunat/extracted_dbfs"
zip_prefix_exportacion: "x"
dbf_encoding: "latin1"
partidas:
  palta: 804400000
  uva: 806100000
  arandano: 810400000
  esparrago: 709200000
excluir:
  cacao: 1801001900
dua_key: "CADU + FANO + NDCL + NSER"
```

### Campos esperados DBF

```text
CADU, FANO, NDCL, NSER, FNUM, FEMB, PART_NANDI, DNOMBRE, NDOC,
FOB_DOLPOL, VPESNET, CPAIDES
```

Los nombres exactos deben confirmarse contra `estructura_bases.xls`.

## BCRP - tipo de cambio mensual

### Endpoint probado

```text
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json/2018-01/2026-06
```

### Parámetros

```yaml
serie: "PN01207PM"
formato: "json"
inicio: "2018-01"
fin: "2026-06"
variable_salida: "tipo_cambio_pen_usd"
granularidad: "mensual"
merge_key: "YYYY-MM"
```

### Normalización

```text
Ene.2018 -> 2018-01
Feb.2018 -> 2018-02
...
May.2026 -> 2026-05
```

## PROMPERÚ Exportemos

### URLs por producto

```text
https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0804400000
https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0806100000
https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0810400000
https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0709200000
```

### Método

```text
GET HTML -> extraer <script id="__NEXT_DATA__" type="application/json"> -> parsear JSON
```

### Claves detectadas

```text
indices
partidasArancelarias
estacionalidad
preciosReferenciales
principalesMercados
exportadoresPorRegion
empresasExportadoras
parametrosFicha
fichaProducto
```

### Variables limpias

```text
producto
partida
mercados_top
empresas_top
precios_referenciales_mensuales
regiones_exportadoras
estacionalidad
```

Uso recomendado: validación comercial y calibración contextual, no sustituto del microdato SUNAT.

## MIDAGRI - comercio exterior agrario

### URL

```text
https://www.gob.pe/institucion/midagri/informes-publicaciones/2730438-compendio-anual-de-comercio-exterior-agrario
```

### Método

```text
GET HTML -> extraer PDF/XLS/XLSX/ZIP de anuarios -> descargar año necesario -> leer tablas
```

### Años con enlaces detectados

```text
2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025
```

### Uso

Contraste agregado por año, subpartida, país destino, valor y peso.

## SISAP MIDAGRI

### URL

```text
https://sistemas.midagri.gob.pe/sisap/portal/
```

### Resultado técnico

La consulta con `requests` falló por handshake SSL:

```text
SSLError: SSLV3_ALERT_HANDSHAKE_FAILURE
```

### Parámetro recomendado

```yaml
metodo_recomendado: "browser/Selenium/Playwright o descarga manual supervisada"
fallback: "reportes gob.pe del Gran Mercado Mayorista de Lima"
```

## SENAMHI - estaciones y descarga

### URLs

```text
https://www.senamhi.gob.pe/site/descarga-datos/
https://www.senamhi.gob.pe/servicios/?p=estaciones
```

### Parámetros detectados

Página de estaciones por departamento:

```text
https://www.senamhi.gob.pe/servicios/main.php?dp=ica&p=estaciones
https://www.senamhi.gob.pe/servicios/main.php?dp=la-libertad&p=estaciones
https://www.senamhi.gob.pe/servicios/main.php?dp=piura&p=estaciones
https://www.senamhi.gob.pe/servicios/main.php?dp=arequipa&p=estaciones
https://www.senamhi.gob.pe/servicios/main.php?dp=lima&p=estaciones
```

Página de descarga detectada:

```text
https://www.senamhi.gob.pe/site/descarga-datos/map_hist_data.php
```

### Método recomendado

```text
1. Raspar estaciones por departamento.
2. Seleccionar estaciones cercanas a zonas productoras.
3. Usar descarga oficial con credenciales si el sistema lo exige.
4. Guardar fuente_clima = SENAMHI.
```

## NASA POWER

### Endpoint patrón

```text
https://power.larc.nasa.gov/api/temporal/daily/point?parameters={PARAMS}&community=AG&longitude={LON}&latitude={LAT}&start={YYYYMMDD}&end={YYYYMMDD}&format=JSON
```

### Parámetros probados

```yaml
parameters:
  - T2M_MAX
  - T2M_MIN
  - PRECTOTCORR
  - RH2M
  - ALLSKY_SFC_SW_DWN
community: "AG"
format: "JSON"
sample_coordinate:
  zona: "Ica"
  longitude: -75.73
  latitude: -14.07
sample_start: "20250101"
sample_end: "20250110"
```

### Coordenadas proxy recomendadas

```yaml
Ica: {latitude: -14.07, longitude: -75.73}
La_Libertad: {latitude: -8.10, longitude: -79.03}
Piura: {latitude: -5.20, longitude: -80.63}
Arequipa: {latitude: -16.40, longitude: -71.54}
Lima: {latitude: -12.05, longitude: -77.04}
```

## APN - tráfico portuario

### URLs

```text
https://www.gob.pe/institucion/apn/informes-publicaciones/6573509-estadisticas-apn-2025-trafico-de-carga
https://www.gob.pe/institucion/apn/informes-publicaciones/5425311-estadisticas-apn-2024-trafico-de-carga
```

### Método

```text
GET HTML -> extraer enlaces PDF/XLSX -> descargar "resumen del movimiento de carga" mensual
```

### Tipos de archivos detectados por mes

```text
movimiento de contenedores = PDF
movimiento de carga = PDF
resumen del movimiento de carga = XLSX
```

### Variables objetivo

```text
fecha_mes
puerto
terminal
carga_ton
contenedores_teu
naves_atendidas
indice_presion_portuaria
```

## OSITRAN / PNDA

### URL Gob.pe

```text
https://www.gob.pe/104704-acceder-a-datos-abiertos-de-puertos-del-ositran-en-la-plataforma-nacional-de-datos-abiertos-pnda
```

### URL PNDA detectada

```text
https://www.datosabiertos.gob.pe/search/field_tags/puertos-623/type/dataset?query=OSITRAN&sort_by=changed&sort_order=DESC
```

### Filtros detectados

```text
field_topic/transporte-25
field_tags/ositran-193
field_resources%253Afield_format/csv-14
field_resources%253Afield_format/xlsx-39
```

### Datasets relevantes detectados

```text
indicadores-mensuales-trafico-...-ene-2019-dic-2025
indicadores-mensuales-ingresos-...-ene-2019-dic-2025
variables-de-trafico-en-puertos-2009-2017
```

## SENASA

### Certificado fitosanitario

```text
https://www.gob.pe/10093-obtener-certificado-fitosanitario-de-exportacion-o-reexportacion-de-plantas-productos-vegetales-y-otros-articulos-reglamentados
```

### Requisitos sanitarios y fitosanitarios

```text
https://www.gob.pe/10950-consultar-los-requisitos-sanitarios-y-fitosanitarios-para-el-comercio-exterior
https://servicios.senasa.gob.pe/consultaRequisitos/consultarRequisitos.action
```

### Método recomendado

```text
GET Gob.pe -> seguir enlace a aplicativo SENASA -> scrape/automatización controlada por producto-destino.
```

Uso: normativa producto-destino. No representa rechazo real por DUA.

## FDA Import Refusals

### URL

```text
https://www.fda.gov/industry/fda-import-process/import-refusals
```

### Reporte detectado

```text
http://www.accessdata.fda.gov/scripts/ImportRefusals/ir_index.cfm
```

### Parámetros de búsqueda posteriores

```yaml
country_area: "Peru"
products:
  - avocado
  - grapes
  - blueberries
  - asparagus
use: "validacion_externa"
```

## RASFF

### URL

```text
https://food.ec.europa.eu/food-safety/rasff_en
```

### Aplicativo detectado

```text
https://webgate.ec.europa.eu/rasff-window/screen/search
```

### Parámetros recomendados

```yaml
origin_country: "Peru"
product_categories:
  - fruits and vegetables
date_start: "2020-01-01"
date_end: "2026-06-07"
use: "validacion_externa"
```

## INEI microdatos

### URL

```text
https://proyectos.inei.gob.pe/microdatos/
```

### Resultado técnico

La página responde, pero la extracción de ENA probablemente requiere interacción con formulario o parámetros de consulta específicos.

### Método recomendado

```text
Automatizar formulario o usar URL directa de consulta cuando se identifiquen cmbTrimestre, cmbanno y cmbencuesta.
```

