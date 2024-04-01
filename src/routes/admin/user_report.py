from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination, Page

from dependencies import get_current_user, get_db

from schemas.admin import CUDistrictSchema, UserRepoertSchema
from schemas.general import DistrictSchema

from sqlalchemy.orm import Session

from models import City, District, Store, User, UserReport


router = APIRouter(prefix="/user_reports")

@router.get("", response_model=Page[UserRepoertSchema])
def get_all_user_reports(db: Session = Depends(get_db)):
    user_reports_query = db.query(UserReport)
    return paginate(user_reports_query)

add_pagination(router)