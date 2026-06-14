#!/usr/bin/env python3
"""
test_extractors.py
==================
Prueba de conexión, scraping y descarga automatizada de datos oficiales
para la Tesis de Agroexportaciones.

Valida:
1. BCRP (REST API - Descarga de Tipo de Cambio en tiempo real).
2. PROMPERÚ / Exportemos (Scraping de fichas arancelarias por HS Code).
3. SENASA Requisitos (Validación de endpoint fitosanitario).
4. SENAMHI Clima (Verificación de disponibilidad de estación climática).
5. SUNAT Aduanet (Test de conexión).

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

from __future__ import annotations

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Configuración de salida
OUT_DIR = Path("data/downloads")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Parámetros del usuario
PARTIDAS = {
    "ARANDANO": "0810400000",
    "UVA": "0806100000",
    "PALTA": "0804400000",
    "ESPARRAGO": "0709200000",
    "CACAO": "1801001900"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def test_bcrp() -> dict:
    """Descarga el tipo de cambio mensual PN01207PM de BCRP (PEN/USD)."""
    log.info("Iniciando prueba de API BCRP (Tipo de Cambio)...")
    # Código de serie para tipo de cambio interbancario mensual (promedio periodo)
    serie = "PN01207PM"
    # Rango de fechas: últimos 12 meses
    year = datetime.now().year
    url = f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{serie}/json/{year - 1}-01/{year}-12"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            data = res.json()
            periods = data.get("periods", [])
            log.info("BCRP API disponible. Se descargaron %d periodos históricos.", len(periods))
            
            # Guardar datos en CSV
            csv_path = OUT_DIR / "bcrp_tipo_cambio.csv"
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["fecha_periodo", "tipo_cambio_pen_usd"])
                for p in periods:
                    val = p.get("values", [""])[0]
                    writer.writerow([p.get("name"), val])
                    
            log.info("Datos del BCRP guardados exitosamente en %s", csv_path)
            return {
                "status": "SUCCESS",
                "message": f"Descargados {len(periods)} periodos históricos.",
                "data_preview": periods[-3:] if len(periods) >= 3 else periods
            }
        else:
            return {"status": "FAILED", "message": f"Código de estado HTTP {res.status_code}"}
    except Exception as e:
        log.error("Fallo al conectar con BCRP: %s", e)
        return {"status": "FAILED", "message": str(e)}


def test_exportemos() -> dict:
    """Prueba conexión a la ficha de Producto de exportemos.pe (PromPerú)."""
    log.info("Iniciando prueba de conexión con Exportemos.pe...")
    # Usar partida de Arándano por defecto para test
    partida = PARTIDAS["ARANDANO"]
    url = f"https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/{partida}"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            # Buscar indicadores en el HTML para ver si cargó bien la ficha
            is_valid = "partida" in res.text.lower() or partida in res.text
            log.info("Exportemos.pe responde (HTTP 200). Contenido verificado: %s", is_valid)
            return {
                "status": "SUCCESS" if is_valid else "WARNING",
                "message": "Página responde. Contiene datos de partida: " + str(is_valid),
                "url_consultada": url
            }
        else:
            return {"status": "FAILED", "message": f"Código de estado HTTP {res.status_code}"}
    except Exception as e:
        log.error("Fallo al conectar con Exportemos.pe: %s", e)
        return {"status": "FAILED", "message": str(e)}


def test_senasa() -> dict:
    """Valida conexión al servicio de consulta fitosanitaria de SENASA."""
    log.info("Iniciando prueba de conexión con SENASA...")
    url = "https://servicios.senasa.gob.pe/consultaRequisitos/consultarRequisitos.action"
    
    try:
        # Petición GET simple para ver si el servidor responde
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            log.info("SENASA responde correctamente (HTTP 200).")
            return {
                "status": "SUCCESS",
                "message": "Formulario de consulta de requisitos fitosanitarios activo.",
                "url": url
            }
        else:
            return {"status": "FAILED", "message": f"Código de estado HTTP {res.status_code}"}
    except Exception as e:
        log.error("Fallo al conectar con SENASA: %s", e)
        return {"status": "FAILED", "message": str(e)}


def test_senamhi() -> dict:
    """Valida la disponibilidad de la plataforma de descarga climática de SENAMHI."""
    log.info("Iniciando prueba de conexión con SENAMHI...")
    url = "https://www.senamhi.gob.pe/site/descarga-datos/"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            log.info("SENAMHI responde correctamente (HTTP 200).")
            return {
                "status": "SUCCESS",
                "message": "Portal de descarga de datos climáticos disponible.",
                "url": url
            }
        else:
            return {"status": "FAILED", "message": f"Código de estado HTTP {res.status_code}"}
    except Exception as e:
        log.error("Fallo al conectar con SENAMHI: %s", e)
        return {"status": "FAILED", "message": str(e)}


def test_sunat() -> dict:
    """Valida el portal aduanero Aduanet de SUNAT."""
    log.info("Iniciando prueba de conexión con SUNAT Aduanet...")
    url = "https://www.aduanet.gob.pe/cl-ad-itconsultadwh/ieITS01Alias?CG_consulta=2&accion=consultar"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            log.info("SUNAT Aduanet responde correctamente (HTTP 200).")
            return {
                "status": "SUCCESS",
                "message": "Módulo de Consulta General de Exportaciones (DWH) disponible.",
                "url": url
            }
        else:
            return {"status": "FAILED", "message": f"Código de estado HTTP {res.status_code}"}
    except Exception as e:
        log.error("Fallo al conectar con SUNAT Aduanet: %s", e)
        return {"status": "FAILED", "message": str(e)}


def run_diagnostics():
    report = {
        "timestamp": datetime.now().isoformat(),
        "bcrp": test_bcrp(),
        "exportemos_promperu": test_exportemos(),
        "senasa": test_senasa(),
        "senamhi": test_senamhi(),
        "sunat_aduanet": test_sunat()
    }
    
    # Escribir reporte de diagnóstico a JSON
    json_path = OUT_DIR / "diagnostico_extractores.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
        
    print("\n=======================================================")
    print("REPORTE DE DIAGNÓSTICO DE EXTRACTORES DE DATOS OFICIALES")
    print("=======================================================")
    print(f"Archivo generado: {json_path}")
    print(f"Tipo Cambio BCRP: {report['bcrp']['status']} - {report['bcrp']['message']}")
    print(f"Exportemos (Arándano): {report['exportemos_promperu']['status']} - {report['exportemos_promperu']['message']}")
    print(f"SENASA Requisitos: {report['senasa']['status']} - {report['senasa']['message']}")
    print(f"SENAMHI Clima: {report['senamhi']['status']} - {report['senamhi']['message']}")
    print(f"SUNAT Aduanet: {report['sunat_aduanet']['status']} - {report['sunat_aduanet']['message']}")
    print("=======================================================\n")

if __name__ == "__main__":
    run_diagnostics()
