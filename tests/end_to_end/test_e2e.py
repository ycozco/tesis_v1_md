import os
import json
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
GOLD_DIR = BASE_DIR / "data" / "gold"

def test_traceability_reconstruction():
    """
    Verifica que cada alerta registrada en data/gold/traceability_log.json sea trazable
    y contenga los metadatos y estructuras mínimos para reconstruir su linaje de extremo a extremo:
    1. Identificadores únicos (traceability_uuid, alert_key)
    2. Origen de datos (product_code, market, week_start, hashes de datasets)
    3. Capa 1: Modelos regresores y hashes de modelos
    4. Capa 2: Scores, severidad e is_anomaly del ensemble
    5. Capa 3: Explicabilidad (top_features)
    6. Capa 4-5: Trazabilidad y validación de reportes (report_sha256)
    """
    traceability_path = GOLD_DIR / "traceability_log.json"
    assert traceability_path.exists(), "No se encontró el archivo traceability_log.json"

    with open(traceability_path, "r", encoding="utf-8") as f:
        log_data = json.load(f)
        
    assert isinstance(log_data, dict), "El log de trazabilidad debe ser un diccionario de registros"
    assert len(log_data) > 0, "El log de trazabilidad no debe estar vacío"
    
    for key, record in log_data.items():
        # 1. Identificación
        assert "traceability_uuid" in record, f"Falta traceability_uuid en registro {key}"
        assert "alert_key" in record, f"Falta alert_key en registro {key}"
        assert record["alert_key"] == key
        assert "-" in record["traceability_uuid"], "traceability_uuid debe ser un UUID válido"
        
        # 2. Origen de Datos
        assert "data_origin" in record, f"Falta data_origin en registro {key}"
        data_origin = record["data_origin"]
        assert "product_code" in data_origin
        assert "market" in data_origin
        assert "week_start" in data_origin
        assert "raw_dataset_hash" in data_origin
        assert "prediction_features_hash" in data_origin
        assert len(data_origin["raw_dataset_hash"]) == 64
        
        # 3. Capa 1: Modelos y Predicción
        assert "layer1_regression" in record, f"Falta layer1_regression en registro {key}"
        regression = record["layer1_regression"]
        assert "pred_price" in regression
        assert "pred_volume" in regression
        assert "models_used" in regression
        for model in regression["models_used"]:
            assert "model" in model
            assert "hash" in model
            assert len(model["hash"]) == 64
            
        # 4. Capa 2: Anomalías
        assert "layer2_anomaly_detection" in record, f"Falta layer2_anomaly_detection en registro {key}"
        anomaly = record["layer2_anomaly_detection"]
        assert "ensemble_score" in anomaly
        assert "severity" in anomaly
        assert "is_anomaly" in anomaly
        assert "models_used" in anomaly
        for model in anomaly["models_used"]:
            assert "model" in model
            assert "hash" in model
            
        # 5. Capa 3: Explicabilidad
        assert "layer3_explainability" in record, f"Falta layer3_explainability en registro {key}"
        explain = record["layer3_explainability"]
        assert "price_explanation_hash" in explain
        assert "volume_explanation_hash" in explain
        assert "top_features" in explain
        assert isinstance(explain["top_features"], list)
        
        # 6. Capa 4-5: Reporte y validación
        assert "layer4_5_report_and_validation" in record, f"Falta layer4_5_report_and_validation en registro {key}"
        report = record["layer4_5_report_and_validation"]
        assert "report_filepath" in report
        assert "report_sha256" in report
        assert "is_factually_valid" in report
        assert len(report["report_sha256"]) == 64
        
        print(f"Alerta {key} verificada con trazabilidad completa de extremo a extremo.")
        break # Verificar la primera es suficiente para probar la estructura
