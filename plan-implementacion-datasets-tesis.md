# Plan de implementacion de datasets para la tesis

Fecha de creacion: 2026-06-07  
Fecha de ultima actualizacion: 2026-06-07 (v2 — instrucciones operativas agregadas)  
Ruta del proyecto: `D:\tesis_yoset`  
Documento rector: `D:\tesis_yoset\plan-implementacion-datasets-tesis.md`  
Documento tecnico base: `codex-revision/informe-final-data.md`

## 0. Identidad y comportamiento del agente

El agente que ejecuta este plan es un asistente de codigo autonomo (Codex, Claude Code, Cursor u equivalente). Su rol es exclusivamente tecnico: implementar, limpiar, integrar y validar datos segun las reglas de este documento. No debe tomar decisiones metodologicas por cuenta propia.

### Reglas de comportamiento obligatorio

1. **Ante ambiguedad, detener y preguntar.** Si una fuente tiene estructura inesperada, columnas distintas a las documentadas, o registros que no encajan con las llaves de integracion definidas en la seccion 7, el agente debe pausar y reportar el problema antes de continuar. No debe asumir ni inventar una solucion silenciosa.

2. **No modificar datos fuente crudos.** Los archivos en `data/sunat/raw_downloads/`, `data-trademap/`, `codex-revision/data_raw/` y equivalentes son de solo lectura. Todas las transformaciones se escriben en rutas `_processed/` o `_clean/` nuevas. Nunca sobreescribir el archivo de entrada.

3. **Registrar cada decision tomada.** Cada script ejecutado debe generar un log en `codex-revision/logs/YYYY-MM-DD_nombre-script.log` con: fecha de ejecucion, archivos de entrada, archivos de salida, filas procesadas, filas descartadas y motivo de descarte.

4. **No entrenar modelos con datos no auditados.** El entrenamiento (Fase 6 del cronograma) solo puede iniciarse si existe el archivo `codex-revision/reporte-calidad-datos.md` generado en la Fase 4. Si ese archivo no existe, detener y reportarlo.

5. **No modificar archivos en `docs/`.** Los capitulos de tesis son territorio exclusivo del tesista. El agente puede generar borradores de reformulacion en `codex-revision/reporte-reformulacion-tesis.md`, pero no editar `docs/tesis.md` ni ningun subcapitulo directamente.

6. **Versionar toda salida.** Cada CSV generado debe incluir sufijo de fecha: `nombre_YYYY-MM-DD.csv`. Nunca sobreescribir una version anterior sin crear primero una copia con sufijo de fecha anterior.

---

## 1. Proposito del plan

Este documento convierte el inventario de datos del proyecto en una ruta de implementacion concreta para la tesis: **Sistema Integrado de Supervision Operativa con Inteligencia Artificial Explicable en Empresas Agroexportadoras Peruanas**.

El plan gobierna el ciclo completo de datos:

- Identificacion de datasets reales, externos, procesados y sinteticos.
- Limpieza, transformacion, normalizacion y control de calidad.
- Integracion de fuentes con diferentes granularidades.
- Construccion del dataset final modelable.
- Entrenamiento de algoritmos predictivos y de deteccion de anomalias.
- Explicabilidad SHAP/TreeSHAP.
- Generacion de reportes tecnicos con RAG/LLM.
- Reformulacion del avance de tesis cuando la evidencia de datos lo exija.

El objetivo metodologico es pasar de una base inicial parcialmente sintetica o fragmentada a un sistema de datos defendible, trazable y alineado con la arquitectura de cuatro capas de la tesis:

| Capa | Funcion en la tesis | Dependencia de datos |
|---|---|---|
| Capa 1 | Prediccion tabular con LightGBM/XGBoost | Dataset limpio, temporal y trazable. |
| Capa 2 | Deteccion de anomalias con ensemble | Variables numericas comparables y etiquetas/proxies auditadas. |
| Capa 3 | Explicabilidad SHAP/TreeSHAP | Variables interpretables con fuente documentada. |
| Capa 4 | Reportes RAG/LLM | Evidencias, metadatos y contexto documental confiable. |

## 2. Estado actual del proyecto

La raiz del proyecto contiene datos, codigo, documentos de tesis y auditorias ya realizadas. Las rutas relevantes son:

| Ruta | Estado | Rol |
|---|---|---|
| `data/` | Existe | Datos base del proyecto: dataset real, sintetico, procesados, SUNAT, BCRP, MIDAGRI y otros. |
| `data-trademap/` | Existe | Descargas manuales de Trade Map ya renombradas y clasificadas. |
| `codex-revision/` | Existe | Carpeta de auditoria, scraping, documentacion, manifiestos y datos procesados por Codex. |
| `src/` | Existe | Codigo del sistema: ETL, generacion sintetica, modelos, SHAP, verificacion e interfaz. |
| `docs/` | Existe | Capitulos y documento de tesis que deberan actualizarse si cambia la base metodologica. |
| `scripts/` | Existe | Utilidades de compilacion, auditoria y mantenimiento. |
| `output/` | Existe | Entregables compilados de tesis. |

`codex-revision` contiene evidencia tecnica y auditoria; este archivo queda en la raiz porque debe funcionar como documento rector de implementacion y no solo como reporte de revision.

Insumos documentales ya existentes:

| Archivo | Uso para este plan |
|---|---|
| `codex-revision/informe-final-data.md` | Inventario detallado y relacion fuente-tesis. |
| `codex-revision/10-descarga-masiva-sisap-midagri.md` | Evidencia de descarga SISAP. |
| `data-trademap/README_renombrado.md` | Control de archivos Trade Map utiles y colados. |
| `README.md` | Arquitectura general de tesis y sistema. |
| `contenido_notebook_lm.md` | Contexto academico, objetivos, hipotesis y arquitectura. |

## 3. Segmentacion de productos

La implementacion debe fijar una segmentacion estable. No se debe volver a mezclar productos sin justificarlo.

| Producto | HS | Estado en proyecto | Fuente principal | Fuente complementaria | Decision metodologica |
|---|---|---|---|---|---|
| Palta | `080440` | Alta cobertura local y Trade Map disponible. | SUNAT/ADUANET y `data/dataset_real_v1.csv` | Trade Map, SISAP, BCRP, clima/logistica | Producto nucleo. Mantener en todos los experimentos. |
| Uva | `080610` | Alta cobertura local y Trade Map disponible. | SUNAT/ADUANET y `data/dataset_real_v1.csv` | Trade Map, SISAP, BCRP, clima/logistica | Producto nucleo. Mantener en todos los experimentos. |
| Arandano | `081040` | Cobertura local menor; Trade Map disponible; no aparece directamente en SISAP. | SUNAT/ADUANET y `data/dataset_real_v1.csv` | Trade Map, BCRP, clima/logistica/sanidad | Producto nucleo. No depender de SISAP. |
| Esparrago | `070920` | Presente en dataset real, Trade Map y SISAP. | SUNAT/ADUANET | Trade Map, SISAP, BCRP | Producto secundario condicionado. Incluir solo si pasa validacion. |
| Cacao | Verificar si existe HS local | Solo 379 filas detectadas en `dataset_real_v1.csv`. | Ninguna fuente canonica actual | No aplica | Excluir del dataset final y del nucleo experimental. |

