#!/usr/bin/env python3
"""
src/scrape_sunat_all.py
=======================
Web scraper para descargar todos los archivos ZIP (exportaciones, importaciones A y B,
informes de verificación) disponibles en el portal de SUNAT de bases definitivas.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import os
import logging
from pathlib import Path
import requests
from lxml import html

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Configuración de rutas
DATA_DIR = Path("data")
SUNAT_DIR = DATA_DIR / "sunat"
RAW_DIR = SUNAT_DIR / "raw_downloads"
RAW_DIR.mkdir(parents=True, exist_ok=True)

PAGE_URL = "http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm"
BASE_HOST = "http://www.aduanet.gob.pe"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_and_download():
    log.info("Accediendo a la página de bases de datos de SUNAT: %s", PAGE_URL)
    try:
        res = requests.get(PAGE_URL, headers=HEADERS, timeout=20)
        if res.status_code != 200:
            log.error("Fallo al acceder a la página. Código de respuesta HTTP: %d", res.status_code)
            return
    except Exception as e:
        log.error("Error al conectar con la página de SUNAT: %s", e)
        return

    # Parsear HTML
    tree = html.fromstring(res.content)
    links = tree.xpath("//a/@href")
    log.info("Total de enlaces encontrados en la página: %d", len(links))

    # Filtrar enlaces de archivos ZIP
    zip_links = []
    for link in links:
        link_lower = link.lower()
        if ".zip" in link_lower or "zip" in link_lower:
            zip_links.append(link)

    log.info("Total de archivos ZIP identificados para descargar: %d", len(zip_links))

    downloaded_count = 0
    skipped_count = 0
    failed_count = 0

    for i, link in enumerate(zip_links, 1):
        # Normalizar barras diagonales de Windows (\ -> /)
        normalized_link = link.replace("\\", "/")
        
        # Construir URL absoluta
        if normalized_link.startswith("/"):
            url = BASE_HOST + normalized_link
        elif normalized_link.startswith("http"):
            url = normalized_link
        else:
            url = f"{BASE_HOST}/aduanas/informae/{normalized_link}"

        # Obtener el nombre del archivo local
        filename = normalized_link.split("/")[-1]
        
        # Corregir extensión .zip si viene mal formateada (ej. idv20260426zip -> idv20260426.zip)
        if not filename.endswith(".zip") and "zip" in filename:
            filename = filename.replace("zip", ".zip")
        
        dest_path = RAW_DIR / filename

        # Si el archivo ya existe localmente, omitir
        if dest_path.exists():
            log.info("[%d/%d] Omitiendo %s (ya existe localmente)", i, len(zip_links), filename)
            skipped_count += 1
            continue

        log.info("[%d/%d] Descargando %s desde %s...", i, len(zip_links), filename, url)
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                with open(dest_path, "wb") as f:
                    f.write(r.content)
                log.info("  -> Guardado exitosamente: %s (%d bytes)", filename, len(r.content))
                downloaded_count += 1
            else:
                log.error("  -> Error al descargar %s. Código HTTP: %d", filename, r.status_code)
                failed_count += 1
        except Exception as e:
            log.error("  -> Excepción al descargar %s: %s", filename, e)
            failed_count += 1

    log.info("=== PROCESO DE DESCARGA FINALIZADO ===")
    log.info("Total procesados: %d", len(zip_links))
    log.info("Descargados nuevos: %d", downloaded_count)
    log.info("Omitidos (ya existentes): %d", skipped_count)
    log.info("Fallidos: %d", failed_count)
    log.info("Archivos ubicados en la carpeta: %s", RAW_DIR.absolute())

if __name__ == "__main__":
    scrape_and_download()
