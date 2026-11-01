from datetime import datetime, timedelta, timezone
import json
import pytest
from pipeline.research.temporal_ledger import ResidualLedger


def test_e3_origin20_last17_target21_has_no_residual21():
    ledger = ResidualLedger()
    origin = datetime(2026, 5, 18, tzinfo=timezone.utc)
    key = ledger.predict('model', ('palta','US'), 'unit_fob', origin, origin, 3.)
    # An outcome may be archived retrospectively, but it is not observable at origin.
    ledger.observe(key, 30., origin+timedelta(weeks=1), 'a'*64)
    result = ledger.interval('model', ('palta','US'), 'unit_fob', origin, 3.)
    assert result['past_errors'] == 0
    assert result['lower'] is None


def test_calibration_is_same_series_run_target_and_publication_cutoff():
    ledger = ResidualLedger()
    start = datetime(2020, 1, 6, tzinfo=timezone.utc)
    for i in range(41):
        origin = start+timedelta(weeks=i)
        key = ledger.predict('a', ('uva','US'), 'volume_kg', origin, origin, 100.)
        ledger.observe(key, 100.+i, origin+timedelta(weeks=1), 'a'*64)
        delayed_key = ledger.predict('a', ('uva','US'), 'volume_kg', origin, origin, 100., embargo=4)
        ledger.observe(delayed_key, 100.+i, origin+timedelta(weeks=1), 'a'*64)
    now = start+timedelta(weeks=41)
    result = ledger.interval('a', ('uva','US'), 'volume_kg', now, 100., coverage=.95)
    assert (result['lower'],result['upper']) == (61.,139.)
    assert ledger.interval('a', ('uva','US'), 'volume_kg', now, 100., embargo=4)['past_errors'] == 37
    assert ledger.interval('a', ('uva','US'), 'volume_kg', now, 100., embargo=8)['past_errors'] == 0
    assert ledger.interval('b', ('uva','US'), 'volume_kg', now, 100.)['past_errors'] == 0
    assert ledger.interval('a', ('uva','NL'), 'volume_kg', now, 100.)['past_errors'] == 0
    assert ledger.interval('a', ('uva','US'), 'unit_fob', now, 100.)['past_errors'] == 0


def test_delayed_publication_not_just_finished_week_controls_eligibility():
    ledger = ResidualLedger()
    start = datetime(2020, 1, 6, tzinfo=timezone.utc)
    key = ledger.predict('a', ('uva','US'), 'volume_kg', start, start, 1.)
    ledger.observe(key, 9., start+timedelta(weeks=10), 'a'*64)
    assert ledger.interval('a', ('uva','US'), 'volume_kg', start+timedelta(weeks=9), 1.)['past_errors'] == 0
    assert ledger.interval('a', ('uva','US'), 'volume_kg', start+timedelta(weeks=10), 1.)['past_errors'] == 1
    with pytest.raises(ValueError, match='immutable'):
        ledger.observe(key, 1., start+timedelta(weeks=11), 'b'*64)
    with pytest.raises(ValueError, match='overwritten'):
        ledger.predict('a', ('uva','US'), 'volume_kg', start, start, 1.)


def test_rejects_naive_time_and_impossible_publication():
    ledger = ResidualLedger()
    start = datetime(2020, 1, 6, tzinfo=timezone.utc)
    with pytest.raises(ValueError, match='timezone'):
        ledger.predict('a', ('uva','US'), 'volume_kg', start.replace(tzinfo=None), start, 1.)
    key = ledger.predict('a', ('uva','US'), 'volume_kg', start, start, 1.)
    with pytest.raises(ValueError, match='end of its week'):
        ledger.observe(key, 1., start, 'a'*64)


def test_persisted_run_detects_altered_value_and_cannot_be_overwritten(tmp_path):
    ledger = ResidualLedger()
    start = datetime(2020, 1, 6, tzinfo=timezone.utc)
    key = ledger.predict('model-a', ('uva','US'), 'volume_kg', start, start, 1.)
    ledger.observe(key, 9., start+timedelta(weeks=1), 'a'*64)
    path = tmp_path/'ledger.json'
    digest = ledger.save(path)
    recovered = ResidualLedger.load(path, digest)
    assert recovered.outcomes == ledger.outcomes
    with pytest.raises(FileExistsError):
        ledger.save(path)
    artifact = json.loads(path.read_text(encoding='utf8'))
    artifact['body']['records'][0]['prediction'] = 99.
    path.write_text(json.dumps(artifact), encoding='utf8')
    with pytest.raises(ValueError, match='integrity mismatch'):
        ResidualLedger.load(path, digest)
