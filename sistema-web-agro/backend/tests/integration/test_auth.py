import pytest
from fastapi.testclient import TestClient

from app_fastapi.main import app
from app_fastapi.core.security import get_password_hash
from models import SessionLocal, Usuario

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_test_user():
    db = SessionLocal()
    # Ensure test user exists
    user = db.query(Usuario).filter(Usuario.username == "test_auditor").first()
    if not user:
        user = Usuario(
            username="test_auditor",
            password_hash=get_password_hash("test_password"),
            email="test@agro.com",
            nombre="Test Auditor",
            rol="AUDITOR"
        )
        db.add(user)
        db.commit()
    
    yield user
    
    # Cleanup
    db.delete(user)
    db.commit()
    db.close()

def test_login_success(setup_test_user):
    response = client.post(
        "/api/auth/login",
        json={"identifier": "test_auditor", "password": "test_password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "user" in data
    assert "condicion" in data
    assert data["user"]["username"] == "test_auditor"

def test_login_failure():
    response = client.post(
        "/api/auth/login",
        json={"identifier": "test_auditor", "password": "wrong_password"}
    )
    assert response.status_code == 401
    
def test_logout(setup_test_user):
    # First login to get a token
    response_login = client.post(
        "/api/auth/login",
        json={"identifier": "test_auditor", "password": "test_password"}
    )
    token = response_login.json()["token"]
    
    # Then logout
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Sesión cerrada."
