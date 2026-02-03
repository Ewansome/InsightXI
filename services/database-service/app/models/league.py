from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LeagueDB(Base):
    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sport_id: Mapped[int] = mapped_column(Integer, nullable=False)
    country_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    short_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_played_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    has_jerseys: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
