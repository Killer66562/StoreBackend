import asyncio
import random
import uuid
import uvicorn

from datetime import datetime, timedelta

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi_pagination import add_pagination

from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig

from fastapi import Depends, FastAPI, BackgroundTasks, Response

from sqlalchemy.orm import Session
from sqlalchemy import or_
from dependencies import get_db, get_password_hash, authenticate_user, create_token, get_current_user_by_refresh_token

from exceptions import UnauthenticatedException
from routes import user as user_route
from routes import admin as admin_route
from routes import general as general_route

from models import User, Verification

from schemas.general import CUForgetPwSchema, ForgetPwCodeConfirmSchema, LoginSchema, RegisterSchema, TokenSchema, UserSchema

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

mail_conf = ConnectionConfig(
    MAIL_USERNAME = settings.mail_username,
    MAIL_PASSWORD = settings.mail_password,
    MAIL_FROM = settings.mail_from,
    MAIL_PORT = settings.mail_port,
    MAIL_SERVER = settings.mail_server,
    MAIL_FROM_NAME = settings.mail_from_name,
    MAIL_STARTTLS = settings.mail_starttls,
    MAIL_SSL_TLS = settings.mail_ssl_tls,
    USE_CREDENTIALS = settings.mail_use_credentials,
    VALIDATE_CERTS = settings.mail_validate_certs
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

def send_mail(message: MessageSchema):
    fm = FastMail(mail_conf)
    asyncio.run(fm.send_message(message=message))

@app.post("/forget_password")
def forget_password(data: CUForgetPwSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.email == data.email).first()
    if not user_exist:
        return JSONResponse(content={"message": "使用者不存在"}, status_code=404)
    
    verification_code = uuid.uuid4().hex
    verification = db.query(Verification).filter(Verification.user_id == user_exist.id).first()

    current_time = datetime.now()
    if verification is not None:
        verification.code = verification_code
        verification.last_request = current_time
    else:
        verification = Verification(user_id=user_exist.id, code=verification_code, last_request=current_time)
        db.add(verification)
        
    message = MessageSchema(
        subject="重設密碼",
        recipients=[user_exist.email],
        body=f"你的重設密碼代碼為{verification_code}",
        subtype=MessageType.plain,
    )

    db.commit()

    background_tasks.add_task(send_mail, message)
    return Response(status_code=204)

@app.post("/forget_password_code_confirm")
def forget_password_code_confirm(data: ForgetPwCodeConfirmSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    verification = db.query(Verification).filter(Verification.code == data.code).first()
    if not verification:
        return JSONResponse(content={"message": "驗證碼錯誤"}, status_code=400)
    if datetime.now() - verification.last_request >= timedelta(minutes=5):
        return JSONResponse(content={"message": "請求超時，請重新生成一個重設密碼代碼。"}, status_code=400)

    chars = [*[chr(_) for _ in range(48, 58)], *[chr(_) for _ in range(65, 91)], *[chr(_) for _ in range(97, 123)]]
    new_password = "".join(random.choices(population=chars, k=20))

    verification.user.password = get_password_hash(new_password)

    db.delete(verification)
    db.commit()

    message = MessageSchema(
        subject="密碼已重設",
        recipients=[verification.user.email],
        body=f"你的新密碼為{new_password}，請盡快再次登入並修改密碼。",
        subtype=MessageType.plain,
    )

    background_tasks.add_task(send_mail, message)
    return Response(status_code=204)

add_pagination(app)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host=settings.app_host, port=settings.app_port, ssl_certfile=settings.ssl_certfile, ssl_keyfile=settings.ssl_keyfile)