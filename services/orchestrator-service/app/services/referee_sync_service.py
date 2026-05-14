import time

import structlog

from app.clients.database_service_client import database_service_client
from app.clients.sportmonks_service_client import sportmonks_service_client
from app.models.sync import SyncResult

logger = structlog.get_logger()


class RefereeSyncService:
    async def sync_referees(self) -> SyncResult:
        logger.info("sync_started", entity="referees")
        start = time.perf_counter()

        logger.info("sportmonks_fetch_started", entity="referees")
        fetch_start = time.perf_counter()
        referees = await sportmonks_service_client.get_referees()
        fetch_duration_ms = int((time.perf_counter() - fetch_start) * 1000)
        logger.info(
            "sportmonks_fetch_completed", entity="referees", records=len(referees), duration_ms=fetch_duration_ms
        )

        logger.info("database_upsert_started", entity="referees", records=len(referees))
        upsert_start = time.perf_counter()
        result = await database_service_client.bulk_upsert_referees(referees)
        upsert_duration_ms = int((time.perf_counter() - upsert_start) * 1000)
        logger.info(
            "database_upsert_completed",
            entity="referees",
            created=result["created"],
            updated=result["updated"],
            duration_ms=upsert_duration_ms,
        )

        total_duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "sync_completed",
            entity="referees",
            created=result["created"],
            updated=result["updated"],
            duration_ms=total_duration_ms,
        )

        return SyncResult(
            entity="referees",
            created=result["created"],
            updated=result["updated"],
            status="completed",
        )


referee_sync_service = RefereeSyncService()
