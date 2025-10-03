from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.models.models import City
from app.schemas.general import FullCitySchema
from app.dependencies.base import  get_db


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