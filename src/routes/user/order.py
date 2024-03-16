from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from sqlalchemy.orm import Session

from models import Item, ItemOption, ItemOptionTitle, Order, OrderDetail, User, Store, District

from schemas.user import CUItemOptionSchema, CUOrderSchema, CUStoreSchema, CUItemSchema, CUItemOptionTitleSchema
from schemas.general import FullItemSchema, ItemOptionSchema, ItemOptionTitleSchema, ItemSchema, StoreSchema

from dependencies import get_current_user, get_db

from enums import OrderStatus


router = APIRouter(prefix="/orders")

@router.get("")
def get_user_owned_orders(user: User = Depends(get_current_user)):
    return user.orders

@router.post("")
def create_user_order(data: CUOrderSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == data.item_id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    if user.store and item.store_id == user.store.id:
        return JSONResponse(content={"message": "你不能購買自己商店裡的物品"}, status_code=400)
    #Check if the item_option_titles all belong to item
    item_option_title_ids = [option_title.id for option_title in item.option_titles]
    data_option_title_ids = [order_detail.item_option_title_id for order_detail in data.order_details]
    for item_option_title_id in data_option_title_ids:
        if item_option_title_id not in item_option_title_ids:
            return JSONResponse(content={"message": "商品選項類型不屬於這個商品"}, status_code=400)
    for item_option_title_id in item_option_title_ids:
        if item_option_title_id not in data_option_title_ids:
            return JSONResponse(content={"message": "缺少商品選項類型"}, status_code=400)
    check_board = {}
    for order_detail in data.order_details:
        item_option = db.query(ItemOption).filter(ItemOption.id == order_detail.item_option_id).first()
        if not item_option.item_option_title_id in item_option_title_ids:
            return JSONResponse(content={"message": "商品選項不屬於這個商品"}, status_code=400)
        if check_board.get(item_option.item_option_title_id) is not None:
            return JSONResponse(content={"message": "同一商品選項類型不得有兩個商品選項"})
        check_board[item_option.item_option_title_id] = order_detail.item_option_id
    order = Order(user_id=user.id, item_id=data.item_id, count=data.count)
    db.add(order)
    db.flush()
    order_details = [OrderDetail(order_id=order.id, item_option_id=order_detail.item_option_id) for order_detail in data.order_details]
    db.add_all(order_details)
    db.commit()
    return order

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