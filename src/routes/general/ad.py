import random

from fastapi import Depends, Response, UploadFile
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy import desc

from dependencies import get_current_admin_user, get_current_user, get_db

from schemas.admin import CUAdSchema, CUCitySchema
from schemas.general import AdSchema, CitySchema

from sqlalchemy.orm import Session

from models import City, District, Store, User, Ad


router = APIRouter(prefix="/ads")

@router.get("", response_model=list[AdSchema])
def get_ads(db: Session = Depends(get_db)):
    ads = db.query(Ad).order_by(desc(Ad.id)).limit(10000).all()
    ads_len = len(ads)
    random.shuffle(ads)
    if ads_len >= 20:
        selected_ads = random.sample(population=ads, k=20)
    else:
        selected_ads = ads
    return selected_ads