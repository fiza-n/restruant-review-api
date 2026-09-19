# 🍽️ Restaurant Reviews API

A production-quality REST API for restaurant discovery and review management — featuring automatic NLP-based sentiment analysis, a leaderboard system, and a clean microservice architecture.

Built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Docker**.

---

## Architecture

<img width="675" height="465" alt="image" src="https://github.com/user-attachments/assets/2c0c9d40-ba84-4062-8aa9-95d45de9f9f4" />



**How it works:**
1. The **Restaurant Reviews App** (frontend or API client) talks to the **Reviews Service**
2. When a review is submitted, the **Reviews Service** calls the **NLP Service** to run VADER sentiment analysis on the review body
3. The sentiment label (`positive` / `negative` / `neutral`) and compound score are stored alongside the review
4. The **PostgreSQL DB** holds both `reviews` and `restaurants` tables — the service keeps `avg_rating` in sync after every create/delete
5. The **Leaderboard** is a derived view — highest avg-rated restaurants surfaced via a ranked query

---

## Features

- 🔐 **JWT Authentication** — register, login, Bearer token on protected routes
- 🏪 **Restaurant CRUD** — create, read, update, delete with owner-only write access
- ⭐ **Review System** — one review per user per restaurant, with live avg rating updates
- 🧠 **Automatic Sentiment Analysis** — every review body is scored by VADER NLP on submission
- 🏆 **Leaderboard** — top restaurants ranked by avg rating
- 🐳 **Docker-first** — entire stack runs with one command
- 🧪 **Full test suite** — 20 pytest tests using SQLite in-memory (no real DB needed)
- 📦 **Alembic migrations** — proper schema versioning, not just `create_all()`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.111 |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (typed, modern style) |
| Migrations | Alembic |
| Auth | JWT via python-jose + bcrypt via passlib |
| NLP | VADER Sentiment (vaderSentiment) |
| Validation | Pydantic v2 |
| Testing | pytest + httpx TestClient |
| Container | Docker + docker-compose |

---

## Getting Started

### Option 1 — Docker (recommended, one command)

```bash
git clone https://github.com/your-username/restaurant-reviews-api.git
cd restaurant-reviews-api
cp .env.example .env          # edit SECRET_KEY before running in production
docker compose up --build
```

API is live at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### Option 2 — Local dev (with PostgreSQL running)

```bash
# 1. Clone and enter the project
git clone https://github.com/your-username/restaurant-reviews-api.git
cd restaurant-reviews-api

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env: set DATABASE_URL and SECRET_KEY

# 5. Run database migrations
alembic upgrade head

# 6. Start the server
uvicorn app.main:app --reload
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/restaurant_db
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```


---

## API Reference

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register` | ❌ | Create a new account |
| POST | `/api/v1/auth/login` | ❌ | Get JWT access token |
| GET | `/api/v1/users/me` | ✅ | Get your profile |

### Restaurants

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/restaurants/` | ✅ | Create a restaurant |
| GET | `/api/v1/restaurants/` | ❌ | List all (filter + paginate) |
| GET | `/api/v1/restaurants/{id}` | ❌ | Get one restaurant |
| PATCH | `/api/v1/restaurants/{id}` | ✅ Owner | Update (partial) |
| DELETE | `/api/v1/restaurants/{id}` | ✅ Owner | Delete |
| GET | `/api/v1/restaurants/leaderboard` | ❌ | Top-rated restaurants |

### Reviews

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/restaurants/{id}/reviews` | ✅ | Submit review (auto-sentiment) |
| GET | `/api/v1/restaurants/{id}/reviews` | ❌ | List all reviews |
| DELETE | `/api/v1/reviews/{id}` | ✅ Owner | Delete your review |

---

## Example Usage

### 1. Register and login

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "fiza@example.com", "username": "fiza", "password": "securepass123"}'

# Login → get token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -F "username=fiza" \
  -F "password=securepass123"
```

### 2. Create a restaurant

```bash
curl -X POST http://localhost:8000/api/v1/restaurants/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Burning Brownie",
    "cuisine_type": "Desserts",
    "address": "DHA Phase 5, Karachi",
    "description": "Best desserts in the city"
  }'
```

### 3. Submit a review (sentiment runs automatically)

```bash
curl -X POST http://localhost:8000/api/v1/restaurants/1/reviews \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "body": "Absolutely amazing! Best brownie I have ever had."}'

# Response includes:
# "sentiment_label": "positive"
# "sentiment_score": 0.8779
```

---

## Sentiment Analysis

Every review body is automatically analyzed using **VADER** (Valence Aware Dictionary and sEntiment Reasoner) — a rule-based NLP model tuned for short social-media-style text.

| Compound Score | Label |
|---|---|
| ≥ 0.05 | `positive` |
| ≤ -0.05 | `negative` |
| between | `neutral` |

This runs synchronously at review creation time and is stored in `sentiment_label` and `sentiment_score` fields — no external API calls, no latency.

---

## Running Tests

```bash
# All 20 tests — no PostgreSQL needed (SQLite in-memory)
pytest -v

# With coverage report
pytest --cov=app --cov-report=term-missing
```

Tests cover:
- ✅ Register / login / duplicate rejection
- ✅ JWT token validation + protected routes
- ✅ Restaurant CRUD + ownership enforcement
- ✅ Review creation with sentiment verification
- ✅ Avg rating recalculation on create and delete
- ✅ Duplicate review rejection
- ✅ Input validation (rating out of range, short body)

---

## Project Structure

```
restaurant-api/
├── app/
│   ├── main.py                        # App factory + router registration
│   ├── api/v1/endpoints/
│   │   ├── auth.py                    # Register, login
│   │   ├── users.py                   # /me endpoint
│   │   ├── restaurants.py             # CRUD + leaderboard
│   │   └── reviews.py                 # Create, list, delete
│   ├── core/
│   │   ├── config.py                  # Pydantic settings from .env
│   │   ├── security.py                # JWT + bcrypt helpers
│   │   └── dependencies.py            # get_db(), get_current_user()
│   ├── db/
│   │   ├── base.py                    # DeclarativeBase + model imports
│   │   └── session.py                 # Engine + SessionLocal
│   ├── models/                        # SQLAlchemy ORM models
│   ├── schemas/                       # Pydantic request/response models
│   ├── services/                      # Business logic layer
│   │   ├── sentiment.py               # VADER wrapper
│   │   ├── auth.py
│   │   ├── restaurant.py
│   │   └── review.py
│   └── tests/
│       ├── conftest.py                # SQLite fixture + TestClient
│       ├── test_auth.py
│       ├── test_restaurants.py
│       └── test_reviews.py
├── alembic/                           # DB migration files
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

## Design Decisions

**Why layered architecture (router → service → model)?**
Routers only handle HTTP concerns (request parsing, response codes). All business logic lives in `services/`. This makes services fully testable without HTTP and keeps endpoints thin and readable.

**Why Alembic instead of `Base.metadata.create_all()`?**
`create_all()` can't handle schema changes after initial creation. Alembic generates version-controlled migration scripts — the same workflow used in production engineering.

**Why SQLite for tests?**
Tests run in-memory SQLite via a `dependency_override` on `get_db`. No Postgres instance needed in CI. The ORM abstraction means the same queries work on both engines.

**Why VADER over a cloud NLP API?**
Zero latency, zero cost, no external dependency, works offline. VADER is well-suited for short review text — exactly the use case here.

**Why one review per user per restaurant?**
Prevents rating manipulation. Enforced at the service layer with a clear 400 error, not just a DB constraint.

---

## License

MIT
