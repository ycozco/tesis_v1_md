"""Authentication checks against an isolated database, never a real user."""


def test_login_success(api_client):
    response = api_client.post('/api/auth/login', json={'identifier': 'test-auditor', 'password': 'OnlyIsolatedTests2026!'})
    assert response.status_code == 200
    data = response.json()
    assert data['token'] and data['user']['username'] == 'test-auditor'
    assert data['user']['rol'] == 'AUDITOR'


def test_login_failure(api_client):
    response = api_client.post('/api/auth/login', json={'identifier': 'test-auditor', 'password': 'wrong'})
    assert response.status_code == 401


def test_logout_requires_authentication(api_client):
    assert api_client.post('/api/auth/logout').status_code == 401
    login = api_client.post('/api/auth/login', json={'identifier': 'test-auditor', 'password': 'OnlyIsolatedTests2026!'})
    response = api_client.post('/api/auth/logout', headers={'Authorization': 'Bearer '+login.json()['token']})
    assert response.status_code == 200
    assert response.json()['message'] == 'Sesión cerrada.'
    # Persistent JWT revocation remains a separate gap.
