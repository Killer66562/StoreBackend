from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from app.schemas.admin import CUDistrictSchema
from app.schemas.general import FullDistrictSchema
from app.dependencies.base import get_current_user, get_db
from app.models.models import City, District, Store, User


"""
鄉鎮市區

未來使用者創建商店時
須設定商店所在區域
"""

router = APIRouter(prefix="/districts")

@router.post("", response_model=FullDistrictSchema)
def create_district(data: CUDistrictSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    city_exist = db.query(City).filter(City.id == data.city_id).first()
    if not city_exist:
        return JSONResponse(content={"message": "城市不存在"}, status_code=400)
    district_exist = db.query(District).filter(District.name == data.name, District.city_id == data.city_id).first()
    if district_exist:
        return JSONResponse(content={"message": "該城市已存在同名區域"}, status_code=409)
    district = District(**data.model_dump())
    db.add(district)
    db.commit()
    return district

@router.put("/{district_id}", response_model=FullDistrictSchema)
def update_district(district_id: int, data: CUDistrictSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        return JSONResponse(content={"message": "區域不存在"}, status_code=400)
    city_exist = db.query(City).filter(City.id == data.city_id).first()
    if not city_exist:
        return JSONResponse(content={"message": "城市不存在"}, status_code=400)
    another_district_exist = db.query(District).filter(District.name == data.name, District.id != district_id, District.city_id == data.city_id).first()
    if another_district_exist:
        return JSONResponse(content={"message": "該城市已存在同名區域"}, status_code=409)
    district.name = data.name
    district.city_id = data.city_id
    db.commit()
    return district

@router.delete("/{district_id}")
def delete_district(district_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        return JSONResponse(content={"message": "區域不存在"}, status_code=400)
    store_in_that_district = db.query(Store).filter(Store.district_id == district_id).first()
    if store_in_that_district:
        return JSONResponse(content={"message": "無法刪除，仍有商店位於該區域中"}, status_code=400)
    db.delete(district)
    db.commit()
    return Response(status_code=204)