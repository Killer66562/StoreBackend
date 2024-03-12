from fastapi.responses import JSONResponse
import uvicorn

from fastapi import Depends, FastAPI

from sqlalchemy.orm import Session
from sqlalchemy import or_
from dependencies import get_db, get_password_hash

from routes import user

from models import User

from schemas.general import RegisterSchema, UserSchema


app = FastAPI()
app.include_router(user.router)

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

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)