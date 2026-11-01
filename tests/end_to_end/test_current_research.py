"""Current E1–E3 component integrations with explicit artificial observations.

These are technical checks, not historical experimental outputs or UI evidence.
"""
from datetime import datetime, timedelta, timezone
import json
import pandas as pd
import pytest
from pipeline.research.protocol import weekly_panel
from pipeline.research.evidence import verify_atomic_claim
from pipeline.research.temporal_ledger import ResidualLedger
from pipeline.research.h4_design import build_design, require_execution_ready


def test_e1_ratio_of_sums_period_difference_and_claim_validation():
    rows = pd.DataFrame({'id_declaracion_serie_sha256':['fixture-a','fixture-b','fixture-c'],
        'producto':['palta']*3,'destino':['TEST']*3,
        'fecha_embarque_raw':['20260105','20260106','20260112'],
        'valor_fob_usd':[200,600,900],'peso_neto_kg':[100,200,300]})
    panel = weekly_panel(rows)
    before, after = panel.unit_fob.tolist()
    assert before == pytest.approx(800/300)
    assert after == 3
    assert after-before == pytest.approx(1/3)
    relative = 100*(after-before)/before
    assert relative == pytest.approx(12.5)
    evidence = {'change':{'value':relative,'unit':'%','source_id':'fixture-comparison-v1'}}
    claim = {'fact_id':'change','value':12.50,'unit':'%','source_id':'fixture-comparison-v1','decimals':2}
    assert verify_atomic_claim(claim,evidence)['valid']
    claim['value'] = 13.0
    assert not verify_atomic_claim(claim,evidence)['valid']


def test_e2_zero_and_incompatible_units_require_abstention_not_invented_value():
    design = build_design()
    for key in design['keys']:
        if key['scenario'] in {'zero_denominator','incompatible_units','incompatible_commercial_level','unpublished_data'}:
            assert 'unit_fob' in key['required_abstentions']
            assert 'unit_fob' not in key['numeric']
    evidence = {'amount':{'value':800,'unit':'USD','source_id':'fixture-v1'}}
    claim = {'fact_id':'amount','value':800,'unit':'kg','source_id':'fixture-v1','decimals':2}
    assert verify_atomic_claim(claim,evidence)['reason'] == 'source_or_unit_mismatch'
    with pytest.raises(ValueError,match='human review'):
        require_execution_ready(design,{})


def test_e3_origin_target_age_reconstruction_and_alteration(tmp_path):
    emission = datetime(2026,5,18,tzinfo=timezone.utc)  # start of ISO target week 21
    last_observed = emission-timedelta(weeks=4)      # week 17
    emission_week = emission-timedelta(weeks=1)     # completed week 20
    assert emission.isocalendar().week == 21
    assert (emission_week-last_observed).days//7 == 3
    ledger = ResidualLedger()
    key = ledger.predict('fixture-run-v1',('palta','TEST'),'unit_fob',emission,emission,3.)
    ledger.observe(key,4.,emission+timedelta(weeks=1),'a'*64)
    assert ledger.interval('fixture-run-v1',('palta','TEST'),'unit_fob',emission,3.)['past_errors'] == 0
    path = tmp_path/'ledger.json'
    digest = ledger.save(path)
    recovered = ResidualLedger.load(path,digest)
    assert recovered.predictions == ledger.predictions
    artifact = json.loads(path.read_text(encoding='utf8'))
    artifact['body']['records'][0]['outcome']['actual'] = 400
    path.write_text(json.dumps(artifact),encoding='utf8')
    with pytest.raises(ValueError,match='integrity mismatch'):
        ResidualLedger.load(path,digest)
