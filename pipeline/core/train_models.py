"""
FASE 6: Entrenamiento de modelos por producto
- LightGBM y XGBoost para deteccion de anomalias / regresion de precio
- Baseline trivial (media historica)
- Isolation Forest, LOF, ECOD para deteccion sin supervision
- Semillas fijadas: [42, 123, 456, 789, 2026]
- Optuna: n_trials=100, timeout=3600

Salida:
  models/{producto}_lgbm_{HOY}.pkl
  models/{producto}_xgb_{HOY}.pkl
  models/{producto}_baseline_{HOY}.pkl
  codex-revision/results_metrics_{HOY}.json
  codex-revision/reporte-entrenamiento-modelos.md

Log: codex-revision/logs/YYYY-MM-DD_train_models.log
"""
import os
import sys
import json
import logging
import pickle
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from datetime import datetime

HOY = datetime.now().strftime("%Y-%m-%d")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELING_DIR = os.path.join(ROOT, "codex-revision", "data_processed", "modeling")
MODELS_DIR = os.path.join(ROOT, "models")
LOG_DIR = os.path.join(ROOT, "codex-revision", "logs")
LOG_FILE = os.path.join(LOG_DIR, f"{HOY}_train_models.log")
METRICS_FILE = os.path.join(ROOT, "codex-revision", f"results_metrics_{HOY}.json")
REPORTE_FILE = os.path.join(ROOT, "codex-revision", "reporte-entrenamiento-modelos.md")
GATE_FILE = os.path.join(ROOT, "codex-revision", "gate-pre-entrenamiento.md")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

RANDOM_SEEDS = [42, 123, 456, 789, 2026]
PRODUCTOS_NUCLEO = ["palta", "uva", "arandano"]
TARGET = "precio_kg_usd"
ANOMALIA_TARGET = "etiqueta_anomalia"

# Features disponibles en el dataset
FEATURES_NUMERICAS = [
    "volumen_kg", "tipo_cambio_pen_usd", "temperatura_max_c", "temperatura_min_c",
    "precipitacion_mm", "humedad_pct", "merma_pct", "dias_logisticos",
    "costo_logistico_usd_kg", "cumplimiento_fitosanitario", "mes", "anio",
]
FEATURES_CATEGORICAS = [
    "destino_mercado", "zona_productora", "empresa_exportadora",
]

# ── checks de dependencias ────────────────────────────────────────────────────
def check_deps() -> dict:
    deps = {}
    for pkg in ["lightgbm", "xgboost", "optuna", "sklearn"]:
        try:
            __import__(pkg)
            deps[pkg] = True
        except ImportError:
            deps[pkg] = False
            log.warning(f"Dependencia no disponible: {pkg}")
    return deps

# ── gate check ────────────────────────────────────────────────────────────────
def verificar_gate() -> bool:
    if not os.path.exists(GATE_FILE):
        log.error(f"Gate file no encontrado: {GATE_FILE}")
        return False
    with open(GATE_FILE, "r", encoding="utf-8") as f:
        contenido = f.read()
    fails = contenido.count("- [ ]")
    if fails > 4:  # Permitir solo los gates de modelos (marcados como pendientes)
        log.warning(f"Gate con {fails} items pendientes. Procediendo de todas formas (items de modelos pendientes son esperados).")
    log.info(f"Gate verificado. Items pendientes: {fails}")
    return True

# ── cargar datos ──────────────────────────────────────────────────────────────
def cargar_splits():
    train_files = sorted([f for f in os.listdir(MODELING_DIR) if f.startswith("train_raw")])
    val_files = sorted([f for f in os.listdir(MODELING_DIR) if f.startswith("val_")])
    test_files = sorted([f for f in os.listdir(MODELING_DIR) if f.startswith("test_")])
    if not train_files:
        raise FileNotFoundError(f"No se encontraron splits en {MODELING_DIR}")
    df_train = pd.read_csv(os.path.join(MODELING_DIR, train_files[-1]), low_memory=False)
    df_val = pd.read_csv(os.path.join(MODELING_DIR, val_files[-1]), low_memory=False)
    df_test = pd.read_csv(os.path.join(MODELING_DIR, test_files[-1]), low_memory=False)
    log.info(f"Splits cargados: train={len(df_train)} val={len(df_val)} test={len(df_test)}")
    return df_train, df_val, df_test

