## Pip modules:
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

## Declarative Base
class Base(DeclarativeBase):
    pass

## Tables
class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(255))
    hashed_pass: Mapped[str] = mapped_column(String(255))
    
class Messages(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(1000))
    deleted: Mapped[bool] = mapped_column(Boolean)
    