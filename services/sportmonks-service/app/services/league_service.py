from app.clients.sportmonks_client import sportmonks_client
from app.models.league import League


class LeagueService:
    def __init__(self):
        self.url_suffix = "football/leagues"

    async def get_all_leagues(self) -> list[League]:
        data = await sportmonks_client.get_all_pages(self.url_suffix)
        return [League(**item) for item in data]

    async def get_league_by_id(self, league_id: int) -> League:
        response = await sportmonks_client.get(f"{self.url_suffix}/{league_id}")
        return League(**response["data"])


league_service = LeagueService()
