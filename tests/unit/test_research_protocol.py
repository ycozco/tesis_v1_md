import pandas as pd
import numpy as np
from pipeline.research.protocol import (weekly_panel, feature_table, past_training,
    residual_interval, macro_mae, top_budget, verify_atomic_claim)


def example():
    return pd.DataFrame({'id_declaracion_serie_sha256': ['a', 'b', 'c'],
        'producto': ['palta']*3, 'destino': ['US']*3,
        'fecha_embarque_raw': ['20260105', '20260106', '20260119'],
        'valor_fob_usd': [10, 90, 50], 'peso_neto_kg': [10, 30, 10]})


def test_ratio_of_sums_and_unknown_gap():
    panel = weekly_panel(example())
    assert panel.iloc[0].unit_fob == 2.5
    assert pd.isna(panel.iloc[1].volume_kg)
    assert panel.iloc[1].coverage_state == 'unknown'


def test_no_shift_across_calendar_gaps_or_embargo():
    panel = weekly_panel(example())
    features = feature_table(panel)
    assert pd.isna(features.iloc[0].target_unit_fob)
    assert pd.isna(features.iloc[2].unit_fob_lag1)
    assert feature_table(panel, 4).unit_fob_lag0.isna().all()
    cutoff = features.iloc[1].emission
    train = past_training(features, cutoff, 'target_unit_fob')
    assert (train.target_week + pd.Timedelta(weeks=1) <= cutoff).all()


def test_quantiles_and_minimum_calibration():
    assert residual_interval(10, list(range(39))) is None
    assert residual_interval(10, [2]*40, .95) == (8, 12)
    assert residual_interval(10, [100]*50 + [2]*52, .9, 52) == (8, 12)


def test_macro_is_equal_series_weight():
    rows = pd.DataFrame({'producto':['palta']*3, 'destino':['US','US','NL'],
                         'actual':[0,0,0], 'prediction':[2,2,10]})
    assert macro_mae(rows) == 6
    assert len(top_budget(np.arange(21))) == 2


def test_numeric_claim_links_unit_and_absolute_tolerance():
    evidence = {'f': {'value':1000, 'source_id':'s', 'unit':'USD'}}
    claim = {'fact_id':'f', 'source_id':'s', 'unit':'USD', 'value':1000.006, 'decimals':2}
    assert not verify_atomic_claim(claim, evidence)['valid']
    claim['value'] = 1000.005
    assert verify_atomic_claim(claim, evidence)['valid']
    claim['unit'] = 'kg'
    assert not verify_atomic_claim(claim, evidence)['valid']


def test_legacy_checker_uses_absolute_decimal_tolerance():
    from pipeline.core.layer5_validation import check_value_in_text, extract_numbers_from_text
    assert not check_value_in_text(1000, [1001])
    assert check_value_in_text(1000, [1000.005])
    assert not check_value_in_text(0, [float('nan')])
    assert extract_numbers_from_text('residuo -20 kg y +1.25 USD') == [-20,1.25]


def test_embargo_applies_to_training_labels_too():
    panel = weekly_panel(example())
    table = feature_table(panel, 4)
    cutoff = pd.Timestamp('2026-02-02')
    assert past_training(table, cutoff, 'target_unit_fob').empty


def test_seasonal_reference_keeps_exact_52_week_distance_under_embargo():
    rows = example().iloc[[0]].copy()
    panel = weekly_panel(rows)
    panel = pd.concat([panel.assign(week=panel.week+pd.Timedelta(weeks=i),unit_fob=float(i)) for i in range(60)],ignore_index=True)
    features = feature_table(panel,8)
    assert features.iloc[55].unit_fob_seasonal52_reference == 4
    assert features.iloc[55].unit_fob_lag0 == 47
