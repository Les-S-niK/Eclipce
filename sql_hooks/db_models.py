## Pip modules:
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

## Project modules:
from sql_hooks.db_engine import Base

## Tables
class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    login: Mapped[str] = mapped_column(String(255))
    hash: Mapped[str] = mapped_column(String(255))