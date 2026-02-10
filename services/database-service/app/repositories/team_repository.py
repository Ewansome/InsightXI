from sqlalchemy.orm import Session

from app.models.team import TeamDB
from app.schemas.team import TeamCreate


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
        return created, updated

    def delete(self, team_id: int) -> bool:
        team = self.get_by_id(team_id)
        if team:
            self.db.delete(team)
            self.db.commit()
            return True
        return False
