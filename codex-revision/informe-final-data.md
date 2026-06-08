# Informe final de datos y relacion con la tesis

Fecha de revision: 2026-06-07  
Workspace local: `D:\tesis_yoset`  
Carpeta de supervision Codex: `D:\tesis_yoset\codex-revision`  
Archivo: `codex-revision/informe-final-data.md`

## 1. Proposito del informe

Este informe consolida el estado de los datasets disponibles para la tesis, describe la ruta local de cada fuente, explica que aporta cada archivo y relaciona directamente cada bloque de datos con el trabajo de investigacion.

La tesis trabaja sobre agroexportaciones peruanas y uso de IA explicable/anomalias para evaluar desempeno, riesgo o comportamiento operativo de productos agroexportadores. Por eso los datos no deben verse solo como archivos sueltos: cada fuente debe cumplir una funcion dentro del marco metodologico.

La organizacion recomendada es:

| Nivel de informacion | Fuente principal | Rol en la tesis |
|---|---|---|
| Microdato de exportacion | SUNAT/ADUANET, dataset real local | Base observacional para modelamiento. |
| Benchmark internacional | Trade Map | Comparacion por mercado destino y posicion comercial. |
| Mercado interno | SISAP/MIDAGRI | Contexto de precio y volumen mayorista interno. |
| Macroeconomia | BCRP | Control por tipo de cambio. |
| Clima/agroclima | NASA POWER, SENAMHI, NDVI | Proxy de condiciones productivas. |
| Logistica | APN, OSITRAN | Proxy de presion portuaria/carga/contenedores. |
| Sanidad/inocuidad | SENASA, FDA, RASFF | Proxy de riesgo fitosanitario o alertas comerciales. |
| Contexto sectorial | MIDAGRI, FAOSTAT, World Bank | Validacion externa, marco descriptivo y discusion. |

## 2. Relacion directa con la tesis

### 2.1 Pregunta metodologica que deben sostener los datos

La base de datos debe permitir responder, como minimo:

1. Que productos agroexportadores peruanos presentan mayor variabilidad, riesgo o comportamiento anomalo.
2. Que variables explican mejor dichos comportamientos: volumen, precio, destino, tipo de cambio, clima, logistica, mercado interno o indicadores externos.
3. Que tan confiables son las alertas o predicciones generadas por el modelo.
4. Como justificar los resultados con fuentes reales y trazables.

### 2.2 Productos objetivo

Productos recomendados como nucleo:

| Producto | Estado local | Justificacion para tesis |
|---|---|---|
| Palta | Alta cobertura local y Trade Map disponible. | Producto fuerte de agroexportacion peruana; permite estudiar precio, volumen, destino y competencia. |
| Uva | Alta cobertura local y Trade Map disponible. | Producto de alta relevancia exportadora; util para analisis de estacionalidad y mercados destino. |
| Arandano | Cobertura local menor, Trade Map disponible. | Producto estrategico de crecimiento reciente; importante para tesis aunque SISAP no lo cubra directamente. |

Producto secundario:

| Producto | Estado local | Decision recomendada |
|---|---|---|
| Esparrago | Presente en dataset real, Trade Map y SISAP. | Puede usarse como producto comparativo o ampliar el estudio si se normaliza bien. |

Producto a excluir:

| Producto | Motivo |
|---|---|
| Cacao | Solo 379 filas en `dataset_real_v1.csv`; baja representatividad y no corresponde al foco principal detectado. |

### 2.3 Como entra cada fuente en la tesis

| Fuente | Capitulo o seccion donde aporta | Funcion |
|---|---|---|
| Dataset real local | Metodologia, experimentos, resultados | Base de entrenamiento/prueba. |
| SUNAT/ADUANET | Metodologia, validacion de datos | Fuente primaria de exportaciones. |
| Trade Map | Marco contextual, analisis de mercados, validacion externa | Benchmark por destino y posicion competitiva. |
| SISAP/MIDAGRI | Variables complementarias, contexto interno | Precio y volumen mayorista local. |
| BCRP | Variables de control macroeconomico | Tipo de cambio. |
| NASA/SENAMHI/NDVI | Variables exogenas | Condiciones climaticas o productivas. |
| APN/OSITRAN | Variables logisticas | Proxy de congestion, carga o capacidad portuaria. |
| SENASA/FDA/RASFF | Variables de riesgo | Alertas, rechazos o contexto sanitario. |
| MIDAGRI/FAOSTAT/World Bank | Marco teorico/descriptivo | Comparacion sectorial y soporte documental. |

