from fastapi.routing import APIRouter

from . import district, city, user_report, item_report


router = APIRouter(prefix="/admin")

router.include_router(district.router)
router.include_router(city.router)
router.include_router(user_report.router)
router.include_router(item_report.router)