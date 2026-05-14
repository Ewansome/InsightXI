import time

import structlog

from app.clients.database_service_client import database_service_client
from app.clients.sportmonks_service_client import sportmonks_service_client
from app.models.sync import SyncResult

logger = structlog.get_logger()


class SeasonSyncService:
    async def sync_seasons(self) -> SyncResult:
        logger.info("sync_started", entity="seasons")
        start = time.perf_counter()

        logger.info("sportmonks_fetch_started", entity="seasons")
        fetch_start = time.perf_counter()
        seasons = await sportmonks_service_client.get_seasons()
        fetch_duration_ms = int((time.perf_counter() - fetch_start) * 1000)
        logger.info("sportmonks_fetch_completed", entity="seasons", records=len(seasons), duration_ms=fetch_duration_ms)

        logger.info("database_upsert_started", entity="seasons", records=len(seasons))
        upsert_start = time.perf_counter()
        result = await database_service_client.bulk_upsert_seasons(seasons)
        upsert_duration_ms = int((time.perf_counter() - upsert_start) * 1000)
        logger.info(
            "database_upsert_completed",
            entity="seasons",
            created=result["created"],
            updated=result["updated"],
            duration_ms=upsert_duration_ms,
        )

        total_duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "sync_completed",
            entity="seasons",
            created=result["created"],
            updated=result["updated"],
            duration_ms=total_duration_ms,
        )

        return SyncResult(
            entity="seasons",
            created=result["created"],
            updated=result["updated"],
            status="completed",
        )


season_sync_service = SeasonSyncService()
