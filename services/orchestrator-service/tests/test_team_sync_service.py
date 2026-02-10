from unittest.mock import AsyncMock, patch

import pytest

from app.services.team_sync_service import team_sync_service


@pytest.mark.asyncio
async def test_sync_teams(mock_teams, mock_bulk_result):
    with (
        patch(
            "app.services.team_sync_service.sportmonks_service_client.get_teams",
            new_callable=AsyncMock,
        ) as mock_get_teams,
        patch(
            "app.services.team_sync_service.database_service_client.bulk_upsert_teams",
            new_callable=AsyncMock,
        ) as mock_bulk_upsert,
    ):
        mock_get_teams.return_value = mock_teams
        mock_bulk_upsert.return_value = mock_bulk_result

        result = await team_sync_service.sync_teams()

        mock_get_teams.assert_called_once()
        mock_bulk_upsert.assert_called_once_with(mock_teams)

        assert result.entity == "teams"
        assert result.created == 2
        assert result.updated == 0
        assert result.status == "completed"
