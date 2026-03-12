"""
Application configuration.

Defines database connection and JWT configuration.
Environment variables can override default values.
"""

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///books.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "change-me-change-me-change-me-change-me")