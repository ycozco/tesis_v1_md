# Fuentes web y datasets externos

## Nota de búsqueda

Se realizó una búsqueda externa de verificación el 2026-06-07 sobre fuentes oficiales/institucionales relevantes para la tesis. Esta revisión fue documental; no se ejecutó descarga masiva ni scraping adicional desde internet en esta carpeta. Cuando se ejecute scraping o descarga, cada acción debe quedar registrada con URL, fecha, método, archivo de salida y limitaciones.

## Criterios de selección

1. Fuente oficial o institucional.
2. Cobertura compatible con 2018-2026.
3. Posibilidad de API, CSV, XLSX, DBF, ZIP, JSON o descarga trazable.
4. Granularidad útil para producto, partida, país, fecha, clima, puerto o evento sanitario.
5. Separación metodológica entre dato real, proxy, validación externa y dato sintético.

## Registro consolidado de fuentes

| Fuente | URL | Tipo | Método | Uso recomendado | Limitación principal |
|---|---|---|---|---|---|
| SUNAT/Aduanet | https://www.sunat.gob.pe/operatividadaduanera/ | Real observado | ZIP/DBF/web scraping | Microdato de exportación: FOB, peso, partida, destino, aduana. | No contiene merma, calidad, costo logístico ni etiqueta oficial de anomalía. |
| Aduanet bases | http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm | Real observado | Scraping de enlaces ZIP | Descarga de bases definitivas en DBF. | Portal puede cambiar rutas y nombres. |
| BCRP API | https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api | Real observado | API JSON/CSV | Tipo de cambio PEN/USD mensual. | No etiqueta anomalías ni explica transacciones. |
| BCRP PN01207PM | https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json/2018-01/2026-06 | Real observado | API JSON | Serie recomendada para tipo de cambio promedio mensual. | Requiere normalizar nombres de meses. |
| PROMPERÚ Exportemos | https://exportemos.pe/descubre-oportunidades-de-exportacion/estadisticas-de-exportaciones-peruanas | Real contextual | HTML/Next.js JSON | Mercados, fichas de producto, empresas, precios referenciales. | Usar como validación/contexto, no reemplazo de SUNAT. |
| MIDAGRI comercio exterior | https://www.gob.pe/institucion/midagri/informes-publicaciones/2730438-compendio-anual-de-comercio-exterior-agrario | Real agregado | PDF/XLSX/descarga | Contraste por subpartida, país, peso y valor. | Agregado; no reemplaza microdato DUA. |
| SISAP MIDAGRI | https://sistemas.midagri.gob.pe/sisap/portal/ | Real observado | Portal/PDF/HTML | Precio mayorista interno y abastecimiento. | Cobertura variable por producto y mercado. |
| SENAMHI descarga | https://www.senamhi.gob.pe/site/descarga-datos/ | Real observado | Descarga con registro | Temperatura, precipitación y estaciones meteorológicas. | Puede requerir registro; proxy si se cruza por región y no finca. |
| Gob.pe SENAMHI | https://www.gob.pe/es/9312-conocer-los-datos-hidrometeorologicos-del-peru-descargar-los-datos-meteorologicos | Real observado | Portal oficial | Confirma descarga diaria en TXT con año, mes, día, precipitación, temperatura máxima y mínima. | Requiere usuario/contraseña. |
| NASA POWER | https://power.larc.nasa.gov/docs/services/api/temporal/daily/ | Proxy real georreferenciado | API JSON/CSV | Respaldo climático por coordenada. | No mide finca; resolución/proxy. |
| MODIS MOD13Q1 | https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13Q1 | Proxy satelital | Google Earth Engine | NDVI/EVI cada 16 días a 250 m. | Requiere polígonos y control de calidad de píxeles. |
| APN tráfico de carga | https://www.gob.pe/institucion/apn/informes-publicaciones/5425311-estadisticas-apn-2024-trafico-de-carga | Proxy logístico real | XLSX/PDF | Movimiento de carga y contenedores por puerto/mes. | No entrega costo ni retraso por embarque. |
| APN 2025 | https://www.gob.pe/institucion/apn/informes-publicaciones/6573509-estadisticas-apn-2025-trafico-de-carga | Proxy logístico real | XLSX/PDF | Continuidad del tráfico portuario 2025. | Granularidad agregada. |
| PIEP APN | https://piep.apn.gob.pe/datos-online/ | Proxy logístico real | Consulta web | Naves, carga y contenedores. | Puede requerir scraping interactivo. |
| OSITRAN datos puertos | https://www.gob.pe/104704-acceder-a-datos-abiertos-de-puertos-del-ositran-en-la-plataforma-nacional-de-datos-abiertos-pnda | Proxy logístico real | PNDA/CSV | Movimiento de carga, contenedores, naves, ingresos e indicadores operativos. | Datos de terminales concesionados; no necesariamente todo el universo portuario. |
| SENASA certificado | https://www.gob.pe/10093-obtener-certificado-fitosanitario-de-exportacion-o-reexportacion-de-plantas-productos-vegetales-y-otros-articulos-reglamentados | Real normativo | Portal | Sustento de certificación fitosanitaria. | No entrega cumplimiento por DUA masivo. |
| SENASA requisitos | https://www.gob.pe/10950-consultar-los-requisitos-sanitarios-y-fitosanitarios-para-el-comercio-exterior | Real normativo | Portal/consulta | Requisitos por producto y destino. | Normativo, no evento transaccional. |
| FDA Import Refusals | https://www.fda.gov/industry/fda-import-process/import-refusals | Validación externa | Reporte/IRR | Rechazos de importación por país/producto. | No se une directamente con DUA SUNAT. |
| FDA datasets | https://www.fda.gov/about-fda/oii-foia-electronic-reading-room/data-sets | Validación externa | Data dashboard | Import Refusals y otros datasets ORA. | Requiere filtros/descarga específica. |
| RASFF | https://food.ec.europa.eu/food-safety/rasff_en | Validación externa | RASFF Window | Alertas alimentarias públicas, 2020 en adelante. | Resúmenes; no microdato comercial completo. |
| FAOSTAT | https://www.fao.org/faostat/es/ | Real agregado internacional | API/descarga | Producción, rendimiento, contexto agrícola. | Agregado anual. |
| UN Comtrade | https://comtrade.un.org/ | Real agregado internacional | API/descarga | Comercio internacional por HS, país, socio y periodo. | API key/registro y límites. |
| ITC Trade Map | https://www.intracen.org/resources/tools/trade-map | Real agregado internacional | Descarga manual/portal | Valor unitario internacional y mercados. | Posibles restricciones de scraping/términos. |
| World Bank Pink Sheet | https://thedocs.worldbank.org/en/doc/18675f1d1639c7a34d463f59263ba0a2-0050012025/world-bank-commodities-price-data-the-pink-sheet | Real macro internacional | CSV/XLSX | Precios de commodities. | Menos aplicable a palta/uva/arándano; cacao útil solo como contexto excluido. |
| INEI microdatos | https://proyectos.inei.gob.pe/microdatos/ | Real encuesta | Descarga manual | Contexto estructural agrario. | No une directamente con DUA. |

