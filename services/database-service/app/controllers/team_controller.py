from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.team_repository import TeamRepository
from app.schemas.team import BulkCreateResponse, TeamCreate, TeamResponse
from app.services.team_service import TeamService

router = APIRouter(prefix="/teams", tags=["teams"])


def get_team_service(db: Session = Depends(get_db)) -> TeamService:
    repository = TeamRepository(db)
    return TeamService(repository)


@router.get("", response_model=list[TeamResponse])
def get_teams(service: TeamService = Depends(get_team_service)) -> list[TeamResponse]:
    return service.get_all_teams()


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, service: TeamService = Depends(get_team_service)) -> TeamResponse:
    return service.get_team_by_id(team_id)


@router.post("", response_model=TeamResponse, status_code=201)
def create_team(team: TeamCreate, service: TeamService = Depends(get_team_service)) -> TeamResponse:
    return service.create_team(team)


@router.post("/bulk", response_model=BulkCreateResponse)
def bulk_upsert_teams(
    teams: list[TeamCreate], service: TeamService = Depends(get_team_service)
) -> BulkCreateResponse:
    return service.bulk_upsert_teams(teams)


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: int, service: TeamService = Depends(get_team_service)) -> None:
    service.delete_team(team_id)
