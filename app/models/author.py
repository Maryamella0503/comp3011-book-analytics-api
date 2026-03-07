from app.extensions.db import db

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    nationality = db.Column(db.String(80), nullable=True)

    books = db.relationship("Book", backref="author_ref", lazy=True)