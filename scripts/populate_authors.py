import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions.db import db
from app.models.book import Book
from app.models.author import Author


def main():
    app = create_app()

    with app.app_context():
        unique_authors = set()
        books = Book.query.all()

        for book in books:
            if book.author:
                unique_authors.add(book.author.strip())

        added = 0
        for name in unique_authors:
            existing = Author.query.filter_by(name=name).first()
            if not existing:
                author = Author(name=name, nationality=None)
                db.session.add(author)
                added += 1

        db.session.commit()
        print(f"Added {added} authors.")

        # optional: connect books to authors
        for book in books:
            author = Author.query.filter_by(name=book.author.strip()).first()
            if author:
                book.author_id = author.id

        db.session.commit()
        print("Linked books to authors.")


if __name__ == "__main__":
    main()