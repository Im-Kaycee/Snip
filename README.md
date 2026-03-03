# URL Shortener with Analytics

A simple URL shortener built with **FastAPI**, **SQLite**, and **Redis**.  
It allows you to shorten URLs, redirect users, track click statistics, and includes a **rate limiter** to simulate high load scenarios.

This project is meant as a learning tool to explore backend concepts like database modeling, caching, and API design.

---

## Features

- Shorten any valid URL to a compact, unique short code.
- Redirect short URLs to the original URLs.
- Track statistics:
  - Click count
  - Created timestamp
  - Expiration timestamp (optional)
- Rate limiting using a **token bucket algorithm** with Redis.
- Minimal dashboard API to fetch all URLs and their short links.
- Designed for **local development and testing** (no authentication).

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **FastAPI** | Backend API framework |
| **SQLite** | Lightweight database for storage |
| **Redis** | Caching and rate-limiting |
| **SQLModel** | ORM for SQLite |
| **Pydantic** | Data validation and serialization |

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Im-Kaycee/Snip.git
cd Snip
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

3. Start Redis (required for caching and rate limiting):

```bash
redis-server
```

4. Run the FastAPI app:

```bash
uvicorn main:app --reload
```

5. Visit the docs to explore endpoints:

```
http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/shorten` | Create a shortened URL (expects JSON body) |
| `GET` | `/api/{short_code}` | Redirect to the original URL |
| `GET` | `/api/urls` | Fetch all URLs with their short codes |
| `GET` | `/api/stats/{short_code}` | Fetch statistics for a given short code |

---

## Rate Limiting

Implemented using a **token bucket algorithm** stored in Redis. Prevents abuse and simulates real-world load limits.

---

## Notes

- This project is intended for learning and local testing.
- SQLite is sufficient for development, but for high load or production, a proper database like PostgreSQL is recommended.
- No authentication is implemented; all endpoints are open.
