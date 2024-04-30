from pydantic import BaseModel

from datetime import datetime


class BaseResourceSchema(BaseModel):
    id: int
    created_at: datetime


class UserSchema(BaseResourceSchema):
    username: str
    email: str
    birthday: datetime
    is_admin: bool
    is_verified: bool


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    birthday: datetime


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
    icon: str | None = None
    user_id: int
    district_id: int


class ItemImageSchema(BaseResourceSchema):
    item_id: int
    path: str


class ItemSchema(BaseResourceSchema):
    name: str
    introduction: str
    icon: str | None = None
    count: int
    price: int
    store_id: int

    images: list[ItemImageSchema] = []


class FullStoreSchema(StoreSchema):
    items: list[ItemSchema] = []


class OrderSchema(BaseResourceSchema):
    item_id: int
    count: int


class FullItemSchema(ItemSchema):
    store: StoreSchema


class FullCitySchema(CitySchema):
    districts: list[DistrictSchema] = []


class CartItemSchema(BaseResourceSchema):
    user_id: int
    item_id: int
    count: int


class BuyNextTimeItemSchema(BaseResourceSchema):
    user_id: int
    item_id: int


class FullCartItemSchema(CartItemSchema):
    item: ItemSchema


class FullBuyNextTimeItemSchema(BuyNextTimeItemSchema):
    item: FullItemSchema