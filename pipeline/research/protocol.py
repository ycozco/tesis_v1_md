"""Small, testable protocol primitives. No fitted-on-training residuals."""
from .evidence import verify_atomic_claim
import math
import numpy as np
import pandas as pd


def weekly_panel(rows):
    """Shipment-week aggregation; missing weeks remain unknown, never zero."""
    rows = rows.copy()
    if rows.id_declaracion_serie_sha256.duplicated().any():
        raise ValueError('Non-unique declaration-series key')
    if not set(rows.producto) <= {'palta', 'uva', 'arandano'}:
        raise ValueError('Product outside thesis scope')
    dates = pd.to_datetime(rows.fecha_embarque_raw.astype(str), format='%Y%m%d', errors='raise')
    rows['week'] = dates - pd.to_timedelta(dates.dt.dayofweek, unit='D')
    for column in ['valor_fob_usd', 'peso_neto_kg']:
        rows[column] = pd.to_numeric(rows[column], errors='raise')
        if not np.isfinite(rows[column]).all():
            raise ValueError('Non-finite customs value')
    if (rows.peso_neto_kg <= 0).any() or (rows.valor_fob_usd < 0).any():
        raise ValueError('Invalid FOB or weight')
    observed = rows.groupby(['producto', 'destino', 'week']).agg(
        fob_usd=('valor_fob_usd', 'sum'), volume_kg=('peso_neto_kg', 'sum'),
        records=('id_declaracion_serie_sha256', 'size')).reset_index()
    observed['unit_fob'] = observed.fob_usd / observed.volume_kg
    panels = []
    for (product, destination), group in observed.groupby(['producto', 'destino']):
        group = group.set_index('week').reindex(pd.date_range(group.week.min(), group.week.max(), freq='W-MON'))
        group.index.name = 'week'
        group['producto'], group['destino'] = product, destination
        group['coverage_state'] = np.where(group.records.notna(), 'observed_partial', 'unknown')
        panels.append(group.reset_index())
    return pd.concat(panels, ignore_index=True)


def feature_table(panel, embargo=0):
    """At end of week t, predict t+1 using only calendar-aligned history.

    Embargo simulates delayed availability; it does not reconstruct publication.
    Targets stay missing when no operations were recovered. No cross-gap shift.
    """
    if embargo not in (0, 4, 8):
        raise ValueError('Embargo must be 0, 4 or 8 weeks')
    result = []
    for _, group in panel.groupby(['producto', 'destino']):
        group = group.sort_values('week').copy()
        group['emission'] = group.week + pd.Timedelta(days=7)
        group['target_week'] = group.week + pd.Timedelta(weeks=1)
        for target in ['unit_fob', 'volume_kg']:
            group['target_' + target] = group[target].shift(-1)
            # Exactly target week minus 52, already older than every tested embargo.
            group[target + '_seasonal52_reference'] = group[target].shift(51)
            for lag in (0, 1, 2, 3, 12, 51):
                group[f'{target}_lag{lag}'] = group[target].shift(lag + embargo)
            group[target + '_mean4'] = group[target].shift(embargo).rolling(4, min_periods=4).mean()
        group['embargo_weeks'] = embargo
        result.append(group)
    return pd.concat(result, ignore_index=True)


def past_training(table, emission, target):
    """Target week must be finished strictly before emission, same cutoff for all series."""
    delays = pd.to_timedelta(table['embargo_weeks'] * 7, unit='D') if 'embargo_weeks' in table else pd.Timedelta(0)
    return table[(table.target_week + pd.Timedelta(weeks=1) + delays <= emission) & table[target].notna()]


def macro_mae(frame, truth='actual', prediction='prediction'):
    valid = frame.dropna(subset=[truth, prediction]).copy()
    if valid.empty:
        return None
    valid['absolute_error'] = (valid[truth] - valid[prediction]).abs()
    return float(valid.groupby(['producto', 'destino']).absolute_error.mean().mean())


def residual_interval(prediction, past_errors, coverage=0.9, window=None):
    """Empirical interval, no coverage guarantee. Caller must supply prior OOS errors."""
    if coverage not in (.9, .95) or window not in (None, 52):
        raise ValueError('Unsupported calibration setting')
    errors = np.asarray(past_errors, dtype=float)
    errors = errors[np.isfinite(errors)]
    if window:
        errors = errors[-window:]
    if len(errors) < 40:
        return None
    width = float(np.quantile(np.abs(errors), coverage, method='higher'))
    return max(0., prediction - width), prediction + width


def top_budget(scores, fraction=.05):
    """Stable common K; indices supplied in a common candidate universe."""
    values = np.asarray(scores, dtype=float)
    if not np.isfinite(values).all():
        raise ValueError('Indeterminate scores need explicit common-universe filtering')
    if not len(values):
        return set()
    k = math.ceil(len(values) * fraction)
    return set(np.argsort(-values, kind='stable')[:k].tolist())
