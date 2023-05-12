from datetime import datetime

from app.core.datamodels.user import BaseUserUsername
from app.core.models.database import User

BASE_USER: User = User(
    name="TEST",
    surname="TEST",
    email="test@test.com",
    hashed_psw="fake_psw",
    disabled=False,
    username="usertest",
    auth_x_token="test_token",
    verified=False,
    updated_at=datetime.now(),
    created_at=datetime.now(),
)

BASE_USER_DICT: BaseUserUsername = BaseUserUsername(**BASE_USER.__dict__)
