from settings.base import AppBaseSettings
from settings.partials.database import DatabaseSettings
from settings.partials.logging import LogSettings


class DevDatabaseSettings(DatabaseSettings):
    ECHO: bool = True


class DevLogSettings(LogSettings):
    LOG_LEVEL: str = "DEBUG"


class DevSettings(AppBaseSettings):
    """Development environment configuration settings."""

    db: DevDatabaseSettings
    log: DevLogSettings = DevLogSettings()
