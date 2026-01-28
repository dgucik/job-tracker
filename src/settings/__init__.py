from functools import lru_cache
import os
from typing import Type

from settings.base import AppBaseSettings
from settings.dev import DevSettings

ENV_CONFIGS: dict[str, Type[AppBaseSettings]] = {
    "dev": DevSettings,
}


@lru_cache
def get_settings() -> AppBaseSettings:
    env_name = os.getenv("APP_ENV", "dev").lower()
    settings_class = ENV_CONFIGS.get(env_name, DevSettings)
    return settings_class()


settings = get_settings()
