from unittest.mock import AsyncMock, patch

import pytest

from app.services.referee_service import RefereeService


class TestRefereeService:
    @pytest.fixture
    def service(self):
        return RefereeService()

    @pytest.mark.asyncio
    async def test_get_all_referees_returns_validated_referees(
        self, service, mock_referees_response, mock_referee_data
    ):
        with patch("app.services.referee_service.sportmonks_client") as mock_client:
            mock_client.get_all_pages = AsyncMock(return_value=mock_referees_response)

            result = await service.get_all_referees()

            assert len(result) == 1
            assert result[0].id == mock_referee_data["id"]
            assert result[0].name == mock_referee_data["name"]

    @pytest.mark.asyncio
    async def test_get_referee_by_id_returns_validated_referee(
        self, service, mock_referee_response, mock_referee_data
    ):
        with patch("app.services.referee_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_referee_response)

            result = await service.get_referee_by_id(15411)

            assert result.id == mock_referee_data["id"]
            assert result.name == mock_referee_data["name"]
