import random

from fastapi import Depends
from fastapi.routing import APIRouter

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.dependencies.base import get_db
from app.schemas.general import AdSchema
from app.models.models import Ad


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