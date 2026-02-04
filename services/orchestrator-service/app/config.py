from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    sportmonks_service_url: str = Field(default="http://127.0.0.1:8000")
    database_service_url: str = Field(default="http://127.0.0.1:8001")

    model_config = {
        "env_file": ENV_FILE if ENV_FILE.exists() else None,
        "extra": "ignore",
    }


settings = Settings()
