from fastapi import Depends, Response
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session
from sqlalchemy import desc

from enums import OrderStatus

from models import User, Order

from schemas import CUOrderSchema, UOrderStatusSchema

from dependencies import get_current_user, get_current_admin_user, get_db, get_order

from exceptions import PermissionException


router = APIRouter(prefix="/orders")

@router.get("")
def index(user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    return db.query(Order).order_by(desc(Order.id)).all()

@router.post("")
def create(data: CUOrderSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = Order(**data.model_dump())
    db.add(order)
    db.commit()
    return order

@router.get("/{order_id}")
def fetch(order: Order = Depends(get_order), user: User = Depends(get_current_user)):
    if not user.is_admin and order.owner.id != user.id and order.item_option.option_title.item.store.user_id != user.id:
        raise PermissionException()
    return order

@router.put("/{order_id}")
def update(data: UOrderStatusSchema, order: Order = Depends(get_order), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if order.item_option.option_title.item.store.user_id != user.id and not user.is_admin:
        raise PermissionException()
    order.status.value = data.status.value
    db.commit()
    return order

@router.delete("/{order_id}")
def delete(order: Order = Depends(get_order), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if order.owner.id != user.id or (order.status.value > OrderStatus.NOT_DELIVERED.value and not user.is_admin):
        raise PermissionException()
    db.delete(order)
    db.commit()
    return Response(status_code=204)