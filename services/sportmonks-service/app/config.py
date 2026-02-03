from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    api_key: str = Field(default="")
    base_url: str = "https://api.sportmonks.com/v3"
    model_config = {
        "env_file": ENV_FILE if ENV_FILE.exists() else None,
        "extra": "ignore",
    }


settings = Settings()
