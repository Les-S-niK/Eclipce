## Pip modules:
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

## Built-in modules
from os import getenv

## Load .env
load_dotenv()
class Settings:
    def __init__(self):
        self.DB_HOST: str = getenv("DB_HOST")
        self.DB_PORT: int = getenv("DB_PORT")
        self.DB_USER: str = getenv("DB_USER")
        self.DB_PASS: str = getenv("DB_PASS")
        self.DB_NAME: str = getenv("DB_NAME")
        self.DATABASE_URL_PYMYSQL: str = f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

engine = create_async_engine(
    url=Settings().DATABASE_URL_PYMYSQL,
    echo=False,
    pool_size=5,
    max_overflow=10
)

session_factory = async_sessionmaker(engine)