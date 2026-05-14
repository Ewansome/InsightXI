from unittest.mock import AsyncMock, patch

import pytest

from app.services.referee_sync_service import RefereeSyncService


class TestRefereeSyncService:
    @pytest.fixture
    def service(self):
        return RefereeSyncService()

    @pytest.mark.asyncio
    async def test_sync_fetches_and_stores_referees(self, service, mock_referees, mock_bulk_result):
        with (
            patch("app.services.referee_sync_service.sportmonks_service_client") as mock_sportmonks,
            patch("app.services.referee_sync_service.database_service_client") as mock_database,
        ):
            mock_sportmonks.get_referees = AsyncMock(return_value=mock_referees)
            mock_database.bulk_upsert_referees = AsyncMock(return_value=mock_bulk_result)

            result = await service.sync_referees()

            assert result.entity == "referees"
            assert result.created == 2
            assert result.updated == 0
            assert result.status == "completed"
            mock_sportmonks.get_referees.assert_called_once()
            mock_database.bulk_upsert_referees.assert_called_once_with(mock_referees)
