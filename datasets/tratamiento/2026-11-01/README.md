# Tratamiento y revisión de los seis pendientes

Fecha: 1 de noviembre de 2026. Estado: avance ejecutado y verificable; experimento final pendiente. No se actualizaron resultados de capítulos de la tesis ni se ejecutó el test reservado.

## 1. Panel semanal y cobertura — implementado, cobertura aún incompleta

Se agregaron por producto–destino–semana ISO las vistas conservadora (93.225 registros) y de sensibilidad (93.298). Ambas producen 3.268 celdas observadas en 133 combinaciones. El calendario entre primera y última observación de cada combinación contiene 14.683 celdas: 11.415 permanecen desconocidas. No son exportaciones cero. Incluso las celdas observadas se marcan `observed_partial`: no se acredita cobertura completa de las operaciones de esa semana.

La fecha analítica es FEMB, fecha de embarque; el lunes identifica la semana ISO. Es una elección retrospectiva documentada, sin equiparar embarque a disponibilidad pública. El valor unitario es suma FOB / suma peso neto. No se promedian precios por operación. Las 205 filas con valores unitarios extremos quedan identificadas para revisión, sin excluirlas ni corregir sus valores.

El calendario común provisional propone desarrollo 2025-10-27–2026-04-20 y reserva 2026-04-27–2026-10-19. Se eligió por fechas, sin resultados del test. Requiere congelación y evaluación de suficiencia antes del experimento definitivo; la última semana recuperada está incompleta. No certifica información disponible históricamente.

## 2. Covariables — recuperación real, elegibilidad pendiente

| Fuente | Recuperación realizada | Límite restante |
|---|---|---|
| BCRP | Caché original de 101 meses, más CSV antiguo: 17 meses solapados coinciden y junio de 2026 amplía a **102 meses, enero de 2018–junio de 2026** | La API actual devuelve control anti-bot. Los respaldos no prueban fechas de publicación ni vintages; falta julio de 2026 en adelante y revisión remota |
| SISAP | Respuestas HTML preservadas, 106 meses por producto, palta y uva, 29 variedades en conjunto; **1.890 celdas numéricas y 1.184 faltantes** | Encabezado genérico de unidades: validar unidad concreta. No se identificó arándano ni disponibilidad histórica; precio interno no equivale a FOB |
| NASA POWER | **3.217 días × 4 parámetros**, 2018-01-01–2026-10-22, punto −16,4/−71,54 | Solo contexto geográfico. No demuestra origen productivo de exportaciones ni publicación histórica |

Las consultas, parámetros, hora UTC, HTTP, tamaños y SHA256 se conservan en `contexto/manifest-recuperacion.json`. SISAP exige meses con dos dígitos: se corrigió la consulta antes de conservar la descarga final. Las celdas faltantes no se imputan. Las covariables recuperadas **no se incorporan todavía a los modelos** y se marcan `eligible_asof=false`; un retardo supuesto no sustituye evidencia de publicación.

