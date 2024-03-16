from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from sqlalchemy.orm import Session

from models import Item, ItemOption, ItemOptionTitle, Order, OrderDetail, User, Store, District

from schemas.user import CUItemOptionSchema, CUStoreSchema, CUItemSchema, CUItemOptionTitleSchema
from schemas.general import FullItemSchema, ItemOptionSchema, ItemOptionTitleSchema, ItemSchema, StoreSchema

from dependencies import get_current_user, get_db


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

@router.get("/items", response_model=list[FullItemSchema], status_code=200)
def get_user_store_items(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    return user.store.items

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

#新增商品選項標題
@router.post("/items/{item_id}/item_option_titles", response_model=ItemOptionTitleSchema, status_code=201)
def get_user_item_item_option_titles(item_id: int, data: CUItemOptionTitleSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option_title_exist = db.query(ItemOptionTitle).filter(ItemOptionTitle.name == data.name).first()
    if item_option_title_exist:
        return JSONResponse(content={"message": "已存在同名的商品選項標題"}, status_code=409)
    item_option_title = ItemOptionTitle(**data.model_dump(), item_id=item_id)
    db.add(item_option_title)
    db.commit()
    return item_option_title

@router.put("/items/{item_id}/item_option_titles/{item_option_title_id}", response_model=ItemOptionTitleSchema, status_code=200)
def get_user_item_item_option_titles(item_id: int, item_option_title_id: int, data: CUItemOptionTitleSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=409)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option_title = db.query(ItemOptionTitle).filter(ItemOptionTitle.id == item_option_title_id, ItemOptionTitle.item_id == item_id).first()
    if not item_option_title:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option_title_exist = db.query(ItemOptionTitle).filter(ItemOptionTitle.name == data.name, ItemOptionTitle.id != item_option_title_id).first()
    if item_option_title_exist:
        return JSONResponse(content={"message": "已存在同名的商品選項標題"}, status_code=409)
    item_option_title.name = data.name
    db.commit()
    return item_option_title

@router.delete("/items/{item_id}/item_option_titles/{item_option_title_id}", status_code=204)
def get_user_item_item_option_titles(item_id: int, item_option_title_id: int, data: CUItemOptionTitleSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option_title = db.query(ItemOptionTitle).filter(ItemOptionTitle.id == item_option_title_id, ItemOptionTitle.item_id == item_id).first()
    if not item_option_title:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    db.delete(item_option_title)
    db.commit()
    return Response(status_code=204)

@router.post("/items/{item_id}/item_option_titles/{item_option_title_id}/item_options", response_model=ItemOptionSchema, status_code=201)
def create_user_item_item_option(item_id: int, item_option_title_id: int, data: CUItemOptionSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option_title = db.query(ItemOptionTitle).filter(ItemOptionTitle.id == item_option_title_id, ItemOptionTitle.item_id == item_id).first()
    if not item_option_title:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option_exist = db.query(ItemOption).filter(ItemOption.name == data.name, ItemOption.item_option_title_id == item_option_title_id).first()
    if item_option_exist:
        return JSONResponse(content={"message": "已存在同名的商品選項"}, status_code=409)
    item_option = ItemOption(**data.model_dump(), item_option_title_id=item_option_title_id)
    db.add(item_option)
    db.commit()
    return item_option

@router.put("/items/{item_id}/item_option_titles/{item_option_title_id}/item_options/{item_option_id}", response_model=ItemOptionSchema, status_code=200)
def create_user_item_item_option(item_id: int, item_option_title_id: int, item_option_id: int, data: CUItemOptionSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option_title = db.query(ItemOptionTitle).filter(ItemOptionTitle.id == item_option_title_id, ItemOptionTitle.item_id == item_id).first()
    if not item_option_title:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option = db.query(ItemOption).filter(ItemOption.id == item_option_id, ItemOption.item_option_title_id == item_option_title_id).first()
    if not item_option:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    order_with_this_item_option_id = db.query(OrderDetail).filter(OrderDetail.item_option_id == item_option_id).first()
    if order_with_this_item_option_id and item_option.additional_price != data.additional_price:
        return JSONResponse(content={"message": "有訂單包含這個商品選項，您暫時無法更改此商品選項的價格。"}, status_code=400)
    item_option_exist = db.query(ItemOption).filter(ItemOption.name == data.name, ItemOption.item_option_title_id == item_option_title_id, ItemOption.id != item_option_id).first()
    if item_option_exist:
        return JSONResponse(content={"message": "已存在同名的商品選項"}, status_code=409)
    item_option.name = data.name
    item_option.additional_price = data.additional_price
    item_option.remaining = data.remaining
    db.commit()
    return item_option

@router.delete("/items/{item_id}/item_option_titles/{item_option_title_id}/item_options/{item_option_id}")
def delete_user_item_item_option(item_id: int, item_option_title_id: int, item_option_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option_title = db.query(ItemOptionTitle).filter(ItemOptionTitle.id == item_option_title_id, ItemOptionTitle.item_id == item_id).first()
    if not item_option_title:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    item_option = db.query(ItemOption).filter(ItemOption.id == item_option_id, ItemOption.item_option_title_id == item_option_title_id).first()
    if not item_option:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    order_with_this_item_option_id = db.query(OrderDetail).filter(OrderDetail.item_option_id == item_option_id).first()
    if order_with_this_item_option_id:
        return JSONResponse(content={"message": "有訂單包含這個商品選項，您暫時無法刪除此商品選項。"}, status_code=400)
    db.delete(item_option)
    db.commit()
    return Response(status_code=204)