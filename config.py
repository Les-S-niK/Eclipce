
## Built-in modules: ##
from os import getenv, PathLike
from os.path import dirname

## Third-party modules: ##
from dataclasses import dataclass
from datetime import timedelta


APP_VERSION: str = "0.2.0"
SECRET_KEY: str = getenv("SECRET_KEY")

## Token configuration: ##
TOKEN_HASH_ALGORITHM: str = getenv("HASH_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
REFRESH_TOKEN_EXPIRE_DAYS: int = 2
ACCESS_TOKEN_EXPIRE_TIME: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE_TIME: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

BEARER: str = "Bearer"
REFRESH_TOKEN: str = "refresh"
ACCESS_TOKEN: str = "access"

## Application endpoints. ##
SERVER_HOST: str = "0.0.0.0"
SERVER_PORT: int = 8080
TOKEN_AUTH_ENDP: str = f"http://{SERVER_HOST}:{SERVER_PORT}/api_v1/token_auth"
SIGN_IN_ENDP: str = f"http://{SERVER_HOST}:{SERVER_PORT}/api_v1/sign_in"
SIGN_UP_ENDP: str = f"http://{SERVER_HOST}:{SERVER_PORT}/api_v1/sign_up"

PROJECT_PATH: PathLike = dirname(__file__)


@dataclass
class CORSMiddleWareSettings:
    """Setting for FastApi CORS middleware."""
    ALLOWED_ORIGINS: tuple[str] = (
        "http://127.0.0.1:3010",
        "http://127.0.0.1:8080",
        "http://0.0.0.0:3010",
        "http://0.0.0.0:8080",
    )
    ALLOWED_CREDENTIALS: bool = True
    ALLOWED_METHODS: tuple[str] = (
        "*"
    )
    ALLOWED_HEADERS: tuple[str] = (
        "*"
    )