Fuentes institucionales: [API BCRP, serie PN01207PM](https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json/2018-1/2026-10/esp), [SISAP](http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/), [NASA POWER: API y coordenadas](https://power.larc.nasa.gov/docs/services/api/temporal/). Los ZIP SUNAT y la conciliación previa conservan su procedencia en `datasets/fuentes/2026-10-31`.

## 3. Código, características y cortes — corregidos en nueva ruta

`pipeline/research/protocol.py` y `tools/build_research_data.py` consumen las vistas conciliadas, limitan a tres productos y producen Parquet. Mantienen semanas faltantes, rezagos calendarios y ventanas completas. No usan sintéticos, backward fill ni constantes climáticas.

La emisión es al inicio de la semana objetivo; se usa historia hasta la semana previa y se entrena únicamente con objetivos que ya habrían terminado. L=0/4/8 retrasa **características y disponibilidad de etiquetas de entrenamiento/calibración**. La referencia estacional mantiene exactamente objetivo−52 semanas bajo todos los retardos. Estas son sensibilidades simuladas de disponibilidad, no una reconstrucción as-of certificada.

La entrada habitual de `prepare_weekly_dataset.py` dirige a esta construcción. El pronóstico antiguo bloquea ejecución directa por defecto. `--legacy-prototype` conserva acceso explícito al prototipo histórico; otras funciones y orquestadores antiguos siguen siendo históricos y no validan el protocolo actual.

## 4. Pronóstico e incertidumbre — piloto de desarrollo ejecutado

Se generaron **34.060 filas de predicción**: referencias naive, media de cuatro semanas y estacional 52, XGBoost y LightGBM, dos objetivos, dos vistas y tres retardos. La cifra cuenta métodos, vistas y retardos; no son 34.060 observaciones independientes. Reajuste por cada fecha común de emisión; ninguna predicción del test reservado. Una configuración pequeña por biblioteca sirve para probar el flujo; **no sustituye la pequeña grilla final de la tesis**.

MAE macro da igual peso a cada combinación producto–destino. `metricas-emparejadas-piloto.csv` compara cada modelo y referencia exclusivamente sobre sus mismas filas disponibles. No comparar como equivalentes los MAE sin emparejar cuando cambian los tamaños o destinos. La selección de biblioteca es exploratoria y solo de desarrollo; no confirma H1.

Se implementó cuantíl empírico de errores absolutos previos de la misma serie para 90/95 %, con ventana expansiva y últimos 52 errores. Se exige al menos 40. **No se emitió ningún intervalo: el desarrollo de 26 semanas no reúne 40 errores anteriores por serie.** No se inventaron bandas ni se agruparon destinos para eludir el mínimo. Falta ampliar historia utilizable/calibración y fijar grilla, criterios de elegibilidad, MASE y denominadores estacionales, cobertura y protocolo final antes de abrir test.

## 5. H3 y SHAP — pruebas técnicas y piloto, evaluación parcial

Pasaron **24 verificaciones de aditividad TreeSHAP** sobre muestras de los modelos realmente ajustados de ambos objetivos, dos vistas y L=0/4/8. Se verifica salida cruda en escala original, con tolerancia relativa al tamaño de la salida; no se atribuye automáticamente la predicción truncada ni se interpreta causalidad.

H3 puntuó **450 casos** con IF/LOF/ECOD, ensemble de rangos y referencia de residuo absoluto, y produjo 300 comparaciones de solapamiento. Los detectores se ajustan con residuos de fechas anteriores, normalizados por historia anterior de cada serie, mínimo piloto de ocho errores y MAD positivo. Casos indeterminados permanecen fuera de la población común, sin forzar scores. K=ceil(0,05×N) es común a los detectores en cada fecha/objetivo; con N pequeño no equivale exactamente a 5 %.

Es una caracterización retrospectiva exploratoria de desarrollo; los residuos actuales solo existen después del cierre de su semana objetivo. La biblioteca supervisada fue elegida en el mismo desarrollo, por lo que no representa evaluación independiente. Falta referencia estacional H3, persistencia, desglose de indeterminados y diseño definitivo de sensibilidad. No hay etiquetas reales de anomalía, fraude ni causalidad.

## 6. H4, persistencia y librerías — corregido y preparado, integración parcial

Se prepararon 30 casos con hechos reales de agregados semanales, diez por producto, trazables a la vista conservadora por hash, producto, destino y semana. Hay 180 posiciones únicas (dos configuraciones × tres repeticiones). Todas tienen `not_executed` y salida nula: **no son 180 reportes ni una evaluación H4 concluida**. Falta revisar dificultad y clave factual, congelar corpus/modelo/prompts, generar y evaluar a ciegas con cobertura, abstenciones, errores numéricos y errores factuales separados.

El verificador atómico nuevo exige identificador del hecho, fuente, unidad y tolerancia absoluta de media última cifra decimal (0,005 para dos decimales). El validador textual antiguo también usa ahora tolerancia absoluta y reconoce que presencia de cifras no demuestra sustento factual. Cero reportes produce resultado no evaluable, en lugar de fidelidad perfecta.

Se ejecutó recuperación BM25 real contra corpus documental local y se conservaron fragmentos con fuentes/hashes. No se probó todavía embedding denso ni recuperación PostgreSQL/pgvector.

FastAPI/Uvicorn y dependencias adicionales se instalaron **solo en `data/runtime-api` local**, conservando el entorno antiguo. Se corrigió el arranque de Settings al leer variables adicionales del dotenv compartido y se ocultan entradas en errores de validación. Se verificaron GET `/health` y `/api/migration/status` con SQLite en memoria. No se conectó PostgreSQL: Docker Desktop no tiene motor activo. Tampoco se validaron autenticación, dashboard con datos reales ni servidor de red Uvicorn.

`environment-observed.json`, `environment-api-observed.json` y los dos archivos de requisitos observados registran versiones efectivamente utilizadas. Son inventarios fijados del piloto en Python 3.14.2, **no una instalación limpia reproducida**. Los requirements históricos siguen identificados como tales; CatBoost no se añade al contraste principal por permanecer en una lista vieja.

## Reproducción y evidencia

Desde raíz del repositorio, con el intérprete auditado:

```powershell
$pythonTesis = 'D:/tesis_yoset/.venv/Scripts/python.exe'
& $pythonTesis -B tools/build_research_data.py
& $pythonTesis -B tools/reconcile_bcrp_cache.py
& $pythonTesis -B tools/recover_context_data.py
& $pythonTesis -B tools/normalize_context_data.py
& $pythonTesis -B tools/run_research_pilot.py
& $pythonTesis -B tools/prepare_h3_h4.py
& $pythonTesis -B tools/verify_research_delivery.py
& $pythonTesis -B -m pytest tests/unit/test_research_protocol.py tests/reporting/test_reports.py -q -p no:cacheprovider
```

La recuperación de respaldos BCRP depende de los originales D:; las copias exactas preservadas permiten inspección aun sin ese disco. Las descargas pueden cambiar con revisiones futuras: contrastar manifiestos, no sobrescribir evidencia histórica sin registrar una nueva versión. Para probar API se requiere también el suplemento local registrado; SQLite no representa PostgreSQL.

La verificación independiente recalcula agregados desde las filas fuente, comprueba unicidad, faltantes no convertidos a ceros, ausencia de predicciones del test, mínimo de calibración, casos H4 sin resultados inventados y dos rutas API. Nueve pruebas específicas pasaron. `hashes.json` fija los archivos de esta entrega salvo el propio listado.

## Pendientes que requieren nueva evidencia

1. Obtener cobertura SUNAT histórica continua o una certificación de cobertura más acotada. Las semanas desconocidas no se solucionan instalando librerías. Si se solicita información institucional, debe incluir diccionario, revisiones y fechas de publicación; no se envió solicitud.
2. Cerrar publicación/vintages y unidades de covariables; validar origen antes de asignar clima. H2 puede resultar no evaluable en determinadas combinaciones.
3. Congelar elegibilidad, calendario y grilla final antes de test, y reunir historia suficiente para calibrar. El piloto actual no prueba superioridad predictiva.
4. Completar caracterización H3 y evaluación H4 humana; activar un entorno PostgreSQL/pgvector y probar persistencia, reconstrucción y recuperación densa de extremo a extremo.

El avance corrige bloqueos de software y recupera datos reales; no convierte esos pendientes metodológicos en resultados concluidos.
