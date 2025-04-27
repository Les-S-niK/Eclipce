
## Built-in modules: ##
from os import getenv

## Third-party modules: ##
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Settings:
    DB_HOST: str = getenv("DB_SQL_HOST")
    DB_PORT: int = getenv("DB_SQL_PORT")
    DB_USER: str = getenv("DB_USER")
    DB_PASS: str = getenv("DB_PASS")
    DB_NAME: str = getenv("DB_NAME")
    DATABASE_URL_PYMYSQL: str = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_async_engine(
    url=Settings.DATABASE_URL_PYMYSQL,
    echo=False,
    pool_size=5,
    max_overflow=10
)

session_factory = async_sessionmaker(engine)