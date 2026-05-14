from fastapi import HTTPException

from app.repositories.season_repository import SeasonRepository
from app.schemas.season import BulkCreateResponse, SeasonCreate, SeasonResponse


class SeasonService:
    def __init__(self, repository: SeasonRepository):
        self.repository = repository

    def get_all_seasons(self) -> list[SeasonResponse]:
        seasons = self.repository.get_all()
        return [SeasonResponse.model_validate(season) for season in seasons]

    def get_season_by_id(self, season_id: int) -> SeasonResponse:
        season = self.repository.get_by_id(season_id)
        if not season:
            raise HTTPException(status_code=404, detail=f"Season {season_id} not found")
        return SeasonResponse.model_validate(season)

    def create_season(self, season: SeasonCreate) -> SeasonResponse:
        existing = self.repository.get_by_id(season.id)
        if existing:
            raise HTTPException(status_code=409, detail=f"Season {season.id} already exists")
        db_season = self.repository.create(season)
        return SeasonResponse.model_validate(db_season)

    def bulk_upsert_seasons(self, seasons: list[SeasonCreate]) -> BulkCreateResponse:
        created, updated = self.repository.bulk_upsert(seasons)
        return BulkCreateResponse(created=created, updated=updated)

    def delete_season(self, season_id: int) -> None:
        if not self.repository.delete(season_id):
            raise HTTPException(status_code=404, detail=f"Season {season_id} not found")
