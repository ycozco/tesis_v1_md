"""
generate_synthetic_dataset.py
=============================
Generador del dataset sintetico agroexportador peruano v1.0.

Tesis UNSA - Yoset Cozco Mauri (2026).
Especificacion: docs/a3-anexo-datasheet.md

Uso:
    python src/generate_synthetic_dataset.py \
        --n 2000 --seed 42 --out data/dataset_agro_sintetico_v1.csv

Estandar: Datasheets for Datasets (Gebru et al., 2021).
Licencia: CC BY 4.0.

Reproducibilidad: la semilla aleatoria principal es 42. Con la misma semilla
y la misma version del codigo, el dataset generado es bit-exact identico.
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Configuracion global del dominio
# ----------------------------------------------------------------------------

PRODUCTOS = ["arandano", "uva", "palta", "cacao", "esparrago"]
PRODUCTO_WEIGHTS = [0.30, 0.25, 0.20, 0.10, 0.15]  # participacion aproximada

ZONAS = ["Ica", "La Libertad", "Piura", "Arequipa", "Lima"]
ZONA_WEIGHTS = [0.30, 0.25, 0.20, 0.15, 0.10]

DESTINOS = ["EEUU", "UE", "Asia", "Otro"]
DESTINO_WEIGHTS = [0.40, 0.35, 0.20, 0.05]

# Parametros por producto (precio medio USD/kg, sigma precio)
PRECIO_BASE = {
    "arandano": (6.5, 1.2),
    "uva": (3.0, 0.7),
    "palta": (2.5, 0.5),
    "cacao": (4.0, 0.8),
    "esparrago": (3.5, 0.6),
}

# Parametros climaticos por zona (Temp_max_media, Temp_max_sigma)
TEMP_BASE = {
    "Ica": (26, 5),
    "La Libertad": (24, 4),
    "Piura": (30, 5),
    "Arequipa": (22, 4),
    "Lima": (23, 4),
}

ANOMALY_RATE = 0.12
ANOMALY_DIST = {
    "precio": 0.30,
    "volumen": 0.25,
    "clima": 0.20,
    "logistica": 0.15,
    "calidad": 0.10,
}

DATE_START = date(2022, 1, 1)
DATE_END = date(2025, 12, 31)
MISSING_RATE = 0.03

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# Estructuras auxiliares
# ----------------------------------------------------------------------------


@dataclass
class GenConfig:
    n_rows: int = 2000
    seed: int = 42
    out_path: Path = Path("data/dataset_agro_sintetico_v1.csv")
    missing_rate: float = MISSING_RATE
    anomaly_rate: float = ANOMALY_RATE


# ----------------------------------------------------------------------------
# Generacion de columnas base
# ----------------------------------------------------------------------------


def _sample_dates(rng: np.random.Generator, n: int) -> pd.Series:
    """Genera fechas uniformes entre DATE_START y DATE_END."""
    delta_days = (DATE_END - DATE_START).days
    offsets = rng.integers(0, delta_days + 1, size=n)
    fechas = [pd.Timestamp(DATE_START) + pd.Timedelta(days=int(o)) for o in offsets]
    return pd.Series(fechas, name="fecha")


def _sample_categorical(
    rng: np.random.Generator, n: int, categories: list[str], weights: list[float], name: str
) -> pd.Series:
    """Muestrea categorias ponderadas."""
    vals = rng.choice(categories, size=n, p=weights)
    return pd.Series(vals, name=name)


def _sample_volumen(rng: np.random.Generator, n: int) -> pd.Series:
    """Volumen kg ~ LogNormal(8, 1.2) truncado a [500, 50000]."""
    raw = rng.lognormal(mean=8.0, sigma=1.2, size=n)
    clipped = np.clip(raw, 500, 50_000)
    return pd.Series(clipped, name="volumen_kg")


def _sample_precio(rng: np.random.Generator, productos: pd.Series) -> pd.Series:
    """Precio USD/kg por producto."""
    vals = np.zeros(len(productos))
    for i, prod in enumerate(productos):
        mu, sigma = PRECIO_BASE[prod]
        vals[i] = rng.normal(loc=mu, scale=sigma)
    return pd.Series(np.clip(vals, 0.5, 12.0), name="precio_kg_usd")


def _sample_clima(
    rng: np.random.Generator, zonas: pd.Series, fechas: pd.Series
) -> pd.DataFrame:
    """Temperatura, precipitacion, humedad por zona y estacion."""
    n = len(zonas)
    temp_max = np.zeros(n)
    temp_min = np.zeros(n)
    precip = np.zeros(n)
    humedad = np.zeros(n)

    for i in range(n):
        zona = zonas.iloc[i]
        fecha = fechas.iloc[i]
        mu_t, sd_t = TEMP_BASE[zona]
        # Modulacion estacional simple (verano +3, invierno -2)
        mes = fecha.month
        estacional = 3 if mes in [12, 1, 2, 3] else (-2 if mes in [6, 7, 8] else 0)
        temp_max[i] = np.clip(rng.normal(mu_t + estacional, sd_t), 15, 38)
        temp_min[i] = np.clip(temp_max[i] - rng.uniform(6, 12), 5, 22)
        precip[i] = np.clip(rng.gamma(shape=0.5, scale=10), 0, 200)
        humedad[i] = np.clip(rng.beta(8, 3) * 100, 40, 95)

    return pd.DataFrame(
        {
            "temperatura_max_c": temp_max,
            "temperatura_min_c": temp_min,
            "precipitacion_mm": precip,
            "humedad_pct": humedad,
        }
    )


def _sample_logistica(rng: np.random.Generator, n: int) -> pd.DataFrame:
    """Dias logisticos, costo logistico y cumplimiento fitosanitario."""
    dias = np.clip(rng.lognormal(mean=2.3, sigma=0.5, size=n).astype(int), 3, 45)
    costo = np.clip(rng.lognormal(mean=-1.5, sigma=0.6, size=n), 0.05, 1.2)
    cumple = rng.binomial(1, 0.92, size=n)
    return pd.DataFrame(
        {
            "dias_logisticos": dias,
            "costo_logistico_usd_kg": costo,
            "cumplimiento_fitosanitario": cumple,
        }
    )


def _sample_merma(rng: np.random.Generator, n: int) -> pd.Series:
    """Merma porcentual ~ Beta(2, 10) escalado a 0-30%."""
    raw = rng.beta(a=2, b=10, size=n) * 30
    return pd.Series(np.clip(raw, 0, 30), name="merma_pct")


def _sample_tipo_cambio(rng: np.random.Generator, fechas: pd.Series) -> pd.Series:
    """Random walk simple del tipo de cambio PEN/USD."""
    n = len(fechas)
    base = 3.7
    walk = np.cumsum(rng.normal(0, 0.01, size=n))
    series = np.clip(base + walk, 3.5, 4.2)
    return pd.Series(series, name="tipo_cambio_pen_usd")


# ----------------------------------------------------------------------------
# Inyeccion de anomalias
# ----------------------------------------------------------------------------


def _inject_anomalies(rng: np.random.Generator, df: pd.DataFrame, anomaly_rate: float) -> pd.DataFrame:
    """
    Inyecta anomalias controladas segun la distribucion ANOMALY_DIST.

    Cada anomalia activa una regla deterministica que modifica el registro
    para garantizar que sea estadisticamente atipica. Se etiqueta y se
    documenta el tipo en la columna tipo_anomalia.
    """
    n = len(df)
    n_anom = int(round(anomaly_rate * n))
    idx_anom = rng.choice(n, size=n_anom, replace=False)

    df["etiqueta_anomalia"] = 0
    df["tipo_anomalia"] = "none"
    df["regla_inyeccion"] = ""

    # Reparto por tipo
    types = list(ANOMALY_DIST.keys())
    weights = np.array([ANOMALY_DIST[t] for t in types])
    weights = weights / weights.sum()
    type_assignments = rng.choice(types, size=n_anom, p=weights)

    for i, idx in enumerate(idx_anom):
        tipo = type_assignments[i]
        df.loc[idx, "etiqueta_anomalia"] = 1
        df.loc[idx, "tipo_anomalia"] = tipo

        if tipo == "precio":
            # +/- 3 sigma del precio base del producto
            prod = df.loc[idx, "producto"]
            mu, sd = PRECIO_BASE[prod]
            direction = rng.choice([-1, 1])
            df.loc[idx, "precio_kg_usd"] = np.clip(mu + direction * 4 * sd, 0.5, 12.0)
            df.loc[idx, "regla_inyeccion"] = f"precio = {mu + direction * 4 * sd:.2f}"

        elif tipo == "volumen":
            df.loc[idx, "volumen_kg"] = np.clip(rng.uniform(45_000, 50_000), 500, 50_000)
            df.loc[idx, "regla_inyeccion"] = "volumen > P99"

        elif tipo == "clima":
            df.loc[idx, "temperatura_max_c"] = rng.uniform(36, 38)
            df.loc[idx, "precipitacion_mm"] = 0.0
            df.loc[idx, "regla_inyeccion"] = "temp>36 AND precip=0"

        elif tipo == "logistica":
            df.loc[idx, "dias_logisticos"] = int(rng.uniform(35, 45))
            df.loc[idx, "cumplimiento_fitosanitario"] = 1
            df.loc[idx, "regla_inyeccion"] = "dias>35 AND cumple=1"

        elif tipo == "calidad":
            df.loc[idx, "merma_pct"] = rng.uniform(25, 30)
            df.loc[idx, "regla_inyeccion"] = "merma>25%"

    return df


# ----------------------------------------------------------------------------
# Faltantes
# ----------------------------------------------------------------------------


def _inject_missing(rng: np.random.Generator, df: pd.DataFrame, rate: float) -> pd.DataFrame:
    """Introduce valores faltantes en columnas seleccionadas."""
    cols = ["humedad_pct", "dias_logisticos", "costo_logistico_usd_kg"]
    n = len(df)
    n_missing = int(round(rate * n))
    for col in cols:
        idx = rng.choice(n, size=n_missing, replace=False)
        df.loc[idx, col] = np.nan
    return df


# ----------------------------------------------------------------------------
# Pipeline principal
# ----------------------------------------------------------------------------


def generate(config: GenConfig) -> pd.DataFrame:
    log.info("Generando dataset sintetico (n=%d, seed=%d)", config.n_rows, config.seed)
    rng = np.random.default_rng(config.seed)
    n = config.n_rows

    fechas = _sample_dates(rng, n)
    productos = _sample_categorical(rng, n, PRODUCTOS, PRODUCTO_WEIGHTS, "producto")
    zonas = _sample_categorical(rng, n, ZONAS, ZONA_WEIGHTS, "zona")
    destinos = _sample_categorical(rng, n, DESTINOS, DESTINO_WEIGHTS, "destino_mercado")
    volumen = _sample_volumen(rng, n)
    precios = _sample_precio(rng, productos)
    clima = _sample_clima(rng, zonas, fechas)
    log_df = _sample_logistica(rng, n)
    merma = _sample_merma(rng, n)
    tc = _sample_tipo_cambio(rng, fechas)

    df = pd.concat(
        [
            pd.Series(np.arange(1, n + 1), name="id"),
            fechas,
            productos,
            zonas,
            volumen,
            precios,
            clima,
            destinos,
            log_df,
            merma,
            tc,
        ],
        axis=1,
    )

    # Ordenar cronologicamente
    df = df.sort_values("fecha").reset_index(drop=True)
    df["id"] = np.arange(1, len(df) + 1)

    # Inyectar anomalias y faltantes
    df = _inject_anomalies(rng, df, config.anomaly_rate)
    df = _inject_missing(rng, df, config.missing_rate)

    # Metadata
    df.attrs["version"] = "1.0"
    df.attrs["seed"] = config.seed
    df.attrs["generated_at"] = datetime.now().isoformat(timespec="seconds")

    log.info("Generadas %d filas | %d anomalias (%.1f%%)",
             len(df), df["etiqueta_anomalia"].sum(),
             df["etiqueta_anomalia"].mean() * 100)

    return df


def save(df: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8")
    log.info("Dataset escrito en %s (%d filas, %d columnas)", out_path, len(df), len(df.columns))


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def parse_args() -> GenConfig:
    parser = argparse.ArgumentParser(description="Genera el dataset sintetico agroexportador.")
    parser.add_argument("--n", type=int, default=2000, help="Numero de filas")
    parser.add_argument("--seed", type=int, default=42, help="Semilla aleatoria")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/dataset_agro_sintetico_v1.csv"),
        help="Ruta de salida CSV",
    )
    parser.add_argument(
        "--anomaly-rate", type=float, default=ANOMALY_RATE, help="Proporcion de anomalias"
    )
    parser.add_argument(
        "--missing-rate", type=float, default=MISSING_RATE, help="Proporcion de valores faltantes"
    )
    args = parser.parse_args()
    return GenConfig(
        n_rows=args.n,
        seed=args.seed,
        out_path=args.out,
        anomaly_rate=args.anomaly_rate,
        missing_rate=args.missing_rate,
    )


def main() -> None:
    config = parse_args()
    df = generate(config)
    save(df, config.out_path)


if __name__ == "__main__":
    main()
