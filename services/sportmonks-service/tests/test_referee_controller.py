from unittest.mock import AsyncMock, patch


class TestGetReferees:
    def test_returns_list_of_referees(self, client, mock_referees_response, mock_referee_data):
        with patch("app.services.referee_service.sportmonks_client") as mock_client:
            mock_client.get_all_pages = AsyncMock(return_value=mock_referees_response)

            response = client.get("/referees")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == mock_referee_data["id"]
            assert data[0]["name"] == mock_referee_data["name"]

    def test_calls_sportmonks_client_with_correct_endpoint(self, client, mock_referees_response):
        with patch("app.services.referee_service.sportmonks_client") as mock_client:
            mock_client.get_all_pages = AsyncMock(return_value=mock_referees_response)

            client.get("/referees")

            mock_client.get_all_pages.assert_called_once_with("football/referees")


class TestGetRefereeById:
    def test_returns_single_referee(self, client, mock_referee_response, mock_referee_data):
        with patch("app.services.referee_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_referee_response)

            response = client.get("/referees/15411")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == mock_referee_data["id"]
            assert data["name"] == mock_referee_data["name"]

    def test_calls_sportmonks_client_with_correct_endpoint(self, client, mock_referee_response):
        with patch("app.services.referee_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_referee_response)

            client.get("/referees/15411")

            mock_client.get.assert_called_once_with("football/referees/15411")
