"""Exploratory past-residual detector pilot and unexecuted paired H4 case pack."""
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.ecod import ECOD
from rank_bm25 import BM25Okapi

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.research.protocol import top_budget
OUT = ROOT / 'datasets/tratamiento/2026-11-01'


def main():
    predictions = pd.read_parquet(OUT / 'predicciones-desarrollo-piloto.parquet')
    summary = json.loads((OUT / 'piloto-resumen.json').read_text())
    normalized = []
    for target in ['unit_fob', 'volume_kg']:
        method = summary['selection_development_only'][f'conservadora|0|{target}']
        rows = predictions[(predictions.view == 'conservadora') & (predictions.L == 0)
                           & (predictions.target == target) & (predictions.method == method)].copy()
        rows['residual'] = rows.actual - rows.prediction
        for _, series in rows.groupby(['producto','destino']):
            prior = []
            for row in series.sort_values('emission').itertuples():
                if len(prior) >= 8:
                    median = float(np.median(prior))
                    mad = float(np.median(np.abs(np.asarray(prior)-median)))
                    if mad > 0:
                        normalized.append({'target':target,'producto':row.producto,'destino':row.destino,
                            'emission':row.emission,'z':(row.residual-median)/(1.4826*mad),
                            'prior_residuals':len(prior)})
                prior.append(row.residual)
    normalized = pd.DataFrame(normalized)
    scored, overlaps = [], []
    if not normalized.empty:
        for target, rows in normalized.groupby('target'):
            for emission, current in rows.groupby('emission'):
                prior = rows[rows.emission < emission]
                if len(prior) < 30:
                    continue
                train = prior[['z']].to_numpy()
                sample = current[['z']].to_numpy()
                models = {'IF':IForest(n_estimators=50, random_state=42, n_jobs=1),
                          'LOF':LOF(n_neighbors=min(20,len(train)-1), n_jobs=1), 'ECOD':ECOD(n_jobs=1)}
                scores = {}
                for name, model in models.items():
                    model.fit(train)
                    scores[name] = model.decision_function(sample)
                # Rank ensemble, not arithmetic average of incomparable detector scales.
                scores['ensemble_rank'] = np.mean([pd.Series(v).rank(pct=True).to_numpy() for v in scores.values()], axis=0)
                scores['residual_reference'] = np.abs(sample[:,0])
                sets = {name:top_budget(values) for name,values in scores.items()}
                for i, row in enumerate(current.itertuples()):
                    item = {'target':target,'emission':str(emission),'producto':row.producto,'destino':row.destino,
                        'z':row.z, 'train_prior_residuals':len(train), 'common_candidates':len(current),
                        'K':math.ceil(.05*len(current)), 'scope':'exploratory_development_selected_model'}
                    for name, values in scores.items():
                        item[name] = float(values[i]); item[name+'_selected'] = i in sets[name]
                    scored.append(item)
                for left in sets:
                    for right in sets:
                        if left >= right: continue
                        intersection, union = sets[left]&sets[right], sets[left]|sets[right]
                        overlaps.append({'target':target,'emission':str(emission),'left':left,'right':right,
                            'intersection':len(intersection), 'jaccard':len(intersection)/len(union) if union else None})
    pd.DataFrame(scored).to_csv(OUT/'h3-scores-piloto.csv', index=False)
    pd.DataFrame(overlaps).to_csv(OUT/'h3-solapamientos-piloto.csv', index=False)
    # Real aggregate evidence; no synthetic observations and no generated report outputs.
    panel = pd.read_parquet(OUT/'panel-conservadora.parquet').dropna(subset=['unit_fob'])
    cases, schedule = [], []
    source_hash = json.loads((OUT/'manifest.json').read_text())['views']['conservadora']['input_sha256']
    for product, rows in panel.groupby('producto'):
        rows = rows.sort_values(['week','destino'])
        indices = np.linspace(0, len(rows)-1, 10, dtype=int)
        for position, index in enumerate(indices, 1):
            row = rows.iloc[index]
            case_id = f'{product}-{position:02}'
            source_id = f'{product}|{row.destino}|{row.week.date()}'
            facts = {f'{case_id}.{field}':{'value':float(row[field]), 'unit':unit, 'source_id':source_id}
                     for field,unit in [('unit_fob','USD/kg'),('volume_kg','kg'),('fob_usd','USD')]}
            cases.append({'case_id':case_id, 'producto':product,'destino':row.destino,'week':str(row.week.date()),
                'evidence':facts,'source_sha256':source_hash,
                'evaluation_status':'prepared_not_executed', 'numeric_decimals':2,
                'manual_reference_status':'awaiting_blinded_factual_key_review'})
            for config in ['reference_no_retrieval_no_validation','full_RAG_and_validation']:
                for repetition in (1,2,3):
                    schedule.append({'case_id':case_id,'configuration':config,'run':repetition,
                        'status':'not_executed','output':None,'numeric_error':None,'factual_error':None})
    (OUT/'h4-casos-30.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
    (OUT/'h4-plan-180.json').write_text(json.dumps(schedule,indent=2),encoding='utf-8')
    # Real local lexical retrieval check. Dense model and persistent pgvector are NOT claimed.
    documents = []
    for file in [ROOT/'datasets/fuentes/2026-10-31/README.md',
                 ROOT/'datasets/fuentes/2026-10-31/conciliacion/informe.md',
                 ROOT/'datasets/fuentes/2026-10-31/conciliacion/resolucion-analitica/informe-resolucion.md']:
        if file.exists():
            documents.extend({'source':str(file.relative_to(ROOT)), 'text':chunk,
                'sha256':hashlib.sha256(chunk.encode()).hexdigest()} for chunk in file.read_text(encoding='utf-8').split('\n\n') if len(chunk)>80)
    tokens = [d['text'].lower().split() for d in documents]
    scores = BM25Okapi(tokens).get_scores('conciliación cuarentena conflictos'.lower().split())
    retrieval = [documents[i] | {'score':float(scores[i])} for i in np.argsort(scores)[-3:][::-1]]
    (OUT/'rag-recuperacion-lexica-prueba.json').write_text(json.dumps(retrieval,indent=2,ensure_ascii=False),encoding='utf-8')
    result = {'h3_scored_cases':len(scored), 'h3_overlap_rows':len(overlaps),
        'h3_limitations':['minimum 8 prior errors is pilot-only', 'development model selection bias',
                          'seasonal baseline and persistence characterization remain pending',
                          'current revised values cannot certify operational as-of signals', 'no anomaly ground truth'],
        'h4_cases_prepared':len(cases),'h4_slots_prepared':len(schedule),'h4_outputs_generated':0,
        'retrieval':'BM25 local corpus query exercised; no dense embeddings/pgvector test',
        'h4_pending':['review factual keys and case difficulty', 'freeze generator/model/prompt/corpus',
                      'execute 180 paired outputs', 'blind factual evaluation', 'separate errors/abstention/coverage']}
    (OUT/'h3-h4-resumen.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__': main()
