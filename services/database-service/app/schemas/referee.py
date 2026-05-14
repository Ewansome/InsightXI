from pydantic import BaseModel


class RefereeBase(BaseModel):
    id: int
    sport_id: int
    country_id: int | None = None
    nationality_id: int | None = None
    city_id: int | None = None
    common_name: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    name: str
    display_name: str | None = None
    image_path: str | None = None
    height: int | None = None
    weight: int | None = None
    date_of_birth: str | None = None
    gender: str | None = None


class RefereeCreate(RefereeBase):
    pass


class RefereeResponse(RefereeBase):
    model_config = {"from_attributes": True}


class BulkCreateResponse(BaseModel):
    created: int
    updated: int
