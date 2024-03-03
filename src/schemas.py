from typing import Literal
from pydantic import BaseModel

from datetime import datetime

from enums import OrderStatus


class BaseSchema(BaseModel):
    id: int
    created_at: datetime


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str


'''
    CU means Create/Update.
    Use the CU* schemas for creating and updating a model.
'''


class CUCitySchema(BaseModel):
    name: str


class CUDistrictSchema(BaseModel):
    name: str
    city_id: int


class CUStoreSchema(BaseModel):
    name: str
    introduction: str
    district_id: int
    user_id: int


class AdminCUStoreSchema(CUStoreSchema):
    user_id: int


class CUItemSchema(BaseModel):
    name: str
    introduction: str
    store_id: int


class CUItemOptionTitleSchema(BaseModel):
    name: str
    item_id: int


class CUItemOptionSchema(BaseModel):
    name: str
    item_option_title_id: int
    remaining: int
    price: int


class CUOrderSchema(BaseModel):
    item_option_id: int
    count: int


class UOrderStatusSchema(BaseModel):
    status: Literal[OrderStatus.NOT_DELIVERED, OrderStatus.DELIVERED, OrderStatus.PROCESSING, OrderStatus.ARRIVED, OrderStatus.DONE]


class CUCartItemSchema(BaseModel):
    user_id: int
    item_option_id: int
    count: int


class CUCommentSchema(BaseModel):
    item_id: int
    content: str


class PCitySchema(BaseSchema):
    name: str


class PDistrictSchema(BaseSchema):
    name: str
    city_id: int


class CitySchema(PCitySchema):
    districts: list[PDistrictSchema] = []


class DistrictSchema(PDistrictSchema):
    city: PCitySchema


class PStoreSchema(BaseModel):
    name: str
    introduction: str
    user_id: int
    district_id: int


class PItemSchema(BaseModel):
    name: str
    introduction: str
    store_id: int


class PItemOptionTitleSchema(BaseModel):
    name: str
    item_id: int


class PItemOptionSchema(BaseModel):
    name: str
    item_option_title_id: int
    count: int
    status: Literal[OrderStatus.NOT_DELIVERED, OrderStatus.DELIVERED, OrderStatus.PROCESSING, OrderStatus.ARRIVED, OrderStatus.DONE]


class PCartItemSchema(BaseModel):
    user_id: int
    item_option_id: int
    count: int


class PCommentSchema(BaseModel):
    user_id: int
    item_id: int
    content: str