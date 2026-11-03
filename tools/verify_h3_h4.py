"""Independent checks of artificial H3/H4 artifacts; no producer imports."""
from datetime import date,timedelta
from decimal import Decimal
import hashlib
import itertools
import json
from math import ceil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'datasets/experimentos/h3-h4-integracion-2026-11-01'


def main():
    import argparse
    global OUT
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-date', default='2026-11-01', choices=['2026-11-01','2026-11-02'])
    args=parser.parse_args()
    OUT=ROOT/f'datasets/experimentos/h3-h4-integracion-{args.run_date}'
    def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
    scores=read('h3-artificial-scores.json');analysis=read('h3-artificial-analysis.json')
    labels=read('h3-artificial-labels.json');rubrics=read('h3-artificial-rubric-inputs.json')
    assert len(scores)==len({r['id'] for r in scores})==189
    for row in scores:
        values=list(row['percentiles'].values())
        assert len(values)==3 and all(0<=value<=1 for value in values)
        assert abs(row['ensemble']-sum(values)/3)<1e-14
    for audit in read('h3-training-audit.json'):
        assert audit['latest_training_week']<audit['week'] and audit['training_rows']>=40
        assert len(audit['scaler_mean'])==len(audit['features'])==4
    for method,products in analysis['selections'].items():
        for product,selected in products.items():
            rows=[r for r in scores if r['product']==product]
            assert len(selected)==max(1,ceil(.05*len(rows)))==4
            value=lambda r:r['percentiles'][method] if method in ('IF','LOF','ECOD') else r[method]
            expected=[r['id'] for r in sorted(rows,key=lambda r:(-value(r),r['week'],r['destination'],r['id']))[:4]]
            assert selected==expected
    for row in rubrics:
        week=date.fromisoformat(row['week']);end=date.fromisoformat(row['test_end'])
        assert week+timedelta(weeks=2)<=end
        observations={date.fromisoformat(v['week']):v for v in row['observations']}
        changes=[]
        for offset in (0,1,2):
            w=week+timedelta(weeks=offset)
            before=observations[w-timedelta(weeks=52)];after=observations[w]
            assert before['coverage_state']==after['coverage_state']=='observed_certified'
            changes.append((Decimal(str(after['value']))-Decimal(str(before['value'])))/Decimal(str(before['value'])))
        for threshold in ('0.1','0.2','0.3'):
            limit=Decimal(threshold)
            positive=all(c>=limit for c in changes) or all(c<=-limit for c in changes)
            assert labels[threshold][row['id']]==('positive' if positive else 'negative')
    for row in analysis['summaries']:
        assert row['q']+row['r']+row['u']==row['K']==4
        selected=analysis['selections'][row['method']][row['product']]
        actual=[labels[row['threshold']][case] for case in selected]
        assert row['q']==actual.count('positive') and row['r']==actual.count('negative')
    for row in analysis['overlaps']:
        a=set(analysis['selections'][row['left']][row['product']]);b=set(analysis['selections'][row['right']][row['product']])
        assert row['intersection']==len(a&b) and row['union']==len(a|b)
    packet=read('h4-blind-technical-fixture.json')
    assert len(packet['public'])==180 and len({r['blind_id'] for r in packet['public']})==180
    assert len(set(packet['second_review_ids']))==45
    assert set(packet['second_review_ids'])<={r['blind_id'] for r in packet['public']}
    assert sorted(packet['stratum_counts'].values())==[7,7,7,8,8,8]
    assert all('configuration' not in r and r['factual_review'] is None for r in packet['public'])
    assert all(r['execution_kind']=='technical_fixture_not_H4_experiment' for r in packet['public'])
    summary=read('summary.json')
    assert summary['H4_LLM_outputs_generated']==summary['H4_final_human_fact_reviews']==summary['paid_provider_calls']==0
    gate=read('historical-h3-gate.json')
    panel=ROOT/'datasets/tratamiento/2026-11-01-expansion/panel-conservadora.parquet'
    assert hashlib.sha256(panel.read_bytes()).hexdigest()==gate['panel_sha256']
    assert gate['eligible_historical_cells']==gate['historical_final_scores_generated']==0
    result={'status':'passed','H3_artificial_scores_verified':189,'H3_budget':4,'H3_methods':5,
        'H3_sensitivities_verified':3,'H4_technical_packet_rows':180,'H4_second_review_sample':45,
        'actual_LLM_outputs':0,'historical_final_H3_scores':0,'human_reviews_performed':0}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
