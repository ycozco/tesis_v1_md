from copy import deepcopy
from decimal import Decimal
import pytest
from pipeline.research.h4_design import (build_design, digest, require_execution_ready,
                                        PRODUCTS, SCENARIOS)


def test_thirty_controlled_cases_and_identical_paired_payloads():
    design = build_design()
    assert len(design['cases']) == 30
    assert len(design['schedule']) == 180
    assert {(c['product'], c['scenario']) for c in design['cases']} == {
        (p, s) for p in PRODUCTS for s in SCENARIOS}
    for case in design['cases']:
        runs = [r for r in design['schedule'] if r['case_id'] == case['case_id']]
        assert len(runs) == 6
        assert {r['payload_sha256'] for r in runs} == {digest(case['payload'])}
        assert all(r['output'] is None for r in runs)
        assert 'numeric' not in case['payload']


def test_period_difference_uses_unrounded_ratio_of_sums():
    keys = [k for k in build_design()['keys'] if k['scenario'] == 'period_difference']
    for key in keys:
        assert abs(Decimal(key['numeric']['relative_difference']['value'])-Decimal('12.5')) < Decimal('1e-20')
        assert Decimal(key['numeric']['next_unit_fob']['value']) == 3


def test_unsafe_cases_have_explicit_acceptable_abstentions():
    design = build_design()
    for key in design['keys']:
        assert set(key['required_elements']) == set(key['numeric']) | set(key['factual']) | set(key['required_abstentions'])
        if key['scenario'] in {'zero_denominator', 'unpublished_data', 'incompatible_units', 'incompatible_commercial_level'}:
            assert 'unit_fob' not in key['numeric']
            assert key['required_abstentions'] == ['unit_fob']


def test_execution_gate_rejects_unreviewed_keys_missing_freeze_and_tampering():
    design = build_design()
    with pytest.raises(ValueError, match='human review'):
        require_execution_ready(design, {})
    for key in design['keys']:
        key['review_status'] = 'reviewed'
    with pytest.raises(ValueError, match='Missing experimental freeze'):
        require_execution_ready(design, {})
    freeze = {name: 'fixed-for-unit-test-only' for name in (
        'generator_model', 'generator_version', 'generation_parameters', 'prompt_sha256',
        'corpus_sha256', 'chunking', 'embedding_model_version', 'retrieval_top_k',
        'retrieval_thresholds', 'temporal_filters', 'correction_attempts')}
    freeze['design_sha256'] = digest(design)
    assert require_execution_ready(design, freeze)
    tampered = deepcopy(design)
    tampered['cases'][0]['payload']['request'] += ' changed'
    with pytest.raises(ValueError, match='differs'):
        require_execution_ready(tampered, freeze)
