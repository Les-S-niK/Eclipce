## Pip modules:
from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
        VARCHAR(16),
        nullable=False,
        unique=True
    )
    hashed_password: Mapped[bytes] = mapped_column(
        VARCHAR(128),
        nullable=False
    )
    chats: Mapped[list["Chats"]] = relationship("ChatsUsers", back_populates="users")

class Chats(Base):
    __tablename__ = "chats"
    chat_name: Mapped[str] = mapped_column(
        VARCHAR(16),
        nullable=False,
    )
    users: Mapped[list["Users"]] = relationship("ChatsUsers", back_populates="chats")
    messages: Mapped[list["Messages"]] = relationship("Messages", back_populates="chat")
    
class Messages(Base):
    __tablename__ = "messages"
    chat: Mapped["Chats"] = relationship("ChatsUsers", back_populates="messages")
    message: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False)
    
class ChatsUsers(Base):
    __tablename__ = "chats_users"
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    
class AsymmetricKeys(Base):
    __tablename__ = "asymmetric_keys"
    public_key: Mapped[bytes] = mapped_column(VARCHAR(512), nullable=False)
    private_key: Mapped[bytes | None] = mapped_column(VARCHAR(512), nullable=False)