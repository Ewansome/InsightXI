import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_leagues():
    return [
        {
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
        },
        {
            "id": 501,
            "sport_id": 1,
            "country_id": 1161,
            "name": "Premiership",
            "active": True,
            "short_code": "SCO P",
            "image_path": "https://cdn.sportmonks.com/images/soccer/leagues/501.png",
            "type": "league",
            "sub_type": "domestic",
            "last_played_at": "2026-02-01 15:00:00",
            "category": 2,
            "has_jerseys": False,
        },
    ]


@pytest.fixture
def mock_bulk_result():
    return {"created": 2, "updated": 0}


@pytest.fixture
def mock_teams():
    return [
        {
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
        },
        {
            "id": 2,
            "sport_id": 1,
            "country_id": 462,
            "venue_id": 215,
            "gender": "male",
            "name": "Manchester United",
            "short_code": "MUN",
            "image_path": "https://cdn.sportmonks.com/images/soccer/teams/2/2.png",
            "founded": 1878,
            "type": "domestic",
            "placeholder": False,
            "last_played_at": "2025-12-08 18:00:00",
        },
    ]


@pytest.fixture
def mock_fixtures():
    return [
        {
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
        },
        {
            "id": 19134031,
            "sport_id": 1,
            "league_id": 501,
            "season_id": 23585,
            "stage_id": 77471899,
            "group_id": None,
            "aggregate_id": None,
            "round_id": 339305,
            "state_id": 5,
            "venue_id": 8910,
            "name": "Premiership",
            "starting_at": "2026-02-01 15:00:00",
            "result_info": "Home team won",
            "leg": "1/1",
            "details": None,
            "length": 90,
            "placeholder": False,
            "has_odds": True,
            "starting_at_timestamp": 1738418400,
        },
    ]
