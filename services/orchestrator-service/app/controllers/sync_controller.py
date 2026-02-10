from fastapi import APIRouter

from app.models.sync import SyncResult
from app.services.league_sync_service import league_sync_service
from app.services.team_sync_service import team_sync_service

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/leagues", response_model=SyncResult)
async def sync_leagues() -> SyncResult:
    return await league_sync_service.sync_leagues()


@router.post("/teams", response_model=SyncResult)
async def sync_teams() -> SyncResult:
    return await team_sync_service.sync_teams()
