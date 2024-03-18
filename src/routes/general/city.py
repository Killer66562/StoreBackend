from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from models import City, Item

from schemas.general import FullCitySchema

from dependencies import  get_db

router = APIRouter(prefix="/cities")

@router.get("", response_model=list[FullCitySchema])
def get_all_cities(db: Session = Depends(get_db)):
    return db.query(City).order_by(City.id).all()

@router.get("/{city_id}", response_model=FullCitySchema)
def get_specfic_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    return city