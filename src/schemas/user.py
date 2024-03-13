from pydantic import BaseModel


class CUStoreSchema(BaseModel):
    name: str
    introduction: str
    district_id: int


class CUItemSchema(BaseModel):
    name: str
    introduction: str


class CUItemOptionTitleSchema(BaseModel):
    name: str


class CUItemOptionSchema(BaseModel):
    name: str
    price: int
    remaining: int