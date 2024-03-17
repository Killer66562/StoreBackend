from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from sqlalchemy.orm import Session

from models import Item, User, Store, District

from schemas.user import CUStoreSchema, CUItemSchema
from schemas.general import ItemSchema, StoreSchema

from dependencies import get_current_user, get_db

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter(prefix="/store")

#取得使用者的商店
@router.get("")
def get_user_store(user: User = Depends(get_current_user)):
    return user.store

#為使用者創建商店
@router.post("", response_model=StoreSchema)
def create_user_store(data: CUStoreSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.store:
        return JSONResponse(content={"message": "你已經創建了一個商店"}, status_code=409)
    if not db.query(District).filter(District.id == data.district_id).first():
        return JSONResponse(content={"message": "該區域不存在"}, status_code=400)
    store = Store(**data.model_dump(), user_id=user.id)
    db.add(store)
    db.commit()
    return store

#更新使用者的商店
@router.put("")
def update_user_store(data: CUStoreSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    if not db.query(District).filter(District.id == data.district_id).first():
        return JSONResponse(content={"message": "該區域不存在"}, status_code=400)
    user.store.name = data.name
    user.store.introduction = data.introduction
    user.store.district_id = data.district_id
    db.commit()
    return user.store

#刪除使用者的商店
@router.delete("")
def delete_user_store(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    db.delete(user.store)
    db.commit()
    return Response(content=None, status_code=204)

@router.get("/items", response_model=Page[ItemSchema], status_code=200)
def get_user_store_items(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    return paginate(db.query(Item).filter(Item.store_id == user.store.id))

@router.post("/items", response_model=ItemSchema)
def create_item_for_user_store(data: CUItemSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = Item(**data.model_dump(), store_id=user.store.id)
    db.add(item)
    db.commit()
    return item

@router.put("/items/{item_id}", response_model=ItemSchema)
def update_item_from_user_store(item_id: int, data: CUItemSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item.name = data.name
    item.introduction = data.introduction
    item.count = data.count
    item.price = data.price
    db.commit()
    return item

#刪除使用者商店中的特定物品
@router.delete("/items/{item_id}")
def delete_item_from_user_store(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    db.delete(item)
    db.commit()
    return Response(content=None, status_code=204)