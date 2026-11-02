import numpy as np
import pytest
from pipeline.research.h3_engine import FrozenECOD,score_origin


def fixture():
    rng=np.random.default_rng(42)
    def row(i):return {'id':str(i),'product':'palta','destination':'TEST','week':f'2025-{i//28+1:02}-{i%28+1:02}',
        'available_at':'2025-06-01T00:00:00Z','forecast_is_oos':True,'data_kind':'artificial',
        'features':{'residual':float(rng.normal()),'relative_change52':float(rng.normal())}}
    history=[row(i) for i in range(45)]
    current=[row(50)];current[0].update(week='2025-07-07',available_at='2025-07-14T00:00:00Z')
    return history,current


def test_frozen_ecod_score_does_not_depend_on_new_batch():
    rng=np.random.default_rng(42);model=FrozenECOD().fit(rng.normal(size=(80,3)))
    case=np.array([[4.,5.,6.]])
    alone=model.decision_function(case)[0]
    together=model.decision_function(np.vstack([case,np.full((100,3),999.)]))[0]
    assert alone==together
    assert np.isfinite(together)


def test_future_history_excluded_and_unpublished_current_rejected():
    history,current=fixture()
    features=['residual','relative_change52']
    result=score_origin(history,current,'2025-07-14T00:00:00Z',features)
    future=dict(history[0],id='future',week='2026-01-01')
    again=score_origin(history+[future],current,'2025-07-14T00:00:00Z',features)
    assert result['rows']==again['rows']
    current[0]['available_at']='2025-07-15T00:00:00Z'
    with pytest.raises(ValueError,match='Future feature'):
        score_origin(history,current,'2025-07-14T00:00:00Z',features)


def test_partial_historical_rows_cannot_be_presented_as_final_h3():
    history,current=fixture();current[0]['data_kind']='historical'
    with pytest.raises(ValueError,match='not certified'):
        score_origin(history,current,'2025-07-14T00:00:00Z',['residual','relative_change52'])


def test_integrated_scores_are_invariant_to_other_current_cases():
    history,current=fixture();features=['residual','relative_change52']
    first=score_origin(history,current,'2025-07-14T00:00:00Z',features)['rows'][0]
    other={**current[0],'id':'other-case','features':{'residual':999.,'relative_change52':999.}}
    together=score_origin(history,current+[other],'2025-07-14T00:00:00Z',features)['rows'][0]
    assert together==first
