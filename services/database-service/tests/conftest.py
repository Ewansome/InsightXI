import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


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
