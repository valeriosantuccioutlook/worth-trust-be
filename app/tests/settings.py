from datetime import datetime

from app.core.datamodels.user import UserBody
from app.core.models.database import User

BASE_USER: User = User(
    given_name="TEST",
    last_name="TEST",
    email="test@test.com",
    hashed_psw="fake_psw",
    disabled=False,
    auth_x_token="test_token",
    verified=False,
    updated_at=datetime.now(),
    created_at=datetime.now(),
    city="Nottingham",
    country="United Kingdom",
    zip_code="NG1",
)

BASE_USER_DICT: UserBody = UserBody(**BASE_USER.__dict__)
