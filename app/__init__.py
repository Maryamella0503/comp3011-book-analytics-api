from flask import Flask
from flask_migrate import Migrate

from app.config import Config
from app.extensions.db import db
from app.extensions.jwt import jwt
from app.routes import api, register_namespaces

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    api.init_app(app)
    register_namespaces(api)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app