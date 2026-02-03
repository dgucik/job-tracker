import logging
import sys
from pydantic import BaseModel


class LogSettings(BaseModel):
    """Configuration settings for Logging."""

    LEVEL: str = "INFO"
    FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    def setup(self) -> None:
        """Applies the logging configuration."""
        log_level = getattr(logging, self.LEVEL.upper(), logging.INFO)
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        if not root_logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(
                logging.Formatter(self.FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
            )
            root_logger.addHandler(handler)
