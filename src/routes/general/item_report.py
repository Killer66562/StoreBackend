import random
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends, Response

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from enums import ItemQueryOrderByEnum
from models import Item, Comment, ItemReport, Order, User

from schemas.general import CommentSchema, FullCommentSchema, FullItemSchema, CUCommentSchema, ItemQuerySchema

from dependencies import  get_current_user, get_db
from schemas.user import CUItemReportSchema

router = APIRouter(prefix="/item_reports")

@router.post("")
def send_report(data: CUItemReportSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == data.reported_item_id).first()
    if not item:
        return JSONResponse(content={"message": "商品不存在"}, status_code=404)
    item_report = ItemReport(**data.model_dump(), reporter_id=user.id)
    db.add(item_report)
    db.commit()