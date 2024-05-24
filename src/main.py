import uvicorn

from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from fastapi import Depends, FastAPI

from sqlalchemy.orm import Session
from sqlalchemy import or_
from dependencies import get_db, get_password_hash, authenticate_user, create_token, get_current_user_by_refresh_token

from exceptions import UnauthenticatedException
from routes import user as user_route
from routes import admin as admin_route
from routes import general as general_route

from models import User

from schemas.general import LoginSchema, RegisterSchema, TokenSchema, UserSchema

from settings import settings

app = FastAPI(title=settings.app_name, description=settings.app_description, version=settings.app_version)

app.mount("/static", StaticFiles(directory="static"))

app.include_router(user_route.router)
app.include_router(admin_route.router)
app.include_router(general_route.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(UnauthenticatedException)
def unauthenciated_handler(request, exc):
    return JSONResponse(content={"message": "身分驗證失敗，請重新登入。"}, status_code=401)

@app.exception_handler(Exception)
def any_exception_handler(request, exc):
    return JSONResponse(content={"message": "伺服器錯誤，請聯繫伺服器管理員。"}, status_code=500)

@app.get("/", tags=["Hello"])
def hello():
    return {"message": "Hello, world!"}

@app.post("/register", response_model=UserSchema, tags=["Auth"])
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(or_(User.username == data.username, User.email == data.email)).first():
        return JSONResponse(content={"message": "重複的使用者名稱或電子郵件信箱"}, status_code=409)
    user = User(username=data.username, email=data.email, password=get_password_hash(data.password), birthday=data.birthday)
    db.add(user)
    db.commit()
    return user

@app.post("/login", response_model=TokenSchema, tags=["Auth"])
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, username=data.username, password=data.password)
    if not user:
        return JSONResponse(content={"message": "使用者名稱或密碼錯誤"}, status_code=401)
    access_token = create_token({"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=1), "for": "access"})
    refresh_token = create_token({"sub": user.username, "exp": datetime.utcnow() + timedelta(days=3600), "for": "refresh"})
    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/refresh", response_model=TokenSchema, tags=["Auth"])
def login(user: User = Depends(get_current_user_by_refresh_token)):
    access_token = create_token({"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=1), "for": "access"})
    refresh_token = create_token({"sub": user.username, "exp": datetime.utcnow() + timedelta(days=3600), "for": "refresh"})
    return {"access_token": access_token, "refresh_token": refresh_token}

add_pagination(app)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host=settings.app_host, port=settings.app_port)