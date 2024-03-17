from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from sqlalchemy.orm import Session

from models import Item, User, Store, District

from schemas.user import CUStoreSchema, CUItemSchema
from schemas.general import FullItemSchema, ItemSchema, StoreSchema

from dependencies import get_current_user, get_db


router = APIRouter(prefix="/items")

@router.get("", response_model=list[FullItemSchema], status_code=200)
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.get("/{item_id}", response_model=FullItemSchema)
def get_specific_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在"})
    return item