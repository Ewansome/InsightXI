from unittest.mock import AsyncMock, patch

import pytest

from app.services.season_sync_service import SeasonSyncService


class TestSeasonSyncService:
    @pytest.fixture
    def service(self):
        return SeasonSyncService()

    @pytest.mark.asyncio
    async def test_sync_fetches_and_stores_seasons(self, service, mock_seasons, mock_bulk_result):
        with (
            patch("app.services.season_sync_service.sportmonks_service_client") as mock_sportmonks,
            patch("app.services.season_sync_service.database_service_client") as mock_database,
        ):
            mock_sportmonks.get_seasons = AsyncMock(return_value=mock_seasons)
            mock_database.bulk_upsert_seasons = AsyncMock(return_value=mock_bulk_result)

            result = await service.sync_seasons()

            assert result.entity == "seasons"
            assert result.created == 2
            assert result.updated == 0
            assert result.status == "completed"
            mock_sportmonks.get_seasons.assert_called_once()
            mock_database.bulk_upsert_seasons.assert_called_once_with(mock_seasons)
