from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response
from sqlalchemy.orm import Session
from models import Item, User, Store, District
from schemas.user import CUStore
from dependencies import get_current_user, get_db
from exceptions import DuplicateModelException


router = APIRouter(prefix="/store")

#取得使用者的商店
@router.get("")
def get_user_store(user: User = Depends(get_current_user)):
    return user.store

#為使用者創建商店
@router.post("")
def create_user_store(data: CUStore, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.store:
        return JSONResponse(content={"message": "你已經創建了一個商店"}, status_code=409)
    if not db.query(District).filter(District.id == data.district_id).first():
        return JSONResponse(content={"message": "該區域不存在"}, status_code=409)
    store = Store(**data.model_dump(), user_id=user.id)
    db.add(store)
    db.commit()
    return store

#更新使用者的商店
@router.put("")
def update_user_store(data: CUStore, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=409)
    if not db.query(District).filter(District.id == data.district_id).first():
        return JSONResponse(content={"message": "該區域不存在"}, status_code=409)
    user.store.name = data.name
    user.store.introduction = data.introduction
    user.store.district_id = data.district_id
    db.commit()
    return user.store

#刪除使用者的商店
@router.delete("")
def delete_user_store(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=409)
    db.delete(user.store)
    db.commit()
    return Response(content=None, status_code=204)

#刪除使用者商店中的特定物品
@router.delete("/items/{item_id}")
def delete_item_from_user_store(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item or item not in user.store.items:
        return JSONResponse(content={"message": "資源不存在或無權存取"})
    db.delete(item)
    db.commit()
    return Response(content=None, status_code=204)