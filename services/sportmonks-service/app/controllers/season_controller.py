from fastapi import APIRouter

from app.models.season import Season
from app.services.season_service import season_service

router = APIRouter(prefix="/seasons", tags=["seasons"])


@router.get("", response_model=list[Season])
async def get_seasons() -> list[Season]:
    return await season_service.get_all_seasons()


@router.get("/{season_id}", response_model=Season)
async def get_season(season_id: int) -> Season:
    return await season_service.get_season_by_id(season_id)
