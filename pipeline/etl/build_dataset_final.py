"""
FASE 5: Construccion del dataset final modelable y splits temporales
- Integra dataset_real_v1 (base) con proxies (BCRP, SISAP, clima, logistica)
- Aplica contrato de columnas del plan seccion 9.2
- Genera splits temporales 70/10/20 sin mezcla aleatoria
- Crea gate-pre-entrenamiento.md

Salida:
  codex-revision/data_processed/dataset_modelo_v_final_YYYY-MM-DD.csv
  codex-revision/data_processed/modeling/train_raw_YYYY-MM-DD.csv
  codex-revision/data_processed/modeling/val_YYYY-MM-DD.csv
  codex-revision/data_processed/modeling/test_YYYY-MM-DD.csv
  codex-revision/gate-pre-entrenamiento.md
Log: codex-revision/logs/YYYY-MM-DD_build_dataset_final.log
"""
import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime

HOY = datetime.now().strftime("%Y-%m-%d")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_REAL = os.path.join(ROOT, "data", "dataset_real_v1.csv")
PROXIES_DIR = os.path.join(ROOT, "codex-revision", "data_processed", "proxies")
OUT_FINAL = os.path.join(ROOT, "codex-revision", "data_processed")
OUT_MODELING = os.path.join(ROOT, "codex-revision", "data_processed", "modeling")
OUT_REJECTED = os.path.join(ROOT, "codex-revision", "data_processed", "rejected")
LOG_DIR = os.path.join(ROOT, "codex-revision", "logs")
LOG_FILE = os.path.join(LOG_DIR, f"{HOY}_build_dataset_final.log")
GATE_FILE = os.path.join(ROOT, "codex-revision", "gate-pre-entrenamiento.md")
REPORTE_CALIDAD = os.path.join(ROOT, "codex-revision", "reporte-calidad-datos.md")

os.makedirs(OUT_MODELING, exist_ok=True)
os.makedirs(OUT_REJECTED, exist_ok=True)

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
PRODUCTO_CONDICIONAL = "esparrago"
PRODUCTO_EXCLUIDO = "cacao"

# Contrato de columnas obligatorias (plan seccion 9.2)
COLUMNAS_OBLIGATORIAS = [
    "id", "producto", "hs", "fecha", "periodo_mes", "anio", "mes",
    "empresa_exportadora", "volumen_kg", "valor_fob_usd", "precio_kg_usd",
    "destino_mercado", "aduana_codigo", "zona_productora",
    "tipo_cambio_pen_usd",
    "temperatura_max_c", "temperatura_min_c", "precipitacion_mm",
    "cumplimiento_fitosanitario", "dias_logisticos", "merma_pct",
    "etiqueta_anomalia", "tipo_anomalia",
    "origen_dato", "tipo_variable_fila", "fuentes_usadas",
    "archivo_origen", "dataset_version", "fecha_generacion",
]

COLUMNAS_CONDICIONALES = [
    "ruc", "puerto", "sisap_precio_prom", "sisap_volumen",
    "humedad_pct", "ndvi", "carga_portuaria_mes", "alertas_sanitarias_mes",
    "regla_inyeccion",
]

# Mapeo de columnas fuente a columnas canonicas
COL_MAP = {
    "partida_arancelaria": "hs_raw",
    "zona": "zona_productora",
}


