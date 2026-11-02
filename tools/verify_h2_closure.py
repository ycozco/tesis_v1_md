"""Independently verify H2 closure, evidence hashes and complete audit matrix."""
import csv
import hashlib
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'datasets/experimentos/h2-cierre-2026-11-01'


def main():
    decision=json.loads((BASE/'decision.json').read_text(encoding='utf-8'))
    inventory=json.loads((BASE/'source-inventory.json').read_text(encoding='utf-8'))
    assert {row['source'] for row in inventory}=={'BCRP','SISAP','NASA_POWER','Comtrade'}
    assert sum(row['verified_eligible_rows'] for row in inventory)==0
    for name,expected in decision['evidence_sha256'].items():
        artifact=(ROOT/name).resolve()
        assert artifact.is_relative_to(ROOT)
        assert hashlib.sha256(artifact.read_bytes()).hexdigest()==expected,name
    with (BASE/'origin-eligibility.csv').open(encoding='utf-8',newline='') as handle:
        matrix=list(csv.DictReader(handle))
    with (ROOT/'datasets/tratamiento/2026-11-01-expansion/calendario-provisional.csv').open(encoding='utf-8',newline='') as handle:
        calendar=list(csv.DictReader(handle))
    expected=set(itertools.product((row['emission'] for row in calendar),('0','4','8'),
                                    ('unit_fob','volume_kg'),('BCRP','SISAP','NASA_POWER','Comtrade')))
    actual={(row['emission_date'],row['L'],row['target'],row['source']) for row in matrix}
    assert len(matrix)==len(actual)==len(expected)==1248 and actual==expected
    assert all(row['verified_context_rows']==row['verified_target_rows']==row['eligible_paired_cases']=='0' for row in matrix)
    assert decision['status']=='closed_not_evaluable_current_release'
    assert decision['supports_h2'] is decision['refutes_h2'] is decision['metrics'] is None
    assert not decision['ablation_executed'] and decision['models_fitted']==0
    report={'status':'passed','source_families_audited':4,'calendar_origins':52,
        'matrix_cells_verified':1248,'evidence_files_verified':len(decision['evidence_sha256']),
        'eligible_paired_cases':0,'hypothesis_result':'not_evaluable_not_supported_or_refuted',
        'final_test_predictions_generated':0,'review_scope':'exact current release, not a claim that all possible public sources are unavailable'}
    (BASE/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
