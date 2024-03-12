from pydantic import BaseModel


class CUCitySchema(BaseModel):
    name: str


class CUDistrictSchema(BaseModel):
    name: str
    city_id: int