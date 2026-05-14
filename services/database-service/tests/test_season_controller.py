class TestGetSeasons:
    def test_returns_empty_list_when_no_seasons(self, client):
        response = client.get("/seasons")

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_list_of_seasons(self, client, mock_season_data):
        client.post("/seasons", json=mock_season_data)

        response = client.get("/seasons")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == mock_season_data["id"]


class TestGetSeasonById:
    def test_returns_season_when_exists(self, client, mock_season_data):
        client.post("/seasons", json=mock_season_data)

        response = client.get(f"/seasons/{mock_season_data['id']}")

        assert response.status_code == 200
        assert response.json()["name"] == mock_season_data["name"]

    def test_returns_404_when_not_found(self, client):
        response = client.get("/seasons/999")

        assert response.status_code == 404


class TestCreateSeason:
    def test_creates_season(self, client, mock_season_data):
        response = client.post("/seasons", json=mock_season_data)

        assert response.status_code == 201
        assert response.json()["id"] == mock_season_data["id"]
        assert response.json()["name"] == mock_season_data["name"]

    def test_returns_409_when_season_exists(self, client, mock_season_data):
        client.post("/seasons", json=mock_season_data)

        response = client.post("/seasons", json=mock_season_data)

        assert response.status_code == 409


class TestBulkUpsertSeasons:
    def test_creates_multiple_seasons(self, client, mock_season_data):
        season2 = mock_season_data.copy()
        season2["id"] = 23585
        season2["name"] = "2023/2024"

        response = client.post("/seasons/bulk", json=[mock_season_data, season2])

        assert response.status_code == 200
        assert response.json()["created"] == 2
        assert response.json()["updated"] == 0

    def test_updates_existing_seasons(self, client, mock_season_data):
        client.post("/seasons", json=mock_season_data)
        mock_season_data["name"] = "Updated 2024/2025"

        response = client.post("/seasons/bulk", json=[mock_season_data])

        assert response.status_code == 200
        assert response.json()["created"] == 0
        assert response.json()["updated"] == 1


class TestDeleteSeason:
    def test_deletes_existing_season(self, client, mock_season_data):
        client.post("/seasons", json=mock_season_data)

        response = client.delete(f"/seasons/{mock_season_data['id']}")

        assert response.status_code == 204

    def test_returns_404_when_not_found(self, client):
        response = client.delete("/seasons/999")

        assert response.status_code == 404
