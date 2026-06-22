#!/usr/bin/env python3
"""
src/feature_engineering.py
==========================
Genera el conjunto de características (lags, estadísticas móviles, 
codificación cíclica, variaciones) para el modelamiento predictivo.
Aplica el principio estricto contra fuga de información (shift 1).

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import logging
from pathlib import Path
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Configuración de rutas
BASE_DIR = Path(".")
GOLD_DIR = BASE_DIR / "data" / "gold"

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

def calculate_mad(x):
    """Calcula la desviación absoluta de la mediana (MAD)."""
    median = np.median(x)
    return np.median(np.abs(x - median))

def build_features():
    log.info("Cargando weekly_product_market...")
    df = load_data(GOLD_DIR / "weekly_product_market.parquet")
    
    # Ordenar cronológicamente
    df["week_start"] = pd.to_datetime(df["week_start"])
    df = df.sort_values(by=["product_code", "market_aggregated", "week_start"]).reset_index(drop=True)
    
    # Extraer variables calendario de la fecha
    df["mes"] = df["week_start"].dt.month
    df["quarter"] = df["week_start"].dt.quarter
    df["year"] = df["week_start"].dt.year
    
    # -------------------------------------------------------------------------
    # 1. Variables Objetivo (t+1)
    # Cada fila representará la predicción para la semana t+1. 
    # Las características se calcularán sobre la información conocida en la semana t.
    # -------------------------------------------------------------------------
    df["target_fob_unit_value_usd_kg_t1"] = df["fob_unit_value_usd_kg"]
    df["target_export_volume_kg_t1"] = df["total_net_weight_kg"]
    
    # -------------------------------------------------------------------------
    # 2. Información base de la semana t (shifted por 1)
    # -------------------------------------------------------------------------
    grouped = df.groupby(["product_code", "market_aggregated"])
    
    # Llenado hacia adelante controlado (máximo 4 semanas) de los precios base
    price_series = df["fob_unit_value_usd_kg"]
    df["price_age_weeks"] = df["weeks_since_last_export"]
    
    # Forward fill controlado en el precio para ingeniería de características
    price_filled = df.groupby(["product_code", "market_aggregated"])["fob_unit_value_usd_kg"].ffill(limit=4)
    
    # Desplazar 1 semana para representar los datos conocidos al cierre de la semana t
    base_price = df.groupby(["product_code", "market_aggregated"])["fob_unit_value_usd_kg"].shift(1)
    base_price_filled = df.groupby(["product_code", "market_aggregated"]).apply(lambda x: x["fob_unit_value_usd_kg"].ffill(limit=4).shift(1)).reset_index(level=[0,1], drop=True)
    base_volume = df.groupby(["product_code", "market_aggregated"])["total_net_weight_kg"].shift(1)
    base_fob = df.groupby(["product_code", "market_aggregated"])["total_fob_usd"].shift(1)
    base_shipments = df.groupby(["product_code", "market_aggregated"])["shipment_count"].shift(1)
    
    # -------------------------------------------------------------------------
    # Lags (Rezagos)
    # -------------------------------------------------------------------------
    log.info("Calculando rezagos temporales...")
    for lag in [1, 2, 4, 8, 13, 26, 52]:
        df[f"price_lag_{lag}"] = df.groupby(["product_code", "market_aggregated"])["fob_unit_value_usd_kg"].shift(lag)
        df[f"volume_lag_{lag}"] = df.groupby(["product_code", "market_aggregated"])["total_net_weight_kg"].shift(lag)
        
    for lag in [1, 4, 13, 52]:
        df[f"fob_lag_{lag}"] = df.groupby(["product_code", "market_aggregated"])["total_fob_usd"].shift(lag)
        
    for lag in [1, 4, 13]:
        df[f"shipment_count_lag_{lag}"] = df.groupby(["product_code", "market_aggregated"])["shipment_count"].shift(lag)
        
    # -------------------------------------------------------------------------
    # Estadísticas Móviles (Rolling Stats)
    # -------------------------------------------------------------------------
    log.info("Calculando estadísticas móviles...")
    # Llenar nulos antes de rolling para evitar NaN en cascada en precios
    df["price_filled_lag1"] = df.groupby(["product_code", "market_aggregated"])["fob_unit_value_usd_kg"].apply(lambda x: x.ffill(limit=4).shift(1)).reset_index(level=[0,1], drop=True)
    df["volume_lag1"] = df.groupby(["product_code", "market_aggregated"])["total_net_weight_kg"].shift(1)
    
    # Agrupación para aplicar rolling sin leaks
    grp_rolling = df.groupby(["product_code", "market_aggregated"])
    
    for w in [4, 8, 13, 26, 52]:
        df[f"price_rolling_mean_{w}"] = grp_rolling["price_filled_lag1"].transform(lambda x: x.rolling(w, min_periods=1).mean())
        df[f"price_rolling_median_{w}"] = grp_rolling["price_filled_lag1"].transform(lambda x: x.rolling(w, min_periods=1).median())
        df[f"price_rolling_std_{w}"] = grp_rolling["price_filled_lag1"].transform(lambda x: x.rolling(w, min_periods=1).std())
        df[f"price_rolling_min_{w}"] = grp_rolling["price_filled_lag1"].transform(lambda x: x.rolling(w, min_periods=1).min())
        df[f"price_rolling_max_{w}"] = grp_rolling["price_filled_lag1"].transform(lambda x: x.rolling(w, min_periods=1).max())
        # MAD con rolling custom
        df[f"price_rolling_mad_{w}"] = grp_rolling["price_filled_lag1"].transform(lambda x: x.rolling(w, min_periods=1).apply(calculate_mad, raw=True))
        
        # Volumen
        df[f"volume_rolling_mean_{w}"] = grp_rolling["volume_lag1"].transform(lambda x: x.rolling(w, min_periods=1).mean())
        df[f"volume_rolling_median_{w}"] = grp_rolling["volume_lag1"].transform(lambda x: x.rolling(w, min_periods=1).median())
        df[f"volume_rolling_std_{w}"] = grp_rolling["volume_lag1"].transform(lambda x: x.rolling(w, min_periods=1).std())
        df[f"volume_rolling_min_{w}"] = grp_rolling["volume_lag1"].transform(lambda x: x.rolling(w, min_periods=1).min())
        df[f"volume_rolling_max_{w}"] = grp_rolling["volume_lag1"].transform(lambda x: x.rolling(w, min_periods=1).max())
        df[f"volume_rolling_mad_{w}"] = grp_rolling["volume_lag1"].transform(lambda x: x.rolling(w, min_periods=1).apply(calculate_mad, raw=True))

    # -------------------------------------------------------------------------
    # Variaciones y Diferencias Logarítmicas
    # -------------------------------------------------------------------------
    log.info("Calculando variaciones porcentuales...")
    eps = 1e-5
    
    # Variaciones porcentuales de precio
    df["price_pct_change_1"] = (df["price_filled_lag1"] - df["price_lag_2"]) / (df["price_lag_2"] + eps)
    df["price_pct_change_4"] = (df["price_filled_lag1"] - df["price_lag_8"]) / (df["price_lag_8"] + eps)
    df["price_pct_change_52"] = (df["price_filled_lag1"] - df["price_lag_52"]) / (df["price_lag_52"] + eps)
    
    # Variaciones porcentuales de volumen
    df["volume_pct_change_1"] = (df["volume_lag1"] - df["volume_lag_2"]) / (df["volume_lag_2"] + eps)
    df["volume_pct_change_4"] = (df["volume_lag1"] - df["volume_lag_8"]) / (df["volume_lag_8"] + eps)
    df["volume_pct_change_52"] = (df["volume_lag1"] - df["volume_lag_52"]) / (df["volume_lag_52"] + eps)
    
    # Diferencias logarítmicas robustas
    df["log_price_difference_1"] = np.log(df["price_filled_lag1"] + eps) - np.log(df["price_lag_2"] + eps)
    df["log_volume_difference_1"] = np.log(df["volume_lag1"] + eps) - np.log(df["volume_lag_2"] + eps)
    
    # -------------------------------------------------------------------------
    # Características Calendario y Cíclicas
    # -------------------------------------------------------------------------
    log.info("Calculando características calendario y cíclicas...")
    df["week_of_campaign"] = df["iso_week"]
    
    # Encodings cíclicos
    df["week_sin"] = np.sin(2 * np.pi * df["iso_week"] / 52.0)
    df["week_sin"] = df["week_sin"].fillna(0)
    df["week_cos"] = np.cos(2 * np.pi * df["iso_week"] / 52.0)
    df["week_cos"] = df["week_cos"].fillna(1)
    df["month_sin"] = np.sin(2 * np.pi * df["mes"] / 12.0)
    df["month_sin"] = df["month_sin"].fillna(0)
    df["month_cos"] = np.cos(2 * np.pi * df["mes"] / 12.0)
    df["month_cos"] = df["month_cos"].fillna(1)
    
    # -------------------------------------------------------------------------
    # Llenado de proxies y banderas
    # -------------------------------------------------------------------------
    # Desplazar variables climatológicas y macroeconómicas 1 semana
    df["tipo_cambio_pen_usd_lag1"] = df.groupby(["product_code", "market_aggregated"])["tipo_cambio_pen_usd"].shift(1)
    df["temperatura_max_c_lag1"] = df.groupby(["product_code", "market_aggregated"])["temperatura_max_c"].shift(1)
    df["temperatura_min_c_lag1"] = df.groupby(["product_code", "market_aggregated"])["temperatura_min_c"].shift(1)
    df["precipitacion_mm_lag1"] = df.groupby(["product_code", "market_aggregated"])["precipitacion_mm"].shift(1)
    df["humedad_pct_lag1"] = df.groupby(["product_code", "market_aggregated"])["humedad_pct"].shift(1)
    df["dias_logisticos_lag1"] = df.groupby(["product_code", "market_aggregated"])["dias_logisticos"].shift(1)
    df["costo_logistico_usd_kg_lag1"] = df.groupby(["product_code", "market_aggregated"])["costo_logistico_usd_kg"].shift(1)
    df["cumplimiento_fitosanitario_lag1"] = df.groupby(["product_code", "market_aggregated"])["cumplimiento_fitosanitario"].shift(1)
    df["merma_pct_lag1"] = df.groupby(["product_code", "market_aggregated"])["merma_pct"].shift(1)
    df["destination_volume_share_lag1"] = df.groupby(["product_code", "market_aggregated"])["destination_volume_share"].shift(1)
    df["destination_fob_share_lag1"] = df.groupby(["product_code", "market_aggregated"])["destination_fob_share"].shift(1)
    
    df["is_imputed"] = 0 # Dummy de control de imputaciones
    
    # Limpiar columnas auxiliares temporales
    df = df.drop(columns=["price_filled_lag1", "volume_lag1"])
    
    # Guardar features listos para modelamiento
    save_data(df, GOLD_DIR / "prediction_features.parquet")
    log.info("prediction_features construida con %d filas y %d columnas.", len(df), len(df.columns))

if __name__ == "__main__":
    build_features()
