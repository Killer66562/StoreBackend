from fastapi.routing import APIRouter

from . import district, item, city


router = APIRouter(prefix="/general")
router.include_router(item.router)
router.include_router(city.router)
router.include_router(district.router)