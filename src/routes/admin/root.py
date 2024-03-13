from fastapi.routing import APIRouter

from . import district, city


router = APIRouter(prefix="/admin")
router.include_router(district.router)
router.include_router(city.router)