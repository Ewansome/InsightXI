from fastapi import APIRouter

from app.models.fixture import Fixture
from app.services.fixture_service import fixture_service

router = APIRouter(prefix="/fixtures", tags=["fixtures"])


@router.get("", response_model=list[Fixture])
async def get_fixtures() -> list[Fixture]:
    return await fixture_service.get_all_fixtures()


@router.get("/{fixture_id}", response_model=Fixture)
async def get_fixture(fixture_id: int) -> Fixture:
    return await fixture_service.get_fixture_by_id(fixture_id)
