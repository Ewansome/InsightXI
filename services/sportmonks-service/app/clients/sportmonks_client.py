import time

import httpx
import structlog

from app.config import settings

logger = structlog.get_logger()


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
        start = time.perf_counter()

        logger.info("pagination_started", endpoint=endpoint)

        while True:
            page_start = time.perf_counter()
            page_params = {"per_page": 50, "page": page}
            if params:
                page_params.update(params)

            response = await self.get(endpoint, params=page_params)
            items = response["data"]
            all_data.extend(items)

            page_duration_ms = int((time.perf_counter() - page_start) * 1000)
            logger.info("page_fetched", endpoint=endpoint, page=page, items=len(items), duration_ms=page_duration_ms)

            if not response.get("pagination", {}).get("has_more", False):
                break

            page += 1

        total_duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "pagination_completed",
            endpoint=endpoint,
            total_pages=page,
            total_items=len(all_data),
            duration_ms=total_duration_ms,
        )

        return all_data


sportmonks_client = SportMonksClient()
