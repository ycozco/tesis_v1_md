"""
FASE 2B: Extraccion y limpieza de archivos SUNAT/ADUANET (ZIP -> DBF -> CSV)
Salida: codex-revision/data_processed/sunat/
Log: codex-revision/logs/YYYY-MM-DD_parse_sunat_dbf.log

Reglas del plan (seccion 4.7, 4.11, 19.1):
- Solo leer DBF de prefijo 'x' (exportaciones)
- Filtrar partidas HS objetivo: 080440, 080610, 081040, 070920
- Encoding: cp850 primero, fallback latin-1
- ZIP corruptos: aislar en data/sunat/failed/
- Nunca sobreescribir fuente cruda
- Etiqueta origen: real_observada
"""
import os
import sys
import glob
import zipfile
import logging
import shutil
import pandas as pd
from datetime import datetime
from pathlib import Path

try:
    from dbfread import DBF
except ImportError:
    print("ERROR: instalar dbfread. Ejecutar: pip install dbfread")
    sys.exit(1)

# ── configuracion ─────────────────────────────────────────────────────────────
HOY = datetime.now().strftime("%Y-%m-%d")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUNAT_RAW = os.path.join(ROOT, "data", "sunat", "raw_downloads")
SUNAT_DIR = os.path.join(ROOT, "data", "sunat")
FAILED_DIR = os.path.join(SUNAT_DIR, "failed")
EXTRACT_DIR = os.path.join(ROOT, "codex-revision", "data_processed", "sunat", "extracted_temp")
OUT_DIR = os.path.join(ROOT, "codex-revision", "data_processed", "sunat")
LOG_DIR = os.path.join(ROOT, "codex-revision", "logs")
LOG_FILE = os.path.join(LOG_DIR, f"{HOY}_parse_sunat_dbf.log")

