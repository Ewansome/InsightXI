import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_league_data():
    return {
        "id": 271,
        "sport_id": 1,
        "country_id": 320,
        "name": "Superliga",
        "active": True,
        "short_code": "DNK SL",
        "image_path": "https://cdn.sportmonks.com/images/soccer/leagues/271.png",
        "type": "league",
        "sub_type": "domestic",
        "last_played_at": "2025-12-08 18:00:00",
        "category": 2,
        "has_jerseys": False,
    }


@pytest.fixture
def mock_leagues_response(mock_league_data):
    return {"data": [mock_league_data]}


@pytest.fixture
def mock_league_response(mock_league_data):
    return {"data": mock_league_data}


@pytest.fixture
def mock_team_data():
    return {
        "id": 1,
        "sport_id": 1,
        "country_id": 462,
        "venue_id": 214,
        "gender": "male",
        "name": "West Ham United",
        "short_code": "WHU",
        "image_path": "https://cdn.sportmonks.com/images/soccer/teams/1/1.png",
        "founded": 1895,
        "type": "domestic",
        "placeholder": False,
        "last_played_at": "2025-12-08 18:00:00",
    }


@pytest.fixture
def mock_teams_response(mock_team_data):
    return {"data": [mock_team_data]}


@pytest.fixture
def mock_team_response(mock_team_data):
    return {"data": mock_team_data}


@pytest.fixture
def mock_fixture_data():
    return {
        "id": 19134030,
        "sport_id": 1,
        "league_id": 271,
        "season_id": 23584,
        "stage_id": 77471898,
        "group_id": None,
        "aggregate_id": None,
        "round_id": 339304,
        "state_id": 5,
        "venue_id": 8909,
        "name": "Superliga",
        "starting_at": "2025-12-08 18:00:00",
        "result_info": "Game ended in draw",
        "leg": "1/1",
        "details": None,
        "length": 90,
        "placeholder": False,
        "has_odds": True,
        "starting_at_timestamp": 1733677200,
    }


@pytest.fixture
def mock_fixtures_response(mock_fixture_data):
    return {"data": [mock_fixture_data]}


@pytest.fixture
def mock_fixture_response(mock_fixture_data):
    return {"data": mock_fixture_data}
