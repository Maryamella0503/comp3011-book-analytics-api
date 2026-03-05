def get_token(client):
    res = client.post("/auth/login", json={
        "username": "demo",
        "password": "demo"
    })
    return res.get_json()["access_token"]


def test_books_requires_auth(client):
    res = client.post("/books", json={
        "title": "X",
        "author": "A",
        "genre": "G",
        "rating": 4.0
    })

    assert res.status_code in (401, 422)


def test_create_book_with_auth(client):
    token = get_token(client)

    res = client.post(
        "/books",
        json={
            "title": "Dune",
            "author": "Frank Herbert",
            "genre": "Sci-Fi",
            "rating": 4.8
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 201