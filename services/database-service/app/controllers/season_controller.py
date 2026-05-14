from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.season_repository import SeasonRepository
from app.schemas.season import BulkCreateResponse, SeasonCreate, SeasonResponse
from app.services.season_service import SeasonService

router = APIRouter(prefix="/seasons", tags=["seasons"])


def get_season_service(db: Session = Depends(get_db)) -> SeasonService:
    repository = SeasonRepository(db)
    return SeasonService(repository)


@router.get("", response_model=list[SeasonResponse])
def get_seasons(service: SeasonService = Depends(get_season_service)) -> list[SeasonResponse]:
    return service.get_all_seasons()


@router.get("/{season_id}", response_model=SeasonResponse)
def get_season(season_id: int, service: SeasonService = Depends(get_season_service)) -> SeasonResponse:
    return service.get_season_by_id(season_id)


@router.post("", response_model=SeasonResponse, status_code=201)
def create_season(season: SeasonCreate, service: SeasonService = Depends(get_season_service)) -> SeasonResponse:
    return service.create_season(season)


@router.post("/bulk", response_model=BulkCreateResponse)
def bulk_upsert_seasons(
    seasons: list[SeasonCreate], service: SeasonService = Depends(get_season_service)
) -> BulkCreateResponse:
    return service.bulk_upsert_seasons(seasons)


@router.delete("/{season_id}", status_code=204)
def delete_season(season_id: int, service: SeasonService = Depends(get_season_service)) -> None:
    service.delete_season(season_id)
