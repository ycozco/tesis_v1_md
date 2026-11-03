"""Audit existing historical eligibility; never infer missing certificates."""
import csv
import hashlib
import json
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'planificacion/2026-11-02/ejecucion'

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    path = ROOT / 'datasets/tratamiento/2026-11-01-expansion/panel-conservadora.parquet'
    panel = pd.read_parquet(path)
    rows = []
    for (product, destination), group in panel.groupby(['producto', 'destino'], sort=True):
        certified = group.coverage_certified.fillna(False).astype(bool)
        published = group.published_at.notna()
        eligible = group.eligible_historical_asof.fillna(False).astype(bool) & certified & published
        rows.append(dict(product=product, destination=destination, first_week=str(group.week.min().date()),
            last_week=str(group.week.max().date()), cells=len(group), observed_partial=int((group.coverage_state=='observed_partial').sum()),
            unknown=int((group.coverage_state=='unknown').sum()), coverage_certified=int(certified.sum()),
            publication_recorded=int(published.sum()), historical_eligible=int(eligible.sum()),
            status='requires_origin_calendar_review' if eligible.any() else 'blocked_no_certified_asof_cells'))
    with (OUT/'elegibilidad-series.csv').open('w', encoding='utf-8', newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    keys=json.loads((ROOT/'datasets/experimentos/h4-controlado-v1/keys.json').read_text(encoding='utf-8'))
    review=[]
    for key in keys:
        review.append(dict(case_id=key.get('case_id',key.get('id')),scenario=key.get('scenario'),
            current_review_status=key.get('review_status'),human_reviewer=None,reviewed_at=None,
            numeric_key_checked=False,documentary_key_checked=False,abstention_policy_accepted=False,
            decision='pending_human_review',notes=''))
    (OUT/'h4-revision-humana-pendiente.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    summary=dict(scope='audit_only_not_final_experiment',series=len(rows),panel_cells=len(panel),
        observed_partial=sum(r['observed_partial'] for r in rows),unknown=sum(r['unknown'] for r in rows),
        historical_eligible=sum(r['historical_eligible'] for r in rows),
        h4_review_cases=len(review),human_reviews_performed=0,paid_calls=0,final_outputs=0,
        panel_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        note='Recorded publication does not independently certify date validity; origin/calendar/selection review remains necessary even for eligible cells.')
    (OUT/'auditoria-elegibilidad.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary))
if __name__=='__main__': main()