## 3. Rutas locales principales

| Ruta local | Descripcion | Uso recomendado |
|---|---|---|
| `D:\tesis_yoset\data` | Datos base del proyecto. | No sobrescribir sin versionar; contiene datasets reales, sinteticos y procesados. |
| `D:\tesis_yoset\data-trademap` | Descargas manuales desde Trade Map. | Convertir los `.xls` utiles a CSV limpio. |
| `D:\tesis_yoset\codex-revision` | Auditoria, documentacion y descargas Codex. | Carpeta de supervision y trazabilidad. |
| `D:\tesis_yoset\codex-revision\data_raw` | Descargas crudas por fuente. | Mantener como evidencia original. |
| `D:\tesis_yoset\codex-revision\data_processed` | Datos limpios derivados. | Usar para integracion y modelamiento. |
| `D:\tesis_yoset\codex-revision\metadata` | Manifiestos de descarga y resumenes. | Usar en anexos metodologicos. |
| `D:\tesis_yoset\codex-revision\scripts` | Scripts reproducibles. | Reejecutar o auditar descargas. |

## 4. Dataset maestro local

### 4.1 Archivo principal

Ruta: `D:\tesis_yoset\data\dataset_real_v1.csv`  
Formato: CSV  
Filas: 40,672  
Columnas: 21

Este archivo es la base local mas importante para la tesis porque ya integra registros por producto con variables comerciales, logisticas, climaticas y de anomalia. Debe tratarse como dataset experimental inicial, pero todavia requiere trazabilidad variable por variable.

### 4.2 Distribucion por producto

| Producto | Filas | Uso en tesis | Decision |
|---|---:|---|---|
| Palta | 17,360 | Producto nucleo. | Mantener. |
| Uva | 15,701 | Producto nucleo. | Mantener. |
| Arandano | 4,633 | Producto nucleo, aunque con menor cobertura. | Mantener y reforzar con SUNAT/Trade Map. |
| Esparrago | 2,599 | Producto secundario/comparativo. | Mantener solo si se normaliza. |
| Cacao | 379 | No corresponde al nucleo. | Excluir del modelo final. |

### 4.3 Columnas y relacion con variables de investigacion

| Columna | Tipo metodologico | Relacion con la tesis | Riesgo o cuidado |
|---|---|---|---|
| `id` | Tecnica | Identificador del registro. | No usar como predictor. |
| `fecha` | Temporal | Permite construir estacionalidad, mes, tendencia y cortes train/test. | Validar formato y rango. |
| `producto` | Categorica clave | Define el grupo de analisis. | Homologar nombres: arandano/arandano, esparrago/esparrago. |
| `partida_arancelaria` | Comercial | Conecta con SUNAT, Trade Map y Comtrade. | Verificar HS correcto por producto. |
| `empresa_exportadora` | Comercial | Puede explicar concentracion o patrones operativos. | Evaluar anonimizar si se publica. |
| `zona` | Geografica | Relaciona produccion con clima/logistica. | Validar si es zona productiva o administrativa. |
| `volumen_kg` | Variable objetivo/explicativa | Mide escala exportadora y puede asociarse a anomalias. | Comparar con SUNAT. |
| `precio_kg_usd` | Variable comercial | Permite detectar variaciones de precio o outliers. | Verificar calculo FOB/peso. |
| `destino_mercado` | Comercial | Relaciona comportamiento con mercado internacional. | Homologar paises con Trade Map. |
| `dias_logisticos` | Operativa | Puede explicar riesgo, merma o retrasos. | Confirmar si es observado o simulado. |
| `costo_logistico_usd_kg` | Operativa | Variable explicativa para desempeno/costo. | Confirmar fuente; si es proxy, declararlo. |
| `cumplimiento_fitosanitario` | Riesgo | Puede vincularse a alertas o rechazos. | No afirmar que es por embarque si no hay fuente directa. |
| `merma_pct` | Riesgo/productividad | Relacionada con calidad, clima y logistica. | Alta sospecha de variable sintetica/proxy. |
| `tipo_cambio_pen_usd` | Macroeconomica | Control por condiciones macro. | Debe validarse con BCRP. |
| `temperatura_max_c` | Climatica | Proxy de estres climatico. | Definir region y agregacion temporal. |
| `temperatura_min_c` | Climatica | Proxy de condiciones productivas. | No usar como dato de contenedor. |
| `precipitacion_mm` | Climatica | Explica productividad/calidad. | Requiere fuente regional. |
| `humedad_pct` | Climatica | Puede explicar deterioro/riesgo. | Verificar origen. |
| `etiqueta_anomalia` | Target/modelo | Variable de clasificacion o evaluacion. | Definir si fue observada o inyectada. |
| `tipo_anomalia` | Target/modelo | Permite clasificar clase de anomalia. | Revisar reglas de construccion. |
| `regla_inyeccion` | Trazabilidad sintetica | Indica generacion artificial de anomalias. | Separar claramente de datos reales. |

