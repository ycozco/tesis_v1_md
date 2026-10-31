# Fuentes y factibilidad de recuperación
Comprobación: 31 de octubre de 2026 (Lima).

## Resultado
La búsqueda y gran parte de la descarga pueden automatizarse. No es necesario digitar operaciones manualmente. Se verificaron descargas reales, no solo páginas descriptivas. Falta comprobar continuidad, duplicados, revisiones y disponibilidad histórica antes de declarar construido el dataset.

## SUNAT / ADUANET — núcleo del experimento
Fuente: http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm
Referencia institucional: https://www.sunat.gob.pe/operatividadaduanera/index.html
El portal respondió por HTTP. HTTPS falló en este entorno. Publica diez ZIP de exportación, desde x17230826.zip hasta x19251026.zip. El texto anuncia publicación cada siete días y permanencia de dos meses; sin embargo se comprobaron archivos anteriores fuera del índice.
Pruebas positivas:
- x19251026.zip: ZIP válido, DBF con 44406 registros; 5725 coinciden con las tres subpartidas (palta 1247, uva 2003, arándano 2475).
- x25310526.zip: ZIP válido, DBF con 42581 registros; 3981 coinciden (palta 2757, uva 1056, arándano 168). Guardado como historico-prueba.bin y DBF extraído.
- x06120125.zip y x01070124.zip: descargados y verificados como archivos ZIP con DBF.
Los DBF inspeccionados incluyen PART_NANDI, CPAIDES, VFOBSERDOL, VPESNET, FNUM, FEMB, FECH_RECEP, identificadores y series. Es posible obtener FOB/kg directamente de FOB y peso observados, sin precios simulados.
Las fechas de embarque dentro de un paquete abarcan periodos anteriores a la semana de publicación. Un ZIP semanal no equivale a operaciones ocurridas exclusivamente esa semana. Deben definirse fecha analítica, llave declaración-serie y reglas para revisiones/duplicados, y conservar fecha de descarga y archivo fuente.
Los resultados filtrados de muestra están en *-tres-productos.json; no constituyen todavía el dataset científico.
No se ha verificado disponibilidad continua 2018–2026 ni la semántica documental de todas las fechas. Los históricos no listados requieren inventario y validación; si hay huecos, recuperar respaldos o solicitar datos.

## BCRP — tipo de cambio
Documentación: https://estadisticas.bcrp.gob.pe/estadisticas/series/documentos/bcrpdataapi.pdf
Serie: PN01207PM, promedio mensual interbancario.
La API está documentada, pero en la prueba devolvió una página anti-bot “Pardon Our Interruption” con HTTP 200, no JSON. bcrp.txt conserva esa evidencia; no contiene datos válidos.
Estado: automatizable como servicio, descarga no conseguida en esta sesión. Puede requerir acceso normal desde navegador y exportación manual. No se intentó eludir el control.
La fecha del mes no acredita por sí sola disponibilidad del dato al origen del pronóstico.

## MIDAGRI / SISAP — precios internos
Fuente: http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/
Endpoint de consulta observado en el código y comprobado: http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrar
Se obtuvo el formulario y una respuesta real por POST: palta, mercado 15011502, enero de 2025, precio promedio mensual. La tabla devuelve variedades y valores, entre ellos palta Hass 4.35 en la unidad declarada S/ por kg para esa consulta. Guardada en sisap-palta-prueba.html.
Estado: automatización comprobada para esta consulta. Falta inventario de cobertura y variedades; no se acreditó cobertura de arándano.
Estos precios corresponden al mercado interno y no sustituyen FOB ni precio recibido por productor.
Respaldo institucional: https://www.gob.pe/institucion/midagri/campa%C3%B1as/3432-precios-de-productos-a-tu-alcance

## NASA POWER — clima contextual opcional
Documentación: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
Prueba positiva: JSON real, siete días (1–7 enero 2025), T2M_MAX, T2M_MIN, PRECTOTCORR, RH2M, punto -16.4/-71.54. Archivo nasa-muestra.json.
Estado: automatización comprobada. Es una muestra técnica, no un enlace validado con las exportaciones. No debe inferirse lugar de producción a partir de la aduana.

## UN Comtrade — contraste o alternativa mensual
Documentación: https://uncomtrade.org/docs/un-comtrade-api/
Prueba positiva de API pública preview: Perú 604, exportaciones, enero de 2025, HS 080440, socio mundo. JSON con una observación, FOB y peso neto. Archivo comtrade-muestra.json.
Estado: automatización comprobada para preview; el acceso más amplio puede requerir cuenta/API key. Frecuencia mensual/anual; no recupera series semanales ni debe desagregarse artificialmente a semanas. HS6 no garantiza exactamente la delimitación de la subpartida nacional; revisar especialmente 081040.

## Si el histórico no se recupera: solicitud institucional
Agromercado: https://facilita.gob.pe/t/1765
Servicio: https://www.gob.pe/11567-solicitar-informacion-estadistica-agropecuaria-de-comercio-exterior
El formulario permite solicitar información agropecuaria de comercio exterior y anuncia respuesta en 15 días. No garantiza de antemano la granularidad solicitada.
Texto de requerimiento sugerido: exportación definitiva, subpartidas 0804400000, 0806100000 y 0810400000; periodo 2018–2026 con fecha de corte explícita; fecha de embarque y numeración, destino, valor FOB USD, peso neto kg, identificador de declaración y serie o agregación semanal compatible; diccionario de campos, cobertura, revisiones y fechas de actualización/publicación. Solicitar CSV o XLSX. No se envió solicitud alguna.

## Decisión práctica
1. Recuperar automáticamente archivos SUNAT accesibles y auditar por fecha real, producto y destino.
2. Conciliar con respaldos previos para localizar faltantes y revisiones.
3. Integrar BCRP solo tras obtener una descarga válida; SISAP solo donde haya cobertura compatible.
4. Mantener clima como opcional hasta justificar localización.
5. Solicitar los huecos históricos si persisten; usar Comtrade para contrastar agregados o reformular a frecuencia mensual antes del test, si fuese necesario.

No se ejecutaron los scripts antiguos del repositorio ni se mezclaron estas muestras con el dataset experimental.
