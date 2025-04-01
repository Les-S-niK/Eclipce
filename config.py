
## Built-in modules: ##
from os import getenv

## Third-party modules: ##
from dataclasses import dataclass
from datetime import timedelta

APP_VERSION: str = "0.1.0"
SECRET_KEY: str = getenv("SECRET_KEY")

## Token configuration: ##
TOKEN_HASH_ALGORITHM: str = getenv("HASH_ALGORITHM")
TOKEN_EXPIRE_DAYS: int = 7
TOKEN_EXPIRE_TIME: timedelta = timedelta(days=TOKEN_EXPIRE_DAYS)
TOKEN_TYPE: str = "Bearer"

@dataclass
class CORSMiddleWareSettings:
    """Setting for FastApi CORS middleware."""
    ALLOWED_ORIGINS: tuple[str] = (
        "http://127.0.0.1:3010",
    )
    ALLOWED_CREDENTIALS: bool = True
    ALLOWED_METHODS: tuple[str] = (
        "*"
    )
    ALLOWED_HEADERS: tuple[str] = (
        "*"
    )