#!/usr/bin/env python3
"""
src/prepare_weekly_dataset.py
=============================
Implementa la arquitectura de datos por capas (Raw, Bronze, Silver, Gold) y 
la agregación semanal a nivel de producto x mercado x semana.
Aplica las reglas metodológicas de selección de mercados e ingeniería de grid.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import os
import shutil
import logging
import hashlib
import json
from pathlib import Path
import yaml
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Configuración de rutas
BASE_DIR = Path(".")
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
CONFIG_DIR = BASE_DIR / "config"

# Crear directorios
for d in [RAW_DIR, BRONZE_DIR, SILVER_DIR, GOLD_DIR, CONFIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Salt para anonimización
SALT = os.getenv("AGRO_SALT", "agro_salt_2026")

# Mapeo de códigos de país ISO alfa-2 a alfa-3
COUNTRY_MAP = {
    'US': 'USA', 'NL': 'NLD', 'ES': 'ESP', 'CL': 'CHL', 'HK': 'HKG',
    'RU': 'RUS', 'PT': 'PRT', 'MX': 'MEX', 'CN': 'CHN', 'TW': 'TWN',
    'GB': 'GBR', 'CA': 'CAN', 'DO': 'DOM', 'VE': 'VEN', 'DE': 'DEU',
    'JP': 'JPN', 'KR': 'KOR', 'HN': 'HND', 'IT': 'ITA', 'FR': 'FRA',
    'BE': 'BEL', 'PL': 'POL', 'BR': 'BRA', 'CO': 'COL', 'AR': 'ARG',
    'EC': 'ECU', 'PE': 'PER', 'PA': 'PAN', 'UY': 'URY', 'CRI': 'CRI',
    'GT': 'GTM', 'SV': 'SLV', 'NI': 'NIC', 'BO': 'BOL', 'PY': 'PRY',
    'IN': 'IND', 'ZA': 'ZAF', 'AU': 'AUS', 'NZ': 'NZL', 'SG': 'SGP',
    'MY': 'MYS', 'TH': 'THA', 'ID': 'IDN', 'PH': 'PHL', 'AE': 'ARE',
    'SA': 'SAU', 'IL': 'ISR', 'TR': 'TUR', 'EG': 'EGY', 'MA': 'MAR',
    'DK': 'DNK', 'SE': 'SWE', 'NO': 'NOR', 'FI': 'FIN', 'CH': 'CHE',
    'AT': 'AUT', 'IE': 'IRL', 'UA': 'UKR', 'GR': 'GRC', 'RO': 'ROU',
    'BG': 'BGR', 'HU': 'HUN', 'CZ': 'CZE', 'SK': 'SVK', 'HR': 'HRV',
    'SI': 'SVN', 'LT': 'LTU', 'LV': 'LVA', 'EE': 'EST'
}

def save_data(df: pd.DataFrame, filepath: Path):
    """Guarda un DataFrame en formato Parquet con fallback a CSV."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_parquet(filepath, index=False)
        log.info("Guardado Parquet en: %s", filepath)
    except ImportError:
        csv_path = filepath.with_suffix(".csv")
        df.to_csv(csv_path, index=False)
        log.info("Guardado CSV (fallback) en: %s", csv_path)

def load_data(filepath: Path) -> pd.DataFrame:
    """Carga un archivo en formato Parquet con fallback a CSV."""
    if filepath.exists():
        try:
            return pd.read_parquet(filepath)
        except Exception:
            pass
    csv_path = filepath.with_suffix(".csv")
    if csv_path.exists():
        return pd.read_csv(csv_path)
    raise FileNotFoundError(f"No se encontró {filepath} ni {csv_path}")

def anonymize_exporter(name):
    """Anonimiza el nombre de la empresa mediante SHA-256."""
    if not name or pd.isna(name):
        return "UNK"
    name_str = str(name).strip()
    if "No Disponible" in name_str or "Ley" in name_str or name_str == "":
        return "ANONYMOUS_EXPORT"
    return hashlib.sha256((SALT + name_str).encode('utf-8')).hexdigest()[:16]

def clean_country_code(code):
    """Normaliza y mapea el código de país de destino a ISO alfa-3."""
    if not code or pd.isna(code):
        return "UNK"
    code_str = str(code).strip().upper()
    if len(code_str) == 3:
        return code_str
    return COUNTRY_MAP.get(code_str, "UNK")

