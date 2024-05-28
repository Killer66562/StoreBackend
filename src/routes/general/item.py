import random
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from enums import ItemQueryOrderByEnum
from models import Item, Comment, Order, User

from schemas.general import CommentSchema, FullCommentSchema, FullItemSchema, CUCommentSchema, ItemQuerySchema

from dependencies import  get_current_user, get_db


router = APIRouter(prefix="/items")

@router.get("", response_model=Page[FullItemSchema], status_code=200)
def get_items(query: ItemQuerySchema = Depends(), db: Session = Depends(get_db)):
    items_query = db.query(Item)

    if query.name is not None:
        names = query.name.split(" ")
        items_query = items_query.filter(or_(*[Item.name.like(f"%{name}%") for name in names]))
    
    if query.order_by is not None:
        if query.order_by == ItemQueryOrderByEnum.ID:
            items_query = items_query.order_by(desc(Item.id) if query.desc is True else Item.id)
        elif query.order_by == ItemQueryOrderByEnum.NAME:
            items_query = items_query.order_by(desc(Item.name) if query.desc is True else Item.name)
        elif query.order_by == ItemQueryOrderByEnum.STORE_ID:
            items_query = items_query.order_by(desc(Item.store_id) if query.desc is True else Item.store_id)
        elif query.order_by == ItemQueryOrderByEnum.HOTTEST:
            pass
        elif query.order_by == ItemQueryOrderByEnum.BEST:
            pass
    else:
        items_query = items_query.order_by(desc(Item.id) if query.desc is True else Item.id)
        
    return paginate(items_query)

@router.get("/hot", response_model=list[FullItemSchema], status_code=200)
def get_hot_items(db: Session = Depends(get_db)):
    hot_items_raw = db.query(Item).outerjoin(Order, Order.item_id == Item.id).order_by(Order.count, Item.id).limit(1000).all()
    hot_items_raw_len = len(hot_items_raw)
    rand_k = 20 if hot_items_raw_len >= 20 else hot_items_raw_len
    hot_items = random.sample(population=hot_items_raw, k=rand_k)
    return sorted(hot_items, key=lambda item : item.id, reverse=False)

@router.get("/best", response_model=list[FullItemSchema], status_code=200)
def get_best_items(db: Session = Depends(get_db)):
    good_items_raw = db.query(Item).order_by(Item.id).limit(1000).all()
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

@router.get("/{item_id}/comments", response_model=list[FullCommentSchema])
def get_specific_item_comments(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在"}, status_code=404)
    return item.comments

@router.put("/{item_id}/comments", response_model=FullCommentSchema)
def add_specific_item_comments(item_id: int, data: CUCommentSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在"}, status_code=404)
    comment = db.query(Comment).filter(Comment.item_id == item_id, Comment.user_id == user.id).first()
    if comment:
        comment.content = data.content
        comment.stars = data.stars
    else:
        comment = Comment(**data.model_dump(), user_id=user.id, item_id=item_id)
        db.add(comment)
    db.commit()
    return comment

@router.get("/{item_id}/comments/{comment_id}", response_model=FullItemSchema)
def get_specific_item(item_id: int, comment_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在"}, status_code=404)
    comment = db.query(Comment).filter(Comment.item_id == item_id, Comment.id == comment_id).first()
    if not comment:
        return JSONResponse(content={"message": "資源不存在"}, status_code=404)
    return comment

add_pagination(router)