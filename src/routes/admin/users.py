from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination, Page

from sqlalchemy import desc, or_

from dependencies import get_current_user, get_db

from enums import UserQuerySortByEnum

from schemas.general import UserSchema
from schemas.admin import CUUserSchema, UserQuerySchema

from sqlalchemy.orm import Session

from models import User


router = APIRouter(prefix="/users")

@router.get("", response_model=Page[UserSchema])
def admin_get_users(query: UserQuerySchema = Depends(), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users_query = db.query(User)

    print(query.sort_by)
    if query.sort_by is not None:
        if (query.sort_by == UserQuerySortByEnum.ID):
            users_query = users_query.order_by(desc(User.id) if query.desc else User.id)
        elif (query.sort_by == UserQuerySortByEnum.IS_ADMIN):
            users_query = users_query.order_by(desc(User.is_admin) if query.desc else User.is_admin)
        elif (query.sort_by == UserQuerySortByEnum.USERNAME):
            users_query = users_query.order_by(desc(User.username) if query.desc else User.username)
        elif (query.sort_by == UserQuerySortByEnum.EMAIL):
            users_query = users_query.order_by(desc(User.email) if query.desc else User.email)
        elif (query.sort_by == UserQuerySortByEnum.BIRTHDAY):
            users_query = users_query.order_by(desc(User.birthday) if query.desc else User.birthday)
        elif (query.sort_by == UserQuerySortByEnum.CREATED_AT):
            users_query = users_query.order_by(desc(User.created_at) if query.desc else User.created_at)
        else:
            users_query = users_query.order_by(User.id)
    else:
        users_query = users_query.order_by(User.id)
        
    if query.is_admin is not None:
        users_query = users_query.filter(User.is_admin == query.is_admin)

    if query.birthday_start is not None:
        users_query = users_query.filter(User.birthday >= query.birthday_start)

    if query.birthday_end is not None:
        users_query = users_query.filter(User.birthday <= query.birthday_end)

    if query.created_at_start is not None:
        users_query = users_query.filter(User.birthday >= query.created_at_start)

    if query.created_at_end is not None:
        users_query = users_query.filter(User.birthday <= query.created_at_end)

    if query.username is not None:
        query_username_splited = query.username.split("|")
        users_query = users_query.filter(or_(*[
            User.username.like(f"%{username.replace('*', '')}%") if (username.startswith("*") and username.endswith("*")) else \
            User.username.like(f"%{username.replace('*', '')}") if username.startswith("*") else \
            User.username.like(f"{username.replace('*', '')}%") if username.endswith("*") else \
            User.username == username for username in query_username_splited]
        ))

    if query.email is not None:
        query_email_splited = query.email.split("|")
        users_query = users_query.filter(or_(*[
            User.email.like(f"%{email.replace("*", "")}%") if email.startswith("*") and email.endswith("*") else \
            User.email.like(f"%{email.replace("*", "")}") if email.startswith("*") else \
            User.email.like(f"{email.replace("*", "")}%") if email.endswith("*") else \
            User.email == email for email in query_email_splited
        ]))

    return paginate(users_query)

@router.put("/{user_id}", response_model=UserSchema)
def admin_update_user(user_id:int, data: CUUserSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(content={"message": "使用者不存在"}, status_code=404)
    user.is_admin = data.is_admin
    db.commit()
    return user

@router.delete("/{user_id}")
def admin_delete_user(user_id:int, data: CUUserSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(content={"message": "使用者不存在"}, status_code=404)
    db.delete(user)
    db.commit()
    return Response(status_code=204)

add_pagination(router)