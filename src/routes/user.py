from fastapi import Depends
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from models import User

from dependencies import get_current_admin_user, get_db


router = APIRouter(prefix="/users")

@router.get("")
def index(user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("")
def create(data, user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    pass

@router.put("/{user_id}")
def update(user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    pass