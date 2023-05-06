import random
import string
from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..core.datamodels.user import BaseUser, BaseUserUsername
from ..core.datamodels.useraccess import Token
from ..core.models.database import User
from .dependencies import authenticate_user, create_access_token, pwd_context


def create_new_user(user: BaseUser, session: Session) -> User:
    """
    Insert new user into `users` table.

    Args:
        user (BaseUser): User model body.
        session (Session): SQLAlchemy transaction session.

    Returns:
        User: new user created.
    """

    def _username_generator(
        size: int = 10, chars: str = string.ascii_uppercase + string.digits
    ) -> str:
        return "".join(random.choice(chars) for _ in range(size))

    user: BaseUserUsername = BaseUserUsername(
        **dict(user), username=_username_generator()
    )
    user.hashed_psw = pwd_context.hash(user.hashed_psw)
    session.add(User(**dict(user)))
    response = user.dict(exclude={"hashed_psw"})
    return response


def login_for_access_token(
    session: Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Create new login access token for the current active user.

    Args:
        :session (Session, optional): SQLAlchemy transaction session.
        :form_data (Annotated[OAuth2PasswordRequestForm, Depends): OAuth2 standard
        form data payload.

    Raises:
        HTTPException: Handled exception: not authenticated.

    Returns:
        Token: access token.
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
