from pydantic import BaseModel


class League(BaseModel):
    id: int
    sport_id: int
    country_id: int | None = None
    name: str
    active: bool
    short_code: str | None = None
    image_path: str | None = None
    type: str | None = None
    sub_type: str | None = None
    last_played_at: str | None = None
    category: int | None = None
    has_jerseys: bool | None = None


class LeagueResponse(BaseModel):
    data: list[League]
