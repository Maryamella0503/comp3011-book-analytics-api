"""
Author database model.

Represents authors and their relationship with books.
"""

from app.extensions.db import db

class Author(db.Model):
    """Author model linked to one or more books."""
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    nationality = db.Column(db.String(80), nullable=True)

    books = db.relationship("Book", backref="author_ref", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "nationality": self.nationality
        }