import uuid

from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response, UploadFile

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from enums import ItemQueryOrderByEnum, OrderStatus
from models import BuyNextTimeItem, CartItem, Item, ItemImage, ItemReport, Order, User, Store, District

from schemas.user import CUOrderSchema, CUStoreSchema, CUItemSchema
from schemas.general import FullItemSchema, FullOrderSchema, ItemQuerySchema, ItemSchema, OrderSchema, StoreSchema

from dependencies import get_current_user, get_db

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter(prefix="/store")

#取得使用者的商店
@router.get("", response_model=StoreSchema)
def get_user_store(user: User = Depends(get_current_user)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
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

@router.put("/icon")
def update_user_store_icon(icon: UploadFile, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    if icon.content_type != "image/jpeg" and icon.content_type != "image/png":
        return JSONResponse(content={"message": "只接受.jpeg和.png檔案"}, status_code=400)
    if icon.size > 2048 * 2048:
        return JSONResponse(content={"message": "icon大小請勿超過1MB"}, status_code=400)
    icon.file.seek(0)
    filename = str(uuid.uuid4())
    if icon.content_type == "image/jpeg":
        filename = filename + ".jpg"
    elif icon.content_type == "image/png":
        filename = filename + ".png"
    with open(f"static/{filename}", "wb") as image:
        image.write(icon.file.read())
    user.store.icon = filename
    db.commit()
    return Response(content=None, status_code=204)

@router.delete("/icon")
def delete_user_store_icon(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    user.store.icon = None
    db.commit()
    return Response(content=None, status_code=204)

@router.get("/items", response_model=Page[FullItemSchema], status_code=200)
def get_user_store_items(query: ItemQuerySchema = Depends(), user: User = Depends(get_current_user), db: Session = Depends(get_db)):      
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    
    items_query = db.query(Item).filter(Item.store_id == user.store.id)

    if query.name is not None:
        names = query.name.split(" ")
        items_query = items_query.filter(or_(*[Item.name.like(f"%{name}%") for name in names]))

    if query.order_by is not None:
        if query.order_by == ItemQueryOrderByEnum.ID:
            items_query = items_query.order_by(Item.id if query.desc is True else desc(Item.id))
        elif query.order_by == ItemQueryOrderByEnum.NAME:
            items_query = items_query.order_by(desc(Item.name) if query.desc is True else Item.name).order_by(Item.id if query.desc is True else desc(Item.id))
        elif query.order_by == ItemQueryOrderByEnum.PRICE:
            items_query = items_query.order_by(Item.price if query.desc is True else desc(Item.price)).order_by(Item.id if query.desc is True else desc(Item.id))
        elif query.order_by == ItemQueryOrderByEnum.HOTTEST:
            items_query = items_query.order_by(desc(Item.comment_counts) if query.desc is True else Item.comment_counts).order_by(Item.id if query.desc is True else desc(Item.id))
        elif query.order_by == ItemQueryOrderByEnum.BEST:
            items_query = items_query.order_by(desc(Item.average_stars ) if query.desc is True else Item.average_stars).order_by(Item.id if query.desc is True else desc(Item.id))
    else:
        items_query = items_query.order_by(Item.id if query.desc is True else desc(Item.id))
    
    return paginate(items_query)

@router.post("/items", response_model=FullItemSchema)
def create_item_for_user_store(data: CUItemSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = Item(**data.model_dump(), store_id=user.store.id)
    db.add(item)
    db.commit()
    return item

@router.get("/items/{item_id}", response_model=FullItemSchema)
def get_item_from_user_store(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    return item

@router.put("/items/{item_id}", response_model=FullItemSchema)
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
    item.need_18 = data.need_18
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
    liked_item_exist = db.query(BuyNextTimeItem).filter(BuyNextTimeItem.item_id == item_id).first()
    if liked_item_exist:
        return JSONResponse(content={"message": "尚有用戶的願望清單包含本商品"}, status_code=400)
    cart_item_exist = db.query(CartItem).filter(CartItem.item_id == item_id).first()
    if cart_item_exist:
        return JSONResponse(content={"message": "尚有用戶的購物車包含本商品"}, status_code=400)
    order_exist = db.query(Order).filter(Order.item_id == item_id, Order.status != OrderStatus.DONE.value).first()
    if order_exist:
        return JSONResponse(content={"message": "尚有包含本商品且未完成的訂單"}, status_code=400)
    item_reports = db.query(ItemReport).filter(ItemReport.reported_item_id == item_id).all()

    for item_report in item_reports:
        db.delete(item_report)
        
    db.delete(item)
    db.commit()
    return Response(content=None, status_code=204)

@router.put("/items/{item_id}/icon")
def update_item_icon_from_user_store(item_id: int, icon: UploadFile, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    if icon.content_type != "image/jpeg" and icon.content_type != "image/png":
        return JSONResponse(content={"message": "只接受.jpeg和.png檔案"}, status_code=400)
    if icon.size > 2048 * 2048:
        return JSONResponse(content={"message": "icon大小請勿超過1MB"}, status_code=400)
    icon.file.seek(0)
    filename = str(uuid.uuid4())
    if icon.content_type == "image/jpeg":
        filename = filename + ".jpg"
    elif icon.content_type == "image/png":
        filename = filename + ".png"
    with open(f"static/{filename}", "wb") as image:
        image.write(icon.file.read())
    item.icon = filename
    db.commit()
    return Response(content=None, status_code=204)

@router.delete("/items/{item_id}/icon")
def delete_item_icon_from_user_store(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    db.delete(item.icon)
    db.commit()
    return Response(status_code=204)

@router.post("/items/{item_id}/images")
def add_item_images_from_user_store(item_id: int, images: list[UploadFile], user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    if len(images) > 10:
        return JSONResponse(content={"message": "一次最多只能上傳10張圖片"}, status_code=400)
    for img in images:
        if img.content_type != "image/jpeg" and img.content_type != "image/png":
            return JSONResponse(content={"message": "只接受.jpeg和.png檔案"}, status_code=400)
        if img.size > 2048 * 2048:
            return JSONResponse(content={"message": "圖片大小請勿超過1MB"}, status_code=400)
    item_images = []
    for img in images:
        img.file.seek(0)
        filename = str(uuid.uuid4())
        if img.content_type == "image/jpeg":
            filename = filename + ".jpg"
        elif img.content_type == "image/png":
            filename = filename + ".png"
        with open(f"static/{filename}", "wb") as image:
            image.write(img.file.read())
        item_image = ItemImage(item_id=item_id, path=filename)
        item_images.append(item_image)
    db.add_all(item_images)
    db.commit()
    return Response(content=None, status_code=204)

@router.put("/items/{item_id}/images")
def fully_update_item_images_from_user_store(item_id: int, images: list[UploadFile], user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    item = db.query(Item).filter(Item.id == item_id, Item.store_id == user.store.id).first()
    if not item:
        return JSONResponse(content={"message": "資源不存在或無權存取"}, status_code=400)
    if len(images) > 10:
        return JSONResponse(content={"message": "一次最多只能上傳10張圖片"}, status_code=400)
    for img in images:
        if img.content_type != "image/jpeg" and img.content_type != "image/png":
            return JSONResponse(content={"message": "只接受.jpeg和.png檔案"}, status_code=400)
        if img.size > 2048 * 2048:
            return JSONResponse(content={"message": "圖片大小請勿超過1MB"}, status_code=400)
    item_images = []
    for img in images:
        img.file.seek(0)
        filename = str(uuid.uuid4())
        if img.content_type == "image/jpeg":
            filename = filename + ".jpg"
        elif img.content_type == "image/png":
            filename = filename + ".png"
        with open(f"static/{filename}", "wb") as image:
            image.write(img.file.read())
        item_image = ItemImage(item_id=item_id, path=filename)
        item_images.append(item_image)
    for item_img in item.images:
        db.delete(item_img)
    for item_image in item_images:
        db.add_all(item_images)
    db.commit()
    return Response(content=None, status_code=204)

@router.get("/orders", response_model=Page[FullOrderSchema])
def get_store_orders(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    orders_query = db.query(Order).join(Item, Order.item_id == Item.id).filter(Item.store_id == user.store.id).order_by(desc(Order.id), Order.status)
    return paginate(orders_query)

@router.put("/orders/{order_id}", response_model=FullOrderSchema)
def update_store_order(order_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return JSONResponse(content={"message": "訂單不存在"}, status_code=404)
    if order.item.store_id != user.store.id:
        return JSONResponse(content={"message": "訂單不存在"}, status_code=404)
    if order.item.count < order.count:
        return JSONResponse(content={"message": "商品數量不足，請補貨。"}, status_code=400)
    if order.status != OrderStatus.NOT_DELIVERED.value:
        return JSONResponse(content={"message": "商品已出貨或已完成"}, status_code=400)
    order.status = OrderStatus.PROCESSING.value
    order.item.count = order.item.count - order.count
    db.commit()
    return order

@router.delete("/orders/{order_id}")
def delete_store_order(order_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.store:
        return JSONResponse(content={"message": "你尚未創建商店"}, status_code=400)
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return JSONResponse(content={"message": "訂單不存在"}, status_code=404)
    if order.item.store_id != user.store.id:
        return JSONResponse(content={"message": "訂單不存在"}, status_code=404)
    if order.status != OrderStatus.NOT_DELIVERED.value:
        return JSONResponse(content={"message": "商品已出貨或已完成"}, status_code=400)
    db.delete(order)
    db.commit()
    return Response(status_code=204)

add_pagination(router)