from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.models.models import District
from app.schemas.general import FullDistrictSchema
from app.dependencies.base import  get_db


router = APIRouter(prefix="/districts")

@router.get("", response_model=list[FullDistrictSchema])
def get_all_cities(db: Session = Depends(get_db)):
    return db.query(District).order_by(District.id).all()

@router.get("/{district_id}", response_model=FullDistrictSchema)
def get_specfic_city(district_id: int, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    return district