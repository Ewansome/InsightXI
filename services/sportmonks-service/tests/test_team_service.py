from unittest.mock import AsyncMock, patch

import pytest

from app.models.team import Team
from app.services.team_service import team_service


@pytest.mark.asyncio
async def test_get_all_teams(mock_teams_response, mock_team_data):
    with patch.object(
        team_service, "get_all_teams", new_callable=AsyncMock
    ) as mock_get_all:
        mock_get_all.return_value = [Team(**mock_team_data)]

        result = await team_service.get_all_teams()

        assert len(result) == 1
        assert result[0].id == mock_team_data["id"]
        assert result[0].name == mock_team_data["name"]
        assert result[0].short_code == mock_team_data["short_code"]


@pytest.mark.asyncio
async def test_get_team_by_id(mock_team_data):
    with patch.object(
        team_service, "get_team_by_id", new_callable=AsyncMock
    ) as mock_get_by_id:
        mock_get_by_id.return_value = Team(**mock_team_data)

        result = await team_service.get_team_by_id(1)

        assert result.id == mock_team_data["id"]
        assert result.name == mock_team_data["name"]
        assert result.country_id == mock_team_data["country_id"]
        assert result.venue_id == mock_team_data["venue_id"]
