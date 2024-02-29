from fastapi.routing import APIRouter

from schemas import CUOrderSchema

from models import Order


router = APIRouter(prefix="/orders")