"""Opt-in read-only checks of a separately identified legacy release.

Without the option the original tests continue to require this checkout's gold
artifacts; missing results are failures, never silently skipped or synthesized.
"""
from pathlib import Path
import pytest


def pytest_addoption(parser):
    parser.addoption('--legacy-gold-dir', default=None,
                     help='Explicit existing legacy gold directory; not current thesis results')


@pytest.fixture(autouse=True)
def explicit_legacy_release(request, monkeypatch):
    selected = request.config.getoption('--legacy-gold-dir')
    if not selected:
        return
    module = request.module
    legacy_directories = {'data_quality', 'leakage', 'end_to_end'}
    if Path(module.__file__).parent.name not in legacy_directories or not hasattr(module, 'GOLD_DIR'):
        return
    path = Path(selected).resolve()
    if not path.is_dir():
        pytest.fail('Explicit legacy release directory does not exist')
    monkeypatch.setattr(module, 'GOLD_DIR', path)
