from unittest.mock import AsyncMock, patch


class TestSyncLeagues:
    def test_sync_leagues_returns_result(self, client, mock_leagues, mock_bulk_result):
        with (
            patch("app.services.league_sync_service.sportmonks_service_client") as mock_sportmonks,
            patch("app.services.league_sync_service.database_service_client") as mock_database,
        ):
            mock_sportmonks.get_leagues = AsyncMock(return_value=mock_leagues)
            mock_database.bulk_upsert_leagues = AsyncMock(return_value=mock_bulk_result)

            response = client.post("/sync/leagues")

            assert response.status_code == 200
            data = response.json()
            assert data["entity"] == "leagues"
            assert data["created"] == 2
            assert data["updated"] == 0
            assert data["status"] == "completed"

    def test_sync_leagues_calls_sportmonks_service(self, client, mock_leagues, mock_bulk_result):
        with (
            patch("app.services.league_sync_service.sportmonks_service_client") as mock_sportmonks,
            patch("app.services.league_sync_service.database_service_client") as mock_database,
        ):
            mock_sportmonks.get_leagues = AsyncMock(return_value=mock_leagues)
            mock_database.bulk_upsert_leagues = AsyncMock(return_value=mock_bulk_result)

            client.post("/sync/leagues")

            mock_sportmonks.get_leagues.assert_called_once()

    def test_sync_leagues_sends_data_to_database_service(self, client, mock_leagues, mock_bulk_result):
        with (
            patch("app.services.league_sync_service.sportmonks_service_client") as mock_sportmonks,
            patch("app.services.league_sync_service.database_service_client") as mock_database,
        ):
            mock_sportmonks.get_leagues = AsyncMock(return_value=mock_leagues)
            mock_database.bulk_upsert_leagues = AsyncMock(return_value=mock_bulk_result)

            client.post("/sync/leagues")

            mock_database.bulk_upsert_leagues.assert_called_once_with(mock_leagues)
