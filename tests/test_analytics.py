"""
Analytics endpoint tests.

Seeds a small dataset and verifies analytics responses such as
top-rated books, recommendations, genre distribution, and averages.
"""

# Helper used by tests to obtain a valid JWT token.
def get_token(client):
    res = client.post("/auth/login", json={
        "username": "demo",
        "password": "demo"
    })
    return res.get_json()["access_token"]

# Seed a small, predictable dataset for analytics testing.
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

# The endpoint should return ranked results for the seeded books.
def test_top_rated(client):
    seed_books(client)

    res = client.get("/analytics/top-rated?limit=2")

    assert res.status_code == 200
    data = res.get_json()
    assert "results" in data

# Recommendations should return the seed book and similar books.
def test_recommendations(client):
    seed_books(client)
    res = client.get("/books?limit=1")
    first_id = res.get_json()["results"][0]["id"]

    res = client.get(f"/analytics/recommendations?seed_book_id={first_id}&limit=2")
    assert res.status_code == 200
    data = res.get_json()
    assert "seed_book" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)

# Genre distribution should return aggregated genre counts.
def test_genre_distribution(client):
    seed_books(client)
    res = client.get("/analytics/genre-distribution")
    assert res.status_code == 200
    data = res.get_json()
    assert "results" in data

# Average rating should return a single aggregated value.
def test_top_authors(client):
    seed_books(client)
    res = client.get("/analytics/top-authors?limit=5")
    assert res.status_code == 200
    data = res.get_json()
    assert "results" in data

# Average rating should return a single aggregated value.
def test_average_rating(client):
    seed_books(client)
    res = client.get("/analytics/average-rating")
    assert res.status_code == 200
    data = res.get_json()
    assert "average_rating" in data