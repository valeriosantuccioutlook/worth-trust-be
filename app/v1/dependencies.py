from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jinja2 import Environment, PackageLoader, select_autoescape
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from ..config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    EMAIL_FROM,
    EMAIL_HOST,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_USERNAME,
    SECRET_KEY,
)
from ..core.datamodels.useraccess import Token, TokenData
from ..core.models.database import User
from ..core.settings import get_db

env = Environment(
    loader=PackageLoader("app", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Email:
    def __init__(
        self,
        user: User,
        url: str,
    ):
        self.user = user
        self.sender = "WorthTrust <admin@admin.com>"
        self.email = [EmailStr(self.user.email)]
        self.url = url

    async def send_email(
        self,
        subject: str,
        template: str,
    ):
        # Define the config
        conf = ConnectionConfig(
            MAIL_USERNAME=EMAIL_USERNAME,
            MAIL_PASSWORD=EMAIL_PASSWORD,
            MAIL_FROM=EMAIL_FROM,
            MAIL_PORT=int(EMAIL_PORT),
            MAIL_SERVER=EMAIL_HOST,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
        # Generate the HTML template base on the template name
        template = env.get_template(f"{template}.html")
        html = template.render(url=self.url, first_name=self.user.name, subject=subject)

        # Define the message options
        message = MessageSchema(
            subject=subject, recipients=self.email, body=html, subtype="html"
        )

        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)

    async def send_verification_code(self):
        await self.send_email("WorthTrust email verification", "verification")


def authenticate_user(
    session: Session,
    username: str,
    password: str,
) -> User:
    user: User = get_user(session, username)
    if user is None:
        return False
    if not pwd_context.verify(password, user.hashed_psw):
        return False
    return user


def get_user(
    session: Session,
    username: str,
) -> User | None:
    user = session.query(User).filter(User.username == username).one_or_none()
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_db),
) -> User:
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


def verify_registered_user(
    access_token: str,
    session: Session = Depends(get_db),
) -> str:
    if session.query(User).filter(User.auth_x_token == access_token).count() == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find existing user or user already verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_token


def login_for_access_token(
    session: Session,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
