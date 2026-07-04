#!/usr/bin/env python3
"""
src/module5_validation.py
=========================
Implementa la Capa 5 (Validador Factual y Consistencia Numérica):
1. Carga los reportes generados en Capa 4 y su evidencia original en local_explanations.json.
2. Parsea el texto Markdown buscando cantidades numéricas clave (precios, volúmenes, scores).
3. Valida la coincidencia numérica contra el objeto JSON de evidencia con una tolerancia del 0.5%.
4. Si se detecta una inconsistencia o alucinación, cae en el reporte descriptivo de TemplateProvider.
5. Calcula métricas cuantitativas de fidelidad factual y completitud.
6. Guarda los reportes validados y sus métricas de consistencia en data/gold/validation_metrics.json.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import sys
import logging
import json
import re
from pathlib import Path
from pipeline.core.layer4_rag_reporting import TemplateProvider

# Configuración de codificación de salida para Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Configuración de rutas
BASE_DIR = Path(".")
GOLD_DIR = BASE_DIR / "data" / "gold"

def load_json(filepath: Path) -> dict:
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extract_numbers_from_text(text: str) -> list[float]:
    """Extrae todos los números decimales y enteros de un texto."""
    # Eliminar comas de miles para parsear correctamente (ej: 1,500.50 -> 1500.50)
    clean_text = text.replace(",", "")
    pattern = r"[-+]?\d*\.\d+|\d+"
    matches = re.findall(pattern, clean_text)
    return [float(m) for m in matches]

def check_value_in_text(expected_val: float, text_numbers: list[float], tolerance: float = 0.005) -> bool:
    """Verifica si un número esperado existe en la lista de números del texto dentro de la tolerancia."""
    if expected_val == 0.0:
        return any(abs(n) < 1e-4 for n in text_numbers)
        
    for num in text_numbers:
        # Calcular error relativo
        error = abs(num - expected_val) / abs(expected_val)
        if error <= tolerance:
            return True
    return False

def validate_report(report_content: str, alert_data: dict) -> dict:
    """Valida la consistencia factual del reporte contra los datos de alerta originales."""
    text_numbers = extract_numbers_from_text(report_content)
    
    # Valores clave a validar
    facts_to_check = {
        "observed_price": alert_data["observed_price"],
        "pred_price": alert_data["pred_price"],
        "price_residual": alert_data["price_residual"],
        "price_robust_z": alert_data["price_robust_z"],
        "observed_volume": alert_data["observed_volume"],
        "pred_volume": alert_data["pred_volume"],
        "volume_residual": alert_data["volume_residual"],
        "volume_robust_z": alert_data["volume_robust_z"],
        "ensemble_score": alert_data["ensemble_score"]
    }
    
    verified_facts = 0
    failed_facts = []
    
    for fact_name, expected_val in facts_to_check.items():
        # Validar
        is_ok = check_value_in_text(expected_val, text_numbers, tolerance=0.005)
        if is_ok:
            verified_facts += 1
        else:
            failed_facts.append(fact_name)
            
    # Verificar completitud del formato
    has_uuid = "UUID" in report_content or "Código Único" in report_content
    has_trazabilidad = "trazabilidad" in report_content.lower() or "audit" in report_content.lower()
    has_shap = "shap" in report_content.lower()
    has_rag = "knowledge_base" in report_content.lower() or "recuperado" in report_content.lower() or "RAG" in report_content or "document" in report_content.lower()
    
    completeness_score = sum([has_uuid, has_trazabilidad, has_shap, has_rag]) / 4.0
    fidelity_score = verified_facts / len(facts_to_check)
    
    # El reporte es válido si la fidelidad es del 100% (todas las métricas clave coinciden)
    is_valid = fidelity_score == 1.0
    
    return {
        "is_valid": is_valid,
        "fidelity_score": fidelity_score,
        "completeness_score": completeness_score,
        "failed_facts": failed_facts,
        "verified_facts_count": verified_facts,
        "total_facts_count": len(facts_to_check)
    }

def main():
    # Cargar los reportes generados
    reports_path = GOLD_DIR / "generated_reports.json"
    local_exp_path = GOLD_DIR / "local_explanations.json"
    
    if not reports_path.exists() or not local_exp_path.exists():
        log.error("Faltan archivos para validación: %s o %s", reports_path, local_exp_path)
        return
        
    generated_reports = load_json(reports_path)
    local_explanations = load_json(local_exp_path)
    
    validation_results = {}
    total_reports = len(generated_reports)
    valid_reports_count = 0
    sum_fidelity = 0.0
    sum_completeness = 0.0
    
    template_provider = TemplateProvider()
    
    for key, report_data in generated_reports.items():
        log.info("Validando reporte factual para alerta: %s", key)
        report_content = report_data["report_content"]
        alert_data = local_explanations[key]
        
        # Validar
        res = validate_report(report_content, alert_data)
        
        # Si el reporte falla la validación factual, cae en el TemplateProvider determinístico
        if not res["is_valid"]:
            log.warning("Reporte %s falló la validación factual (inconsistencias detectadas: %s). Reemplazando con el TemplateProvider...", key, res["failed_facts"])
            corrected_content = template_provider.generate_report(alert_data, [])
            
            # Sobrescribir el archivo físico
            filepath = Path(report_data["filepath"])
            filepath.write_text(corrected_content, encoding="utf-8")
            
            # Recalcular la validación sobre el reporte corregido (debe pasar 100%)
            res = validate_report(corrected_content, alert_data)
            report_content = corrected_content
            
        valid_reports_count += 1 if res["is_valid"] else 0
        sum_fidelity += res["fidelity_score"]
        sum_completeness += res["completeness_score"]
        
        validation_results[key] = {
            "is_valid": res["is_valid"],
            "fidelity_score": res["fidelity_score"],
            "completeness_score": res["completeness_score"],
            "failed_facts": res["failed_facts"],
            "filepath": report_data["filepath"]
        }
        
    # Calcular métricas globales del sistema
    avg_fidelity = sum_fidelity / total_reports if total_reports > 0 else 1.0
    avg_completeness = sum_completeness / total_reports if total_reports > 0 else 1.0
    
    system_metrics = {
        "total_reports_evaluated": total_reports,
        "valid_reports_count": valid_reports_count,
        "average_fidelity_score": avg_fidelity,
        "average_completeness_score": avg_completeness,
        "validation_by_report": validation_results
    }
    
    # Guardar métricas en JSON
    metrics_path = GOLD_DIR / "validation_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(system_metrics, f, indent=4)
        
    log.info("Capa 5 completada: Evaluados %d reportes. Fidelidad promedio = %.2f%%, Completitud = %.2f%%.",
             total_reports, avg_fidelity * 100, avg_completeness * 100)
    log.info("Métricas de validación guardadas en: %s", metrics_path)

if __name__ == "__main__":
    main()
