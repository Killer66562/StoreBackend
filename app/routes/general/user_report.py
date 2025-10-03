from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.models.models import User, UserReport
from app.schemas.user import CUUserReportSchema
from app.dependencies.base import  get_current_user, get_db


router = APIRouter(prefix="/user_reports")

@router.post("")
def create_user_report(data: CUUserReportSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.id == data.reported_user_id).first()
    if not user_exist:
        return JSONResponse(content={"message": f"使用者ID為{data.reported_user_id}的使用者不存在"})
    user_report = UserReport(repoter_id=user.id, **data.model_dump())
    db.add(user_report)
    db.commit()
    return user_report