# Plan de supervisión, scraping y ETL

## Regla de trazabilidad

Cada ejecución de scraping, descarga o extracción debe registrar:

```text
fecha_hora
script
fuente_url
metodo
parametros
archivo_salida
filas_obtenidas
hash_o_tamano
errores
limitaciones
```

El registro puede guardarse en:

```text
codex-revision/log-scraping.md
metadata/data_lineage.yml
metadata/data_source_registry.csv
```

## Fase 1 - Corrección de alcance experimental

Objetivo: crear una versión sin cacao y evitar que el sistema siga entrenando o reportando resultados experimentales con cacao.

### Acciones

1. Crear configuración única de productos:

```yaml
products:
  primary:
    palta: "0804400000"
    uva: "0806100000"
    arandano: "0810400000"
  secondary:
    esparrago: "0709200000"
  excluded:
    cacao:
      hs_code: "1801001900"
      reason: "Baja representatividad muestral en dataset real consolidado: 379 registros."
```

2. Modificar o parametrizar:

```text
src/etl_real_data.py
src/build_real_dataset.py
src/generate_synthetic_dataset.py
src/summarize_scraped_data.py
src/segment_datasets.py
limpieza_de_datos_y_normalizacion/preprocess_data.py
scripts/run_experiments.py
```

3. Generar salidas:

```text
data/real/dataset_real_v1_1_no_cacao.csv
data/real/dataset_real_primary.csv
data/real/dataset_real_secondary_esparrago.csv
data/real_processed/esparrago/dataset_esparrago_raw.csv
data/synthetic/synthetic_agroexport_v2_calibrated_no_cacao.csv
```

4. Generar reportes:

```text
reports/data_audit/product_distribution_no_cacao.md
reports/data_audit/exclusion_cacao_justification.md
reports/data_audit/data_quality_by_product.md
```

## Fase 2 - SUNAT/Aduanet

Objetivo: consolidar microdatos reales de exportación.

### Procedimiento

1. Usar `src/scrape_sunat_all.py` o versión mejorada.
2. Acceder a la página de bases:

```text
http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm
```

3. Extraer enlaces `.zip`.
4. Descargar solo a:

```text
data/sunat/raw_downloads/
```

5. Extraer DBF con Python local.
6. Filtrar partidas:

```text
palta: 0804400000
uva: 0806100000
arandano: 0810400000
esparrago: 0709200000
cacao: excluir 1801001900
```

7. Construir clave DUA:

```text
dua_key = CADU + FANO + NDCL + NSER
```

8. Deduplicar conservando el registro más completo o más reciente.

### Controles

```text
n_registros
fecha_min
fecha_max
fob_total
peso_total
precio_kg_p05
precio_kg_p50
precio_kg_p95
top_destinos
top_aduanas
duplicados_dua_key
nulos_por_columna
```

## Fase 3 - BCRP

Objetivo: incorporar tipo de cambio real observado.

Endpoint:

```text
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json/2018-01/2026-06
```

Salida:

```text
data/raw/bcrp/exchange_rates.json
data/processed/bcrp_exchange_monthly.csv
```

Merge:

```text
fecha SUNAT -> mes -> tipo_cambio_pen_usd
```

## Fase 4 - PROMPERÚ/Exportemos

Objetivo: validar mercados, empresas, tendencias y precios referenciales.

URLs por producto:

```text
https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0804400000
https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0806100000
https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0810400000
https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0709200000
```

Método:

1. Descargar HTML.
2. Extraer `<script id="__NEXT_DATA__" type="application/json">`.
3. Guardar JSON crudo por producto.
4. Parsear mercados y empresas.

Uso: validación contextual, no base operacional principal.

## Fase 5 - MIDAGRI/SISAP y comercio exterior agrario

Objetivo: precios internos y contraste agregado.

Procedimiento:

1. Descargar compendios y/o archivos XLSX/PDF.
2. Extraer tablas de comercio exterior agrario.
3. Descargar o raspar precios mayoristas SISAP.
4. Convertir precios PEN/kg a USD/kg con BCRP.
5. Crear:

```text
ratio_fob_vs_mayorista = precio_kg_usd / precio_mayorista_usd_kg
```

## Fase 6 - Clima

Prioridad:

1. SENAMHI si hay estación y periodo disponibles.
2. NASA POWER si SENAMHI no cubre fecha/zona.

Zonas iniciales:

```text
Ica
La Libertad
Piura
Arequipa
Lima
```

Variables:

```text
temp_max_7d
temp_max_30d
precip_7d
precip_30d
anomalia_temp_mes
anomalia_precip_mes
fuente_clima
```

Declaración obligatoria: si se cruza por región o aduana, se trata como proxy regional, no clima de finca.

## Fase 7 - APN/OSITRAN

Objetivo: índice de presión portuaria.

Variables:

```text
contenedores_teu
carga_ton
naves_atendidas
indice_presion_portuaria
```

Fórmula inicial:

```text
indice_presion_portuaria =
  zscore(contenedores_teu) +
  zscore(carga_ton) +
  zscore(naves_atendidas)
```

Cruce:

```text
aduana -> puerto_probable
fecha -> mes
```

## Fase 8 - FDA/RASFF/SENASA

Objetivo: validar plausibilidad sanitaria y fitosanitaria.

Uso correcto:

- SENASA: requisitos normativos producto-destino.
- FDA: rechazos de importación hacia EEUU.
- RASFF: alertas alimentarias UE desde 2020.

Uso incorrecto:

- No unir como si fueran rechazos oficiales por DUA SUNAT.
- No declarar cumplimiento fitosanitario real por embarque si no existe microdato público.

## Fase 9 - Dataset sintético calibrado

Objetivo: modelar variables privadas no públicas.

Variables sintéticas permitidas:

```text
merma_pct
calidad_lote_score
temperatura_contenedor_simulada
costo_logistico_usd_kg
cumplimiento_fitosanitario_simulado
etiqueta_anomalia
tipo_anomalia
regla_inyeccion
```

Productos:

```text
palta
uva
arandano
esparrago
```

Excluir:

```text
cacao
```

## Entregable final esperado

```text
data/enriched/dataset_real_v1_2_enriched_no_cacao.csv
data/synthetic/synthetic_agroexport_v2_calibrated_no_cacao.csv
reports/data_audit/enrichment_coverage_report.md
reports/data_audit/synthetic_datasheet_v2.md
metadata/data_source_registry.csv
metadata/data_lineage.yml
```

