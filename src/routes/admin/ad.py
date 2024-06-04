import uuid

from fastapi import Depends, Response, UploadFile
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from dependencies import get_current_admin_user, get_current_user, get_db

from schemas.admin import CUAdSchema, CUCitySchema
from schemas.general import AdSchema, CitySchema

from sqlalchemy.orm import Session

from models import City, District, Store, User, Ad


router = APIRouter(prefix="/ads")

@router.post("", response_model=AdSchema)
def create_ad(data: CUAdSchema, user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    ad = Ad(url=data.url)
    db.add(ad)
    db.commit()
    return ad

@router.put("/{ad_id}", response_model=AdSchema)
def update_ad(ad_id: int, data: CUAdSchema, user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        return JSONResponse(content={"message": "廣告不存在"}, status_code=404)
    ad.url = data.url
    db.commit()
    return ad

@router.put("/{ad_id}/icon")
def update_ad_icon(ad_id: int, icon: UploadFile, user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        return JSONResponse(content={"message": "廣告不存在"}, status_code=404)
    if icon.content_type != "image/jpeg" and icon.content_type != "image/png" and icon.content_type != "image/gif":
        return JSONResponse(content={"message": "只接受.jpeg和.png檔案"}, status_code=400)
    if icon.size > 2048 * 2048:
        return JSONResponse(content={"message": "廣告圖標大小請勿超過4MB"}, status_code=400)
    icon.file.seek(0)
    filename = str(uuid.uuid4())
    if icon.content_type == "image/jpeg":
        filename = filename + ".jpg"
    elif icon.content_type == "image/png":
        filename = filename + ".png"
    with open(f"static/{filename}", "wb") as image:
        image.write(icon.file.read())
    ad.icon = filename
    db.commit()
    return Response(content=None, status_code=204)

@router.delete("/{ad_id}", response_model=AdSchema)
def delete_ad(ad_id: int, user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        return JSONResponse(content={"message": "廣告不存在"}, status_code=404)
    db.delete(ad)
    db.commit()
    return ad