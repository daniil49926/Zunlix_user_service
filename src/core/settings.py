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

    BASE_DIR: str = _BASE_DIR

    TESTING: bool = os.environ.get("TESTING")


settings = __Settings()
