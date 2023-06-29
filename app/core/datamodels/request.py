from uuid import UUID

from pydantic import BaseModel, Field

from ..enums.enums import RequestStatus
from .ad import AdBody
from .user import UserLinked


class BaseRequest(BaseModel):
    ad_guid: UUID = Field(...)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class RequestBody(BaseRequest):
    status: RequestStatus = Field(RequestStatus.PENDING)
    user_guid: UUID = Field(...)


class RequestCreationResponse(BaseRequest):
    status: RequestStatus = Field(...)


class UserRequest(BaseModel):
    status: RequestStatus
    ad: AdBody
    added_by: UserLinked
