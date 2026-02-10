from fastapi import APIRouter

from app.models.team import Team
from app.services.team_service import team_service

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("", response_model=list[Team])
async def get_teams() -> list[Team]:
    return await team_service.get_all_teams()


@router.get("/{team_id}", response_model=Team)
async def get_team(team_id: int) -> Team:
    return await team_service.get_team_by_id(team_id)
