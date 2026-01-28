from pydantic import BaseModel


class LogSettings(BaseModel):
    """Configuration settings for Logging."""

    LOG_LEVEL: str = "INFO"
