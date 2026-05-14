from pydantic import BaseModel


class SeasonBase(BaseModel):
    id: int
    sport_id: int
    league_id: int
    tie_breaker_rule_id: int | None = None
    name: str
    finished: bool = False
    pending: bool = False
    is_current: bool = False
    starting_at: str | None = None
    ending_at: str | None = None
    standing_method: str | None = None
    games_in_current_week: bool | None = None


class SeasonCreate(SeasonBase):
    pass


class SeasonResponse(SeasonBase):
    model_config = {"from_attributes": True}


class BulkCreateResponse(BaseModel):
    created: int
    updated: int
