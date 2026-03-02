from pydantic import BaseModel


class Fixture(BaseModel):
    id: int
    sport_id: int
    league_id: int
    season_id: int
    stage_id: int | None = None
    group_id: int | None = None
    aggregate_id: int | None = None
    round_id: int | None = None
    state_id: int
    venue_id: int | None = None
    name: str | None = None
    starting_at: str | None = None
    result_info: str | None = None
    leg: str | None = None
    details: str | None = None
    length: int | None = None
    placeholder: bool
    has_odds: bool
    starting_at_timestamp: int | None = None


class FixtureResponse(BaseModel):
    data: list[Fixture]
