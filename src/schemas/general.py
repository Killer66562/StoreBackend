from pydantic import BaseModel

from datetime import datetime


class BaseResourceSchema(BaseModel):
    id: int
    created_at: datetime


class UserSchema(BaseResourceSchema):
    username: str
    email: str
    is_admin: bool
    is_verified: bool


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class CitySchema(BaseResourceSchema):
    name: str


class DistrictSchema(BaseResourceSchema):
    name: str
    city_id: int


class StoreSchema(BaseResourceSchema):
    name: str
    introduction: str
    user_id: int
    district_id: int