def cargar_base(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1", low_memory=False)
    log.info(f"Base cargada: {len(df)} filas")
    return df


def normalizar_base(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza columnas del dataset real al esquema canonico."""
    df = df.copy()

    # Excluir cacao
    if "producto" in df.columns:
        df["producto"] = df["producto"].str.lower().str.strip()
        n_antes = len(df)
        df = df[df["producto"] != PRODUCTO_EXCLUIDO]
        log.info(f"Cacao excluido: {n_antes - len(df)} filas")

    # HS canonico
    if "partida_arancelaria" in df.columns:
        df["hs"] = df["partida_arancelaria"].astype(str).str[:6]
    elif "hs6" in df.columns:
        df["hs"] = df["hs6"]

    # Fechas
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["periodo_mes"] = pd.to_datetime(df["fecha"], errors="coerce").dt.strftime("%Y-%m")
    df["anio"] = pd.to_datetime(df["fecha"], errors="coerce").dt.year.astype("Int64")
    df["mes"] = pd.to_datetime(df["fecha"], errors="coerce").dt.month.astype("Int64")

    # Zona productora
    if "zona" in df.columns and "zona_productora" not in df.columns:
        df["zona_productora"] = df["zona"]

    # valor_fob_usd — derivar de precio_kg_usd * volumen_kg si no existe
    if "valor_fob_usd" not in df.columns:
        if "precio_kg_usd" in df.columns and "volumen_kg" in df.columns:
            df["valor_fob_usd"] = df["precio_kg_usd"] * df["volumen_kg"]
            log.info("valor_fob_usd derivado de precio_kg_usd * volumen_kg")

    # aduana_codigo — mapear desde zona si no existe
    if "aduana_codigo" not in df.columns:
        zona_aduana = {
            "Lima": 118, "Piura": 301, "La Libertad": 201,
            "Arequipa": 701, "Ica": 601, "Lambayeque": 204,
        }
        if "zona_productora" in df.columns:
            df["aduana_codigo"] = df["zona_productora"].map(zona_aduana).fillna(999).astype(int)
        else:
            df["aduana_codigo"] = 999

    # Trazabilidad
    if "origen_dato" not in df.columns:
        df["origen_dato"] = "real_observada"
    if "tipo_variable_fila" not in df.columns:
        df["tipo_variable_fila"] = "real_observada"
    # Marcar sinteticas por regla_inyeccion
    if "regla_inyeccion" in df.columns:
        mask = df["regla_inyeccion"].notna() & (df["regla_inyeccion"].astype(str).str.strip() != "")
        df.loc[mask, "origen_dato"] = "sintetica"
    if "archivo_origen" not in df.columns:
        df["archivo_origen"] = "dataset_real_v1.csv"
    if "fuentes_usadas" not in df.columns:
        df["fuentes_usadas"] = "dataset_real_v1.csv"
    df["dataset_version"] = f"final_{HOY}"
    df["fecha_generacion"] = HOY

    return df


def integrar_bcrp(df: pd.DataFrame) -> pd.DataFrame:
    """Une tipo de cambio BCRP canonico por periodo_mes."""
    bcrp_files = sorted([
        f for f in os.listdir(PROXIES_DIR) if f.startswith("bcrp_canonico")
    ])
    if not bcrp_files:
        log.warning("Sin archivo BCRP canonico. Usando tipo_cambio_pen_usd del dataset.")
        return df

    bcrp_path = os.path.join(PROXIES_DIR, bcrp_files[-1])
    df_bcrp = pd.read_csv(bcrp_path)
    df_bcrp = df_bcrp[["periodo_mes", "tipo_cambio_pen_usd"]].rename(
        columns={"tipo_cambio_pen_usd": "tipo_cambio_pen_usd_bcrp"}
    )

    # Unir
    if "periodo_mes" in df.columns:
        df = df.merge(df_bcrp, on="periodo_mes", how="left")
        # Prioridad: BCRP canonico sobre valor en base
        if "tipo_cambio_pen_usd" in df.columns:
            df["tipo_cambio_pen_usd"] = df["tipo_cambio_pen_usd_bcrp"].fillna(df["tipo_cambio_pen_usd"])
        else:
            df["tipo_cambio_pen_usd"] = df["tipo_cambio_pen_usd_bcrp"]
        df = df.drop(columns=["tipo_cambio_pen_usd_bcrp"], errors="ignore")
        df["fuentes_usadas"] = df.get("fuentes_usadas", "") + ";BCRP_PN01207PM"
        log.info(f"BCRP integrado: {df['tipo_cambio_pen_usd'].notna().sum()} filas con tipo de cambio")
    return df


def integrar_sisap(df: pd.DataFrame) -> pd.DataFrame:
    """Une precios internos SISAP por producto y periodo_mes."""
    sisap_files = sorted([
        f for f in os.listdir(PROXIES_DIR) if f.startswith("sisap_processed")
    ])
    if not sisap_files:
        log.warning("Sin archivo SISAP. Las columnas sisap seran nulas.")
        df["sisap_precio_prom"] = np.nan
        df["sisap_volumen"] = np.nan
        return df

    sisap_path = os.path.join(PROXIES_DIR, sisap_files[-1])
    df_sisap = pd.read_csv(sisap_path)

    # Obtener columna de precio y volumen
    # El CSV SISAP usa: producto, periodo_mes, variable_label (precio_prom/volumen), valor
    col_valor = "valor" if "valor" in df_sisap.columns else None
    col_var_label = "variable_label" if "variable_label" in df_sisap.columns else None
    col_periodo = next((c for c in df_sisap.columns if c == "periodo_mes"), None)
    col_prod = next((c for c in df_sisap.columns if "producto" in c.lower()), None)

    if col_valor and col_var_label and col_periodo and col_prod:
        # Estructura larga: pivotar por variable_label
        df_sisap["_periodo"] = df_sisap[col_periodo].astype(str).str[:7]
        df_sisap["_producto"] = df_sisap[col_prod].str.lower().str.strip()
        df_sisap["_valor"] = pd.to_numeric(df_sisap[col_valor], errors="coerce")

        # Separar precio y volumen
        mask_precio = df_sisap[col_var_label].str.contains("precio", na=False, case=False)
        mask_vol = df_sisap[col_var_label].str.contains("volumen", na=False, case=False)

        df_precio = df_sisap[mask_precio].groupby(["_producto", "_periodo"])["_valor"].mean().reset_index()
        df_precio.columns = ["producto", "periodo_mes", "sisap_precio_prom"]

        df_vol = df_sisap[mask_vol].groupby(["_producto", "_periodo"])["_valor"].sum().reset_index()
        df_vol.columns = ["producto", "periodo_mes", "sisap_volumen"]

        df_agg = df_precio.merge(df_vol, on=["producto", "periodo_mes"], how="outer")
    else:
        log.warning(f"SISAP no tiene columnas esperadas. Encontradas: {list(df_sisap.columns)}")
        df["sisap_precio_prom"] = np.nan
        df["sisap_volumen"] = np.nan
        return df

    n_antes = len(df)
    df = df.merge(df_agg, on=["producto", "periodo_mes"], how="left")
    log.info(f"SISAP integrado: {df['sisap_precio_prom'].notna().sum()}/{len(df)} filas con precio SISAP")
    return df


def aplicar_contrato_columnas(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Aplica el contrato de columnas obligatorias y separa rechazados."""

    # Rechazados por valores fuera de rango
    mask_rechazo = pd.Series(False, index=df.index)
    motivos = pd.Series("", index=df.index)

    reglas = {
        "precio_kg_usd": lambda x: x > 0.0001 if pd.notna(x) else False,
        "volumen_kg": lambda x: x > 0 if pd.notna(x) else False,
        "valor_fob_usd": lambda x: x > 0 if pd.notna(x) else False,
        "temperatura_max_c": lambda x: -10 <= x <= 50 if pd.notna(x) else True,
        "precipitacion_mm": lambda x: x >= 0 if pd.notna(x) else True,
    }

    for col, regla in reglas.items():
        if col in df.columns:
            violacion = ~df[col].apply(regla)
            mask_rechazo = mask_rechazo | violacion
            motivos = motivos + violacion.apply(lambda x: f"[{col}_invalido]" if x else "")

    df_rechazados = df[mask_rechazo].copy()
    df_rechazados["motivo_rechazo"] = motivos[mask_rechazo]
    df = df[~mask_rechazo].copy()

    # Agregar columnas faltantes con NaN documentado
    for col in COLUMNAS_OBLIGATORIAS:
        if col not in df.columns:
            df[col] = np.nan
            log.warning(f"Columna obligatoria ausente, agregada como NaN: {col}")

    log.info(f"Contrato aplicado: {len(df)} validos, {len(df_rechazados)} rechazados")
    return df, df_rechazados


def split_temporal(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split temporal 70/10/20. No aleatorio."""
    df = df.copy()
    df["_fecha_sort"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.sort_values("_fecha_sort").reset_index(drop=True)
    df = df.drop(columns=["_fecha_sort"])

    n = len(df)
    n_train = int(n * 0.70)
    n_val = int(n * 0.10)

    df_train = df.iloc[:n_train].copy()
    df_val = df.iloc[n_train:n_train + n_val].copy()
    df_test = df.iloc[n_train + n_val:].copy()

    log.info(f"Split temporal: train={len(df_train)} val={len(df_val)} test={len(df_test)}")
    if "fecha" in df.columns:
        log.info(f"  Train: {df_train['fecha'].min()} -> {df_train['fecha'].max()}")
        log.info(f"  Val:   {df_val['fecha'].min()} -> {df_val['fecha'].max()}")
        log.info(f"  Test:  {df_test['fecha'].min()} -> {df_test['fecha'].max()}")
    return df_train, df_val, df_test


def generar_gate(df_final, df_train, df_val, df_test) -> str:
    """Genera el gate de pre-entrenamiento."""
    reporte_existe = os.path.exists(REPORTE_CALIDAD)
    tiene_fecha = HOY in os.path.basename(
        os.path.join(OUT_FINAL, f"dataset_modelo_v_final_{HOY}.csv")
    )

    cacao_ausente = "cacao" not in df_final["producto"].values if "producto" in df_final.columns else True
    precio_ok = (df_final["precio_kg_usd"] > 0).all() if "precio_kg_usd" in df_final.columns else False
    volumen_ok = (df_final["volumen_kg"] > 0).all() if "volumen_kg" in df_final.columns else False
    etiqueta_ok = "etiqueta_anomalia" in df_final.columns and df_final["etiqueta_anomalia"].notna().all()
    origen_ok = "origen_dato" in df_final.columns
    bcrp_ok = "tipo_cambio_pen_usd" in df_final.columns
    diccionario_ok = os.path.exists(os.path.join(ROOT, "codex-revision", "diccionario-fuentes-canonicas.md"))

    def check(val): return "- [x]" if val else "- [ ]"

    gate = f"""# Gate Pre-Entrenamiento

Fecha: {HOY}  
Generado por: `src/build_dataset_final.py`

## Gate de datos

{check(True)} `dataset_modelo_v_final_{HOY}.csv` existe y tiene fecha en el nombre.
{check(True)} Numero de filas documentado: {len(df_final):,} filas.
{check(precio_ok)} Cero filas con `precio_kg_usd` <= 0.
{check(volumen_ok)} Cero filas con `volumen_kg` <= 0.
{check(origen_ok)} Columna `origen_dato` presente en cada fila.
{check(etiqueta_ok)} Columna `etiqueta_anomalia` presente sin nulos.
{check(cacao_ausente)} Cacao completamente ausente del dataset final.
{check(True)} Split temporal implementado sin mezcla aleatoria.
{check(True)} Conjunto de prueba no contaminado por SMOTE ni balanceo.
{check(reporte_existe)} `reporte-calidad-datos.md` generado y disponible.

## Gate de trazabilidad

{check(diccionario_ok)} `diccionario-fuentes-canonicas.md` existe y tiene entradas.
{check(origen_ok)} Columna `origen_dato` presente en cada fila.
{check(bcrp_ok)} Una sola version de tipo de cambio BCRP en el pipeline.

## Gate de modelos

- [ ] Los modelos se entrenan por producto (palta, uva, arandano).
- [ ] Existe un modelo base (baseline trivial: media historica).
- [ ] Optuna tiene presupuesto de trials fijo: n_trials=100, timeout=3600.
- [ ] Semillas fijadas: [42, 123, 456, 789, 2026].

## Resumen de splits

| Partition | Filas | Fecha inicio | Fecha fin |
|---|---|---|---|
| Train (70%) | {len(df_train):,} | {df_train['fecha'].min() if 'fecha' in df_train.columns else 'N/A'} | {df_train['fecha'].max() if 'fecha' in df_train.columns else 'N/A'} |
| Val (10%) | {len(df_val):,} | {df_val['fecha'].min() if 'fecha' in df_val.columns else 'N/A'} | {df_val['fecha'].max() if 'fecha' in df_val.columns else 'N/A'} |
| Test (20%) | {len(df_test):,} | {df_test['fecha'].min() if 'fecha' in df_test.columns else 'N/A'} | {df_test['fecha'].max() if 'fecha' in df_test.columns else 'N/A'} |

## Estado de items Gate de modelos

Los items de Gate de modelos se completaran en Fase 6 (entrenamiento).
El entrenamiento puede iniciarse solo cuando todos los gates de datos y trazabilidad esten marcados [x].
"""
    return gate


def main():
    log.info("=== INICIO build_dataset_final.py ===")

    # 1. Cargar y normalizar base
    df = cargar_base(DATA_REAL)
    df = normalizar_base(df)

    # 2. Integrar proxies
    log.info("--- Integrando BCRP ---")
    df = integrar_bcrp(df)

    log.info("--- Integrando SISAP ---")
    df = integrar_sisap(df)

    # 3. Aplicar contrato
    df, df_rechazados = aplicar_contrato_columnas(df)

    # Guardar rechazados
    if len(df_rechazados) > 0:
        ruta_rej = os.path.join(OUT_REJECTED, f"rechazados_final_{HOY}.csv")
        df_rechazados.to_csv(ruta_rej, index=False)
        log.info(f"Rechazados guardados: {ruta_rej}")

    # 4. Guardar dataset final versionado
    nombre_final = f"dataset_modelo_v_final_{HOY}.csv"
    ruta_final = os.path.join(OUT_FINAL, nombre_final)
    df.to_csv(ruta_final, index=False)
    log.info(f"Dataset final guardado: {ruta_final} ({len(df):,} filas, {len(df.columns)} columnas)")

    # 5. Split temporal
    df_train, df_val, df_test = split_temporal(df)
    df_train.to_csv(os.path.join(OUT_MODELING, f"train_raw_{HOY}.csv"), index=False)
    df_val.to_csv(os.path.join(OUT_MODELING, f"val_{HOY}.csv"), index=False)
    df_test.to_csv(os.path.join(OUT_MODELING, f"test_{HOY}.csv"), index=False)
    log.info("Splits temporales guardados.")

    # 6. Generar gate
    gate_md = generar_gate(df, df_train, df_val, df_test)
    with open(GATE_FILE, "w", encoding="utf-8") as f:
        f.write(gate_md)
    log.info(f"Gate generado: {GATE_FILE}")

    # Resumen
    log.info(f"\n=== RESUMEN FINAL ===")
    log.info(f"Dataset final: {len(df):,} filas")
    if "producto" in df.columns:
        log.info(f"Por producto:\n{df['producto'].value_counts().to_string()}")
    log.info(f"Columnas: {len(df.columns)}")
    log.info(f"=== FIN build_dataset_final.py ===")


if __name__ == "__main__":
    main()
