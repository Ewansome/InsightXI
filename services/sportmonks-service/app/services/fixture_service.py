import time

import structlog

from app.clients.sportmonks_client import sportmonks_client
from app.models.fixture import Fixture

logger = structlog.get_logger()


class FixtureService:
    def __init__(self):
        self.url_suffix = "football/fixtures"

    async def get_all_fixtures(self) -> list[Fixture]:
        logger.info("fetch_started", entity="fixtures")
        start = time.perf_counter()

        data = await sportmonks_client.get_all_pages(self.url_suffix)
        fixtures = [Fixture(**item) for item in data]

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("fetch_completed", entity="fixtures", records=len(fixtures), duration_ms=duration_ms)
        return fixtures

    async def get_fixture_by_id(self, fixture_id: int) -> Fixture:
        response = await sportmonks_client.get(f"{self.url_suffix}/{fixture_id}")
        return Fixture(**response["data"])


fixture_service = FixtureService()
