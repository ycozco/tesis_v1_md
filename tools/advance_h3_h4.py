"""Exercise integrated H3 and H4 software on explicitly artificial fixtures.

Preserves existing historical pilots. Does not call an LLM, spend API credit,
fabricate human grading or turn missing historical publication into eligibility.
"""
from datetime import date,datetime,timedelta,timezone
from decimal import Decimal,ROUND_HALF_UP
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ['MPLCONFIGDIR']=str(ROOT/'data/runtime-research-clean/matplotlib-cache')


def main():
    import numpy as np
    import pandas as pd
    import requests
    from pipeline.research.h3_engine import score_origin,common_budget_analysis
    from pipeline.research.h3_rules import persistence_label
    from pipeline.research.h4_design import digest
    from pipeline.research.h4_runner import run_pairs
    from pipeline.research.h4_blind import blind_packet
    out=ROOT/'datasets/experimentos/h3-h4-integracion-2026-11-01'
    out.mkdir(parents=True,exist_ok=True)
    private=ROOT/'data/h4-technical-fixture';private.mkdir(parents=True,exist_ok=True)
    def save(name,value):
        (out/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    import inspect
    import importlib.metadata as metadata
    from pyod.models.ecod import ECOD
    source=inspect.getsource(ECOD.decision_function)
    save('ecod-source-inspection.json',{'installed_package_version':metadata.version('pyod'),
        'source_file_sha256':hashlib.sha256(Path(inspect.getsourcefile(ECOD)).read_bytes()).hexdigest(),
        'appends_training_and_new_batch':'np.concatenate((self.X_train, X)' in source,
        'official_source_url':'https://pyod.readthedocs.io/en/latest/_modules/pyod/models/ecod.html',
        'historical_protocol_review_of_inductive_adaptation_required':True})
    rng=np.random.default_rng(42);base=date(2020,1,6);rubric_records=[]
    features=['residual_unit_fob','residual_volume','relative_change52','unit_fob']
    products=('palta','uva','arandano');history=[];scored=[];audits=[];injections=[]
    labels={str(t):{} for t in (.1,.2,.3)}
    for product in products:
        for week_number in range(40,100):
            for destination in range(3):
                week=base+timedelta(weeks=week_number)
                values=rng.normal(size=4)
                values[2]=.02*np.tanh(values[2]);values[3]=3.+.2*np.tanh(values[3])
                history.append({'id':f'train-{product}-{week_number}-{destination}',
                    'product':product,'destination':f'TEST-{destination:02}','week':week.isoformat(),
                    'available_at':f'{week+timedelta(weeks=1)}T00:00:00Z',
                    'forecast_is_oos':True,'data_kind':'artificial','features':dict(zip(features,values.tolist()))})
    for week_number in (100,101,102):
        for product in products:
            current=[];week=base+timedelta(weeks=week_number)
            for destination in range(21):
                values=rng.normal(size=4);persistent=destination<5
                if persistent:values[:2]+=8
                values[2]=.25 if persistent else .02;values[3]=3.75 if persistent else 3.06
                case_id=f'artificial-{product}-{week_number}-{destination}'
                row={'id':case_id,'product':product,'destination':f'TEST-{destination:02}',
                    'week':week.isoformat(),'available_at':f'{week+timedelta(weeks=1)}T00:00:00Z',
                    'forecast_is_oos':True,'data_kind':'artificial','features':dict(zip(features,values.tolist()))}
                current.append(row)
                observations={}
                for offset in (0,1,2):
                    w=week+timedelta(weeks=offset)
                    observations[w]={'value':125. if persistent else 102.,'coverage_state':'observed_certified'}
                    observations[w-timedelta(weeks=52)]={'value':100.,'coverage_state':'observed_certified'}
                for threshold in (.1,.2,.3):
                    labels[str(threshold)][case_id]=persistence_label(week,observations,base+timedelta(weeks=104),threshold)
                rubric_records.append({'id':case_id,'week':week.isoformat(),'test_end':str(base+timedelta(weeks=104)),
                    'observations':[{'week':str(w),**value} for w,value in sorted(observations.items())]})
                if persistent:injections.append({'id':case_id,'kind':'artificial_residual_shift_and_persistent_25pct','residual_shift':8,'seed':42})
            result=score_origin(history,current,f'{week+timedelta(weeks=1)}T00:00:00Z',features)
            scored+=result['rows'];audits.append(result['audit']);history+=current
    analysis=common_budget_analysis(scored,labels)
    save('h3-artificial-scores.json',scored);save('h3-training-audit.json',audits)
    save('h3-artificial-analysis.json',analysis);save('h3-artificial-injections.json',injections)
    save('h3-artificial-labels.json',labels);save('h3-artificial-rubric-inputs.json',rubric_records)
    panel_path=ROOT/'datasets/tratamiento/2026-11-01-expansion/panel-conservadora.parquet'
    panel=pd.read_parquet(panel_path,columns=['coverage_certified','published_at','eligible_historical_asof'])
    assert not panel.coverage_certified.any() and panel.published_at.isna().all() and not panel.eligible_historical_asof.any()
    save('historical-h3-gate.json',{'status':'not_executed_missing_eligible_final_forecasts_and_coverage',
        'panel_sha256':hashlib.sha256(panel_path.read_bytes()).hexdigest(),'cells_audited':len(panel),
        'eligible_historical_cells':0,'historical_final_scores_generated':0,
        'reason':'Final H1 forecasts are not selected/executed; coverage and publication remain unverified.'})
    design={name:json.loads((ROOT/f'datasets/experimentos/h4-controlado-v1/{name}.json').read_text(encoding='utf-8'))
            for name in ('cases','keys','documents','schedule')}
    freeze={'generator_model':'deterministic_test_transport','generator_version':'artificial-transport-v1',
        'generation_parameters':{'temperature':0},'correction_attempts':0,'fallback_policy':'none',
        'retrieval_kind':'exact_document_id_fixture_lookup_not_pgvector_RAG'}
    generator_calls=0
    def generate(payload,documents,settings,correction):
        nonlocal generator_calls
        generator_calls+=1
        data=payload['structured_data'];denominator=sum(Decimal(r['net_weight']) for r in data['operations'])
        scope='complete_fixture_customs_export';abstain=[];numeric=[]
        if data['commercial_level']!='customs_export':scope='incompatible_commercial_level'
        elif data['weight_unit']!='kg':scope='incompatible_units'
        elif data['published_at']>data['origin']:scope='unpublished_at_origin'
        elif denominator==0:scope='undefined_zero_denominator'
        elif data['coverage']=='incomplete':scope='partial_recovered_operations_only'
        def number(element,value,unit):
            numeric.append({'element_id':element,'value':str(value.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)),'unit':unit})
        if scope in ('incompatible_commercial_level','incompatible_units','unpublished_at_origin','undefined_zero_denominator'):
            abstain.append('unit_fob')
        else:
            before=sum(Decimal(r['fob']) for r in data['operations'])/denominator
            number('unit_fob',before,'USD/kg')
            if 'next_period' in data:
                after=Decimal(data['next_period']['fob'])/Decimal(data['next_period']['net_weight'])
                number('next_unit_fob',after,'USD/kg');number('absolute_difference',after-before,'USD/kg')
                number('relative_difference',100*(after-before)/before,'%')
        if 'rentable' in payload['request']:abstain.append('profitability_claim')
        if 'causalmente' in payload['request']:abstain.append('causal_claim')
        return {'numeric_claims':numeric,'factual_claims':[
            {'claim_id':'scope','element_id':'scope','value':scope},
            {'claim_id':'definition','element_id':'definition','value':data['definition_notice']['current_document_id']}],
            'abstentions':abstain,'text':''}
    def retrieve(payload,settings):
        # Exact ID is intentional for transport tests; no dense RAG is claimed.
        return [d for d in design['documents'] if d['id']==payload['structured_data']['definition_notice']['current_document_id']]
    def verify(payload,documents,output):
        return {'valid':isinstance(output,dict) and set(output)=={'numeric_claims','factual_claims','abstentions','text'},
                'issues':[],'scope':'technical_schema_check_only_not_factual_grading'}
    checkpoint=private/'technical-traces.jsonl'
    with checkpoint.open('w',encoding='utf-8') as handle:
        traces=run_pairs(design,freeze,generate,retrieve,verify,technical_fixture=True,
                         checkpoint=lambda trace:handle.write(json.dumps(trace,ensure_ascii=False)+'\n'))
    packet=blind_packet(traces,{c['case_id']:c['payload'] for c in design['cases']})
    (private/'private-blind-mapping.json').write_text(json.dumps(packet.pop('private_mapping_keep_hidden'),indent=2)+'\n',encoding='utf-8')
    save('h4-blind-technical-fixture.json',packet)
    save('h4-review-checklist.json',{'human_key_reviews_completed':0,'required':30,
        'keys_file':'datasets/experimentos/h4-controlado-v1/keys.json',
        'pending_before_generation':['Review keys and abstention coverage policy',
            'Review undefined-rate aggregation policy before results are seen',
            'Freeze actual generator/version, prompt, corpus, embeddings, retrieval and attempts',
            'Configure actual Ollama or explicitly authorized paid provider'],
        'pending_after_generation':['Blindly atomize and grade all factual claims',
            'Second-grade 45 stratified outputs independently or intra-rater after seven days',
            'Report pre-adjudication agreement and kappa only if calculable']})
    try:
        response=requests.get('http://127.0.0.1:11434/api/tags',timeout=3)
        local={'http_status':response.status_code,'models':[r['name'] for r in response.json().get('models',[])]}
    except (requests.RequestException,ValueError):local={'available':False,'models':[]}
    try:
        docker=subprocess.run(['docker','info','--format','{{.ServerVersion}}'],capture_output=True,text=True,timeout=5)
        docker_ready=docker.returncode==0
    except (OSError,subprocess.TimeoutExpired):docker_ready=False
    save('runtime-readiness.json',{'ollama':local,'docker_daemon_available':docker_ready,
        'PostgreSQL_pgvector_validated':False,'paid_provider_called':False})
    summary={'H3_historical_status':'not_executed_missing_eligible_final_forecasts_and_coverage',
        'H3_artificial_cases_scored':len(scored),'H3_training_origins':len(audits),'H3_methods':5,
        'H3_ECOD':'inductive frozen-training adaptation, not unchanged PyOD transductive scoring',
        'H4_status':'not_executed_as_LLM_experiment','H4_technical_fixture_traces':len(traces),
        'H4_deterministic_transport_calls':generator_calls,'H4_LLM_outputs_generated':0,
        'H4_final_human_fact_reviews':0,'H4_second_review_sample_prepared':len(packet['second_review_ids']),
        'historical_final_test_executed':False,'paid_provider_calls':0}
    save('summary.json',summary);print(json.dumps(summary))


if __name__=='__main__':main()
