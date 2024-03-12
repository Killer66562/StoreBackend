from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
import uvicorn

from fastapi import Depends, FastAPI

from sqlalchemy.orm import Session
from sqlalchemy import or_
from dependencies import get_db, get_password_hash, authenticate_user, create_token

from routes import user as user_route
from routes import admin as admin_route

from models import User

from schemas.general import LoginSchema, RegisterSchema, TokenSchema, UserSchema


app = FastAPI()
app.include_router(user_route.router)
app.include_router(admin_route.router)

@app.get("/")
def hello():
    return {"message": "Hello, world!"}

@app.post("/register", response_model=UserSchema)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(or_(User.username == data.username, User.email == data.email)).first():
        return JSONResponse(content={"message": "重複的使用者名稱或電子郵件信箱"}, status_code=409)
    user = User(username=data.username, email=data.email, password=get_password_hash(data.password))
    db.add(user)
    db.commit()
    return user

@app.post("/login", response_model=TokenSchema)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, username=data.username, password=data.password)
    if not user:
        return JSONResponse(content={"message": "使用者名稱或密碼錯誤"}, status_code=401)
    access_token = create_token({"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=1), "for": "access"})
    refresh_token = create_token({"sub": user.username, "exp": datetime.utcnow() + timedelta(days=3600), "for": "refresh"})
    return {"access_token": access_token, "refresh_token": refresh_token}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)