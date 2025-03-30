## Third-party modules: ##
from dataclasses import dataclass

APP_VERION: str = "0.1.0"


@dataclass
class CORSMiddleWareSettings:
    """Setting for FastApi CORS middleware."""
    ALLOWED_ORIGINS: list[str] = [
        "http://127.0.0.1:3010",
    ]
    ALLOWED_CREDENTIALS: bool = True
    ALLOWED_METHODS: list[str] = [
        "*"
    ]
    ALLOWED_HEADERS: list[str] = [
        "*"
    ]