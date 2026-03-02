import time

import structlog

from app.clients.database_service_client import database_service_client
from app.clients.sportmonks_service_client import sportmonks_service_client
from app.models.sync import SyncResult

logger = structlog.get_logger()


class TeamSyncService:
    async def sync_teams(self) -> SyncResult:
        logger.info("sync_started", entity="teams")
        start = time.perf_counter()

        logger.info("sportmonks_fetch_started", entity="teams")
        fetch_start = time.perf_counter()
        teams = await sportmonks_service_client.get_teams()
        fetch_duration_ms = int((time.perf_counter() - fetch_start) * 1000)
        logger.info("sportmonks_fetch_completed", entity="teams", records=len(teams), duration_ms=fetch_duration_ms)

        logger.info("database_upsert_started", entity="teams", records=len(teams))
        upsert_start = time.perf_counter()
        result = await database_service_client.bulk_upsert_teams(teams)
        upsert_duration_ms = int((time.perf_counter() - upsert_start) * 1000)
        logger.info(
            "database_upsert_completed",
            entity="teams",
            created=result["created"],
            updated=result["updated"],
            duration_ms=upsert_duration_ms,
        )

        total_duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "sync_completed",
            entity="teams",
            created=result["created"],
            updated=result["updated"],
            duration_ms=total_duration_ms,
        )

        return SyncResult(
            entity="teams",
            created=result["created"],
            updated=result["updated"],
            status="completed",
        )


team_sync_service = TeamSyncService()
