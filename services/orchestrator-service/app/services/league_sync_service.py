import time

import structlog

from app.clients.database_service_client import database_service_client
from app.clients.sportmonks_service_client import sportmonks_service_client
from app.models.sync import SyncResult

logger = structlog.get_logger()


class LeagueSyncService:
    async def sync_leagues(self) -> SyncResult:
        logger.info("sync_started", entity="leagues")
        start = time.perf_counter()

        logger.info("sportmonks_fetch_started", entity="leagues")
        fetch_start = time.perf_counter()
        leagues = await sportmonks_service_client.get_leagues()
        fetch_duration_ms = int((time.perf_counter() - fetch_start) * 1000)
        logger.info("sportmonks_fetch_completed", entity="leagues", records=len(leagues), duration_ms=fetch_duration_ms)

        logger.info("database_upsert_started", entity="leagues", records=len(leagues))
        upsert_start = time.perf_counter()
        result = await database_service_client.bulk_upsert_leagues(leagues)
        upsert_duration_ms = int((time.perf_counter() - upsert_start) * 1000)
        logger.info(
            "database_upsert_completed",
            entity="leagues",
            created=result["created"],
            updated=result["updated"],
            duration_ms=upsert_duration_ms,
        )

        total_duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "sync_completed",
            entity="leagues",
            created=result["created"],
            updated=result["updated"],
            duration_ms=total_duration_ms,
        )

        return SyncResult(
            entity="leagues",
            created=result["created"],
            updated=result["updated"],
            status="completed",
        )


league_sync_service = LeagueSyncService()
