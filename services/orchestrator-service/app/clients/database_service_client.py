import httpx

from app.config import settings


class DatabaseServiceClient:
    def __init__(self):
        self.base_url = settings.database_service_url

    async def bulk_upsert_leagues(self, leagues: list[dict]) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/leagues/bulk", json=leagues)
            response.raise_for_status()
            return response.json()

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

    async def bulk_upsert_teams(self, teams: list[dict]) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/teams/bulk", json=teams)
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


database_service_client = DatabaseServiceClient()
