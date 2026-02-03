from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    db_user: str = Field(default="")
    db_password: str = Field(default="")
    db_name: str = Field(default="")
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=3306)

    model_config = {
        "env_file": ENV_FILE if ENV_FILE.exists() else None,
        "extra": "ignore",
    }

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
