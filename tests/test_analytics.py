def get_token(client):
    res = client.post("/auth/login", json={
        "username": "demo",
        "password": "demo"
    })
    return res.get_json()["access_token"]


def seed_books(client):
    token = get_token(client)

    books = [
        {"title": "A", "author": "X", "genre": "Sci-Fi", "rating": 4.9},
        {"title": "B", "author": "Y", "genre": "Sci-Fi", "rating": 4.1},
        {"title": "C", "author": "Z", "genre": "Fantasy", "rating": 3.2},
    ]

    for book in books:
        client.post(
            "/books",
            json=book,
            headers={"Authorization": f"Bearer {token}"}
        )


def test_top_rated(client):
    seed_books(client)

    res = client.get("/analytics/top-rated?limit=2")

    assert res.status_code == 200
    data = res.get_json()
    assert "results" in data

def test_recommendations(client):
    seed_books(client)  # your existing seeding function
    res = client.get("/books?limit=1")
    first_id = res.get_json()["results"][0]["id"]

    res = client.get(f"/analytics/recommendations?seed_book_id={first_id}&limit=2")
    assert res.status_code == 200
    data = res.get_json()
    assert "seed" in data
    assert "results" in data

def test_genre_distribution(client):
    seed_books(client)
    res = client.get("/analytics/genre-distribution")
    assert res.status_code == 200
    data = res.get_json()
    assert "results" in data


def test_top_authors(client):
    seed_books(client)
    res = client.get("/analytics/top-authors?limit=5")
    assert res.status_code == 200
    data = res.get_json()
    assert "results" in data


def test_average_rating(client):
    seed_books(client)
    res = client.get("/analytics/average-rating")
    assert res.status_code == 200
    data = res.get_json()
    assert "average_rating" in data