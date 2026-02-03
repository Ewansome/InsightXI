import httpx
from app.config import settings


class SportMonksClient:
    def __init__(self):
        self.base_url = settings.base_url
        self.api_token = settings.api_key

    async def get(self, endpoint: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            request_params = {"api_token": self.api_token}
            if params:
                request_params.update(params)

            response = await client.get(
                f"{self.base_url}/{endpoint}",
                params=request_params,
            )
            response.raise_for_status()
            return response.json()


sportmonks_client = SportMonksClient()