Reglas:

- Los resultados principales se reportaran para palta, uva y arandano.
- Esparrago puede aparecer como producto comparativo si se normaliza con suficiente calidad.
- Cacao se excluye por baja representatividad y por desalineacion con el foco final.
- Si se mantiene una mencion historica a cacao en capitulos previos, debe reformularse como producto descartado por control metodologico.

## 4. Inventario de datasets conocidos

### 4.1 Dataset real local

| Campo | Detalle |
|---|---|
| Ruta | `data/dataset_real_v1.csv` |
| Formato | CSV |
| Estado | Disponible |
| Filas auditadas | 40,672 |
| Productos detectados | palta, uva, arandano, esparrago, cacao |
| Uso principal | Base experimental inicial y referencia para construir el dataset final. |
| Relacion con tesis | Soporta metodologia, entrenamiento, deteccion de anomalias y resultados. |

Variables esperadas:

- Identificacion: `id`, `fecha`, `producto`, `partida_arancelaria`.
- Comercio: `empresa_exportadora`, `zona`, `volumen_kg`, `precio_kg_usd`, `destino_mercado`.
- Logistica: `dias_logisticos`, `costo_logistico_usd_kg`.
- Sanidad/calidad: `cumplimiento_fitosanitario`, `merma_pct`.
- Macro/clima: `tipo_cambio_pen_usd`, `temperatura_max_c`, `temperatura_min_c`, `precipitacion_mm`, `humedad_pct`.
- Modelamiento: `etiqueta_anomalia`, `tipo_anomalia`, `regla_inyeccion`.

Riesgos metodologicos:

- Algunas variables pueden ser proxies o sinteticas.
- `regla_inyeccion` indica posible generacion artificial de anomalias.
- Debe validarse contra SUNAT/ADUANET y fuentes externas.
- No debe afirmarse que todas las columnas son observaciones oficiales.

### 4.2 Dataset sintetico local

| Campo | Detalle |
|---|---|
| Ruta | `data/dataset_agro_sintetico_v1.csv` |
| Formato | CSV |
| Estado | Disponible |
| Uso principal | Simulacion, balanceo, pruebas de interfaz y robustez. |
| Relacion con tesis | Puede respaldar escenarios controlados, no sustituir evidencia real. |

Uso permitido:

- Balancear clases de anomalias cuando la clase positiva sea escasa.
- Simular escenarios de supervision operacional.
- Probar modulos de SHAP y reportes RAG.
- Comparar desempeno real vs sintetico.

Riesgo:

- No presentar como dato observado.
- Marcar toda fila o variable sintetica con etiqueta `sintetica`.
- Documentar regla de generacion y parametro usado.

### 4.3 Datasets procesados reales

| Ruta | Formato | Estado | Uso |
|---|---|---|---|
| `data/real_processed/` | CSV | Disponible | Versiones procesadas agregadas y por producto. |
| `data/real_processed/palta/` | CSV | Disponible | Segmento real de palta. |
| `data/real_processed/uva/` | CSV | Disponible | Segmento real de uva. |
| `data/real_processed/arandano/` | CSV | Disponible | Segmento real de arandano. |

Pendiente:

- Confirmar si debe crearse `data/real_processed/esparrago/`.
- Verificar que los splits existentes sigan una division temporal y no aleatoria.
- Validar que los archivos balanceados no contaminen el conjunto de prueba.

### 4.4 Datasets procesados sinteticos

| Ruta | Formato | Estado | Uso |
|---|---|---|---|
| `data/synthetic_processed/` | CSV | Disponible | Entrenamiento/pruebas auxiliares con datos sinteticos. |

Regla:

- No mezclar con datos reales sin columna `origen_dato`.
- Usar para pruebas comparativas, no como resultado principal.

### 4.5 Trade Map

Ruta: `data-trademap/`  
Formato externo: `.xls`  
Formato interno: HTML exportado como Excel  
Estado: descargado manualmente y renombrado.

Archivos utiles:

| Archivo | Producto | HS | Vista | Uso |
|---|---|---|---|---|
| `export_indicadores_2025_hs070920_esparrago.xls` | Esparrago | `070920` | Indicadores 2025 | Benchmark por mercados destino. |
| `export_indicadores_2025_hs080440_palta.xls` | Palta | `080440` | Indicadores 2025 | Benchmark por mercados destino. |
| `export_indicadores_2025_hs080610_uva.xls` | Uva | `080610` | Indicadores 2025 | Benchmark por mercados destino. |
| `export_indicadores_2025_hs081040_arandano.xls` | Arandano | `081040` | Indicadores 2025 | Benchmark por mercados destino. |
| `export_serie_anual_2021_2025_hs070920_esparrago.xls` | Esparrago | `070920` | Serie anual | Tendencia anual por destino. |
| `export_serie_anual_2021_2025_hs080440_palta.xls` | Palta | `080440` | Serie anual | Tendencia anual por destino. |
| `export_serie_anual_2021_2025_hs080610_uva.xls` | Uva | `080610` | Serie anual | Tendencia anual por destino. |
| `export_serie_anual_2021_2025_hs081040_arandano.xls` | Arandano | `081040` | Serie anual | Tendencia anual por destino. |

Archivos descartados:

| Patron | Decision |
|---|---|
| `data-trademap/import_colado_*` | Mantener por trazabilidad, excluir del pipeline final. |

Variables esperadas:

- Valor exportado.
- Cantidad exportada.
- Unidad.
- Valor unitario.
- Participacion.
- Tasa de crecimiento.
- Posicion relativa del socio.
- Distancia.
- Arancel estimado.

Relacion con tesis:

- Marco contextual.
- Validacion externa por mercados destino.
- Justificacion de relevancia de productos.
- Soporte para arandano, que no se cubre por SISAP.

### 4.6 SISAP/MIDAGRI

| Campo | Detalle |
|---|---|
| CSV procesado | `codex-revision/data_processed/sisap_midagri/sisap_midagri_mensual_2018_2026_2026-06-07.csv` |
| HTML crudos | `codex-revision/data_raw/sisap_midagri/massive/` |
| Formato | CSV y HTML |
| Estado | Descargado y documentado |
| Cobertura | Palta, uva, esparrago |
| Variables | `precio_prom`, `volumen` |

