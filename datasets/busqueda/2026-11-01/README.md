# Búsqueda de datos pendientes — 1 de noviembre de 2026

Se hizo una búsqueda acotada y reproducible de seis enlaces semanales históricos de SUNAT. Los nombres se derivaron del patrón observado y del calendario semanal; solo las respuestas positivas prueban existencia. Un 404 de un enlace no demuestra ausencia del año completo ni agotamiento de todas las vías de recuperación.

## Recuperado físicamente

| Paquete | Resultado | Filas de los tres productos |
|---|---|---:|
| x03090122.zip | ZIP y DBF válidos | 3.750 |
| x02080123.zip | ZIP y DBF válidos | 4.829 |

Los 8.579 registros contienen 8.334 claves candidatas distintas; 8.321 no estaban en la colección anterior y 13 sí. Hay 243 claves repetidas en los nuevos archivos, que deben conciliarse por versiones, no eliminarse ciegamente. Los identificadores usan la misma concatenación textual de campos DBF y SHA256 que la extracción anterior; siguen siendo claves operativas, no una certificación del diccionario oficial.

Productos: uva 5.422, arándano 2.239 y palta 918. Fechas de embarque: 2019-12-18–2023-01-04, distribuidas en 2019 (1 fila), 2021 (3.945), 2022 (4.574) y 2023 (59). **El año del paquete no equivale al año de sus embarques.** Las 8.321 claves nuevas no son 8.321 semanas nuevas, ni necesariamente incrementos netos tras conciliación de declaraciones.

La revisión básica encontró cero números inválidos, pesos no positivos, FOB negativos o fechas inválidas. Eso no certifica validez económica, cobertura ni disponibilidad histórica. `historicos-candidatos.csv` conserva archivo, fila y campos analíticos sin nombres, RUC ni domicilios. Los ZIP/DBF originales permanecen exclusivamente en `data/busqueda_2026-11-01`, ignorado por Git.

## Aún no recuperado o no acreditado

- x01070118.zip, x31060119.zip, x30050120.zip y x28030121.zip devolvieron HTTP 404. Son seis pruebas de disponibilidad, no un inventario exhaustivo 2018–2026.
- El enlace institucional `estructura_bases.xls` sigue devolviendo 404. `procedimiento.doc` respondió 200 y su SHA256 coincide con el procedimiento ya conservado: no aporta un nuevo diccionario.
- `totales_2011.xls` respondió 200, pero corresponde a otra época y se conserva solo localmente; no completa el periodo de la tesis.
- BCRP sigue sin descarga actual válida por control anti-bot en la verificación anterior de esta fecha; quedan los 102 meses respaldados hasta junio de 2026. No se intentó eludir controles ni se atribuyeron fechas de publicación.
- SISAP: faltan unidad específica y disponibilidad histórica, y no se identificó serie de arándano. NASA: falta origen productivo justificable. Ninguna búsqueda documental permite convertir esos supuestos en hechos.
- La [Plataforma Nacional de Datos Abiertos / MINCETUR](https://www.datosabiertos.gob.pe/dataset/comercio-exterior-de-bienes-ministerio-de-comercio-exterior-y-turismo-mincetur/resource-4) aparece en el índice con recursos 2019–2024 y diccionario. La apertura devolvió 403; no se descargó ni verificó su granularidad. Se documenta como vía pendiente, no como datos disponibles.

## Decisión y siguiente paso

Conservar los históricos como **entrada candidata separada**. Antes de incorporarlos hay que ejecutar conciliación contra todos los snapshots, respetar revisiones de la declaración completa, revisar las claves repetidas y rehacer cobertura y manifiestos. Después se generará una nueva versión del panel y, si cambia la elegibilidad, un nuevo calendario antes de test. No se modificaron el panel ni las métricas del piloto del 1 de noviembre para introducir estas filas sin esa revisión.

En paralelo se avanzó la UI con el corte ya verificado. La pantalla Fuentes muestra explícitamente los nuevos paquetes pendientes de incorporación. El estado experimental y las métricas siguen refiriéndose al panel conservador de 22 paquetes.

Reproducción: `python -B tools/search_pending_data.py`. Las descargas futuras pueden cambiar; conservar el manifiesto y comparar hashes. `manifest-busqueda.json` fija URLs, fecha UTC, HTTP, tamaño y SHA256; `comparacion-con-coleccion.json` fija el contraste de claves. La solicitud institucional de cobertura, diccionario y publicaciones sigue pendiente de envío; no se enviaron comunicaciones a terceros.
