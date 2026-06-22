import os
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
GOLD_DIR = BASE_DIR / "data" / "gold"

def test_data_quality():
    """
    Realiza pruebas críticas de calidad de datos en el dataset final semanal:
    1. Códigos de producto válidos y exclusión completa de cacao.
    2. Ausencia de duplicados temporales por producto-mercado.
    3. Cero división: validación de que fob_unit_value_usd_kg es consistente.
    4. Alineación de semanas ISO (inician en lunes).
    """
    weekly_path = GOLD_DIR / "weekly_product_market.parquet"
    if not weekly_path.exists():
        weekly_path = GOLD_DIR / "weekly_product_market.csv"
        
    assert weekly_path.exists(), "No se encontró weekly_product_market"
    
    if weekly_path.suffix == ".parquet":
        df = pd.read_parquet(weekly_path)
    else:
        df = pd.read_csv(weekly_path)
        
    # 1. Códigos válidos (Palta, Uva, Arándano, Espárrago opcional, NO cacao)
    allowed_codes = {"avocado", "grape", "blueberry", "esparrago", "0804400000", "0806100000", "0810400000", "0709200000"}
    cacao_code = "1801001900" # subpartida cacao
    
    products = df["product_code"].astype(str).unique()
    for prod in products:
        assert prod in allowed_codes, f"Código de producto no permitido encontrado: {prod}"
        assert prod != cacao_code, "El cultivo de cacao no debe estar presente en el dataset analítico"
        
    # 2. Ausencia de duplicados
    df["week_start"] = pd.to_datetime(df["week_start"])
    duplicates = df.duplicated(subset=["product_code", "market_aggregated", "week_start"])
    assert not duplicates.any(), "Existen combinaciones duplicadas de producto-mercado-semana"
    
    # 3. Cero división en valor unitario
    # Comprobar que si total_net_weight_kg es 0 o nulo, fob_unit_value_usd_kg es nulo o 0, y no causó división por cero
    zero_weight_mask = df["total_net_weight_kg"] <= 0
    if zero_weight_mask.any():
        zero_weight_prices = df.loc[zero_weight_mask, "fob_unit_value_usd_kg"]
        for price in zero_weight_prices:
            assert pd.isna(price) or price == 0 or np.isinf(price) == False, "División por cero detectada: precio infinito o inválido con peso cero"
            
    # 4. Alineación a lunes (semanas ISO)
    for date in df["week_start"].unique():
        ts = pd.Timestamp(date)
        assert ts.dayofweek == 0, f"La fecha {ts} no corresponde a un lunes (inicio de semana ISO)"
