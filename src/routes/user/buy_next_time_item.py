from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from sqlalchemy.orm import Session

from models import BuyNextTimeItem, Item, Order, User, Store, District

from schemas.user import CUOrderSchema, CUBuyNextTimeItemSchema
from schemas.general import ItemSchema, OrderSchema, StoreSchema

from dependencies import get_current_user, get_db

from enums import OrderStatus


router = APIRouter(prefix="/buy_next_time_items")

@router.get("")
def get_user_buy_next_time_items(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return user.buy_next_time_items

@router.post("")
def create_user_buy_next_time_item(data: CUBuyNextTimeItemSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == data.item_id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    '''
    if item.store.user_id == user.id:
        return JSONResponse(content={"message": "你不能將自己商店中的商品加入願望清單"}, status_code=400)
    '''
    buy_next_time_item = db.query(BuyNextTimeItem).filter(BuyNextTimeItem.user_id == user.id, BuyNextTimeItem.item_id == item.id).first()
    if buy_next_time_item:
        return buy_next_time_item
    new_buy_next_time_item = BuyNextTimeItem(item_id=data.item_id, user_id=user.id)
    db.add(new_buy_next_time_item)
    db.commit()
    return new_buy_next_time_item

@router.delete("/{buy_next_time_item_id}")
def delete_user_buy_next_time_item(buy_next_time_item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    buy_next_time_item = db.query(BuyNextTimeItem).filter(BuyNextTimeItem.user_id == user.id, BuyNextTimeItem.id == buy_next_time_item_id).first()
    if not buy_next_time_item:
        return JSONResponse(content={"message", "資源不存在或無權存取"}, status_code=400)
    db.delete(buy_next_time_item)
    db.commit()
    return Response(status_code=204)
