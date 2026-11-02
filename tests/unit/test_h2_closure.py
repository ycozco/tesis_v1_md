import pytest
from pipeline.research.h2 import decide_h2


def test_thesis_non_evaluable_is_not_a_negative_result():
    result=decide_h2([{'verified_eligible_rows':0}],0,0)
    assert result['status']=='closed_not_evaluable_current_release'
    assert result['supports_h2'] is result['refutes_h2'] is result['metrics'] is None
    assert not result['ablation_executed']


def test_one_eligible_context_is_enough_but_requires_common_target_cases():
    sources=[{'verified_eligible_rows':10},{'verified_eligible_rows':0}]
    assert decide_h2(sources,0,0)['status']=='closed_not_evaluable_current_release'
    assert decide_h2(sources,10,10)['status']=='requires_protocol_freeze_and_development_selection'
    assert decide_h2(sources,10,10,True)['status']=='ready_for_paired_ablation_not_executed'


def test_protocol_approval_cannot_override_missing_observations():
    assert decide_h2([{'verified_eligible_rows':0}],100,0,True)['status']=='closed_not_evaluable_current_release'


def test_audited_inventory_required_and_negative_counts_rejected():
    with pytest.raises(ValueError):decide_h2([],1,1)
    with pytest.raises(ValueError):decide_h2([{'verified_eligible_rows':1}],-1,1)
