from fastapi import HTTPException

from app.repositories.league_repository import LeagueRepository
from app.schemas.league import LeagueCreate, LeagueResponse, BulkCreateResponse


class LeagueService:
    def __init__(self, repository: LeagueRepository):
        self.repository = repository

    def get_all_leagues(self) -> list[LeagueResponse]:
        leagues = self.repository.get_all()
        return [LeagueResponse.model_validate(league) for league in leagues]

    def get_league_by_id(self, league_id: int) -> LeagueResponse:
        league = self.repository.get_by_id(league_id)
        if not league:
            raise HTTPException(status_code=404, detail=f"League {league_id} not found")
        return LeagueResponse.model_validate(league)

    def create_league(self, league: LeagueCreate) -> LeagueResponse:
        existing = self.repository.get_by_id(league.id)
        if existing:
            raise HTTPException(status_code=409, detail=f"League {league.id} already exists")
        db_league = self.repository.create(league)
        return LeagueResponse.model_validate(db_league)

    def bulk_upsert_leagues(self, leagues: list[LeagueCreate]) -> BulkCreateResponse:
        created, updated = self.repository.bulk_upsert(leagues)
        return BulkCreateResponse(created=created, updated=updated)

    def delete_league(self, league_id: int) -> None:
        if not self.repository.delete(league_id):
            raise HTTPException(status_code=404, detail=f"League {league_id} not found")
