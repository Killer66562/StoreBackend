from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from sqlalchemy.orm import Session

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from models import CartItem, Item, Order, User, Store, District

from schemas.user import CUCartItemSchema
from schemas.general import FullCartItemSchema

from dependencies import get_current_user, get_db


router = APIRouter(prefix="/cart_items")

@router.get("", response_model=list[FullCartItemSchema])
def get_user_cart_items(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    return user_cart_items

@router.post("")
def create_user_cart_item(data: CUCartItemSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == data.item_id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    if item.store.user_id == user.id:
        return JSONResponse(content={"message": "你不能將自己商店中的商品加入購物車"}, status_code=400)
    cart_item = CartItem(**data.model_dump(), user_id=user.id)
    db.add(cart_item)
    db.commit()
    return cart_item

@router.put("/{cart_item_id}")
def update_user_cart_item(cart_item_id: int, data: CUCartItemSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.user_id == user.id, CartItem.id == cart_item_id).first()
    if not cart_item:
        return JSONResponse(content={"message", "資源不存在或無權存取"}, status_code=400)
    cart_item.count = data.count
    db.commit()
    return cart_item

@router.delete("/{cart_item_id}")
def delete_user_cart_item(cart_item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.user_id == user.id, CartItem.id == cart_item_id).first()
    if not cart_item:
        return JSONResponse(content={"message", "資源不存在或無權存取"}, status_code=400)
    db.delete(cart_item)
    db.commit()
    return Response(status_code=204)

add_pagination(router)