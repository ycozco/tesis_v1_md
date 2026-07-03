#!/usr/bin/env python3
"""
src/verify_integrity.py
=======================
Verifica formalmente la calidad de los datos de entrada para la tesis:
1. Completitud de las variables obligatorias de la operacionalización.
2. Consistencia de tipos (fechas, RUC, numéricas, categóricas).
3. Rangos de plausibilidad física y lógica.
4. Tasa de nulos y existencia de duplicados.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import sys
import pandas as pd
from pathlib import Path

# Configuración de codificación de salida para Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 8 variables operacionales continuas + discretas + categorizaciones
REQUIRED_COLUMNS = [
    "id", "fecha", "producto", "partida_arancelaria", "empresa_exportadora", "zona",
    "volumen_kg", "precio_kg_usd", "destino_mercado", "dias_logisticos",
    "costo_logistico_usd_kg", "cumplimiento_fitosanitario", "merma_pct",
    "tipo_cambio_pen_usd", "temperatura_max_c", "temperatura_min_c",
    "precipitacion_mm", "humedad_pct"
]

def verify_dataset(filepath: Path, label: str) -> bool:
    print(f"\n--- Verificando Integridad de Dataset {label.upper()}: {filepath.name} ---")
    if not filepath.exists():
        print(f"❌ Error: El archivo {filepath} no existe.")
        return False
        
    df = pd.read_csv(filepath)
    has_errors = False
    
    # 1. Completitud
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        print(f"❌ Completitud fallida. Columnas faltantes: {missing_cols}")
        has_errors = True
    else:
        print("✅ Completitud: Todas las variables requeridas están presentes.")
        
    # 2. Consistencia de formatos y tipos
    # Formato de fechas
    try:
        parsed_dates = pd.to_datetime(df['fecha'], format='%Y-%m-%d', errors='coerce')
        invalid_dates = parsed_dates.isna().sum()
        if invalid_dates > 0:
            print(f"❌ Consistencia de Fecha fallida. Encontradas {invalid_dates} fechas inválidas.")
            has_errors = True
        else:
            print("✅ Formato de Fecha: Todas las fechas están en el formato YYYY-MM-DD.")
    except Exception as e:
        print(f"❌ Error al parsear fechas: {e}")
        has_errors = True
        
    # Tipado numérico
    numeric_cols = [
        "volumen_kg", "precio_kg_usd", "dias_logisticos", "costo_logistico_usd_kg",
        "cumplimiento_fitosanitario", "merma_pct", "tipo_cambio_pen_usd",
        "temperatura_max_c", "temperatura_min_c", "precipitacion_mm", "humedad_pct"
    ]
    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"❌ Tipo inválido: La columna '{col}' no es numérica.")
            has_errors = True
            
    # 3. Rangos y Plausibilidad
    # Precios y Volúmenes
    invalid_prices = (df['precio_kg_usd'] <= 0).sum()
    invalid_volumes = (df['volumen_kg'] <= 0).sum()
    if invalid_prices > 0 or invalid_volumes > 0:
        print(f"❌ Plausibilidad fallida: Encontrados {invalid_prices} precios <= 0 y {invalid_volumes} volúmenes <= 0.")
        has_errors = True
    else:
        print("✅ Plausibilidad: Todos los precios y volúmenes son mayores que cero.")
        
    # Clima (SENAMHI)
    invalid_temp_max = ((df['temperatura_max_c'] < -10) | (df['temperatura_max_c'] > 48)).sum()
    invalid_temp_min = ((df['temperatura_min_c'] < -15) | (df['temperatura_min_c'] > 38)).sum()
    invalid_precip = ((df['precipitacion_mm'] < 0) | (df['precipitacion_mm'] > 500)).sum()
    invalid_humidity = ((df['humedad_pct'] < 0) | (df['humedad_pct'] > 100)).sum()
    
    if invalid_temp_max or invalid_temp_min or invalid_precip or invalid_humidity:
        print(f"❌ Clima fallido: Encontradas temperaturas fuera de rango (-10°C a 48°C) o humedad fuera de [0, 100].")
        has_errors = True
    else:
        print("✅ Clima: Todas las temperaturas, precipitaciones y humedades están dentro de los rangos físicos plausibles.")
        
    # Sanidad (SENASA)
    invalid_fito = (~df['cumplimiento_fitosanitario'].isin([0, 1])).sum()
    if invalid_fito > 0:
        print(f"❌ Fitosanitario fallido: Encontrados {invalid_fito} valores no binarios.")
        has_errors = True
    else:
        print("✅ Fitosanitario: Todos los estados de cumplimiento fitosanitario son binarios (0 o 1).")
        
    # Mermas
    invalid_merma = ((df['merma_pct'] < 0) | (df['merma_pct'] > 100)).sum()
    if invalid_merma > 0:
        print(f"❌ Mermas fallidas: Encontradas {invalid_merma} mermas fuera del rango [0%, 100%].")
        has_errors = True
    else:
        print("✅ Mermas: Todos los porcentajes de merma están acotados entre 0% y 100%.")

    # 4. Control de Nulos y Duplicados
    nulls = df.isnull().sum().sum()
    duplicates = df.duplicated(subset=[c for c in df.columns if c != 'id']).sum()
    
    print(f"ℹ️  Valores nulos iniciales: {nulls}")
    print(f"ℹ️  Registros duplicados: {duplicates}")
    
    if duplicates > 0:
        print(f"⚠️  Advertencia: Se detectaron {duplicates} registros duplicados (serán ignorados durante el modelado).")
        
    return not has_errors

def main():
    print("==================================================")
    print("🔍 VERIFICADOR DE INTEGRIDAD DE DATOS DE TESIS")
    print("==================================================")
    
    synthetic_path = Path("data/dataset_agro_sintetico_v1.csv")
    real_path = Path("data/dataset_real_v1.csv")
    
    s_ok = verify_dataset(synthetic_path, "sintético")
    r_ok = verify_dataset(real_path, "real")
    
    print("\n==================================================")
    if s_ok and r_ok:
        print("🎉 ¡TODOS LOS DATOS HAN PASADO LA AUDITORÍA DE INTEGRIDAD!")
        sys.exit(0)
    else:
        print("⚠️  Se encontraron errores o advertencias en los datos.")
        sys.exit(1)

if __name__ == "__main__":
    main()
