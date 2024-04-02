from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination, Page

from dependencies import get_current_user, get_db

from schemas.admin import UserRepoertSchema

from sqlalchemy.orm import Session

from models import User, UserReport


router = APIRouter(prefix="/user_reports")

@router.get("", response_model=Page[UserRepoertSchema])
def get_all_user_reports(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_reports_query = db.query(UserReport)
    return paginate(user_reports_query)

@router.get("/{user_report_id}", response_model=UserRepoertSchema)
def get_user_report(user_report_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = db.query(UserReport).filter(UserReport.id == user_report_id).first()
    if not report:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    return report

@router.delete("/{user_report_id}")
def delete_user_report(user_report_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = db.query(UserReport).filter(UserReport.id == user_report_id).first()
    if not report:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    db.delete(report)
    db.commit()
    return Response(status_code=204)

add_pagination(router)