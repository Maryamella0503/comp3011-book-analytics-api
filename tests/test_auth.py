def test_login_success(client):
    res = client.post("/auth/login", json={
        "username": "demo",
        "password": "demo"
    })

    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data