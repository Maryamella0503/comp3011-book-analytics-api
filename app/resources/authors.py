from flask_restx import Namespace, Resource
from app.models.author import Author

ns = Namespace("authors", description="Author endpoints")


@ns.route("")
class AuthorList(Resource):
    def get(self):
        """List all authors"""
        authors = Author.query.all()
        return [a.to_dict() for a in authors], 200


@ns.route("/<int:author_id>/books")
class AuthorBooks(Resource):
    def get(self, author_id):
        """Get books written by an author"""
        author = Author.query.get(author_id)
        if not author:
            return {"message": "Author not found"}, 404

        return {
            "author": author.to_dict(),
            "books": [b.to_dict() for b in author.books]
        }, 200