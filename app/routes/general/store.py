from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from app.enums.base import ItemQueryOrderByEnum
from app.models.models import Item, Store
from app.schemas.general import FullItemSchema, FullStoreSchema, ItemQuerySchema
from app.dependencies.base import  get_db


router = APIRouter(prefix="/stores")

@router.get("/{store_id}", response_model=FullStoreSchema)
def get_specific_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        return JSONResponse(content={"message": "商店不存在"}, status_code=404)
    return store

@router.get("/{store_id}/items", response_model=Page[FullItemSchema])
def get_specific_store(store_id: int, query: ItemQuerySchema = Depends(), db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        return JSONResponse(content={"message": "商店不存在"}, status_code=404)
    
    items_query = db.query(Item).filter(Item.store_id == store_id)

    if query.need18 is not None:
        items_query = items_query.filter(or_(Item.need_18 == False, Item.need_18 == query.need18))
    else:
        items_query = items_query.filter(Item.need_18 == False)

    if query.name is not None:
        names = query.name.split(" ")
        items_query = items_query.filter(or_(*[Item.name.like(f"%{name}%") for name in names]))

    if query.order_by is not None:
        if query.order_by == ItemQueryOrderByEnum.ID:
            items_query = items_query.order_by(Item.id if query.desc is True else desc(Item.id))
        elif query.order_by == ItemQueryOrderByEnum.NAME:
            items_query = items_query.order_by(desc(Item.name) if query.desc is True else Item.name).order_by(Item.id if query.desc is True else desc(Item.id))
        elif query.order_by == ItemQueryOrderByEnum.STORE_ID:
            items_query = items_query.order_by(desc(Item.store_id) if query.desc is True else Item.store_id).order_by(Item.id if query.desc is True else desc(Item.id))
        elif query.order_by == ItemQueryOrderByEnum.PRICE:
            items_query = items_query.order_by(Item.price if query.desc is True else desc(Item.price)).order_by(Item.id if query.desc is True else desc(Item.id))
        elif query.order_by == ItemQueryOrderByEnum.HOTTEST:
            items_query = items_query.order_by(Item.comment_counts if query.desc is True else desc(Item.comment_counts)).order_by(Item.id if query.desc is True else desc(Item.id))
        elif query.order_by == ItemQueryOrderByEnum.BEST:
            items_query = items_query.order_by(Item.average_stars if query.desc is True else desc(Item.average_stars)).order_by(Item.id if query.desc is True else desc(Item.id))
    else:
        items_query = items_query.order_by(Item.id if query.desc is True else desc(Item.id))

    return paginate(items_query)

add_pagination(router)