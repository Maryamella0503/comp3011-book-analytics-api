"""
Authentication endpoint tests.

Verifies that valid credentials return a JWT access token.
"""

# Submit valid demo credentials and expect a token in response.
def test_login_success(client):
    res = client.post("/auth/login", json={
        "username": "demo",
        "password": "demo"
    })

    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data