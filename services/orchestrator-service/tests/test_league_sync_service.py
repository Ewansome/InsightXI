from unittest.mock import AsyncMock, patch

import pytest

from app.services.league_sync_service import LeagueSyncService


class TestLeagueSyncService:
    @pytest.fixture
    def service(self):
        return LeagueSyncService()

    @pytest.mark.asyncio
    async def test_sync_fetches_and_stores_leagues(self, service, mock_leagues, mock_bulk_result):
        with (
            patch("app.services.league_sync_service.sportmonks_service_client") as mock_sportmonks,
            patch("app.services.league_sync_service.database_service_client") as mock_database,
        ):
            mock_sportmonks.get_leagues = AsyncMock(return_value=mock_leagues)
            mock_database.bulk_upsert_leagues = AsyncMock(return_value=mock_bulk_result)

            result = await service.sync_leagues()

            assert result.entity == "leagues"
            assert result.created == 2
            assert result.updated == 0
            assert result.status == "completed"
            mock_sportmonks.get_leagues.assert_called_once()
            mock_database.bulk_upsert_leagues.assert_called_once_with(mock_leagues)
