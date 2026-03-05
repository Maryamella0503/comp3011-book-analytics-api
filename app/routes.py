from flask_restx import Api

authorizations = {
    "BearerAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Add: Bearer <JWT token>"
    }
}

api = Api(
    title="COMP3011 Book Analytics API",
    version="0.1.0",
    description="Book catalogue CRUD + analytics endpoints (Flask).",
    doc="/docs",
    authorizations=authorizations,
    security="BearerAuth",
    validate=True,
    catch_all_404s=False
)

def register_namespaces(api: Api):
    from app.resources.books import ns as books_ns
    from app.resources.analytics import ns as analytics_ns

    api.add_namespace(books_ns)
    api.add_namespace(analytics_ns)

from app.resources.auth import ns as auth_ns
...
api.add_namespace(auth_ns)