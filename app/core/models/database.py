from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import BinaryExpression, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.session import Session

from ..enums.enums import AdType, RequestStatus
from ..settings import Base


class Request(Base):
    __tablename__ = "requests"

    user_guid: Mapped[UUID] = mapped_column(ForeignKey("users.guid"), primary_key=True)
    ad_guid: Mapped[UUID] = mapped_column(ForeignKey("ads.guid"), primary_key=True)
    status: Mapped[RequestStatus] = mapped_column(nullable=False)

    # association between Request -> User
    user: Mapped["User"] = relationship(back_populates="requests")
    # association between Ad -> User
    ad: Mapped["Ad"] = relationship(back_populates="requests")


class User(Base):
    __tablename__ = "users"

    guid: Mapped[UUID] = mapped_column(
        primary_key=True, unique=True, index=True, nullable=False, default=uuid4
    )
    given_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_psw: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[bool] = mapped_column(nullable=False, default=False)
    auth_x_token: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    city: Mapped[str] = mapped_column(nullable=False, default=False)
    country: Mapped[str] = mapped_column(nullable=False, default=False)
    address: Mapped[str] = mapped_column(nullable=True, default=False)
    zip_code: Mapped[str] = mapped_column(nullable=False, default=False)
    birthday: Mapped[str] = mapped_column(nullable=True, default=False)
    phone_numb_prefix: Mapped[str] = mapped_column(nullable=True)
    phone_numb: Mapped[str] = mapped_column(nullable=True)

    # many-to-many relationship to Ad, bypassing the `Request` class
    ads: Mapped[List["Ad"]] = relationship(secondary="requests", back_populates="users")
    # association between User -> Request -> Ad
    requests: Mapped[List["Request"]] = relationship(back_populates="user")


class Ad(Base):
    __tablename__ = "ads"

    guid: Mapped[UUID] = mapped_column(
        primary_key=True, unique=True, index=True, nullable=False, default=uuid4
    )
    added_by: Mapped[UUID] = mapped_column(ForeignKey("users.guid"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    zip_code: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    value_estimation: Mapped[float] = mapped_column(nullable=False)
    ad_type: Mapped[AdType] = mapped_column(nullable=False)

    # many-to-many relationship to User, bypassing the `Request` class
    users: Mapped[List["User"]] = relationship(
        secondary="requests", back_populates="ads"
    )
    # association between Ad -> Request -> User
    requests: Mapped[List["Request"]] = relationship(back_populates="ad")

    @classmethod
    def get_ads(
        cls, session: Session, _filters: List[BinaryExpression] = list()
    ) -> List["Ad"]:
        """
        Query `Ad` class by filtering according to the list of
        binary expressions iven.

        Returns:
            List[Ad]: List of ads.
        """
        q = session.query(cls)
        if not len(_filters):
            return q.all()
        return q.filter(*_filters).all()