Uso:

- Contexto de mercado interno.
- Variables mensuales por producto.
- Comparacion con exportaciones cuando la granularidad sea mensual.

Limitaciones:

- No es fuente de exportaciones.
- Arandano no aparece como producto directo.
- Julio-diciembre 2026 no estaba disponible al momento de descarga.

### 4.7 SUNAT/ADUANET

Rutas:

- `data/sunat/raw_downloads/*.zip`
- `data/sunat/*.DBF`
- `data/sunat/sunat-exportacion-sectorial-2026.csv`
- `codex-revision/data_raw/aduanet_bases`

Formatos:

- ZIP.
- DBF.
- XLS.
- CSV.

Uso principal:

- Fuente primaria final para exportaciones reales.
- Validacion de volumen, valor, partida, fecha, destino y empresa.

Variables esperadas:

- Partida arancelaria.
- Fecha de embarque/exportacion.
- Valor FOB.
- Peso neto o volumen.
- Pais destino.
- Empresa exportadora.
- Aduana/puerto si existe.

Riesgo:

- Requiere parseo cuidadoso.
- Puede tener codificaciones antiguas.
- No todos los ZIP contienen la misma estructura.

### 4.8 BCRP

Rutas:

- `data/bcrp/bcrp-tipo-cambio-mensual.csv`
- `data/bcrp/exchange_rates_cache.json`
- `data/downloads/bcrp_tipo_cambio.csv`
- `codex-revision/data_raw/bcrp/PN01207PM_2018-01_2026-06.csv`

Uso:

- Tipo de cambio mensual PEN/USD.
- Variable macro de control.
- Union por `periodo_mes`.

Riesgo:

- Debe elegirse una sola version canonica.
- No duplicar fuentes de tipo de cambio.

### 4.9 MIDAGRI compendios y Agro en cifras

Rutas:

- `data/midagri/agro-en-cifras-*`
- `codex-revision/data_raw/midagri_compendio`

Formatos:

- PDF.
- XLS.
- XLSX.

Uso:

- Contexto sectorial.
- Validacion descriptiva.
- Posible fuente agregada de comercio interno/externo.

Riesgo:

- Reportes agregados no deben mezclarse con microdatos sin declarar granularidad.

### 4.10 Fuentes externas complementarias

| Fuente | Ruta | Formato | Uso en tesis | Riesgo |
|---|---|---|---|---|
| FAOSTAT | `codex-revision/data_raw/faostat`, `data/faostat` | ZIP/CSV | Benchmark macro internacional. | Granularidad agregada. |
| NASA POWER | `codex-revision/data_raw/nasa_power` | JSON/CSV | Clima proxy por region/mes. | No representa contenedor ni embarque. |
| SENAMHI | `codex-revision/data_raw/senamhi` | HTML/CSV/PDF segun fuente | Clima local. | Cobertura parcial. |
| APN | `codex-revision/data_raw/apn_2024`, `apn_2025` | XLS/XLSX/PDF/HTML | Movimiento portuario. | Union solo por puerto/mes si existe. |
| OSITRAN | `codex-revision/data_raw/ositran_pnda`, `ositran_gobpe` | CSV/XLS/HTML/PDF | Logistica y puertos. | Datos agregados. |
| SENASA | `codex-revision/data_raw/senasa` | HTML/CSV/JSON | Riesgo fitosanitario. | No asumir cumplimiento por embarque. |
| FDA | `codex-revision/data_raw/fda` | HTML/CSV/JSON | Rechazos o alertas EE.UU. | Eventos no siempre vinculables a embarque. |
| RASFF | `codex-revision/data_raw/rasff` | HTML/CSV/JSON | Alertas UE. | Contexto, no causalidad directa. |
| World Bank | `codex-revision/data_raw/world_bank`, `data/global_benchmarks` | XLSX/PDF/CSV | Contexto macro/precios. | Puede no tener producto fresco equivalente. |
| INEI | `codex-revision/data_raw/inei`, `data/inei` | PDF/HTML | Contexto estadistico. | No es fuente de microdatos exportadores aqui. |

### 4.11 Protocolo ante fallos de descarga o estructura inesperada

Cada fuente puede fallar de distintas formas. El agente debe seguir este protocolo por fuente:

| Fuente | Fallo posible | Accion del agente |
|---|---|---|
| SUNAT/ADUANET | ZIP corrupto, DBF con codificacion CP850 inesperada, columnas renombradas | Intentar encoding alternativo (latin-1, cp1252). Si falla, aislar el archivo en `data/sunat/failed/` y continuar con los demas. Documentar en log. |
| Trade Map XLS | Archivo HTML disfrazado de XLS, hojas vacias, filas de totales mezcladas | Leer con `pd.read_html()` si `pd.read_excel()` falla. Eliminar filas donde el campo de valor sea "Total" o este vacio. Documentar filas descartadas. |
| BCRP API | Timeout, cambio de endpoint, respuesta JSON malformada | Usar version en cache `codex-revision/data_raw/bcrp/PN01207PM_2018-01_2026-06.csv`. No hacer mas de 3 reintentos. |
| SISAP | Pagina HTML con estructura cambiada, tabla ausente | Marcar el mes como nulo estructural. No imputar con valor anterior sin declararlo. |
| NASA POWER API | Rate limit, coordenadas sin cobertura | Reducir resolucion a nivel departamental. Si persiste, usar SENAMHI como alternativa. Documentar el cambio. |
| SENASA datos abiertos | Dataset con columnas distintas a las esperadas | No asumir equivalencias. Reportar columnas encontradas vs esperadas y esperar instruccion. |

Si un fallo impide completar una fase entera del cronograma, el agente debe crear el archivo `codex-revision/BLOQUEO_fase_N.md` describiendo el problema, la fuente, el error exacto y las opciones tecnicas posibles, y detenerse hasta recibir instruccion.

## 5. Diccionario de etiquetas metodologicas

Toda variable o dataset que entre al pipeline final debe recibir etiquetas de origen, granularidad y uso.

### 5.1 Etiquetas de origen

| Etiqueta | Definicion | Ejemplo |
|---|---|---|
| `real_observada` | Dato observado directamente en una fuente primaria o dataset real auditado. | Volumen exportado SUNAT. |
| `real_agregada` | Dato real pero publicado a nivel agregado. | Precio promedio mensual SISAP. |
| `proxy` | Variable aproximada para representar un fenomeno no observado directamente. | Congestion portuaria por carga mensual. |
| `derivada` | Variable calculada desde otras variables. | Precio USD/kg = FOB / kg. |
| `sintetica` | Variable o fila generada por reglas/simulacion. | Merma simulada. |
| `descartada` | Variable o archivo excluido del pipeline final. | Importaciones coladas de Trade Map. |

