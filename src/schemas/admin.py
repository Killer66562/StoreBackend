from datetime import datetime
from typing import Literal
from pydantic import BaseModel

from enums import UserQuerySortByEnum
from .general import BaseResourceSchema, UserSchema, ItemSchema


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


class ItemRepoertImageSchema(BaseResourceSchema):
    report_id: int
    path: str


class ItemReportSchema(BaseResourceSchema):
    reporter_id: int
    reported_item_id: int
    reason: str
    reporter: UserSchema
    reported_item: ItemSchema
    images: list[ItemRepoertImageSchema]


class CUUserSchema(BaseModel):
    is_admin: bool
    is_banned: bool | None = None


class UserQuerySchema(BaseModel):
    username: str | None = None
    email: str | None = None
    birthday_start: datetime | None = None
    birthday_end: datetime | None = None
    created_at_start: datetime | None = None
    created_at_end: datetime | None = None
    is_admin: bool | None = None
    sort_by: UserQuerySortByEnum | None = None
    desc: bool | None = None


class CUAdSchema(BaseModel):
    url: str