### 4.4 Implicacion para la tesis

Este dataset permite ejecutar experimentos de IA, pero para una defensa academica no basta con reportar metricas. Debe mostrarse:

- Cuales variables vienen de fuentes reales.
- Cuales son proxies agregados.
- Cuales fueron sintetizadas o calibradas.
- Como se evita fuga de informacion entre entrenamiento y prueba.
- Como se justifica la etiqueta de anomalia.

La tesis debe declarar que el dataset final es una integracion de fuentes publicas y variables derivadas, no necesariamente un registro oficial unico a nivel embarque.

## 5. Datasets procesados locales

Rutas:

| Ruta | Descripcion | Relacion con tesis |
|---|---|---|
| `data/dataset_processed_train_raw.csv` | Entrenamiento sin balanceo. | Sirve para evaluar desempeno real con distribucion original. |
| `data/dataset_processed_train_balanced.csv` | Entrenamiento balanceado. | Sirve para manejar desbalance de anomalias. |
| `data/dataset_processed_test.csv` | Prueba. | Debe permanecer fuera del ajuste del modelo. |
| `data/real_processed/` | Procesados desde datos reales. | Base preferida para resultados principales. |
| `data/synthetic_processed/` | Procesados sinteticos. | Usar solo para comparacion o robustez, no como evidencia principal. |

Subcarpetas por producto:

| Producto | Ruta | Estado |
|---|---|---|
| Arandano | `data/real_processed/arandano` | Existe. |
| Palta | `data/real_processed/palta` | Existe. |
| Uva | `data/real_processed/uva` | Existe. |
| Esparrago | No encontrada como subcarpeta especifica | Pendiente si se incluye. |

Relacion con la tesis:

- Estas particiones sostienen el capitulo experimental.
- Deben acompanarse con tabla de conteos, distribucion de clases y productos.
- Se recomienda reportar resultados separados por producto, no solo promedio global.

## 6. Trade Map

Ruta: `D:\tesis_yoset\data-trademap`  
Formato externo: `.xls`  
Formato interno observado: HTML exportado como Excel  
Documentacion local: `D:\tesis_yoset\data-trademap\README_renombrado.md`  
Manifiesto: `D:\tesis_yoset\data-trademap\rename_manifest_trademap.json`

### 6.1 Rol de Trade Map en la tesis

Trade Map no debe reemplazar los microdatos SUNAT. Su mejor uso es como benchmark internacional:

- Identificar principales mercados importadores de productos peruanos.
- Comparar participacion de Peru por destino.
- Analizar crecimiento 2021-2025.
- Validar si los destinos del dataset local coinciden con mercados comercialmente relevantes.
- Justificar la importancia economica de palta, uva, arandano y esparrago.

En la tesis puede aparecer en:

| Seccion | Uso |
|---|---|
| Planteamiento del problema | Evidencia de relevancia internacional de productos. |
| Marco contextual | Mercados destino y competitividad. |
| Metodologia | Fuente externa de validacion y variables agregadas. |
| Resultados descriptivos | Ranking de mercados, crecimiento y participacion. |
| Discusion | Comparacion entre patrones del modelo y posicion comercial externa. |

### 6.2 Archivos utiles de exportacion

| Archivo | HS | Producto | Vista | Variable/uso principal |
|---|---|---|---|---|
| `export_indicadores_2025_hs070920_esparrago.xls` | 070920 | Esparrago | Indicadores 2025 | Mercados destino, valor exportado, cantidad, participacion, crecimiento, arancel. |
| `export_indicadores_2025_hs080440_palta.xls` | 080440 | Palta | Indicadores 2025 | Mercados destino y desempeno competitivo. |
| `export_indicadores_2025_hs080610_uva.xls` | 080610 | Uva | Indicadores 2025 | Mercados destino y crecimiento. |
| `export_indicadores_2025_hs081040_arandano.xls` | 081040 | Arandano | Indicadores 2025 | Mercados destino para producto clave no cubierto por SISAP. |
| `export_serie_anual_2021_2025_hs070920_esparrago.xls` | 070920 | Esparrago | Serie anual | Evolucion anual 2021-2025. |
| `export_serie_anual_2021_2025_hs080440_palta.xls` | 080440 | Palta | Serie anual | Evolucion anual 2021-2025. |
| `export_serie_anual_2021_2025_hs080610_uva.xls` | 080610 | Uva | Serie anual | Evolucion anual 2021-2025. |
| `export_serie_anual_2021_2025_hs081040_arandano.xls` | 081040 | Arandano | Serie anual | Evolucion anual 2021-2025. |