### 5.2 Etiquetas de granularidad

| Etiqueta | Definicion |
|---|---|
| `embarque` | Registro cercano a operacion/exportacion individual. |
| `empresa` | Variable agregada o identificada por empresa. |
| `producto_mes` | Dato mensual por producto. |
| `producto_destino_anio` | Dato anual por producto y mercado destino. |
| `region_mes` | Dato mensual por region productiva. |
| `puerto_mes` | Dato mensual por puerto o terminal. |

### 5.3 Etiquetas de uso

| Etiqueta | Uso |
|---|---|
| `entrenamiento` | Puede alimentar modelos. |
| `validacion` | Puede usarse para comparar o verificar resultados. |
| `contexto` | Sirve para marco descriptivo o discusion. |
| `explicabilidad` | Puede aparecer en SHAP o interpretacion. |
| `reporte_rag` | Puede alimentar evidencias del reporte narrativo. |
| `anexo` | Se conserva como evidencia documental. |
| `exclusion` | Se conserva pero no se usa en modelamiento. |

## 6. Plan de tratamiento y limpieza

### 6.1 Reglas globales

1. Normalizar nombres de productos:
   - `palta`
   - `uva`
   - `arandano`
   - `esparrago`
2. Homologar partidas HS:
   - Palta: `080440`
   - Uva: `080610`
   - Arandano: `081040`
   - Esparrago: `070920`
3. Convertir fechas:
   - `fecha` en formato `YYYY-MM-DD`.
   - `periodo_mes` en formato `YYYY-MM`.
   - `anio` numerico.
4. Homologar mercados destino:
   - Normalizar nombres de paises.
   - Crear tabla puente si Trade Map y SUNAT usan nombres distintos.
5. Convertir unidades:
   - kg como unidad base de volumen transaccional.
   - toneladas convertidas a kg cuando sea necesario.
   - USD como moneda base.
   - miles USD convertidos a USD para comparaciones.
6. Eliminar duplicados:
   - Duplicado exacto.
   - Duplicado funcional por `producto + hs + fecha + destino + empresa + volumen + valor`.
7. Separar nulos:
   - Nulo estructural: fuente no lo provee.
   - Nulo por error: dato esperado ausente.
8. Identificar outliers antes de entrenar:
   - Precio unitario extremo.
   - Volumen extremo.
   - Tipo de cambio fuera de rango.
   - Clima fuera de rango fisico.
9. Preservar trazabilidad:
   - `archivo_origen`.
   - `fuente`.
   - `fecha_descarga`.
   - `granularidad`.
   - `tipo_origen_variable`.

### 6.2 Tratamiento por fuente

| Fuente | Tratamiento |
|---|---|
| Trade Map | Parsear `.xls` HTML a CSV; separar indicadores 2025 y serie anual 2021-2025; excluir `import_colado_*`. |
| SUNAT/ADUANET | Extraer ZIP/DBF; leer estructuras; filtrar HS objetivo; homologar fecha, destino, empresa, volumen y FOB. |
| SISAP | Mantener como precio/volumen interno para palta, uva y esparrago; agregar por producto/mes si se requiere. |
| BCRP | Elegir una version canonica; normalizar a `periodo_mes`; unir por mes. |
| MIDAGRI | Clasificar hojas de comercio exterior, interno y agricola; usar como contexto o validacion agregada. |
| Clima | Agregar NASA/SENAMHI/NDVI por region/mes; etiquetar como proxy. |
| Logistica | Agregar APN/OSITRAN por puerto/mes; etiquetar como proxy. |
| Sanidad | Agregar SENASA/FDA/RASFF por producto/destino/mes si existe; etiquetar como proxy/contexto. |

## 7. Plan de integracion

La integracion se realizara por capas para evitar unir datos incompatibles.

### 7.1 Capas de integracion

| Capa | Fuentes | Rol |
|---|---|---|
| Capa real primaria | SUNAT/ADUANET + `dataset_real_v1.csv` auditado | Base observacional de exportaciones. |
| Capa contextual externa | Trade Map, MIDAGRI, FAOSTAT, World Bank | Validacion macro y contexto comercial. |
| Capa proxy explicativa | SISAP, BCRP, clima, logistica, sanidad | Variables explicativas agregadas. |

### 7.2 Llaves de integracion

| Llave | Uso |
|---|---|
| `producto` | Union principal de producto normalizado. |
| `hs` | Union con SUNAT/ADUANET/Trade Map. |
| `fecha` | Operacion individual cuando exista. |
| `periodo_mes` | Union mensual con BCRP, SISAP, clima y logistica. |
| `destino_mercado` | Union con Trade Map y alertas destino. |
| `region_productiva` | Union con clima/NDVI si existe. |
| `puerto` | Union con APN/OSITRAN si existe. |

Regla critica:

No se debe forzar una union a nivel embarque si la fuente es agregada. En esos casos la variable debe entrar como proxy mensual, regional o portuario.

### 7.3 Matriz fuente-variable-tesis

| Variable final | Fuente preferida | Etiqueta origen | Granularidad | Relacion con tesis |
|---|---|---|---|---|
| `volumen_kg` | SUNAT/ADUANET | `real_observada` | `embarque` o `producto_mes` | Base para prediccion y deteccion de anomalias. |
| `valor_fob_usd` | SUNAT/ADUANET | `real_observada` | `embarque` | Base comercial real. |
| `precio_kg_usd` | Derivada de FOB/kg o dataset real | `derivada` | `embarque` | Variable clave para outliers de precio. |
| `destino_mercado` | SUNAT/ADUANET + Trade Map | `real_observada` | `embarque` | Segmentacion comercial. |
| `trade_valor_exportado` | Trade Map | `real_agregada` | `producto_destino_anio` | Benchmark internacional. |
| `trade_crecimiento` | Trade Map | `real_agregada` | `producto_destino_anio` | Contexto de mercados en expansion. |
| `sisap_precio_prom` | SISAP/MIDAGRI | `real_agregada` | `producto_mes` | Contexto interno. |
| `sisap_volumen` | SISAP/MIDAGRI | `real_agregada` | `producto_mes` | Oferta interna mayorista. |
| `tipo_cambio_pen_usd` | BCRP | `real_agregada` | `producto_mes` | Control macro. |
| `temperatura_max_c` | NASA/SENAMHI | `proxy` | `region_mes` | Condicion climatica. |
| `precipitacion_mm` | NASA/SENAMHI | `proxy` | `region_mes` | Riesgo climatico. |
| `ndvi` | NDVI local | `proxy` | `region_mes` | Vigor vegetativo. |
| `carga_portuaria_mes` | APN/OSITRAN | `proxy` | `puerto_mes` | Presion logistica. |
| `alertas_sanitarias_mes` | SENASA/FDA/RASFF | `proxy` | `producto_destino_mes` | Riesgo sanitario contextual. |
| `merma_pct` | Dataset real o sintetico | `proxy` o `sintetica` | `embarque` | Debe justificarse con cuidado. |
| `etiqueta_anomalia` | Dataset real/reglas | `derivada` o `sintetica` | `embarque` | Target experimental. |

