from fastapi import Depends, Response
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from models import User, Store

from schemas import CUStoreSchema

from dependencies import get_current_user, get_current_admin_user, get_db, get_store

from exceptions import PermissionException, DuplicateModelException


router = APIRouter(prefix="/stores")

@router.get("")
def index(db: Session = Depends(get_db)):
    return db.query(Store).all()

@router.post("", response_model=None)
def create(data: CUStoreSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.user_id == data.user_id).first()
    if store:
        raise DuplicateModelException("Store")
    if user.id != data.user_id and not user.is_admin:
        raise PermissionException()
    store = Store(**data.model_dump())
    db.add(store)
    db.commit()
    return store

@router.get("/{store_id}")
def fetch(store: Store = Depends(get_store)):
    return store

@router.put("/{store_id}")
def update(data: CUStoreSchema, store: Store = Depends(get_store), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if store.user_id != data.user_id and store.user_id != user.id and not user.is_admin:
        raise PermissionException()
    #Updation
    store.name = data.name
    store.district_id = data.district_id
    store.user_id = data.user_id
    store.introduction = data.introduction
    #Always do these things
    db.commit()
    return store

@router.delete("/{store_id}")
def delete(store: Store = Depends(get_store), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if store.user_id != user.id and not user.is_admin:
        raise PermissionException()
    db.delete(store)
    db.commit()
    return Response(status_code=204)