# Recopilación verificada de fuentes — 31 de octubre de 2026

Esta entrega contiene 110253 filas de palta, uva fresca y arándano extraídas de 22 paquetes oficiales de SUNAT. Es una recopilación parcial y multiversión, NO el dataset experimental final ni una serie semanal completa.

## Contenido

- observaciones-sunat.csv: FOB USD, peso neto kg, FOB/kg, destino, fechas originales y procedencia por archivo/fila. No incluye nombres, RUC ni direcciones. El identificador de declaración-serie se conserva mediante SHA-256.
- manifest-sunat.json: URLs originales, tamaños, hashes, resultados por paquete y controles.
- cobertura-observada.json: recuentos y fechas de embarque observadas por producto/destino; no acredita cobertura completa ni disponibilidad en tiempo real.
- muestras-contextuales/: respuestas de NASA POWER, SISAP y UN Comtrade verificadas previamente. Son muestras técnicas separadas, no covariables integradas.
- informe-fuentes.md: búsqueda y factibilidad de acceso.
- hashes.json: hashes de los archivos de esta entrega.
- incorporacion-respaldo.json: conciliación de las colecciones y paquetes recuperados.

## Resultado y limitaciones

Se identificaron 93298 claves de declaración-serie. Hay 9811 repeticiones exactas de los campos extraídos y 7019 claves con versiones distintas; se preservaron todas las filas para no resolver revisiones arbitrariamente. No sumar este CSV directamente: primero definir selección de versiones, deduplicación y fecha analítica. La llave candidata se forma con CADU, FANO, NDCL y NSER; su suficiencia debe validarse contra el diccionario SUNAT. Las fechas se conservan como cadenas originales; su semántica debe confirmarse antes de modelar.

Los 22 paquetes incluyen diez de marzo–mayo de 2026 recuperados del respaldo anterior, diez de agosto–octubre de 2026 y dos muestras de enero de 2024 y enero de 2025. El paquete de mayo presente en ambas colecciones se incorporó una sola vez y coincide por SHA-256. No representan todas las semanas 2018–2026. Fechas de embarque antiguas dentro de un paquete no demuestran continuidad histórica. Todos los registros seleccionados tienen valores numéricos FOB no negativos y peso positivo; este control físico no certifica calidad integral.

La consulta nueva de BCRP devolvió HTML anti-bot y no se incluyó como dato válido. La revisión posterior encontró una caché anterior con 101 meses numéricos (enero de 2018–mayo de 2026) en D:/tesis_yoset/data/bcrp/exchange_rates_cache.json: queda pendiente validar e incorporar esa caché; no falta todo el histórico. NASA utiliza un punto ilustrativo de Arequipa: no está enlazado al origen productivo. SISAP corresponde a precios internos; Comtrade a datos mensuales. No convertir esos datos en exportaciones semanales artificiales.

## Fuentes

- SUNAT: http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm
- Portal institucional: https://www.sunat.gob.pe/operatividadaduanera/index.html
- SISAP: http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/
- NASA: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- Comtrade: https://uncomtrade.org/docs/un-comtrade-api/

## Reproducibilidad y almacenamiento

Los ZIP originales se conservan solo localmente en data/fuentes_2026-10-31/sunat/ (directorio excluido de Git) y en la copia local de drive. La carpeta remota de Drive recibe únicamente la extracción filtrada y documentación. El manifiesto conserva sus URLs y hashes. GitHub incluye la extracción sin identificadores personales directos y el código, evitando publicar los originales que contienen nombres y direcciones.

Con Node.js, desde la raíz del repositorio y después de recuperar los ZIP y extraer sus DBF en esa carpeta:

    powershell -File tools/download_sunat_collection.ps1
    node tools/ingest_sunat_dbf.mjs .
    node tools/verify_sunat_collection.mjs .

La extracción no entrena modelos, no completa ceros, no imputa variables ni genera datos sintéticos. La verificación comprueba estructura, hashes originales y conteos; no certifica pertinencia científica ni cobertura histórica.

Drive: https://drive.google.com/drive/folders/14H1M-gkaHlfzT-mgy9Pt2bECEBwoPKVC

## Conciliación ejecutada

La entrada de 110253 filas permanece intacta. Se generó [una vista conciliada de 93225 series](conciliacion/vista-conciliada.csv), con 108 filas (73 series de 25 declaraciones) en cuarentena. Las reglas oficiales de reemplazo por declaración se aplicaron al último paquete disponible. Véanse [protocolo](conciliacion/protocolo.md), [informe](conciliacion/informe.md) y [decisiones](conciliacion/decisiones.csv). No es todavía un dataset experimental ni una reconstrucción acreditada de disponibilidad en tiempo real.

    python -B tools/reconcile_sunat.py .
    python -B tools/verify_sunat_reconciliation.py .
