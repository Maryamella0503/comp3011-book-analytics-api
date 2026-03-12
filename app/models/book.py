"""
Book database model.

Represents book metadata stored in the database,
including title, author, genre, rating, and author relationship.
"""

from app.extensions.db import db

class Book(db.Model):
    """Book model storing metadata and an optional link to an author."""
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(120), nullable=False, index=True)
    genre = db.Column(db.String(60), nullable=False, index=True)
    rating = db.Column(db.Float, nullable=False)

    # relationship to Author model
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "rating": self.rating,
            "author_id": self.author_id
        }