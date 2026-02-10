from pydantic import BaseModel


class TeamBase(BaseModel):
    id: int
    sport_id: int
    country_id: int | None = None
    venue_id: int | None = None
    gender: str | None = None
    name: str
    short_code: str | None = None
    image_path: str | None = None
    founded: int | None = None
    type: str | None = None
    placeholder: bool | None = None
    last_played_at: str | None = None


class TeamCreate(TeamBase):
    pass


class TeamResponse(TeamBase):
    model_config = {"from_attributes": True}


class BulkCreateResponse(BaseModel):
    created: int
    updated: int
