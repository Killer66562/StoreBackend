from fastapi import Depends
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from models import User, Store

from schemas import CUStoreSchema

from dependencies import get_current_user, get_current_admin_user, get_db, get_store

from exceptions import PermissionException, DuplicateModelException


router = APIRouter(prefix="/stores")

@router.get("")
def index(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("", response_model=None)
def create(data: CUStoreSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.store:
        raise DuplicateModelException("Store")
    store = Store(**data.model_dump(), user_id=user.id)
    db.add(store)
    db.commit()
    return store

@router.get("/{store_id}")
def fetch(store: Store = Depends(get_store), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return store

@router.put("/{store_id}")
def update(data, store: Store = Depends(get_store), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if store.user_id != user.id and not user.is_admin:
        raise PermissionException()
    #Updation

    #Always do these things
    db.commit()
    db.refresh(store)
    return store

@router.delete("/{store_id}")
def delete(store: Store = Depends(get_store), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if store.user_id != user.id and not user.is_admin:
        raise PermissionException()
    db.delete(store)
    return store