from typing import Annotated, Dict

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...core.datamodels.user import BaseUser
from ...core.datamodels.useraccess import Token, UserMe
from ...core.models.database import User
from ...core.settings import get_db
from .. import corefuncs
from ..dependencies import get_current_active_user
from ..utils import manage_transaction

router = APIRouter()


@router.get("/user", response_model=UserMe)
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


@router.post("/token", response_model=Token)
@manage_transaction
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db),
) -> Token:
    """
    Create login access token for the current active user.

    Args:
        :form_data (Annotated[OAuth2PasswordRequestForm, Depends): OAuth2 standard
        form data payload.
        :session (Session, optional): SQLAlchemy transaction session.

    Returns:
        Token: access token.
    """
    return corefuncs.login_for_access_token(session, form_data)


@router.post(
    "/user",
    description="Add new `user`.",
    status_code=201,
)
@manage_transaction
def create_new_user(
    user: Annotated[BaseUser, Body(..., embed=False)],
    session: Session = Depends(get_db),
) -> Dict:
    """
    Add new user in `user` table.

    Args:
        :user (BaseUser). User content needed to perform insert.
        :session (Session). SQLAlchemy transaction session. Defaults to Depends(get_db).

    Returns:
        User: User created.
    """
    return corefuncs.create_new_user(user, session)