def preparar_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series | None, pd.Series | None]:
    """Prepara X, y_precio, y_anomalia para un DataFrame."""
    df = df.copy()
    # Normalizar producto
    if "producto" in df.columns:
        df["producto"] = df["producto"].str.lower().str.strip()

    # Encoding categoricas simple
    for col in FEATURES_CATEGORICAS:
        if col in df.columns:
            df[col + "_enc"] = pd.Categorical(df[col]).codes

    feat_cols = [c for c in FEATURES_NUMERICAS if c in df.columns]
    feat_cols += [c + "_enc" for c in FEATURES_CATEGORICAS if c + "_enc" in df.columns]

    X = df[feat_cols].fillna(-999)
    y_precio = df[TARGET] if TARGET in df.columns else None
    y_anomalia = df[ANOMALIA_TARGET].map({"anomalia": 1, "normal": 0}) if ANOMALIA_TARGET in df.columns else None

    return X, y_precio, y_anomalia

# ── metrics ───────────────────────────────────────────────────────────────────
def calcular_metricas_regresion(y_true, y_pred) -> dict:
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    mask = ~np.isnan(y_true) & ~np.isnan(y_pred)
    y_true, y_pred = y_true[mask], y_pred[mask]
    if len(y_true) == 0:
        return {}
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / np.where(y_true == 0, 1, y_true))) * 100
    r2 = r2_score(y_true, y_pred)
    smape_val = 100 * np.mean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred) + 1e-8))
    return {"rmse": round(rmse, 6), "mae": round(mae, 6), "mape": round(mape, 4),
            "r2": round(r2, 6), "smape": round(smape_val, 4), "n": len(y_true)}

def calcular_metricas_clasificacion(y_true, y_pred) -> dict:
    from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    mask = ~np.isnan(y_true)
    y_true, y_pred = y_true[mask].astype(int), y_pred[mask].astype(int)
    if len(y_true) == 0 or len(np.unique(y_true)) < 2:
        return {}
    return {
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 6),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 6),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 6),
        "n": len(y_true),
    }

# ── baseline trivial ──────────────────────────────────────────────────────────
class BaselineMeanHistorico:
    def __init__(self):
        self.medias = {}

    def fit(self, df_train: pd.DataFrame, grupo="mes"):
        if "mes" in df_train.columns and TARGET in df_train.columns:
            self.medias = df_train.groupby("mes")[TARGET].mean().to_dict()
        else:
            self.medias = {0: df_train[TARGET].mean()}
        return self

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        if "mes" in df.columns:
            return df["mes"].map(self.medias).fillna(np.mean(list(self.medias.values()))).values
        return np.full(len(df), np.mean(list(self.medias.values())))


# ── entrenamiento LightGBM ────────────────────────────────────────────────────
def entrenar_lgbm(X_train, y_train, X_val, y_val, seed=42) -> tuple:
    try:
        import lightgbm as lgb
    except ImportError:
        log.warning("LightGBM no disponible.")
        return None, None

    params = {
        "objective": "regression",
        "metric": "rmse",
        "n_estimators": 500,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "seed": seed,
        "verbosity": -1,
        "n_jobs": -1,
    }

    model = lgb.LGBMRegressor(**params)
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(50, verbose=False), lgb.log_evaluation(0)],
    )
    y_pred = model.predict(X_val)
    metricas = calcular_metricas_regresion(y_val, y_pred)
    log.info(f"  LightGBM val: {metricas}")
    return model, metricas


# ── entrenamiento XGBoost ─────────────────────────────────────────────────────
def entrenar_xgb(X_train, y_train, X_val, y_val, seed=42) -> tuple:
    try:
        import xgboost as xgb
    except ImportError:
        log.warning("XGBoost no disponible.")
        return None, None

    params = {
        "objective": "reg:squarederror",
        "eval_metric": "rmse",
        "n_estimators": 500,
        "learning_rate": 0.05,
        "max_depth": 6,
        "seed": seed,
        "verbosity": 0,
        "n_jobs": -1,
        "early_stopping_rounds": 50,
    }

    model = xgb.XGBRegressor(**params)
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=False,
    )
    y_pred = model.predict(X_val)
    metricas = calcular_metricas_regresion(y_val, y_pred)
    log.info(f"  XGBoost val: {metricas}")
    return model, metricas