### 7.4 Reglas de resolucion de conflictos entre fuentes

Cuando dos fuentes proveen el mismo campo con valores distintos, el agente aplica esta jerarquia sin excepcion:

**Para volumen y valor FOB de exportacion:**
SUNAT/ADUANET > dataset_real_v1.csv > Trade Map > FAOSTAT

**Para precio unitario FOB (USD/kg):**
Derivado de SUNAT (FOB/kg) > dataset_real_v1.csv > Trade Map valor unitario > SISAP como referencia interna (no como precio FOB, son mercados distintos)

**Para tipo de cambio:**
BCRP serie PN01207PM > ninguna otra fuente. Una sola version canonica: `codex-revision/data_raw/bcrp/PN01207PM_2018-01_2026-06.csv`.
No usar archivos `data/bcrp/bcrp-tipo-cambio-mensual.csv` ni `data/downloads/bcrp_tipo_cambio.csv` en paralelo. Elegir uno, documentarlo en `diccionario-fuentes-canonicas.md` y eliminar referencias a los demas del pipeline.

**Para clima:**
NASA POWER (cobertura completa por coordenada) > SENAMHI estaciones (mayor precision local, menor cobertura) > valor nulo documentado.
No imputar clima con la media del mes anterior sin declararlo como `proxy_imputado` en la columna `tipo_variable`.

**Regla general:** cuando haya conflicto, documentar ambos valores en columnas separadas (`campo_fuente_a`, `campo_fuente_b`) y crear columna `campo_seleccionado` con el valor ganador segun jerarquia. No silenciar el conflicto.

---

## 8. Uso de datos sinteticos

Los datos sinteticos solo se usaran cuando exista una razon metodologica explicita.

### 8.1 Casos permitidos

| Caso | Justificacion | Condicion |
|---|---|---|
| Vacios imposibles de cubrir con fuente publica | Algunas variables operativas no son publicas por embarque. | Etiquetar como `sintetica` o `proxy`. |
| Balanceo de anomalias | La clase anomalía puede ser escasa. | No contaminar test real. |
| Simulacion de supervision | Se requieren escenarios para evaluar tiempo-a-decision. | Separar de resultados principales. |
| Pruebas de robustez | Validar estabilidad del pipeline. | Reportar como experimento auxiliar. |

### 8.2 Escenarios sinteticos defendibles

| Variable o escenario | Uso | Requisito documental |
|---|---|---|
| Merma estimada | Simular perdida por deterioro/logistica. | Explicar regla y rango. |
| Retraso logistico simulado | Probar alertas por demora. | Basar rangos en literatura o datos agregados. |
| Cumplimiento fitosanitario proxy | Simular riesgo de incumplimiento. | No llamarlo dato oficial por embarque. |
| Etiquetas de anomalia por reglas | Entrenar/evaluar detectores supervisados o semisupervisados. | Guardar `regla_inyeccion`. |

### 8.3 Prohibiciones

- No presentar datos sinteticos como observaciones oficiales.
- No mezclar train/test sintetico y real sin columna `origen_dato`.
- No usar variables sinteticas en conclusiones de impacto real sin aclaracion.
- No imputar con sinteticos mercados o productos completos sin sustento.

### 8.4 Relacion con la tesis

El capitulo metodologico debe reformularse para decir que el sistema usa:

1. Datos reales observados.
2. Datos reales agregados.
3. Proxies publicos.
4. Datos sinteticos controlados para escenarios y balanceo.

## 9. Construccion del dataset final

### 9.1 Salida esperada

Archivo final recomendado:

`data/dataset_modelo_v_final.csv`

Salida alternativa de trabajo si se desea mantener `data/` intacto durante la fase experimental:

`codex-revision/data_processed/dataset_modelo_v_final.csv`

La version final debe ser versionada. Ejemplo:

`data/dataset_modelo_v_final_2026-06-07.csv`

### 9.2 Esquema obligatorio del dataset final — Contrato de columnas

El agente no puede entregar el dataset final si falta alguna columna marcada como OBLIGATORIA. Las marcadas CONDICIONAL se incluyen solo si la fuente las provee con cobertura >= 60% del periodo.

| Columna | Tipo | Obligatoria | Fuente canonica | Etiqueta origen |
|---|---|---|---|---|
| `id` | string | SI | Generada | `derivada` |
| `producto` | categorical | SI | SUNAT | `real_observada` |
| `hs` | string (6 digitos) | SI | SUNAT | `real_observada` |
| `fecha` | date YYYY-MM-DD | SI | SUNAT | `real_observada` |
| `periodo_mes` | string YYYY-MM | SI | Derivada de fecha | `derivada` |
| `anio` | int | SI | Derivada de fecha | `derivada` |
| `mes` | int (1-12) | SI | Derivada de fecha | `derivada` |
| `empresa_exportadora` | string | SI | SUNAT | `real_observada` |
| `ruc` | string | CONDICIONAL | SUNAT | `real_observada` |
| `volumen_kg` | float > 0 | SI | SUNAT | `real_observada` |
| `valor_fob_usd` | float > 0 | SI | SUNAT | `real_observada` |
| `precio_kg_usd` | float > 0 | SI | Derivada FOB/kg | `derivada` |
| `destino_mercado` | string | SI | SUNAT | `real_observada` |
| `aduana_codigo` | int | SI | SUNAT | `real_observada` |
| `zona_productora` | string | SI | Mapeada de aduana | `derivada` |
| `puerto` | string | CONDICIONAL | APN/SUNAT | `proxy` |
| `tipo_cambio_pen_usd` | float | SI | BCRP | `real_agregada` |
| `sisap_precio_prom` | float | CONDICIONAL (palta/uva/esparrago) | SISAP | `real_agregada` |
| `sisap_volumen` | float | CONDICIONAL (palta/uva/esparrago) | SISAP | `real_agregada` |
| `temperatura_max_c` | float | SI | NASA POWER / SENAMHI | `proxy` |
| `temperatura_min_c` | float | SI | NASA POWER / SENAMHI | `proxy` |
| `precipitacion_mm` | float | SI | NASA POWER / SENAMHI | `proxy` |
| `humedad_pct` | float | CONDICIONAL | NASA POWER / SENAMHI | `proxy` |
| `ndvi` | float [0-1] | CONDICIONAL | NASA POWER / GEE | `proxy` |
| `carga_portuaria_mes` | float | CONDICIONAL | APN/OSITRAN | `proxy` |
| `alertas_sanitarias_mes` | int | CONDICIONAL | SENASA/FDA/RASFF | `proxy` |
| `cumplimiento_fitosanitario` | int (0/1) | SI* | SENASA o sintetica | `proxy` o `sintetica` |
| `dias_logisticos` | float | SI* | Dataset real o estimado | `proxy` o `sintetica` |
| `merma_pct` | float [0-1] | SI* | Dataset real o estimado | `proxy` o `sintetica` |
| `etiqueta_anomalia` | int (0/1) | SI | Reglas o real | `derivada` o `sintetica` |
| `tipo_anomalia` | categorical | SI | Reglas o real | `derivada` o `sintetica` |
| `regla_inyeccion` | string | SI (si sintetica) | Generada | `sintetica` |
| `origen_dato` | categorical | SI | Generada | `derivada` |
| `tipo_variable_fila` | categorical | SI | Generada | `derivada` |
| `fuentes_usadas` | string | SI | Generada | `derivada` |
| `archivo_origen` | string | SI | Generada | `derivada` |
| `dataset_version` | string | SI | Generada | `derivada` |
| `fecha_generacion` | date | SI | Generada | `derivada` |

