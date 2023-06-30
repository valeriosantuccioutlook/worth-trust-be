from uuid import UUID

from pydantic import BaseModel, Field, StrictFloat, StrictStr

from ..enums.enums import AdType


class BaseAd(BaseModel):
    title: StrictStr = Field(...)
    city: StrictStr = Field(...)
    zip_code: StrictStr = Field(...)
    description: StrictStr = Field(None)
    value_estimation: StrictFloat = Field(...)
    ad_type: AdType = Field(...)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class AdBody(BaseAd):
    added_by: UUID = Field(...)


class AdResponseBody(BaseAd):
    guid: UUID = Field(...)