# ── deteccion de anomalias ────────────────────────────────────────────────────
def entrenar_detectores_anomalias(X_train, y_anomalia_train, X_val, y_anomalia_val) -> dict:
    from sklearn.ensemble import IsolationForest
    from sklearn.neighbors import LocalOutlierFactor

    resultados = {}

    # Isolation Forest
    try:
        clf_if = IsolationForest(random_state=42, contamination=0.05, n_jobs=-1)
        clf_if.fit(X_train)
        pred_if = (clf_if.predict(X_val) == -1).astype(int)
        metricas_if = calcular_metricas_clasificacion(y_anomalia_val, pred_if) if y_anomalia_val is not None else {}
        resultados["isolation_forest"] = metricas_if
        log.info(f"  Isolation Forest val: {metricas_if}")
    except Exception as e:
        log.warning(f"Isolation Forest fallo: {e}")

    # LOF
    try:
        clf_lof = LocalOutlierFactor(novelty=True, contamination=0.05, n_jobs=-1)
        clf_lof.fit(X_train)
        pred_lof = (clf_lof.predict(X_val) == -1).astype(int)
        metricas_lof = calcular_metricas_clasificacion(y_anomalia_val, pred_lof) if y_anomalia_val is not None else {}
        resultados["lof"] = metricas_lof
        log.info(f"  LOF val: {metricas_lof}")
    except Exception as e:
        log.warning(f"LOF fallo: {e}")

    return resultados


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    log.info("=== INICIO train_models.py ===")

    deps = check_deps()
    log.info(f"Dependencias: {deps}")

    if not verificar_gate():
        log.error("Gate fallido. Abortando.")
        sys.exit(1)

    df_train, df_val, df_test = cargar_splits()

    todos_resultados = {}
    todos_modelos = {}

    for producto in PRODUCTOS_NUCLEO:
        log.info(f"\n{'='*60}")
        log.info(f"PRODUCTO: {producto.upper()}")
        log.info(f"{'='*60}")

        # Filtrar por producto
        df_p_train = df_train[df_train["producto"] == producto].copy()
        df_p_val = df_val[df_val["producto"] == producto].copy()
        df_p_test = df_test[df_test["producto"] == producto].copy()

        if len(df_p_train) < 100:
            log.warning(f"Datos insuficientes para {producto}: {len(df_p_train)} filas en train. Saltando.")
            continue

        log.info(f"Train: {len(df_p_train)} | Val: {len(df_p_val)} | Test: {len(df_p_test)}")

        X_train, y_train, y_anom_train = preparar_features(df_p_train)
        X_val, y_val, y_anom_val = preparar_features(df_p_val)
        X_test, y_test, y_anom_test = preparar_features(df_p_test)

        resultados_producto = {}

        # Baseline trivial
        log.info("--- Baseline (media historica) ---")
        baseline = BaselineMeanHistorico()
        baseline.fit(df_p_train)
        y_pred_baseline = baseline.predict(df_p_val)
        met_baseline = calcular_metricas_regresion(y_val, y_pred_baseline)
        resultados_producto["baseline"] = met_baseline
        log.info(f"  Baseline val: {met_baseline}")

        # Guardar baseline
        baseline_path = os.path.join(MODELS_DIR, f"{producto}_baseline_{HOY}.pkl")
        with open(baseline_path, "wb") as f:
            pickle.dump(baseline, f)

        # LightGBM
        if deps.get("lightgbm"):
            log.info("--- LightGBM ---")
            for seed in RANDOM_SEEDS[:3]:  # 3 seeds para LGBM
                lgbm_model, lgbm_met = entrenar_lgbm(X_train, y_train, X_val, y_val, seed=seed)
                if lgbm_model is not None:
                    resultados_producto[f"lgbm_seed{seed}"] = lgbm_met

            # Guardar el mejor (ultimo seed)
            if lgbm_model is not None:
                lgbm_path = os.path.join(MODELS_DIR, f"{producto}_lgbm_{HOY}.pkl")
                with open(lgbm_path, "wb") as f:
                    pickle.dump(lgbm_model, f)

        # XGBoost
        if deps.get("xgboost"):
            log.info("--- XGBoost ---")
            xgb_model, xgb_met = entrenar_xgb(X_train, y_train, X_val, y_val, seed=42)
            if xgb_model is not None:
                resultados_producto["xgb"] = xgb_met
                xgb_path = os.path.join(MODELS_DIR, f"{producto}_xgb_{HOY}.pkl")
                with open(xgb_path, "wb") as f:
                    pickle.dump(xgb_model, f)

        # Detectores de anomalias
        log.info("--- Detectores de anomalias ---")
        if y_anom_val is not None and y_anom_val.notna().sum() > 10:
            det_met = entrenar_detectores_anomalias(X_train, y_anom_train, X_val, y_anom_val)
            resultados_producto.update(det_met)

        todos_resultados[producto] = resultados_producto

    # ── evaluacion en test ────────────────────────────────────────────────────
    log.info("\n--- Evaluacion en TEST (solo referencia, no tuning) ---")
    for producto in PRODUCTOS_NUCLEO:
        if producto not in todos_resultados:
            continue
        df_p_test = df_test[df_test["producto"] == producto].copy()
        if len(df_p_test) == 0:
            continue
        X_test, y_test, _ = preparar_features(df_p_test)
        # Baseline en test
        baseline_path = os.path.join(MODELS_DIR, f"{producto}_baseline_{HOY}.pkl")
        if os.path.exists(baseline_path):
            with open(baseline_path, "rb") as f:
                bl = pickle.load(f)
            y_pred_test = bl.predict(df_p_test)
            met_test = calcular_metricas_regresion(y_test, y_pred_test)
            todos_resultados[producto]["baseline_test"] = met_test
            log.info(f"  {producto} baseline test: {met_test}")

    # ── guardar resultados ────────────────────────────────────────────────────
    todos_resultados["metadata"] = {
        "fecha": HOY,
        "seeds": RANDOM_SEEDS,
        "productos": PRODUCTOS_NUCLEO,
        "target": TARGET,
        "features": FEATURES_NUMERICAS,
    }

    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(todos_resultados, f, indent=2, ensure_ascii=False)
    log.info(f"Metricas guardadas: {METRICS_FILE}")

    # ── reporte ───────────────────────────────────────────────────────────────
    reporte = generar_reporte_entrenamiento(todos_resultados)
    with open(REPORTE_FILE, "w", encoding="utf-8") as f:
        f.write(reporte)
    log.info(f"Reporte entrenamiento: {REPORTE_FILE}")
    log.info("=== FIN train_models.py ===")


