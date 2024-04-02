import random
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from models import Item

from schemas.general import FullItemSchema

from dependencies import  get_db


router = APIRouter(prefix="/items")

@router.get("", response_model=Page[FullItemSchema], status_code=200)
def get_items(db: Session = Depends(get_db)):
    return paginate(db.query(Item))

@router.get("/hot", response_model=list[FullItemSchema], status_code=200)
def get_items(db: Session = Depends(get_db)):
    hot_items_raw = db.query(Item).order_by(Item.id).limit(50).all()
    hot_items_raw_len = len(hot_items_raw)
    rand_k = 20 if hot_items_raw_len >= 20 else hot_items_raw_len
    hot_items = random.sample(population=hot_items_raw, k=rand_k)
    return sorted(hot_items, key=lambda item : item.id, reverse=False)

@router.get("/good", response_model=list[FullItemSchema], status_code=200)
def get_items(db: Session = Depends(get_db)):
    good_items_raw = db.query(Item).order_by(Item.id).limit(50).all()
    good_items_raw_len = len(good_items_raw)
    rand_k = 20 if good_items_raw_len >= 20 else good_items_raw_len
    good_items = random.sample(population=good_items_raw, k=rand_k)
    return sorted(good_items, key=lambda item : item.id, reverse=True)

@router.get("/{item_id}", response_model=FullItemSchema)
def get_specific_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在"}, status_code=404)
    return item

add_pagination(router)