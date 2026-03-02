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

    async def get_all_pages(
        self, endpoint: str, params: dict | None = None
    ) -> list[dict]:
        all_data = []
        page = 1

        while True:
            page_params = {"per_page": 50, "page": page}
            if params:
                page_params.update(params)

            response = await self.get(endpoint, params=page_params)
            all_data.extend(response["data"])

            if not response.get("pagination", {}).get("has_more", False):
                break

            page += 1

        return all_data


sportmonks_client = SportMonksClient()
