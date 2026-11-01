"""Thesis rules independent of model runtimes; no experiment is run on import.

History entries are (week, value, observable_at); caller supplies one series.
Publication dates must be evidenced, never inferred from shipment dates.
"""
from datetime import timedelta
from math import isfinite
from statistics import mean, median


def baselines(history, emission, target_week, embargo=0):
    if embargo not in (0, 4, 8):
        raise ValueError('Unsupported embargo')
    if target_week != emission:
        raise ValueError('Origin is the start of target week')
    available = sorted((week, float(value)) for week, value, published in history
                       if value is not None and isfinite(float(value))
                       and published is not None
                       and published + timedelta(weeks=embargo) <= emission
                       and week < target_week)
    if len({week for week, _ in available}) != len(available):
        raise ValueError('Duplicate weekly values')
    values = [max(0., value) for _, value in available]
    seasonal = dict(available).get(target_week - timedelta(weeks=52))
    return {'last_available': values[-1] if values else None,
            'mean4_valid': mean(values[-4:]) if len(values) >= 4 else None,
            'median13_valid': median(values[-13:]) if len(values) >= 13 else None,
            'seasonal52': max(0., seasonal) if seasonal is not None else None}


def mase_scale(observed_training):
    """One series, only published eligible training values, exact 52-week pairs."""
    pairs = [abs(value - observed_training[week - timedelta(weeks=52)])
             for week, value in observed_training.items()
             if week - timedelta(weeks=52) in observed_training
             and isfinite(value) and isfinite(observed_training[week - timedelta(weeks=52)])]
    scale = mean(pairs) if len(pairs) >= 26 else 0
    return scale if scale > 0 else None


def smape(actual, prediction):
    prediction = max(0., prediction)
    denominator = abs(actual) + abs(prediction)
    return 0. if denominator == 0 else 200 * abs(actual - prediction) / denominator


def candidate_grid():
    """Eight fully specified candidate configurations; one grid per objective."""
    common = {'learning_rate': .05, 'random_state': 42, 'n_jobs': 1}
    xgb = [dict(common, algorithm='xgboost', max_depth=d, n_estimators=n,
                objective='reg:squarederror', tree_method='hist', subsample=1.,
                colsample_bytree=1., reg_alpha=0., reg_lambda=1., min_child_weight=1., gamma=0.)
           for d in (3, 6) for n in (200, 500)]
    lgb = [dict(common, algorithm='lightgbm', num_leaves=l, n_estimators=n,
                objective='regression', max_depth=-1, min_child_samples=20,
                subsample=1., subsample_freq=0, colsample_bytree=1., reg_alpha=0.,
                reg_lambda=0., verbosity=-1, deterministic=True, force_col_wise=True)
           for l in (15, 31) for n in (200, 500)]
    return xgb + lgb
