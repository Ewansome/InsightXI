class TestGetReferees:
    def test_returns_empty_list_when_no_referees(self, client):
        response = client.get("/referees")

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_list_of_referees(self, client, mock_referee_data):
        client.post("/referees", json=mock_referee_data)

        response = client.get("/referees")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == mock_referee_data["id"]


class TestGetRefereeById:
    def test_returns_referee_when_exists(self, client, mock_referee_data):
        client.post("/referees", json=mock_referee_data)

        response = client.get(f"/referees/{mock_referee_data['id']}")

        assert response.status_code == 200
        assert response.json()["name"] == mock_referee_data["name"]

    def test_returns_404_when_not_found(self, client):
        response = client.get("/referees/999")

        assert response.status_code == 404


class TestCreateReferee:
    def test_creates_referee(self, client, mock_referee_data):
        response = client.post("/referees", json=mock_referee_data)

        assert response.status_code == 201
        assert response.json()["id"] == mock_referee_data["id"]
        assert response.json()["name"] == mock_referee_data["name"]

    def test_returns_409_when_referee_exists(self, client, mock_referee_data):
        client.post("/referees", json=mock_referee_data)

        response = client.post("/referees", json=mock_referee_data)

        assert response.status_code == 409


class TestBulkUpsertReferees:
    def test_creates_multiple_referees(self, client, mock_referee_data):
        referee2 = mock_referee_data.copy()
        referee2["id"] = 15412
        referee2["name"] = "Anthony Taylor"

        response = client.post("/referees/bulk", json=[mock_referee_data, referee2])

        assert response.status_code == 200
        assert response.json()["created"] == 2
        assert response.json()["updated"] == 0

    def test_updates_existing_referees(self, client, mock_referee_data):
        client.post("/referees", json=mock_referee_data)
        mock_referee_data["name"] = "Updated Michael Oliver"

        response = client.post("/referees/bulk", json=[mock_referee_data])

        assert response.status_code == 200
        assert response.json()["created"] == 0
        assert response.json()["updated"] == 1


class TestDeleteReferee:
    def test_deletes_existing_referee(self, client, mock_referee_data):
        client.post("/referees", json=mock_referee_data)

        response = client.delete(f"/referees/{mock_referee_data['id']}")

        assert response.status_code == 204

    def test_returns_404_when_not_found(self, client):
        response = client.delete("/referees/999")

        assert response.status_code == 404
