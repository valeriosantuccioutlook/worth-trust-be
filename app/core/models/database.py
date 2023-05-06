from typing import List
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..settings import Base


class UserCompany(Base):
    __tablename__ = "users_companies"

    user_guid: Mapped[UUID] = mapped_column(ForeignKey("users.guid"), primary_key=True)
    company_guid: Mapped[UUID] = mapped_column(
        ForeignKey("companies.guid"), primary_key=True
    )
    n_process_steps: Mapped[int] = mapped_column(nullable=False)
    n_steps_performed: Mapped[int] = mapped_column(nullable=False)
    joboffer_location: Mapped[str] = mapped_column(nullable=False)
    hired: Mapped[bool] = mapped_column(nullable=True, default=False)

    # association between UserCompany -> User
    user: Mapped["User"] = relationship(back_populates="users_companies")
    # association between Company -> User
    company: Mapped["Company"] = relationship(back_populates="users_companies")


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

    # many-to-many relationship to Company, bypassing the `UserCompany` class
    companies: Mapped[List["Company"]] = relationship(
        secondary="users_companies", back_populates="users"
    )
    # association between User -> UserCompany -> Company
    users_companies: Mapped[List["UserCompany"]] = relationship(back_populates="user")


class Company(Base):
    __tablename__ = "companies"

    guid: Mapped[UUID] = mapped_column(
        primary_key=True, unique=True, index=True, nullable=False, default=uuid4
    )
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    linkedin_link: Mapped[str] = mapped_column(nullable=False, unique=True)

    # many-to-many relationship to User, bypassing the `UserCompany` class
    users: Mapped[List["User"]] = relationship(
        secondary="users_companies", back_populates="companies"
    )
    # association between Company -> UserCompany -> User
    users_companies: Mapped[List["UserCompany"]] = relationship(
        back_populates="company"
    )
