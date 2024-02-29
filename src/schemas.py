from pydantic import BaseModel


class CUOrderSchema(BaseModel):
    item_option_id: int
    count: int