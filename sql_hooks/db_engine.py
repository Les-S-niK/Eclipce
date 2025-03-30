## Pip modules:
from dotenv import load_dotenv
from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

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
    echo=True,
    pool_size=5,
    max_overflow=10
)

session_factory = async_sessionmaker(engine)
## Declarative Base
class Base(DeclarativeBase):
    pass

## Generate URL
class Settings(): 
    def __init__(self):
        self.DB_HOST: str = getenv("DB_HOST")
        self.DB_PORT: int = getenv("DB_PORT")
        self.DB_USER: str = getenv("DB_USER")
        self.DB_PASS: str = getenv("DB_PASS")
        self.DB_NAME: str = getenv("DB_NAME")
    
    @property
    def DATABASE_URL_PYMYSQL(self): return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
## Create engine
engine = create_async_engine(
    url=Settings().DATABASE_URL_PYMYSQL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

## Create async session
session_factory = async_sessionmaker(engine)
