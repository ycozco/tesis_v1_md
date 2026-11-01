"""Exploratory H3 rules. Historical detection and persistence are distinct.

Scores must be oriented so larger means more unusual. The caller must fit all
detectors on strictly prior data and pass those training-score distributions.
The empirical CDF convention is right-inclusive: count(train <= score) / n.
"""
from bisect import bisect_right
from datetime import timedelta
from math import ceil, isfinite

DETECTORS = ('IF', 'LOF', 'ECOD')
VALID_STATES = {'observed_certified', 'certified_no_operations'}


def calibrated_ensemble(training_scores, current_scores):
    if set(training_scores) != set(DETECTORS) or set(current_scores) != set(DETECTORS):
        raise ValueError('Exactly IF, LOF and ECOD are required')
    percentiles = {}
    for detector in DETECTORS:
        training = sorted(float(v) for v in training_scores[detector])
        value = float(current_scores[detector])
        if not training or not all(isfinite(v) for v in training) or not isfinite(value):
            raise ValueError('Finite nonempty prior training distribution required')
        percentiles[detector] = bisect_right(training, value) / len(training)
    return {'percentiles': percentiles, 'ensemble': sum(percentiles.values())/3}


def select_per_product(candidates):
    """Caller supplies common eligible universe; K is per product across weeks.

    Entries require id/product/week/destination/score. Undefined scores must be
    excluded consistently across methods before calling, not silently dropped.
    """
    if len({row['id'] for row in candidates}) != len(candidates):
        raise ValueError('Duplicate candidate identity')
    groups = {}
    for row in candidates:
        if not isfinite(row['score']):
            raise ValueError('Indeterminate common universe')
        groups.setdefault(row['product'], []).append(row)
    return {product: [row['id'] for row in sorted(rows,
             key=lambda row: (-row['score'], row['week'], row['destination'], row['id']))
             [:max(1, ceil(.05*len(rows)))]] for product, rows in groups.items()}


def persistence_label(week, observations, test_end, threshold=.2):
    """Retrospective rubric only, never a detector input.

    observations: week -> {value, coverage_state}. Uncertified partial observations
    are indeterminate. Last two test weeks are ineligible, not negatives.
    """
    if threshold not in (.1, .2, .3):
        raise ValueError('Unsupported prespecified sensitivity')
    if week > test_end or week + timedelta(weeks=2) > test_end:
        return 'ineligible'
    changes = []
    for offset in (0, 1, 2):
        target = week + timedelta(weeks=offset)
        current, reference = observations.get(target), observations.get(target-timedelta(weeks=52))
        if current is None or reference is None:
            return 'indeterminate'
        if current['coverage_state'] not in VALID_STATES or reference['coverage_state'] not in VALID_STATES:
            return 'indeterminate'
        value, base = current['value'], reference['value']
        if value is None or base is None or not isfinite(value) or not isfinite(base) or base <= 0:
            return 'indeterminate'
        changes.append((value-base)/base)
    return 'positive' if (all(v >= threshold for v in changes) or
                          all(v <= -threshold for v in changes)) else 'negative'


def persistence_summary(labels):
    if any(label not in {'positive', 'negative', 'indeterminate'} for label in labels):
        raise ValueError('Only selected eligible cases enter K')
    q, r, u = (labels.count(value) for value in ('positive', 'negative', 'indeterminate'))
    k = q+r+u
    return {'K': k, 'q': q, 'r': r, 'u': u,
            'proportion_determinate': q/(q+r) if q+r else None,
            'indeterminacy_bounds_not_confidence_interval': [q/k, (q+u)/k] if k else None}
