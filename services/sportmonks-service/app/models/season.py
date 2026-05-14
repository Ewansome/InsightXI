from pydantic import BaseModel


class Season(BaseModel):
    id: int
    sport_id: int
    league_id: int
    tie_breaker_rule_id: int | None = None
    name: str
    finished: bool
    pending: bool
    is_current: bool
    starting_at: str | None = None
    ending_at: str | None = None
    standing_method: str | None = None
    games_in_current_week: bool | None = None


class SeasonResponse(BaseModel):
    data: list[Season]
