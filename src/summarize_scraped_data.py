#!/usr/bin/env python3
"""
src/summarize_scraped_data.py
=============================
Genera un análisis y resumen de los datos obtenidos de las 3 fuentes web raspadas:
1. SUNAT (45,639 transacciones de exportación de la base de aduanas).
2. BCRP (Tipo de cambio interbancario oficial PEN/USD).
3. PROMPERÚ (Fichas de exportación de arándano, uva, palta, espárrago y cacao).

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import pandas as pd
import json
import requests
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# Configuración
CULTIVOS = {
    "arandano": "0810400000",
    "uva": "0806100000",
    "palta": "0804400000",
    "esparrago": "0709200000",
    "cacao": "1801001900"
}

def analyze_promperu():
    print("=== ANALIZANDO DATOS DE PROMPERÚ (SCRAPING DE FICHAS) ===")
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for crop, code in CULTIVOS.items():
        url = f"https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/{code}"
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', r.text, re.DOTALL)
                if match:
                    data = json.loads(match.group(1))
                    crop_data = data.get("props", {}).get("pageProps", {}).get("data", {})
                    
                    # Mercados
                    markets = crop_data.get("principalesMercados", {}).get("anioCerrado", [])
                    top_markets = [f"{m.get('pais_Descripcion')} ({m.get('participacion')}%)" for m in markets[:3]]
                    
                    # Empresas
                    companies = crop_data.get("empresasExportadoras", {}).get("anioCerrado", [])
                    top_cos = [c.get("edco_NombreEmpresa") for c in companies[:3]]
                    
                    # Evolución FOB
                    fob_evolution = crop_data.get("evolucionExportacion", {}).get("lista", [])
                    last_fob = fob_evolution[-1] if fob_evolution else {}
                    
                    print(f"\n🌾 Cultivo: {crop.upper()} (Partida: {code})")
                    print(f"  - Top 3 Destinos: {', '.join(top_markets)}")
                    print(f"  - Top 3 Exportadoras: {', '.join(top_cos)}")
                    if last_fob:
                        print(f"  - Exportación Total ({last_fob.get('anio')}): {float(last_fob.get('valor', 0)):,.2f} USD FOB | Peso: {float(last_fob.get('peso', 0)):,.2f} kg")
                else:
                    print(f"  - No se encontró script __NEXT_DATA__ para {crop}")
            else:
                print(f"  - Error HTTP {r.status_code} al descargar {crop}")
        except Exception as e:
            print(f"  - Error al procesar {crop}: {e}")

def analyze_bcrp():
    print("\n=== ANALIZANDO DATOS DE BCRP (TIPO DE CAMBIO API) ===")
    url = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json/2026-01/2026-06"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            periods = r.json().get("periods", [])
            print("Historial de Tipo de Cambio PEN/USD en 2026:")
            for p in periods:
                print(f"  - {p.get('name')}: {p.get('values')[0]} PEN/USD")
        else:
            print(f"  - Error HTTP {r.status_code} al conectar con BCRP")
    except Exception as e:
        print(f"  - Error al conectar con BCRP: {e}")

def analyze_sunat():
    print("\n=== ANALIZANDO DATOS DE SUNAT (EXPORTACIONES REALES) ===")
    path = Path("data/dataset_real_v1.csv")
    if not path.exists():
        print("  - Archivo de dataset real no existe.")
        return
        
    df = pd.read_csv(path)
    print(f"Total de registros de transacciones reales importadas: {len(df)}")
    print(f"Rango de Fechas: {df['fecha'].min()} hasta {df['fecha'].max()}")
    
    print("\nDistribución por Cultivo:")
    counts = df['producto'].value_counts()
    fob_sum = df.groupby('producto')['precio_kg_usd'].mean()
    vol_sum = df.groupby('producto')['volumen_kg'].sum()
    
    for crop in counts.index:
        print(f"  - {crop.upper()}: {counts[crop]} transacciones | Volumen Total: {vol_sum[crop]:,.2f} kg | Precio Promedio FOB/kg: {fob_sum[crop]:.4f} USD")
        
    print("\nDistribución por Zonas Aduaneras de Origen:")
    zonas = df['zona'].value_counts()
    for z in zonas.index:
        print(f"  - {z}: {zonas[z]} transacciones")
        
    print("\nTop 5 Destinos de Exportación:")
    destinos = df['destino_mercado'].value_counts().head(5)
    for dest in destinos.index:
        print(f"  - {dest}: {destinos[dest]} transacciones")

if __name__ == "__main__":
    analyze_promperu()
    analyze_bcrp()
    analyze_sunat()
