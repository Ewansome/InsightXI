from pydantic import BaseModel


class SyncResult(BaseModel):
    entity: str
    created: int
    updated: int
    status: str
