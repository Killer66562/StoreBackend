from fastapi import Depends
from fastapi.routing import APIRouter
from dependencies import get_current_user, get_db

from models import User

from sqlalchemy.orm import Session

from . import store

router = APIRouter(prefix="/user")
router.include_router(store.router)

@router.get("")
def get_user_info(user: User = Depends(get_current_user)):
    return user