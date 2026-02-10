from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TeamDB(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sport_id: Mapped[int] = mapped_column(Integer, nullable=False)
    country_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    venue_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    founded: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    placeholder: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    last_played_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
