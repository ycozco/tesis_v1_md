import importlib.util
import json
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('final_preflight', Path(__file__).resolve().parents[2]/'tools/check_final_experiment.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_missing_evidence_fails_closed_without_running_any_experiment(tmp_path):
    result = MODULE.inspect(tmp_path)
    assert result['status'] == 'not_ready'
    assert result['final_test_executed_by_this_command'] is False
    assert any(item['code'] == 'coverage_audit_unavailable' for item in result['blockers'])


def test_reported_ready_boolean_does_not_override_missing_certificates(tmp_path):
    path = tmp_path/'planificacion/2026-11-01/ejecucion'
    path.mkdir(parents=True)
    (path/'auditoria-expansion.json').write_text(json.dumps({
        'final_test_authorized': True, 'source_sha256': 'fabricated',
        'complete_week_certificates': 0, 'publication_vintage_certificates': 0}))
    codes = {item['code'] for item in MODULE.inspect(tmp_path)['blockers']}
    assert 'expanded_source_hash_mismatch' in codes
    assert 'no_complete_week_certificates' in codes
    assert 'no_historical_publication_certificates' in codes
