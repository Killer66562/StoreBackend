import uuid

from fastapi import Depends, Response, UploadFile
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.dependencies.base import get_current_user, get_db, get_password_hash
from app.models.models import User
from app.schemas.general import RegisterSchema, UserSchema
from app.routes.user import store, order, cart_item, buy_next_time_item


router = APIRouter(prefix="/user", tags=["User"])

router.include_router(store.router)
router.include_router(order.router)
router.include_router(cart_item.router)
router.include_router(buy_next_time_item.router)

@router.get("", response_model=UserSchema)
def get_user_info(user: User = Depends(get_current_user)):
    return user

@router.put("", response_model=UserSchema)
def update_user_data(data: RegisterSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.id != user.id, or_(User.username == data.username, User.email == data.email)).first()
    if user_exist:
        return JSONResponse(content={"message": "重複的使用者名稱或電子郵件信箱"}, status_code=409)
    user.username = data.username
    user.email = data.email
    if len(data.password) > 0:
        user.password = get_password_hash(data.password)
    db.commit()
    return user

@router.put("/icon", response_model=UserSchema)
def update_user_icon(icon: UploadFile | None = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if icon is None:
        user.icon = None
        db.commit()
        return Response(content=None, status_code=204)
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
    with open(f"app/static/{filename}", "wb") as image:
        image.write(icon.file.read())
    user.icon = filename
    db.commit()
    return Response(content=None, status_code=204)

@router.delete("/icon")
def delete_user_icon(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.icon = None
    db.commit()
    return Response(content=None, status_code=204)