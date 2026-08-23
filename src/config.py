from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    bot_token: SecretStr = SecretStr("dummy_token_for_migrations")
    db_url: str = "postgresql+asyncpg://postgres:postgres_password@localhost:5432/job_hunter"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()