"""Integration fixtures are artificial and isolated in SQLite memory."""
import os
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT/'sistema-web-agro/backend'))
os.environ['DATABASE_URL'] = 'sqlite+pysqlite:///:memory:'


@pytest.fixture
def database_factory(monkeypatch):
    import models
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    from app_fastapi.main import app
    from app_fastapi.api.deps import get_db
    engine = create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
    models.Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    monkeypatch.setattr(models,'engine',engine)
    with factory() as db:
        from app_fastapi.core.security import get_password_hash
        db.add(models.Usuario(username='test-auditor',email='test@example.invalid',nombre='Artificial tester',
            rol='AUDITOR',password_hash=get_password_hash('OnlyIsolatedTests2026!')))
        db.commit()
    def session():
        with factory() as db:
            yield db
    app.dependency_overrides[get_db] = session
    yield factory
    app.dependency_overrides.pop(get_db, None)
    engine.dispose()


@pytest.fixture
def api_client(database_factory):
    from fastapi.testclient import TestClient
    from app_fastapi.main import app
    with TestClient(app) as client:
        yield client
