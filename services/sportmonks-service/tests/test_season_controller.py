from unittest.mock import AsyncMock, patch


class TestGetSeasons:
    def test_returns_list_of_seasons(self, client, mock_seasons_response, mock_season_data):
        with patch("app.services.season_service.sportmonks_client") as mock_client:
            mock_client.get_all_pages = AsyncMock(return_value=mock_seasons_response)

            response = client.get("/seasons")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == mock_season_data["id"]
            assert data[0]["name"] == mock_season_data["name"]

    def test_calls_sportmonks_client_with_correct_endpoint(self, client, mock_seasons_response):
        with patch("app.services.season_service.sportmonks_client") as mock_client:
            mock_client.get_all_pages = AsyncMock(return_value=mock_seasons_response)

            client.get("/seasons")

            mock_client.get_all_pages.assert_called_once_with("football/seasons")


class TestGetSeasonById:
    def test_returns_single_season(self, client, mock_season_response, mock_season_data):
        with patch("app.services.season_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_season_response)

            response = client.get("/seasons/23584")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == mock_season_data["id"]
            assert data["name"] == mock_season_data["name"]

    def test_calls_sportmonks_client_with_correct_endpoint(self, client, mock_season_response):
        with patch("app.services.season_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_season_response)

            client.get("/seasons/23584")

            mock_client.get.assert_called_once_with("football/seasons/23584")
