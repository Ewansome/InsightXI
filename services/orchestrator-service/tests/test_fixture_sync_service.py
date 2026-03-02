from unittest.mock import AsyncMock, patch

import pytest

from app.services.fixture_sync_service import FixtureSyncService


class TestFixtureSyncService:
    @pytest.fixture
    def service(self):
        return FixtureSyncService()

    @pytest.mark.asyncio
    async def test_sync_fetches_and_stores_fixtures(self, service, mock_fixtures, mock_bulk_result):
        with (
            patch("app.services.fixture_sync_service.sportmonks_service_client") as mock_sportmonks,
            patch("app.services.fixture_sync_service.database_service_client") as mock_database,
        ):
            mock_sportmonks.get_fixtures = AsyncMock(return_value=mock_fixtures)
            mock_database.bulk_upsert_fixtures = AsyncMock(return_value=mock_bulk_result)

            result = await service.sync_fixtures()

            assert result.entity == "fixtures"
            assert result.created == 2
            assert result.updated == 0
            assert result.status == "completed"
            mock_sportmonks.get_fixtures.assert_called_once()
            mock_database.bulk_upsert_fixtures.assert_called_once_with(mock_fixtures)
