import time

import structlog

from app.clients.sportmonks_client import sportmonks_client
from app.models.referee import Referee

logger = structlog.get_logger()


class RefereeService:
    def __init__(self):
        self.url_suffix = "football/referees"

    async def get_all_referees(self) -> list[Referee]:
        logger.info("fetch_started", entity="referees")
        start = time.perf_counter()

        data = await sportmonks_client.get_all_pages(self.url_suffix)
        referees = [Referee(**item) for item in data]

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("fetch_completed", entity="referees", records=len(referees), duration_ms=duration_ms)
        return referees

    async def get_referee_by_id(self, referee_id: int) -> Referee:
        response = await sportmonks_client.get(f"{self.url_suffix}/{referee_id}")
        return Referee(**response["data"])


referee_service = RefereeService()
