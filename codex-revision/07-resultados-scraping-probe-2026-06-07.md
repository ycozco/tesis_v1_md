# Resultados del scraping probe

Fecha de ejecución: 2026-06-07  
Entorno: `d:\tesis_yoset\.venv\Scripts\python.exe`  
Propósito: verificar accesibilidad, parámetros reales y estrategia de extracción para el plan de scraping/ETL.

## Resumen de resultados

| Fuente | Estado | Resultado |
|---|---:|---|
| SUNAT/Aduanet bases | 200 | Página accesible; 55 enlaces; se detectaron ZIP y XLS. |
| BCRP API PN01207PM | 200 | JSON accesible; 101 periodos entre Ene.2018 y May.2026. |
| PROMPERÚ Exportemos | 200 | Las 4 fichas tienen `__NEXT_DATA__`; 11 mercados, 11 empresas y 12 precios por producto. |
| MIDAGRI compendio | 200 | Página accesible; detectados PDF/XLS/XLSX/ZIP de 2018 a 2025. |
| SISAP | Bloqueo SSL | `requests` falla por handshake; requiere navegador/Playwright/Selenium o descarga manual. |
| SENAMHI descarga | 200 | Página accesible; detectado `map_hist_data.php`. |
| SENAMHI estaciones | 200 | Página accesible; detectados enlaces por departamento. |
| NASA POWER | 200 | API JSON accesible; muestra diaria con 5 parámetros y 10 días. |
| APN 2025 | 200 | Página accesible; detectados XLSX/PDF mensuales. |
| APN 2024 | 200 | Página accesible; detectados XLSX/PDF mensuales. |
| OSITRAN Gob.pe | 200 | Página accesible; enlace a PNDA detectado. |
| PNDA OSITRAN | 200 | Búsqueda accesible; datasets de tráfico/ingresos 2019-2025 detectados. |
| SENASA certificado | 200 | Página accesible; enlace a VUCE detectado. |
| SENASA requisitos | 200 | Página accesible; enlace a aplicativo `consultaRequisitos` detectado. |
| FDA Import Refusals | 200 | Página accesible; enlace a IRR detectado. |
| FDA datasets | 200 | Página accesible; confirma sección de datasets/import refusals. |
| RASFF | 200 | Página accesible; enlace a RASFF Window detectado. |
| INEI microdatos | 200 | Página accesible; requiere parámetros/formulario para ENA. |

## SUNAT/Aduanet

URL consultada:

```text
http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm
```

Resultado:

- HTTP 200.
- 55 enlaces detectados.
- Enlaces relevantes detectados:

```text
totales_2011.xls
estructura_bases.xls
x23290326.zip
ma23290326.zip
mb23290326.zip
idv23290326.zip
mam23290326.zip
x30050426.zip
ma30050426.zip
mb30050426.zip
idv30050426.zip
mam30050426.zip
x06120426.zip
ma06120426.zip
mb06120426.zip
idv06120426.zip
```

Interpretación:

`x*.zip` es el patrón prioritario para exportaciones. Se debe normalizar la URL porque la página devuelve rutas con barras invertidas y dobles segmentos.

## BCRP

Endpoint consultado:

```text
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json/2018-01/2026-06
```

Resultado:

```text
status: 200
periodos: 101
primer_periodo: Ene.2018 = 3.21490952380952
ultimo_periodo_disponible: May.2026 = 3.435275
```

Interpretación:

Aunque se pidió hasta 2026-06, al 2026-06-07 el último valor mensual disponible en la API fue mayo de 2026. Esto es esperable porque junio aún no está cerrado.

## PROMPERÚ Exportemos

URLs consultadas:

```text
0804400000 palta
0806100000 uva
0810400000 arandano
0709200000 esparrago
```

Resultado por producto:

| Producto | HTTP | `__NEXT_DATA__` | Mercados | Empresas | Precios |
|---|---:|---|---:|---:|---:|
| palta | 200 | Sí | 11 | 11 | 12 |
| uva | 200 | Sí | 11 | 11 | 12 |
| arándano | 200 | Sí | 11 | 11 | 12 |
| espárrago | 200 | Sí | 11 | 11 | 12 |

Claves JSON detectadas:

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

Interpretación:

PROMPERÚ es muy viable para scraping estructurado. Debe guardarse JSON crudo y CSV limpio por producto.

