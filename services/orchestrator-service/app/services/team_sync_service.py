from app.clients.database_service_client import database_service_client
from app.clients.sportmonks_service_client import sportmonks_service_client
from app.models.sync import SyncResult


class TeamSyncService:
    async def sync_teams(self) -> SyncResult:
        teams = await sportmonks_service_client.get_teams()
        result = await database_service_client.bulk_upsert_teams(teams)

        return SyncResult(
            entity="teams",
            created=result["created"],
            updated=result["updated"],
            status="completed",
        )


team_sync_service = TeamSyncService()
