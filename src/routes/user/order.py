from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from sqlalchemy.orm import Session

from models import Item, ItemOption, ItemOptionTitle, Order, User, Store, District

from schemas.user import CUItemOptionSchema, CUStoreSchema, CUItemSchema, CUItemOptionTitleSchema
from schemas.general import FullItemSchema, ItemOptionSchema, ItemOptionTitleSchema, ItemSchema, StoreSchema

from dependencies import get_current_user, get_db


router = APIRouter(prefix="/orders")

@router.get("")
def get_user_owned_orders(user: User = Depends(get_current_user)):
    return user.orders