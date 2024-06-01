from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from sqlalchemy.orm import Session

from models import Item, Order, User, Store, District

from schemas.user import CUOrderSchema
from schemas.general import OrderSchema

from dependencies import get_current_user, get_db

from enums import OrderStatus


router = APIRouter(prefix="/orders")

@router.get("", response_model=list[OrderSchema])
def get_user_owned_orders(user: User = Depends(get_current_user)):
    return user.orders

@router.post("", response_model=list[OrderSchema])
def create_user_order(data: list[CUOrderSchema], user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for order in data:
        item = db.query(Item).filter(Item.id == order.item_id).first()
        if not item:
            return JSONResponse(content={"message": "資源不存在"}, status_code=400)
        if order.count > item.count:
            return JSONResponse(content={"message": "商品不足"}, status_code=400)
        if user.store and item.store_id == user.store.id:
            return JSONResponse(content={"message": "你不能購買自己商店裡的物品"}, status_code=400)
        item.count = item.count - order.count
    orders = [Order(**order.model_dump(), user_id=user.id) for order in data]
    db.add_all(orders)
    db.commit()
    return orders

@router.delete("/{order_id}")
def delete_user_order(order_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    if order.status.value > OrderStatus.NOT_DELIVERED.value:
        return JSONResponse(content={"message": "賣家已出貨，你無法取消訂單。"}, status_code=400)
    db.delete(order)
    db.commit()
    return Response(status_code=204)