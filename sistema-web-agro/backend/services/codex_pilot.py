"""Read-only, exposed Codex pilot. No model invocation, cached replay count or API."""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
from services.research_ai import ResearchError

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'datasets/experimentos/codex-piloto-declarado-2026-11-01'


def load():
    manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
    content=(BASE/'responses.json').read_bytes()
    case_content=(ROOT/'datasets/experimentos/h4-controlado-v1/cases.json').read_bytes()
    if hashlib.sha256(content).hexdigest()!=manifest['responses_sha256'] or hashlib.sha256(case_content).hexdigest()!=manifest['source_cases_sha256']:
        raise ResearchError('codex_pilot_integrity','La evidencia del piloto Codex cambió; requiere revisión.',409)
    return manifest,json.loads(content),{c['case_id']:c for c in json.loads(case_content)}


def catalogue():
    manifest,responses,_=load()
    return {'provenance':manifest,'pilots':[{k:r[k] for k in ('id','case_id','title')} for r in responses]}


def detail(pilot_id):
    manifest,responses,cases=load()
    response=next((r for r in responses if r['id']==pilot_id),None)
    if response is None:raise ResearchError('codex_pilot_not_found','Piloto Codex no disponible.',404)
    case=cases[response['case_id']]
    expected=next(r for r in manifest['cases'] if r['case_id']==case['case_id'])
    if expected['payload_sha256']!=case['payload_sha256']:
        raise ResearchError('codex_case_changed','Las entradas del piloto cambiaron.',409)
    keys=json.loads((ROOT/'datasets/experimentos/h4-controlado-v1/keys.json').read_text(encoding='utf-8'))
    if hashlib.sha256((ROOT/'datasets/experimentos/h4-controlado-v1/keys.json').read_bytes()).hexdigest()!=manifest['source_keys_sha256']:
        raise ResearchError('codex_key_changed','La referencia numérica del piloto cambió.',409)
    key=next(k for k in keys if k['case_id']==case['case_id'])
    from decimal import Decimal
    checks=[]
    for claim in response['numeric_claims']:
        reference=key['numeric'].get(claim['element_id'])
        valid=False
        if reference:
            tolerance=Decimal('.5')*Decimal(10)**-reference['decimals']+Decimal('1e-9')
            valid=claim['unit']==reference['unit'] and abs(Decimal(claim['value'])-Decimal(reference['value']))<=tolerance
        checks.append({**claim,'valid':valid})
    complete={c['element_id'] for c in checks}==set(key['numeric']) and len(checks)==len(key['numeric'])
    return {**response,'provenance':manifest,'input':case['payload'],
        'numeric_validation':{'status':'passed' if checks and complete and all(c['valid'] for c in checks) else 'not_applicable' if not checks and not key['numeric'] else 'failed','claims':checks},
        'factual_status':'requires_human_review','delivery':'archived_not_new_inference',
        'source_catalogue_sha256':manifest['responses_sha256'],'new_inference':False,
        'h4_final_output':False}


def export(pilot_id):
    content=json.dumps(detail(pilot_id),indent=2,ensure_ascii=False).encode('utf-8')
    return content,hashlib.sha256(content).hexdigest()


def progress():
    content=(BASE/'progress-evidence.json').read_bytes()
    hashes=json.loads((BASE/'hashes.json').read_text(encoding='utf-8'))
    if hashlib.sha256(content).hexdigest()!=hashes['progress-evidence.json']:
        raise ResearchError('progress_changed','El estado del proyecto requiere revisión de integridad.',409)
    data=json.loads(content);checked=[]
    for name,expected in data['evidence_sha256'].items():
        path=(ROOT/name).resolve()
        if not path.is_relative_to(ROOT):raise ResearchError('progress_path','Ruta de evidencia no válida.',409)
        actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        checked.append({'artifact':name,'expected_sha256':expected,'actual_sha256':actual,'matches':actual==expected})
    if not all(r['matches'] for r in checked):raise ResearchError('progress_stale','Las fuentes cambiaron; reconstruya el estado del proyecto.',409)
    return {**data,'files':checked,'verified_files':len(checked),'total_files':len(checked),
        'integrity_ok':True,'checked_at':datetime.now(timezone.utc).isoformat()}
