import time

import structlog

from app.clients.sportmonks_client import sportmonks_client
from app.models.league import League

logger = structlog.get_logger()


class LeagueService:
    def __init__(self):
        self.url_suffix = "football/leagues"

    async def get_all_leagues(self) -> list[League]:
        logger.info("fetch_started", entity="leagues")
        start = time.perf_counter()

        data = await sportmonks_client.get_all_pages(self.url_suffix)
        leagues = [League(**item) for item in data]

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("fetch_completed", entity="leagues", records=len(leagues), duration_ms=duration_ms)
        return leagues

    async def get_league_by_id(self, league_id: int) -> League:
        response = await sportmonks_client.get(f"{self.url_suffix}/{league_id}")
        return League(**response["data"])


league_service = LeagueService()
