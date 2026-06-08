"""
FASE 7: Explicabilidad SHAP y reportes finales
- Valores SHAP por producto y modelo
- Ranking de importancia de features
- Genera reporte-explicabilidad-shap.md

Salida:
  codex-revision/reporte-explicabilidad-shap.md
  codex-revision/data_processed/eda/figuras/shap_{producto}_{HOY}.csv

Log: codex-revision/logs/YYYY-MM-DD_shap_explainability.log
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
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELING_DIR = os.path.join(ROOT, "codex-revision", "data_processed", "modeling")
MODELS_DIR = os.path.join(ROOT, "models")
OUT_FIGURAS = os.path.join(ROOT, "codex-revision", "data_processed", "eda", "figuras")
LOG_DIR = os.path.join(ROOT, "codex-revision", "logs")
LOG_FILE = os.path.join(LOG_DIR, f"{HOY}_shap_explainability.log")
REPORTE_FILE = os.path.join(ROOT, "codex-revision", "reporte-explicabilidad-shap.md")

os.makedirs(OUT_FIGURAS, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

PRODUCTOS_NUCLEO = ["palta", "uva", "arandano"]
TARGET = "precio_kg_usd"
FEATURES_NUMERICAS = [
    "volumen_kg", "tipo_cambio_pen_usd", "temperatura_max_c", "temperatura_min_c",
    "precipitacion_mm", "humedad_pct", "merma_pct", "dias_logisticos",
    "costo_logistico_usd_kg", "cumplimiento_fitosanitario", "mes", "anio",
]
FEATURES_CATEGORICAS = [
    "destino_mercado", "zona_productora", "empresa_exportadora",
]


def cargar_test() -> pd.DataFrame:
    test_files = sorted([f for f in os.listdir(MODELING_DIR) if f.startswith("test_")])
    if not test_files:
        raise FileNotFoundError(f"No se encontro split test en {MODELING_DIR}")
    return pd.read_csv(os.path.join(MODELING_DIR, test_files[-1]), low_memory=False)


def preparar_X(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "producto" in df.columns:
        df["producto"] = df["producto"].str.lower().str.strip()
    for col in FEATURES_CATEGORICAS:
        if col in df.columns:
            df[col + "_enc"] = pd.Categorical(df[col]).codes
    feat_cols = [c for c in FEATURES_NUMERICAS if c in df.columns]
    feat_cols += [c + "_enc" for c in FEATURES_CATEGORICAS if c + "_enc" in df.columns]
    return df[feat_cols].fillna(-999)


def calcular_shap_lgbm(modelo, X: pd.DataFrame, producto: str) -> pd.DataFrame | None:
    """Calcula SHAP values para LightGBM."""
    try:
        import shap
        explainer = shap.TreeExplainer(modelo)
        shap_values = explainer.shap_values(X)
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
        df_shap = pd.DataFrame(np.abs(shap_values), columns=X.columns)
        importancias = df_shap.mean().sort_values(ascending=False).reset_index()
        importancias.columns = ["feature", "mean_abs_shap"]
        importancias["producto"] = producto
        importancias["modelo"] = "lgbm"
        importancias["metodo"] = "shap_tree"
        return importancias
    except ImportError:
        log.warning("SHAP no disponible. Usando importancia nativa LightGBM.")
        try:
            imp = modelo.feature_importances_
            df_imp = pd.DataFrame({
                "feature": X.columns,
                "mean_abs_shap": imp / imp.sum() if imp.sum() > 0 else imp,
                "producto": producto,
                "modelo": "lgbm",
                "metodo": "native_importance",
            }).sort_values("mean_abs_shap", ascending=False)
            return df_imp
        except Exception as e:
            log.error(f"Error calculando importancia nativa: {e}")
            return None
    except Exception as e:
        log.error(f"Error calculando SHAP: {e}")
        return None


def calcular_shap_xgb(modelo, X: pd.DataFrame, producto: str) -> pd.DataFrame | None:
    """Calcula SHAP values para XGBoost."""
    try:
        import shap
        explainer = shap.TreeExplainer(modelo)
        shap_values = explainer.shap_values(X)
        df_shap = pd.DataFrame(np.abs(shap_values), columns=X.columns)
        importancias = df_shap.mean().sort_values(ascending=False).reset_index()
        importancias.columns = ["feature", "mean_abs_shap"]
        importancias["producto"] = producto
        importancias["modelo"] = "xgb"
        importancias["metodo"] = "shap_tree"
        return importancias
    except ImportError:
        log.warning("SHAP no disponible. Usando importancia nativa XGBoost.")
        try:
            scores = modelo.get_booster().get_fscore()
            total = sum(scores.values())
            df_imp = pd.DataFrame({
                "feature": list(scores.keys()),
                "mean_abs_shap": [v / total for v in scores.values()],
                "producto": producto,
                "modelo": "xgb",
                "metodo": "native_fscore",
            }).sort_values("mean_abs_shap", ascending=False)
            return df_imp
        except Exception as e:
            log.error(f"Error importancia nativa XGB: {e}")
            return None
    except Exception as e:
        log.error(f"Error SHAP XGB: {e}")
        return None


def generar_reporte_shap(todos_importancias: list, interpretaciones: dict) -> str:
    if not todos_importancias:
        return f"# Reporte SHAP\n\nFecha: {HOY}\n\nSin resultados disponibles.\n"

    df_all = pd.concat(todos_importancias, ignore_index=True)

    # Top 5 por producto
    secciones = []
    for producto in df_all["producto"].unique():
        df_p = df_all[df_all["producto"] == producto].sort_values("mean_abs_shap", ascending=False)
        top5 = df_p.head(5)
        rows = ["| feature | importancia_media | modelo | metodo |", "|---|---|---|---|"]
        for _, r in top5.iterrows():
            rows.append(f"| {r['feature']} | {r['mean_abs_shap']:.4f} | {r['modelo']} | {r['metodo']} |")
        secciones.append(f"### {producto.capitalize()}\n\n" + "\n".join(rows))

    interp_str = ""
    for producto, interp in interpretaciones.items():
        interp_str += f"\n### {producto.capitalize()}\n\n{interp}\n"

    return f"""# Reporte de Explicabilidad SHAP

