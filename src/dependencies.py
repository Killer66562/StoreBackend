from typing import Annotated

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from models import Base, User, City, District, Store, Item, Order, CartItem, Comment

from exceptions import UnauthenticatedException, ModelNotFoundException, PermissionException

from settings import settings


engine = create_engine(settings.db_connection)
SessionLocal = sessionmaker(engine, autoflush=False)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        raise
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_token(data: dict):
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

def get_user_no_exc(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        used_for: str = payload.get("for")
        if not used_for:
            raise UnauthenticatedException()
        if used_for != "access":
            raise UnauthenticatedException()
        username: str = payload.get("sub")
        if not username:
            raise UnauthenticatedException()
    except JWTError:
        raise UnauthenticatedException()
    user = db.query(User).filter(User.username == username).first()
    return user

def get_current_user(user: User | None = Depends(get_user_no_exc)) -> User:
    '''
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        used_for: str = payload.get("for")
        if not used_for:
            raise UnauthenticatedException()
        if used_for != "access":
            raise UnauthenticatedException()
        username: str = payload.get("sub")
        if not username:
            raise UnauthenticatedException()
    except JWTError:
        raise UnauthenticatedException()
    user = db.query(User).filter(User.username == username).first()
    '''
    if not user:
        raise UnauthenticatedException()
    return user

def get_current_user_by_refresh_token(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        used_for: str = payload.get("for")
        if not used_for:
            raise UnauthenticatedException()
        if used_for != "refresh":
            raise UnauthenticatedException()
        username: str = payload.get("sub")
        if not username:
            raise UnauthenticatedException()
    except JWTError:
        raise UnauthenticatedException()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UnauthenticatedException()
    return user

def get_current_admin_user(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise PermissionException()
    return user

def get_obj(obj_type:type[Base], obj_id: int, db: Session):
    obj = db.query(obj_type).filter(obj_type.id == obj_id).first()
    if not obj:
        raise ModelNotFoundException(obj_type.__name__, obj_id)
    return obj

def get_city(city_id: int, db: Session = Depends(get_db)):
    return get_obj(City, city_id, db)

def get_district(district_id: int, db: Session = Depends(get_db)):
    return get_obj(District, district_id, db)

def get_store(store_id: int, db: Session = Depends(get_db)):
    return get_obj(Store, store_id, db)

def get_item(item_id: int, db: Session = Depends(get_db)):
    return get_obj(Item, item_id, db)

def get_order(order_id: int, db: Session = Depends(get_db)):
    return get_obj(Order, order_id, db)

def get_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    return get_obj(CartItem, cart_item_id, db)

def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return get_obj(Comment, comment_id, db)