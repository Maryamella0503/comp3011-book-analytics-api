"""
Database extension.

Creates the SQLAlchemy instance used across the application.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()