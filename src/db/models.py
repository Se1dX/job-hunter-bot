import enum
from datetime import datetime
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, Enum, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ApplicationStatus(enum.Enum):
    """
    Represents the current state of a job application.
    """
    NEW = "NEW"
    COVER_GENERATED = "COVER_GENERATED"
    APPLIED = "APPLIED"
    REJECTED = "REJECTED"
    SKIPPED = "SKIPPED"


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy declarative models.
    """
    pass


class User(Base):
    """
    Represents a Telegram user interacting with the bot.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    resume_text: Mapped[Optional[str]] = mapped_column(Text)
    resume_embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(768))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Vacancy(Base):
    """
    Represents a job vacancy fetched from HH.ru.
    """
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hh_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    salary: Mapped[Optional[str]] = mapped_column(String)
    employer: Mapped[str] = mapped_column(String)
    description_embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(768))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Application(Base):
    """
    Represents a user's interaction or application to a specific vacancy.
    """
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(index=True)
    vacancy_id: Mapped[int] = mapped_column(index=True)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus), default=ApplicationStatus.NEW, index=True
    )
    cover_letter: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )