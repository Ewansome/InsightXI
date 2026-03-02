from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.fixture_repository import FixtureRepository
from app.schemas.fixture import BulkCreateResponse, FixtureCreate, FixtureResponse
from app.services.fixture_service import FixtureService

router = APIRouter(prefix="/fixtures", tags=["fixtures"])


def get_fixture_service(db: Session = Depends(get_db)) -> FixtureService:
    repository = FixtureRepository(db)
    return FixtureService(repository)


@router.get("", response_model=list[FixtureResponse])
def get_fixtures(service: FixtureService = Depends(get_fixture_service)) -> list[FixtureResponse]:
    return service.get_all_fixtures()


@router.get("/{fixture_id}", response_model=FixtureResponse)
def get_fixture(fixture_id: int, service: FixtureService = Depends(get_fixture_service)) -> FixtureResponse:
    return service.get_fixture_by_id(fixture_id)


@router.post("", response_model=FixtureResponse, status_code=201)
def create_fixture(fixture: FixtureCreate, service: FixtureService = Depends(get_fixture_service)) -> FixtureResponse:
    return service.create_fixture(fixture)


@router.post("/bulk", response_model=BulkCreateResponse)
def bulk_upsert_fixtures(
    fixtures: list[FixtureCreate], service: FixtureService = Depends(get_fixture_service)
) -> BulkCreateResponse:
    return service.bulk_upsert_fixtures(fixtures)


@router.delete("/{fixture_id}", status_code=204)
def delete_fixture(fixture_id: int, service: FixtureService = Depends(get_fixture_service)) -> None:
    service.delete_fixture(fixture_id)
