from fastapi import Depends, Response
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import User, ItemOptionTitle, ItemOption

from schemas import CUItemOptionSchema

from dependencies import get_current_user, get_db, get_item_option_title, get_item_option

from exceptions import PermissionException, ModelNotFoundException, DuplicateModelException


router = APIRouter(prefix="/item_options")

'''
CUD permission required: admin, store owner

If an item_option_title have another item_option that its name is the same as the name of the data,
the item_option cannot be created or be updated to that name.
'''
@router.post("")
def create(data: CUItemOptionSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item_option_title_query = db.query(ItemOptionTitle).filter(ItemOptionTitle.id == data.item_option_title_id)
    item_option_title = item_option_title_query.first()
    if not item_option_title:
        raise ModelNotFoundException("ItemOptionTitle", data.item_option_title_id)
    if item_option_title.item.store.user_id != user.id and not user.is_admin:
        raise PermissionException()
    item_option_existing = item_option_title_query.join(ItemOption, ItemOption.name == data.name).first()
    if item_option_existing:
        raise DuplicateModelException("name")
    item_option = ItemOption(**data.model_dump())
    db.add(item_option)
    db.commit()
    return item_option

@router.put("/{item_option_id}")
def update(data: CUItemOptionSchema, item_option: ItemOption = Depends(get_item_option), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item_option_title_query = db.query(ItemOptionTitle).filter(ItemOptionTitle.id == data.item_option_title_id)
    item_option_title = item_option_title_query.first()
    if not item_option_title:
        raise ModelNotFoundException("ItemOptionTitle", data.item_option_title_id)
    if item_option_title.item.store.user_id != user.id and not user.is_admin:
        raise PermissionException()
    item_option_existing = item_option_title_query.join(ItemOption, and_(ItemOption.name == data.name, ItemOption.id != item_option.id)).first()
    if item_option_existing:
        raise DuplicateModelException("name")
    item_option.name = data.name
    item_option.price = data.price
    item_option.remaining = data.remaining
    item_option.item_option_title_id = data.item_option_title_id
    db.commit()
    return item_option

@router.delete("/{item_option_id}")
def delete(item_option: ItemOption = Depends(get_item_option), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if item_option.option_title.item.store.user_id != user.id and not user.is_admin:
        raise PermissionException()
    db.delete(item_option)
    db.commit()
    return Response(status_code=204)