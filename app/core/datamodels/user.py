from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, StrictBool, StrictStr


class BaseUser(BaseModel):
    given_name: StrictStr = Field(...)
    second_name: StrictStr = Field(None)
    last_name: StrictStr = Field(...)
    email: EmailStr = Field(...)
    hashed_psw: StrictStr = Field(alias="password")
    city: StrictStr = Field(...)
    country: StrictStr = Field(...)
    address: StrictStr = Field(None)
    zip_code: StrictStr = Field(...)
    birthday: StrictStr = Field(None)
    phone_numb_prefix: StrictStr = Field(None)
    phone_numb: StrictStr = Field(None)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UserBody(BaseUser):
    updated_at: datetime = Field(...)
    created_at: datetime = Field(...)
    auth_x_token: StrictStr | None = Field(alias="auth_x_token")
    verified: StrictBool = Field(...)


class UserLinked(BaseModel):
    pass
