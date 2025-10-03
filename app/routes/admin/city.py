from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from app.dependencies.base import get_current_user, get_db
from app.schemas.admin import CUCitySchema
from app.schemas.general import CitySchema
from app.models.models import City, User


router = APIRouter(prefix="/cities")

@router.post("", response_model=CitySchema, status_code=201)
def create_city(data: CUCitySchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    city_exist = db.query(City).filter(City.name == data.name).first()
    if city_exist:
        return JSONResponse(content={"message": "已存在同名的縣市"}, status_code=409)
    city = City(**data.model_dump())
    db.add(city)
    db.commit()
    return city

@router.put("/{city_id}", response_model=CitySchema, status_code=201)
def create_city(city_id: int, data: CUCitySchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        return JSONResponse(content={"message": "城市不存在"}, status_code=400)
    city_exist = db.query(City).filter(City.name == data.name, City.id != city_id).first()
    if city_exist:
        return JSONResponse(content={"message": "已存在同名的縣市"}, status_code=409)
    city.name = data.name
    db.commit()
    return city

@router.delete("/{city_id}", response_model=CitySchema, status_code=201)
def create_city(city_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        return JSONResponse(content={"message": "城市不存在"}, status_code=400)
    db.delete(city)
    db.commit()
    return Response(status_code=204)