### 6.3 Variables esperadas desde Trade Map

| Variable Trade Map | Como se relaciona con la tesis |
|---|---|
| Valor exportado | Valida relevancia economica por producto/destino. |
| Cantidad exportada | Contrasta con volumen local/SUNAT. |
| Valor unitario | Proxy externo de precio promedio internacional. |
| Participacion de exportaciones de Peru | Mide concentracion por mercado destino. |
| Tasa de crecimiento 2021-2025 | Permite explicar mercados en expansion o contraccion. |
| Tasa de crecimiento 2024-2025 | Mide cambio reciente. |
| Posicion del socio en importaciones mundiales | Evalua atractivo del mercado destino. |
| Distancia media | Proxy logistico/comercial para discutir costos o dificultad. |
| Arancel medio estimado | Variable de friccion comercial. |

### 6.4 Archivos de importacion colados

Estos archivos no deben entrar al dataset final de exportaciones:

| Archivo | Razon de exclusion |
|---|---|
| `import_colado_indicadores_2025_hs080440_palta.xls` | Describe proveedores hacia Peru, no mercados destino de Peru. |
| `import_colado_indicadores_2025_hs080610_uva.xls` | Flujo incorrecto para la tesis. |
| `import_colado_indicadores_2025_hs081040_arandano.xls` | Flujo incorrecto para la tesis. |
| `import_colado_serie_anual_2021_2025_hs080440_palta.xls` | Serie de importacion, no exportacion. |
| `import_colado_serie_anual_2021_2025_hs080610_uva.xls` | Serie de importacion, no exportacion. |
| `import_colado_serie_anual_2021_2025_hs080610_uva_duplicado2.xls` | Duplicado colado. |

Relacion con la tesis: deben mencionarse solo como archivos descartados por control de calidad. No deben alimentar graficos, tablas ni entrenamiento.

### 6.5 Pendiente tecnico

Convertir los `.xls` HTML utiles a CSV:

- `trademap_export_indicadores_2025.csv`
- `trademap_export_serie_anual_2021_2025.csv`

Esto permitira cruzar Trade Map con `dataset_real_v1.csv` por producto, HS y mercado destino.

## 7. SISAP/MIDAGRI

Fuente: `http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/`  
Endpoint usado: `http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrar`  
CSV generado: `codex-revision/data_processed/sisap_midagri/sisap_midagri_mensual_2018_2026_2026-06-07.csv`

### 7.1 Rol de SISAP en la tesis

SISAP aporta informacion de mercado interno mayorista. No mide exportacion, pero ayuda a contextualizar:

- Precio interno mayorista.
- Volumen interno transado en mercado mayorista.
- Diferencias por variedad.
- Estacionalidad interna de palta, uva y esparrago.

En la tesis, SISAP puede responder:

- Si existen meses donde precio interno y volumen exportado se mueven de forma divergente.
- Si la presion de mercado interno coincide con anomalias de precio o volumen.
- Si existe estacionalidad local que ayude a explicar patrones del modelo.

### 7.2 Cobertura descargada

| Producto | Codigo SISAP | Mercado | Variable | Periodo |
|---|---:|---|---|---|
| Palta | 0626 | Mercado mayorista nro 2-frutas | Precio promedio, volumen | 2018-01 a 2026-06 efectivo |
| Uva | 0637 | Mercado mayorista nro 2-frutas | Precio promedio, volumen | 2018-01 a 2026-06 efectivo |
| Esparrago | 0216 | Gran mercado mayorista de Lima | Precio promedio, volumen | 2018-01 a 2026-06 efectivo |

Resumen:

| Indicador | Valor |
|---|---:|
| Consultas ejecutadas | 648 |
| Consultas con datos | 612 |
| Consultas sin datos | 36 |
| Filas CSV | 3,826 |
| Errores | 0 |

Las consultas sin datos son julio-diciembre de 2026, meses posteriores al corte disponible.

