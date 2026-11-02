"""Read-only, fail-closed preflight. Exit 2 means expected unmet prerequisites.

This diagnostic never executes the reserved block and is not an authorization
mechanism. It reports evidence currently available instead of accepting flags.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inspect(root):
    root = Path(root)
    evidence = {}
    blockers = []

    def read(relative):
        path = root / relative
        if not path.is_file():
            blockers.append({'code': 'missing_artifact', 'path': relative})
            return None
        evidence[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        return json.loads(path.read_text(encoding='utf-8'))

    audit = read('planificacion/2026-11-01/ejecucion/auditoria-expansion.json')
    source_path = root / 'datasets/fuentes/2026-11-01-expansion/conciliacion/vista-conciliada.csv'
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest() if source_path.is_file() else None
    if source_hash is None:
        blockers.append({'code': 'expanded_source_missing'})
    if audit:
        if audit.get('source_sha256') != source_hash:
            blockers.append({'code': 'expanded_source_hash_mismatch'})
        if not audit.get('complete_week_certificates', 0):
            blockers.append({'code': 'no_complete_week_certificates', 'component': 'H1_H2_H3'})
        if not audit.get('publication_vintage_certificates', 0):
            blockers.append({'code': 'no_historical_publication_certificates', 'component': 'H1_H2_H3'})
        if not audit.get('prior_exposure'):
            blockers.append({'code': 'exposure_not_declared'})
    else:
        blockers.append({'code': 'coverage_audit_unavailable'})
    expanded_treatment = 'datasets/tratamiento/2026-11-01-expansion/manifest.json'
    treatment = read(expanded_treatment if (root/expanded_treatment).is_file()
                     else 'datasets/tratamiento/2026-11-01/manifest.json')
    if treatment:
        if treatment.get('views', {}).get('conservadora', {}).get('input_sha256') != source_hash:
            blockers.append({'code': 'features_not_rebuilt_for_expanded_source', 'component': 'H1_H2_H3'})
        if treatment.get('calendar', {}).get('requires_pretest_protocol_freeze', True):
            blockers.append({'code': 'calendar_and_protocol_not_frozen', 'component': 'H1_H2_H3'})
        if treatment.get('eligible_final_rows', 0) == 0:
            blockers.append({'code': 'no_verified_asof_eligible_final_rows', 'component': 'H1_H2_H3'})
        treatment_dir = root / (expanded_treatment if (root/expanded_treatment).is_file()
                                else 'datasets/tratamiento/2026-11-01/manifest.json')
        for name, expected in treatment.get('outputs_sha256', {}).items():
            artifact = (treatment_dir.parent/name).resolve()
            if not artifact.is_relative_to(treatment_dir.parent.resolve()) or not artifact.is_file():
                blockers.append({'code': 'feature_artifact_missing_or_invalid_path', 'artifact': name})
            elif hashlib.sha256(artifact.read_bytes()).hexdigest() != expected:
                blockers.append({'code': 'feature_artifact_hash_mismatch', 'artifact': name})
    selection = root / 'datasets/experimentos/h1-final/development-selection.json'
    if not selection.is_file():
        blockers.append({'code': 'no_final_grid_development_selection', 'component': 'H1_H2_H3'})
    h4 = read('datasets/experimentos/h4-controlado-v1/manifest.json')
    keys = read('datasets/experimentos/h4-controlado-v1/keys.json')
    reviewed = sum(key.get('review_status') == 'reviewed' for key in keys) if isinstance(keys, list) else 0
    if reviewed != 30:
        blockers.append({'code': 'h4_keys_not_human_reviewed', 'reviewed': reviewed, 'required': 30, 'component': 'H4'})
    if not h4 or not h4.get('generator_frozen'):
        blockers.append({'code': 'h4_generator_and_retrieval_not_frozen', 'component': 'H4'})
    environment = root / 'planificacion/2026-11-01/ejecucion/environment-clean.json'
    if not environment.is_file():
        blockers.append({'code': 'scientific_clean_environment_not_verified', 'component': 'environment'})
    else:
        env = read(str(environment.relative_to(root)).replace('\\', '/'))
        if not env or not env.get('smoke_all_passed') or not env.get('pip_check_passed'):
            blockers.append({'code': 'scientific_clean_environment_checks_failed', 'component': 'environment'})
    h2_status='not_closed_in_current_checkout'
    closure_path=root/'datasets/experimentos/h2-cierre-2026-11-01/decision.json'
    if closure_path.is_file():
        closure=read(str(closure_path.relative_to(root)).replace('\\','/'))
        source_hashes=closure.get('evidence_sha256',{}) if closure else {}
        required={
            'datasets/tratamiento/2026-11-01/bcrp-mensual-conciliado.csv',
            'datasets/tratamiento/2026-11-01/contexto/sisap-mensual-normalizado.csv',
            'datasets/tratamiento/2026-11-01/contexto/nasa-arequipa-contexto-2018-2026.json',
            'datasets/fuentes/2026-10-31/muestras-contextuales/comtrade-muestra.json',
            'datasets/tratamiento/2026-11-01-expansion/panel-conservadora.parquet'}
        current=required.issubset(source_hashes)
        for name,expected in source_hashes.items():
            artifact=(root/name).resolve()
            if not artifact.is_relative_to(root.resolve()) or not artifact.is_file() or hashlib.sha256(artifact.read_bytes()).hexdigest()!=expected:
                current=False
        if current and closure.get('status')=='closed_not_evaluable_current_release' and closure.get('eligible_context_families')==0:
            h2_status='closed_not_evaluable_current_release'
            for blocker in blockers:
                if blocker.get('component')=='H1_H2_H3':blocker['component']='H1_H3'
        else:
            h2_status='closure_stale_or_incomplete_reaudit_required'
            blockers.append({'code':'h2_closure_stale_or_incomplete','component':'H2'})
    return {'status': 'not_ready' if blockers else 'requires_full_protocol_review',
            'h2_status':h2_status,
            'diagnostic_only_not_execution_authorization': True,
            'final_test_executed_by_this_command': False,
            'source_sha256': source_hash, 'blockers': blockers, 'evidence_sha256': evidence,
            'note': 'Artifact presence does not certify scientific validity. No final runner is invoked.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='planificacion/2026-11-01/ejecucion/preflight-final.json')
    args = parser.parse_args()
    target = (ROOT / args.output).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError('Output must stay in repository')
    result = inspect(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=True))
    return 2 if result['blockers'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
