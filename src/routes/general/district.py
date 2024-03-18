from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from models import District

from schemas.general import FullCitySchema

from dependencies import  get_db

router = APIRouter(prefix="/districts")

@router.get("", response_model=list[FullCitySchema])
def get_all_cities(db: Session = Depends(get_db)):
    return db.query(District).order_by(District.id).all()

@router.get("/{district_id}", response_model=FullCitySchema)
def get_specfic_city(district_id: int, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    return district