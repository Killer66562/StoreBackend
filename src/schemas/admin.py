from pydantic import BaseModel
from .general import BaseResourceSchema, UserSchema


class CUCitySchema(BaseModel):
    name: str


class CUDistrictSchema(BaseModel):
    name: str
    city_id: int


class UserRepoertImageSchema(BaseResourceSchema):
    report_id: int
    path: str


class UserRepoertSchema(BaseResourceSchema):
    reporter_id: int
    reported_user_id: int
    reporter: UserSchema
    reported_user: UserSchema
    images: list[UserRepoertImageSchema]