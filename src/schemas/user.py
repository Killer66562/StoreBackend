from pydantic import BaseModel


class CUStore(BaseModel):
    name: str
    introduction: str
    district_id: int