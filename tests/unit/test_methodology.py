from datetime import datetime, timedelta
from pipeline.research.methodology import baselines, mase_scale, smape, candidate_grid


def test_valid_observations_cross_gaps_but_never_publication_cutoff():
    origin = datetime(2026, 1, 5)
    history = [(origin-timedelta(weeks=i*2), i, origin-timedelta(weeks=i*2-1))
               for i in range(1, 14)]
    history += [(origin-timedelta(weeks=1), 999, origin+timedelta(days=1))]
    refs = baselines(history, origin, origin)
    assert refs['last_available'] == 1
    assert refs['mean4_valid'] == 2.5
    assert refs['median13_valid'] == 7
    assert baselines(history, origin, origin, 4)['last_available'] == 3
    assert refs['seasonal52'] is None


def test_seasonal_is_fixed_target_minus_52_and_requires_availability():
    origin = datetime(2026, 1, 5)
    assert baselines([(origin-timedelta(weeks=52), 8, origin-timedelta(weeks=51))],
                     origin, origin, 8)['seasonal52'] == 8


def test_mase_requires_26_nonzero_seasonal_pairs():
    origin = datetime(2020, 1, 6)
    values = {origin+timedelta(weeks=i): float(i) for i in range(78)}
    assert mase_scale(values) == 52
    values.pop(max(values))
    assert mase_scale(values) is None
    assert smape(0, -1) == 0
    assert smape(2, 0) == 200
    assert len(candidate_grid()) == 8
