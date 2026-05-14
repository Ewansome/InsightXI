from fastapi import APIRouter

from app.models.referee import Referee
from app.services.referee_service import referee_service

router = APIRouter(prefix="/referees", tags=["referees"])


@router.get("", response_model=list[Referee])
async def get_referees() -> list[Referee]:
    return await referee_service.get_all_referees()


@router.get("/{referee_id}", response_model=Referee)
async def get_referee(referee_id: int) -> Referee:
    return await referee_service.get_referee_by_id(referee_id)
