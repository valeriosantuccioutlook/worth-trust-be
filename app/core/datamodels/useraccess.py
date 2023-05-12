from pydantic import BaseModel, Field, StrictStr

from ...core.datamodels.user import BaseUser


class UserAccess(BaseUser):
    hashed_password: StrictStr


class UserMe(BaseModel):
    name: StrictStr = Field(alias="name")
    surname: StrictStr = Field(alias="surname")
    email: StrictStr = Field(alias="email")
    username: StrictStr = Field(alias="username")

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: StrictStr
    token_type: StrictStr


class TokenData(BaseModel):
    username: StrictStr | None = None
