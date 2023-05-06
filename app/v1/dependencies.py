from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from ..config import ALGORITHM, SECRET_KEY
from ..core.datamodels.useraccess import TokenData
from ..core.models.database import User
from ..core.settings import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(session: Session, username: str, password: str) -> User:
    user: User = get_user(session, username)
    if user is None:
        return False
    if not pwd_context.verify(password, user.hashed_psw):
        return False
    return user


def get_user(session: Session, username: str) -> User | None:
    user = session.query(User).filter(User.username == username).one_or_none()
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)
) -> User:
    """_summary_

    Args:
        token (Annotated[str, Depends): _description_
        session (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        credentials_exception: _description_
        credentials_exception: _description_
        credentials_exception: _description_

    Returns:
        User: _description_
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user: User = get_user(session, username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
