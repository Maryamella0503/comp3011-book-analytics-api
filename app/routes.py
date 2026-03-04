from flask_restx import Api

api = Api(
    title="COMP3011 Book Analytics API",
    version="0.1.0",
    description="Book catalogue CRUD + analytics endpoints (Flask).",
    doc="/docs",  # Swagger UI
)

def register_namespaces(api: Api):
    from app.resources.books import ns as books_ns
    from app.resources.analytics import ns as analytics_ns

    api.add_namespace(books_ns)
    api.add_namespace(analytics_ns)