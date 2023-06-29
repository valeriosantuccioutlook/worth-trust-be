from datetime import datetime
from typing import List

from sqlalchemy import Column
from sqlalchemy.orm import Session
from starlette import status

from ..core.datamodels.ad import AdBody, AdResponseBody, BaseAd
from ..core.datamodels.request import (
    BaseRequest,
    RequestBody,
    RequestCreationResponse,
    UserRequest,
)
from ..core.datamodels.user import BaseUser, UserBody
from ..core.enums.enums import AdType, RequestStatus
from ..core.models.database import Ad, Request, User
from .dependencies import create_access_token, pwd_context


def create_new_user(user: BaseUser, session: Session) -> UserBody:
    """
    Insert new user into `users` table.

    Args:
        user (BaseUser): User model body.
        session (Session): SQLAlchemy transaction session.

    Returns:
        User: new user created.
    """
    user: UserBody = UserBody(
        **dict(user),
        updated_at=datetime.now(),
        created_at=datetime.now(),
        auth_x_token=None,
        verified=False,
    )
    user.given_name = user.given_name.lower()
    user.last_name = user.last_name.lower()
    user.hashed_psw = pwd_context.hash(user.hashed_psw)
    access_token = create_access_token({"sub": user.email})
    user.auth_x_token = access_token
    session.add(User(**dict(user)))
    session.flush()
    return user


def disable_user(user: User) -> status.HTTP_202_ACCEPTED:
    """
    Disable user.

    Args:
        :user (User): Current active user to make unactive.

    Returns:
        status.HTTP_202_ACCEPTED: Accepted.
    """
    user.disabled = True
    return status.HTTP_202_ACCEPTED


def create_new_ad(user: User, session: Session, ad: BaseAd) -> BaseAd:
    """
    Add new ad.

    Args:
        :user (User): Current active user.
        :session (Session): SQLAlchemy transaction session.
        :ad (Ad): Ad model body.

    Returns:
        BaseAd: new ad created.
    """
    new_ad: AdBody = AdBody(**dict(ad), added_by=user.guid)
    session.add(Ad(**dict(new_ad)))
    return BaseAd(**dict(new_ad))


def get_user_ads(
    user: User, session: Session, ad_type: AdType | None, title: str | None
) -> List[AdResponseBody]:
    """
    Get user ads.

    Args:
        :user (User): Current active user.
        :session (Session): SQLAlchemy transaction session.
        :ad_type (AdType | None): Enum type to filter the query on `ad_type` domain.
        :title (str | None): Possible word contained into the title to filter.

    Returns:
        List[BaseAd]: List of ads.
    """
    _filters: list = [Column("added_by") == user.guid]
    if ad_type is not None:
        _filters.append(Column("ad_type") == ad_type.name)
    if title is not None:
        _filters.append(Column("title").contains(title))
    return [
        AdResponseBody(**ad)
        for ad in [r.__dict__ for r in Ad.get_ads(session, _filters)]
    ]


def get_all_ads(session: Session) -> List[AdResponseBody]:
    """
    #TODO -> filter by location
    """
    return [AdResponseBody(**ad) for ad in [r.__dict__ for r in Ad.get_ads(session)]]


def create_new_request(
    user: User, session: Session, request: BaseRequest
) -> BaseRequest:
    """
    Create new user's `request`.

    Args:
        :user (User): Current active user.
        :session (Session): SQLAlchemy transaction session.
        :request (BaseRequest): Request modelbody.

    Returns:
        BaseRequest: User's request created.
    """
    new_request: RequestBody = RequestBody(
        **dict(request),
        user_guid=user.guid,
    )
    session.add(Request(**dict(new_request)))
    return RequestCreationResponse(**dict(new_request))


def get_user_requests(user: User, status: RequestStatus) -> List[UserRequest]:
    """
    Get user's requetss.

    Args:
        :user (User): Current active user.
        :session (Session): SQLAlchemy transaction session.

    Returns:
        List[UserRequest]: User's requests.
    """
    requests = list()
    for req in user.requests:
        if status is not None:
            if req.status == status:
                requests.append(UserRequest(ad=req.ad, status=req.status))
            return requests
        requests.append(UserRequest(ad=req.ad, status=req.status))
    return requests