## Variables esperadas por fuente

### SUNAT/Aduanet

```text
dua_key, fecha_numeracion, fecha_embarque, producto, partida_arancelaria,
aduana_codigo, aduana_nombre, pais_destino, fob_usd, peso_neto_kg,
precio_kg_usd, ruc_exportador_si_disponible, empresa_exportadora_si_disponible
```

### BCRP

```text
fecha_mes, tipo_cambio_pen_usd, tc_lag_1, tc_lag_3, variacion_tc_mensual
```

### PROMPERÚ/Exportemos

```text
producto, partida, top_destinos, top_exportadoras, participacion_destino,
participacion_empresa, sector, mercado_objetivo, precios_referenciales
```

### MIDAGRI/SISAP

```text
fecha, producto_sisap, mercado, precio_mayorista_pen_kg,
precio_mayorista_usd_kg, volumen_ingreso_kg, promedio_7_dias
```

### SENAMHI/NASA POWER

```text
fecha, estacion_codigo, estacion_nombre, latitud, longitud,
temp_max_c, temp_min_c, precipitacion_mm, humedad_relativa_pct,
fuente_clima
```

### APN/OSITRAN

```text
fecha_mes, puerto, terminal, contenedores_teu, carga_ton,
naves_atendidas, indice_presion_portuaria
```

### FDA/RASFF

```text
fecha_evento, pais_origen, producto, categoria, razon_rechazo,
riesgo, mercado_destino, fuente_validacion
```

## Matriz real/proxy/sintético recomendada

| Variable | Fuente | Tipo | Uso |
|---|---|---|---|
| Precio FOB/kg | SUNAT | Real observado | Entrenamiento/ranking. |
| Volumen kg | SUNAT | Real observado | Entrenamiento/ranking. |
| Destino | SUNAT | Real observado | Segmentación. |
| Aduana | SUNAT | Real observado | Proxy logístico. |
| Tipo de cambio | BCRP | Real observado | Control macro. |
| Precio mayorista | MIDAGRI/SISAP | Real observado | Calibración de precios. |
| Precio internacional | UN Comtrade/FAOSTAT/Trade Map | Real agregado | Benchmark. |
| Clima | SENAMHI/NASA POWER | Real/proxy | Clima extremo. |
| NDVI/EVI | MODIS | Proxy real | Vigor vegetal. |
| Presión portuaria | APN/OSITRAN | Proxy real | Logística. |
| Requisitos fitosanitarios | SENASA | Real normativo | Riesgo producto-destino. |
| Rechazos externos | FDA/RASFF | Validación externa | Plausibilidad sanitaria. |
| Merma | Sintético calibrado | Sintético | Variable privada. |
| Calidad lote | Sintético calibrado | Sintético | Variable privada. |
| Temperatura contenedor | Sintético calibrado | Sintético | Variable privada. |
| Costo logístico kg | Sintético calibrado | Sintético | Variable privada. |
| Etiqueta anomalía | Reglas + sintético + experto | Mixta | Evaluación controlada. |

