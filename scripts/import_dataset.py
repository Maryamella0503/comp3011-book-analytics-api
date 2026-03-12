"""
Dataset import script.

Loads a book dataset from CSV and inserts records
into the database for analytics queries.
"""

import os
import sys
import csv
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions.db import db
from app.models.book import Book

CSV_PATH = "data/books.csv"

GENRES = [
    "Fantasy",
    "Sci-Fi",
    "Romance",
    "Mystery",
    "Nonfiction",
    "Thriller",
    "Historical",
    "Adventure"
]

def main():
    """Import the book dataset into the SQLite database."""
    app = create_app()

    with app.app_context():
        added = 0

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    title = row["title"].strip()
                    author = row["authors"].strip()
                    rating = float(row["average_rating"])
                except Exception:
                    continue

                if not title or not author:
                    continue

                book = Book(
                    title=title,
                    author=author,
                    genre=random.choice(GENRES),
                    rating=rating
                )

                db.session.add(book)
                added += 1

                # Commit in batches to avoid a very large uncommitted transaction
                if added % 100 == 0:
                    db.session.commit()

        db.session.commit()
        print(f"Imported {added} books successfully")

if __name__ == "__main__":
    main()