### 7.3 Relacion variable-tesis

| Variable SISAP | Relacion con tesis | Uso recomendado |
|---|---|---|
| `precio_prom` | Precio mayorista interno por variedad. | Variable contextual mensual por producto. |
| `volumen` | Movimiento/abastecimiento interno. | Proxy de oferta interna mensual. |
| `variedad` | Diferencia subproducto. | Puede agregarse por producto o analizarse aparte. |
| `mercado_nombre` | Mercado de referencia. | Control de fuente/localizacion. |

### 7.4 Limitaciones

| Limitacion | Implicacion |
|---|---|
| Arandano no aparece como producto directo. | No usar SISAP para arandano. |
| Datos son de mercado mayorista interno, no exportacion. | No reemplazan SUNAT ni Trade Map. |
| Diferentes variedades por producto. | Debe decidirse si se agregan por promedio/suma o se conservan. |
| Precio minimo/maximo no descargado. | Opcional; solo descargar si se usara como variable. |

## 8. SUNAT/ADUANET

Rutas:

- `codex-revision/data_raw/aduanet_bases/files`
- `data/sunat/raw_downloads`
- `data/sunat/x23290326.DBF`
- `data/sunat/sunat-exportacion-sectorial-2026.csv`

Formatos: ZIP, DBF, XLS, CSV.

### 8.1 Rol en la tesis

SUNAT/ADUANET debe ser la fuente primaria para exportaciones peruanas. Si la tesis afirma trabajar con exportaciones reales, esta es la fuente que debe sostener:

- Fecha de exportacion.
- Partida arancelaria.
- Valor FOB.
- Peso/volumen.
- Empresa exportadora.
- Pais destino.
- Aduana o puerto, si esta disponible.

### 8.2 Relacion con productos objetivo

| Producto | HS | Relacion |
|---|---|---|
| Esparrago | 070920 | Exportacion de esparragos frescos/refrigerados. |
| Palta | 080440 | Aguacates/paltas. |
| Uva | 080610 | Uvas frescas. |
| Arandano | 081040 | Arandanos y frutos similares. |

### 8.3 Uso en metodologia

SUNAT debe servir para:

1. Construir o validar el dataset transaccional.
2. Comparar volumen/precio con `dataset_real_v1.csv`.
3. Verificar que las partidas arancelarias sean correctas.
4. Generar variables reales de exportacion mensual.
5. Sustentar que los experimentos no se basan solo en datos sinteticos.

### 8.4 Pendiente

Extraer y normalizar todos los ZIP/DBF para crear:

`codex-revision/data_processed/sunat/sunat_exportaciones_hs_objetivo_2018_2026.csv`

Este archivo deberia ser uno de los pilares del dataset final.

## 9. BCRP

Rutas:

- `codex-revision/data_raw/bcrp/PN01207PM_2018-01_2026-06.csv`
- `data/bcrp/bcrp-tipo-cambio-mensual.csv`
- `data/downloads/bcrp_tipo_cambio.csv`

### 9.1 Rol en la tesis

BCRP aporta el tipo de cambio PEN/USD. Esta variable es relevante porque las exportaciones se valorizan usualmente en USD, mientras muchos costos internos estan en soles.

### 9.2 Relacion variable-tesis

| Variable | Uso |
|---|---|
| Tipo de cambio mensual | Control macroeconomico para precio, margen o anomalia. |
| Fecha mensual | Llave de integracion con exportaciones y SISAP. |

### 9.3 Cuidado metodologico

No se debe usar multiples versiones de tipo de cambio al mismo tiempo. Debe elegirse una version canonica y documentarse el codigo BCRP usado.

## 10. MIDAGRI compendios y Agro en cifras

Rutas:

- `codex-revision/data_raw/midagri_compendio`
- `data/midagri/agro-en-cifras-*`

Formatos: PDF, XLS, XLSX.

### 10.1 Rol en la tesis

Estos archivos son utiles para el marco contextual, no necesariamente para alimentar el modelo fila por fila. Aportan:

- Produccion agricola.
- Comercio exterior agrario.
- Comercio interno.
- Insumos y servicios agropecuarios.
- Indicadores sectoriales mensuales.

### 10.2 Relacion con capitulos

| Capitulo | Uso |
|---|---|
| Introduccion | Justificar relevancia del sector agroexportador. |
| Marco teorico/contextual | Describir evolucion del agro peruano. |
| Metodologia | Respaldar seleccion de productos. |
| Discusion | Contrastar resultados con indicadores sectoriales. |

