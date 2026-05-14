import time

import structlog
from sqlalchemy.orm import Session

from app.models.referee import RefereeDB
from app.schemas.referee import RefereeCreate

logger = structlog.get_logger()


class RefereeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[RefereeDB]:
        return self.db.query(RefereeDB).all()

    def get_by_id(self, referee_id: int) -> RefereeDB | None:
        return self.db.query(RefereeDB).filter(RefereeDB.id == referee_id).first()

    def create(self, referee: RefereeCreate) -> RefereeDB:
        db_referee = RefereeDB(**referee.model_dump())
        self.db.add(db_referee)
        self.db.commit()
        self.db.refresh(db_referee)
        return db_referee

    def bulk_upsert(self, referees: list[RefereeCreate]) -> tuple[int, int]:
        logger.info("bulk_upsert_started", entity="referees", records=len(referees))
        start = time.perf_counter()

        created = 0
        updated = 0

        for referee in referees:
            existing = self.get_by_id(referee.id)
            if existing:
                for key, value in referee.model_dump().items():
                    setattr(existing, key, value)
                updated += 1
            else:
                self.db.add(RefereeDB(**referee.model_dump()))
                created += 1

        self.db.commit()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "bulk_upsert_completed", entity="referees", created=created, updated=updated, duration_ms=duration_ms
        )
        return created, updated

    def delete(self, referee_id: int) -> bool:
        referee = self.get_by_id(referee_id)
        if referee:
            self.db.delete(referee)
            self.db.commit()
            return True
        return False
