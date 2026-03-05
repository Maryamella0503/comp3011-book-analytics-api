from flask import request
from flask_restx import Namespace, Resource, fields
from app.extensions.db import db
from app.models.book import Book
from flask_jwt_extended import jwt_required
from sqlalchemy import or_

ns = Namespace("books", description="Book CRUD endpoints")

book_model = ns.model("Book", {
    "id": fields.Integer(readOnly=True),
    "title": fields.String(required=True),
    "author": fields.String(required=True),
    "genre": fields.String(required=True),
    "rating": fields.Float(required=True, min=0, max=5),
})

book_create_model = ns.model("BookCreate", {
    "title": fields.String(required=True),
    "author": fields.String(required=True),
    "genre": fields.String(required=True),
    "rating": fields.Float(required=True, min=0, max=5),
})

def _validate_rating(value):
    try:
        v = float(value)
    except Exception:
        return False
    return 0.0 <= v <= 5.0

@ns.route("")
class BooksCollection(Resource):
    @ns.marshal_list_with(book_model)
    def get(self):
        """List all books"""
        return Book.query.all(), 200

    @ns.expect(book_create_model, validate=True)
    @ns.marshal_with(book_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new book"""
        data = request.json or {}
        if not _validate_rating(data.get("rating")):
            ns.abort(400, "rating must be a number between 0 and 5")

        book = Book(
            title=data["title"].strip(),
            author=data["author"].strip(),
            genre=data["genre"].strip(),
            rating=float(data["rating"]),
        )
        db.session.add(book)
        db.session.commit()
        return book, 201

@ns.route("/<int:book_id>")
@ns.param("book_id", "Book ID")
class BookItem(Resource):
    @ns.marshal_with(book_model)
    def get(self, book_id: int):
        """Get one book"""
        book = Book.query.get(book_id)
        if not book:
            ns.abort(404, "Book not found")
        return book, 200

    @ns.expect(book_create_model, validate=True)
    @ns.marshal_with(book_model)
    @jwt_required()
    def put(self, book_id: int):
        """Update a book"""
        book = Book.query.get(book_id)
        if not book:
            ns.abort(404, "Book not found")

        data = request.json or {}
        if not _validate_rating(data.get("rating")):
            ns.abort(400, "rating must be a number between 0 and 5")

        book.title = data["title"].strip()
        book.author = data["author"].strip()
        book.genre = data["genre"].strip()
        book.rating = float(data["rating"])

        db.session.commit()
        return book, 200

    @jwt_required()
    def delete(self, book_id: int):
        """Delete a book"""
        book = Book.query.get(book_id)
        if not book:
            ns.abort(404, "Book not found")

        db.session.delete(book)
        db.session.commit()
        return {"message": "deleted"}, 200

@ns.route("")
class BooksCollection(Resource):
    def get(self):
        q = request.args.get("q", type=str)
        genre = request.args.get("genre", type=str)
        min_rating = request.args.get("min_rating", type=float)
        limit = request.args.get("limit", default=50, type=int)
        offset = request.args.get("offset", default=0, type=int)
        sort = request.args.get("sort", default="rating_desc", type=str)

        query = Book.query

        if q:
            like = f"%{q}%"
            query = query.filter(or_(Book.title.ilike(like), Book.author.ilike(like)))

        if genre:
            query = query.filter(Book.genre == genre)

        if min_rating is not None:
            query = query.filter(Book.rating >= min_rating)

        if sort == "rating_asc":
            query = query.order_by(Book.rating.asc())
        elif sort == "title_asc":
            query = query.order_by(Book.title.asc())
        else:
            query = query.order_by(Book.rating.desc())

        total = query.count()
        items = query.offset(offset).limit(limit).all()

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "results": [b.to_dict() for b in items]
        }, 200