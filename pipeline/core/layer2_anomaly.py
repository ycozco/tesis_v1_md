#!/usr/bin/env python3
"""
src/module2_anomaly.py
======================
Implementa la Capa 2 (Detección de Anomalías - Ensemble No Supervisado):
1. Carga anomaly_features.parquet (con los residuos de Capa 1).
2. Selecciona variables operativas, logísticas, climáticas y de residuos.
3. Entrena Isolation Forest, LOF y ECOD sobre el set de Desarrollo.
4. Normaliza scores a percentiles [0, 1] usando la distribución de entrenamiento.
5. Genera el ensemble (promedio de percentiles) y activa alertas si score >= 0.95 o votos >= 2.
6. Realiza un experimento controlado inyectando 5% de anomalías sintéticas (Tipos A-E)
   para calcular Precision, Recall, F1, PR-AUC, ROC-AUC y Recall por Tipo.
7. Guarda los modelos, el scaler, las alertas reales y las métricas en JSON.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import sys
import logging
import time
import pickle
import json
from pathlib import Path
import numpy as np
import pandas as pd
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.ecod import ECOD
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import precision_recall_curve, auc, roc_auc_score, f1_score, precision_score, recall_score

# Configuración de codificación de salida para Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Configuración de rutas
BASE_DIR = Path(".")
GOLD_DIR = BASE_DIR / "data" / "gold"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Columnas seleccionadas para la detección de anomalías
ANOMALY_FEATURE_COLS = [
    "price_residual_robust_z", "price_abs_residual_robust_z",
    "volume_residual_robust_z", "volume_abs_residual_robust_z",
    "price_pct_change_1", "price_pct_change_4", "price_pct_change_52",
    "volume_pct_change_1", "volume_pct_change_4", "volume_pct_change_52",
    "dias_logisticos_lag1", "costo_logistico_usd_kg_lag1",
    "cumplimiento_fitosanitario_lag1", "merma_pct_lag1",
    "temperatura_max_c_lag1", "temperatura_min_c_lag1",
    "precipitacion_mm_lag1", "humedad_pct_lag1",
    "destination_volume_share_lag1", "destination_fob_share_lag1"
]

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

def save_data(df: pd.DataFrame, filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_parquet(filepath, index=False)
        log.info("Guardado Parquet en: %s", filepath)
    except ImportError:
        csv_path = filepath.with_suffix(".csv")
        df.to_csv(csv_path, index=False)
        log.info("Guardado CSV (fallback) en: %s", csv_path)

def percentile_normalize(scores: np.ndarray, train_scores: np.ndarray) -> np.ndarray:
    """Calcula el percentil de cada score respecto a la distribución de entrenamiento."""
    sorted_train = np.sort(train_scores)
    pos = np.searchsorted(sorted_train, scores, side='right')
    return np.clip(pos / len(train_scores), 0.0, 1.0)

def inject_synthetic_anomalies(df: pd.DataFrame, seed: int, rate: float = 0.05) -> pd.DataFrame:
    """
    Inyecta un 5% de anomalías de manera estratificada.
    Distribuye los tipos uniformemente:
    - Tipo A: precio (residuos y cambios drásticos)
    - Tipo B: volumen (residuos y cambios drásticos)
    - Tipo C: clima (temperaturas extremas con sequía)
    - Tipo D: logística (retrasos severos con sobrecosto)
    - Tipo E: calidad (mermas muy elevadas)
    """
    df_copy = df.copy()
    n = len(df_copy)
    n_anom = int(round(rate * n))
    
    rng = np.random.default_rng(seed)
    selected_indices = rng.choice(n, size=n_anom, replace=False)
    
    df_copy["etiqueta_anomalia"] = 0
    df_copy["tipo_anomalia"] = "none"
    df_copy["regla_inyeccion"] = ""
    
    # Asignar 5 tipos equitativamente
    types = ["precio", "volumen", "clima", "logistica", "calidad"]
    type_assignments = [types[i % 5] for i in range(n_anom)]
    
    # Mapeo de índices globales del DataFrame
    global_indices = df_copy.index.tolist()
    
    for local_idx, idx in enumerate(selected_indices):
        global_idx = global_indices[idx]
        tipo = type_assignments[local_idx]
        df_copy.loc[global_idx, "etiqueta_anomalia"] = 1
        df_copy.loc[global_idx, "tipo_anomalia"] = tipo
        
        if tipo == "precio":
            # Residuos y variaciones extremos de precio (Subvaluación/Sobrevaluación)
            direction = rng.choice([-1, 1])
            df_copy.loc[global_idx, "price_residual_robust_z"] = direction * 4.5
            df_copy.loc[global_idx, "price_abs_residual_robust_z"] = 4.5
            df_copy.loc[global_idx, "price_pct_change_1"] = 1.5 if direction > 0 else -0.8
            df_copy.loc[global_idx, "regla_inyeccion"] = f"precio_resid_z = {direction * 4.5:.1f}"
            
        elif tipo == "volumen":
            # Residuos y variaciones extremos de volumen (Volumen inusual)
            direction = rng.choice([-1, 1])
            df_copy.loc[global_idx, "volume_residual_robust_z"] = direction * 4.5
            df_copy.loc[global_idx, "volume_abs_residual_robust_z"] = 4.5
            df_copy.loc[global_idx, "volume_pct_change_1"] = 2.0 if direction > 0 else -0.9
            df_copy.loc[global_idx, "regla_inyeccion"] = f"volumen_resid_z = {direction * 4.5:.1f}"
            
        elif tipo == "clima":
            # Temperatura extremadamente alta y precipitación nula (Drought)
            df_copy.loc[global_idx, "temperatura_max_c_lag1"] = rng.uniform(36.0, 39.0)
            df_copy.loc[global_idx, "precipitacion_mm_lag1"] = 0.0
            df_copy.loc[global_idx, "regla_inyeccion"] = "temp_max > 36 AND precip = 0"
            
        elif tipo == "logistica":
            # Días logísticos muy elevados y sobrecosto
            df_copy.loc[global_idx, "dias_logisticos_lag1"] = rng.uniform(35.0, 45.0)
            df_copy.loc[global_idx, "costo_logistico_usd_kg_lag1"] = rng.uniform(1.2, 1.8)
            df_copy.loc[global_idx, "regla_inyeccion"] = "dias_log > 35 AND costo_log > 1.2"
            
        elif tipo == "calidad":
            # Mermas críticas
            df_copy.loc[global_idx, "merma_pct_lag1"] = rng.uniform(25.0, 30.0)
            df_copy.loc[global_idx, "regla_inyeccion"] = "merma > 25%"
            
    return df_copy

def evaluate_predictions(y_true: np.ndarray, scores: np.ndarray, threshold: float = 0.95) -> dict:
    """Calcula métricas de detección a un umbral operativo fijo."""
    preds = (scores >= threshold).astype(int)
    
    # Precision-Recall Curve para PR-AUC
    precision_curve, recall_curve, _ = precision_recall_curve(y_true, scores)
    pr_auc = auc(recall_curve, precision_curve)
    
    # ROC-AUC
    try:
        roc_auc = roc_auc_score(y_true, scores)
    except Exception:
        roc_auc = 0.5
        
    return {
        "pr_auc": float(pr_auc),
        "roc_auc": float(roc_auc),
        "f1": float(f1_score(y_true, preds, zero_division=0)),
        "precision": float(precision_score(y_true, preds, zero_division=0)),
        "recall": float(recall_score(y_true, preds, zero_division=0)),
        "threshold": float(threshold)
    }

def main():
    log.info("Cargando anomaly_features.parquet...")
    df = load_data(GOLD_DIR / "anomaly_features.parquet")
    
    df["week_start"] = pd.to_datetime(df["week_start"])
    df = df.sort_values(by=["product_code", "market_aggregated", "week_start"]).reset_index(drop=True)
    
    # Separar en Desarrollo (entrenamiento) y Prueba Final
    split_date = pd.to_datetime("2025-06-02")
    df_dev = df[df["week_start"] < split_date].copy()
    df_test = df[df["week_start"] >= split_date].copy()
    
    # Preparación de datos reales (rellenar NaNs de lags a 0)
    X_train_df = df_dev[ANOMALY_FEATURE_COLS].fillna(0)
    X_test_df = df_test[ANOMALY_FEATURE_COLS].fillna(0)
    X_full_df = df[ANOMALY_FEATURE_COLS].fillna(0)
    
    # Escalador robusto
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train_df)
    X_test_scaled = scaler.transform(X_test_df)
    X_full_scaled = scaler.transform(X_full_df)
    
    # Guardar scaler
    with open(MODELS_DIR / "anomaly_scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
        
    # -------------------------------------------------------------------------
    # Entrenamiento de Detectores (PyOD)
    # -------------------------------------------------------------------------
    log.info("Entrenando detectores Isolation Forest, LOF y ECOD...")
    
    # IF
    t0 = time.time()
    model_if = IForest(contamination=0.05, random_state=42, n_jobs=1)
    model_if.fit(X_train_scaled)
    t_if = time.time() - t0
    
    # LOF
    t0 = time.time()
    model_lof = LOF(contamination=0.05, n_jobs=1)
    model_lof.fit(X_train_scaled)
    t_lof = time.time() - t0
    
    # ECOD
    t0 = time.time()
    model_ecod = ECOD(contamination=0.05)
    model_ecod.fit(X_train_scaled)
    t_ecod = time.time() - t0
    
    # Guardar modelos
    with open(MODELS_DIR / "if_model.pkl", "wb") as f:
        pickle.dump(model_if, f)
    with open(MODELS_DIR / "lof_model.pkl", "wb") as f:
        pickle.dump(model_lof, f)
    with open(MODELS_DIR / "ecod_model.pkl", "wb") as f:
        pickle.dump(model_ecod, f)
        
    # Obtener scores brutos de entrenamiento (calibración)
    train_scores_if = model_if.decision_scores_
    train_scores_lof = model_lof.decision_scores_
    train_scores_ecod = model_ecod.decision_scores_
    
    # -------------------------------------------------------------------------
    # Predicción y Alertas sobre Datos Reales
    # -------------------------------------------------------------------------
    log.info("Calculando percentiles y ensemble sobre datos reales...")
    
    scores_if = model_if.decision_function(X_full_scaled)
    scores_lof = model_lof.decision_function(X_full_scaled)
    scores_ecod = model_ecod.decision_function(X_full_scaled)
    
    df["pct_if"] = percentile_normalize(scores_if, train_scores_if)
    df["pct_lof"] = percentile_normalize(scores_lof, train_scores_lof)
    df["pct_ecod"] = percentile_normalize(scores_ecod, train_scores_ecod)
    
    # Score consolidado y votos
    df["ensemble_score"] = (df["pct_if"] + df["pct_lof"] + df["pct_ecod"]) / 3.0
    
    votes = ((df["pct_if"] >= 0.95).astype(int) + 
             (df["pct_lof"] >= 0.95).astype(int) + 
             (df["pct_ecod"] >= 0.95).astype(int))
    df["votes"] = votes
    
    # Alerta activa si score >= 0.95 o votos >= 2
    df["is_anomaly"] = ((df["ensemble_score"] >= 0.95) | (df["votes"] >= 2)).astype(int)
    
    # Severidad
    df["severity"] = "none"
    df.loc[df["is_anomaly"] == 1, "severity"] = "Baja"
    df.loc[df["ensemble_score"] >= 0.975, "severity"] = "Media"
    df.loc[df["ensemble_score"] >= 0.99, "severity"] = "Alta"
    
    # Guardar dataframe unificado con predicciones e indicadores
    save_data(df, GOLD_DIR / "anomaly_features.parquet")
    
    # Guardar alertas reales
    df_alerts = df[df["is_anomaly"] == 1].copy()
    save_data(df_alerts, GOLD_DIR / "alerts.parquet")
    log.info("Detectadas %d alertas reales en total (%d en test).", len(df_alerts), len(df_alerts[df_alerts["week_start"] >= split_date]))
    
    # -------------------------------------------------------------------------
    # EXPERIMENTO DE VALIDACIÓN SINTÉTICA (E1)
    # -------------------------------------------------------------------------
    log.info("=== INICIANDO EXPERIMENTO DE VALIDACIÓN SINTÉTICA E1 ===")
    
    # Generar sets de validación y test con anomalías sintéticas inyectadas al 5%
    df_val_synth = inject_synthetic_anomalies(df_dev, seed=4201, rate=0.05)
    df_test_synth = inject_synthetic_anomalies(df_test, seed=4202, rate=0.05)
    
    # Obtener arrays de características y ground truth
    X_val_s_df = df_val_synth[ANOMALY_FEATURE_COLS].fillna(0)
    y_val_true = df_val_synth["etiqueta_anomalia"].values
    
    X_test_s_df = df_test_synth[ANOMALY_FEATURE_COLS].fillna(0)
    y_test_true = df_test_synth["etiqueta_anomalia"].values
    
    # Escalar
    X_val_s_scaled = scaler.transform(X_val_s_df)
    X_test_s_scaled = scaler.transform(X_test_s_df)
    
    # Calcular scores brutos en conjuntos sintéticos
    # IF
    val_s_if = model_if.decision_function(X_val_s_scaled)
    test_s_if = model_if.decision_function(X_test_s_scaled)
    
    # LOF
    val_s_lof = model_lof.decision_function(X_val_s_scaled)
    test_s_lof = model_lof.decision_function(X_test_s_scaled)
    
    # ECOD
    val_s_ecod = model_ecod.decision_function(X_val_s_scaled)
    test_s_ecod = model_ecod.decision_function(X_test_s_scaled)
    
    # Normalizar a percentiles
    pct_val_if = percentile_normalize(val_s_if, train_scores_if)
    pct_test_if = percentile_normalize(test_s_if, train_scores_if)
    
    pct_val_lof = percentile_normalize(val_s_lof, train_scores_lof)
    pct_test_lof = percentile_normalize(test_s_lof, train_scores_lof)
    
    pct_val_ecod = percentile_normalize(val_s_ecod, train_scores_ecod)
    pct_test_ecod = percentile_normalize(test_s_ecod, train_scores_ecod)
    
    # Ensemble scores
    score_val_b2 = (pct_val_if + pct_val_lof) / 2.0
    score_test_b2 = (pct_test_if + pct_test_lof) / 2.0
    
    score_val_ens = (pct_val_if + pct_val_lof + pct_val_ecod) / 3.0
    score_test_ens = (pct_test_if + pct_test_lof + pct_test_ecod) / 3.0
    
    # Calcular métricas para cada detector y ensemble en el Test Set Sintético
    metrics = {
        "if": evaluate_predictions(y_test_true, pct_test_if, threshold=0.95),
        "lof": evaluate_predictions(y_test_true, pct_test_lof, threshold=0.95),
        "ecod": evaluate_predictions(y_test_true, pct_test_ecod, threshold=0.95),
        "ensemble_b2": evaluate_predictions(y_test_true, score_test_b2, threshold=0.95),
        "ensemble_propuesto": evaluate_predictions(y_test_true, score_test_ens, threshold=0.95),
    }
    
    # Añadir tiempos de inferencia promedio aproximados por registro en test set (ms)
    n_test = len(df_test)
    metrics["if"]["inference_time_ms"] = float((t_if / len(df_dev)) * 1000)
    metrics["lof"]["inference_time_ms"] = float((t_lof / len(df_dev)) * 1000)
    metrics["ecod"]["inference_time_ms"] = float((t_ecod / len(df_dev)) * 1000)
    metrics["ensemble_b2"]["inference_time_ms"] = float(((t_if + t_lof) / len(df_dev)) * 1000)
    metrics["ensemble_propuesto"]["inference_time_ms"] = float(((t_if + t_lof + t_ecod) / len(df_dev)) * 1000)
    
    # -------------------------------------------------------------------------
    # EVALUACIÓN DE RECALL POR TIPO DE ANOMALÍA (Tabla 4.2)
    # -------------------------------------------------------------------------
    log.info("Evaluando Recall por tipo de anomalía en el conjunto de test...")
    
    # Predicción final sobre test set sintético con la regla operativa
    test_votes = ((pct_test_if >= 0.95).astype(int) + 
                  (pct_test_lof >= 0.95).astype(int) + 
                  (pct_test_ecod >= 0.95).astype(int))
    df_test_synth["pred_ensemble"] = ((score_test_ens >= 0.95) | (test_votes >= 2)).astype(int)
    
    # Recall por tipo (Proposed Ensemble vs Baseline B1/B2)
    df_test_synth["pred_b1"] = (pct_test_if >= 0.95).astype(int)
    
    recall_by_type = {}
    anomaly_types = ["precio", "volumen", "clima", "logistica", "calidad"]
    for tipo in anomaly_types:
        sub_df = df_test_synth[df_test_synth["tipo_anomalia"] == tipo]
        if len(sub_df) > 0:
            rec_ens = recall_score(sub_df["etiqueta_anomalia"], sub_df["pred_ensemble"], zero_division=0)
            rec_b1 = recall_score(sub_df["etiqueta_anomalia"], sub_df["pred_b1"], zero_division=0)
            recall_by_type[tipo] = {
                "recall_ensemble": float(rec_ens),
                "recall_baseline": float(rec_b1),
                "diff": float(rec_ens - rec_b1)
            }
            log.info("Recall Tipo %s: Ensemble = %.4f | Baseline IF = %.4f | Diff = %+.4f",
                     tipo.upper(), rec_ens, rec_b1, rec_ens - rec_b1)
            
    metrics["recall_by_type"] = recall_by_type
    
    # Guardar métricas experimentales
    metrics_path = GOLD_DIR / "anomaly_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
        
    log.info("Resultados de Detección (Conjunto de Test Sintético):")
    for method, met in metrics.items():
        if method == "recall_by_type":
            continue
        log.info("%s: PR-AUC = %.4f | ROC-AUC = %.4f | F1 = %.4f | Precision = %.4f | Recall = %.4f | T.Inf = %.4f ms",
                 method.upper(), met["pr_auc"], met["roc_auc"], met["f1"],
                 met["precision"], met["recall"], met["inference_time_ms"])
        
    log.info("Métricas guardadas exitosamente en %s.", metrics_path)

if __name__ == "__main__":
    main()
