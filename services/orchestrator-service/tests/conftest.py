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
