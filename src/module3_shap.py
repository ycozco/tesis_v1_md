#!/usr/bin/env python3
"""
src/module3_shap.py
===================
Implementa la Capa 3 (Explicabilidad Local y Global mediante TreeSHAP):
1. Carga los modelos regresores globales entrenados (XGBoost y LightGBM).
2. Genera explicaciones locales (top-5 factores positivos y top-5 negativos)
   de los desvíos para precio y volumen.
3. Genera gráficos globales (summary bar y beeswarm) a 300 DPI en formato PNG y SVG.
4. Guarda las explicaciones locales estructuradas en data/gold/local_explanations.json.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import sys
import logging
import pickle
import json
from pathlib import Path
import numpy as np
import pandas as pd
import shap
import matplotlib
matplotlib.use('Agg')  # Configuración para ejecución en segundo plano sin GUI
import matplotlib.pyplot as plt

# Configuración de codificación de salida para Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Configuración de rutas
BASE_DIR = Path(".")
GOLD_DIR = BASE_DIR / "data" / "gold"
MODELS_DIR = BASE_DIR / "models"
STATIC_IMG_DIR = BASE_DIR / "src" / "static" / "images"
STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)

def load_data(filepath: Path) -> pd.DataFrame:
    if filepath.exists():
        try:
            return pd.read_parquet(filepath)
        except Exception:
            pass
    csv_path = filepath.with_suffix(".csv")
    if csv_path.exists():
        return pd.read_csv(csv_path)
    raise FileNotFoundError(f"No se encontró {filepath} ni {csv_path}")

class IntegratedSHAPExplainer:
    def __init__(self):
        log.info("Cargando modelos regresores para SHAP...")
        # Cargar modelos de precio
        with open(MODELS_DIR / "xgb_price_model.pkl", "rb") as f:
            self.m_xgb_price = pickle.load(f)
        with open(MODELS_DIR / "lgb_price_model.pkl", "rb") as f:
            self.m_lgb_price = pickle.load(f)
            
        # Cargar modelos de volumen
        with open(MODELS_DIR / "xgb_vol_model.pkl", "rb") as f:
            self.m_xgb_vol = pickle.load(f)
        with open(MODELS_DIR / "lgb_vol_model.pkl", "rb") as f:
            self.m_lgb_vol = pickle.load(f)
            
        # Instanciar TreeExplainers para cada modelo
        self.exp_xgb_price = shap.TreeExplainer(self.m_xgb_price)
        self.exp_lgb_price = shap.TreeExplainer(self.m_lgb_price)
        self.exp_xgb_vol = shap.TreeExplainer(self.m_xgb_vol)
        self.exp_lgb_vol = shap.TreeExplainer(self.m_lgb_vol)
        
    def get_local_explanation(self, X_row: pd.DataFrame, target_type: str = "price") -> dict:
        """
        Calcula la explicación SHAP local para una fila específica.
        Devuelve el top-5 de factores que aumentan la predicción y el top-5 que la reducen.
        """
        if target_type == "price":
            shap_xgb = self.exp_xgb_price.shap_values(X_row)[0]
            shap_lgb = self.exp_lgb_price.shap_values(X_row)[0]
        else: # volume
            shap_xgb = self.exp_xgb_vol.shap_values(X_row)[0]
            shap_lgb = self.exp_lgb_vol.shap_values(X_row)[0]
            
        # Promedio de SHAP (ensemble)
        shap_ens = 0.5 * shap_xgb + 0.5 * shap_lgb
        
        feature_names = X_row.columns.tolist()
        feature_values = X_row.values[0]
        
        contributions = []
        for name, sh_val, feat_val in zip(feature_names, shap_ens, feature_values):
            # Omitir variables dummy que tengan valor 0 para no saturar con ruido OHE
            if ("product_code_" in name or "market_aggregated_" in name) and feat_val == 0:
                continue
            contributions.append({
                "feature": name,
                "value": float(feat_val),
                "shap_value": float(sh_val),
                "abs_value": float(abs(sh_val))
            })
            
        # Dividir en positivos y negativos
        positives = [c for c in contributions if c["shap_value"] > 0]
        negatives = [c for c in contributions if c["shap_value"] < 0]
        
        # Ordenar
        positives_sorted = sorted(positives, key=lambda x: x["shap_value"], reverse=True)[:5]
        negatives_sorted = sorted(negatives, key=lambda x: x["shap_value"], reverse=False)[:5]
        
        return {
            "top_positive": positives_sorted,
            "top_negative": negatives_sorted
        }

    def generate_global_plots(self, X_sample: pd.DataFrame):
        """Genera y guarda gráficos de explicabilidad global a 300 DPI."""
        log.info("Generando gráficos SHAP globales...")
        
        # Explicar una muestra
        shap_price_xgb = self.exp_xgb_price.shap_values(X_sample)
        shap_price_lgb = self.exp_lgb_price.shap_values(X_sample)
        shap_price_ens = 0.5 * shap_price_xgb + 0.5 * shap_price_lgb
        
        shap_vol_xgb = self.exp_xgb_vol.shap_values(X_sample)
        shap_vol_lgb = self.exp_lgb_vol.shap_values(X_sample)
        shap_vol_ens = 0.5 * shap_vol_xgb + 0.5 * shap_vol_lgb
        
        # 1. Summary Bar Plot - Precio
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_price_ens, X_sample, plot_type="bar", show=False)
        plt.title("TreeSHAP Global Feature Importance - FOB Unit Value (USD/kg)", fontsize=12, pad=15)
        plt.tight_layout()
        plt.savefig(STATIC_IMG_DIR / "shap_price_bar.png", dpi=300)
        plt.savefig(STATIC_IMG_DIR / "shap_price_bar.svg", dpi=300)
        plt.close()
        
        # 2. Beeswarm Plot - Precio
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_price_ens, X_sample, show=False)
        plt.title("TreeSHAP Beeswarm Plot - FOB Unit Value (USD/kg)", fontsize=12, pad=15)
        plt.tight_layout()
        plt.savefig(STATIC_IMG_DIR / "shap_price_beeswarm.png", dpi=300)
        plt.savefig(STATIC_IMG_DIR / "shap_price_beeswarm.svg", dpi=300)
        plt.close()

        # 3. Summary Bar Plot - Volumen
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_vol_ens, X_sample, plot_type="bar", show=False)
        plt.title("TreeSHAP Global Feature Importance - Export Volume (log-kg)", fontsize=12, pad=15)
        plt.tight_layout()
        plt.savefig(STATIC_IMG_DIR / "shap_volume_bar.png", dpi=300)
        plt.savefig(STATIC_IMG_DIR / "shap_volume_bar.svg", dpi=300)
        plt.close()
        
        # 4. Beeswarm Plot - Volumen
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_vol_ens, X_sample, show=False)
        plt.title("TreeSHAP Beeswarm Plot - Export Volume (log-kg)", fontsize=12, pad=15)
        plt.tight_layout()
        plt.savefig(STATIC_IMG_DIR / "shap_volume_beeswarm.png", dpi=300)
        plt.savefig(STATIC_IMG_DIR / "shap_volume_beeswarm.svg", dpi=300)
        plt.close()
        
        log.info("Gráficos globales SHAP guardados en %s.", STATIC_IMG_DIR)

def main():
    log.info("Cargando datos de anomaly_features.parquet...")
    df = load_data(GOLD_DIR / "anomaly_features.parquet")
    
    # Seleccionar las características usando la misma lógica que el entrenamiento (Capa 1)
    feature_cols_base = [
        c for c in df.columns if any(p in c for p in [
            "lag_", "rolling_", "pct_change_", "log_price_difference",
            "log_volume_difference", "week_sin", "week_cos", "month_sin", "month_cos",
            "price_age_weeks"
        ])
    ]
    dummy_cols = [c for c in df.columns if c.startswith("product_code_") or c.startswith("market_aggregated_")]
    feature_cols = feature_cols_base + dummy_cols
    
    # Instanciar el explicador
    explainer = IntegratedSHAPExplainer()
    
    # Generar gráficos globales sobre una muestra de 400 registros para velocidad
    sample_df = df[df["week_start"] < pd.to_datetime("2025-06-02")].sample(min(400, len(df)), random_state=42)
    X_sample = sample_df[feature_cols]
    explainer.generate_global_plots(X_sample)
    
    # Generar explicaciones locales para todas las alertas reales y guardarlas
    log.info("Generando explicaciones locales SHAP para alertas...")
    df_alerts = df[df["is_anomaly"] == 1].copy()
    
    local_explanations = {}
    for idx, row in df_alerts.iterrows():
        # Crear un DataFrame de 1 fila para pasar al explicador
        X_row = pd.DataFrame([row[feature_cols]])
        
        # Explicar precio y volumen
        exp_price = explainer.get_local_explanation(X_row, "price")
        exp_vol = explainer.get_local_explanation(X_row, "volume")
        
        # Crear clave única
        key = f"{row['product_code']}_{row['market_aggregated']}_{row['week_start'].strftime('%Y-%m-%d')}"
        local_explanations[key] = {
            "product_code": row["product_code"],
            "market": row["market_aggregated"],
            "week_start": row["week_start"].strftime("%Y-%m-%d"),
            "observed_price": float(row["fob_unit_value_usd_kg"]),
            "pred_price": float(row["pred_price"]),
            "price_residual": float(row["price_residual"]),
            "price_robust_z": float(row["price_residual_robust_z"]),
            "observed_volume": float(row["total_net_weight_kg"]),
            "pred_volume": float(row["pred_volume"]),
            "volume_residual": float(row["volume_residual"]),
            "volume_robust_z": float(row["volume_residual_robust_z"]),
            "ensemble_score": float(row["ensemble_score"]),
            "severity": row["severity"],
            "price_explanation": exp_price,
            "volume_explanation": exp_vol
        }
        
    # Guardar explicaciones locales
    out_path = GOLD_DIR / "local_explanations.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(local_explanations, f, indent=4)
    log.info("Explicaciones SHAP locales guardadas en %s (%d alertas explicadas).", out_path, len(local_explanations))

if __name__ == "__main__":
    main()