*Las columnas marcadas SI* son obligatorias pero pueden ser proxy documentado o sinteticas justificadas. No pueden estar completamente ausentes del dataset final.

**Valores prohibidos en columnas obligatorias:**
- `precio_kg_usd` <= 0
- `volumen_kg` <= 0
- `valor_fob_usd` <= 0
- `temperatura_max_c` fuera de [-10, 48]
- `precipitacion_mm` < 0
- `ndvi` fuera de [0, 1]
- `merma_pct` fuera de [0, 1]
- `cumplimiento_fitosanitario` fuera de {0, 1}

Si algun registro viola estas reglas, el agente debe aislarlo en `codex-revision/data_processed/rejected/rechazados_YYYY-MM-DD.csv` con columna `motivo_rechazo` y nunca incluirlo en el dataset final.

### 9.3 Reglas de inclusion

- Incluir palta, uva y arandano siempre que tengan cobertura suficiente.
- Incluir esparrago solo si se crea segmento validado.
- Excluir cacao.
- Mantener columna `origen_dato`.
- Mantener columna `dataset_version`.
- Mantener columna `fecha_generacion`.

## 10. Analisis exploratorio

Antes de entrenar modelos, generar un EDA obligatorio.

### 10.1 Analisis requeridos

| Analisis | Objetivo | Salida |
|---|---|---|
| Cobertura por producto y anio | Confirmar representatividad temporal. | Tabla CSV y grafico. |
| Distribucion por mercado destino | Detectar concentracion comercial. | Tabla ranking y grafico. |
| Volumen por producto | Validar escala exportadora. | Series temporales. |
| Precio por producto | Detectar volatilidad y outliers. | Boxplots y series. |
| Estacionalidad mensual | Ver patrones agroexportadores. | Heatmap producto-mes. |
| Nulos por fuente | Diferenciar vacios reales y errores. | Matriz de nulos. |
| Duplicados | Evitar inflar datos. | Reporte de duplicados. |
| Outliers | Detectar extremos antes de modelar. | Reporte de reglas. |
| Correlaciones | Identificar relaciones y colinealidad. | Matriz correlacion. |
| Real vs TradeMap/SUNAT | Validar consistencia externa. | Tabla comparativa. |
| Variables sinteticas | Confirmar separacion y justificacion. | Reporte metodologico. |

### 10.2 Salidas esperadas

- `codex-revision/data_processed/eda/tablas/*.csv`
- `codex-revision/data_processed/eda/figuras/*.png`
- `codex-revision/reporte-calidad-datos.md`

## 11. Procesamiento para modelos

### 11.1 Split temporal

La division principal debe ser temporal:

| Particion | Porcentaje | Uso |
|---|---:|---|
| Train | 70% | Ajuste de modelos. |
| Validacion | 10% | Hiperparametros y umbrales. |
| Test | 20% | Evaluacion final. |

Regla:

No usar split aleatorio como evaluacion principal, porque generaria fuga temporal en series agroexportadoras con estacionalidad.

### 11.2 Preprocesamiento

| Tipo de variable | Tratamiento |
|---|---|
| Numerica continua | Imputacion documentada, escalado si el algoritmo lo requiere. |
| Categorica baja cardinalidad | One-hot encoding. |
| Categorica alta cardinalidad | Target encoding o hashing, evitando fuga temporal. |
| Temporal | Extraer anio, mes, trimestre, campana si aplica. |
| Producto | Mantener como categorica y tambien entrenar modelos por producto si procede. |
| Destino mercado | Homologar paises y codificar. |
| Sintetica/proxy | Mantener flags de origen. |

### 11.3 Datasets derivados

Archivos esperados:

- `dataset_train_raw.csv`
- `dataset_train_balanced.csv`
- `dataset_validation.csv`
- `dataset_test.csv`
- `dataset_inference_examples.csv`

Ubicacion recomendada:

`codex-revision/data_processed/modeling/`

## 11.5 Checklist de validacion pre-entrenamiento (gate obligatorio)

El agente NO puede iniciar la Fase 6 (entrenamiento) sin que todos los siguientes items esten marcados como PASS en el archivo `codex-revision/gate-pre-entrenamiento.md`:

### Gate de datos
- [ ] `dataset_modelo_v_final.csv` existe y tiene fecha en el nombre.
- [ ] Numero de filas documentado y consistente con el EDA.
- [ ] Cero filas con `precio_kg_usd` <= 0.
- [ ] Cero filas con `volumen_kg` <= 0.
- [ ] Columna `origen_dato` presente en cada fila.
- [ ] Columna `etiqueta_anomalia` presente sin nulos.
- [ ] Cacao completamente ausente del dataset final.
- [ ] Split temporal implementado sin mezcla aleatoria.
- [ ] Conjunto de prueba no contaminado por SMOTE ni balanceo.
- [ ] `reporte-calidad-datos.md` generado y disponible.

### Gate de trazabilidad
- [ ] `diccionario-fuentes-canonicas.md` existe y tiene entrada para cada fuente usada en el dataset final.
- [ ] Cada columna proxy tiene etiqueta `proxy` en `tipo_variable_fila`.
- [ ] Cada columna sintetica tiene etiqueta `sintetica` y la `regla_inyeccion` documentada.
- [ ] No existen dos versiones activas del tipo de cambio BCRP en el pipeline.

