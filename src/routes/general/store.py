from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from models import Store

from schemas.general import FullStoreSchema

from dependencies import  get_db


router = APIRouter(prefix="/stores")

@router.get("/{store_id}", response_model=FullStoreSchema)
def get_specific_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        return JSONResponse(content={"message": "資源不存在"}, status_code=404)
    return store