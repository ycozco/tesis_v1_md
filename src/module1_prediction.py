#!/usr/bin/env python3
"""
src/module1_prediction.py
=========================
Implementa la Capa 1 (Predicción Tabular GBDT Global):
1. Carga prediction_features.
2. Divide en set de Desarrollo (antes de 2025-06-02) y Prueba Final.
3. Entrena modelos globales de Regresión (XGBoost y LightGBM) para:
   - Valor Unitario FOB (target_fob_unit_value_usd_kg_t1)
   - Volumen de Exportación (target_export_volume_kg_t1)
4. Optimiza hiperparámetros con Optuna (50 trials).
5. Genera predicciones out-of-fold para Desarrollo y predicciones sobre Prueba.
6. Calcula residuos robustos normalizados (robust-z con ventana de 13 semanas).

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import sys
import logging
import warnings
import pickle
import json
from pathlib import Path
import numpy as np
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
import optuna
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_log_error, r2_score

# Configuración de codificación de salida para Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Optuna verbosity lower
optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings('ignore', category=UserWarning)

# Configuración de rutas
BASE_DIR = Path(".")
GOLD_DIR = BASE_DIR / "data" / "gold"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Lista de semillas
SEEDS = [42, 123, 2026]

def save_data(df: pd.DataFrame, filepath: Path):
    try:
        df.to_parquet(filepath, index=False)
        log.info("Guardado Parquet en: %s", filepath)
    except ImportError:
        csv_path = filepath.with_suffix(".csv")
        df.to_csv(csv_path, index=False)
        log.info("Guardado CSV (fallback) en: %s", csv_path)

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

def calculate_robust_z(series):
    """Calcula el robust z-score usando una ventana móvil de 13 semanas."""
    rolling_median = series.rolling(13, min_periods=1).median()
    rolling_mad = series.rolling(13, min_periods=1).apply(lambda x: np.median(np.abs(x - np.median(x))), raw=True)
    return (series - rolling_median) / (1.4826 * rolling_mad + 1e-5)

def run_optuna_tuning(X, y, model_type, target_type, n_trials=50) -> dict:
    """Optimiza los hiperparámetros con Optuna usando TimeSeriesSplit (5 splits)."""
    tscv = TimeSeriesSplit(n_splits=5)
    
    def objective(trial):
        if model_type == "xgb":
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 300, 1500),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
                'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
                'min_child_weight': trial.suggest_int('min_child_weight', 1, 20),
                'reg_alpha': trial.suggest_float('reg_alpha', 0, 10),
                'reg_lambda': trial.suggest_float('reg_lambda', 0.1, 20),
                'random_state': 42,
                'n_jobs': -1,
                'verbosity': 0
            }
        else: # lgb
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 300, 1500),
                'num_leaves': trial.suggest_int('num_leaves', 15, 127),
                'max_depth': trial.suggest_int('max_depth', 4, 12),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
                'min_child_samples': trial.suggest_int('min_child_samples', 10, 100),
                'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
                'reg_alpha': trial.suggest_float('reg_alpha', 0, 10),
                'reg_lambda': trial.suggest_float('reg_lambda', 0.1, 20),
                'random_state': 42,
                'n_jobs': -1,
                'verbosity': -1
            }
            
        scores = []
        for train_idx, val_idx in tscv.split(X):
            X_tr, X_v = X.iloc[train_idx], X.iloc[val_idx]
            y_tr, y_v = y.iloc[train_idx], y.iloc[val_idx]
            
            if model_type == "xgb":
                model = xgb.XGBRegressor(**params)
            else:
                model = lgb.LGBMRegressor(**params)
                
            model.fit(X_tr, y_tr)
            preds = model.predict(X_v)
            
            if target_type == "volume":
                # Para volumen evaluamos en RMSLE
                preds_orig = np.expm1(np.clip(preds, 0, None))
                y_v_orig = np.expm1(y_v)
                rmse = np.sqrt(np.mean((np.log1p(preds_orig) - np.log1p(y_v_orig)) ** 2))
                scores.append(rmse)
            else:
                # Para precio evaluamos en MAE
                scores.append(mean_absolute_error(y_v, preds))
                
        return np.mean(scores)

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials)
    return study.best_params

def train_and_predict():
    log.info("Cargando prediction_features...")
    df = load_data(GOLD_DIR / "prediction_features.parquet")
    
    df["week_start"] = pd.to_datetime(df["week_start"])
    df = df.sort_values(by=["product_code", "market_aggregated", "week_start"]).reset_index(drop=True)
    
    # Separar en Desarrollo (antes de 2025-06-02) y Prueba Final (últimas 52 semanas)
    split_date = pd.to_datetime("2025-06-02")
    df_dev = df[df["week_start"] < split_date].copy()
    df_test = df[df["week_start"] >= split_date].copy()
    
    # -------------------------------------------------------------------------
    # Definición de características de entrada
    # -------------------------------------------------------------------------
    feature_cols = [
        c for c in df.columns if any(p in c for p in [
            "lag_", "rolling_", "pct_change_", "log_price_difference",
            "log_volume_difference", "week_sin", "week_cos", "month_sin", "month_cos",
            "price_age_weeks"
        ])
    ]
    
    # One-hot encoding de product_code y market_aggregated
    df_encoded = pd.get_dummies(df[["product_code", "market_aggregated"] + feature_cols], columns=["product_code", "market_aggregated"])
    encoded_feature_cols = [c for c in df_encoded.columns if c not in ["product_code", "market_aggregated"]]
    
    # Unir columnas codificadas al df principal sin perder las columnas originales
    df = pd.concat([df, df_encoded], axis=1)
    df = df.loc[:, ~df.columns.duplicated()] # eliminar duplicados si los hay
    
    # Separar df de Desarrollo y Prueba Final codificados
    df_dev = df[df["week_start"] < split_date].copy()
    df_test = df[df["week_start"] >= split_date].copy()
    
    # Inicializar columnas para predicciones
    df["pred_price"] = np.nan
    df["pred_volume"] = np.nan
    
    # -------------------------------------------------------------------------
    # PARTE A: Modelo de Precio (Valor Unitario FOB)
    # -------------------------------------------------------------------------
    log.info("--- MODELAMIENTO DE PRECIO (VALOR UNITARIO FOB) ---")
    # Filtrar nulos en target (semanas sin exportaciones) para el entrenamiento de precio
    dev_price = df_dev[df_dev["target_fob_unit_value_usd_kg_t1"].notna()]
    X_dev_price = dev_price[encoded_feature_cols]
    y_dev_price = dev_price["target_fob_unit_value_usd_kg_t1"]
    
    # Optuna tuning
    log.info("Optimizando XGBoost para precio...")
    xgb_price_params = run_optuna_tuning(X_dev_price, y_dev_price, "xgb", "price", n_trials=10)
    log.info("Optimizando LightGBM para precio...")
    lgb_price_params = run_optuna_tuning(X_dev_price, y_dev_price, "lgb", "price", n_trials=10)
    
    # Generar predicciones out-of-fold para el periodo de desarrollo
    tscv = TimeSeriesSplit(n_splits=5)
    
    # Mapeo de índices para indexación correcta
    price_indices = dev_price.index.tolist()
    
    for train_idx, val_idx in tscv.split(X_dev_price):
        X_tr, X_v = X_dev_price.iloc[train_idx], X_dev_price.iloc[val_idx]
        y_tr = y_dev_price.iloc[train_idx]
        
        # Ensemble 50% XGB y 50% LGB
        m_xgb = xgb.XGBRegressor(**xgb_price_params, random_state=42)
        m_lgb = lgb.LGBMRegressor(**lgb_price_params, random_state=42)
        
        m_xgb.fit(X_tr, y_tr)
        m_lgb.fit(X_tr, y_tr)
        
        preds = 0.5 * m_xgb.predict(X_v) + 0.5 * m_lgb.predict(X_v)
        
        # Asignar directamente al df principal usando indices globales
        global_val_indices = [price_indices[i] for i in val_idx]
        df.loc[global_val_indices, "pred_price"] = preds
            
    # Para la primera ventana de TimeSeriesSplit que no tiene predicciones oof, 
    # entrenar en el primer split y predecir
    first_train_idx = tscv.split(X_dev_price).__next__()[0]
    X_tr_first = X_dev_price.iloc[first_train_idx]
    y_tr_first = y_dev_price.iloc[first_train_idx]
    m_xgb_first = xgb.XGBRegressor(**xgb_price_params, random_state=42).fit(X_tr_first, y_tr_first)
    m_lgb_first = lgb.LGBMRegressor(**lgb_price_params, random_state=42).fit(X_tr_first, y_tr_first)
    preds_first = 0.5 * m_xgb_first.predict(X_dev_price.iloc[first_train_idx]) + 0.5 * m_lgb_first.predict(X_dev_price.iloc[first_train_idx])
    global_train_indices = [price_indices[i] for i in first_train_idx]
    df.loc[global_train_indices, "pred_price"] = preds_first
    
    # Entrenar modelos finales sobre todo el periodo de desarrollo para predecir test
    m_xgb_price_final = xgb.XGBRegressor(**xgb_price_params, random_state=42).fit(X_dev_price, y_dev_price)
    m_lgb_price_final = lgb.LGBMRegressor(**lgb_price_params, random_state=42).fit(X_dev_price, y_dev_price)
    
    # Guardar modelos de precio
    with open(MODELS_DIR / "xgb_price_model.pkl", "wb") as f:
        pickle.dump(m_xgb_price_final, f)
    with open(MODELS_DIR / "lgb_price_model.pkl", "wb") as f:
        pickle.dump(m_lgb_price_final, f)
        
    # Predecir test set
    X_test_price = df_test[encoded_feature_cols]
    preds_test_price = 0.5 * m_xgb_price_final.predict(X_test_price) + 0.5 * m_lgb_price_final.predict(X_test_price)
    df.loc[df["week_start"] >= split_date, "pred_price"] = preds_test_price
    
    # -------------------------------------------------------------------------
    # PARTE B: Modelo de Volumen (Export Volume)
    # -------------------------------------------------------------------------
    log.info("--- MODELAMIENTO DE VOLUMEN (EXPORT VOLUME) ---")
    X_dev_vol = df_dev[encoded_feature_cols]
    # Aplicar transformación log1p
    y_dev_vol = np.log1p(df_dev["target_export_volume_kg_t1"])
    
    # Optuna tuning
    log.info("Optimizando XGBoost para volumen...")
    xgb_vol_params = run_optuna_tuning(X_dev_vol, y_dev_vol, "xgb", "volume", n_trials=10)
    log.info("Optimizando LightGBM para volumen...")
    lgb_vol_params = run_optuna_tuning(X_dev_vol, y_dev_vol, "lgb", "volume", n_trials=10)
    
    # Generar predicciones oof para volumen
    vol_indices = df_dev.index.tolist()
    
    for train_idx, val_idx in tscv.split(X_dev_vol):
        X_tr, X_v = X_dev_vol.iloc[train_idx], X_dev_vol.iloc[val_idx]
        y_tr = y_dev_vol.iloc[train_idx]
        
        m_xgb = xgb.XGBRegressor(**xgb_vol_params, random_state=42)
        m_lgb = lgb.LGBMRegressor(**lgb_vol_params, random_state=42)
        
        m_xgb.fit(X_tr, y_tr)
        m_lgb.fit(X_tr, y_tr)
        
        preds_log = 0.5 * m_xgb.predict(X_v) + 0.5 * m_lgb.predict(X_v)
        # Convertir a escala original con expm1 y asignar directamente usando indices globales
        global_val_indices = [vol_indices[i] for i in val_idx]
        df.loc[global_val_indices, "pred_volume"] = np.expm1(np.clip(preds_log, 0, None))
        
    # Primer split predictions
    m_xgb_first = xgb.XGBRegressor(**xgb_vol_params, random_state=42).fit(X_dev_vol.iloc[first_train_idx], y_dev_vol.iloc[first_train_idx])
    m_lgb_first = lgb.LGBMRegressor(**lgb_vol_params, random_state=42).fit(X_dev_vol.iloc[first_train_idx], y_dev_vol.iloc[first_train_idx])
    preds_first_log = 0.5 * m_xgb_first.predict(X_dev_vol.iloc[first_train_idx]) + 0.5 * m_lgb_first.predict(X_dev_vol.iloc[first_train_idx])
    global_train_indices = [vol_indices[i] for i in first_train_idx]
    df.loc[global_train_indices, "pred_volume"] = np.expm1(np.clip(preds_first_log, 0, None))
    
    # Entrenar modelos finales sobre todo el periodo de desarrollo para predecir test
    m_xgb_vol_final = xgb.XGBRegressor(**xgb_vol_params, random_state=42).fit(X_dev_vol, y_dev_vol)
    m_lgb_vol_final = lgb.LGBMRegressor(**lgb_vol_params, random_state=42).fit(X_dev_vol, y_dev_vol)
    
    # Guardar modelos de volumen
    with open(MODELS_DIR / "xgb_vol_model.pkl", "wb") as f:
        pickle.dump(m_xgb_vol_final, f)
    with open(MODELS_DIR / "lgb_vol_model.pkl", "wb") as f:
        pickle.dump(m_lgb_vol_final, f)
        
    # Predecir test set
    X_test_vol = df_test[encoded_feature_cols]
    preds_test_vol_log = 0.5 * m_xgb_vol_final.predict(X_test_vol) + 0.5 * m_lgb_vol_final.predict(X_test_vol)
    df.loc[df["week_start"] >= split_date, "pred_volume"] = np.expm1(np.clip(preds_test_vol_log, 0, None))
    
    # -------------------------------------------------------------------------
    # Cálculo de Residuos e Ingeniería de Anomalías
    # -------------------------------------------------------------------------
    log.info("Calculando residuos analíticos y normalizaciones robust-z...")
    
    # Residuos de precio (raw)
    df["price_residual"] = df["target_fob_unit_value_usd_kg_t1"] - df["pred_price"]
    df["price_abs_residual"] = df["price_residual"].abs()
    
    # Residuos de volumen (raw)
    df["volume_residual"] = df["target_export_volume_kg_t1"] - df["pred_volume"]
    df["volume_abs_residual"] = df["volume_residual"].abs()
    
    # Calcular robust z-scores agrupados por producto y mercado (ventana de 13 semanas)
    df = df.sort_values(by=["product_code", "market_aggregated", "week_start"]).reset_index(drop=True)
    grp_res = df.groupby(["product_code", "market_aggregated"])
    
    df["price_residual_robust_z"] = grp_res["price_residual"].transform(calculate_robust_z)
    df["price_abs_residual_robust_z"] = grp_res["price_abs_residual"].transform(calculate_robust_z)
    df["volume_residual_robust_z"] = grp_res["volume_residual"].transform(calculate_robust_z)
    df["volume_abs_residual_robust_z"] = grp_res["volume_abs_residual"].transform(calculate_robust_z)
    
    # Rellenar NaNs residuales de semanas sin exportación
    df["price_residual"] = df["price_residual"].fillna(0)
    df["price_abs_residual"] = df["price_abs_residual"].fillna(0)
    df["price_residual_robust_z"] = df["price_residual_robust_z"].fillna(0)
    df["price_abs_residual_robust_z"] = df["price_abs_residual_robust_z"].fillna(0)
    
    # Guardar anomalía features
    save_data(df, GOLD_DIR / "anomaly_features.parquet")
    log.info("Capa 1 completada exitosamente. Archivo guardado en anomaly_features.parquet.")

if __name__ == "__main__":
    train_and_predict()
