from datetime import date, timedelta
import pytest
from pipeline.research.h3_rules import (calibrated_ensemble, select_per_product,
                                       persistence_label, persistence_summary)


def test_ensemble_uses_prior_training_distribution_not_current_cohort():
    training = {name: [0, 1, 2, 3] for name in ('IF', 'LOF', 'ECOD')}
    scores = {'IF': 1, 'LOF': 2, 'ECOD': 99}
    assert calibrated_ensemble(training, scores) == {
        'percentiles': {'IF': .5, 'LOF': .75, 'ECOD': 1.}, 'ensemble': .75}
    with pytest.raises(ValueError):
        calibrated_ensemble({**training, 'IF': []}, scores)


def test_budget_per_product_and_ties_by_date_destination():
    rows = [{'id': str(i), 'product': 'uva', 'week': date(2026, 1, 5),
             'destination': f'{i:02}', 'score': 1.} for i in range(21)]
    rows += [{'id': 'palta', 'product': 'palta', 'week': date(2026, 1, 5),
              'destination': 'US', 'score': 0.}]
    assert select_per_product(list(reversed(rows))) == {'palta': ['palta'], 'uva': ['0', '1']}
    assert select_per_product([]) == {}


def test_rubric_does_not_treat_partial_data_as_ground_truth():
    week = date(2026, 1, 5)
    observed = {}
    for offset in (0, 1, 2):
        current = week+timedelta(weeks=offset)
        observed[current] = {'value': 125., 'coverage_state': 'observed_certified'}
        observed[current-timedelta(weeks=52)] = {'value': 100., 'coverage_state': 'observed_certified'}
    end = week+timedelta(weeks=3)
    assert persistence_label(week, observed, end) == 'positive'
    assert persistence_label(week, observed, end, .3) == 'negative'
    assert persistence_label(week, observed, week+timedelta(weeks=1)) == 'ineligible'
    observed[week]['coverage_state'] = 'observed_partial'
    assert persistence_label(week, observed, end) == 'indeterminate'


def test_zero_baseline_is_indeterminate_and_bounds_are_not_ci():
    week = date(2026, 1, 5)
    observed = {week: {'value': 3., 'coverage_state': 'observed_certified'},
                week-timedelta(weeks=52): {'value': 0., 'coverage_state': 'certified_no_operations'}}
    assert persistence_label(week, observed, week+timedelta(weeks=2)) == 'indeterminate'
    result = persistence_summary(['positive', 'negative', 'indeterminate'])
    assert result['K'] == 3
    assert result['proportion_determinate'] == .5
    assert result['indeterminacy_bounds_not_confidence_interval'] == [1/3, 2/3]
    assert persistence_summary([])['proportion_determinate'] is None
