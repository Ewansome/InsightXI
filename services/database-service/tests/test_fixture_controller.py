class TestGetFixtures:
    def test_returns_empty_list_when_no_fixtures(self, client):
        response = client.get("/fixtures")

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_list_of_fixtures(self, client, mock_fixture_data):
        client.post("/fixtures", json=mock_fixture_data)

        response = client.get("/fixtures")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == mock_fixture_data["id"]


class TestGetFixtureById:
    def test_returns_fixture_when_exists(self, client, mock_fixture_data):
        client.post("/fixtures", json=mock_fixture_data)

        response = client.get(f"/fixtures/{mock_fixture_data['id']}")

        assert response.status_code == 200
        assert response.json()["name"] == mock_fixture_data["name"]

    def test_returns_404_when_not_found(self, client):
        response = client.get("/fixtures/999")

        assert response.status_code == 404


class TestCreateFixture:
    def test_creates_fixture(self, client, mock_fixture_data):
        response = client.post("/fixtures", json=mock_fixture_data)

        assert response.status_code == 201
        assert response.json()["id"] == mock_fixture_data["id"]
        assert response.json()["name"] == mock_fixture_data["name"]

    def test_returns_409_when_fixture_exists(self, client, mock_fixture_data):
        client.post("/fixtures", json=mock_fixture_data)

        response = client.post("/fixtures", json=mock_fixture_data)

        assert response.status_code == 409


class TestBulkUpsertFixtures:
    def test_creates_multiple_fixtures(self, client, mock_fixture_data):
        fixture2 = mock_fixture_data.copy()
        fixture2["id"] = 19134031
        fixture2["name"] = "Premier League"

        response = client.post("/fixtures/bulk", json=[mock_fixture_data, fixture2])

        assert response.status_code == 200
        assert response.json()["created"] == 2
        assert response.json()["updated"] == 0

    def test_updates_existing_fixtures(self, client, mock_fixture_data):
        client.post("/fixtures", json=mock_fixture_data)
        mock_fixture_data["name"] = "Updated Superliga"

        response = client.post("/fixtures/bulk", json=[mock_fixture_data])

        assert response.status_code == 200
        assert response.json()["created"] == 0
        assert response.json()["updated"] == 1


class TestDeleteFixture:
    def test_deletes_existing_fixture(self, client, mock_fixture_data):
        client.post("/fixtures", json=mock_fixture_data)

        response = client.delete(f"/fixtures/{mock_fixture_data['id']}")

        assert response.status_code == 204

    def test_returns_404_when_not_found(self, client):
        response = client.delete("/fixtures/999")

        assert response.status_code == 404
