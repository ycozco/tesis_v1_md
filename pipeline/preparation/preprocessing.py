"""
preprocess_data.py
==================
Pipeline de preprocesamiento de datos para la tesis.
Aplica:
1. Ingeniería de características (Lags temporales, Codificación Cíclica de Fechas).
2. Particionado temporal estricto (Train: 2022-2024, Test: 2025).
3. Imputación por KNN (KNNImputer) ajustada únicamente en Train.
4. Escalamiento por RobustScaler ajustado únicamente en Train.
5. Balanceo de clases por SMOTE (Synthetic Minority Over-sampling Technique) en Train.
6. Exportación de datasets limpios y procesados en la carpeta `data/`.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

from __future__ import annotations

import logging
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import RobustScaler
from imblearn.over_sampling import SMOTE

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Configuración de rutas
DATA_DIR = Path("data")
RAW_DATA_PATH = DATA_DIR / "dataset_real_v1.csv"
TRAIN_RAW_OUT = DATA_DIR / "dataset_processed_train_raw.csv"
TRAIN_BAL_OUT = DATA_DIR / "dataset_processed_train_balanced.csv"
TEST_OUT = DATA_DIR / "dataset_processed_test.csv"


def load_data(path: Path) -> pd.DataFrame:
    """Carga el dataset sintético crudo."""
    if not path.exists():
        raise FileNotFoundError(
            f"El archivo {path} no existe. Por favor, genere el dataset sintético primero."
        )
    log.info("Cargando dataset crudo desde %s", path)
    df = pd.read_csv(path)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica ingeniería de características."""
    log.info("Aplicando ingeniería de características...")
    
    # 1. Ordenar cronológicamente para calcular lags
    df = df.sort_values("fecha").reset_index(drop=True)
    
    # 2. Codificación Cíclica de Fechas (Seno/Coseno)
    df["mes"] = df["fecha"].dt.month
    df["mes_sin"] = np.sin(2 * np.pi * df["mes"] / 12)
    df["mes_cos"] = np.cos(2 * np.pi * df["mes"] / 12)
    
    df["dia_ano"] = df["fecha"].dt.dayofyear
    df["dia_ano_sin"] = np.sin(2 * np.pi * df["dia_ano"] / 365.25)
    df["dia_ano_cos"] = np.cos(2 * np.pi * df["dia_ano"] / 365.25)
    
    # Eliminar auxiliares
    df = df.drop(columns=["mes", "dia_ano"])
    
    # 3. Lags Temporales (t-1, t-7, t-30) agrupados por producto y zona
    log.info("Generando variables de rezago temporal (Lags)...")
    lag_cols = []
    for lag in [1, 7, 30]:
        p_lag_col = f"precio_lag_{lag}"
        v_lag_col = f"volumen_lag_{lag}"
        lag_cols.extend([p_lag_col, v_lag_col])
        
        df[p_lag_col] = df.groupby(["producto", "zona"])["precio_kg_usd"].shift(lag)
        df[v_lag_col] = df.groupby(["producto", "zona"])["volumen_kg"].shift(lag)
        
    # Imputar los primeros lags vacíos mediante ffill + bfill por grupos
    df[lag_cols] = df.groupby(["producto", "zona"])[lag_cols].ffill().bfill()
    # Si quedan nulos globales residuales, llenar con la mediana global
    for col in lag_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
            
    return df


def split_and_encode(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    """Aplica particionado temporal y One-Hot Encoding."""
    log.info("Aplicando particionamiento temporal y One-Hot Encoding...")
    
    # One-Hot Encoding de categorizaciones fijas
    categorical_cols = ["producto", "zona", "destino_mercado"]
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False, dtype=int)
    
    # Identificar columnas codificadas para el entrenamiento
    all_cols = list(df_encoded.columns)
    exclude_cols = ["id", "fecha", "tipo_anomalia", "regla_inyeccion", "etiqueta_anomalia", "empresa_exportadora", "partida_arancelaria"]
    feature_cols = [c for c in all_cols if c not in exclude_cols]
    
    # Particionado temporal estricto (Train: 2022-2024, Test: 2025)
    train_mask = df_encoded["fecha"] < "2026-01-01"
    test_mask = df_encoded["fecha"] >= "2026-01-01"
    
    df_train = df_encoded[train_mask].copy()
    df_test = df_encoded[test_mask].copy()
    
    log.info("Registros en Train: %d (2022-2024)", len(df_train))
    log.info("Registros en Test:  %d (2025)", len(df_test))
    
    return df_train, df_test, feature_cols


