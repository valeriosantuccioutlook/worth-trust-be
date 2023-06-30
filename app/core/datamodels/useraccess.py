from pydantic import BaseModel, Field, StrictStr

from ...core.datamodels.user import BaseUser


class UserAccess(BaseUser):
    hashed_password: StrictStr


class UserMe(BaseModel):
    given_name: StrictStr = Field(...)
    last_name: StrictStr = Field(...)
    email: StrictStr = Field(...)

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: StrictStr
    token_type: StrictStr


class TokenData(BaseModel):
    username: StrictStr | None = None
