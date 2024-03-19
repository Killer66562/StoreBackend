from fastapi import Depends
from fastapi.routing import APIRouter

from dependencies import get_current_user

from models import User

from . import store, order, cart_item


router = APIRouter(prefix="/user")

router.include_router(store.router)
router.include_router(order.router)
router.include_router(cart_item.router)

@router.get("")
def get_user_info(user: User = Depends(get_current_user)):
    return user