from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.clients.sportmonks_client import SportMonksClient


class TestSportMonksClient:
    @pytest.fixture
    def client(self):
        with patch("app.clients.sportmonks_client.settings") as mock_settings:
            mock_settings.base_url = "https://api.sportmonks.com/v3"
            mock_settings.api_key = "test_api_key"
            return SportMonksClient()

    @pytest.mark.asyncio
    async def test_get_includes_api_token_in_params(self, client):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            await client.get("football/leagues")

            mock_client_instance.get.assert_called_once()
            call_kwargs = mock_client_instance.get.call_args
            assert call_kwargs[1]["params"]["api_token"] == "test_api_key"

    @pytest.mark.asyncio
    async def test_get_constructs_correct_url(self, client):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            await client.get("football/leagues")

            call_args = mock_client_instance.get.call_args
            assert call_args[0][0] == "https://api.sportmonks.com/v3/football/leagues"

    @pytest.mark.asyncio
    async def test_get_merges_additional_params(self, client):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            await client.get("football/leagues", params={"include": "seasons"})

            call_kwargs = mock_client_instance.get.call_args
            assert call_kwargs[1]["params"]["api_token"] == "test_api_key"
            assert call_kwargs[1]["params"]["include"] == "seasons"

    @pytest.mark.asyncio
    async def test_get_all_pages_single_page(self, client):
        response_data = {
            "data": [{"id": 1}, {"id": 2}],
            "pagination": {"has_more": False},
        }

        with patch.object(client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = response_data

            result = await client.get_all_pages("football/leagues")

            assert result == [{"id": 1}, {"id": 2}]
            mock_get.assert_called_once_with(
                "football/leagues", params={"per_page": 50, "page": 1}
            )

    @pytest.mark.asyncio
    async def test_get_all_pages_multiple_pages(self, client):
        page_1 = {
            "data": [{"id": 1}, {"id": 2}],
            "pagination": {"has_more": True},
        }
        page_2 = {
            "data": [{"id": 3}],
            "pagination": {"has_more": False},
        }

        with patch.object(client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = [page_1, page_2]

            result = await client.get_all_pages("football/leagues")

            assert result == [{"id": 1}, {"id": 2}, {"id": 3}]
            assert mock_get.call_count == 2
            mock_get.assert_any_call(
                "football/leagues", params={"per_page": 50, "page": 1}
            )
            mock_get.assert_any_call(
                "football/leagues", params={"per_page": 50, "page": 2}
            )
