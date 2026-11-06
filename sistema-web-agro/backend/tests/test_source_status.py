from services import source_status as sources


class Response:
    status_code = 200

    def __enter__(self): return self
    def __exit__(self, *args): pass
    def raise_for_status(self): pass
    def json(self):
        return {'periods': [{'name': 'Oct.2026', 'values': ['3.4']},
                            {'name': 'Nov.2026', 'values': ['n.d.']}]}


def test_bcrp_uses_latest_numeric_period(monkeypatch):
    monkeypatch.setattr(sources.requests, 'get', lambda *a, **k: Response())
    row = sources.check_source(sources.SOURCES[2])
    assert row['status'] == 'available'
    assert row['live_observation']['period'] == 'Oct.2026'
    assert row['live_observation']['value'] == 3.4


def test_invalid_series_is_not_marked_available(monkeypatch):
    response = Response()
    response.json = lambda: {'periods': [{'name': 'Oct.2026', 'values': ['NaN']}]}
    monkeypatch.setattr(sources.requests, 'get', lambda *a, **k: response)
    row = sources.check_source(sources.SOURCES[2])
    assert row['status'] == 'unavailable'
    assert row['last_success_at'] is None


def test_cached_context_survives_failed_refresh(monkeypatch):
    previous = dict(id='bcrp', status='available', last_success_at='2026-11-01',
                    live_observation={'value': 3.4, 'period': 'Oct.2026'})
    monkeypatch.setattr(sources, '_cached', {'sources': [previous]})
    monkeypatch.setattr(sources, '_expires', 0)
    monkeypatch.setattr(sources, 'SOURCES', [sources.SOURCES[2]])
    monkeypatch.setattr(sources, 'check_source', lambda source: dict(
        id='bcrp', status='unavailable', last_success_at=None, live_observation=None))
    row = sources.catalogue()['sources'][0]
    assert row['status'] == 'unavailable'
    assert row['live_observation'] == previous['live_observation']
    assert row['last_success_at'] == previous['last_success_at']
    monkeypatch.setattr(sources, 'check_source', lambda source: (_ for _ in ()).throw(AssertionError('Cache missed')))
    assert sources.catalogue()['cached'] is True
