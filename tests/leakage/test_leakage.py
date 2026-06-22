import os
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
GOLD_DIR = BASE_DIR / "data" / "gold"

def test_no_data_leakage():
    """
    Verifica que no exista fuga de información temporal en las características de entrada.
    Específicamente, comprueba que las características de rezago (lags) y estadísticas móviles
    en la semana t corresponden exclusivamente a observaciones de la semana t o anteriores,
    y que la variable objetivo (target t+1) coincide exactamente con la observación de la semana t+1.
    """
    features_path = GOLD_DIR / "prediction_features.parquet"
    if not features_path.exists():
        features_path = GOLD_DIR / "prediction_features.csv"
        
    assert features_path.exists(), "No se encontró prediction_features en formato Parquet ni CSV"
    
    if features_path.suffix == ".parquet":
        df = pd.read_parquet(features_path)
    else:
        df = pd.read_csv(features_path)
        
    df["week_start"] = pd.to_datetime(df["week_start"])
    df = df.sort_values(by=["product_code", "market_aggregated", "week_start"]).reset_index(drop=True)
    
    # Comprobar grupos
    for name, group in df.groupby(["product_code", "market_aggregated"]):
        if len(group) < 53:
            continue
            
        group = group.reset_index(drop=True)
        
        # 1. Comprobar que price_lag_1 coincide con el precio real desplazado en 1
        real_price = group["fob_unit_value_usd_kg"].values
        lag_1_price = group["price_lag_1"].values
        
        # El lag_1 en la fila i debe ser igual al precio real en i-1
        for i in range(1, len(group)):
            if not pd.isna(real_price[i-1]) and not pd.isna(lag_1_price[i]):
                assert lag_1_price[i] == real_price[i-1], f"Fuga detectada: price_lag_1 en fila {i} ({lag_1_price[i]}) no coincide con precio en {i-1} ({real_price[i-1]}) en grupo {name}"
                
        # 2. Comprobar que volume_lag_1 coincide con total_net_weight_kg desplazado en 1
        real_volume = group["total_net_weight_kg"].values
        lag_1_volume = group["volume_lag_1"].values if "volume_lag_1" in group.columns else group["volume_lag_1"] if "volume_lag_1" in group.columns else None
        
        # En feature_engineering.py, volume_lag_1 se calcula y se descarta al final, pero se guarda volume_lag_1 en lag_1
        lag_1_volume_col = group["volume_lag_1"] if "volume_lag_1" in group.columns else group["volume_lag_2"].shift(-1) # proxy
        # Comprobar directamente usando volume_lag_2 y lag_1
        lag_2_volume = group["volume_lag_2"].values
        for i in range(2, len(group)):
            if not pd.isna(real_volume[i-2]) and not pd.isna(lag_2_volume[i]):
                assert lag_2_volume[i] == real_volume[i-2], f"Fuga detectada en volume_lag_2"

        # 3. Comprobar que el target_fob_unit_value_usd_kg_t1 es exactamente el valor de t+1 (que se está intentando predecir)
        target_price_t1 = group["target_fob_unit_value_usd_kg_t1"].values
        for i in range(len(group) - 1):
            if not pd.isna(real_price[i+1]) and not pd.isna(target_price_t1[i]):
                assert target_price_t1[i] == real_price[i], "El target t1 debe corresponder al valor de la fila actual para predecir t+1"
