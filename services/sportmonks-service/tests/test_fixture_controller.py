from unittest.mock import AsyncMock, patch


class TestGetFixtures:
    def test_returns_list_of_fixtures(self, client, mock_fixtures_response, mock_fixture_data):
        with patch("app.services.fixture_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_fixtures_response)

            response = client.get("/fixtures")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == mock_fixture_data["id"]
            assert data[0]["name"] == mock_fixture_data["name"]

    def test_calls_sportmonks_client_with_correct_endpoint(self, client, mock_fixtures_response):
        with patch("app.services.fixture_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_fixtures_response)

            client.get("/fixtures")

            mock_client.get.assert_called_once_with("football/fixtures")


class TestGetFixtureById:
    def test_returns_single_fixture(self, client, mock_fixture_response, mock_fixture_data):
        with patch("app.services.fixture_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_fixture_response)

            response = client.get("/fixtures/19134030")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == mock_fixture_data["id"]
            assert data["name"] == mock_fixture_data["name"]

    def test_calls_sportmonks_client_with_correct_endpoint(self, client, mock_fixture_response):
        with patch("app.services.fixture_service.sportmonks_client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_fixture_response)

            client.get("/fixtures/19134030")

            mock_client.get.assert_called_once_with("football/fixtures/19134030")
