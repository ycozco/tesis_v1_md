# Descarga masiva SISAP MIDAGRI

Fecha de ejecucion: 2026-06-07  
Fuente: `http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/`  
Endpoint usado: `http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrar`

## Alcance

Se ejecuto una descarga mensual para el periodo 2018-2026 sobre las combinaciones confirmadas en SISAP:

| Producto | Codigo SISAP | Mercado | Codigo mercado | Variables |
|---|---:|---|---:|---|
| Palta | 0626 | Mercado mayorista nro 2-frutas | 15011502 | precio_prom, volumen |
| Uva | 0637 | Mercado mayorista nro 2-frutas | 15011502 | precio_prom, volumen |
| Esparrago | 0216 | Gran mercado mayorista de lima | 15011501 | precio_prom, volumen |

## Resultado

| Indicador | Valor |
|---|---:|
| Consultas ejecutadas | 648 |
| Consultas con datos | 612 |
| Consultas sin datos | 36 |
| Consultas con error | 0 |
| Filas consolidadas | 3826 |

Las 36 consultas sin datos corresponden a julio-diciembre de 2026 para los tres productos y dos variables. A la fecha de ejecucion esos meses son posteriores al corte disponible de la fuente.

## Archivos generados

CSV consolidado fechado:

`data_processed/sisap_midagri/sisap_midagri_mensual_2018_2026_2026-06-07.csv`

Manifiestos:

`metadata/sisap_midagri_mensual_manifest_2026-06-07.csv`  
`metadata/sisap_midagri_mensual_manifest_2026-06-07.json`  
`metadata/sisap_midagri_mensual_summary_2026-06-07.json`

HTML crudo descargado recursivamente:

`data_raw/sisap_midagri/massive/{producto}/{variable}/{anio}/{anio-mes}.html`

Script reproducible:

`scripts/download_sisap_massive.py`

## Estructura del CSV

El CSV esta en formato largo. Cada fila representa una observacion mensual por producto, variedad y variable.

Columnas principales:

| Columna | Descripcion |
|---|---|
| fuente | Fuente institucional |
| endpoint | Endpoint consultado |
| fecha_descarga | Fecha local de ejecucion |
| periodicidad | Mensual |
| anio | Año consultado |
| mes | Mes consultado |
| producto | Producto normalizado |
| producto_id | Codigo SISAP del producto |
| mercado | Codigo SISAP del mercado |
| mercado_nombre | Nombre del mercado |
| variable | Variable tecnica consultada |
| variable_label | Etiqueta descriptiva |
| periodo_sisap | Periodo reportado por SISAP |
| variedad | Variedad dentro del producto |
| valor | Valor numerico reportado |
| titulo_reporte | Titulo original del reporte |
| raw_file | Ruta relativa al HTML fuente |

## Control por producto y variable

| Producto | Variable | Filas |
|---|---|---:|
| Palta | precio_prom | 713 |
| Palta | volumen | 713 |
| Uva | precio_prom | 1098 |
| Uva | volumen | 1098 |
| Esparrago | precio_prom | 102 |
| Esparrago | volumen | 102 |

## Pendiente

Arandano aun no queda incorporado porque no aparece como producto directo en los selectores confirmados de SISAP. Debe investigarse dentro de `Otros fruticolas` o con una consulta adicional de variedades/generos antes de ejecutar una descarga equivalente.
