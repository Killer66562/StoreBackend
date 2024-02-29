from pydantic import BaseModel


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


class AdminCUStoreSchema(CUStoreSchema):
    user_id: int


class CUOrderSchema(BaseModel):
    item_option_id: int
    count: int