### 10.3 Cuidado

Estos documentos suelen estar agregados por sector o producto. Si se usan como variable del modelo, debe indicarse que son datos agregados mensuales y no microdatos de embarque.

## 11. FAOSTAT

Rutas:

- `codex-revision/data_raw/faostat/Production_Crops_Livestock_E_All_Data_Normalized.zip`
- `codex-revision/data_raw/faostat/Trade_CropsLivestock_E_All_Data_Normalized.zip`
- `data/faostat/faostat-produccion-peru-2024.csv`

### 11.1 Rol en la tesis

FAOSTAT sirve como comparacion internacional y validacion macro. Puede ayudar a justificar:

- Produccion agricola agregada.
- Posicion de Peru frente a otros paises.
- Tendencias de comercio agricola.

### 11.2 Uso recomendado

Usarlo en graficos descriptivos o anexo metodologico, no como sustituto de SUNAT. Su granularidad es mas agregada.

## 12. APN y OSITRAN

Rutas:

- `codex-revision/data_raw/apn_2024`
- `codex-revision/data_raw/apn_2025`
- `codex-revision/data_raw/ositran_pnda`
- `codex-revision/data_raw/ositran_gobpe`

### 12.1 Rol en la tesis

Estas fuentes aportan contexto logistico portuario. Son relevantes si la tesis analiza anomalias o riesgo operativo porque retrasos, congestion o capacidad portuaria pueden afectar:

- Dias logisticos.
- Costo logistico.
- Merma.
- Cumplimiento de ventanas comerciales.

### 12.2 Variables posibles

| Variable derivada | Fuente | Relacion con tesis |
|---|---|---|
| Movimiento de carga mensual | APN/OSITRAN | Proxy de actividad portuaria. |
| Movimiento de contenedores | APN/OSITRAN | Proxy de capacidad/presion logistica. |
| Puerto o terminal | APN/OSITRAN/SUNAT si disponible | Permite segmentar riesgo logistico. |

### 12.3 Cuidado

No asignar congestion portuaria a un embarque individual si no existe llave directa por puerto/fecha. Lo defendible es usar variables agregadas por mes y puerto.

## 13. NASA POWER, SENAMHI y NDVI

Rutas:

- `codex-revision/data_raw/nasa_power`
- `codex-revision/data_raw/senamhi`
- `data/vegetation/ndvi_regional_index.json`

### 13.1 Rol en la tesis

Estas fuentes pueden explicar variabilidad productiva o de calidad a traves de clima y vegetacion. Sirven como variables exogenas.

### 13.2 Variables posibles

| Variable | Relacion |
|---|---|
| Temperatura maxima/minima | Estres termico, calidad, productividad. |
| Precipitacion | Riesgo agricola, afectacion de cosecha/transporte. |
| Humedad | Riesgo de deterioro o condiciones productivas. |
| NDVI | Proxy de vigor vegetativo regional. |

### 13.3 Cuidado

Estas variables no son temperatura del contenedor ni condiciones reales de cada embarque. Deben describirse como proxies por region y periodo.

## 14. SENASA, FDA y RASFF

Rutas:

- `codex-revision/data_raw/senasa`
- `codex-revision/data_raw/fda`
- `codex-revision/data_raw/rasff`

### 14.1 Rol en la tesis

Estas fuentes ayudan a construir contexto de riesgo sanitario e inocuidad. Pueden respaldar una discusion sobre rechazos, alertas, regulaciones o sensibilidad por mercado.

### 14.2 Uso posible

| Uso | Explicacion |
|---|---|
| Indicador mensual de alertas | Conteo de alertas/rechazos por producto o pais. |
| Variable contextual por destino | Riesgo regulatorio en mercados como EE.UU. o UE. |
| Discusion de resultados | Si el modelo detecta anomalias, contrastar con eventos sanitarios. |

### 14.3 Cuidado

No convertir alertas generales en cumplimiento fitosanitario por embarque si no hay una relacion directa. La tesis debe evitar afirmar causalidad sin evidencia.

## 15. World Bank Pink Sheet

Ruta:

`codex-revision/data_raw/world_bank`

Archivos relevantes:

- `CMO-Historical-Data-Monthly.xlsx`
- `CMO-Historical-Data-Annual.xlsx`
- PDFs mensuales Pink Sheet 2025-2026.

### 15.1 Rol en la tesis

