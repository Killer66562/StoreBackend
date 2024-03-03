from fastapi import Depends, Response
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from models import User, Item, ItemOptionTitle

from schemas import CUItemOptionTitleSchema

from dependencies import get_current_user, get_db, get_item_option_title

from exceptions import PermissionException, ModelNotFoundException


router = APIRouter(prefix="/items")

'''
CUD permission required: admin, store owner

If an item have another item_option_title that its name is the same as the name of the data,
the item_option_title cannot be created or be updated to that name.
'''

@router.post("")
def create(data: CUItemOptionTitleSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == data.item_id).first()
    if not item:
        raise ModelNotFoundException("Item", data.item_id)
    if item.store.user_id != user.id and not user.is_admin:
        raise PermissionException()
    item_option_title = ItemOptionTitle(**data.model_dump())
    db.add(item_option_title)
    db.commit()
    return item_option_title

@router.put("/{item_option_title_id}")
def update(data: CUItemOptionTitleSchema, item_option_title: ItemOptionTitle = Depends(get_item_option_title), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if item_option_title.item.store.id != user.id and not user.is_admin:
        raise PermissionException()
    item_option_title.name = data.name
    item_option_title.item_id = data.item_id
    db.commit()
    return item_option_title

@router.delete("/{item_option_title_id}")
def delete(item_option_title: ItemOptionTitle = Depends(get_item_option_title), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if item_option_title.item.store.id != user.id and not user.is_admin:
        raise PermissionException()
    db.delete(item_option_title)
    db.commit()
    return Response(status_code=204)