from pydantic import BaseModel


class Referee(BaseModel):
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


class RefereeResponse(BaseModel):
    data: list[Referee]
