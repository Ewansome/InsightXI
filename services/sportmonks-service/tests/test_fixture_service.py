from unittest.mock import AsyncMock, patch

import pytest

from app.services.fixture_service import FixtureService


class TestFixtureService:
    @pytest.fixture
    def service(self):
        return FixtureService()

    @pytest.mark.asyncio
    async def test_get_all_fixtures_returns_validated_fixtures(
        self, service, mock_fixtures_response, mock_fixture_data
    ):
        with patch("app.services.fixture_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_fixtures_response)

            result = await service.get_all_fixtures()

            assert len(result) == 1
            assert result[0].id == mock_fixture_data["id"]
            assert result[0].name == mock_fixture_data["name"]

    @pytest.mark.asyncio
    async def test_get_fixture_by_id_returns_validated_fixture(
        self, service, mock_fixture_response, mock_fixture_data
    ):
        with patch("app.services.fixture_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_fixture_response)

            result = await service.get_fixture_by_id(19134030)

            assert result.id == mock_fixture_data["id"]
            assert result.name == mock_fixture_data["name"]
