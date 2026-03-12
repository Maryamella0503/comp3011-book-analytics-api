"""
Authentication endpoints.

Implements JWT-based login for protecting write operations
such as creating, updating, and deleting books.
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token

ns = Namespace("auth", description="Authentication endpoints")

login_model = ns.model("LoginRequest", {
    "username": fields.String(required=True),
    "password": fields.String(required=True),
})

token_model = ns.model("TokenResponse", {
    "access_token": fields.String,
    "token_type": fields.String,
})

# Demo user (explained in report)
DEMO_USER = {"username": "demo", "password": "demo"}

@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model, validate=True)
    @ns.marshal_with(token_model)
    def post(self):
        data = request.json or {}
        if data.get("username") != DEMO_USER["username"] or data.get("password") != DEMO_USER["password"]:
            ns.abort(401, "Invalid credentials")

        token = create_access_token(identity=data["username"])
        return {"access_token": token, "token_type": "bearer"}, 200