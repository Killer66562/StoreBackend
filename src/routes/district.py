from fastapi import Depends, Response
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from models import User, District

from schemas import CUDistrictSchema, DistrictSchema

from dependencies import get_current_admin_user, get_db, get_district

from exceptions import DuplicateModelException


router = APIRouter(prefix="/districts")

@router.get("", response_model=list[DistrictSchema])
def index(db: Session = Depends(get_db)):
    return db.query(District).all()

@router.post("", response_model=DistrictSchema)
def create(data: CUDistrictSchema, user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    if db.query(District).filter(District.name == data.name, District.city_id == data.city_id).first():
        raise DuplicateModelException("name or city_id")
    district = District(**data.model_dump())
    db.add(district)
    db.commit()
    return district

@router.get("/{district_id}", response_model=DistrictSchema)
def fetch(district: District = Depends(get_district)):
    return district

@router.put("/{district_id}", response_model=DistrictSchema)
def update(data: CUDistrictSchema, user: User = Depends(get_current_admin_user), district: District = Depends(get_district), db: Session = Depends(get_db)):
    if db.query(District).filter(District.name == data.name, District.city_id == data.city_id, District.id != District.id).first():
        raise DuplicateModelException("name")
    district.name = data.name
    district.city_id = data.city_id
    db.commit()
    return district

@router.delete("/{district_id}")
def delete(user: User = Depends(get_current_admin_user), district: District = Depends(get_district), db: Session = Depends(get_db)):
    db.delete(district)
    db.commit()
    return Response(status_code=204)