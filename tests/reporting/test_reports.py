import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from pipeline.core.layer5_validation import validate_report
from pipeline.core.layer4_rag_reporting import TemplateProvider

BASE_DIR = Path(__file__).resolve().parent.parent.parent
GOLD_DIR = BASE_DIR / "data" / "gold"

def test_template_provider_and_factual_validation():
    """
    Prueba que el TemplateProvider genere reportes consistentes y que el validador
    factual admita desviaciones menores por redondeo (<= 0.5%) y rechace
    alucinaciones numéricas mayores.
    """
    # 1. Crear evidencia ficticia de una alerta
    evidence = {
        "alert_id": "8f830a7d-b103-4c9f-85d1-6789e0839e9f",
        "product_code": "0804400000",
        "product_name": "Palta",
        "market": "USA",
        "market_aggregated": "USA",
        "week_start": "2025-08-04",
        "observed_price": 2.50,
        "pred_price": 1.80,
        "expected_price": 1.80,
        "price_residual": 0.70,
        "price_robust_z": 1.5,
        "observed_volume": 120000.0,
        "pred_volume": 100000.0,
        "expected_volume": 100000.0,
        "volume_residual": 20000.0,
        "volume_robust_z": 0.8,
        "ensemble_score": 0.985,
        "severity": "MEDIA",
        "price_explanation": {
            "top_positive": [{"feature": "volume_lag_1", "shap_value": 0.45}],
            "top_negative": [{"feature": "tipo_cambio_pen_usd_lag1", "shap_value": -0.10}]
        },
        "volume_explanation": {
            "top_positive": [{"feature": "temperatura_max_c_lag1", "shap_value": 0.20}],
            "top_negative": []
        }
    }
    
    # 2. Probar TemplateProvider
    provider = TemplateProvider()
    report = provider.generate_report(evidence, retrieved_context=[])
    
    assert "0804400000" in report
    assert "USA" in report
    assert "2025-08-04" in report
    assert "MEDIA" in report
    
    # 3. Probar validador factual con reporte correcto (del TemplateProvider)
    # Debe pasar porque las cifras coinciden exactamente
    res = validate_report(report, evidence)
    assert res["is_valid"], f"El reporte generado por la plantilla falló la validación. Errores: {res['failed_facts']}"
    assert res["fidelity_score"] == 1.0
    
    # 4. Probar validador factual con reporte modificado con cifras erróneas (alucinación)
    bad_report = report.replace("1.8000", "9.9000") # cambia el precio predicho
    res_bad = validate_report(bad_report, evidence)
    assert not res_bad["is_valid"], "El validador debió rechazar el reporte con precio alucinado (9.9)"
    assert "pred_price" in res_bad["failed_facts"] or "expected_price" in res_bad["failed_facts"]
    
    # 5. Probar tolerancia de redondeo menor (dentro del 0.5%)
    # Si el valor real es 120000.0 y el texto dice 120100.0 (desviación de 0.08%), debe ser aceptado
    tolerable_report = report.replace("120,000.00", "120,100.00")
    res_tol = validate_report(tolerable_report, evidence)
    assert res_tol["is_valid"], f"El validador debió aceptar desviación menor por redondeo. Errores: {res_tol['failed_facts']}"
