from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..settings import Base


class Application(Base):
    __tablename__ = "applications"

    user_guid: Mapped[UUID] = mapped_column(ForeignKey("users.guid"), primary_key=True)
    company_guid: Mapped[UUID] = mapped_column(
        ForeignKey("companies.guid"), primary_key=True
    )
    n_process_steps: Mapped[int] = mapped_column(nullable=False)
    n_steps_performed: Mapped[int] = mapped_column(nullable=False)
    joboffer_location: Mapped[str] = mapped_column(nullable=False)
    hired: Mapped[bool] = mapped_column(nullable=True, default=False)

    # association between Application -> User
    user: Mapped["User"] = relationship(back_populates="applications")
    # association between Company -> User
    company: Mapped["Company"] = relationship(back_populates="applications")


class User(Base):
    __tablename__ = "users"

    guid: Mapped[UUID] = mapped_column(
        primary_key=True, unique=True, index=True, nullable=False, default=uuid4
    )
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_psw: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[bool] = mapped_column(nullable=False, default=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    auth_x_token: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    verified: Mapped[bool] = mapped_column(nullable=False, default=False)

    # many-to-many relationship to Company, bypassing the `Application` class
    companies: Mapped[List["Company"]] = relationship(
        secondary="applications", back_populates="users"
    )
    # association between User -> Application -> Company
    applications: Mapped[List["Application"]] = relationship(back_populates="user")


class Company(Base):
    __tablename__ = "companies"

    guid: Mapped[UUID] = mapped_column(
        primary_key=True, unique=True, index=True, nullable=False, default=uuid4
    )
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    linkedin_link: Mapped[str] = mapped_column(nullable=False, unique=True)

    # many-to-many relationship to User, bypassing the `Application` class
    users: Mapped[List["User"]] = relationship(
        secondary="applications", back_populates="companies"
    )
    # association between Company -> Application -> User
    applications: Mapped[List["Application"]] = relationship(back_populates="company")
