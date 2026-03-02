from fastapi import HTTPException

from app.repositories.fixture_repository import FixtureRepository
from app.schemas.fixture import BulkCreateResponse, FixtureCreate, FixtureResponse


class FixtureService:
    def __init__(self, repository: FixtureRepository):
        self.repository = repository

    def get_all_fixtures(self) -> list[FixtureResponse]:
        fixtures = self.repository.get_all()
        return [FixtureResponse.model_validate(fixture) for fixture in fixtures]

    def get_fixture_by_id(self, fixture_id: int) -> FixtureResponse:
        fixture = self.repository.get_by_id(fixture_id)
        if not fixture:
            raise HTTPException(status_code=404, detail=f"Fixture {fixture_id} not found")
        return FixtureResponse.model_validate(fixture)

    def create_fixture(self, fixture: FixtureCreate) -> FixtureResponse:
        existing = self.repository.get_by_id(fixture.id)
        if existing:
            raise HTTPException(status_code=409, detail=f"Fixture {fixture.id} already exists")
        db_fixture = self.repository.create(fixture)
        return FixtureResponse.model_validate(db_fixture)

    def bulk_upsert_fixtures(self, fixtures: list[FixtureCreate]) -> BulkCreateResponse:
        created, updated = self.repository.bulk_upsert(fixtures)
        return BulkCreateResponse(created=created, updated=updated)

    def delete_fixture(self, fixture_id: int) -> None:
        if not self.repository.delete(fixture_id):
            raise HTTPException(status_code=404, detail=f"Fixture {fixture_id} not found")