World Bank Pink Sheet es util como contexto macro de precios internacionales de commodities. Para productos frescos especificos puede no tener correspondencia directa, por lo que debe usarse con cautela.

Uso recomendado:

- Contexto de precios internacionales.
- Variables macro generales si hay una serie relevante.
- Discusion economica, no variable principal del modelo si no existe producto equivalente.

## 16. ITC/Trade Map y UN Comtrade

### 16.1 ITC/Trade Map

La descarga automatizada quedo bloqueada por HTTP 403, pero el usuario descargo manualmente los archivos necesarios en `data-trademap`.

Decision:

- Usar los archivos manuales `export_*`.
- No insistir en scraping automatizado si la interfaz requiere sesion, navegador o protecciones.
- Documentar que la extraccion fue manual y los archivos fueron renombrados/auditados localmente.

### 16.2 UN Comtrade

Estado: API respondio HTTP 401 por falta de subscription key.

Uso esperado si se consigue acceso:

| Parametro | Valor |
|---|---|
| Reporter | Peru (`604`) |
| Flow | Exportaciones |
| Sistema | HS |
| Productos | `070920`, `080440`, `080610`, `081040` |
| Periodo | 2018-2026 |

Decision actual:

Trade Map cubre parcialmente esta necesidad, porque sus archivos ya incluyen calculos basados en INEI/Comtrade segun el encabezado exportado.

## 17. Descargas institucionales en `codex-revision/data_raw`

Resumen local:

| Fuente | Archivos | MB aprox. | Estado | Relacion con tesis |
|---|---:|---:|---|---|
| `aduanet_bases` | 53 | 588.17 | Descargado | Base primaria exportadora. |
| `faostat` | 4 | 297.34 | Descargado | Benchmark macro internacional. |
| `midagri_compendio` | 21 | 72.32 | Descargado | Contexto sectorial peruano. |
| `apn_2024` | 41 | 9.10 | Descargado | Logistica portuaria. |
| `apn_2025` | 42 | 9.25 | Descargado | Logistica portuaria reciente. |
| `world_bank` | 19 | 11.64 | Descargado parcial | Contexto macro/precios. |
| `nasa_power` | 5 | 1.22 | Descargado | Clima proxy. |
| `promperu_exportemos` | 9 | 1.43 | Descargado/generado | Contexto promocion/exportacion. |
| `ositran_pnda` | 61 | 2.28 | Descargado/generado | Logistica/puertos. |
| `ositran_gobpe` | 7 | 0.58 | Parcial | Logistica/puertos; enlaces sociales descartables. |
| `senamhi` | 13 | 0.46 | Parcial | Clima local. |
| `senasa` | 3 | 0.09 | Descargado | Riesgo fitosanitario. |
| `fda` | 3 | 0.08 | Descargado | Rechazos/alertas EE.UU. |
| `rasff` | 2 | 0.17 | Descargado | Alertas UE. |
| `inei` | 2 | 0.01 | Descargado | Contexto estadistico. |
| `bcrp` | 2 | 0.01 | Descargado | Tipo de cambio. |
| `sisap_midagri` | 754 | 1.26 | Descargado | Precio/volumen mercado interno. |
| `sunat` | 1 | 0.22 | Descargado | Acceso/operatividad aduanera. |
| `itc` | 0 | 0 | Bloqueado | Cubierto manualmente por Trade Map. |
| `un_comtrade` | 0 | 0 | Bloqueado | Pendiente API key. |

Manifiesto general:

- `codex-revision/metadata/download_manifest.csv`
- `codex-revision/metadata/download_manifest.json`
- `codex-revision/metadata/download_report.md`

Resumen general:

| Indicador | Valor |
|---|---:|
| Entradas de manifiesto | 341 |
| Descargados/generados | 329 |
| Errores/bloqueos HTTP | 12 |
| Bytes descargados/generados | 1,049,210,854 |

## 18. Estado real de faltantes

| Faltante | Impacto en tesis | Accion |
|---|---|---|
| Arandano en SISAP | Bajo, porque SISAP es mercado interno y arandano se cubre mejor con SUNAT/Trade Map. | Descartar SISAP para arandano. |
| Precio minimo/maximo SISAP | Medio si se quiere medir dispersion de precios internos. | Descargar solo si se formula una variable de volatilidad interna. |
| Julio-diciembre 2026 SISAP | Bajo; son meses futuros al corte de descarga. | Reintentar cuando existan datos. |
| Trade Map a CSV limpio | Alto; arandano depende mucho de Trade Map como benchmark. | Prioridad inmediata. |
| SUNAT/ADUANET normalizado | Muy alto; sostiene la validez real de exportaciones. | Prioridad maxima. |
| UN Comtrade API | Medio; Trade Map ya cubre parte. | Conseguir key o documentar descarte. |
| Trazabilidad de variables sinteticas/proxy | Muy alto; afecta defensa metodologica. | Crear diccionario final. |
| Duplicados/nulos/outliers | Alto; afecta metricas del modelo. | Ejecutar auditoria antes de resultados finales. |

