from fastapi import APIRouter
from app.models.sync import SyncResult
from app.services.league_sync_service import league_sync_service

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/leagues", response_model=SyncResult)
async def sync_leagues() -> SyncResult:
    return await league_sync_service.sync_leagues()
