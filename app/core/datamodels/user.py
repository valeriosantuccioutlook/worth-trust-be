from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, StrictStr


class BaseUser(BaseModel):
    name: StrictStr = Field(alias="user_name")
    surname: StrictStr = Field(alias="user_surname")
    email: EmailStr = Field(alias="user_email")
    hashed_psw: StrictStr = Field(alias="user_psw")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class BaseUserUsername(BaseUser):
    username: StrictStr = Field(alias="username")


class BaseCompany(BaseModel):
    guid: Optional[UUID] = Field(alias="company_guid")
    name: StrictStr = Field(alias="company_name")
    location: StrictStr = Field(alias="company_location")
    linkedin_link: StrictStr = Field(alias="company_linkedin_link")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UserSchema(BaseUser):
    companies: Optional[List[BaseCompany]]


class CompanySchema(BaseCompany):
    pass
