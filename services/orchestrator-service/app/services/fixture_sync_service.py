import time

import structlog

from app.clients.database_service_client import database_service_client
from app.clients.sportmonks_service_client import sportmonks_service_client
from app.models.sync import SyncResult

logger = structlog.get_logger()


class FixtureSyncService:
    async def sync_fixtures(self) -> SyncResult:
        logger.info("sync_started", entity="fixtures")
        start = time.perf_counter()

        logger.info("sportmonks_fetch_started", entity="fixtures")
        fetch_start = time.perf_counter()
        fixtures = await sportmonks_service_client.get_fixtures()
        fetch_duration_ms = int((time.perf_counter() - fetch_start) * 1000)
        logger.info(
            "sportmonks_fetch_completed", entity="fixtures", records=len(fixtures), duration_ms=fetch_duration_ms
        )

        logger.info("database_upsert_started", entity="fixtures", records=len(fixtures))
        upsert_start = time.perf_counter()
        result = await database_service_client.bulk_upsert_fixtures(fixtures)
        upsert_duration_ms = int((time.perf_counter() - upsert_start) * 1000)
        logger.info(
            "database_upsert_completed",
            entity="fixtures",
            created=result["created"],
            updated=result["updated"],
            duration_ms=upsert_duration_ms,
        )

        total_duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "sync_completed",
            entity="fixtures",
            created=result["created"],
            updated=result["updated"],
            duration_ms=total_duration_ms,
        )

        return SyncResult(
            entity="fixtures",
            created=result["created"],
            updated=result["updated"],
            status="completed",
        )


fixture_sync_service = FixtureSyncService()
