from app.clients.sportmonks_service_client import sportmonks_service_client
from app.clients.database_service_client import database_service_client
from app.models.sync import SyncResult


class LeagueSyncService:
    async def sync_leagues(self) -> SyncResult:
        leagues = await sportmonks_service_client.get_leagues()
        result = await database_service_client.bulk_upsert_leagues(leagues)

        return SyncResult(
            entity="leagues",
            created=result["created"],
            updated=result["updated"],
            status="completed",
        )


league_sync_service = LeagueSyncService()
