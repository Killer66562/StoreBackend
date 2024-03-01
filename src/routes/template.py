from fastapi import Depends
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from models import User, Store

from schemas import CUStoreSchema

from dependencies import get_current_user, get_current_admin_user, get_db, get_store

from exceptions import PermissionException, DuplicateModelException


router = APIRouter(prefix="")

@router.get("")
def index(db: Session = Depends(get_db)):
    pass

@router.post("")
def create(*, db: Session = Depends(get_db)):
    pass

@router.get("/{}")
def fetch(*, db: Session = Depends(get_db)):
    pass

@router.put("/{}")
def update(*, db: Session = Depends(get_db)):
    pass

@router.delete("/{}")
def delete(*, db: Session = Depends(get_db)):
    pass