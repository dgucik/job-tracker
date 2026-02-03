# Job Tracker

API for tracking job applications: company, role, status, location, compensation, notes, and document attachments.

**Stack:** FastAPI, SQLAlchemy 2 (async + asyncpg), Alembic, Pydantic Settings. CQRS-style (Command/Query Bus).

## Requirements

- Python 3.12+
- Poetry
- PostgreSQL 15+ (e.g. via Docker locally)

## Setup & run

```bash
# Dependencies
poetry install

# Database (Docker)
cp .env.example .env   # set DB__* for your database
docker compose up -d postgres

# Migrations
poetry run alembic upgrade head

# Server
poetry run uvicorn main:app --reload --app-dir src
```

API: `http://127.0.0.1:8000` (docs: `/docs`).

## API (prefix `/v1/job-applications`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List applications |
| POST | `/` | Create application |
| DELETE | `/{id}` | Delete application |
| PUT | `/{id}/status` | Update status |
| PUT | `/{id}/notes` | Update notes |
| POST | `/{id}/document` | Upload document (file) |
| GET | `/{id}/document` | Get document |

## Tests

```bash
# Unit
poetry run pytest tests/unit -v

# Integration (requires Docker)
poetry run pytest tests/integration -m integration -v
```

## Configuration

Environment variables (or `.env`), e.g.:

- `DB__USER`, `DB__PASSWORD`, `DB__HOST`, `DB__PORT`, `DB__NAME` — PostgreSQL connection
- `LOG__LEVEL` — log level (e.g. DEBUG, INFO)

See `.env.example`.
