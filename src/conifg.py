from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FINAM_API_KEY: str | None = None
    FINAM_ACCOUNT_ID: str | None = None
    INCLUDE_SERVERS: list[str] | None = None

    @field_validator("INCLUDE_SERVERS", mode="before")
    @classmethod
    def set_include_server_tags(cls, v: str | list[str]) -> list[str] | None:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list | str):
            return v
        return None

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()