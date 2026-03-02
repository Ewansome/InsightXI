import time

import httpx
import structlog

from app.config import settings

logger = structlog.get_logger()


class DatabaseServiceClient:
    def __init__(self):
        self.base_url = settings.database_service_url
        self.timeout = httpx.Timeout(timeout=90.0)

    async def bulk_upsert_leagues(self, leagues: list[dict]) -> dict:
        logger.info("database_request_started", entity="leagues", operation="bulk_upsert", records=len(leagues))
        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/leagues/bulk", json=leagues)
            response.raise_for_status()
            data = response.json()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("database_request_completed", entity="leagues", operation="bulk_upsert", duration_ms=duration_ms)
        return data

    async def get_leagues(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/leagues")
            response.raise_for_status()
            return response.json()

    async def get_league(self, league_id: int) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/leagues/{league_id}")
            response.raise_for_status()
            return response.json()

    async def bulk_upsert_teams(self, teams: list[dict]) -> dict:
        logger.info("database_request_started", entity="teams", operation="bulk_upsert", records=len(teams))
        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/teams/bulk", json=teams)
            response.raise_for_status()
            data = response.json()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("database_request_completed", entity="teams", operation="bulk_upsert", duration_ms=duration_ms)
        return data

    async def get_teams(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/teams")
            response.raise_for_status()
            return response.json()

    async def get_team(self, team_id: int) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/teams/{team_id}")
            response.raise_for_status()
            return response.json()

    async def bulk_upsert_fixtures(self, fixtures: list[dict]) -> dict:
        logger.info("database_request_started", entity="fixtures", operation="bulk_upsert", records=len(fixtures))
        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/fixtures/bulk", json=fixtures)
            response.raise_for_status()
            data = response.json()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("database_request_completed", entity="fixtures", operation="bulk_upsert", duration_ms=duration_ms)
        return data

    async def get_fixtures(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/fixtures")
            response.raise_for_status()
            return response.json()

    async def get_fixture(self, fixture_id: int) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/fixtures/{fixture_id}")
            response.raise_for_status()
            return response.json()


database_service_client = DatabaseServiceClient()
