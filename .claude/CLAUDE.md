# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

InsightXI is a sports data collation application. Data is sourced from the SportMonks Football API.

## Tech Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Database:** MySQL
- **Validation:** Pydantic
- **Linting:** Ruff
- **Project Manager:** uv
- **Containerization:** Podman/Docker

## Architecture

Three decoupled FastAPI services:

- **orchestrator-service** - Coordinates data sync workflows, exposes manual sync triggers
- **sportmonks-service** - Handles SportMonks API interactions (auth, rate limiting, retries)
- **database-service** - Handles MySQL operations (CRUD + bulk endpoints)

Data flow: `Orchestrator → SportMonks Service → SportMonks API`
                    `→ Database Service → MySQL`

## Project Structure

Each service follows the same pattern:
```
services/{service-name}/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── controllers/     # Route handlers
│   ├── services/        # Business logic
│   ├── clients/         # HTTP clients (orchestrator/sportmonks)
│   ├── repositories/    # Data access (database-service only)
│   └── models/          # Pydantic schemas
├── tests/
├── Dockerfile
└── pyproject.toml
```

## Pull-request format
Description should be split into 3 concise sections and should never credit claude:
- **Overview:** Couple of sentence summary of implemented functionality.
- **Changes:** Bullet point list of changes enabling the functionality.

## Branches
- Before checking out a new branch always run `git branch` and check the current branch.
- All branches should follow the format of **branch-type**/**feature-summary**
Where branch-type is one of:
    - feature
    - bug
    - infra
    - refactor

## Commits
- One sentence description of changes being implemented.
- All commits should have the linter and unit tets run before pushing.
