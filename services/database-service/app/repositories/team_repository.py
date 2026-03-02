import time

import structlog
from sqlalchemy.orm import Session

from app.models.team import TeamDB
from app.schemas.team import TeamCreate

logger = structlog.get_logger()


class TeamRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[TeamDB]:
        return self.db.query(TeamDB).all()

    def get_by_id(self, team_id: int) -> TeamDB | None:
        return self.db.query(TeamDB).filter(TeamDB.id == team_id).first()

    def create(self, team: TeamCreate) -> TeamDB:
        db_team = TeamDB(**team.model_dump())
        self.db.add(db_team)
        self.db.commit()
        self.db.refresh(db_team)
        return db_team

    def bulk_upsert(self, teams: list[TeamCreate]) -> tuple[int, int]:
        logger.info("bulk_upsert_started", entity="teams", records=len(teams))
        start = time.perf_counter()

        created = 0
        updated = 0

        for team in teams:
            existing = self.get_by_id(team.id)
            if existing:
                for key, value in team.model_dump().items():
                    setattr(existing, key, value)
                updated += 1
            else:
                self.db.add(TeamDB(**team.model_dump()))
                created += 1

        self.db.commit()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("bulk_upsert_completed", entity="teams", created=created, updated=updated, duration_ms=duration_ms)
        return created, updated

    def delete(self, team_id: int) -> bool:
        team = self.get_by_id(team_id)
        if team:
            self.db.delete(team)
            self.db.commit()
            return True
        return False
