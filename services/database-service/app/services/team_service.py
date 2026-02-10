from fastapi import HTTPException

from app.repositories.team_repository import TeamRepository
from app.schemas.team import BulkCreateResponse, TeamCreate, TeamResponse


class TeamService:
    def __init__(self, repository: TeamRepository):
        self.repository = repository

    def get_all_teams(self) -> list[TeamResponse]:
        teams = self.repository.get_all()
        return [TeamResponse.model_validate(team) for team in teams]

    def get_team_by_id(self, team_id: int) -> TeamResponse:
        team = self.repository.get_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return TeamResponse.model_validate(team)

    def create_team(self, team: TeamCreate) -> TeamResponse:
        existing = self.repository.get_by_id(team.id)
        if existing:
            raise HTTPException(status_code=409, detail="Team already exists")
        created = self.repository.create(team)
        return TeamResponse.model_validate(created)

    def bulk_upsert_teams(self, teams: list[TeamCreate]) -> BulkCreateResponse:
        created, updated = self.repository.bulk_upsert(teams)
        return BulkCreateResponse(created=created, updated=updated)

    def delete_team(self, team_id: int) -> None:
        deleted = self.repository.delete(team_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Team not found")
