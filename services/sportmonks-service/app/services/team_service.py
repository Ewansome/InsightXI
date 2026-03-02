import time

import structlog

from app.clients.sportmonks_client import sportmonks_client
from app.models.team import Team

logger = structlog.get_logger()


class TeamService:
    def __init__(self) -> None:
        self.url_suffix = "football/teams"

    async def get_all_teams(self) -> list[Team]:
        logger.info("fetch_started", entity="teams")
        start = time.perf_counter()

        data = await sportmonks_client.get_all_pages(self.url_suffix)
        teams = [Team(**item) for item in data]

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("fetch_completed", entity="teams", records=len(teams), duration_ms=duration_ms)
        return teams

    async def get_team_by_id(self, team_id: int) -> Team:
        response = await sportmonks_client.get(f"{self.url_suffix}/{team_id}")
        return Team(**response["data"])


team_service = TeamService()
