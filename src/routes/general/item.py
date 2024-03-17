from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from models import Item

from schemas.general import FullItemSchema

from dependencies import  get_db


router = APIRouter(prefix="/items")

@router.get("", response_model=Page[FullItemSchema], status_code=200)
def get_items(db: Session = Depends(get_db)):
    return paginate(db.query(Item))

@router.get("/{item_id}", response_model=FullItemSchema)
def get_specific_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在"})
    return item