import importlib.util
import json
import hashlib
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


def test_h2_closure_is_scoped_to_unchanged_evidence_and_reopens_on_change(tmp_path):
    paths=['datasets/tratamiento/2026-11-01/bcrp-mensual-conciliado.csv',
        'datasets/tratamiento/2026-11-01/contexto/sisap-mensual-normalizado.csv',
        'datasets/tratamiento/2026-11-01/contexto/nasa-arequipa-contexto-2018-2026.json',
        'datasets/fuentes/2026-10-31/muestras-contextuales/comtrade-muestra.json',
        'datasets/tratamiento/2026-11-01-expansion/panel-conservadora.parquet']
    hashes={}
    for name in paths:
        path=tmp_path/name;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(b'artificial-integrity-fixture-not-scientific-data')
        hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    closure=tmp_path/'datasets/experimentos/h2-cierre-2026-11-01/decision.json'
    closure.parent.mkdir(parents=True)
    closure.write_text(json.dumps({'status':'closed_not_evaluable_current_release',
        'eligible_context_families':0,'evidence_sha256':hashes}))
    assert MODULE.inspect(tmp_path)['h2_status']=='closed_not_evaluable_current_release'
    (tmp_path/paths[0]).write_bytes(b'changed')
    result=MODULE.inspect(tmp_path)
    assert result['h2_status']=='closure_stale_or_incomplete_reaudit_required'
    assert any(item['code']=='h2_closure_stale_or_incomplete' for item in result['blockers'])


def test_h2_closure_without_evidence_does_not_close_hypothesis(tmp_path):
    closure=tmp_path/'datasets/experimentos/h2-cierre-2026-11-01/decision.json'
    closure.parent.mkdir(parents=True)
    closure.write_text(json.dumps({'status':'closed_not_evaluable_current_release',
        'eligible_context_families':0,'evidence_sha256':{}}))
    assert MODULE.inspect(tmp_path)['h2_status']=='closure_stale_or_incomplete_reaudit_required'
