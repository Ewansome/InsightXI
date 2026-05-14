from fastapi import HTTPException

from app.repositories.referee_repository import RefereeRepository
from app.schemas.referee import BulkCreateResponse, RefereeCreate, RefereeResponse


class RefereeService:
    def __init__(self, repository: RefereeRepository):
        self.repository = repository

    def get_all_referees(self) -> list[RefereeResponse]:
        referees = self.repository.get_all()
        return [RefereeResponse.model_validate(referee) for referee in referees]

    def get_referee_by_id(self, referee_id: int) -> RefereeResponse:
        referee = self.repository.get_by_id(referee_id)
        if not referee:
            raise HTTPException(status_code=404, detail=f"Referee {referee_id} not found")
        return RefereeResponse.model_validate(referee)

    def create_referee(self, referee: RefereeCreate) -> RefereeResponse:
        existing = self.repository.get_by_id(referee.id)
        if existing:
            raise HTTPException(status_code=409, detail=f"Referee {referee.id} already exists")
        db_referee = self.repository.create(referee)
        return RefereeResponse.model_validate(db_referee)

    def bulk_upsert_referees(self, referees: list[RefereeCreate]) -> BulkCreateResponse:
        created, updated = self.repository.bulk_upsert(referees)
        return BulkCreateResponse(created=created, updated=updated)

    def delete_referee(self, referee_id: int) -> None:
        if not self.repository.delete(referee_id):
            raise HTTPException(status_code=404, detail=f"Referee {referee_id} not found")
