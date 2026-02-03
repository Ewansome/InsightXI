from unittest.mock import AsyncMock, patch


class TestGetLeagues:
    def test_returns_list_of_leagues(self, client, mock_leagues_response, mock_league_data):
        with patch("app.services.league_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_leagues_response)

            response = client.get("/leagues")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == mock_league_data["id"]
            assert data[0]["name"] == mock_league_data["name"]

    def test_calls_sportmonks_client_with_correct_endpoint(self, client, mock_leagues_response):
        with patch("app.services.league_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_leagues_response)

            client.get("/leagues")

            mock_client.get.assert_called_once_with("football/leagues")


class TestGetLeagueById:
    def test_returns_single_league(self, client, mock_league_response, mock_league_data):
        with patch("app.services.league_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_league_response)

            response = client.get("/leagues/271")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == mock_league_data["id"]
            assert data["name"] == mock_league_data["name"]

    def test_calls_sportmonks_client_with_correct_endpoint(self, client, mock_league_response):
        with patch("app.services.league_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_league_response)

            client.get("/leagues/271")

            mock_client.get.assert_called_once_with("football/leagues/271")