### Gate de modelos
- [ ] Los modelos se entrenan por producto (palta, uva, arandano) y no solo en dataset unificado.
- [ ] Existe un modelo base (baseline trivial: media historica) para comparar contra XGBoost/LightGBM.
- [ ] Optuna tiene un presupuesto de trials fijo documentado (no dejar corriendo indefinidamente).
- [ ] Las semillas estan fijadas: lista exacta definida antes del primer entrenamiento y no modificada despues.

Si algun item falla, el agente crea `codex-revision/BLOQUEO_gate.md` y espera instruccion.

---

## 12. Entrenamiento de algoritmos

### 12.1 Relacion con arquitectura de tesis

| Capa | Algoritmos | Objetivo |
|---|---|---|
| Capa 1 | LightGBM, XGBoost | Prediccion tabular de precio o volumen esperado. |
| Capa 2 | Isolation Forest, LOF, ECOD | Score de anomalia y alerta operacional. |
| Capa 3 | SHAP, TreeSHAP | Top-5 variables explicativas por alerta. |
| Capa 4 | RAG/LLM | Reporte tecnico trazable basado en evidencia. |

### 12.2 Objetivos de modelamiento

| Objetivo | Variable o salida |
|---|---|
| Prediccion de precio esperado | `precio_kg_usd` o precio derivado. |
| Prediccion de volumen esperado | `volumen_kg`. |
| Deteccion de anomalia | `score_anomalia`, `etiqueta_anomalia`. |
| Clasificacion de tipo de anomalia | `tipo_anomalia`, si es confiable. |
| Explicacion local | Top-5 variables SHAP. |
| Reporte tecnico | Markdown/PDF con evidencias y recomendaciones. |

### 12.3 Metricas

| Dimension | Metricas |
|---|---|
| Prediccion | MAE, RMSE, MAPE si aplica, R2 como apoyo. |
| Deteccion | ROC-AUC, PR-AUC, F1, precision, recall. |
| Anomalias desbalanceadas | PR-AUC como metrica prioritaria. |
| Explicabilidad | Estabilidad SHAP, cobertura Top-K, consistencia de variables. |
| Reportes | Rubrica de completitud, coherencia, accionabilidad, evidencia y consistencia. |
| Usabilidad | Tiempo-a-decision, comprension percibida, decisiones correctas. |

### 12.4 Comparaciones obligatorias

- IF vs LOF vs ECOD vs ensemble.
- Entrenamiento con datos reales vs reales + proxies.
- Con y sin variables sinteticas.
- Resultados por producto.
- Resultados globales ponderados por soporte.

## 13. Generacion de informes

Los informes deben generarse como evidencia metodologica y alimentar la tesis si cambian conclusiones o alcance.

| Informe | Contenido | Uso |
|---|---|---|
| `reporte-calidad-datos.md` | Cobertura, nulos, duplicados, outliers. | Metodologia/anexo. |
| `reporte-integracion-datasets.md` | Fuentes integradas y llaves usadas. | Trazabilidad. |
| `reporte-entrenamiento-modelos.md` | Modelos, parametros, metricas y comparaciones. | Resultados. |
| `reporte-explicabilidad-shap.md` | Variables relevantes, estabilidad y ejemplos. | Resultados/discusion. |
| `reporte-rag-alertas.md` | Calidad de reportes generados y evidencias. | Evaluacion de Capa 4. |
| `reporte-reformulacion-tesis.md` | Cambios necesarios al avance. | Gestion academica. |

Ubicacion recomendada:

`codex-revision/`

Si algun informe cambia la narrativa de la tesis, debe abrir una tarea de actualizacion en `docs/`.

## 14. Reformulacion del avance de tesis

El avance actual menciona una arquitectura basada en dataset agroexportador sintetico. La evidencia local sugiere reformular hacia una base integrada y trazable.

### 14.1 Ajustes recomendados

| Aspecto actual | Ajuste recomendado |
|---|---|
| Dataset sintetico como base central | Cambiar a dataset integrado con capas reales, proxies y sinteticas controladas. |
| Productos amplios incluyendo cacao | Mantener palta, uva, arandano; esparrago condicionado; cacao excluido. |
| Variables operativas como si fueran observadas | Marcar cada variable como real, proxy, derivada o sintetica. |
| SISAP como fuente de producto interno general | Presentar SISAP solo como mercado interno para palta, uva y esparrago. |
| Arandano con cobertura incompleta en SISAP | Soportarlo con SUNAT/ADUANET y Trade Map. |
| Reportes RAG generales | Anclarlos a SHAP, fuente, archivo y evidencia numerica. |

### 14.2 Documentos probables a revisar

- `docs/tesis.md`
- Capitulo de metodologia.
- Capitulo de experimentos.
- Capitulo de resultados.
- Anexos de datos.
- Anexo de uso de IA.
- `README.md` si describe dataset sintetico como unica fuente.

### 14.3 Nueva formulacion metodologica recomendada

La tesis debe declarar que el sistema se valida con un **dataset agroexportador integrado**, compuesto por:

1. Datos reales observados de exportacion.
2. Datos reales agregados institucionales.
3. Proxies publicos de clima, logistica, mercado interno y sanidad.
4. Variables sinteticas controladas solo para escenarios, balanceo o etiquetas experimentales.

### 14.4 Lo que el agente puede y no puede hacer respecto a la tesis

**PUEDE hacer:**
- Generar `codex-revision/reporte-reformulacion-tesis.md` con una lista de cambios recomendados, indicando el capitulo afectado, el texto actual (referenciado por seccion), y el texto sugerido.
- Indicar que tablas del Capitulo IV deben actualizarse con nuevas metricas, con los valores exactos a reemplazar.
- Detectar inconsistencias entre los datos reales y las afirmaciones del documento de tesis (ej: si el dataset final tiene 35,000 filas y la tesis dice 40,672, reportarlo).

**NO PUEDE hacer:**
- Editar directamente ningun archivo dentro de `docs/`.
- Cambiar el titulo, hipotesis, objetivos o estructura de capitulos sin aprobacion explicita del tesista.
- Reformular conclusiones del Capitulo V ni recomendaciones del Capitulo VII.
- Actualizar la portada, resumen o abstract.

**Formato del reporte de reformulacion:**
Cada cambio recomendado debe tener:
1. Archivo afectado (ruta exacta).
2. Seccion o tabla afectada.
3. Motivo del cambio (que dato nuevo lo justifica).
4. Texto o valor actual.
5. Texto o valor propuesto.
6. Prioridad: CRITICO / IMPORTANTE / SUGERIDO.

## 15. Cronograma operativo

