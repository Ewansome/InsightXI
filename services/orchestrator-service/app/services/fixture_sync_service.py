from app.clients.database_service_client import database_service_client
from app.clients.sportmonks_service_client import sportmonks_service_client
from app.models.sync import SyncResult


class FixtureSyncService:
    async def sync_fixtures(self) -> SyncResult:
        fixtures = await sportmonks_service_client.get_fixtures()
        result = await database_service_client.bulk_upsert_fixtures(fixtures)

        return SyncResult(
            entity="fixtures",
            created=result["created"],
            updated=result["updated"],
            status="completed",
        )


fixture_sync_service = FixtureSyncService()
