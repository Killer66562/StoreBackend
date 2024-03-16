from pydantic import BaseModel


class CUStoreSchema(BaseModel):
    name: str
    introduction: str
    district_id: int


class CUItemSchema(BaseModel):
    name: str
    introduction: str
    price: int


class CUItemOptionTitleSchema(BaseModel):
    name: str


class CUItemOptionSchema(BaseModel):
    name: str
    additional_price: int
    remaining: int


class _OrderDetail(BaseModel):
    item_option_title_id: int
    item_option_id: int


class CUOrderSchema(BaseModel):
    item_id: int
    order_details: list[_OrderDetail]
    count: int