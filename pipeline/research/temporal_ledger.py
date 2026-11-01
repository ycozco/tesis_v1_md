"""Publication-aware OOS residual ledger; no target outcome before prediction.

All timestamps are timezone-aware. The explicit observation vintage is immutable;
embargo delays publication eligibility in baselines, labels and calibration alike.
"""
from datetime import datetime, timedelta
import hashlib
import json
from math import ceil, isfinite
from pathlib import Path


def timestamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00')) if isinstance(value, str) else value
    if not isinstance(result, datetime) or result.tzinfo is None:
        raise ValueError('A timezone-aware timestamp is required')
    return result


class ResidualLedger:
    def __init__(self):
        self.predictions = {}
        self.outcomes = {}

    def predict(self, run_id, series, target, emission, target_week, prediction, embargo=0):
        emission, target_week = timestamp(emission), timestamp(target_week)
        if embargo not in (0, 4, 8):
            raise ValueError('Unsupported embargo')
        if emission != target_week:
            raise ValueError('Weekly horizon one: origin is start of target week')
        if not isfinite(prediction) or prediction < 0:
            raise ValueError('Presented prediction must be finite and nonnegative')
        key = (run_id, tuple(series), target, target_week, embargo)
        if key in self.predictions:
            raise ValueError('Prediction is immutable and cannot be overwritten')
        self.predictions[key] = {'emission': emission, 'prediction': float(prediction)}
        return key

    def observe(self, key, actual, published_at, vintage_sha256):
        if key not in self.predictions or key in self.outcomes:
            raise ValueError('Outcome requires an existing prediction and immutable vintage')
        published = timestamp(published_at)
        if published < key[3] + timedelta(weeks=1):
            raise ValueError('Weekly target cannot be complete before the end of its week')
        if not isfinite(actual) or actual < 0:
            raise ValueError('Invalid target observation')
        if len(vintage_sha256) != 64 or any(c not in '0123456789abcdef' for c in vintage_sha256):
            raise ValueError('Observation requires a source vintage SHA-256')
        self.outcomes[key] = {'actual': float(actual), 'published_at': published,
                              'vintage_sha256': vintage_sha256}

    def interval(self, run_id, series, target, emission, prediction, embargo=0, coverage=.9, window=None):
        if embargo not in (0, 4, 8) or coverage not in (.9, .95) or window not in (None, 52):
            raise ValueError('Unsupported prespecified calibration setting')
        emission = timestamp(emission)
        if not isfinite(prediction) or prediction < 0:
            raise ValueError('Prediction must already be clipped and finite')
        errors = []
        for key, outcome in self.outcomes.items():
            if key[:3] != (run_id, tuple(series), target):
                continue
            if key[4] != embargo:
                continue
            record = self.predictions[key]
            if record['emission'] >= emission:
                continue
            if outcome['published_at'] + timedelta(weeks=embargo) <= emission:
                errors.append((key[3], abs(outcome['actual']-record['prediction'])))
        errors.sort()
        if window:
            errors = errors[-window:]
        count = len(errors)
        rank = ceil((count+1)*coverage)
        width = sorted(value for _, value in errors)[rank-1] if count >= 40 and rank <= count else None
        return {'past_errors': count, 'order_statistic': rank,
                'status': 'calibrated' if width is not None else 'insufficient_prior_errors',
                'lower': max(0., prediction-width) if width is not None else None,
                'upper': prediction+width if width is not None else None,
                'calibration_target_weeks': [week.isoformat() for week, _ in errors]}

    def save(self, path):
        """Write once. Return digest to retain in an independent run manifest."""
        records = []
        for key, prediction in self.predictions.items():
            outcome = self.outcomes.get(key)
            records.append({'run_id': key[0], 'series': list(key[1]), 'target': key[2],
                'target_week': key[3].isoformat(), 'emission': prediction['emission'].isoformat(),
                'embargo': key[4],
                'prediction': prediction['prediction'],
                'outcome': {**outcome, 'published_at': outcome['published_at'].isoformat()} if outcome else None})
        body = {'schema': 'research-oos-ledger-v1', 'records': records}
        digest = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        with Path(path).open('x', encoding='utf-8') as handle:
            json.dump({'sha256': digest, 'body': body}, handle, indent=2)
        return digest

    @classmethod
    def load(cls, path, expected_sha256):
        """Verify independent manifest hash, then reconstruct all temporal checks."""
        artifact = json.loads(Path(path).read_text(encoding='utf-8'))
        body = artifact['body']
        digest = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        if digest != expected_sha256 or artifact.get('sha256') != digest:
            raise ValueError('Ledger integrity mismatch')
        if body.get('schema') != 'research-oos-ledger-v1':
            raise ValueError('Unsupported ledger schema')
        ledger = cls()
        for row in body['records']:
            key = ledger.predict(row['run_id'], row['series'], row['target'], row['emission'],
                                 row['target_week'], row['prediction'], row['embargo'])
            if row['outcome'] is not None:
                outcome = row['outcome']
                ledger.observe(key, outcome['actual'], outcome['published_at'], outcome['vintage_sha256'])
        return ledger
