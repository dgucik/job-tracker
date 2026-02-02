from pydantic import BaseModel


class LogSettings(BaseModel):
    """Configuration settings for Logging."""

    LEVEL: str = "INFO"
