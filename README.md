# COMP3011 Book Analytics API

A Flask-based REST API for managing and analysing book metadata. This project was developed for **COMP3011 – Web Services and Web Data** and demonstrates CRUD operations, JWT authentication, relational database modelling, dataset integration, and analytics endpoints.

## Features

- CRUD operations for books
- JWT authentication for protected write operations
- Filtering, sorting, and pagination on `/books`
- Analytics endpoints including recommendations, top-rated books, and genre statistics
- Relational modelling between **authors** and **books**
- Automated tests with `pytest`
- Swagger / OpenAPI documentation via Flask-RESTX
- SQLite database with SQLAlchemy and Flask-Migrate

## Tech Stack

- Python
- Flask
- Flask-RESTX
- SQLAlchemy
- SQLite
- Flask-JWT-Extended
- Flask-Migrate
- Pytest

## Project Structure

```text
app/
  __init__.py
  config.py
  routes.py
  extensions/
    db.py
    jwt.py
  models/
    __init__.py
    author.py
    book.py
  resources/
    analytics.py
    auth.py
    authors.py
    books.py
scripts/
  import_dataset.py
  populate_authors.py
tests/
  conftest.py
  test_analytics.py
  test_auth.py
  test_books.py
docs/
  api-documentation.pdf
instance/
  books.db
migrations/
run.py
requirements.txt
