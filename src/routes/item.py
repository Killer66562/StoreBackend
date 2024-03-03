from fastapi import Depends, Response
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import User, Item

from schemas import CUItemSchema

from dependencies import get_current_user, get_db, get_item

from exceptions import PermissionException


router = APIRouter(prefix="/items")

@router.get("")
def index(db: Session = Depends(get_db)):
    return db.query(Item).order_by(desc(Item.id)).all()

@router.post("")
def create(data: CUItemSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store or (user.store.id != data.store_id and not user.is_admin):
        raise PermissionException()
    item = Item(**data.model_dump())
    db.add(item)
    db.commit()
    return item

@router.get("/{item_id}")
def fetch(item: Item = Depends(get_item)):
    return item

@router.put("/{item_id}")
def update(data: CUItemSchema, item: Item = Depends(get_item), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store or (user.store.id != data.store_id and user.store.id != item.store_id and not user.is_admin):
        raise PermissionException()
    item.name = data.name
    item.introduction = data.introduction
    item.store_id = data.store_id
    db.commit()
    return item

@router.delete("/{item_id}")
def delete(item: Item = Depends(get_item), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store or (item.store_id != user.store.id and not user.is_admin):
        raise PermissionException()
    db.delete(item)
    db.commit()
    return Response(status_code=204)