| Fase | Nombre | Tareas | Salidas |
|---|---|---|---|
| 1 | Inventario y congelamiento | Confirmar fuentes canonicas, excluir colados, fijar productos. | Diccionario de fuentes canonicas. |
| 2 | Normalizacion TradeMap y SUNAT | Parsear `.xls` HTML, extraer ZIP/DBF, filtrar HS. | CSV TradeMap y SUNAT limpios. |
| 3 | Integracion de fuentes proxy | Integrar BCRP, SISAP, clima, logistica y sanidad por mes. | Tablas proxy normalizadas. |
| 4 | EDA y calidad | Nulos, duplicados, outliers, cobertura. | `reporte-calidad-datos.md`. |
| 5 | Dataset final y splits | Crear dataset final y particiones temporales. | CSV modelables. |
| 6 | Entrenamiento | Entrenar GBDT y detectores. | Modelos y metricas. |
| 7 | SHAP y reportes | Generar explicaciones y reportes RAG. | Reportes tecnicos. |
| 8 | Reformulacion tesis | Ajustar metodologia, datos, resultados y anexos. | Cambios en `docs/`. |

## 16. Criterios de aceptacion

El pipeline de datos se considerara listo cuando:

- Cada dataset tenga ruta, formato, estado y uso documentado.
- Cada variable del dataset final tenga fuente, granularidad y etiqueta metodologica.
- Palta, uva y arandano esten presentes como nucleo.
- Esparrago este validado o formalmente limitado.
- Cacao este excluido.
- Trade Map tenga CSV limpios solo de exportacion.
- SUNAT/ADUANET este normalizado para HS objetivo.
- SISAP este integrado solo como contexto interno.
- BCRP tenga una unica version canonica.
- Las variables sinteticas esten separadas y justificadas.
- El split temporal este implementado.
- Los reportes de calidad, integracion, entrenamiento, SHAP y RAG existan.
- La tesis tenga una narrativa coherente con los datos reales, proxies y sinteticos.

## 17. Salidas finales esperadas

| Salida | Ruta sugerida | Descripcion |
|---|---|---|
| Dataset final | `data/dataset_modelo_v_final.csv` | Base final para entrenamiento y evaluacion. |
| Dataset final versionado | `data/dataset_modelo_v_final_YYYY-MM-DD.csv` | Copia fechada reproducible. |
| TradeMap limpio | `codex-revision/data_processed/trademap/` | CSV de indicadores y series anuales. |
| SUNAT limpio | `codex-revision/data_processed/sunat/` | CSV de exportaciones HS objetivo. |
| Proxies integrados | `codex-revision/data_processed/proxies/` | BCRP, SISAP, clima, logistica, sanidad. |
| Splits | `codex-revision/data_processed/modeling/` | Train, validation, test e inference examples. |
| Reportes | `codex-revision/*.md` | Calidad, integracion, modelos, SHAP, RAG y reformulacion. |

## 18. Orden de implementacion recomendado

1. Crear `diccionario-fuentes-canonicas.md`.
2. Convertir Trade Map a CSV y excluir importaciones coladas.
3. Extraer SUNAT/ADUANET y filtrar HS objetivo.
4. Normalizar BCRP como tipo de cambio mensual.
5. Normalizar SISAP como contexto interno.
6. Agregar clima, logistica y sanidad como proxies.
7. Crear dataset integrado mensual y transaccional segun disponibilidad.
8. Ejecutar EDA y calidad.
9. Construir dataset final modelable.
10. Generar splits temporales.
11. Entrenar modelos.
12. Ejecutar SHAP.
13. Generar reportes RAG.
14. Reformular documentos de tesis en `docs/`.

## 19. Regla de oro metodologica

Ningun resultado de la tesis debe depender de una variable cuyo origen no este documentado.

Cada columna usada por los modelos debe responder:

- De que fuente viene.
- En que ruta local esta.
- Si es real observada, real agregada, proxy, derivada o sintetica.
- A que granularidad pertenece.
- Como se unio al dataset final.
- Que limitacion tiene.

Esta regla protege la defensa academica, reduce riesgo de alucinacion en reportes RAG y permite que SHAP explique variables comprensibles para supervisores operativos.

---

## 19.1 Entorno tecnico y convenciones de codigo

### Entorno
- Python 3.11+
- Todas las dependencias deben declararse en `requirements.txt` en la raiz del proyecto.
- No usar Jupyter Notebooks para el pipeline de produccion. Solo scripts `.py` en `src/` o `scripts/`.
- Los notebooks van en `notebooks/` y son solo exploracion, nunca fuente de datos para el dataset final.

### Librerias y prioridades

| Tarea | Libreria preferida | Alternativa |
|---|---|---|
| Leer DBF | `dbfread` | `simpledbf` |
| Leer XLS HTML disfrazado | `pd.read_html()` | `BeautifulSoup` |
| Leer XLS/XLSX normal | `openpyxl` | `xlrd` solo para .xls antiguo |
| HTTP requests | `httpx` con timeout explicito | `requests` |
| Encoding DBF legacy | `cp850`, probar `latin-1` si falla | — |
| Modelos GBDT | `lightgbm`, `xgboost` | — |
| Deteccion anomalias | `pyod` | — |
| SHAP | `shap` | — |
| Optimizacion HP | `optuna` | — |
| Validacion datos | `great_expectations` o validacion manual | — |

### Convenciones de nombres de archivos de salida

- Dataset final: `dataset_modelo_v_final_YYYY-MM-DD.csv`
- Splits: `train_raw_YYYY-MM-DD.csv`, `val_YYYY-MM-DD.csv`, `test_YYYY-MM-DD.csv`
- Reportes: `reporte-calidad-datos.md`, `reporte-integracion-datasets.md`
- Logs: `logs/YYYY-MM-DD_nombre-script.log`
- Modelos serializados: `models/modelo_producto_algoritmo_YYYY-MM-DD.pkl`
- Metricas: `codex-revision/results_metrics_YYYY-MM-DD.json`

### Manejo de encoding para archivos SUNAT

Los DBF de SUNAT usan codificacion CP850 o Latin-1. Usar siempre este patron:

```python
try:
    table = DBF(path, encoding='cp850')
except UnicodeDecodeError:
    table = DBF(path, encoding='latin-1', ignore_missing_memofile=True)
```

### Manejo de Trade Map XLS

Los archivos `.xls` de Trade Map son HTML exportados. Usar siempre:

```python
try:
    df = pd.read_excel(path, engine='openpyxl')
except Exception:
    dfs = pd.read_html(path)
    df = dfs[0]  # Primera tabla relevante
# Eliminar filas de totales o encabezados duplicados
df = df[~df.iloc[:, 0].astype(str).str.contains('Total|Reporter', na=False)]
```
