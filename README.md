# comp3011-book-analytics-api

# COMP3011 Book Analytics API

A data-driven Web API for managing a book catalogue and generating analytics insights (e.g., top-rated books, genre statistics, rating distributions).  
Built for **COMP3011: Web Services and Web Data** (Coursework 1).

## Features
- **CRUD** for Books (Create, Read, Update, Delete) backed by an SQL database
- **Analytics endpoints** (e.g., top-rated, genre trends, rating summary)
- **Authentication** (JWT) for protected routes (optional routes may remain public depending on design)
- **OpenAPI / Swagger** interactive docs via FastAPI
- **Automated tests** + CI workflow (GitHub Actions)

---

## Tech Stack
- **API Framework:** FastAPI
- **Language:** Python 3.11+ (3.10+ should work)
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Auth:** JWT (via python-jose / PyJWT)
- **Testing:** pytest
- **Docs:** Swagger UI + exported PDF in `/docs`

---

## Project Structure
```text
app/
  main.py          # FastAPI entrypoint
  db.py            # database engine/session
  models.py        # SQLAlchemy models
  schemas.py       # Pydantic schemas
  crud.py          # CRUD operations
  auth.py          # JWT auth helpers + dependencies
  analytics.py     # analytics logic + endpoints
tests/
docs/
scripts/
