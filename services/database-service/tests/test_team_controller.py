def test_get_teams_empty(client):
    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == []


def test_create_team(client, mock_team_data):
    response = client.post("/teams", json=mock_team_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == mock_team_data["id"]
    assert data["name"] == mock_team_data["name"]
    assert data["short_code"] == mock_team_data["short_code"]


def test_create_team_duplicate(client, mock_team_data):
    client.post("/teams", json=mock_team_data)
    response = client.post("/teams", json=mock_team_data)
    assert response.status_code == 409


def test_get_team_by_id(client, mock_team_data):
    client.post("/teams", json=mock_team_data)
    response = client.get(f"/teams/{mock_team_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_team_data["id"]
    assert data["name"] == mock_team_data["name"]


def test_get_team_not_found(client):
    response = client.get("/teams/999")
    assert response.status_code == 404


def test_bulk_upsert_teams(client, mock_team_data):
    teams = [mock_team_data]
    response = client.post("/teams/bulk", json=teams)
    assert response.status_code == 200
    data = response.json()
    assert data["created"] == 1
    assert data["updated"] == 0


def test_bulk_upsert_teams_update(client, mock_team_data):
    client.post("/teams", json=mock_team_data)
    updated_team = {**mock_team_data, "name": "Updated Team Name"}
    response = client.post("/teams/bulk", json=[updated_team])
    assert response.status_code == 200
    data = response.json()
    assert data["created"] == 0
    assert data["updated"] == 1

    get_response = client.get(f"/teams/{mock_team_data['id']}")
    assert get_response.json()["name"] == "Updated Team Name"


def test_delete_team(client, mock_team_data):
    client.post("/teams", json=mock_team_data)
    response = client.delete(f"/teams/{mock_team_data['id']}")
    assert response.status_code == 204

    get_response = client.get(f"/teams/{mock_team_data['id']}")
    assert get_response.status_code == 404


def test_delete_team_not_found(client):
    response = client.delete("/teams/999")
    assert response.status_code == 404
