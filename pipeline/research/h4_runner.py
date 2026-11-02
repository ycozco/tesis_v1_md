"""Paired H4 orchestration. Evaluation keys never reach generator/retriever/verifier."""
from copy import deepcopy
from pipeline.research.h4_design import digest, require_execution_ready, CONFIGURATIONS


def apply_key_reviews(design,reviews):
    """Version explicit supplied human attestations; never infer them from outputs.

    This records declarations, not human identity verification or independent
    review. Agent-generated approval flags are not a substitute for a reviewer.
    """
    validate_design_integrity(design)
    indexed={row['case_id']:row for row in reviews}
    if len(reviews)!=30 or set(indexed)!={k['case_id'] for k in design['keys']}:
        raise ValueError('Thirty explicit case reviews required')
    result=deepcopy(design)
    from datetime import datetime
    for key in result['keys']:
        review=indexed[key['case_id']]
        if review.get('decision')!='approved' or not review.get('reviewer_id'):
            raise ValueError('Human approval and reviewer identity required')
        timestamp=datetime.fromisoformat(review['reviewed_at'].replace('Z','+00:00'))
        if timestamp.tzinfo is None:raise ValueError('Review timestamp needs timezone')
        key.update(review_status='reviewed',human_review=deepcopy(review))
    keys={k['case_id']:k for k in result['keys']}
    for case in result['cases']:case['key_sha256']=digest(keys[case['case_id']])
    for slot in result['schedule']:slot['key_sha256']=digest(keys[slot['case_id']])
    validate_design_integrity(result)
    return result


def validate_design_integrity(design):
    cases={c['case_id']:c for c in design['cases']}
    keys={k['case_id']:k for k in design['keys']}
    if len(cases)!=30 or len(keys)!=30 or set(cases)!=set(keys):raise ValueError('Exactly thirty complete cases required')
    products={c['product'] for c in cases.values()}
    if len(products)!=3 or any(sum(c['product']==p for c in cases.values())!=10 for p in products):raise ValueError('Ten cases per product required')
    for case_id,case in cases.items():
        if case['payload_sha256']!=digest(case['payload']) or case['key_sha256']!=digest(keys[case_id]):
            raise ValueError('Case or key hash mismatch')
    expected={(case_id,config,rep) for case_id in cases for config in CONFIGURATIONS for rep in (1,2,3)}
    slots={(r['case_id'],r['configuration'],r['repetition']) for r in design['schedule']}
    if len(design['schedule'])!=180 or slots!=expected:raise ValueError('Incomplete/duplicate paired schedule')
    for slot in design['schedule']:
        case=cases[slot['case_id']]
        if slot['payload_sha256']!=case['payload_sha256'] or slot['key_sha256']!=case['key_sha256']:
            raise ValueError('Schedule differs from frozen inputs')


def run_pairs(design,freeze,generate,retrieve,verify,*,technical_fixture=False,fallback=None,checkpoint=None):
    """Injected transports must use the exact frozen model/parameters in both arms.

    technical_fixture bypasses review only for deterministic test transport and
    never counts as LLM/H4 execution. Real execution fails closed before calls.
    verify(payload, documents, output) must return valid, issues, optional final.
    Any correction uses the same generator; all attempts/failures remain in trace.
    """
    validate_design_integrity(design)
    if technical_fixture:
        if freeze.get('generator_model')!='deterministic_test_transport':raise ValueError('Technical fixture requires explicit test transport')
    else:
        require_execution_ready(design,freeze)
        if any(not key.get('human_review',{}).get('reviewer_id') for key in design['keys']):raise ValueError('Explicit human key-review attestations required')
        if freeze.get('provider_id') not in ('ollama','deepseek'):raise ValueError('A real configured LLM provider is required')
        if freeze['corpus_sha256']!=digest(design['documents']):raise ValueError('Corpus differs from freeze')
        if freeze['prompt_sha256']!=digest(freeze['prompt']):raise ValueError('Prompt differs from freeze')
    cases={c['case_id']:c for c in design['cases']}
    traces=[]
    for slot in design['schedule']:
        case=cases[slot['case_id']]
        payload=deepcopy(case['payload'])
        trace={**deepcopy(slot),'product':case['product'],'scenario':case['scenario'],
            'execution_kind':'technical_fixture_not_H4_experiment' if technical_fixture else 'H4_experiment',
            'generator_model':freeze['generator_model'],'generator_version':freeze.get('generator_version'),
            'generation_parameters':deepcopy(freeze.get('generation_parameters')),
            'attempts':[],'retrieved_document_ids':[],'status':'not_executed','initial':None,
            'final':None,'fallback':False}
        try:
            full=slot['configuration']=='full_RAG_and_validation'
            documents=retrieve(deepcopy(payload),deepcopy(freeze)) if full else []
            trace['retrieved_document_ids']=[d['id'] for d in documents]
            correction=None
            for attempt in range(1+(int(freeze.get('correction_attempts',0)) if full else 0)):
                output=generate(deepcopy(payload),deepcopy(documents),deepcopy(freeze),deepcopy(correction))
                if attempt==0:trace['initial']=deepcopy(output)
                checked=verify(deepcopy(payload),deepcopy(documents),deepcopy(output)) if full else None
                trace['attempts'].append({'output':deepcopy(output),'verification':deepcopy(checked)})
                if not full or checked['valid']:
                    trace['final']=deepcopy(output);trace['status']='completed';break
                correction={'issues':checked.get('issues',[])}
            if trace['final'] is None:
                trace['status']='verification_failed';trace['final']=None
                if fallback is not None and freeze.get('fallback_policy')=='verified_template':
                    template=fallback(deepcopy(payload),deepcopy(documents),deepcopy(freeze))
                    checked=verify(deepcopy(payload),deepcopy(documents),deepcopy(template))
                    trace.update(fallback=True,fallback_output=deepcopy(template),fallback_verification=deepcopy(checked))
                    if checked['valid']:trace.update(final=deepcopy(template),status='completed_verified_fallback')
        except Exception as error:
            # Do not serialize provider exceptions/headers containing possible keys.
            trace['status']='execution_failed';trace['error_type']=type(error).__name__
        traces.append(trace)
        if checkpoint is not None:checkpoint(deepcopy(trace))
    return traces
