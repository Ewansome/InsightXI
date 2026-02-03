# InsightXI
### Overview
Application for collating sports data for visualisation. Data sourced from [SportMonks API](https://docs.sportmonks.com/football).

-----
### Tech Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Database:** MySQL
- **Validation:** Pydantic
- **Linting:** Ruff
- **Project Manager:** uv
- **Containerisation:** Podman/Docker

-----
### Architecture

```
                    ┌─────────────────────────┐
                    │  Orchestrator Service   │
                    │       (FastAPI)         │
                    │                         │
    Manual ────────▶│  POST /sync/leagues     │
    Trigger         │  POST /sync/teams       │
                    │  POST /sync/fixtures    │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                                   ▼
┌─────────────────────┐             ┌─────────────────────┐
│  SportMonks Service │             │   Database Service  │
│     (FastAPI)       │             │     (FastAPI)       │
│                     │             │                     │
│  GET /leagues       │             │  POST /leagues      │
│  GET /teams         │             │  POST /leagues/bulk │
│  GET /fixtures      │             │  GET /leagues/{id}  │
└─────────┬───────────┘             └──────────┬──────────┘
          │                                    │
          ▼                                    ▼
    SportMonks API                           MySQL
```
-----
### Services

**Orchestrator Service** - Coordinates data sync workflows between services
- Exposes sync endpoints for manual triggers
- Fetches data from SportMonks Service, stores via Database Service
- Handles errors and returns sync status

**SportMonks Service** - Handles all SportMonks API interactions
- Fetches and validates data from SportMonks
- Manages authentication, rate limiting, retries

**Database Service** - Handles all database operations
- CRUD endpoints per entity
- Bulk operations for data ingestion

-----
### Project Structure

```
services/
├── orchestrator-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── clients/
│   │   └── models/
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
│
├── sportmonks-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── clients/
│   │   └── models/
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
│
└── database-service/
    ├── app/
    │   ├── main.py
    │   ├── controllers/
    │   ├── services/
    │   ├── repositories/
    │   └── models/
    ├── tests/
    ├── Dockerfile
    └── pyproject.toml
```