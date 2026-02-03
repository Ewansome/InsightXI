from app.clients.sportmonks_client import sportmonks_client
from app.models.league import League, LeagueResponse


class LeagueService:
    def __init__(self):
        self.url_suffix = "football/leagues"

    async def get_all_leagues(self) -> list[League]:
        response = await sportmonks_client.get(self.url_suffix)
        validated = LeagueResponse(**response)
        return validated.data

    async def get_league_by_id(self, league_id: int) -> League:
        response = await sportmonks_client.get(f"{self.url_suffix}/{league_id}")
        return League(**response["data"])


league_service = LeagueService()
