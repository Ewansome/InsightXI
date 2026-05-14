import time

import structlog

from app.clients.sportmonks_client import sportmonks_client
from app.models.season import Season

logger = structlog.get_logger()


class SeasonService:
    def __init__(self):
        self.url_suffix = "football/seasons"

    async def get_all_seasons(self) -> list[Season]:
        logger.info("fetch_started", entity="seasons")
        start = time.perf_counter()

        data = await sportmonks_client.get_all_pages(self.url_suffix)
        seasons = [Season(**item) for item in data]

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("fetch_completed", entity="seasons", records=len(seasons), duration_ms=duration_ms)
        return seasons

    async def get_season_by_id(self, season_id: int) -> Season:
        response = await sportmonks_client.get(f"{self.url_suffix}/{season_id}")
        return Season(**response["data"])


season_service = SeasonService()
