from functools import lru_cache
import environ
from pydantic import BaseConfig

env = environ.Env()


class Settings(BaseConfig):
    access_token_expire_minutes: str = env.str("ACCESS_TOKEN_EXPIRE_MINUTES", default="300000")
    refresh_token_expire_minutes: str = env.str("REFRESH_TOKEN_EXPIRE_MINUTES", default="300000")
    jwt_secret_key: str = env.str("JWT_SECRET_KEY", default="")
    jwt_refresh_secret_key: str = env.str("JWT_REFRESH_SECRET_KEY", default="")
    jwt_algorithm: str = env.str("JWT_ALGORITHM", default="HS256")


@lru_cache()
def get_settings():
    _settings = Settings()
    return _settings


settings = get_settings()