## MIDAGRI comercio exterior agrario

URL consultada:

```text
https://www.gob.pe/institucion/midagri/informes-publicaciones/2730438-compendio-anual-de-comercio-exterior-agrario
```

Resultado:

- HTTP 200.
- 61 enlaces.
- Archivos detectados para 2018-2025.

Enlaces clave:

```text
2730438-compendio-del-anuario-comercio-exterior-agrario-2025.pdf
2730438-cuadros-en-excel-del-anuario-comercio-exterior-agrario-2025.xlsx
2730438-compendio-del-anuario-comercio-exterior-agrario-2024.pdf
2730438-cuadros-en-excel-del-anuario-comercio-exterior-agrario-2024.zip
2730438-compendio-del-anuario-comercio-exterior-agrario-2023.pdf
2730438-compendio-del-anuario-comercio-exterior-agrario-2022.pdf
2730438-cuadros-en-excel-del-anuario-comercio-exterior-agrario-2022.xlsx
Cuadros en Excel del anuario COMERCIO EXTERIOR AGRARIO 2021.xlsx
Cuadros en Excel del anuario COMERCIO EXTERIOR AGRARIO 2020.xlsx
Cuadros en Excel del anuario COMERCIO EXTERIOR AGRARIO 2019.xls
Cuadros en Excel del anuario COMERCIO EXTERIOR AGRARIO 2018.xls
```

Interpretación:

MIDAGRI es viable para contraste agregado anual, especialmente por subpartida y país.

## SISAP

URL consultada:

```text
https://sistemas.midagri.gob.pe/sisap/portal/
```

Resultado:

```text
SSLError: SSLV3_ALERT_HANDSHAKE_FAILURE
```

Interpretación:

No conviene depender de `requests` simple para SISAP. Usar navegador automatizado o descarga manual supervisada. También se puede usar Gob.pe de reportes del Gran Mercado Mayorista como respaldo.

## SENAMHI

URLs consultadas:

```text
https://www.senamhi.gob.pe/site/descarga-datos/
https://www.senamhi.gob.pe/servicios/?p=estaciones
```

Resultado:

- Descarga datos: HTTP 200, 127 enlaces.
- Estaciones: HTTP 200, 47 enlaces.
- Se detectó:

```text
https://www.senamhi.gob.pe/site/descarga-datos/map_hist_data.php
```

Enlaces por departamento detectados:

```text
dp=arequipa&p=estaciones
dp=ica&p=estaciones
dp=la-libertad&p=estaciones
dp=lima&p=estaciones
```

Interpretación:

SENAMHI es viable para inventario de estaciones. La descarga histórica puede requerir registro/credenciales; se debe documentar si se usa NASA POWER como fallback.

## NASA POWER

Endpoint de prueba:

```text
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN&community=AG&longitude=-75.73&latitude=-14.07&start=20250101&end=20250110&format=JSON
```

Resultado:

```text
status: 200
parameters: T2M_MAX, T2M_MIN, PRECTOTCORR, RH2M, ALLSKY_SFC_SW_DWN
days_per_parameter: 10
```

Interpretación:

NASA POWER queda listo como fallback climático por coordenada. Para producción se debe ejecutar por zona y periodo completo.

## APN

URLs consultadas:

```text
https://www.gob.pe/institucion/apn/informes-publicaciones/6573509-estadisticas-apn-2025-trafico-de-carga
https://www.gob.pe/institucion/apn/informes-publicaciones/5425311-estadisticas-apn-2024-trafico-de-carga
```

Resultado:

| Año | HTTP | Enlaces | Evidencia |
|---|---:|---:|---|
| 2025 | 200 | 103 | PDF de contenedores/carga y XLSX de resumen mensual. |
| 2024 | 200 | 101 | PDF de contenedores/carga y XLSX de resumen mensual. |

Ejemplo 2025:

```text
resumen-del-movimiento-de-carga-en-los-terminales-portuarios-de-uso-publico-enero-2025.xlsx
resumen-del-movimiento-de-carga-en-los-terminales-portuarios-de-uso-publico-febrero-2025.xlsx
resumen-del-movimiento-de-carga-en-los-terminales-portuarios-de-uso-publico-marzo-2025.xlsx
resumen-del-movimiento-de-carga-en-los-terminales-portuarios-de-uso-publico-abril-2025.xlsx
resumen-del-movimiento-de-carga-en-los-terminales-portuarios-de-uso-publico-mayo-2025.xlsx
```

