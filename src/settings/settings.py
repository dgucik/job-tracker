from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.partials.database import DatabaseSettings
from settings.partials.logging import LogSettings


class Settings(BaseSettings):
    """Main application configuration settings."""

    APP_BASE_URL: str
    log: LogSettings = LogSettings()
    db: DatabaseSettings

    # Pydantic Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
