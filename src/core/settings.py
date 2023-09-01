import os

from pydantic_settings import BaseSettings

from src.core.utils.base_classes import Singleton
from src.core.utils.load_env import load_environ

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_environ(_BASE_DIR)


class __Settings(Singleton, BaseSettings):
    HOST: str = os.environ.get("APPLICATION_HOST")
    PORT: int = os.environ.get("APPLICATION_PORT")

    RELOAD: bool = True
    PG_DSN: str = os.environ.get("PG_DSN")
    MAX_ATTEMPTS_TO_CONN_TO_PG: int = 5

    BASE_DIR: str = _BASE_DIR

    CRYPTO_KEY: bytes = os.environ.get("CRYPTO_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720

    TESTING: bool = os.environ.get("TESTING")


settings = __Settings()