os.makedirs(FAILED_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
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

# ── partidas objetivo ─────────────────────────────────────────────────────────
HS_OBJETIVO = {
    "0804400000": {"producto": "palta", "hs6": "080440"},
    "0806100000": {"producto": "uva", "hs6": "080610"},
    "0810400000": {"producto": "arandano", "hs6": "081040"},
    "0709200000": {"producto": "esparrago", "hs6": "070920"},
    # variantes de 6 digitos
    "080440": {"producto": "palta", "hs6": "080440"},
    "080610": {"producto": "uva", "hs6": "080610"},
    "081040": {"producto": "arandano", "hs6": "081040"},
    "070920": {"producto": "esparrago", "hs6": "070920"},
}


def leer_dbf(path: str) -> pd.DataFrame | None:
    """Lee un DBF con fallback de encoding."""
    try:
        table = DBF(path, encoding="cp850", ignore_missing_memofile=True)
        df = pd.DataFrame(iter(table))
        log.info(f"  Leido con cp850: {len(df)} filas, {len(df.columns)} columnas")
        return df
    except UnicodeDecodeError:
        log.warning(f"  cp850 fallo, intentando latin-1")
        try:
            table = DBF(path, encoding="latin-1", ignore_missing_memofile=True)
            df = pd.DataFrame(iter(table))
            log.info(f"  Leido con latin-1: {len(df)} filas")
            return df
        except Exception as e:
            log.error(f"  Fallo latin-1 tambien: {e}")
            return None
    except Exception as e:
        log.error(f"  Error leyendo DBF {path}: {e}")
        return None


def filtrar_hs(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra filas por partida arancelaria objetivo."""
    # Detectar columna de partida — SUNAT usa PART_NANDI como nombre canonico
    col_partida = None
    candidatos_prioritarios = ["PART_NANDI", "PARTIDA", "NANDINA", "SUBPART", "ARANCEL"]
    for candidato in candidatos_prioritarios:
        for col in df.columns:
            if candidato in col.upper():
                col_partida = col
                break
        if col_partida:
            break

    if col_partida is None:
        # Fallback por contenido: buscar columna con valores que empiecen con 08 o 07
        for col in df.columns:
            sample = df[col].dropna().astype(str).head(50)
            if sample.str.match(r"^0[78]\d{6,8}").any():
                col_partida = col
                break

    if col_partida is None:
        log.warning("  No se encontro columna de partida arancelaria. Reportando columnas.")
        log.warning(f"  Columnas disponibles: {list(df.columns)}")
        return pd.DataFrame()

    log.info(f"  Columna partida detectada: {col_partida}")
    df = df.copy()
    df["_partida_str"] = df[col_partida].astype(str).str.strip()
    # NANDINA SUNAT tiene 10 digitos, los 6 primeros son HS6
    df["_hs6"] = df["_partida_str"].str[:6]

    # Filtrar por HS objetivo
    hs6_objetivo = {k for k in HS_OBJETIVO.keys() if len(k) == 6}
    mask = df["_hs6"].isin(hs6_objetivo)
    df_filtrado = df[mask].copy()

    if len(df_filtrado) == 0:
        log.info(f"  No hay registros de HS objetivo en este DBF.")
        return pd.DataFrame()

    # Agregar producto y hs6
    df_filtrado["hs6"] = df_filtrado["_hs6"]
    df_filtrado["producto"] = df_filtrado["_hs6"].map(
        {k: v["producto"] for k, v in HS_OBJETIVO.items() if len(k) == 6}
    )
    df_filtrado["col_partida_original"] = col_partida

    # Renombrar columnas SUNAT a nombres canonicos
    renombres = {
        "DNOMBRE": "empresa_exportadora",
        "CPAIDES": "destino_mercado",
        "FEMB": "fecha",
        "VFOBSERDOL": "valor_fob_usd",
        "VPESNET": "volumen_kg",
        "VPESBRU": "peso_bruto_kg",
        "CADU": "aduana_codigo",
        "UBIGEO": "ubigeo",
        "FANO": "anio",
        "CPUEDES": "puerto_destino",
    }
    for col_orig, col_nuevo in renombres.items():
        if col_orig in df_filtrado.columns:
            df_filtrado = df_filtrado.rename(columns={col_orig: col_nuevo})

    # Limpiar temporales
    df_filtrado = df_filtrado.drop(columns=["_partida_str", "_hs6"], errors="ignore")

    log.info(f"  Filas antes: {len(df)} | Filas objetivo: {len(df_filtrado)}")
    if "producto" in df_filtrado.columns:
        log.info(f"  Por producto:\n{df_filtrado['producto'].value_counts().to_string()}")
    return df_filtrado


def agregar_trazabilidad(df: pd.DataFrame, archivo_origen: str) -> pd.DataFrame:
    """Agrega columnas de trazabilidad al DataFrame."""
    df = df.copy()
    df["archivo_origen"] = archivo_origen
    df["origen_dato"] = "real_observada"
    df["granularidad"] = "embarque"
    df["fecha_generacion"] = HOY
    df["dataset_version"] = f"sunat_dbf_{HOY}"
    return df


def procesar_zip(zip_path: str) -> pd.DataFrame | None:
    """Extrae y procesa un ZIP de SUNAT que contiene DBF de exportaciones."""
    nombre = os.path.basename(zip_path)

    # Solo procesar ZIPs de exportaciones (prefijo 'x')
    if not nombre.lower().startswith("x"):
        log.info(f"  Saltando (no es exportacion): {nombre}")
        return None

    log.info(f"Procesando ZIP: {nombre}")

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            dbf_files = [f for f in z.namelist() if f.upper().endswith(".DBF")]
            if not dbf_files:
                log.warning(f"  ZIP sin DBF: {nombre}")
                return None
            for dbf_name in dbf_files:
                extract_path = os.path.join(EXTRACT_DIR, dbf_name)
                z.extract(dbf_name, EXTRACT_DIR)
                log.info(f"  Extraido: {dbf_name}")
    except zipfile.BadZipFile as e:
        log.error(f"  ZIP corrupto: {nombre} -> {e}. Aislando en failed/")
        shutil.copy2(zip_path, os.path.join(FAILED_DIR, nombre))
        return None
    except Exception as e:
        log.error(f"  Error abriendo ZIP {nombre}: {e}")
        return None

    dfs = []
    for dbf_name in dbf_files:
        dbf_path = os.path.join(EXTRACT_DIR, dbf_name)
        if not os.path.exists(dbf_path):
            continue
        df = leer_dbf(dbf_path)
        if df is not None and len(df) > 0:
            df_filtrado = filtrar_hs(df)
            if len(df_filtrado) > 0:
                df_filtrado = agregar_trazabilidad(df_filtrado, f"{nombre}/{dbf_name}")
                dfs.append(df_filtrado)

    return pd.concat(dfs, ignore_index=True) if dfs else None


def procesar_dbf_suelto(dbf_path: str) -> pd.DataFrame | None:
    """Procesa un DBF ya extraido en data/sunat/."""
    nombre = os.path.basename(dbf_path)
    if not nombre.lower().startswith("x"):
        return None
    log.info(f"Procesando DBF suelto: {nombre}")
    df = leer_dbf(dbf_path)
    if df is None or len(df) == 0:
        return None
    df_filtrado = filtrar_hs(df)
    if len(df_filtrado) == 0:
        return None
    return agregar_trazabilidad(df_filtrado, nombre)


def main():
    log.info("=== INICIO parse_sunat_dbf.py ===")
    log.info(f"Fuente ZIP: {SUNAT_RAW}")
    log.info(f"Fuente DBF suelto: {SUNAT_DIR}")

    todos_dfs = []

    # 1. Procesar ZIPs en raw_downloads
    zips = sorted(glob.glob(os.path.join(SUNAT_RAW, "x*.zip")))
    log.info(f"ZIPs de exportacion encontrados: {len(zips)}")
    for zip_path in zips:
        df = procesar_zip(zip_path)
        if df is not None and len(df) > 0:
            todos_dfs.append(df)

    # 2. Procesar DBF sueltos en data/sunat/
    dbfs = sorted(glob.glob(os.path.join(SUNAT_DIR, "x*.DBF")))
    log.info(f"DBFs sueltos encontrados: {len(dbfs)}")
    for dbf_path in dbfs:
        df = procesar_dbf_suelto(dbf_path)
        if df is not None and len(df) > 0:
            todos_dfs.append(df)

    if not todos_dfs:
        log.warning("No se encontraron registros con las partidas HS objetivo.")
        log.info(f"=== FIN. Ver log: {LOG_FILE} ===")
        return

    # Consolidar
    df_total = pd.concat(todos_dfs, ignore_index=True)

    # Deduplicar
    cols_dedup = [c for c in ["producto", "hs6", "fecha", "empresa", "volumen", "fob"] if c in df_total.columns]
    if cols_dedup:
        antes = len(df_total)
        df_total = df_total.drop_duplicates(subset=cols_dedup)
        log.info(f"Deduplicacion: {antes} -> {len(df_total)} filas")

    # Guardar
    nombre_salida = f"sunat_exportaciones_hs_objetivo_{HOY}.csv"
    ruta_salida = os.path.join(OUT_DIR, nombre_salida)
    df_total.to_csv(ruta_salida, index=False, encoding="utf-8")

    log.info(f"\n=== RESUMEN FINAL ===")
    log.info(f"Total filas procesadas: {len(df_total)}")
    if "producto" in df_total.columns:
        log.info(f"Por producto:\n{df_total['producto'].value_counts().to_string()}")
    log.info(f"Archivo salida: {ruta_salida}")
    log.info(f"Log: {LOG_FILE}")

    # Limpiar temporales
    shutil.rmtree(EXTRACT_DIR, ignore_errors=True)
    log.info("Temporales limpiados.")
    log.info("=== FIN parse_sunat_dbf.py ===")


if __name__ == "__main__":
    main()
