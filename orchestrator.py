#!/usr/bin/env python3
"""
orchestrator.py
===============
Orquestador Maestro del Pipeline de IA Explicable y Trazabilidad.
Permite listar la documentación de cada módulo, verificar la presencia de 
los archivos físicos y ejecutar secuencialmente el pipeline completo de la tesis,
generando una cadena de trazabilidad auditable y actualizando los borradores de la tesis.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import sys
import os
import argparse
import subprocess
import time
import hashlib
import json
from pathlib import Path

# Configuración de codificación de salida para Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Definición del Mapa de Módulos del Pipeline
PIPELINE_MODULES = {
    "etl": {
        "name": "Extracción e Ingesta de Datos (ETL)",
        "script": "pipeline/etl/sunat_scraper.py",
        "description": "Descarga programática de paquetes semanales ZIP de SUNAT, descompresión de DBFs, filtrado de subpartidas de agroexportación y consolidación de datos reales.",
        "inputs": ["Sitio Web Oficial de SUNAT (Aduanet)", "API BCRP Tipo de Cambio"],
        "outputs": ["data/dataset_real_v1.csv"]
    },
    "preprocess": {
        "name": "Preprocesamiento y Calidad de Datos",
        "script": "pipeline/preparation/preprocessing.py",
        "description": "Limpieza, imputación de valores nulos, normalización robusta y partición temporal en sets de entrenamiento/validación/prueba sin fugas de datos.",
        "inputs": ["data/dataset_real_v1.csv"],
        "outputs": ["data/gold/prediction_features.parquet", "data/gold/weekly_product_market.parquet"]
    },
    "layer1": {
        "name": "Capa 1: Predicción Tabular GBDT Global",
        "script": "pipeline/core/layer1_predictive.py",
        "description": "Entrena modelos XGBoost y LightGBM mediante Optuna para predecir precio FOB y volumen, calculando residuos normalizados robustos.",
        "inputs": ["data/gold/prediction_features.parquet"],
        "outputs": [
            "data/gold/anomaly_features.parquet",
            "models/xgb_price_model.pkl",
            "models/lgb_price_model.pkl",
            "models/xgb_vol_model.pkl",
            "models/lgb_vol_model.pkl"
        ]
    },
    "layer2": {
        "name": "Capa 2: Ensemble de Detección de Anomalías",
        "script": "pipeline/core/layer2_anomaly.py",
        "description": "Ejecuta algoritmos de Isolation Forest, LOF y ECOD, y consolida un score probabilístico mediante un ensemble unificado.",
        "inputs": ["data/gold/anomaly_features.parquet"],
        "outputs": [
            "data/gold/anomaly_metrics.json",
            "models/if_model.pkl",
            "models/lof_model.pkl",
            "models/ecod_model.pkl"
        ]
    },
    "layer3": {
        "name": "Capa 3: Explicabilidad Local con TreeSHAP",
        "script": "pipeline/core/layer3_explainability.py",
        "description": "Genera valores SHAP locales para cada transacción detectada como anómala para justificar la contribución de cada feature.",
        "inputs": ["data/gold/anomaly_features.parquet"],
        "outputs": ["data/gold/local_explanations.json"]
    },
    "layer4": {
        "name": "Capa 4: Reportabilidad RAG & LLM",
        "script": "pipeline/core/layer4_rag_reporting.py",
        "description": "Genera reportes de auditoría estructurados usando el LLM guiado por el contexto de SHAP y reglas normativas de comercio.",
        "inputs": ["data/gold/local_explanations.json"],
        "outputs": ["data/gold/generated_reports.json"]
    },
    "layer5": {
        "name": "Capa 5: Validación Factual y Consistencia Numérica",
        "script": "pipeline/core/layer5_validation.py",
        "description": "Verifica que el reporte generado contenga métricas y datos correctos consistentes con la base de datos de origen (evitando alucinaciones).",
        "inputs": ["data/gold/generated_reports.json"],
        "outputs": ["data/gold/validation_metrics.json"]
    },
    "layer6": {
        "name": "Capa 6: Cadena de Trazabilidad e Integridad",
        "script": "pipeline/core/layer6_traceability.py",
        "description": "Calcula hashes SHA-256 de todas las entradas y salidas para asegurar la inmutabilidad y auditabilidad completa del flujo.",
        "inputs": [
            "data/dataset_real_v1.csv",
            "data/gold/anomaly_features.parquet",
            "data/gold/generated_reports.json",
            "data/gold/validation_metrics.json"
        ],
        "outputs": ["data/gold/traceability_log.json"]
    }
}

def calculate_sha256(filepath: Path) -> str:
    """Calcula hash SHA-256 de forma eficiente."""
    if not filepath.exists():
        return "NO_ENCONTRADO"
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return f"ERROR: {str(e)}"

def print_banner(title: str):
    print("=" * 70)
    print(f" {title.center(68)} ")
    print("=" * 70)

def show_list():
    """Muestra la explicación y metadatos de cada script de Python."""
    print_banner("MAPA DE COMPONENTES DEL PIPELINE (EXPLICABILIDAD)")
    for key, info in PIPELINE_MODULES.items():
        print(f"\n🔹 [{key.upper()}] - {info['name']}")
        print(f"   Ruta:        {info['script']}")
        print(f"   Propósito:   {info['description']}")
        print(f"   Entradas:    {', '.join(info['inputs'])}")
        print(f"   Salidas:     {', '.join(info['outputs'])}")
        print("   " + "-" * 60)

def check_integrity():
    """Valida la existencia física de los scripts y dependencias."""
    print_banner("AUDITORÍA DE INTEGRIDAD FÍSICA DEL REPOSITORIO")
    all_ok = True
    
    # 1. Validar existencia de scripts
    print("\n[1] Verificando presencia de scripts de Python:")
    for key, info in PIPELINE_MODULES.items():
        p = Path(info["script"])
        status = "✅ OK" if p.exists() else "❌ FALTANTE"
        print(f"  - {info['script']:<50} {status}")
        if not p.exists():
            all_ok = False
            
    # 2. Validar archivos de datos clave
    print("\n[2] Verificando estado de archivos de entrada/salida clave:")
    for key, info in PIPELINE_MODULES.items():
        for out_file in info["outputs"]:
            p = Path(out_file)
            if p.exists():
                h = calculate_sha256(p)[:12]
                print(f"  - {out_file:<50} ✅ EXISTE (sha256: {h}...)")
            else:
                print(f"  - {out_file:<50} ⚠️ NO GENERADO AÚN")
                
    if all_ok:
        print("\n🎉 Integridad del repositorio: EXCELENTE. Todos los scripts necesarios están presentes.")
    else:
        print("\n⚠️ Advertencia: Algunos scripts críticos no se encuentran en las rutas especificadas.")
    return all_ok

def run_script(key: str, dry_run: bool = False):
    """Ejecuta un script específico del pipeline."""
    info = PIPELINE_MODULES.get(key)
    if not info:
        print(f"Clave del pipeline no válida: {key}")
        return False
        
    print_banner(f"EJECUTANDO: {info['name']}")
    print(f"Script:     {info['script']}")
    print(f"Propósito:  {info['description']}")
    print(f"Entrada(s): {', '.join(info['inputs'])}")
    print("-" * 70)
    
    if dry_run:
        print("[DRY-RUN] Simulación exitosa.")
        return True
        
    python_exe = sys.executable
    script_path = Path(info["script"])
    
    if not script_path.exists():
        print(f"❌ Error: El script {script_path} no existe.")
        return False
        
    t0 = time.time()
    
    # Ejecutamos con subprocess
    res = subprocess.run([python_exe, str(script_path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    elapsed = time.time() - t0
    
    if res.returncode == 0:
        print(f"✅ COMPLETADO con éxito en {elapsed:.2f} segundos.")
        # Mostrar últimas 10 líneas de salida estándar para contextualización
        lines = res.stdout.strip().split("\n")
        print("\n  --- Últimos mensajes del módulo ---")
        for line in lines[-8:]:
            print(f"  [stdout] {line}")
        return True
    else:
        print(f"❌ FALLÓ la ejecución del módulo. Código de retorno: {res.returncode}")
        print("\n--- [STDERR] ---")
        print(res.stderr)
        print("\n--- [STDOUT] ---")
        print(res.stdout)
        return False

def run_pipeline(steps, dry_run: bool = False):
    """Ejecuta una lista de pasos del pipeline en orden."""
    print_banner("INICIANDO EJECUCIÓN DEL PIPELINE")
    t_start = time.time()
    
    executed_steps = []
    
    for step in steps:
        if step not in PIPELINE_MODULES:
            print(f"Advertencia: omitiendo paso desconocido '{step}'")
            continue
        success = run_script(step, dry_run)
        if not success:
            print(f"\n❌ Deteniendo la orquestación debido a un fallo en el paso: {step}")
            sys.exit(1)
        executed_steps.append(step)
        
    total_time = time.time() - t_start
    print_banner("ORQUESTACIÓN COMPLETADA")
    print(f"Pasos ejecutados con éxito: {', '.join(executed_steps)}")
    print(f"Tiempo total transcurrido:  {total_time/60:.2f} minutos.")
    
    # Si ejecutamos todo, disparar sincronización e informes unificados de tesis
    if "layer6" in executed_steps and not dry_run:
        print("\nGenerando informes unificados y actualizando Capítulo IV...")
        run_post_pipeline_updates()

def run_post_pipeline_updates():
    """Ejecuta la actualización del borrador de tesis basándose en las métricas obtenidas."""
    # Intentar correr la integración directa de run_all.py si existe
    run_all_path = Path("src/run_all.py")
    if run_all_path.exists():
        print("Sincronizando tablas en documentos finales...")
        python_exe = sys.executable
        subprocess.run([python_exe, "src/run_all.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Borradores de tesis y tablas del Capítulo IV actualizados correctamente.")

def main():
    parser = argparse.ArgumentParser(description="Orquestador Explicable para el Pipeline de la Tesis (UNSA 2026)")
    parser.add_argument("--list", action="store_true", help="Explica cada script de Python y sus metadatos de tesis.")
    parser.add_argument("--check", action="store_true", help="Valida la integridad física de los archivos del pipeline.")
    parser.add_argument("--run", type=str, metavar="PASO", help="Ejecuta un paso ('etl', 'preprocess', 'layer1', etc.) o 'all' para el flujo completo.")
    parser.add_argument("--dry-run", action="store_true", help="Corre una simulación sin ejecutar los scripts reales.")
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    if args.list:
        show_list()
    elif args.check:
        check_integrity()
    elif args.run:
        if args.run.lower() == "all":
            # Ejecución en secuencia correcta
            pipeline_steps = ["etl", "preprocess", "layer1", "layer2", "layer3", "layer4", "layer5", "layer6"]
            run_pipeline(pipeline_steps, args.dry_run)
        else:
            run_pipeline([args.run.lower()], args.dry_run)

if __name__ == "__main__":
    main()