def ingest_raw_data():
    """Ingeesta el archivo original y crea las capas Raw y Bronze."""
    src_file = DATA_DIR / "dataset_real_v1.csv"
    if not src_file.exists():
        src_file = DATA_DIR / "dataset_agro_sintetico_v1.csv"
        
    if not src_file.exists():
        raise FileNotFoundError("No se encontró dataset_real_v1.csv ni dataset_agro_sintetico_v1.csv en data/")

    log.info("--- 1. CAPA RAW ---")
    dest_raw = RAW_DIR / "exports_raw.csv"
    shutil.copy(src_file, dest_raw)
    log.info("Copiado archivo original a: %s", dest_raw)

    log.info("--- 2. CAPA BRONZE ---")
    df_raw = pd.read_csv(dest_raw)
    dest_bronze = BRONZE_DIR / "exports_raw.parquet"
    save_data(df_raw, dest_bronze)

def build_silver_layer():
    """Limpia, normaliza y anonimiza los datos (Capa Silver)."""
    log.info("--- 3. CAPA SILVER ---")
    
    # Cargar Bronze
    df = load_data(BRONZE_DIR / "exports_raw.parquet")
    
    # Cargar configuración de productos
    with open(CONFIG_DIR / "products.yml", "r", encoding="utf-8") as f:
        config_prod = yaml.safe_load(f)["products"]
        
    # Crear mapeo inverso de subpartidas arancelarias a códigos internos
    tariff_to_code = {}
    for code, info in config_prod.items():
        for tariff in info["tariff_codes"]:
            # Normalizar a 10 dígitos
            tariff_to_code[tariff.zfill(10)] = code
            tariff_to_code[tariff.zfill(10)[:6]] = code

    # Normalizar partida arancelaria
    df["tariff_code"] = df["partida_arancelaria"].astype(str).str.replace(".", "").str.strip().str.zfill(10)
    
    # Mapear product_code
    df["product_code"] = df["tariff_code"].map(tariff_to_code)
    # Si no mapea, mapear por los primeros 6 dígitos
    mask_null = df["product_code"].isna()
    df.loc[mask_null, "product_code"] = df.loc[mask_null, "tariff_code"].str[:6].map(tariff_to_code)
    
    # Exclusión de cacao y nulos
    df = df[df["product_code"].notna()]
    df = df[df["product_code"] != "cacao"]
    
    # Validar rangos físicos lógicos
    df = df[(df["volumen_kg"] > 0) & (df["precio_kg_usd"] > 0)]
    df["fob_usd"] = df["precio_kg_usd"] * df["volumen_kg"]
    
    # Fechas
    df["declaration_date"] = pd.to_datetime(df["fecha"])
    
    # Homologar países a ISO alfa-3
    df["destination_country_code"] = df["destino_mercado"].apply(clean_country_code)
    
    # Anonimizar exportador
    df["exporter_id_hash"] = df["empresa_exportadora"].apply(anonymize_exporter)
    
    # Agregar metadatos de auditoría
    df["record_id"] = df["id"].astype(str)
    df["source_file"] = "dataset_real_v1.csv"
    df["source_row_number"] = df.index + 1
    df["ingestion_timestamp"] = pd.Timestamp.now()
    
    # Renombrar campos menores
    df["customs_code"] = df["zona"].fillna("Lima")
    df["transport_mode"] = "MARÍTIMO"
    df["net_weight_kg"] = df["volumen_kg"]
    df["gross_weight_kg"] = df["net_weight_kg"] * 1.10
    df["declaration_id_hash"] = df["record_id"].apply(lambda x: hashlib.sha256((SALT + x).encode()).hexdigest()[:16])
    
    # Limpieza final de columnas Silver
    silver_cols = [
        "record_id", "source_file", "source_row_number", "declaration_date",
        "tariff_code", "product_code", "destination_country_code", "customs_code",
        "transport_mode", "exporter_id_hash", "declaration_id_hash", "fob_usd",
        "net_weight_kg", "gross_weight_kg", "ingestion_timestamp", "tipo_cambio_pen_usd",
        "temperatura_max_c", "temperatura_min_c", "precipitacion_mm", "humedad_pct",
        "dias_logisticos", "costo_logistico_usd_kg", "cumplimiento_fitosanitario", "merma_pct"
    ]
    df_silver = df[silver_cols]
    
    save_data(df_silver, SILVER_DIR / "exports_clean.parquet")
    log.info("Silver Layer construida con %d registros.", len(df_silver))

