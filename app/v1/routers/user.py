from datetime import datetime
from typing import Annotated, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from ...core.datamodels.user import BaseUser
from ...core.datamodels.useraccess import Token, UserMe
from ...core.models.database import User
from ...core.settings import get_db
from .. import corefuncs
from ..dependencies import (
    Email,
    create_access_token,
    get_current_active_user,
    login_for_access_token,
    verify_registered_user,
)
from ..utils import manage_transaction

router = APIRouter()


@router.get(
    "/user",
    response_model=UserMe,
    description="Get logged `user` info.",
)
def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserMe:
    """
    Returns current active user info.

    Args:
        :current_user (Annotated[User, Depends): Active user.

    Returns:
        UserMe: response model.
    """
    return current_user


@router.post("/token", response_model=Token, status_code=status.HTTP_202_ACCEPTED)
@manage_transaction
def login__access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db),
) -> Token:
    """
    Create login access token for the current active `user`.

    Args:
        :form_data (Annotated[OAuth2PasswordRequestForm, Depends): OAuth2 standard
        form data payload.
        :session (Session, optional): SQLAlchemy transaction session.

    Returns:
        Token: access token.
    """
    return login_for_access_token(session, form_data)


@router.delete(
    "/user/disable",
    description="Disable `user`.",
    status_code=status.HTTP_202_ACCEPTED,
)
@manage_transaction
def disable_user(
    session: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
) -> int:
    """
    Disable existing `user`.

    Args:
        :session (Session, optional): SQLAlchemy transaction session.
        :user (Annotated[User, Depends): _description_

    Returns:
        int: _description_
    """
    return corefuncs.disable_user(user)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    description="Create new `user`.",
)
async def create_user(
    user_form: BaseUser,
    session: Annotated[Session, Depends(get_db)],
    request: Request,
) -> UserMe:
    """
    Register a new `user`.

    Args:
        :user_form (BaseUser): User content form.
        :session (Session, optional): SQLAlchemy transaction session.
        :request (Request): FastAPI Request class.

    Returns:
        UserMe: Basic user info.
    """
    user = corefuncs.create_new_user(user_form, session)
    access_token = create_access_token({"sub": user.username})
    user.auth_x_token = access_token
    url = f"{request.url.scheme}://{request.client.host}:{request.url.port}/verifyemail/{user.auth_x_token}"
    sender = Email(user, url)
    await sender.send_verification_code()
    return UserMe(**user.dict())


@router.get(
    "/verifyemail/{access_token}",
    status_code=status.HTTP_200_OK,
    description="Send a verification email to a registering `user`.",
)
@manage_transaction
def verify_user_by_email_sender(
    access_token: Annotated[str, Depends(verify_registered_user)],
    session: Annotated[Session, Depends(get_db)],
) -> Dict:
    """
    Verify user registration by email.

    Args:
        :access_token (Annotated[str, Depends): Access token.
        :session (Session, optional): SQLAlchemy transaction session.

    Raises:
        HTTPException: Account already verified.

    Returns:
        Dict: Success response of verification.
    """
    user = session.query(User).filter(User.auth_x_token == access_token).one_or_none()
    if user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account already verified",
        )
    user.verified = True
    user.updated_at = datetime.now()
    return {"status": status.HTTP_200_OK, "message": "Account successfully verified"}


@router.post(
    "/verifyemail/resend",
    status_code=status.HTTP_202_ACCEPTED,
    description="Resend a verification email to an existing `user`.",
)
async def resend_email_verification(
    user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    session: Session = Depends(get_db),
) -> int:
    """
    Resend verification email.

    Args:
        :user (Annotated[User, Depends): _description_
        :request (Request): FastAPI Request class.
        :session (Session, optional): SQLAlchemy transaction session.

    Returns:
        int: Accepted request.
    """
    acces_token = create_access_token({"sub": user.username})
    user.auth_x_token = acces_token
    session.flush()
    session.commit()
    url = f"{request.url.scheme}://{request.client.host}:{request.url.port}/verifyemail/{user.auth_x_token}"
    sender = Email(user, url)
    await sender.send_verification_code()
    return status.HTTP_202_ACCEPTED
