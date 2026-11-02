"""Independent audit of saved BCRP reconciliation; does not import its producer."""
import csv
from datetime import date
from decimal import Decimal
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'datasets/contexto/h2-bcrp-2026-11-01'


def main():
    def read(name):
        return json.loads((BASE/name).read_text(encoding='utf-8'))
    failures=[]
    hashes=read('hashes.json')
    for name, expected in hashes.items():
        if hashlib.sha256((BASE/name).read_bytes()).hexdigest()!=expected:
            failures.append('artifact_hash_mismatch:'+name)
    source=ROOT/'datasets/tratamiento/2026-11-01/bcrp-mensual-conciliado.csv'
    with source.open(encoding='utf-8',newline='') as handle:
        rows=list(csv.DictReader(handle))
    local={r['month']:r for r in rows}
    assert len(local)==len(rows)==102
    data=read('documentary-candidates.json')
    documents={d['id']:d for d in data['documents']}
    candidates=data['observations']
    comparisons={(r['document_id'],r['month']):r for r in read('reconciliation.json')}
    expected_periods={f'2025-{i:02}' for i in range(1,13)}|{f'2026-{i:02}' for i in range(1,5)}
    seen=set(); differences=[]
    for row in candidates:
        key=(row['document_id'],row['month'])
        assert key not in seen
        seen.add(key)
        document=documents[row['document_id']]
        assert row['document_date']==document['document_date']
        assert row['month'] in expected_periods
        assert not row['eligible_asof'] and row['verified_available_at'] is None
        assert not document['original_pdf_verified']
        assert row['month'] < document['document_date'][:7]
        actual=Decimal(local[row['month']]['pen_per_usd'])
        printed=Decimal(row['value'])
        assert actual.is_finite() and printed.is_finite()
        difference=abs(actual-printed)
        assert difference<=Decimal('0.000500001')
        assert Decimal(comparisons[key]['absolute_difference'])==difference
        assert comparisons[key]['status']=='matches_printed_precision'
        differences.append(difference)
    for doc in documents:
        assert {r['month'] for r in candidates if r['document_id']==doc}==expected_periods
    assert len(seen)==len(comparisons)==32
    retrieval=read('retrieval-manifest.json');body_checks=0
    for entry in retrieval:
        path=(ROOT/entry['file']).resolve()
        assert path.is_relative_to((ROOT/'data/h2-bcrp-retrieval').resolve())
        if path.is_file():
            body=path.read_bytes()
            assert len(body)==entry['bytes']
            assert hashlib.sha256(body).hexdigest()==entry['sha256']
            assert not body.startswith(b'%PDF-')
            body_checks+=1
    summary=read('summary.json')
    assert summary['local_source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
    assert summary['candidate_eligible_asof_rows']==0 and not summary['h2_ablation_executed']
    report={'status':'passed_with_original_document_verification_pending' if not failures else 'failed',
            'artifact_hash_failures':failures,'local_months':102,'candidate_comparisons':32,
            'independent_months':16,'document_count':2,'max_absolute_difference':str(max(differences)),
            'retrieved_response_bodies_verified':body_checks,'retrieved_response_count':len(retrieval),
            'original_pdfs_verified':0,'eligible_context_rows':0,
            'evidence_limitation':'Two manual indexed transcriptions; not independent original-PDF extraction or complete historical publication evidence',
            'source_backup_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
    (BASE/'independent-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
    if failures:raise SystemExit(1)


if __name__=='__main__':main()
