from datetime import datetime
from uuid import uuid4

from app.core.datamodels.ad import AdBody
from app.core.datamodels.user import UserBody
from app.core.enums.enums import AdType, Currency
from app.core.models.database import Ad, User

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

BASE_AD: Ad = Ad(
    title="Gigabyte Aorus 15P",
    city="Wien",
    zip_code="22. Wien",
    description="Used but in perfect conditions, as new.",
    value_estimation=900.00,
    ad_type=AdType.ITEM,
    currency=Currency.EUR,
    added_by=uuid4(),
)
BASE_AD_DICT: AdBody = AdBody(**BASE_AD.__dict__)
