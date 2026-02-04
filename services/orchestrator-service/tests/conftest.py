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
