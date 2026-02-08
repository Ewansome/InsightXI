from fastapi import APIRouter

from app.models.league import League
from app.services.league_service import league_service

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get("", response_model=list[League])
async def get_leagues() -> list[League]:
    return await league_service.get_all_leagues()


@router.get("/{league_id}", response_model=League)
async def get_league(league_id: int) -> League:
    return await league_service.get_league_by_id(league_id)