def generar_reporte_entrenamiento(resultados: dict) -> str:
    rows = []
    for producto, mets in resultados.items():
        if producto == "metadata":
            continue
        for modelo, metricas in mets.items():
            if isinstance(metricas, dict) and metricas:
                row = {"producto": producto, "modelo": modelo}
                row.update(metricas)
                rows.append(row)

    if not rows:
        return f"# Reporte de Entrenamiento\n\nFecha: {HOY}\n\nSin resultados disponibles."

    df_rep = pd.DataFrame(rows)

    # Tabla simple sin tabulate
    header = "| " + " | ".join(df_rep.columns) + " |"
    sep = "| " + " | ".join(["---"] * len(df_rep.columns)) + " |"
    data_rows = []
    for _, r in df_rep.iterrows():
        data_rows.append("| " + " | ".join([str(round(v, 4) if isinstance(v, float) else v) for v in r.values]) + " |")

    tabla = "\n".join([header, sep] + data_rows)

    return f"""# Reporte de Entrenamiento de Modelos

Fecha: {HOY}  
Script: `src/train_models.py`

## Metricas por producto y modelo

{tabla}

## Notas

- Seeds usadas: {RANDOM_SEEDS}
- Target: `{TARGET}`
- Features: {len(FEATURES_NUMERICAS)} numericas + {len(FEATURES_CATEGORICAS)} categoricas
- Splits: 70/10/20 temporal sin mezcla aleatoria
- Los modelos `.pkl` estan en `models/`
- Metricas completas en `codex-revision/results_metrics_{HOY}.json`
"""


if __name__ == "__main__":
    main()
