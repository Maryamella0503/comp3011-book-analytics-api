import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import csv
from app import create_app
from app.extensions.db import db
from app.models.book import Book


CSV_PATH = "data/books.csv"


def main():
    app = create_app()

    with app.app_context():
        added = 0

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    title = row["title"]
                    author = row["authors"]
                    rating = float(row["average_rating"])

                    # simple genre fallback
                    genre = "General"

                except Exception:
                    continue

                if not title or not author:
                    continue

                book = Book(
                    title=title.strip(),
                    author=author.strip(),
                    genre=genre,
                    rating=rating
                )

                db.session.add(book)
                added += 1

                # commit every 100 rows
                if added % 100 == 0:
                    db.session.commit()

        db.session.commit()
        print(f"Imported {added} books successfully")


if __name__ == "__main__":
    main()