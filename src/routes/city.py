from fastapi import Depends, Response
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from models import User, City

from schemas import CUCitySchema, CitySchema

from dependencies import get_current_admin_user, get_db, get_city

from exceptions import DuplicateModelException


router = APIRouter(prefix="/cities")

@router.get("", response_model=list[CitySchema])
def index(db: Session = Depends(get_db)):
    return db.query(City).all()

@router.post("", response_model=CitySchema)
def create(data: CUCitySchema, user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    city = db.query(City).filter(City.name == data.name).first()
    if city:
        raise DuplicateModelException("name")
    city = City(**data.model_dump())
    db.add(city)
    db.commit()
    return city

@router.get("/{city_id}", response_model=CitySchema)
def fetch(city: City = Depends(get_city)):
    return city

@router.put("/{city_id}", response_model=CitySchema)
def update(data: CUCitySchema, city: City = Depends(get_city), user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    if db.query(City).filter(City.name == data.name, City.id != city.id).first():
        raise DuplicateModelException("name")
    city.name = data.name
    db.commit()
    return city

@router.delete("/{city_id}")
def delete(city: City = Depends(get_city), user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    db.delete(city)
    db.commit()
    return Response(status_code=204)