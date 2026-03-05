from flask import Flask
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.extensions.db import db
from app.extensions.jwt import jwt
from app.routes import api, register_namespaces


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config["ERROR_404_HELP"] = False
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    api.init_app(app)
    register_namespaces(api)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    # error handlers
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return {
            "error": e.name,
            "message": e.description,
            "status_code": e.code
        }, e.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        return {
            "error": "Internal Server Error",
            "message": str(e),
            "status_code": 500
        }, 500

    return app