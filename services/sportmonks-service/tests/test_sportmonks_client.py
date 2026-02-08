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