## 19. Plan de trabajo iterativo para version Codex

### Iteracion 1: Congelar fuentes canonicas

Objetivo: decidir que archivos entran al pipeline final.

Entradas:

- `data/dataset_real_v1.csv`
- `data-trademap/export_*`
- `codex-revision/data_processed/sisap_midagri/sisap_midagri_mensual_2018_2026_2026-06-07.csv`
- `codex-revision/data_raw/bcrp/PN01207PM_2018-01_2026-06.csv`
- ZIP/DBF SUNAT/ADUANET

Salida:

`codex-revision/diccionario-fuentes-canonicas.md`

### Iteracion 2: Normalizar Trade Map

Objetivo: transformar los `.xls` HTML utiles a CSV.

Salida:

- `codex-revision/data_processed/trademap/trademap_export_indicadores_2025.csv`
- `codex-revision/data_processed/trademap/trademap_export_serie_anual_2021_2025.csv`

Relacion con tesis:

Permite construir tablas de mercados destino, crecimiento y competitividad para el marco contextual y resultados descriptivos.

### Iteracion 3: Normalizar SUNAT/ADUANET

Objetivo: construir fuente primaria exportadora filtrada por HS.

Salida:

`codex-revision/data_processed/sunat/sunat_exportaciones_hs_objetivo_2018_2026.csv`

Relacion con tesis:

Sostiene que los resultados se basan en exportaciones reales y no solo en dataset sintetico.

### Iteracion 4: Integrar variables mensuales

Objetivo: crear tabla mensual por producto/destino.

Fuentes:

- SUNAT/ADUANET: exportaciones.
- Trade Map: benchmark destino/anual.
- SISAP: mercado interno.
- BCRP: tipo de cambio.
- NASA/SENAMHI/NDVI: clima.
- APN/OSITRAN: logistica.

Salida:

`codex-revision/data_processed/dataset_integrado_mensual_v1.csv`

### Iteracion 5: Dataset modelable final

Objetivo: construir base final para IA/XAI.

Reglas:

1. Mantener palta, uva y arandano como nucleo.
2. Incluir esparrago solo si pasa validacion.
3. Excluir cacao.
4. Marcar variables como `real`, `proxy`, `sintetica` o `derivada`.
5. Separar entrenamiento/prueba por fecha para evitar fuga temporal.

Salida:

`codex-revision/data_processed/dataset_modelo_v_final.csv`

### Iteracion 6: Auditoria y anexos

Objetivo: dejar defendible la tesis.

Salidas:

- `codex-revision/reporte-trazabilidad-dataset-final.md`
- `codex-revision/diccionario-datos-final.md`
- `codex-revision/reporte-calidad-datos-final.md`

## 20. Recomendacion metodologica final

El orden correcto de trabajo no es seguir descargando mas fuentes sin integrarlas. La prioridad debe ser convertir lo ya disponible en evidencia defendible:

1. Normalizar Trade Map porque cubre palta, uva, arandano y esparrago en exportaciones.
2. Normalizar SUNAT/ADUANET porque debe ser la fuente primaria real.
3. Usar SISAP solo como contexto interno para palta, uva y esparrago.
4. Usar BCRP como control macro.
5. Incorporar clima, logistica y sanidad como proxies agregados, nunca como observaciones por embarque si no existe llave directa.
6. Construir el dataset final con trazabilidad por variable.

La tesis gana solidez si presenta los datos en tres capas:

| Capa | Contenido | Funcion |
|---|---|---|
| Capa real primaria | SUNAT/ADUANET y dataset real auditado | Entrenamiento y validacion principal. |
| Capa contextual externa | Trade Map, MIDAGRI, FAOSTAT, World Bank | Justificacion economica y comparacion. |
| Capa proxy explicativa | SISAP, BCRP, clima, logistica, sanidad | Variables explicativas agregadas y discusion. |

Con esa separacion, los modelos de IA explicable pueden defenderse mejor porque cada variable tendra fuente, granularidad y limitacion documentada.
