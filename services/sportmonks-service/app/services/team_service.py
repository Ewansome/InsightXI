from app.clients.sportmonks_client import sportmonks_client
from app.models.team import Team, TeamResponse


class TeamService:
    def __init__(self) -> None:
        self.url_suffix = "football/teams"

    async def get_all_teams(self) -> list[Team]:
        response = await sportmonks_client.get(self.url_suffix)
        validated = TeamResponse(**response)
        return validated.data

    async def get_team_by_id(self, team_id: int) -> Team:
        response = await sportmonks_client.get(f"{self.url_suffix}/{team_id}")
        return Team(**response["data"])


team_service = TeamService()
