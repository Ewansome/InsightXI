import httpx

from app.config import settings


class SportMonksServiceClient:
    def __init__(self):
        self.base_url = settings.sportmonks_service_url

    async def get_leagues(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/leagues")
            response.raise_for_status()
            return response.json()

    async def get_league(self, league_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/leagues/{league_id}")
            response.raise_for_status()
            return response.json()

    async def get_teams(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/teams")
            response.raise_for_status()
            return response.json()

    async def get_team(self, team_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/teams/{team_id}")
            response.raise_for_status()
            return response.json()


sportmonks_service_client = SportMonksServiceClient()
