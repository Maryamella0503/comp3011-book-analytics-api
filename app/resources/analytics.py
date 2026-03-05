from flask_restx import Namespace, Resource
from sqlalchemy import func
from app.models.book import Book
from app.extensions.db import db
from flask import request

ns = Namespace("analytics", description="Analytics endpoints")

@ns.route("/top-rated")
class TopRated(Resource):
    def get(self):
        """Top-rated books (default limit=10)"""
        # simple + reliable: order by rating desc
        limit = 10
        try:
            limit = int((__import__("flask").request.args.get("limit", "10")))
        except Exception:
            limit = 10

        books = Book.query.order_by(Book.rating.desc()).limit(limit).all()
        return {
            "limit": limit,
            "results": [
                {"id": b.id, "title": b.title, "author": b.author, "genre": b.genre, "rating": b.rating}
                for b in books
            ],
        }, 200

@ns.route("/genres")
class GenreSummary(Resource):
    def get(self):
        """Count books per genre + average rating per genre"""
        rows = (
            db.session.query(
                Book.genre,
                func.count(Book.id).label("count"),
                func.avg(Book.rating).label("avg_rating"),
            )
            .group_by(Book.genre)
            .order_by(func.count(Book.id).desc())
            .all()
        )
        return {
            "results": [
                {"genre": genre, "count": int(count), "avg_rating": float(avg_rating) if avg_rating is not None else None}
                for (genre, count, avg_rating) in rows
            ]
        }, 200

@ns.route("/rating-distribution")
class RatingDistribution(Resource):
    def get(self):
        """Simple rating distribution buckets"""
        # Buckets: 0-1, 1-2, 2-3, 3-4, 4-5
        buckets = [(0,1),(1,2),(2,3),(3,4),(4,5)]
        out = []
        for lo, hi in buckets:
            c = Book.query.filter(Book.rating >= lo, Book.rating < hi).count()
            out.append({"range": f"{lo}-{hi}", "count": c})
        return {"results": out}, 200
    
@ns.route("/recommendations")
class Recommendations(Resource):
    @ns.doc(params={
        "seed_book_id": "ID of the book to base recommendations on",
        "limit": "How many recommendations to return (default 10)"
    })
    def get(self):
        seed_book_id = request.args.get("seed_book_id", type=int)
        limit = request.args.get("limit", default=10, type=int)

        if not seed_book_id:
            ns.abort(400, "seed_book_id is required")

        seed = Book.query.get(seed_book_id)
        if not seed:
            ns.abort(404, "Seed book not found")

        recs = (
            Book.query
            .filter(Book.genre == seed.genre, Book.id != seed.id)
            .order_by(Book.rating.desc())
            .limit(limit)
            .all()
        )

        # Return format compatible with your existing API style:
        return {
            "seed": seed.to_dict() if hasattr(seed, "to_dict") else {
                "id": seed.id, "title": seed.title, "author": seed.author, "genre": seed.genre, "rating": seed.rating
            },
            "results": [
                r.to_dict() if hasattr(r, "to_dict") else {
                    "id": r.id, "title": r.title, "author": r.author, "genre": r.genre, "rating": r.rating
                }
                for r in recs
            ]
        }, 200