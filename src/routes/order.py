from fastapi.routing import APIRouter

from schemas import CUOrderSchema

from models import Order


router = APIRouter(prefix="/orders")

@router.post(path="")
def create(data: list[CUOrderSchema]):
    if len(data) <= 0:
        raise Exception()
    orders = [Order(**order_data, user_id=user.id)]