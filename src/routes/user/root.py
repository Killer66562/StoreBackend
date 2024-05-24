import uuid

from fastapi import Depends, Response, UploadFile
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db

from models import User

from . import store, order, cart_item, buy_next_time_item

from dependencies import get_db

from schemas.general import UserSchema

router = APIRouter(prefix="/user", tags=["User"])

router.include_router(store.router)
router.include_router(order.router)
router.include_router(cart_item.router)
router.include_router(buy_next_time_item.router)

@router.get("", response_model=UserSchema)
def get_user_info(user: User = Depends(get_current_user)):
    return user

@router.put("", response_model=UserSchema)
def update_user_icon(icon: UploadFile | None = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if icon is None:
        user.icon = None
        db.commit()
        return Response(content=None, status_code=204)
    if icon.content_type != "image/jpeg" and icon.content_type != "image/png":
        return JSONResponse(content={"message": "只接受.jpeg和.png檔案"}, status_code=400)
    if icon.size > 1024 * 1024:
        return JSONResponse(content={"message": "icon大小請勿超過1MB"}, status_code=400)
    icon.file.seek(0)
    filename = str(uuid.uuid4())
    if icon.content_type == "image/jpeg":
        filename = filename + ".jpg"
    elif icon.content_type == "image/png":
        filename = filename + ".png"
    with open(f"static/{filename}", "wb") as image:
        image.write(icon.file.read())
    user.icon = filename
    db.commit()
    return Response(content=None, status_code=204)