import pytest
from unittest.mock import AsyncMock, patch

from app.services.league_service import LeagueService


class TestLeagueService:
    @pytest.fixture
    def service(self):
        return LeagueService()

    @pytest.mark.asyncio
    async def test_get_all_leagues_returns_validated_leagues(
        self, service, mock_leagues_response, mock_league_data
    ):
        with patch("app.services.league_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_leagues_response)

            result = await service.get_all_leagues()

            assert len(result) == 1
            assert result[0].id == mock_league_data["id"]
            assert result[0].name == mock_league_data["name"]

    @pytest.mark.asyncio
    async def test_get_league_by_id_returns_validated_league(
        self, service, mock_league_response, mock_league_data
    ):
        with patch("app.services.league_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_league_response)

            result = await service.get_league_by_id(271)

            assert result.id == mock_league_data["id"]
            assert result.name == mock_league_data["name"]
