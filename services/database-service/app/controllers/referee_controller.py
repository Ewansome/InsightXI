from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.referee_repository import RefereeRepository
from app.schemas.referee import BulkCreateResponse, RefereeCreate, RefereeResponse
from app.services.referee_service import RefereeService

router = APIRouter(prefix="/referees", tags=["referees"])


def get_referee_service(db: Session = Depends(get_db)) -> RefereeService:
    repository = RefereeRepository(db)
    return RefereeService(repository)


@router.get("", response_model=list[RefereeResponse])
def get_referees(service: RefereeService = Depends(get_referee_service)) -> list[RefereeResponse]:
    return service.get_all_referees()


@router.get("/{referee_id}", response_model=RefereeResponse)
def get_referee(referee_id: int, service: RefereeService = Depends(get_referee_service)) -> RefereeResponse:
    return service.get_referee_by_id(referee_id)


@router.post("", response_model=RefereeResponse, status_code=201)
def create_referee(referee: RefereeCreate, service: RefereeService = Depends(get_referee_service)) -> RefereeResponse:
    return service.create_referee(referee)


@router.post("/bulk", response_model=BulkCreateResponse)
def bulk_upsert_referees(
    referees: list[RefereeCreate], service: RefereeService = Depends(get_referee_service)
) -> BulkCreateResponse:
    return service.bulk_upsert_referees(referees)


@router.delete("/{referee_id}", status_code=204)
def delete_referee(referee_id: int, service: RefereeService = Depends(get_referee_service)) -> None:
    service.delete_referee(referee_id)
