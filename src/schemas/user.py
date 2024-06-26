from pydantic import BaseModel
from enums import OrderStatus

class CUStoreSchema(BaseModel):
    name: str
    introduction: str
    district_id: int


class CUItemSchema(BaseModel):
    name: str
    introduction: str
    count: int
    price: int
    need_18: bool


class CUItemOptionTitleSchema(BaseModel):
    name: str


class CUItemOptionSchema(BaseModel):
    name: str
    additional_price: int
    remaining: int


class CUOrderSchema(BaseModel):
    address: str
    note: str | None = None
    item_id: int
    count: int


class CUCartItemSchema(BaseModel):
    item_id: int
    count: int


class CUItemReportSchema(BaseModel):
    reported_item_id: int
    reason: str


class CUUserReportSchema(BaseModel):
    reported_user_id: int
    reason: str


class CUBuyNextTimeItemSchema(BaseModel):
    item_id: int


class CUUserIconSchema(BaseModel):
    icon: str | None


class UserStoreOrderQuery(BaseModel):
    status: OrderStatus | None = None