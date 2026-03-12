"""
Pytest fixtures for the Book Analytics API.

Configures an isolated in-memory SQLite database and provides
a Flask test client for endpoint testing.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import create_app
from app.extensions.db import db

# Use an isolated in-memory database for fast and repeatable tests
@pytest.fixture()
def app():
    app = create_app()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        JWT_SECRET_KEY="test-secret-test-secret-test-secret-test-32",
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# Clean up database state after each test session
@pytest.fixture()
def client(app):
    return app.test_client()