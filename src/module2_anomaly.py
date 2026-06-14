#!/usr/bin/env python3
"""
src/module2_anomaly.py
======================
Implementa la Capa 2 (Detección de Anomalías - Ensemble No Supervisado):
1. Carga los datos procesados (con residuos de la Capa 1).
2. Entrena Isolation Forest, LOF y ECOD.
3. Normaliza probabilísticamente las puntuaciones utilizando el MinMax del conjunto de entrenamiento.
4. Consolida y evalúa detectores individuales y ensembles.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import sys
import logging
import time
from pathlib import Path
import numpy as np
import pandas as pd
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.ecod import ECOD
from sklearn.metrics import precision_recall_curve, auc, roc_auc_score, f1_score, precision_score, recall_score

# Configuración de codificación de salida para Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def minmax_normalize(scores: np.ndarray, min_val: float, max_val: float) -> np.ndarray:
    """Normaliza de forma probabilística (lineal) un vector de scores a [0, 1]."""
    if max_val - min_val == 0:
        return np.zeros_like(scores)
    return np.clip((scores - min_val) / (max_val - min_val), 0, 1)


def evaluate_scores(y_true: np.ndarray, scores: np.ndarray, threshold: float = None) -> dict:
    """Calcula todas las métricas de rendimiento basadas en scores y etiquetas reales."""
    precision, recall, thresholds = precision_recall_curve(y_true, scores)
    pr_auc = auc(recall, precision)
    roc_auc = roc_auc_score(y_true, scores)
    
    # Si no se provee umbral, buscar el que maximice F1
    if threshold is None:
        f1_scores = []
        for t in thresholds:
            preds = (scores >= t).astype(int)
            f1_scores.append(f1_score(y_true, preds))
        if len(f1_scores) > 0:
            opt_idx = np.argmax(f1_scores)
            threshold = thresholds[opt_idx]
            f1 = f1_scores[opt_idx]
        else:
            threshold = 0.5
            f1 = 0.0
    else:
        preds = (scores >= threshold).astype(int)
        f1 = f1_score(y_true, preds)
        
    opt_preds = (scores >= threshold).astype(int)
    
    return {
        "pr_auc": pr_auc,
        "roc_auc": roc_auc,
        "f1": f1,
        "precision": precision_score(y_true, opt_preds, zero_division=0),
        "recall": recall_score(y_true, opt_preds, zero_division=0),
        "threshold": threshold
    }


def run_anomaly_experiment(data_dir: Path, seed: int, contamination: float = 0.08, include_capa1: bool = True) -> dict:
    """Entrena los detectores en el conjunto de entrenamiento y evalúa en el de pruebas."""
    train_path = data_dir / "dataset_processed_train_raw.csv"
    test_path = data_dir / "dataset_processed_test.csv"
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    # Determinar columnas a usar
    exclude_cols = ["etiqueta_anomalia"]
    if not include_capa1:
        exclude_cols.extend(["pred_precio_kg_usd", "residual_precio_kg_usd"])
        
    feature_cols = [c for c in train_df.columns if c not in exclude_cols]
    
    X_train = train_df[feature_cols]
    X_test = test_df[feature_cols]
    y_test = test_df["etiqueta_anomalia"]
    
    # 1. Instanciar detectores
    # Usar n_jobs=1 para evitar problemas de paralelización en LOF en sistemas Windows
    model_if = IForest(contamination=contamination, random_state=seed, n_jobs=1)
    model_lof = LOF(contamination=contamination, n_jobs=1)
    model_ecod = ECOD(contamination=contamination)
    
    # 2. Entrenar y predecir
    # IF
    t0 = time.time()
    model_if.fit(X_train)
    t_if = time.time() - t0
    train_s_if = model_if.decision_scores_
    test_s_if = model_if.decision_function(X_test)
    
    # LOF
    t0 = time.time()
    model_lof.fit(X_train)
    t_lof = time.time() - t0
    train_s_lof = model_lof.decision_scores_
    test_s_lof = model_lof.decision_function(X_test)
    
    # ECOD
    t0 = time.time()
    model_ecod.fit(X_train)
    t_ecod = time.time() - t0
    train_s_ecod = model_ecod.decision_scores_
    test_s_ecod = model_ecod.decision_function(X_test)
    
    # 3. Normalizar puntuaciones marginales utilizando MinMax del set de entrenamiento
    norm_train_if = minmax_normalize(train_s_if, train_s_if.min(), train_s_if.max())
    norm_test_if = minmax_normalize(test_s_if, train_s_if.min(), train_s_if.max())
    
    norm_train_lof = minmax_normalize(train_s_lof, train_s_lof.min(), train_s_lof.max())
    norm_test_lof = minmax_normalize(test_s_lof, train_s_lof.min(), train_s_lof.max())
    
    norm_train_ecod = minmax_normalize(train_s_ecod, train_s_ecod.min(), train_s_ecod.max())
    norm_test_ecod = minmax_normalize(test_s_ecod, train_s_ecod.min(), train_s_ecod.max())
    
    # 4. Agregación (Ensembles)
    # Ensemble B2 (IF + LOF)
    train_s_b2 = (norm_train_if + norm_train_lof) / 2
    test_s_b2 = (norm_test_if + norm_test_lof) / 2
    
    # Ensemble Propuesto (IF + LOF + ECOD)
    train_s_ens = (norm_train_if + norm_train_lof + norm_train_ecod) / 3
    test_s_ens = (norm_test_if + norm_test_lof + norm_test_ecod) / 3
    
    # Si estamos en el set de pruebas sintético, evaluamos cuantitativamente
    results = {}
    if y_test.nunique() > 1:
        results["if"] = {**evaluate_scores(y_test, norm_test_if), "time": t_if}
        results["lof"] = {**evaluate_scores(y_test, norm_test_lof), "time": t_lof}
        results["ecod"] = {**evaluate_scores(y_test, norm_test_ecod), "time": t_ecod}
        results["ensemble_b2"] = {**evaluate_scores(y_test, test_s_b2), "time": (t_if + t_lof) / 2}
        results["ensemble_propuesto"] = {**evaluate_scores(y_test, test_s_ens), "time": (t_if + t_lof + t_ecod) / 3}
    else:
        # Para el set real, calculamos y devolvemos los scores en la escala de probabilidad
        results["real_scores"] = test_s_ens
        results["real_scores_if"] = norm_test_if
        
    return results


def main():
    log.info("==================================================")
    log.info("🔍 DETECCIÓN DE ANOMALÍAS CON ENSEMBLE PYOD")
    log.info("==================================================")
    
    synthetic_dir = Path("data/synthetic_processed")
    results = run_anomaly_experiment(synthetic_dir, seed=42)
    
    log.info("\nResultados Preliminares (Semilla 42) en Dataset Sintético:")
    for method, metrics in results.items():
        log.info("%s: PR-AUC = %.4f | ROC-AUC = %.4f | F1 = %.4f | Precision = %.4f | Recall = %.4f | Tiempo = %.4fs",
                 method.upper(), metrics["pr_auc"], metrics["roc_auc"], metrics["f1"],
                 metrics["precision"], metrics["recall"], metrics["time"])


if __name__ == "__main__":
    main()
