from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    """Configuration settings for Database."""

    USER: str
    PASSWORD: str
    HOST: str
    PORT: int = 5432
    NAME: str
    ECHO: bool = False

    @property
    def sqlalchemy_database_url(self) -> str:
        """Constructs the SQLAlchemy URL from individual settings."""
        return (
            f"postgresql+asyncpg://"
            f"{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/"
            f"{self.NAME}"
        )
