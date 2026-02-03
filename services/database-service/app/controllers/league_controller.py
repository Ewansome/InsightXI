from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.league_repository import LeagueRepository
from app.services.league_service import LeagueService
from app.schemas.league import LeagueCreate, LeagueResponse, BulkCreateResponse

router = APIRouter(prefix="/leagues", tags=["leagues"])


def get_league_service(db: Session = Depends(get_db)) -> LeagueService:
    repository = LeagueRepository(db)
    return LeagueService(repository)


@router.get("", response_model=list[LeagueResponse])
def get_leagues(service: LeagueService = Depends(get_league_service)) -> list[LeagueResponse]:
    return service.get_all_leagues()


@router.get("/{league_id}", response_model=LeagueResponse)
def get_league(league_id: int, service: LeagueService = Depends(get_league_service)) -> LeagueResponse:
    return service.get_league_by_id(league_id)


@router.post("", response_model=LeagueResponse, status_code=201)
def create_league(league: LeagueCreate, service: LeagueService = Depends(get_league_service)) -> LeagueResponse:
    return service.create_league(league)


@router.post("/bulk", response_model=BulkCreateResponse)
def bulk_upsert_leagues(
    leagues: list[LeagueCreate], service: LeagueService = Depends(get_league_service)
) -> BulkCreateResponse:
    return service.bulk_upsert_leagues(leagues)


@router.delete("/{league_id}", status_code=204)
def delete_league(league_id: int, service: LeagueService = Depends(get_league_service)) -> None:
    service.delete_league(league_id)
