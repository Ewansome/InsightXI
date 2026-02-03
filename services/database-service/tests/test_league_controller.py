class TestGetLeagues:
    def test_returns_empty_list_when_no_leagues(self, client):
        response = client.get("/leagues")

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_list_of_leagues(self, client, mock_league_data):
        client.post("/leagues", json=mock_league_data)

        response = client.get("/leagues")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == mock_league_data["id"]


class TestGetLeagueById:
    def test_returns_league_when_exists(self, client, mock_league_data):
        client.post("/leagues", json=mock_league_data)

        response = client.get(f"/leagues/{mock_league_data['id']}")

        assert response.status_code == 200
        assert response.json()["name"] == mock_league_data["name"]

    def test_returns_404_when_not_found(self, client):
        response = client.get("/leagues/999")

        assert response.status_code == 404


class TestCreateLeague:
    def test_creates_league(self, client, mock_league_data):
        response = client.post("/leagues", json=mock_league_data)

        assert response.status_code == 201
        assert response.json()["id"] == mock_league_data["id"]
        assert response.json()["name"] == mock_league_data["name"]

    def test_returns_409_when_league_exists(self, client, mock_league_data):
        client.post("/leagues", json=mock_league_data)

        response = client.post("/leagues", json=mock_league_data)

        assert response.status_code == 409


class TestBulkUpsertLeagues:
    def test_creates_multiple_leagues(self, client, mock_league_data):
        league2 = mock_league_data.copy()
        league2["id"] = 501
        league2["name"] = "Premiership"

        response = client.post("/leagues/bulk", json=[mock_league_data, league2])

        assert response.status_code == 200
        assert response.json()["created"] == 2
        assert response.json()["updated"] == 0

    def test_updates_existing_leagues(self, client, mock_league_data):
        client.post("/leagues", json=mock_league_data)
        mock_league_data["name"] = "Updated Superliga"

        response = client.post("/leagues/bulk", json=[mock_league_data])

        assert response.status_code == 200
        assert response.json()["created"] == 0
        assert response.json()["updated"] == 1


class TestDeleteLeague:
    def test_deletes_existing_league(self, client, mock_league_data):
        client.post("/leagues", json=mock_league_data)

        response = client.delete(f"/leagues/{mock_league_data['id']}")

        assert response.status_code == 204

    def test_returns_404_when_not_found(self, client):
        response = client.delete("/leagues/999")

        assert response.status_code == 404
