import time

import httpx
import structlog

from app.config import settings

logger = structlog.get_logger()


class SportMonksServiceClient:
    def __init__(self):
        self.base_url = settings.sportmonks_service_url
        self.timeout = httpx.Timeout(timeout=90.0)

    async def get_leagues(self) -> list[dict]:
        logger.info("sportmonks_request_started", entity="leagues")
        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/leagues")
            response.raise_for_status()
            data = response.json()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("sportmonks_request_completed", entity="leagues", records=len(data), duration_ms=duration_ms)
        return data

    async def get_league(self, league_id: int) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/leagues/{league_id}")
            response.raise_for_status()
            return response.json()

    async def get_teams(self) -> list[dict]:
        logger.info("sportmonks_request_started", entity="teams")
        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/teams")
            response.raise_for_status()
            data = response.json()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("sportmonks_request_completed", entity="teams", records=len(data), duration_ms=duration_ms)
        return data

    async def get_team(self, team_id: int) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/teams/{team_id}")
            response.raise_for_status()
            return response.json()

    async def get_fixtures(self) -> list[dict]:
        logger.info("sportmonks_request_started", entity="fixtures")
        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/fixtures")
            response.raise_for_status()
            data = response.json()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("sportmonks_request_completed", entity="fixtures", records=len(data), duration_ms=duration_ms)
        return data

    async def get_fixture(self, fixture_id: int) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/fixtures/{fixture_id}")
            response.raise_for_status()
            return response.json()


sportmonks_service_client = SportMonksServiceClient()
