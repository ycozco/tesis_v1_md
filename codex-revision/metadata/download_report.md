# Reporte de descarga completa de fuentes

Actualizado: 2026-06-07
Workspace: `d:\tesis_yoset\codex-revision`

## Resumen

- Entradas de manifiesto: 341
- Descargados/generados: 329
- Errores/bloqueos HTTP: 12
- Bytes descargados/generados: 1049210854

## Resumen por fuente

| Fuente | Archivos OK | Errores | MB |
|---|---:|---:|---:|
| ADUANET | 53 | 0 | 588.17 |
| FAOSTAT | 4 | 0 | 297.34 |
| MIDAGRI | 21 | 0 | 72.32 |
| APN | 83 | 0 | 18.35 |
| WORLD_BANK | 20 | 1 | 11.89 |
| SENAMHI | 51 | 3 | 6.38 |
| OSITRAN_PNDA | 62 | 0 | 2.34 |
| PROMPERU | 9 | 0 | 1.43 |
| NASA_POWER | 5 | 0 | 1.22 |
| OSITRAN | 7 | 2 | 0.58 |
| SUNAT | 1 | 0 | 0.22 |
| RASFF | 2 | 0 | 0.17 |
| SENASA | 3 | 0 | 0.09 |
| FDA | 3 | 0 | 0.08 |
| INEI | 2 | 0 | 0.01 |
| BCRP | 2 | 0 | 0.01 |
| SISAP_MIDAGRI | 1 | 1 | 0.00 |
| ITC | 0 | 1 | 0.00 |
| UN_COMTRADE | 0 | 4 | 0.00 |

## Errores o bloqueos

- `SENAMHI` / `linked_file` / `http_error` / HTTP `404`: https://www.senamhi.gob.pe/site/descarga-datos/site/volcan/ :: <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
</body></html>

- `SENAMHI` / `linked_file` / `http_error` / HTTP `404`: https://www.senamhi.gob.pe/site/descarga-datos/site/incendio/ :: <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
</body></html>

- `SENAMHI` / `linked_file` / `http_error` / HTTP `404`: https://www.senamhi.gob.pe/site/descarga-datos/site/incendio :: <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
</body></html>

- `OSITRAN` / `php` / `http_error` / HTTP `400`: https://www.facebook.com/sharer/sharer.php?u=https://www.gob.pe/104704-acceder-a-datos-abiertos-de-puertos-del-ositran-en-la-plataforma-nacional-de-datos-abiertos-pnda :: <!DOCTYPE html><html lang="en" id="facebook"><head><title>Error</title><meta charset="utf-8" /><meta http-equiv="Cache-Control" content="no-cache" /><meta name="robots" content="noindex,nofollow" /><style nonce="HGQP1eCX
- `OSITRAN` / `linked_file` / `error` / HTTP ``: mailto:?subject=Acceder a datos abiertos de puertos del Ositrán en la Plataforma Nacional de Datos Abiertos (PNDA)&body=Hola! te comparto esta página: https%3A%2F%2Fwww.gob.pe%2F104704-acceder-a-datos-abiertos-de-puertos-del-ositran-en-la-plataforma-nacional-de-datos-abiertos-pnda :: InvalidSchema: No connection adapters were found for 'mailto:?subject=Acceder a datos abiertos de puertos del Ositrán en la Plataforma Nacional de Datos Abiertos (PNDA)&body=Hola! te comparto esta página: https%3A%2F%2Fw
- `SISAP_MIDAGRI` / `portal_https` / `error` / HTTP ``: https://sistemas.midagri.gob.pe/sisap/portal/ :: SSLError: HTTPSConnectionPool(host='sistemas.midagri.gob.pe', port=443): Max retries exceeded with url: /sisap/portal/ (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (
- `ITC` / `trade_map` / `http_error` / HTTP `403`: https://www.intracen.org/resources/tools/trade-map :: <!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=Edge"><meta name="robots" content="
- `WORLD_BANK` / `pink_sheet_csv_candidate` / `http_error` / HTTP `404`: http://pubdocs.worldbank.org/en/561011504107123456/CMO-Historical-Data-Monthly.csv :: 
    


<!DOCTYPE html>
<html lang="en">
<head>
     

<meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <script defer="defer" type="text/javascript" src="https://rum.hlx.page/.rum/@adobe/helix-rum-js@%5E2/dist
- `UN_COMTRADE` / `palta_080440_annual_exports` / `http_error` / HTTP `401`: https://comtradeapi.un.org/data/v1/get/C/A/HS?reporterCode=604&period=2018,2019,2020,2021,2022,2023,2024,2025,2026&cmdCode=080440&flowCode=X&partnerCode=0 :: { "statusCode": 401, "message": "Access denied due to missing subscription key. Make sure to include subscription key when making requests to an API." } | API may require subscription key or changed endpoint
- `UN_COMTRADE` / `uva_080610_annual_exports` / `http_error` / HTTP `401`: https://comtradeapi.un.org/data/v1/get/C/A/HS?reporterCode=604&period=2018,2019,2020,2021,2022,2023,2024,2025,2026&cmdCode=080610&flowCode=X&partnerCode=0 :: { "statusCode": 401, "message": "Access denied due to missing subscription key. Make sure to include subscription key when making requests to an API." } | API may require subscription key or changed endpoint
- `UN_COMTRADE` / `arandano_081040_annual_exports` / `http_error` / HTTP `401`: https://comtradeapi.un.org/data/v1/get/C/A/HS?reporterCode=604&period=2018,2019,2020,2021,2022,2023,2024,2025,2026&cmdCode=081040&flowCode=X&partnerCode=0 :: { "statusCode": 401, "message": "Access denied due to missing subscription key. Make sure to include subscription key when making requests to an API." } | API may require subscription key or changed endpoint
- `UN_COMTRADE` / `esparrago_070920_annual_exports` / `http_error` / HTTP `401`: https://comtradeapi.un.org/data/v1/get/C/A/HS?reporterCode=604&period=2018,2019,2020,2021,2022,2023,2024,2025,2026&cmdCode=070920&flowCode=X&partnerCode=0 :: { "statusCode": 401, "message": "Access denied due to missing subscription key. Make sure to include subscription key when making requests to an API." } | API may require subscription key or changed endpoint

## Archivos de control

- `metadata/download_manifest.json`
- `metadata/download_manifest.csv`