def build_gold_layer():
    """Realiza la agregación semanal, selección de mercados y completa la cuadrícula (Capa Gold)."""
    log.info("--- 4. CAPA GOLD ---")
    
    df = load_data(SILVER_DIR / "exports_clean.parquet")
    
    # Calcular semana ISO, lunes de inicio
    df["week_start"] = df["declaration_date"].dt.to_period("W").dt.start_time
    df["week_end"] = df["week_start"] + pd.Timedelta(days=6)
    df["iso_year"] = df["declaration_date"].dt.isocalendar().year
    df["iso_week"] = df["declaration_date"].dt.isocalendar().week
    
    # -------------------------------------------------------------------------
    # Selección de Mercados de Destino (Solo con periodo de desarrollo)
    # -------------------------------------------------------------------------
    dev_split_date = pd.to_datetime("2025-06-02")
    df_dev = df[df["declaration_date"] < dev_split_date].copy()
    
    # 1. Agregado semanal para desarrollo a nivel de producto-país-semana
    weekly_dev = df_dev.groupby(["product_code", "destination_country_code", "week_start"]).agg(
        weekly_volume=("net_weight_kg", "sum"),
        weekly_fob=("fob_usd", "sum")
    ).reset_index()
    
    # 2. Contar estadísticas de mercado
    market_stats = weekly_dev.groupby(["product_code", "destination_country_code"]).agg(
        total_fob=("weekly_fob", "sum"),
        obs_weeks=("week_start", "count"),
        pos_vol_weeks=("weekly_volume", lambda x: (x > 0).sum())
    ).reset_index()
    
    selected_markets = {}
    products = df["product_code"].unique()
    
    for prod in products:
        prod_stats = market_stats[market_stats["product_code"] == prod]
        
        # Filtro: >= 52 semanas observadas y >= 30 semanas con volumen positivo
        eligible = prod_stats[(prod_stats["obs_weeks"] >= 52) & (prod_stats["pos_vol_weeks"] >= 30)]
        
        # Seleccionar top 10 países por FOB acumulado
        top_10 = eligible.sort_values(by="total_fob", ascending=False).head(10)["destination_country_code"].tolist()
        
        # Si top_10 está vacío, tomar el top-3 histórico de países elegibles o no elegibles para evitar que todo sea OTHER
        if not top_10:
            log.warning("No hay países elegibles con el filtro duro para '%s'. Usando fallback de volumen.", prod)
            top_10 = prod_stats.sort_values(by="total_fob", ascending=False).head(5)["destination_country_code"].tolist()
            
        # Añadir OTHER si no está
        if "OTHER" not in top_10:
            top_10.append("OTHER")
        selected_markets[prod] = top_10
        
    log.info("Mercados seleccionados por producto (top-10 + OTHER):")
    log.info(json.dumps(selected_markets, indent=2))
    
    # Guardar configuración de mercados
    with open(CONFIG_DIR / "selected_markets.json", "w", encoding="utf-8") as f:
        json.dump(selected_markets, f, indent=2)
        
    # Aplicar mapeo de mercados a Silver
    def map_market(row):
        prod = row["product_code"]
        mkt = row["destination_country_code"]
        if mkt in selected_markets.get(prod, []):
            return mkt
        return "OTHER"
        
    df["market_aggregated"] = df.apply(map_market, axis=1)
    
    # -------------------------------------------------------------------------
    # Agregación semanal por producto, mercado agregado y semana
    # -------------------------------------------------------------------------
    weekly_agg = df.groupby(["product_code", "market_aggregated", "week_start", "week_end", "iso_year", "iso_week"]).agg(
        total_fob_usd=("fob_usd", "sum"),
        total_net_weight_kg=("net_weight_kg", "sum"),
        total_gross_weight_kg=("gross_weight_kg", "sum"),
        shipment_count=("record_id", "count"),
        exporter_count=("exporter_id_hash", "nunique"),
        avg_shipment_weight_kg=("net_weight_kg", "mean"),
        median_shipment_weight_kg=("net_weight_kg", "median"),
        tipo_cambio_pen_usd=("tipo_cambio_pen_usd", "mean"),
        temperatura_max_c=("temperatura_max_c", "mean"),
        temperatura_min_c=("temperatura_min_c", "mean"),
        precipitacion_mm=("precipitacion_mm", "mean"),
        humedad_pct=("humedad_pct", "mean"),
        dias_logisticos=("dias_logisticos", "mean"),
        costo_logistico_usd_kg=("costo_logistico_usd_kg", "mean"),
        cumplimiento_fitosanitario=("cumplimiento_fitosanitario", "mean"),
        merma_pct=("merma_pct", "mean")
    ).reset_index()
    
    # Calcular valor unitario FOB
    weekly_agg["fob_unit_value_usd_kg"] = weekly_agg["total_fob_usd"] / weekly_agg["total_net_weight_kg"]
    
    # -------------------------------------------------------------------------
    # Creación del Grid Temporal Completo (2018-06-04 a 2026-05-31)
    # -------------------------------------------------------------------------
    start_grid = pd.to_datetime("2018-06-04")
    end_grid = pd.to_datetime("2026-05-31")
    mondays = pd.date_range(start=start_grid, end=end_grid, freq="W-MON")
    
    grid_rows = []
    for prod in products:
        mkts = selected_markets[prod]
        for mkt in mkts:
            for mon in mondays:
                grid_rows.append({
                    "product_code": prod,
                    "market_aggregated": mkt,
                    "week_start": mon,
                    "week_end": mon + pd.Timedelta(days=6),
                    "iso_year": mon.isocalendar().year,
                    "iso_week": mon.isocalendar().week
                })
                
    df_grid = pd.DataFrame(grid_rows)
    
    # Unir grid con agregados semanales
    df_gold = df_grid.merge(weekly_agg, on=["product_code", "market_aggregated", "week_start", "week_end", "iso_year", "iso_week"], how="left")
    
    # Rellenar valores para semanas sin exportación
    df_gold["has_exports"] = df_gold["total_net_weight_kg"].notna().astype(int)
    
    fill_zeros = ["total_fob_usd", "total_net_weight_kg", "total_gross_weight_kg", "shipment_count", "exporter_count"]
    for col in fill_zeros:
        df_gold[col] = df_gold[col].fillna(0)
        
    # fob_unit_value_usd_kg queda nulo si no hay exportaciones
    df_gold["fob_unit_value_usd_kg"] = df_gold["fob_unit_value_usd_kg"].where(df_gold["has_exports"] == 1, np.nan)
    
    # -------------------------------------------------------------------------
    # Imputación de variables contextuales y proxies para semanas sin exportación
    # -------------------------------------------------------------------------
    # 1. Tipo de cambio mensual
    # Obtener el promedio mensual real observado para rellenar vacíos
    tc_mensual = df.groupby(df["declaration_date"].dt.to_period("M"))["tipo_cambio_pen_usd"].mean().to_dict()
    def get_tc(row):
        if pd.notna(row["tipo_cambio_pen_usd"]):
            return row["tipo_cambio_pen_usd"]
        period = row["week_start"].to_period("M")
        return tc_mensual.get(period, 3.765)
    df_gold["tipo_cambio_pen_usd"] = df_gold.apply(get_tc, axis=1)
    
    # 2. Clima regional por producto-semana
    # Promediar clima por producto y semana para tener un proxy regional libre de nulos
    clima_prod_week = df_gold[df_gold["has_exports"] == 1].groupby(["product_code", "week_start"]).agg(
        temp_max=("temperatura_max_c", "mean"),
        temp_min=("temperatura_min_c", "mean"),
        precip=("precipitacion_mm", "mean"),
        hum_pct=("humedad_pct", "mean")
    ).reset_index()
    
    # Ordenar
    clima_prod_week = clima_prod_week.sort_values(by=["product_code", "week_start"]).reset_index(drop=True)
    
    # Forward/Backward fill a nivel de producto usando transform para evitar KeyError
    clima_prod_week["temp_max"] = clima_prod_week.groupby("product_code")["temp_max"].transform(lambda x: x.ffill().bfill())
    clima_prod_week["temp_min"] = clima_prod_week.groupby("product_code")["temp_min"].transform(lambda x: x.ffill().bfill())
    clima_prod_week["precip"] = clima_prod_week.groupby("product_code")["precip"].transform(lambda x: x.ffill().bfill())
    clima_prod_week["hum_pct"] = clima_prod_week.groupby("product_code")["hum_pct"].transform(lambda x: x.ffill().bfill())
    
    # Mezclar con Gold
    df_gold = df_gold.merge(clima_prod_week, on=["product_code", "week_start"], how="left")
    df_gold["temperatura_max_c"] = df_gold["temperatura_max_c"].fillna(df_gold["temp_max"])
    df_gold["temperatura_min_c"] = df_gold["temperatura_min_c"].fillna(df_gold["temp_min"])
    df_gold["precipitacion_mm"] = df_gold["precipitacion_mm"].fillna(df_gold["precip"])
    df_gold["humedad_pct"] = df_gold["humedad_pct"].fillna(df_gold["hum_pct"])
    df_gold = df_gold.drop(columns=["temp_max", "temp_min", "precip", "hum_pct"])
    
    # Si aún quedan nulos marginales en clima (e.g. al inicio del dataset), usar valores típicos históricos
    df_gold["temperatura_max_c"] = df_gold["temperatura_max_c"].fillna(25.0)
    df_gold["temperatura_min_c"] = df_gold["temperatura_min_c"].fillna(15.0)
    df_gold["precipitacion_mm"] = df_gold["precipitacion_mm"].fillna(0.0)
    df_gold["humedad_pct"] = df_gold["humedad_pct"].fillna(70.0)
    
    # 3. Llenar logística e de mermas
    log_mkt = df_gold[df_gold["has_exports"] == 1].groupby(["product_code", "market_aggregated"]).agg(
        dias=("dias_logisticos", "mean"),
        costo=("costo_logistico_usd_kg", "mean"),
        merma=("merma_pct", "mean")
    ).reset_index()
    
    df_gold = df_gold.merge(log_mkt, on=["product_code", "market_aggregated"], how="left")
    df_gold["dias_logisticos"] = df_gold["dias_logisticos"].fillna(df_gold["dias"]).fillna(12).astype(int)
    df_gold["costo_logistico_usd_kg"] = df_gold["costo_logistico_usd_kg"].fillna(df_gold["costo"]).fillna(0.35)
    df_gold["merma_pct"] = df_gold["merma_pct"].fillna(df_gold["merma"]).fillna(5.0)
    df_gold["cumplimiento_fitosanitario"] = df_gold["cumplimiento_fitosanitario"].fillna(1.0) # default compliance
    
    df_gold = df_gold.drop(columns=["dias", "costo", "merma"])
    
    # Calcular semanas desde la última exportación
    df_gold = df_gold.sort_values(by=["product_code", "market_aggregated", "week_start"]).reset_index(drop=True)
    
    weeks_counter = []
    for name, group in df_gold.groupby(["product_code", "market_aggregated"]):
        counter = 0
        for has_exp in group["has_exports"]:
            if has_exp == 1:
                counter = 0
            else:
                counter += 1
            weeks_counter.append(counter)
    df_gold["weeks_since_last_export"] = weeks_counter
    
    # Calcular participaciones de mercado semanales
    prod_weekly_tot = df_gold.groupby(["product_code", "week_start"]).agg(
        weekly_tot_vol=("total_net_weight_kg", "sum"),
        weekly_tot_fob=("total_fob_usd", "sum")
    ).reset_index()
    
    df_gold = df_gold.merge(prod_weekly_tot, on=["product_code", "week_start"], how="left")
    df_gold["destination_volume_share"] = df_gold["total_net_weight_kg"] / df_gold["weekly_tot_vol"]
    df_gold["destination_fob_share"] = df_gold["total_fob_usd"] / df_gold["weekly_tot_fob"]
    df_gold["destination_volume_share"] = df_gold["destination_volume_share"].fillna(0)
    df_gold["destination_fob_share"] = df_gold["destination_fob_share"].fillna(0)
    
    df_gold = df_gold.drop(columns=["weekly_tot_vol", "weekly_tot_fob"])
    
    # Convertir fechas a string para serialización
    df_gold["week_start_str"] = df_gold["week_start"].dt.strftime("%Y-%m-%d")
    df_gold = df_gold.drop(columns=["week_start"])
    df_gold = df_gold.rename(columns={"week_start_str": "week_start"})
    df_gold["week_end"] = df_gold["week_end"].dt.strftime("%Y-%m-%d")
    
    save_data(df_gold, GOLD_DIR / "weekly_product_market.parquet")
    log.info("Gold Layer (weekly aggregated) construida con %d registros.", len(df_gold))

def main():
    log.info("Iniciando preparación del dataset semanal por capas...")
    ingest_raw_data()
    build_silver_layer()
    build_gold_layer()
    log.info("Procesamiento de datos por capas finalizado con éxito.")

if __name__ == "__main__":
    main()
