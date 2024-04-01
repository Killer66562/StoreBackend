from fastapi.routing import APIRouter

from . import district, city, user_report


router = APIRouter(prefix="/admin")
router.include_router(district.router)
router.include_router(city.router)
router.include_router(user_report.router)