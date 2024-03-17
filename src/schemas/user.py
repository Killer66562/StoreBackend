from pydantic import BaseModel


class CUStoreSchema(BaseModel):
    name: str
    introduction: str
    district_id: int


class CUItemSchema(BaseModel):
    name: str
    introduction: str
    count: int
    price: int


class CUItemOptionTitleSchema(BaseModel):
    name: str


class CUItemOptionSchema(BaseModel):
    name: str
    additional_price: int
    remaining: int


class CUOrderSchema(BaseModel):
    item_id: int
    count: int