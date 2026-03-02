from app.clients.sportmonks_client import sportmonks_client
from app.models.fixture import Fixture


class FixtureService:
    def __init__(self):
        self.url_suffix = "football/fixtures"

    async def get_all_fixtures(self) -> list[Fixture]:
        data = await sportmonks_client.get_all_pages(self.url_suffix)
        return [Fixture(**item) for item in data]

    async def get_fixture_by_id(self, fixture_id: int) -> Fixture:
        response = await sportmonks_client.get(f"{self.url_suffix}/{fixture_id}")
        return Fixture(**response["data"])


fixture_service = FixtureService()
