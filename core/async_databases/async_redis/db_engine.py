
## Built-in modules
from os import getenv
from dataclasses import dataclass

## Third-party modules: ##
from redis.asyncio import from_url, Redis


@dataclass
class Settings:
    DB_HOST: str = getenv("DB_REDIS_HOST")
    DB_PORT: int = getenv("DB_REDIS_PORT")
    DB_USER: str = getenv("DB_USER")
    DB_PASS: str = getenv("DB_PASS")
    DB_NAME: str = getenv("DB_NAME")
    REDIS_DATABASE: str = "redis://localhost"


asym_keys_redis: Redis = from_url(
    url=Settings.REDIS_DATABASE,
    # db="asym_keys"
)

sym_key_redis: Redis = from_url(
    url=Settings.REDIS_DATABASE,
    # db="sym_key"
)