def run_pipeline(input_path: Path, output_dir: Path):
    """Ejecuta el pipeline completo de tratamiento de datos."""
    output_dir.mkdir(parents=True, exist_ok=True)
    df = load_data(input_path)
    df = add_features(df)
    df_train, df_test, feature_cols = split_and_encode(df)
    
    # Columnas numéricas que requieren imputación y escalamiento
    num_cols = [
        "volumen_kg", "precio_kg_usd", "temperatura_max_c", "temperatura_min_c",
        "precipitacion_mm", "humedad_pct", "dias_logisticos", "costo_logistico_usd_kg",
        "cumplimiento_fitosanitario", "merma_pct", "tipo_cambio_pen_usd",
        "precio_lag_1", "volumen_lag_1", "precio_lag_7", "volumen_lag_7",
        "precio_lag_30", "volumen_lag_30"
    ]
    
    # 1. Imputación mediante KNNImputer (Fiteado en Train, transformado en Train y Test)
    log.info("Ajustando e imputando con KNNImputer (n_neighbors=5)...")
    imputer = KNNImputer(n_neighbors=5)
    
    # Ajustamos el imputador en el set de entrenamiento
    df_train[num_cols] = imputer.fit_transform(df_train[num_cols])
    # Aplicamos la transformación al set de pruebas sin fitear de nuevo (evitar data leakage)
    df_test[num_cols] = imputer.transform(df_test[num_cols])
    
    # 2. Escalamiento mediante RobustScaler (Mediana e IQR)
    log.info("Escalando variables continuas mediante RobustScaler...")
    scaler = RobustScaler()
    
    df_train[num_cols] = scaler.fit_transform(df_train[num_cols])
    df_test[num_cols] = scaler.transform(df_test[num_cols])
    
    # Separar X (features) e y (target) para entrenamiento y prueba
    X_train = df_train[feature_cols]
    y_train = df_train["etiqueta_anomalia"]
    
    X_test = df_test[feature_cols]
    y_test = df_test["etiqueta_anomalia"]
    
    # Exportar Train Raw (Preprocesado pero sin balancear)
    df_train_raw_out = pd.concat([X_train, y_train], axis=1)
    train_raw_path = output_dir / "dataset_processed_train_raw.csv"
    df_train_raw_out.to_csv(train_raw_path, index=False)
    log.info("Exportado Train Raw en %s (%d registros)", train_raw_path, len(df_train_raw_out))
    
    # Exportar Test (Permanece desbalanceado para métricas de evaluación realistas)
    df_test_out = pd.concat([X_test, y_test], axis=1)
    test_path = output_dir / "dataset_processed_test.csv"
    df_test_out.to_csv(test_path, index=False)
    log.info("Exportado Test en %s (%d registros, %.2f%% anomalías)", 
             test_path, len(df_test_out), df_test_out["etiqueta_anomalia"].mean() * 100)
             
    # 3. Sobremuestreo de anomalías mediante SMOTE
    if y_train.nunique() > 1:
        log.info("Aplicando sobremuestreo SMOTE en el conjunto de entrenamiento...")
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    else:
        log.warning("Solo se encontró una clase en y_train (datos reales sin etiquetar). Omitiendo SMOTE.")
        X_train_res, y_train_res = X_train, y_train
    
    # Exportar Train Balanced
    df_train_bal_out = pd.concat([X_train_res, y_train_res], axis=1)
    train_bal_path = output_dir / "dataset_processed_train_balanced.csv"
    df_train_bal_out.to_csv(train_bal_path, index=False)
    log.info("Exportado Train Balanced (SMOTE) en %s (%d registros, %.2f%% anomalías)", 
             train_bal_path, len(df_train_bal_out), df_train_bal_out["etiqueta_anomalia"].mean() * 100)
             
    log.info("¡Pipeline de preprocesamiento finalizado con éxito para %s!", input_path.name)


if __name__ == "__main__":
    # 1. Procesar dataset sintético global
    run_pipeline(
        input_path=DATA_DIR / "dataset_agro_sintetico_v1.csv",
        output_dir=DATA_DIR / "synthetic_processed"
    )
    # 2. Procesar dataset real global
    run_pipeline(
        input_path=DATA_DIR / "dataset_real_v1.csv",
        output_dir=DATA_DIR / "real_processed"
    )
    # 3. Procesar segmentos reales individuales por cada cultivo principal
    for crop in ["palta", "uva", "arandano"]:
        crop_raw = DATA_DIR / "real_processed" / crop / f"dataset_{crop}_raw.csv"
        if crop_raw.exists():
            log.info("Iniciando preprocesamiento del segmento: %s", crop.upper())
            run_pipeline(
                input_path=crop_raw,
                output_dir=DATA_DIR / "real_processed" / crop
            )


