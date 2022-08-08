from functools import lru_cache
import environ
from pydantic import BaseConfig

env = environ.Env()


class Settings(BaseConfig):
    app_title: str = env.str("APP_TITLE", default="Raspberries backend core")

    server_host: str = env.str("SERVER_HOST", default="")
    server_port: int = env.int("SERVER_PORT", default=80)

    postgres_url: str = env.str(
        "POSTGRES_URL",
        default="postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/raspberries"
    )


@lru_cache()
def get_settings():
    _settings = Settings()
    return _settings


settings = get_settings()
