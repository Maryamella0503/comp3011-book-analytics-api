"""
JWT extension configuration.

Initialises Flask-JWT-Extended for authentication and token handling.
"""

from flask_jwt_extended import JWTManager

jwt = JWTManager()