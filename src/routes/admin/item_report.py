from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination, Page
from sqlalchemy import desc

from dependencies import get_current_user, get_db

from schemas.admin import ItemReportSchema

from sqlalchemy.orm import Session

from models import User, ItemReport


router = APIRouter(prefix="/item_reports")

@router.get("", response_model=Page[ItemReportSchema])
def get_all_item_reports(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item_reports_query = db.query(ItemReport).order_by(desc(ItemReport.id))
    return paginate(item_reports_query)

@router.get("/{item_report_id}", response_model=ItemReportSchema)
def get_item_report(item_report_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = db.query(ItemReport).filter(ItemReport.id == item_report_id).first()
    if not report:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    return report

@router.delete("/{item_report_id}")
def delete_item_report(item_report_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = db.query(ItemReport).filter(ItemReport.id == item_report_id).first()
    if not report:
        return JSONResponse(content={"message": "資源不存在"}, status_code=400)
    db.delete(report)
    db.commit()
    return Response(status_code=204)

add_pagination(router)