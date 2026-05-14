from unittest.mock import AsyncMock, patch

import pytest

from app.services.season_service import SeasonService


class TestSeasonService:
    @pytest.fixture
    def service(self):
        return SeasonService()

    @pytest.mark.asyncio
    async def test_get_all_seasons_returns_validated_seasons(
        self, service, mock_seasons_response, mock_season_data
    ):
        with patch("app.services.season_service.sportmonks_client") as mock_client:
            mock_client.get_all_pages = AsyncMock(return_value=mock_seasons_response)

            result = await service.get_all_seasons()

            assert len(result) == 1
            assert result[0].id == mock_season_data["id"]
            assert result[0].name == mock_season_data["name"]

    @pytest.mark.asyncio
    async def test_get_season_by_id_returns_validated_season(
        self, service, mock_season_response, mock_season_data
    ):
        with patch("app.services.season_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_season_response)

            result = await service.get_season_by_id(23584)

            assert result.id == mock_season_data["id"]
            assert result.name == mock_season_data["name"]
