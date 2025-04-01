## Pip modules:
from sqlalchemy import VARCHAR, BINARY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

## Declarative Base
class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False, 
        autoincrement=True,
        unique=True
    )
    

## Tables
class Users(Base):
    __tablename__ = "users"
    login: Mapped[str] = mapped_column(
        VARCHAR(24),
        nullable=False,
        unique=True
    )
    hashed_pass: Mapped[bytes] = mapped_column(
        VARCHAR(128),
        nullable=False
    )