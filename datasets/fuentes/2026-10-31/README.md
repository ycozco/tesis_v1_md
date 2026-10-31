# Recopilación verificada de fuentes — 31 de octubre de 2026

Esta entrega contiene 71810 filas de palta, uva fresca y arándano extraídas de 13 paquetes oficiales de SUNAT. Es una recopilación parcial y multiversión, NO el dataset experimental final ni una serie semanal completa.

## Contenido

- observaciones-sunat.csv: FOB USD, peso neto kg, FOB/kg, destino, fechas originales y procedencia por archivo/fila. No incluye nombres, RUC ni direcciones. El identificador de declaración-serie se conserva mediante SHA-256.
- manifest-sunat.json: URLs originales, tamaños, hashes, resultados por paquete y controles.
- cobertura-observada.json: recuentos y fechas de embarque observadas por producto/destino; no acredita cobertura completa ni disponibilidad en tiempo real.
- muestras-contextuales/: respuestas de NASA POWER, SISAP y UN Comtrade verificadas previamente. Son muestras técnicas separadas, no covariables integradas.
- informe-fuentes.md: búsqueda y factibilidad de acceso.
- hashes.json: hashes de los archivos de esta entrega.

## Resultado y limitaciones

Se identificaron 61780 claves de declaración-serie. Hay 6793 repeticiones exactas de los campos extraídos y 3185 claves con versiones distintas; se preservaron todas las filas para no resolver revisiones arbitrariamente. No sumar este CSV directamente: primero definir selección de versiones, deduplicación y fecha analítica. La llave candidata se forma con CADU, FANO, NDCL y NSER; su suficiencia debe validarse contra el diccionario SUNAT. Las fechas se conservan como cadenas originales; su semántica debe confirmarse antes de modelar.

Los 13 paquetes incluyen diez publicados en el índice actual (agosto–octubre de 2026) y tres muestras históricas de enero de 2024, enero de 2025 y mayo de 2026. No representan todas las semanas 2018–2026. Fechas de embarque antiguas dentro de un paquete no demuestran continuidad histórica. Todos los registros seleccionados tienen valores numéricos FOB no negativos y peso positivo; este control físico no certifica calidad integral.

BCRP quedó pendiente: la consulta devolvió HTML de protección anti-bot en lugar de JSON. No se incluyó como dato válido. NASA utiliza un punto ilustrativo de Arequipa: no está enlazado al origen productivo. SISAP corresponde a precios internos; Comtrade a datos mensuales. No convertir esos datos en exportaciones semanales artificiales.

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
