import random
import string
from datetime import datetime

from sqlalchemy.orm import Session
from starlette import status

from ..core.datamodels.user import BaseUser, BaseUserUsername
from ..core.models.database import User
from .dependencies import create_access_token, pwd_context


def create_new_user(user: BaseUser, session: Session) -> BaseUserUsername:
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
        **dict(user),
        username=_username_generator(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
        auth_x_token=None,
        verified=False
    )
    user.name = user.name.upper()
    user.surname = user.surname.upper()
    user.hashed_psw = pwd_context.hash(user.hashed_psw)
    access_token = create_access_token({"sub": user.username})
    user.auth_x_token = access_token
    session.add(User(**dict(user)))
    session.flush()
    session.commit()
    return user


def disable_user(user: User) -> status.HTTP_202_ACCEPTED:
    """
    Disable user.

    Args:
        :user (User): Current active user to make inactive.

    Returns:
        status.HTTP_202_ACCEPTED: Accepted.
    """
    user.disabled = True
    return status.HTTP_202_ACCEPTED
    return status.HTTP_202_ACCEPTED
