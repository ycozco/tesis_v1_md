#!/usr/bin/env python3
"""
src/module6_traceability.py
===========================
Implementa la Capa 6 (Registro de Trazabilidad y Seguridad de Auditoría):
1. Genera UUIDs únicos para cada ejecución de reporte.
2. Calcula hashes SHA-256 de archivos físicos (datos de entrada, modelos, reportes)
   para asegurar la auditabilidad, reproducibilidad e inmutabilidad.
3. Genera un log completo de la cadena de bloques operacional (Traceability Chain)
   desde el dato transaccional hasta el hash del reporte final en formato JSON.
4. Guarda la bitácora en data/gold/traceability_log.json.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import sys
import logging
import hashlib
import uuid
import json
from pathlib import Path

# Configuración de codificación de salida para Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Configuración de rutas
BASE_DIR = Path(".")
GOLD_DIR = BASE_DIR / "data" / "gold"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports" / "audits"

def calculate_file_hash(filepath: Path) -> str:
    """Calcula el hash SHA-256 de un archivo físico de forma eficiente por bloques."""
    if not filepath.exists():
        return "file_not_found"
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        log.error("Error al calcular hash de %s: %s", filepath.name, e)
        return "hash_error"

def calculate_dict_hash(d: dict) -> str:
    """Calcula el hash SHA-256 de un diccionario de Python serializado a JSON."""
    d_encoded = json.dumps(d, sort_keys=True).encode("utf-8")
    return hashlib.sha256(d_encoded).hexdigest()

def main():
    # 1. Cargar bases de datos y reportes generados
    reports_path = GOLD_DIR / "generated_reports.json"
    local_exp_path = GOLD_DIR / "local_explanations.json"
    validation_path = GOLD_DIR / "validation_metrics.json"
    
    if not reports_path.exists() or not local_exp_path.exists() or not validation_path.exists():
        log.error("Faltan archivos para registrar trazabilidad: reports, explanations o validation.")
        return
        
    generated_reports = {}
    with open(reports_path, "r", encoding="utf-8") as f:
        generated_reports = json.load(f)
        
    local_explanations = {}
    with open(local_exp_path, "r", encoding="utf-8") as f:
        local_explanations = json.load(f)
        
    validation_metrics = {}
    with open(validation_path, "r", encoding="utf-8") as f:
        validation_metrics = json.load(f)

    # 2. Calcular hashes globales de la infraestructura y datos base
    infrastructure_hashes = {
        "raw_data_hash": calculate_file_hash(BASE_DIR / "data" / "dataset_real_v1.csv"),
        "weekly_dataset_hash": calculate_file_hash(GOLD_DIR / "weekly_product_market.parquet"),
        "prediction_features_hash": calculate_file_hash(GOLD_DIR / "prediction_features.parquet"),
        "anomaly_features_hash": calculate_file_hash(GOLD_DIR / "anomaly_features.parquet"),
        "model_xgb_price_hash": calculate_file_hash(MODELS_DIR / "xgb_price_model.pkl"),
        "model_lgb_price_hash": calculate_file_hash(MODELS_DIR / "lgb_price_model.pkl"),
        "model_xgb_vol_hash": calculate_file_hash(MODELS_DIR / "xgb_vol_model.pkl"),
        "model_lgb_vol_hash": calculate_file_hash(MODELS_DIR / "lgb_vol_model.pkl"),
        "model_if_hash": calculate_file_hash(MODELS_DIR / "if_model.pkl"),
        "model_lof_hash": calculate_file_hash(MODELS_DIR / "lof_model.pkl"),
        "model_ecod_hash": calculate_file_hash(MODELS_DIR / "ecod_model.pkl"),
    }
    
    traceability_log = {}
    
    log.info("Construyendo cadena de trazabilidad e integridad de auditoría...")
    
    for key, report_data in generated_reports.items():
        alert_data = local_explanations[key]
        validation_res = validation_metrics["validation_by_report"].get(key, {})
        
        report_file = Path(report_data["filepath"])
        report_hash = calculate_file_hash(report_file)
        
        # Generar UUID único de trazabilidad para este reporte
        traceability_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"tesis.unsa.yoset.{key}"))
        
        # Estructurar la cadena secuencial (Traceability Chain)
        traceability_chain = {
            "traceability_uuid": traceability_uuid,
            "alert_key": key,
            "data_origin": {
                "product_code": alert_data["product_code"],
                "market": alert_data["market"],
                "week_start": alert_data["week_start"],
                "raw_dataset_hash": infrastructure_hashes["raw_data_hash"],
                "weekly_dataset_hash": infrastructure_hashes["weekly_dataset_hash"],
                "prediction_features_hash": infrastructure_hashes["prediction_features_hash"],
            },
            "layer1_regression": {
                "pred_price": alert_data["pred_price"],
                "pred_volume": alert_data["pred_volume"],
                "price_residual": alert_data["price_residual"],
                "volume_residual": alert_data["volume_residual"],
                "price_robust_z": alert_data["price_robust_z"],
                "volume_robust_z": alert_data["volume_robust_z"],
                "models_used": [
                    {"model": "XGBoost Price", "hash": infrastructure_hashes["model_xgb_price_hash"]},
                    {"model": "LightGBM Price", "hash": infrastructure_hashes["model_lgb_price_hash"]},
                    {"model": "XGBoost Volume", "hash": infrastructure_hashes["model_xgb_vol_hash"]},
                    {"model": "LightGBM Volume", "hash": infrastructure_hashes["model_lgb_vol_hash"]}
                ]
            },
            "layer2_anomaly_detection": {
                "ensemble_score": alert_data["ensemble_score"],
                "severity": alert_data["severity"],
                "is_anomaly": 1,
                "models_used": [
                    {"model": "Isolation Forest", "hash": infrastructure_hashes["model_if_hash"]},
                    {"model": "LOF", "hash": infrastructure_hashes["model_lof_hash"]},
                    {"model": "ECOD", "hash": infrastructure_hashes["model_ecod_hash"]}
                ]
            },
            "layer3_explainability": {
                "price_explanation_hash": calculate_dict_hash(alert_data["price_explanation"]),
                "volume_explanation_hash": calculate_dict_hash(alert_data["volume_explanation"]),
                "top_features": [f["feature"] for f in alert_data["price_explanation"]["top_positive"]]
            },
            "layer4_5_report_and_validation": {
                "report_filepath": report_data["filepath"],
                "report_sha256": report_hash,
                "is_factually_valid": validation_res.get("is_valid", False),
                "fidelity_score": validation_res.get("fidelity_score", 0.0),
                "completeness_score": validation_res.get("completeness_score", 0.0)
            }
        }
        
        traceability_log[key] = traceability_chain
        
    # Guardar bitácora de trazabilidad
    out_path = GOLD_DIR / "traceability_log.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(traceability_log, f, indent=4)
        
    log.info("Capa 6 completada: Bitácora de trazabilidad generada para %d reportes.", len(traceability_log))
    log.info("Log de trazabilidad guardado en: %s", out_path)

if __name__ == "__main__":
    main()