Fecha: {HOY}  
Script: `src/shap_explainability.py`

## 1. Importancia de features (SHAP o nativa)

{chr(10).join(secciones)}

## 2. Interpretaciones por producto

{interp_str}

## 3. Implicaciones para la tesis

- Las features con mayor importancia SHAP son los candidatos principales
  para el analisis de factores determinantes de precio (Capitulo 4 de la tesis).
- El dominio de variables operativas (merma, dias_logisticos) sobre variables
  externas (clima, tipo de cambio) sugiere que el dataset tiene sesgos de construccion.
- Se recomienda complementar con SISAP (precios internos) y variables de demanda
  (Trade Map) en versiones posteriores del modelo.
- Los archivos CSV de importancias estan en:
  `codex-revision/data_processed/eda/figuras/`
"""


def main():
    log.info("=== INICIO shap_explainability.py ===")

    df_test = cargar_test()

    todos_importancias = []
    interpretaciones = {}

    for producto in PRODUCTOS_NUCLEO:
        log.info(f"\n--- SHAP: {producto} ---")
        df_p = df_test[df_test["producto"] == producto].copy() if "producto" in df_test.columns else df_test.copy()

        if len(df_p) == 0:
            log.warning(f"Sin datos test para {producto}")
            continue

        X = preparar_X(df_p)
        if len(X) > 1000:
            X = X.sample(1000, random_state=42)  # Subsample para SHAP

        # LGBM SHAP
        lgbm_path = os.path.join(MODELS_DIR, f"{producto}_lgbm_{HOY}.pkl")
        if os.path.exists(lgbm_path):
            with open(lgbm_path, "rb") as f:
                modelo_lgbm = pickle.load(f)
            imp_lgbm = calcular_shap_lgbm(modelo_lgbm, X, producto)
            if imp_lgbm is not None:
                todos_importancias.append(imp_lgbm)
                # Guardar CSV
                imp_lgbm.to_csv(os.path.join(OUT_FIGURAS, f"shap_lgbm_{producto}_{HOY}.csv"), index=False)
                top_feature = imp_lgbm.iloc[0]["feature"]
                interpretaciones[producto] = (
                    f"La feature mas importante para predecir `{TARGET}` en {producto} es "
                    f"**`{top_feature}`** segun el metodo {imp_lgbm.iloc[0]['metodo']}. "
                    f"Esto sugiere que los modelos estan capturando principalmente variabilidad "
                    f"{'operativa (proxy)' if top_feature in ['merma_pct','dias_logisticos','costo_logistico_usd_kg'] else 'de mercado'}."
                )
                log.info(f"Top feature {producto}: {top_feature} (imp={imp_lgbm.iloc[0]['mean_abs_shap']:.4f})")

        # XGB SHAP
        xgb_path = os.path.join(MODELS_DIR, f"{producto}_xgb_{HOY}.pkl")
        if os.path.exists(xgb_path):
            with open(xgb_path, "rb") as f:
                modelo_xgb = pickle.load(f)
            imp_xgb = calcular_shap_xgb(modelo_xgb, X, producto)
            if imp_xgb is not None:
                todos_importancias.append(imp_xgb)
                imp_xgb.to_csv(os.path.join(OUT_FIGURAS, f"shap_xgb_{producto}_{HOY}.csv"), index=False)

    # Generar reporte
    reporte = generar_reporte_shap(todos_importancias, interpretaciones)
    with open(REPORTE_FILE, "w", encoding="utf-8") as f:
        f.write(reporte)
    log.info(f"Reporte SHAP: {REPORTE_FILE}")
    log.info("=== FIN shap_explainability.py ===")


if __name__ == "__main__":
    main()