Interpretación:

APN es viable para descarga XLSX mensual. Conviene extraer resúmenes XLSX antes que PDFs.

## OSITRAN / PNDA

URLs consultadas:

```text
https://www.gob.pe/104704-acceder-a-datos-abiertos-de-puertos-del-ositran-en-la-plataforma-nacional-de-datos-abiertos-pnda
https://www.datosabiertos.gob.pe/search/field_tags/puertos-623/type/dataset?query=OSITRAN&sort_by=changed&sort_order=DESC
```

Resultado:

- Gob.pe: HTTP 200, enlace a PNDA detectado.
- PNDA: HTTP 200, 64 enlaces.
- Filtros detectados:

```text
CSV: field_resources%253Afield_format/csv-14
XLSX: field_resources%253Afield_format/xlsx-39
Transporte: field_topic/transporte-25
```

Datasets detectados:

```text
indicadores-mensuales-trafico-msctcatpptps-ene-2019-dic-2025
indicadores-mensuales-trafico-apmtnty-ene-2019-dic-2025
indicadores-mensuales-trafico-matpai-ene-2019-dic-2025
variables-de-trafico-en-puertos-2009-2017
```

Interpretación:

OSITRAN es buen complemento a APN, especialmente para terminales concesionados y series 2019-2025.

## SENASA

URLs consultadas:

```text
https://www.gob.pe/10093-obtener-certificado-fitosanitario-de-exportacion-o-reexportacion-de-plantas-productos-vegetales-y-otros-articulos-reglamentados
https://www.gob.pe/10950-consultar-los-requisitos-sanitarios-y-fitosanitarios-para-el-comercio-exterior
```

Resultado:

- Certificado: HTTP 200, 32 enlaces.
- Requisitos: HTTP 200, 24 enlaces.
- Enlaces operativos detectados:

```text
https://authorize.vuce.gob.pe/public/login-options/mercancias-restringidas
https://servicios.senasa.gob.pe/consultaRequisitos/consultarRequisitos.action
```

Interpretación:

SENASA sirve como fuente normativa/procedimental. No entrega rechazo público por DUA.

## FDA

URLs consultadas:

```text
https://www.fda.gov/industry/fda-import-process/import-refusals
https://www.fda.gov/about-fda/oii-foia-electronic-reading-room/data-sets
```

Resultado:

- Import Refusals: HTTP 200.
- Data Sets: HTTP 200.
- Enlace de reporte detectado:

```text
http://www.accessdata.fda.gov/scripts/ImportRefusals/ir_index.cfm
```

Interpretación:

FDA es viable como validación externa de rechazos para EEUU, por país/producto, sin unión directa por DUA.

## RASFF

URL consultada:

```text
https://food.ec.europa.eu/food-safety/rasff_en
```

Resultado:

- HTTP 200.
- Enlace detectado:

```text
https://webgate.ec.europa.eu/rasff-window/screen/search
```

Interpretación:

RASFF requiere automatizar búsqueda en RASFF Window. Es fuente de validación externa, no microdato DUA.

## INEI

URL consultada:

```text
https://proyectos.inei.gob.pe/microdatos/
```

Resultado:

- HTTP 200.
- La página base carga, pero el acceso a ENA requiere parámetros de formulario.

Interpretación:

INEI debe tratarse como descarga manual/automatizada por formulario. Útil para contexto estructural agrícola, no para anomalía por embarque.

## Próxima ejecución recomendada

1. Descargar y normalizar SUNAT `x*.zip`.
2. Generar `dataset_real_v1_1_no_cacao.csv`.
3. Descargar BCRP completo a JSON/CSV.
4. Raspar PROMPERÚ por las 4 partidas permitidas.
5. Descargar MIDAGRI Excel 2018-2025.
6. Descargar APN XLSX 2024-2025.
7. Descargar OSITRAN CSV/XLSX por terminal.
8. Ejecutar NASA POWER para coordenadas proxy.
9. Dejar SISAP, SENASA interactivo, FDA IRR, RASFF e INEI como módulos con Playwright/Selenium o descarga manual supervisada.

