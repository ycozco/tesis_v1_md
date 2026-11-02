from copy import deepcopy
import pytest
from pipeline.research.h4_design import build_design
from pipeline.research.h4_runner import run_pairs,apply_key_reviews,validate_design_integrity
from pipeline.research.h4_evaluation import grade_output,aggregate_paired
from pipeline.research.h4_blind import blind_packet,require_repeat_delay,agreement


def transports():
    design=build_design();calls=[]
    def generate(payload,documents,freeze,correction):
        assert 'keys' not in payload and 'numeric' not in payload
        calls.append((deepcopy(payload),deepcopy(freeze['generation_parameters'])))
        return {'numeric_claims':[],'factual_claims':[],'abstentions':[]}
    freeze={'generator_model':'deterministic_test_transport','generator_version':'fixture-v1',
            'generation_parameters':{'temperature':0},'correction_attempts':0}
    return design,calls,generate,freeze


def test_real_runner_blocks_unreviewed_design_before_any_provider_call():
    design,calls,generate,freeze=transports()
    with pytest.raises(ValueError,match='human review'):
        run_pairs(design,freeze,generate,lambda p,f:[],lambda p,d,o:{'valid':True})
    assert calls==[]


def test_180_technical_traces_share_inputs_and_do_not_leak_keys():
    design,calls,generate,freeze=transports();checkpoints=[]
    traces=run_pairs(design,freeze,generate,lambda p,f:[],lambda p,d,o:{'valid':True},
                     technical_fixture=True,checkpoint=checkpoints.append)
    assert len(traces)==len(calls)==len(checkpoints)==180
    assert all(t['execution_kind']=='technical_fixture_not_H4_experiment' for t in traces)
    for case in design['cases']:
        assert sum(payload==case['payload'] for payload,_ in calls)==6
    packet=blind_packet(traces,{c['case_id']:c['payload'] for c in design['cases']})
    assert len(packet['second_review_ids'])==45
    assert sorted(packet['stratum_counts'].values())==[7,7,7,8,8,8]
    assert all('configuration' not in row for row in packet['public'])
    alternate=blind_packet(traces,{c['case_id']:c['payload'] for c in design['cases']},private_blind_seed=123)
    selected=lambda p:{(r['case_id'],r['configuration'],r['repetition']) for r in p['private_mapping_keep_hidden'] if r['second_review_selected']}
    assert selected(alternate)==selected(packet)


def test_correction_and_verified_fallback_are_retained():
    design,calls,generate,freeze=transports()
    freeze.update(correction_attempts=1,fallback_policy='verified_template')
    traces=run_pairs(design,freeze,generate,lambda p,f:[],
        lambda p,d,o:{'valid':o.get('template',False),'issues':['bad_fixture']},technical_fixture=True,
        fallback=lambda p,d,f:{'template':True})
    full=[r for r in traces if r['configuration']=='full_RAG_and_validation']
    assert len(calls)==270
    assert all(len(r['attempts'])==2 and r['fallback'] and r['fallback_verification']['valid'] for r in full)


def test_numeric_key_precision_cannot_be_relaxed_by_generated_claim():
    key=build_design()['keys'][0]
    output={'numeric_claims':[{'element_id':'unit_fob','value':3,'unit':'USD/kg','decimals':0}],
            'factual_claims':[],'abstentions':[]}
    with pytest.raises(ValueError,match='atomization'):
        grade_output(output,key,{})
    grade=grade_output(output,key,{'atomization_reviewed':True,
        'atoms':[{'claim_id':'number-0','element_id':'unit_fob','numeric_index':0}],
        'claims':{'number-0':{'supported':False}}})
    assert grade['numeric_error_rate']==1 and grade['factual_error_rate']==1
    empty=grade_output({},key,{'atomization_reviewed':True,'claims':{}})
    assert empty['numeric_error_rate'] is empty['factual_error_rate'] is None


def test_conflicting_claim_cannot_be_hidden_by_simultaneous_abstention():
    key=next(k for k in build_design()['keys'] if k['scenario']=='unsupported_causal_request')
    output={'numeric_claims':[],'factual_claims':[{'claim_id':'a','element_id':'causal_claim'}],
            'abstentions':['causal_claim']}
    result=grade_output(output,key,{'atomization_reviewed':True,'claims':{'a':{'supported':False}}})
    assert result['coverage']==0


def test_macro_averages_repetitions_inside_case_and_keeps_undefined_rates():
    grades=[]
    for i in range(30):
        for config in ('reference_no_retrieval_no_validation','full_RAG_and_validation'):
            for repetition in (1,2,3):grades.append({'case_id':str(i),'configuration':config,
                'repetition':repetition,'numeric_error_rate':.5 if config.startswith('reference') else .1,
                'factual_error_rate':.5 if config.startswith('reference') else .1,'coverage':1.})
    result=aggregate_paired(grades)
    assert result['status']=='descriptively_supported' and result['case_count']==30
    grades[0]['numeric_error_rate']=None
    assert aggregate_paired(grades)['status']=='not_conclusive_undefined_primary_rates'


def test_agreement_requires_identical_atoms_and_repeat_is_delayed_seven_days():
    ratings={('B001','a'):True,('B001','b'):True}
    result=agreement(ratings,ratings)
    assert result['agreement']==1 and result['kappa'] is None and result['outputs']==1
    with pytest.raises(ValueError,match='seven days'):
        require_repeat_delay('2026-11-01T00:00:00Z','2026-11-07T00:00:00Z')
    require_repeat_delay('2026-11-01T00:00:00Z','2026-11-08T00:00:00Z')


def test_supplied_review_fixture_rehashes_all_references_without_modifying_original():
    design=build_design()
    reviews=[{'case_id':key['case_id'],'reviewer_id':'artificial-unit-test-reviewer-not-a-human-review',
              'decision':'approved','reviewed_at':'2026-11-01T00:00:00Z'} for key in design['keys']]
    reviewed=apply_key_reviews(design,reviews)
    validate_design_integrity(reviewed)
    assert all(k['review_status']=='awaiting_human_review' for k in design['keys'])
    assert reviewed['cases'][0]['key_sha256']!=design['cases'][0]['key_sha256']
    with pytest.raises(ValueError,match='Thirty'):
        apply_key_reviews(design,reviews[:29])


def test_numbers_cannot_be_hidden_from_factual_atom_denominator():
    key=build_design()['keys'][0]
    output={'numeric_claims':[{'element_id':'unsupported_number','value':99,'unit':'USD'}]}
    with pytest.raises(ValueError,match='numeric assertion'):
        grade_output(output,key,{'atomization_reviewed':True,'claims':{}})
