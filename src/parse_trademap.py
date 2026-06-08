"""
FASE 2A: Parseo y limpieza de archivos Trade Map (.xls HTML)
Salida: codex-revision/data_processed/trademap/
Log: codex-revision/logs/YYYY-MM-DD_parse_trademap.log

Reglas del plan (seccion 6.2, 19.1):
- Los XLS de Trade Map son HTML exportados
- Excluir archivos import_colado_*
- Eliminar filas de totales y encabezados duplicados
- Solo incluir archivos export_*
- Etiqueta origen: real_agregada
- Granularidad: producto_destino_anio o producto
"""
import os
import sys
import glob
import logging
import pandas as pd
from datetime import datetime

# ── configuracion ─────────────────────────────────────────────────────────────
HOY = datetime.now().strftime("%Y-%m-%d")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRADEMAP_DIR = os.path.join(ROOT, "data-trademap")
OUT_DIR = os.path.join(ROOT, "codex-revision", "data_processed", "trademap")
LOG_DIR = os.path.join(ROOT, "codex-revision", "logs")
LOG_FILE = os.path.join(LOG_DIR, f"{HOY}_parse_trademap.log")

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

# ── mapeo de productos por patron de nombre ───────────────────────────────────
HS_MAP = {
    "hs070920": {"producto": "esparrago", "hs": "070920"},
    "hs080440": {"producto": "palta", "hs": "080440"},
    "hs080610": {"producto": "uva", "hs": "080610"},
    "hs081040": {"producto": "arandano", "hs": "081040"},
}

TIPO_MAP = {
    "export_indicadores_2025": "indicadores_2025",
    "export_serie_anual_2021_2025": "serie_anual_2021_2025",
}


def detectar_tipo_y_producto(fname: str):
    """Devuelve (tipo, producto, hs) o None si el archivo debe excluirse."""
    base = os.path.basename(fname).lower()
    # Excluir importaciones coladas
    if base.startswith("import_colado") or base.startswith("import"):
        return None
    tipo = None
    for patron, t in TIPO_MAP.items():
        if patron in base:
            tipo = t
            break
    if tipo is None:
        return None
    prod_info = None
    for patron, info in HS_MAP.items():
        if patron in base:
            prod_info = info
            break
    if prod_info is None:
        return None
    return tipo, prod_info["producto"], prod_info["hs"]


def leer_xls_html(path: str) -> pd.DataFrame:
    """Lee un XLS de Trade Map (puede ser HTML disfrazado)."""
    try:
        df = pd.read_excel(path, engine="openpyxl")
        log.info(f"  Leido con openpyxl: {os.path.basename(path)} ({len(df)} filas)")
        return df
    except Exception as e1:
        log.warning(f"  openpyxl fallo: {e1}. Intentando pd.read_html()")
        try:
            dfs = pd.read_html(path)
            if not dfs:
                raise ValueError("pd.read_html() no encontro tablas")
            df = dfs[0]
            log.info(f"  Leido con pd.read_html(): {os.path.basename(path)} ({len(df)} filas)")
            return df
        except Exception as e2:
            log.error(f"  Fallo total lectura {path}: {e1} | {e2}")
            return None


def limpiar_df(df: pd.DataFrame, tipo: str, producto: str, hs: str, archivo: str) -> pd.DataFrame:
    """Limpia y etiqueta el DataFrame."""
    filas_ini = len(df)

    # Eliminar filas de totales o encabezados duplicados en primera columna
    primera_col = df.columns[0]
    mask_total = df[primera_col].astype(str).str.contains(
        "Total|Reporter|Exporters|Importers|World|nan", na=False, case=False
    )
    df = df[~mask_total].copy()

    # Eliminar filas completamente vacias
    df = df.dropna(how="all")

    # Normalizar nombres de columnas
    df.columns = [
        str(c).strip().lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        for c in df.columns
    ]

    # Agregar columnas de trazabilidad
    df["producto"] = producto
    df["hs"] = hs
    df["tipo_vista"] = tipo
    df["archivo_origen"] = os.path.basename(archivo)
    df["origen_dato"] = "real_agregada"
    df["granularidad"] = "producto_destino_anio" if "anual" in tipo else "producto_destino"
    df["fecha_generacion"] = HOY
    df["dataset_version"] = f"trademap_{tipo}_{HOY}"

    filas_fin = len(df)
    descartadas = filas_ini - filas_fin
    log.info(f"  Limpieza: {filas_ini} -> {filas_fin} filas ({descartadas} descartadas)")
    return df


def procesar_todos():
    archivos = glob.glob(os.path.join(TRADEMAP_DIR, "*.xls"))
    log.info(f"Encontrados {len(archivos)} archivos XLS en {TRADEMAP_DIR}")

    resumen = []
    total_filas = 0

    for path in sorted(archivos):
        info = detectar_tipo_y_producto(path)
        if info is None:
            log.info(f"EXCLUIDO (import_colado o desconocido): {os.path.basename(path)}")
            continue

        tipo, producto, hs = info
        log.info(f"Procesando: {os.path.basename(path)} -> tipo={tipo}, producto={producto}")

        df = leer_xls_html(path)
        if df is None:
            log.error(f"  No se pudo leer {path}. Aislando como fallo.")
            continue

        df_limpio = limpiar_df(df, tipo, producto, hs, path)

        # Salida
        nombre_salida = f"trademap_{tipo}_{producto}_{HOY}.csv"
        ruta_salida = os.path.join(OUT_DIR, nombre_salida)
        df_limpio.to_csv(ruta_salida, index=False, encoding="utf-8")
        log.info(f"  Guardado: {ruta_salida} ({len(df_limpio)} filas)")

        total_filas += len(df_limpio)
        resumen.append({
            "archivo_origen": os.path.basename(path),
            "archivo_salida": nombre_salida,
            "tipo": tipo,
            "producto": producto,
            "hs": hs,
            "filas": len(df_limpio),
        })

    # Resumen consolidado
    if resumen:
        df_resumen = pd.DataFrame(resumen)
        ruta_resumen = os.path.join(OUT_DIR, f"trademap_resumen_{HOY}.csv")
        df_resumen.to_csv(ruta_resumen, index=False)
        log.info(f"\n=== RESUMEN ===")
        log.info(f"Archivos procesados: {len(resumen)}")
        log.info(f"Filas totales: {total_filas}")
        log.info(f"Resumen guardado en: {ruta_resumen}")
    else:
        log.warning("No se proceso ningun archivo Trade Map.")

    log.info(f"Log guardado en: {LOG_FILE}")


if __name__ == "__main__":
    procesar_todos()
