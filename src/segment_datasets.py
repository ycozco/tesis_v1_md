#!/usr/bin/env python3
"""
src/segment_datasets.py
=======================
Particiona el dataset consolidado de microdatos reales por producto/cultivo
para permitir el entrenamiento independiente y modularizado de cada uno de ellos.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import logging
from pathlib import Path
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Directorios de datos
DATA_DIR = Path("data")
MASTER_DATA_PATH = DATA_DIR / "dataset_real_v1.csv"
OUTPUT_DIR = DATA_DIR / "real_processed"

def segment_by_product():
    if not MASTER_DATA_PATH.exists():
        log.error("❌ El dataset maestro real '%s' no existe. Ejecute el ETL primero.", MASTER_DATA_PATH)
        return False
        
    log.info("📖 Cargando dataset consolidado real...")
    df = pd.read_csv(MASTER_DATA_PATH)
    
    # 3 Cultivos principales de agroexportación
    crops = ["palta", "uva", "arandano"]
    
    for crop in crops:
        crop_dir = OUTPUT_DIR / crop
        crop_dir.mkdir(parents=True, exist_ok=True)
        
        # Filtrar registros específicos de este producto
        df_crop = df[df["producto"] == crop].copy()
        
        # Exportar a la subcarpeta del cultivo
        out_path = crop_dir / f"dataset_{crop}_raw.csv"
        df_crop.to_csv(out_path, index=False)
        log.info("✅ Segmento [%s] generado con éxito en '%s' (%d registros)", 
                 crop.upper(), out_path.relative_to(DATA_DIR.parent), len(df_crop))
                 
    return True

if __name__ == "__main__":
    segment_by_product()
